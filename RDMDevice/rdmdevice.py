from uuid import uuid4
from threading import Thread, Timer
import socket
import asyncio
import ipaddress
from RDM import gethandlers, pids, nackcodes, sensors, rdmpacket, defines
from LLRP import asyncllrp
from RDMNet import pdus, vectors, brokerhandlers
from RDMDevice import devicedescriptor


class rdmdevice(Thread):
    """Creates a dummy RDM device

    This class creates a dummy RDM fixture with it's own UID, CID, PIDs. 
    This is designed to be used in conjunction with the DummyArtRDM and 
    DummyRDMNet classes to function as a set of test devices. The LLRP
    responder is built into the rdmdevice class

    """

    desc = devicedescriptor.DeviceDescriptor()
    desc.sensors = [sensors.dummysensor("Sensor 1", -100, 100, -50, 50, defines.Sens_temperature,
    cid.extend(uuid4().bytes[2:])
    uid = cid[:6]

    label = "D5 RDMNet Test Device"
    mfr = "D5 Systems"
    model = "Test Device"
    softwareverslabel = "0.01 Alpha"
    category = 0x7101
    factorystatus = 1
    identifystatus = 1
    sensors = [sensors.dummysensor("Sensor 1", -100, 100, -50, 50, defines.Sens_temperature,
                                   defines.Sens_unit_centigrade, defines.Prefix_none)
               , sensors.dummysensor("Sensor 2", -100, 100, -50, 50, defines.Sens_temperature,
                                     defines.Sens_unit_centigrade, defines.Prefix_none)
               , sensors.dummysensor("Sensor 3", -100, 100, -50, 50, defines.Sens_temperature,
                                     defines.Sens_unit_centigrade, defines.Prefix_none)]

    currentpers = 0
    desc.perslist = {
        "Sample Personality": 4,
        "Another Personality": 8,
    }

    desc.dmxaddress = 1
    desc.dmxfootprint = 4
    desc.lamphours = 1
    desc.lampstrikes = 1
    desc.devhours = 1
    desc.powercycles = 1
    
    #LLRP/RDMNet Details
    desc.hwaddr = ""
    desc.devtype = 0
    desc.brokerip = ""
    desc.searchdomain = ".local"
    desc.scope = "default"

    # These dicts contains lists of device supported PIDS

    #llrpswitcher contains PIDs that are supported by both LLRP and Art/RDMNet targets
    desc.llrpswitcher = {
        pids.RDM_device_info: gethandlers.devinfo,
        pids.RDM_reset_device: gethandlers.devreset,
        pids.RDM_factory_defaults: gethandlers.devfactory,
        pids.RDM_device_label: gethandlers.devlabel,
        pids.RDM_manufacturer_label: gethandlers.devmanufacturer,
        pids.RDM_device_model_description: gethandlers.devmodel,
        pids.RDM_identify: gethandlers.devidentify,
        #Lock State
        #Lock State Description
        pids.E133_component_scope: gethandlers.devscope,
        pids.E133_search_domain: gethandlers.devsearch,
        #E133 tcp comms status
        #E133 Broker Status
        #E137-2 Messages as appropriate
    }

    #getswitcher contains PIDs that are supported by ONLY Art/RDMNet targets
    desc.getswitcher = {
        pids.RDM_software_version_label: gethandlers.devsoftwareversion,
        pids.RDM_dmx_start_address: gethandlers.dmxaddress,
        pids.RDM_device_hours: gethandlers.devhours,
        pids.RDM_lamp_hours: gethandlers.lamphours,
        pids.RDM_lamp_strikes: gethandlers.lampstrikes,
        pids.RDM_device_power_cycles: gethandlers.powercycles,
        pids.RDM_supported_parameters: gethandlers.supportedpids,
        pids.RDM_sensor_definition: gethandlers.sensordef,
        pids.RDM_sensor_value: gethandlers.sensorval,
        #Personalities
        #
    }

    def __init__(self):
        super().__init__()
        try:
            self.brokersocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error:
            print("Error opening RDMNet Socket")
        self.llrpsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.llrpsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.llrpsocket.bind(('0.0.0.0', llrp.llrpport))
        self.llrpsocket.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_IF,
                                   socket.inet_aton('192.168.3.2'))
        mreq = struct.pack("4s4s", socket.inet_aton(llrp.llrp_multicast_v4_request),
                           socket.inet_aton('192.168.3.2'))
        self.llrpsocket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        self.tcptimer = Timer(15, self.sendtcpheartbeat)
        print("LLRP Listening")

    def run(self):
        asyncio.run(self.main())
            data, = self.llrpsocket.recvfrom(1024)
            llrp.handlellrp(self, data)

    async def main(self):
        await asyncio.gather(self.sendtcpheartbeat(), self.llrpmain(), self.identify())

    async def llrpmain(self):
        loop = asyncio.get_running_loop()
        protocol = await asyncllrp.listenllrp(self, loop, '192.168.3.2', self.desc)

    def getpid(self, pid, recpdu) -> rdmpacket.RDMpacket:
        """Checks to see if either the LLRP PIDS or the RDM-only PIDS contains the
        requested PID. If they do, an RDM PDU is returned to the requesting
        engine, to be sent out from there. Used by Art-Net and RDMNet responders"""

        func = self.desc.llrpswitcher.get(pid, "NACK")  
        if func is "NACK":
            func = self.desc.getswitcher.get(pid, "NACK")
        if func is not "NACK":
            return func(self, recpdu)
        else:
            return gethandlers.nackreturn(self, recpdu, nackcodes.nack_unknown)

    def newbroker(self, desc):
        if self.desc.scope == desc.scope:
            brokeraddress = ipaddress.ip_address(desc.address)
            try:
                self.brokersocket.connect((brokeraddress.compressed, desc.port))
            except socket.error as e:
                print("Error connecting to broker {}: {}".format(desc.hostname, e))
            try:
                packet = pdus.ACNTCPPreamble()

                rlppacket = pdus.RLPPDU(vectors.vector_root_broker, self.cid)
                
                clientpacket = pdus.ClientConnect(self.scope, self.searchdomain)
                clientpacket.vector = vectors.vector_broker_connect
                cliententry = pdus.ClientEntry()
                cliententry.UID = self.uid
                cliententry.CID = self.cid
                cliententry.vector = vectors.vector_root_rpt
                
                packet.message = rlppacket
                rlppacket.message = clientpacket
                clientpacket.message = cliententry
                retval = packet.serialise()
                self.brokersocket.send(retval)
            except socket.error as e:
                print("Error sending init_connect packet: {}".format(e))
            self.tcptimer.start()

    def disconnectbroker(self, desc):
        if self.scope == desc.scope:
            self.brokersocket.shutdown()
            self.brokersocket.close()

    async def identify(self):
        while True:
            if self.desc.identifystatus is 0x01:
                print("Annoying Identify Pattern")
            await asyncio.sleep(1)

    async def sendtcpheartbeat(self):
        while True:
            print("Would be TCP hearbeat")
            if self.brokerconnected:
                packet = pdus.ACNTCPPreamble()

                rlppacket = pdus.RLPPDU(vectors.vector_root_broker, self.desc.cid)

                nullpacket = pdus.BrokerNull()

                packet.message = rlppacket

                rlppacket.message = nullpacket

                retval = packet.serialise()

                try:
                    self.brokersocket.send(retval)
                except socket.error as e:
                    print("Error sending hearbeat packet: {}".format(e))
            await asyncio.sleep(15)

    def handlerdmnet(self, data):
        if data[0:12] is not vectors.ACNheader:
            print("Incorrect ACN Header")
            return
        if data[12:16] != len(data[16:]):
            print("Preamble length incorrect")
            return