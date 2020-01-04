from RDM import checksums, rdmpacket, defines, nackcodes
from struct import unpack, pack 
#TODO: Check any PIDs that return strings return without padding spaces
#TODO: Personality Descriptions, Parameter Description, Sensors

def devreset(self, recpdu: rdmpacket.RDMpacket) -> rdmpacket.RDMpacket:
    """Performs a simulated hot/cold reset on the device
    RDM_GET = no
    RDM_SET = yes
    """

    if recpdu.cc == defines.CC_Set_command:
        if recpdu.pd[0] == 0x01:
            #Warm Reset
            print("Device {}: Warm reset requested").format(self.uid.hex())
        elif recpdu[1] == 0xFF:
            #Cold Reset
            print("Device {}: Cold reset requested").format(self.uid.hex())
        else:
            #Out of range NACK
            return nackreturn(self, recpdu, nackcodes.nack_data_range)
        sendpdu = rdmpacket.RDMpacket()
        sendpdu.length = 24
        sendpdu.destuid = recpdu.srcuid
        sendpdu.srcuid = self.uid
        sendpdu.tn = recpdu.tn
        sendpdu.port_resp = 0x00
        sendpdu.mess_cnt = 0x00
        sendpdu.sub_id = 0x0000
        sendpdu.cc = defines.CC_Set_command_resp
        sendpdu.pid = recpdu.pid
        sendpdu.pdl = 0
        sendpdu.calcchecksum()
        return sendpdu
    else:
        return nackreturn(self, recpdu, nackcodes.nack_unsupported_cc)

def devfactory(self, recpdu: rdmpacket.RDMpacket) -> rdmpacket.RDMpacket:
    """Either sets the device to factory defaults or gets if the device is 
    currently set to factory defaults
    RDM_GET = yes
    RDM_SET = yes
    """

    if recpdu.cc == defines.CC_Get_command:
        sendpdu = rdmpacket.RDMpacket()
        sendpdu.length = 25
        sendpdu.destuid = recpdu.srcuid
        sendpdu.srcuid = self.uid
        sendpdu.tn = recpdu.tn
        sendpdu.port_resp = 0x00
        sendpdu.mess_cnt = 0x00
        sendpdu.sub_id = 0x0000
        sendpdu.cc = defines.CC_Get_command_resp
        sendpdu.pid = recpdu.pid
        sendpdu.pdl = 1
        sendpdu.pd = self.factorystatus.to_bytes(1, 'big')
        sendpdu.calcchecksum()
        return sendpdu
    elif recpdu.cc == defines.CC_Set_command:
        if recpdu.pd[0] <= 1:
            print("Device {}: Factory Reset set to {:02x}").format(self.uid.hex(), recpdu.pd[0])
            sendpdu = rdmpacket.RDMpacket()
            sendpdu.length = 24
            sendpdu.destuid = recpdu.srcuid
            sendpdu.srcuid = self.uid
            sendpdu.tn = recpdu.tn
            sendpdu.port_resp = 0x00
            sendpdu.mess_cnt = 0x00
            sendpdu.sub_id = 0x0000
            sendpdu.cc = defines.CC_Set_command_resp
            sendpdu.pid = recpdu.pid
            sendpdu.pdl = 0
            sendpdu.calcchecksum()
            return sendpdu
        else:
            #Out of range NACK
            return nackreturn(self, recpdu, nackcodes.nack_data_range)
    else:
        return nackreturn(self, recpdu, nackcodes.nack_unsupported_cc)

def devidentify(self, recpdu: rdmpacket.RDMpacket) -> rdmpacket.RDMpacket:
    """Either sets the device identify status or returns the device identify
    status to the requesting controller
    RDM_GET = yes
    RDM_SET = no
    """

    if recpdu.cc == defines.CC_Get_command:
        sendpdu = rdmpacket.RDMpacket()
        sendpdu.length = 25
        sendpdu.destuid = recpdu.srcuid
        sendpdu.srcuid = self.uid
        sendpdu.tn = recpdu.tn
        sendpdu.port_resp = 0x00
        sendpdu.mess_cnt = 0x00
        sendpdu.sub_id = 0x0000
        sendpdu.cc = defines.CC_Get_command_resp
        sendpdu.pid = recpdu.pid
        sendpdu.pdl = 1
        sendpdu.pd = self.identifystatus.to_bytes(1, 'big')
        sendpdu.calcchecksum()
        return sendpdu
    elif recpdu.cc == defines.CC_Set_command:
        if recpdu.pd[0] <= 1:
            print("Device {}: Identify set to {:02x}").format(self.uid.hex(), recpdu.pd[0])
            sendpdu = rdmpacket.RDMpacket()
            sendpdu.length = 24
            sendpdu.destuid = recpdu.srcuid
            sendpdu.srcuid = self.uid
            sendpdu.tn = recpdu.tn
            sendpdu.port_resp = 0x00
            sendpdu.mess_cnt = 0x00
            sendpdu.sub_id = 0x0000
            sendpdu.cc = defines.CC_Set_command_resp
            sendpdu.pid = recpdu.pid
            sendpdu.pdl = 0
            sendpdu.calcchecksum()
            return sendpdu
        else:
            #Out of range NACK
            return nackreturn(self, recpdu, nackcodes.nack_data_range)
    else:
        return nackreturn(self, recpdu, nackcodes.nack_unsupported_cc)

def devinfo(self, recpdu: rdmpacket.RDMpacket) -> rdmpacket.RDMpacket:
    """Returns an device info rdmpacket for the given device
    RDM_GET = yes
    RDM_SET = no
    """

    if recpdu.cc is not defines.CC_Get_command:
        return nackreturn(self, recpdu, nackcodes.nack_unsupported_cc)
    sendpdu = rdmpacket.RDMpacket()
    sendpdu.length = 0x2b
    sendpdu.destuid = recpdu.srcuid
    sendpdu.srcuid = self.uid
    sendpdu.tn = recpdu.tn
    sendpdu.port_resp = 0x00
    sendpdu.mess_cnt = 0x00
    sendpdu.sub_id = 0x0000
    sendpdu.cc = 0x21
    sendpdu.pid = 0x0060
    sendpdu.pdl = 0x13
    # 16-bit Protocol Version
    sendpdu.pd.extend(b'\x01\x00')
    # Model ID
    sendpdu.pd.extend(b'\x01\x02')
    # Category
    sendpdu.pd.extend(b'\x71\x01')
    # Software Version
    sendpdu.pd.extend(b'\x01\x02\x03\x04')
    # DMX Footprint
    sendpdu.pd.extend(self.dmxfootprint.to_bytes(2, 'big'))
    # DMX Personality
    sendpdu.pd.extend(self.currentpers.to_bytes(1, 'big'))
    perslen = len(self.perslist)+1
    sendpdu.pd.extend(perslen.to_bytes(1, 'big'))
    # DMX Start Address
    sendpdu.pd.extend(self.dmxaddress.to_bytes(2, 'big'))
    # Sub Device Count
    sendpdu.pd.extend(b'\x00\x00')
    # Sensor Count
    sendpdu.pd.extend(len(self.sensors).to_bytes(1, 'big'))
    sendpdu.calcchecksum()
    return sendpdu

def devsoftwareversion(self, recpdu: rdmpacket.RDMpacket) -> rdmpacket.RDMpacket:
    """Returns a Device Software Version rdmpacket for the given device
    RDM_GET = yes
    RDM_SET = no
    """

    if recpdu.cc is not defines.CC_Get_command:
        return nackreturn(self, recpdu, nackcodes.nack_unsupported_cc)
    sendpdu = rdmpacket.RDMpacket()
    sendpdu.length = 0x38
    sendpdu.destuid = recpdu.srcuid
    sendpdu.srcuid = self.uid
    sendpdu.tn = recpdu.tn
    sendpdu.port_resp = 0x00
    sendpdu.mess_cnt = 0x00
    sendpdu.sub_id = 0x0000
    sendpdu.cc = 0x21
    sendpdu.pid = 0x00C0
    sendpdu.pdl = 32
    sendpdu.pd = (bytes('{:<32}'.format(self.softwareverslabel), 'utf8'))
    sendpdu.calcchecksum()
    return sendpdu

def devmanufacturer(self, recpdu: rdmpacket.RDMpacket) -> rdmpacket.RDMpacket:
    """Returns a Device Manufacturer rdmpacket for the given device
    RDM_GET = yes
    RDM_SET = no
    """

    if recpdu.cc is not defines.CC_Get_command:
        return nackreturn(self, recpdu, nackcodes.nack_unsupported_cc)
    sendpdu = rdmpacket.RDMpacket()
    sendpdu.length = 0x38
    sendpdu.destuid = recpdu.srcuid
    sendpdu.srcuid = self.uid
    sendpdu.tn = recpdu.tn
    sendpdu.port_resp = 0x00
    sendpdu.mess_cnt = 0x00
    sendpdu.sub_id = 0x0000
    sendpdu.cc = 0x21
    sendpdu.pid = 0x0081
    sendpdu.pdl = 32
    sendpdu.pd = (bytes('{:<32}'.format(self.mfr), 'utf8'))
    sendpdu.calcchecksum()
    return sendpdu

def devmodel(self, recpdu: rdmpacket.RDMpacket) -> rdmpacket.RDMpacket:
    """Returns a Device Model Description rdmpacket for the given device
    RDM_GET = yes
    RDM_SET = no
    """

    if recpdu.cc is not defines.CC_Get_command:
        return nackreturn(self, recpdu, nackcodes.nack_unsupported_cc)
    sendpdu = rdmpacket.RDMpacket()
    sendpdu.length = 0x38
    sendpdu.destuid = recpdu.srcuid
    sendpdu.srcuid = self.uid
    sendpdu.tn = recpdu.tn
    sendpdu.port_resp = 0x00
    sendpdu.mess_cnt = 0x00
    sendpdu.sub_id = 0x0000
    sendpdu.cc = 0x21
    sendpdu.pid = 0x0080
    sendpdu.pdl = 32
    sendpdu.pd = (bytes('{:<32}'.format(self.model), 'utf8'))
    sendpdu.calcchecksum()
    return sendpdu

def devlabel(self, recpdu: rdmpacket.RDMpacket) -> rdmpacket.RDMpacket:
    """Returns a Device label rdmpacket for the given device
    RDM_GET = yes
    RDM_SET = yes
    """

    if recpdu.cc == defines.CC_Get_command:
        sendpdu = rdmpacket.RDMpacket()
        sendpdu.length = 0x38
        sendpdu.destuid = recpdu.srcuid
        sendpdu.srcuid = self.uid
        sendpdu.tn = recpdu.tn
        sendpdu.port_resp = 0x00
        sendpdu.mess_cnt = 0x00
        sendpdu.sub_id = 0x0000
        sendpdu.cc = 0x21
        sendpdu.pid = 0x0082
        sendpdu.pdl = 32
        sendpdu.pd = (bytes('{:<32}'.format(self.devlabel), 'utf8'))
        sendpdu.calcchecksum()
        return sendpdu
    elif recpdu.cc == defines.CC_Set_command:
        self.label = recpdu.pd.decode('utf-8')
        sendpdu = rdmpacket.RDMpacket()
        sendpdu.length = 24
        sendpdu.destuid = recpdu.srcuid
        sendpdu.srcuid = self.uid
        sendpdu.tn = recpdu.tn
        sendpdu.port_resp = 0x00
        sendpdu.mess_cnt = 0x00
        sendpdu.sub_id = 0x0000
        sendpdu.cc = defines.CC_Set_command_resp
        sendpdu.pid = recpdu.pid
        sendpdu.pdl = 0
        sendpdu.calcchecksum()
    else:
        return nackreturn(self, recpdu, nackcodes.nack_unsupported_cc)

def dmxaddress(self, recpdu: rdmpacket.RDMpacket) -> rdmpacket.RDMpacket:
    """Returns a dmx address rdmpacket for the given device
    RDM_GET = yes
    RDM_SET = yes
    """

    if recpdu.cc == defines.CC_Get_command:
        sendpdu = rdmpacket.RDMpacket()
        sendpdu.length = 0x1a
        sendpdu.destuid = recpdu.srcuid
        sendpdu.srcuid = self.uid
        sendpdu.tn = recpdu.tn
        sendpdu.port_resp = 0x00
        sendpdu.mess_cnt = 0x00
        sendpdu.sub_id = 0x0000
        sendpdu.cc = 0x21
        sendpdu.pid = 0x00f0
        sendpdu.pdl = 0x02
        sendpdu.pd = self.dmxaddress.to_bytes(2, 'big')
        sendpdu.calcchecksum()
        return sendpdu
    elif recpdu.cc == defines.CC_Set_command:
        self.dmxaddress = unpack('!H', recpdu.pd[0:2])[0]
        sendpdu = rdmpacket.RDMpacket()
        sendpdu.length = 24
        sendpdu.destuid = recpdu.srcuid
        sendpdu.srcuid = self.uid
        sendpdu.tn = recpdu.tn
        sendpdu.port_resp = 0x00
        sendpdu.mess_cnt = 0x00
        sendpdu.sub_id = 0x0000
        sendpdu.cc = defines.CC_Set_command_resp
        sendpdu.pid = recpdu.pid
        sendpdu.pdl = 0
        sendpdu.calcchecksum()
    else:
        return nackreturn(self, recpdu, nackcodes.nack_unsupported_cc)

def devhours(self, recpdu: rdmpacket.RDMpacket) -> rdmpacket.RDMpacket:
    """Returns a device hours rdmpacket for the given device
    RDM_GET = yes
    RDM_SET = yes
    """

    if recpdu.cc == defines.CC_Get_command:
        self.devhours += 1
        sendpdu = rdmpacket.RDMpacket()
        sendpdu.length = 0x1c
        sendpdu.destuid = recpdu.srcuid
        sendpdu.srcuid = self.uid
        sendpdu.tn = recpdu.tn
        sendpdu.port_resp = 0x00
        sendpdu.mess_cnt = 0x00
        sendpdu.sub_id = 0x0000
        sendpdu.cc = 0x21
        sendpdu.pid = 0x0400
        sendpdu.pdl = 0x04
        sendpdu.pd = self.devhours.to_bytes(4, 'big')
        sendpdu.calcchecksum()
        return sendpdu
    elif recpdu.cc == defines.CC_Set_command:
        self.devhours = unpack('!L', recpdu.pd[0:4])[0]
        sendpdu = rdmpacket.RDMpacket()
        sendpdu.length = 24
        sendpdu.destuid = recpdu.srcuid
        sendpdu.srcuid = self.uid
        sendpdu.tn = recpdu.tn
        sendpdu.port_resp = 0x00
        sendpdu.mess_cnt = 0x00
        sendpdu.sub_id = 0x0000
        sendpdu.cc = defines.CC_Set_command_resp
        sendpdu.pid = recpdu.pid
        sendpdu.pdl = 0
        sendpdu.calcchecksum()
    else:
        return nackreturn(self, recpdu, nackcodes.nack_unsupported_cc)

def lamphours(self, recpdu: rdmpacket.RDMpacket) -> rdmpacket.RDMpacket:
    """Returns a lamp hours rdmpacket for the given device
    RDM_GET = yes
    RDM_SET = yes
    """

    if recpdu.cc == defines.CC_Get_command:
        self.lamphours += 1
        sendpdu = rdmpacket.RDMpacket()
        sendpdu.length = 0x1c
        sendpdu.destuid = recpdu.srcuid
        sendpdu.srcuid = self.uid
        sendpdu.tn = recpdu.tn
        sendpdu.port_resp = 0x00
        sendpdu.mess_cnt = 0x00
        sendpdu.sub_id = 0x0000
        sendpdu.cc = 0x21
        sendpdu.pid = 0x0401
        sendpdu.pdl = 0x04
        sendpdu.pd = self.lamphours.to_bytes(4, 'big')
        sendpdu.calcchecksum()
        return sendpdu
    elif recpdu.cc == defines.CC_Set_command:
        self.lamphours = unpack('!L', recpdu.pd[0:4])[0]
        sendpdu = rdmpacket.RDMpacket()
        sendpdu.length = 24
        sendpdu.destuid = recpdu.srcuid
        sendpdu.srcuid = self.uid
        sendpdu.tn = recpdu.tn
        sendpdu.port_resp = 0x00
        sendpdu.mess_cnt = 0x00
        sendpdu.sub_id = 0x0000
        sendpdu.cc = defines.CC_Set_command_resp
        sendpdu.pid = recpdu.pid
        sendpdu.pdl = 0
        sendpdu.calcchecksum()
    else:
        return nackreturn(self, recpdu, nackcodes.nack_unsupported_cc)

def lampstrikes(self, recpdu: rdmpacket.RDMpacket) -> rdmpacket.RDMpacket:
    """Returns a lamp strikes rdmpacket for the given device
    RDM_GET = yes
    RDM_SET = yes
    """

    if recpdu.cc == defines.CC_Get_command:
        self.lampstrikes += 1
        sendpdu = rdmpacket.RDMpacket()
        sendpdu.length = 0x1c
        sendpdu.destuid = recpdu.srcuid
        sendpdu.srcuid = self.uid
        sendpdu.tn = recpdu.tn
        sendpdu.port_resp = 0x00
        sendpdu.mess_cnt = 0x00
        sendpdu.sub_id = 0x0000
        sendpdu.cc = 0x21
        sendpdu.pid = 0x0402
        sendpdu.pdl = 0x04
        sendpdu.pd = self.lampstrikes.to_bytes(4, 'big')
        sendpdu.calcchecksum()
        return sendpdu
    elif recpdu.cc == defines.CC_Set_command:
        self.lampstrikes = unpack('!L', recpdu.pd[0:4])[0]
        sendpdu = rdmpacket.RDMpacket()
        sendpdu.length = 24
        sendpdu.destuid = recpdu.srcuid
        sendpdu.srcuid = self.uid
        sendpdu.tn = recpdu.tn
        sendpdu.port_resp = 0x00
        sendpdu.mess_cnt = 0x00
        sendpdu.sub_id = 0x0000
        sendpdu.cc = defines.CC_Set_command_resp
        sendpdu.pid = recpdu.pid
        sendpdu.pdl = 0
        sendpdu.calcchecksum()
    else:
        return nackreturn(self, recpdu, nackcodes.nack_unsupported_cc)

def powercycles(self, recpdu: rdmpacket.RDMpacket) -> rdmpacket.RDMpacket:
    """Returns a power cycles rdmpacket for the given device
    RDM_GET = yes
    RDM_SET = yes
    """

    if recpdu.cc == defines.CC_Get_command:
        self.powercycles += 1
        sendpdu = rdmpacket.RDMpacket()
        sendpdu.length = 0x1c
        sendpdu.destuid = recpdu.srcuid
        sendpdu.srcuid = self.uid
        sendpdu.tn = recpdu.tn
        sendpdu.port_resp = 0x00
        sendpdu.mess_cnt = 0x00
        sendpdu.sub_id = 0x0000
        sendpdu.cc = 0x21
        sendpdu.pid = 0x0405
        sendpdu.pdl = 0x04
        sendpdu.pd = self.powercycles.to_bytes(4, 'big')
        sendpdu.calcchecksum()
        return sendpdu
    elif recpdu.cc == defines.CC_Set_command:
        self.powercycles = unpack('!L', recpdu.pd[0:4])[0]
        sendpdu = rdmpacket.RDMpacket()
        sendpdu.length = 24
        sendpdu.destuid = recpdu.srcuid
        sendpdu.srcuid = self.uid
        sendpdu.tn = recpdu.tn
        sendpdu.port_resp = 0x00
        sendpdu.mess_cnt = 0x00
        sendpdu.sub_id = 0x0000
        sendpdu.cc = defines.CC_Set_command_resp
        sendpdu.pid = recpdu.pid
        sendpdu.pdl = 0
        sendpdu.calcchecksum()
    else:
        return nackreturn(self, recpdu, nackcodes.nack_unsupported_cc)

def supportedpids(self, recpdu: rdmpacket.RDMpacket) -> rdmpacket.RDMpacket:
    """Returns an rdmpacket containing a list of supported pids
    for the given device
    RDM_GET = yes
    RDM_SET = no
    """

    if recpdu.cc is not defines.CC_Get_command:
        return nackreturn(self, recpdu, nackcodes.nack_unsupported_cc)
    sendpdu = rdmpacket.RDMpacket()
    sendpdu.destuid = recpdu.srcuid
    sendpdu.srcuid = self.uid
    sendpdu.tn = recpdu.tn
    sendpdu.port_resp = 0x00
    sendpdu.mess_cnt = 0x00
    sendpdu.sub_id = 0x0000
    sendpdu.cc = 0x21
    sendpdu.pid = 0x0050  
    rdmlist = list(self.getswitcher.keys())
    llrplist = list(self.llrpswitcher.keys())
    sendpdu.pdl = (len(rdmlist)+len(llrplist))*2
    keybytes = bytearray()
    for key in rdmlist:
        keybytes.extend(key.to_bytes(2, byteorder='big'))
    for key in llrplist:
        keybytes.extend(key.to_bytes(2, byteorder='big'))
    sendpdu.pd = keybytes
    sendpdu.length = 24+sendpdu.pdl
    sendpdu.calcchecksum()
    return sendpdu

def devscope(self, recpdu: rdmpacket.RDMpacket) -> rdmpacket.RDMpacket:
    """Return an RDM packet for device scope
    RDM_GET = yes
    RDM_SET = yes
    """

    if recpdu.cc == defines.CC_Get_command:
        sendpdu = rdmpacket.RDMpacket()
        sendpdu.destuid = recpdu.srcuid
        sendpdu.srcuid = self.uid
        sendpdu.tn = recpdu.tn
        sendpdu.port_resp = 0x00
        sendpdu.mess_cnt = 0x00
        sendpdu.sub_id = 0x0000
        sendpdu.cc = 0x21
        sendpdu.pid = 0x0800 
        sendpdu.pdl = 34
        sendpdu.pd = bytearray(b'\x00\x00')
        sendpdu.pd.extend(bytes('{:<32}'.format(self.scope), 'utf8'))
        sendpdu.length = 24+sendpdu.pdl
        sendpdu.calcchecksum()
        return sendpdu
    elif recpdu.cc == defines.CC_Set_command:
        self.scope = recpdu.pd.decode('utf-8')
        sendpdu = rdmpacket.RDMpacket()
        sendpdu.length = 24
        sendpdu.destuid = recpdu.srcuid
        sendpdu.srcuid = self.uid
        sendpdu.tn = recpdu.tn
        sendpdu.port_resp = 0x00
        sendpdu.mess_cnt = 0x00
        sendpdu.sub_id = 0x0000
        sendpdu.cc = defines.CC_Set_command_resp
        sendpdu.pid = recpdu.pid
        sendpdu.pdl = 0
        sendpdu.calcchecksum()
    else:
        return nackreturn(self, recpdu, nackcodes.nack_unsupported_cc)

def devsearch(self, recpdu: rdmpacket.RDMpacket) -> rdmpacket.RDMpacket:
    """Return an RDM packet for device scope 
    RDM_GET = yes
    RDM_SET = yes
    """
    
    if recpdu.cc == defines.CC_Get_command:
        sendpdu = rdmpacket.RDMpacket()
        sendpdu.destuid = recpdu.srcuid
        sendpdu.srcuid = self.uid
        sendpdu.tn = recpdu.tn
        sendpdu.port_resp = 0x00
        sendpdu.mess_cnt = 0x00
        sendpdu.sub_id = 0x0000
        sendpdu.cc = 0x21
        sendpdu.pid = 0x0801
        sendpdu.pdl = 32
        sendpdu.pd = (bytes('{:<32}'.format(self.searchdomain), 'utf8'))
        sendpdu.length = 24+sendpdu.pdl
        sendpdu.calcchecksum()
        return sendpdu
    elif recpdu.cc == defines.CC_Set_command:
        self.searchdomain = recpdu.pd.decode('utf-8')
        sendpdu = rdmpacket.RDMpacket()
        sendpdu.length = 24
        sendpdu.destuid = recpdu.srcuid
        sendpdu.srcuid = self.uid
        sendpdu.tn = recpdu.tn
        sendpdu.port_resp = 0x00
        sendpdu.mess_cnt = 0x00
        sendpdu.sub_id = 0x0000
        sendpdu.cc = defines.CC_Set_command_resp
        sendpdu.pid = recpdu.pid
        sendpdu.pdl = 0
        sendpdu.calcchecksum()
    else:
        return nackreturn(self, recpdu, nackcodes.nack_unsupported_cc)

def sensordef(self, recpdu: rdmpacket.RDMpacket) -> rdmpacket.RDMpacket:
    """Returns a sensor definition rdmpacket for the given device
    RDM_GET = yes
    RDM_SET = no
    """

    if recpdu.cc is not defines.CC_Get_command:
        return nackreturn(self, recpdu, nackcodes.nack_unsupported_cc)
    else:
        sensno = recpdu.pd[0]
        if sensno < len(self.sensors):
            #Ack and return definition
            sendpdu = rdmpacket.RDMpacket()
            
            sendpdu.destuid = recpdu.srcuid
            sendpdu.srcuid = self.uid
            sendpdu.tn = recpdu.tn
            sendpdu.port_resp = 0x00
            sendpdu.mess_cnt = 0x00
            sendpdu.sub_id = 0x0000
            sendpdu.cc = 0x21
            sendpdu.pid = 0x0200
            sendpdu.pd = self.sensors[sensno].rdmdef(sensno)
            sendpdu.pdl = len(sendpdu.pd)
            sendpdu.length = 0x18 + sendpdu.pdl
            sendpdu.calcchecksum()
            return sendpdu
        else:
            #NACK
            return nackreturn(self, recpdu, nackcodes.nack_data_range)


def sensorval(self, recpdu: rdmpacket.RDMpacket) -> rdmpacket.RDMpacket:
    """Returns a sensor value rdmpacket for the given device
    RDM_GET = yes
    RDM_SET = no
    """

    if recpdu.cc is not defines.CC_Get_command:
        return nackreturn(self, recpdu, nackcodes.nack_unsupported_cc)
    else:
        sensno = recpdu.pd[0]
        if sensno < len(self.sensors):
            #Ack and return definition
            sendpdu = rdmpacket.RDMpacket()
            self.sensors[sensno].updateval()
            sendpdu.destuid = recpdu.srcuid
            sendpdu.srcuid = self.uid
            sendpdu.tn = recpdu.tn
            sendpdu.port_resp = 0x00
            sendpdu.mess_cnt = 0x00
            sendpdu.sub_id = 0x0000
            sendpdu.cc = 0x21
            sendpdu.pid = 0x0201
            sendpdu.pd = bytearray(sensno.to_bytes(1, 'big'))
            sendpdu.pd.extend(pack('!h', self.sensors[sensno].value))
            sendpdu.pdl = len(sendpdu.pd)
            sendpdu.length = 0x18 + sendpdu.pdl
            sendpdu.calcchecksum()
            return sendpdu
        else:
            #NACK
            return nackreturn(self, recpdu, nackcodes.nack_data_range)
        

def nackreturn(self,recpdu: rdmpacket.RDMpacket, reasoncode) -> rdmpacket.RDMpacket:
    print("Nacking PID {:04x}".format(recpdu.pid))
    sendpdu = rdmpacket.RDMpacket()
    sendpdu.length = 0x1a
    sendpdu.destuid = recpdu.srcuid
    sendpdu.srcuid = self.uid
    sendpdu.tn = recpdu.tn
    sendpdu.port_resp = 0x02
    sendpdu.cc = 0x21
    sendpdu.pid = recpdu.pid
    sendpdu.pdl = 0x02
    sendpdu.pd = reasoncode
    sendpdu.calcchecksum()
    return sendpdu
