from uuid import uuid4
from threading import Thread, Timer
import socket
import struct
from RDM import gethandlers, pids, nackcodes, sensors, rdmpacket, defines
from LLRP import llrp


class rdmdevice(Thread):
    """Creates a dummy RDM device

    This class creates a dummy RDM fixture with it's own UID, CID, PIDs. 
    This is designed to be used in conjunction with the DummyArtRDM and 
    DummyRDMNet classes to function as a set of test devices. The LLRP
    responder is built into the rdmdevice class

    """

    # These parameters are to define the basic features for the device
    cid = bytearray(b'\xD5\xD5')
    cid.extend(uuid4().bytes[2:])
    uid = cid[:6]

    label = "D5 RDMNet Test Device"
    mfr = "D5 Systems"
    model = "Test Device"
    devlabel = "Device ID"
    softwareverslabel = "0.01 Alpha"
    category = 0x7101
    factorystatus = 1
    identifystatus = 1
    sensors = [sensors.dummysensor("Sensor 1", -100, 100, -50, 50, defines.Sens_temperature, defines.Sens_unit_centigrade, defines.Prefix_none)
    , sensors.dummysensor("Sensor 2", -100, 100, -50, 50, defines.Sens_temperature, defines.Sens_unit_centigrade, defines.Prefix_none)
    , sensors.dummysensor("Sensor 3", -100, 100, -50, 50, defines.Sens_temperature, defines.Sens_unit_centigrade, defines.Prefix_none)]

    currentpers = 0
    perslist = {
        "Sample Personality": 4,
        "Another Personality": 8,
    }

    dmxaddress = 1
    dmxfootprint = 4
    lamphours = 1
    lampstrikes = 1
    devhours = 1
    powercycles = 1
    
    #LLRP/RDMNet Details
    hwaddr = ""
    devtype = 0
    brokerip = ""
    searchdomain = ".local"
    scope = "default"

    # These dicts contains lists of device supported PIDS

    #llrpswitcher contains PIDs that are supported by both LLRP and Art/RDMNet targets
    llrpswitcher = {
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
    getswitcher = {
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
        self.llrpsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.llrpsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.llrpsocket.bind(('0.0.0.0', llrp.llrpport))
        self.llrpsocket.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_IF, socket.inet_aton('192.168.1.195'))
        mreq = struct.pack("4s4s", socket.inet_aton(llrp.llrp_multicast_v4_request), socket.inet_aton('192.168.1.195'))
        self.llrpsocket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        print("LLRP Listening")

    def run(self):
        while True:
            data, addr = self.llrpsocket.recvfrom(1024)
            llrp.handlellrp(self, data)

    def getpid(self, pid, recpdu) -> rdmpacket.RDMpacket:
        """Checks to see if either the LLRP PIDS or the RDM-only PIDS contains the
        requested PID. If they do, an RDM PDU is returned to the requesting
        engine, to be sent out from there. Used by Art-Net and RDMNet responders"""

        func = self.llrpswitcher.get(pid, "NACK")  
        if func is "NACK":
            func = self.getswitcher.get(pid, "NACK")
        if func is not "NACK":
            return func(self, recpdu)
        else:
            return gethandlers.nackreturn(self, recpdu, nackcodes.nack_unknown)
       
