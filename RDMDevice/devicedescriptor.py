from uuid import uuid4
class DeviceDescriptor:
    def __init__(self):
        # These parameters are to define the basic features for the device
        self.cid = bytearray(b'\xD5\xD5')
        self.cid.extend(uuid4().bytes[2:])
        self.uid = self.cid[:6]

        self.label = "D5 RDMNet Test Device"
        self.mfr = "D5 Systems"
        self.model = "Test Device"
        self.softwareverslabel = "0.01 Alpha"
        self.category = 0x7101
        self.factorystatus = 1
        self.identifystatus = 0
        self.sensors = list()

        self.currentpers = 0
        self.perslist = dict()

        self.dmxaddress = 1
        self.dmxfootprint = 4
        self.lamphours = 1
        self.lampstrikes = 1
        self.devhours = 1
        self.powercycles = 1
        
        #LLRP/RDMNet Details
        self.hwaddr = ""
        self.devtype = 0
        self.brokerip = ""
        self.searchdomain = ".local"
        self.scope = "default"

        # These dicts contains lists of device supported PIDS

        #llrpswitcher contains PIDs that are supported by both LLRP and Art/RDMNet targets
        self.llrpswitcher = dict()

        #getswitcher contains PIDs that are supported by ONLY Art/RDMNet targets
        self.getswitcher = dict()
