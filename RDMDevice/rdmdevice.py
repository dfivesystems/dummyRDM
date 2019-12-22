from uuid import uuid4
from threading import Thread
import socket
import struct
from RDM import gethandlers, sethandlers, pids, nackcodes, sensors
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
    sensors = []

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
    pidlist = [0x0060, 0x00c0, 0x00F0, 0x1000, ]
    llrppidlist = {
        pids.RDM_device_info: "Device Info",
        pids.RDM_manufacturer_label: "Device Manufacturer",
        pids.RDM_device_model_description: "Device Model",
        pids.E133_component_scope: "Scope",
        pids.E133_search_domain: "Search Domain",
        pids.RDM_reset_device: "Device Reset",
        pids.RDM_factory_defaults: "Factory Reset",
        pids.RDM_device_label: "Device Label",
        pids.RDM_identify: "Identify",
    }

    getswitcher = {
            pids.RDM_device_info: gethandlers.devinfo,
            pids.RDM_software_version_label: gethandlers.devsoftwareversion,
            pids.RDM_manufacturer_label: gethandlers.devmanufacturer,
            pids.RDM_device_model_description: gethandlers.devmodel,
            pids.RDM_device_label: gethandlers.devlabel,
            pids.RDM_dmx_start_address: gethandlers.dmxaddress,#DMX Start Address
            pids.RDM_device_hours: gethandlers.devhours,
            pids.RDM_lamp_hours: gethandlers.lamphours,
            pids.RDM_lamp_strikes: gethandlers.lampstrikes,
            pids.RDM_device_power_cycles: gethandlers.powercycles,
            pids.RDM_supported_parameters: gethandlers.supportedpids,

            # pids.RDM_identify: None,#Identify
    }

    def __init__(self):
        super().__init__()
        self.llrpsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.llrpsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.llrpsocket.bind(("0.0.0.0", llrp.llrpport))
        mreq = struct.pack("4sl", socket.inet_aton(llrp.llrp_multicast_v4_request), socket.INADDR_ANY)
        self.llrpsocket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        print("LLRP Listening")

    def run(self):
        while True:
            data, addr = self.llrpsocket.recvfrom(1024)
            llrp.handlellrp(self, data)

    def getpid(self, pid, recpdu):
        func = self.getswitcher.get(pid, "NACK")
        if func is not "NACK":
            return func(self, recpdu)
        else:
            return gethandlers.nackreturn(self, pid, nackcodes.nack_unknown, recpdu)

       



