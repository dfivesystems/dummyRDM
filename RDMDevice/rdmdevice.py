from threading import Thread, current_thread
import socket
import asyncio
import ipaddress
from RDM import gethandlers, pids, nackcodes, sensors, rdmpacket, defines
from LLRP import asyncllrp
from RDMNet import asyncrdmnet
from RDMDevice import devicedescriptor


class RdmDevice(Thread):
    """Creates a dummy RDM device

    This class creates a dummy RDM fixture with it's own UID, CID, PIDs.
    This is designed to be used in conjunction with the DummyArtRDM and
    DummyRDMNet classes to function as a set of test devices. The LLRP
    responder is built into the rdmdevice class

    """

    device_descriptor = devicedescriptor.DeviceDescriptor()
    device_descriptor.sensors = [sensors.dummysensor("Sensor 1", -100, 100, -50, 50, defines.Sens_temperature,
                                   defines.Sens_unit_centigrade, defines.Prefix_none)
               , sensors.dummysensor("Sensor 2", -100, 100, -50, 50, defines.Sens_temperature,
                                     defines.Sens_unit_centigrade, defines.Prefix_none)
               , sensors.dummysensor("Sensor 3", -100, 100, -50, 50, defines.Sens_temperature,
                                     defines.Sens_unit_centigrade, defines.Prefix_none)]

    currentpers = 0
    device_descriptor.perslist = {
        "Sample Personality": 4,
        "Another Personality": 8,
    }

    device_descriptor.dmxaddress = 1
    device_descriptor.dmxfootprint = 4
    device_descriptor.lamphours = 1
    device_descriptor.lampstrikes = 1
    device_descriptor.devhours = 1
    device_descriptor.powercycles = 1
    
    #LLRP/RDMNet Details
    device_descriptor.hwaddr = ""
    device_descriptor.devtype = 0
    device_descriptor.brokerip = ""
    device_descriptor.searchdomain = ".local"
    device_descriptor.scope = "default"

    # These dicts contains lists of device supported PIDS

    #llrpswitcher contains PIDs that are supported by both LLRP and Art/RDMNet targets
    device_descriptor.llrpswitcher = {
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
    device_descriptor.getswitcher = {
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
        #Queued Message
        #Status Message
    }

    def __init__(self):
        super().__init__()
        current_thread().name = "RDM Device"
        self.loop = None

    def run(self):
        asyncio.run(self.main())

    async def main(self):
        self.loop = asyncio.get_running_loop()
        await asyncio.gather(self.llrpmain(), self.identify())

    async def llrpmain(self):
        loop = asyncio.get_running_loop()
        protocol = await asyncllrp.listenllrp(self, loop, '192.168.3.1', self.device_descriptor)

    def getpid(self, pid, recpdu) -> rdmpacket.RDMpacket:
        """Checks to see if either the LLRP PIDS or the RDM-only PIDS contains the
        requested PID. If they do, an RDM PDU is returned to the requesting
        engine, to be sent out from there. Used by Art-Net and RDMNet responders"""

        func = self.device_descriptor.llrpswitcher.get(pid, "NACK")  
        if func is "NACK":
            func = self.device_descriptor.getswitcher.get(pid, "NACK")
        if func is not "NACK":
            return func(self, recpdu)
        else:
            return gethandlers.nackreturn(self, recpdu, nackcodes.nack_unknown)

    def newbroker(self, broker_descriptor):
        self.rdmnet = asyncio.run_coroutine_threadsafe(asyncrdmnet.listenRDMNet(self, self.device_descriptor, broker_descriptor), self.loop)

    def disconnectbroker(self):
        self.rdmnet.cancel()

    async def identify(self):
        while True:
            if self.device_descriptor.identifystatus is 0x01:
                print("Annoying Identify Pattern")
            await asyncio.sleep(1)

