"""Get handlers for DummyRDM Device"""
from struct import unpack, pack
from RDM import rdmpacket, defines, nackcodes


#TODO: Personality Descriptions, Parameter Description

def devreset(self, recpdu: rdmpacket.RDMpacket) -> rdmpacket.RDMpacket:
    """Performs a simulated hot/cold reset on the device
    RDM_GET = no
    RDM_SET = yes
    """

    if recpdu.cc == defines.CC_Set_command:
        if recpdu.pd[0] == 0x01:
            #Warm Reset
            print("Device {}: Warm reset requested".format(self.device_descriptor.uid.hex()))
        elif recpdu.pd[0] == 0xFF:
            #Cold Reset
            print("Device {}: Cold reset requested".format(self.device_descriptor.uid.hex()))
        else:
            #Out of range NACK
            return nackreturn(self, recpdu, nackcodes.nack_data_range)
        sendpdu = rdmpacket.RDMpacket()
        sendpdu.length = 24
        sendpdu.destuid = recpdu.srcuid
        sendpdu.srcuid = self.device_descriptor.uid
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
    #BUG: Currently Returning with incorrect checksum - needs verification
    if recpdu.cc == defines.CC_Get_command:
        sendpdu = rdmpacket.RDMpacket()
        sendpdu.length = 25
        sendpdu.destuid = recpdu.srcuid
        sendpdu.srcuid = self.device_descriptor.uid
        sendpdu.tn = recpdu.tn
        sendpdu.port_resp = 0x00
        sendpdu.mess_cnt = 0x00
        sendpdu.sub_id = 0x0000
        sendpdu.cc = defines.CC_Get_command_resp
        sendpdu.pid = recpdu.pid
        sendpdu.pdl = 1
        sendpdu.pd = self.device_descriptor.factorystatus.to_bytes(1, 'big')
        sendpdu.calcchecksum()
        return sendpdu
    elif recpdu.cc == defines.CC_Set_command:
        print("Device {}: Factory Reset".format(self.device_descriptor.uid.hex()))
        sendpdu = rdmpacket.RDMpacket()
        sendpdu.length = 24
        sendpdu.destuid = recpdu.srcuid
        sendpdu.srcuid = self.device_descriptor.uid
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
        sendpdu.srcuid = self.device_descriptor.uid
        sendpdu.tn = recpdu.tn
        sendpdu.port_resp = 0x00
        sendpdu.mess_cnt = 0x00
        sendpdu.sub_id = 0x0000
        sendpdu.cc = defines.CC_Get_command_resp
        sendpdu.pid = recpdu.pid
        sendpdu.pdl = 1
        sendpdu.pd = self.device_descriptor.identifystatus.to_bytes(1, 'big')
        sendpdu.calcchecksum()
        return sendpdu
    elif recpdu.cc == defines.CC_Set_command:
        if recpdu.pd[0] <= 1:
            print("Device {}: Identify set to {:02x}".format(self.device_descriptor.uid.hex(), recpdu.pd[0]))
            self.device_descriptor.identifystatus = recpdu.pd[0]
            sendpdu = rdmpacket.RDMpacket()
            sendpdu.length = 24
            sendpdu.destuid = recpdu.srcuid
            sendpdu.srcuid = self.device_descriptor.uid
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
    sendpdu.srcuid = self.device_descriptor.uid
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
    sendpdu.pd.extend(self.device_descriptor.dmxfootprint.to_bytes(2, 'big'))
    # DMX Personality
    sendpdu.pd.extend(self.device_descriptor.currentpers.to_bytes(1, 'big'))
    perslen = len(self.device_descriptor.perslist)+1
    sendpdu.pd.extend(perslen.to_bytes(1, 'big'))
    # DMX Start Address
    sendpdu.pd.extend(self.device_descriptor.dmxaddress.to_bytes(2, 'big'))
    # Sub Device Count
    sendpdu.pd.extend(b'\x00\x00')
    # Sensor Count
    sendpdu.pd.extend(len(self.device_descriptor.sensors).to_bytes(1, 'big'))
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
    sendpdu.destuid = recpdu.srcuid
    sendpdu.srcuid = self.device_descriptor.uid
    sendpdu.tn = recpdu.tn
    sendpdu.port_resp = 0x00
    sendpdu.mess_cnt = 0x00
    sendpdu.sub_id = 0x0000
    sendpdu.cc = 0x21
    sendpdu.pid = 0x00C0
    if len(self.device_descriptor.softwareverslabel) > 32:
        sendpdu.pd = bytes(self.device_descriptor.softwareverslabel[:32], 'utf-8')
    else:
        sendpdu.pd = bytes(self.device_descriptor.softwareverslabel, 'utf-8') #Limit 32 Characters
    sendpdu.pdl = len(sendpdu.pd)
    sendpdu.length = 24+sendpdu.pdl
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
    
    sendpdu.destuid = recpdu.srcuid
    sendpdu.srcuid = self.device_descriptor.uid
    sendpdu.tn = recpdu.tn
    sendpdu.port_resp = 0x00
    sendpdu.mess_cnt = 0x00
    sendpdu.sub_id = 0x0000
    sendpdu.cc = 0x21
    sendpdu.pid = 0x0081
    if len(self.device_descriptor.mfr) > 32:
        sendpdu.pd = bytes(self.device_descriptor.mfr[:32], 'utf-8')
    else:
        sendpdu.pd = bytes(self.device_descriptor.mfr, 'utf-8') #Limit 32 Characters
    sendpdu.pdl = len(sendpdu.pd)
    sendpdu.length = 24+sendpdu.pdl
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
    sendpdu.destuid = recpdu.srcuid
    sendpdu.srcuid = self.device_descriptor.uid
    sendpdu.tn = recpdu.tn
    sendpdu.port_resp = 0x00
    sendpdu.mess_cnt = 0x00
    sendpdu.sub_id = 0x0000
    sendpdu.cc = 0x21
    sendpdu.pid = 0x0080
    if len(self.device_descriptor.model) > 32:
        sendpdu.pd = bytes(self.device_descriptor.model[:32], 'utf-8')
    else:
        sendpdu.pd = bytes(self.device_descriptor.model, 'utf-8') #Limit 32 Characters
    sendpdu.pdl = len(sendpdu.pd)
    sendpdu.length = 24+sendpdu.pdl
    sendpdu.calcchecksum()
    return sendpdu

def devlabel(self, recpdu: rdmpacket.RDMpacket) -> rdmpacket.RDMpacket:
    """Returns a Device label rdmpacket for the given device
    RDM_GET = yes
    RDM_SET = yes
    """

    if recpdu.cc == defines.CC_Get_command:
        sendpdu = rdmpacket.RDMpacket()
        sendpdu.destuid = recpdu.srcuid
        sendpdu.srcuid = self.device_descriptor.uid
        sendpdu.tn = recpdu.tn
        sendpdu.port_resp = 0x00
        sendpdu.mess_cnt = 0x00
        sendpdu.sub_id = 0x0000
        sendpdu.cc = 0x21
        sendpdu.pid = 0x0082
        if len(self.device_descriptor.label) > 32:
            sendpdu.pd = bytes(self.device_descriptor.label[:32], 'utf-8')
        else:
            sendpdu.pd = bytes(self.device_descriptor.label, 'utf-8') #Limit 32 Characters
        sendpdu.pdl = len(sendpdu.pd)
        sendpdu.length = 24+sendpdu.pdl
        sendpdu.calcchecksum()
        return sendpdu
    elif recpdu.cc == defines.CC_Set_command:
        self.device_descriptor.label = recpdu.pd.decode('utf-8')
        sendpdu = rdmpacket.RDMpacket()
        sendpdu.length = 24
        sendpdu.destuid = recpdu.srcuid
        sendpdu.srcuid = self.device_descriptor.uid
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
        sendpdu.srcuid = self.device_descriptor.uid
        sendpdu.tn = recpdu.tn
        sendpdu.port_resp = 0x00
        sendpdu.mess_cnt = 0x00
        sendpdu.sub_id = 0x0000
        sendpdu.cc = 0x21
        sendpdu.pid = 0x00f0
        sendpdu.pdl = 0x02
        sendpdu.pd = self.device_descriptor.dmxaddress.to_bytes(2, 'big')
        sendpdu.calcchecksum()
        return sendpdu
    elif recpdu.cc == defines.CC_Set_command:
        self.device_descriptor.dmxaddress = unpack('!H', recpdu.pd[0:2])[0]
        sendpdu = rdmpacket.RDMpacket()
        sendpdu.length = 24
        sendpdu.destuid = recpdu.srcuid
        sendpdu.srcuid = self.device_descriptor.uid
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
        self.device_descriptor.devhours += 1
        sendpdu = rdmpacket.RDMpacket()
        sendpdu.length = 0x1c
        sendpdu.destuid = recpdu.srcuid
        sendpdu.srcuid = self.device_descriptor.uid
        sendpdu.tn = recpdu.tn
        sendpdu.port_resp = 0x00
        sendpdu.mess_cnt = 0x00
        sendpdu.sub_id = 0x0000
        sendpdu.cc = 0x21
        sendpdu.pid = 0x0400
        sendpdu.pdl = 0x04
        sendpdu.pd = self.device_descriptor.devhours.to_bytes(4, 'big')
        sendpdu.calcchecksum()
        return sendpdu
    elif recpdu.cc == defines.CC_Set_command:
        self.device_descriptor.devhours = unpack('!L', recpdu.pd[0:4])[0]
        sendpdu = rdmpacket.RDMpacket()
        sendpdu.length = 24
        sendpdu.destuid = recpdu.srcuid
        sendpdu.srcuid = self.device_descriptor.uid
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
        self.device_descriptor.lamphours += 1
        sendpdu = rdmpacket.RDMpacket()
        sendpdu.length = 0x1c
        sendpdu.destuid = recpdu.srcuid
        sendpdu.srcuid = self.device_descriptor.uid
        sendpdu.tn = recpdu.tn
        sendpdu.port_resp = 0x00
        sendpdu.mess_cnt = 0x00
        sendpdu.sub_id = 0x0000
        sendpdu.cc = 0x21
        sendpdu.pid = 0x0401
        sendpdu.pdl = 0x04
        sendpdu.pd = self.device_descriptor.lamphours.to_bytes(4, 'big')
        sendpdu.calcchecksum()
        return sendpdu
    elif recpdu.cc == defines.CC_Set_command:
        self.device_descriptor.lamphours = unpack('!L', recpdu.pd[0:4])[0]
        sendpdu = rdmpacket.RDMpacket()
        sendpdu.length = 24
        sendpdu.destuid = recpdu.srcuid
        sendpdu.srcuid = self.device_descriptor.uid
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
        self.device_descriptor.lampstrikes += 1
        sendpdu = rdmpacket.RDMpacket()
        sendpdu.length = 0x1c
        sendpdu.destuid = recpdu.srcuid
        sendpdu.srcuid = self.device_descriptor.uid
        sendpdu.tn = recpdu.tn
        sendpdu.port_resp = 0x00
        sendpdu.mess_cnt = 0x00
        sendpdu.sub_id = 0x0000
        sendpdu.cc = 0x21
        sendpdu.pid = 0x0402
        sendpdu.pdl = 0x04
        sendpdu.pd = self.device_descriptor.lampstrikes.to_bytes(4, 'big')
        sendpdu.calcchecksum()
        return sendpdu
    elif recpdu.cc == defines.CC_Set_command:
        self.device_descriptor.lampstrikes = unpack('!L', recpdu.pd[0:4])[0]
        sendpdu = rdmpacket.RDMpacket()
        sendpdu.length = 24
        sendpdu.destuid = recpdu.srcuid
        sendpdu.srcuid = self.device_descriptor.uid
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
        self.device_descriptor.powercycles += 1
        sendpdu = rdmpacket.RDMpacket()
        sendpdu.length = 0x1c
        sendpdu.destuid = recpdu.srcuid
        sendpdu.srcuid = self.device_descriptor.uid
        sendpdu.tn = recpdu.tn
        sendpdu.port_resp = 0x00
        sendpdu.mess_cnt = 0x00
        sendpdu.sub_id = 0x0000
        sendpdu.cc = 0x21
        sendpdu.pid = 0x0405
        sendpdu.pdl = 0x04
        sendpdu.pd = self.device_descriptor.powercycles.to_bytes(4, 'big')
        sendpdu.calcchecksum()
        return sendpdu
    elif recpdu.cc == defines.CC_Set_command:
        self.device_descriptor.powercycles = unpack('!L', recpdu.pd[0:4])[0]
        sendpdu = rdmpacket.RDMpacket()
        sendpdu.length = 24
        sendpdu.destuid = recpdu.srcuid
        sendpdu.srcuid = self.device_descriptor.uid
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

def lampstatus(self, recpdu: rdmpacket.RDMpacket) -> rdmpacket.RDMpacket:
    """Returns an rdmpacket containing the lamp status as a unsigned char
    for the given device
    RDM_GET = yes
    RDM_SET = yes
    """

    if recpdu.cc == defines.CC_Get_command:
        sendpdu = rdmpacket.RDMpacket()
        sendpdu.length = 0x1c
        sendpdu.destuid = recpdu.srcuid
        sendpdu.srcuid = self.device_descriptor.uid
        sendpdu.tn = recpdu.tn
        sendpdu.port_resp = 0x00
        sendpdu.mess_cnt = 0x00
        sendpdu.sub_id = 0x0000
        sendpdu.cc = 0x21
        sendpdu.pid = 0x0405
        sendpdu.pdl = 0x04
        sendpdu.pd = self.device_descriptor.lampstatus.to_bytes(1, 'big')
        sendpdu.calcchecksum()
        return sendpdu
    elif recpdu.cc == defines.CC_Set_command:
        self.device_descriptor.lampstatus = unpack('!B', recpdu.pd[0])[0]
        print("Device {}: Lamp State set to: {}".format(self.device_descriptor.uid.hex(),
                                                        self.device_descriptor.lampstatus))
        sendpdu = rdmpacket.RDMpacket()
        sendpdu.length = 24
        sendpdu.destuid = recpdu.srcuid
        sendpdu.srcuid = self.device_descriptor.uid
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

def lamppowerstate(self, recpdu: rdmpacket.RDMpacket) -> rdmpacket.RDMpacket:
    """Returns an rdmpacket containing the lamp sate on power on
    as a unsigned char for the given device
    RDM_GET = yes
    RDM_SET = yes
    """

    if recpdu.cc == defines.CC_Get_command:
        sendpdu = rdmpacket.RDMpacket()
        sendpdu.length = 0x1c
        sendpdu.destuid = recpdu.srcuid
        sendpdu.srcuid = self.device_descriptor.uid
        sendpdu.tn = recpdu.tn
        sendpdu.port_resp = 0x00
        sendpdu.mess_cnt = 0x00
        sendpdu.sub_id = 0x0000
        sendpdu.cc = 0x21
        sendpdu.pid = 0x0405
        sendpdu.pdl = 0x04
        sendpdu.pd = self.device_descriptor.lamppowerstate.to_bytes(1, 'big')
        sendpdu.calcchecksum()
        return sendpdu
    elif recpdu.cc == defines.CC_Set_command:
        self.device_descriptor.lamppowerstate = unpack('!B', recpdu.pd[0])[0]
        print("Device {}: Lamp Power State set to: {}".format(self.device_descriptor.uid.hex(),
                                                              self.device_descriptor.lamppowerstatus))
        sendpdu = rdmpacket.RDMpacket()
        sendpdu.length = 24
        sendpdu.destuid = recpdu.srcuid
        sendpdu.srcuid = self.device_descriptor.uid
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
    sendpdu.srcuid = self.device_descriptor.uid
    sendpdu.tn = recpdu.tn
    sendpdu.port_resp = 0x00
    sendpdu.mess_cnt = 0x00
    sendpdu.sub_id = 0x0000
    sendpdu.cc = 0x21
    sendpdu.pid = 0x0050  
    rdmlist = list(self.device_descriptor.getswitcher.keys())
    llrplist = list(self.device_descriptor.llrpswitcher.keys())
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
    #TODO: Currently this only returns scope 1
    if recpdu.cc == defines.CC_Get_command:
        sendpdu = rdmpacket.RDMpacket()
        sendpdu.destuid = recpdu.srcuid
        sendpdu.srcuid = self.device_descriptor.uid
        sendpdu.tn = recpdu.tn
        sendpdu.port_resp = 0x00
        sendpdu.mess_cnt = 0x00
        sendpdu.sub_id = 0x0000
        sendpdu.cc = 0x21
        sendpdu.pid = 0x0800 
        sendpdu.pdl = 34
        sendpdu.pd = bytearray(b'\x00\x01')
        if len(self.device_descriptor.scope) > 63:
            sendpdu.pd.extend(bytes(self.device_descriptor.scope[:63], 'utf-8'))
        else:
            sendpdu.pd.extend(bytes(self.device_descriptor.scope, 'utf-8'))
            for i in range(63-len(self.device_descriptor.scope)):
                sendpdu.pd.extend(b'\x00')
        #Static config Type,
        sendpdu.pd.extend(b'\x01')
        #IPv4 Address
        sendpdu.pd.extend(b'\x7f\x00\x00\x01')
        #IPv6 Address
        sendpdu.pd.extend(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01')
        #Port
        sendpdu.pd.extend(b'\x00\x00')
        sendpdu.pdl = len(sendpdu.pd)
        sendpdu.length = 24+sendpdu.pdl
        sendpdu.calcchecksum()
        return sendpdu
    elif recpdu.cc == defines.CC_Set_command:
        self.device_descriptor.scope = recpdu.pd.decode('utf-8')
        sendpdu = rdmpacket.RDMpacket()
        sendpdu.length = 24
        sendpdu.destuid = recpdu.srcuid
        sendpdu.srcuid = self.device_descriptor.uid
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
        sendpdu.srcuid = self.device_descriptor.uid
        sendpdu.tn = recpdu.tn
        sendpdu.port_resp = 0x00
        sendpdu.mess_cnt = 0x00
        sendpdu.sub_id = 0x0000
        sendpdu.cc = 0x21
        sendpdu.pid = 0x0801
        if len(self.device_descriptor.searchdomain) > 32:
            sendpdu.pd = bytes(self.device_descriptor.searchdomain[:32], 'utf-8')
        else:
            sendpdu.pd = bytes(self.device_descriptor.searchdomain, 'utf-8') #Limit 32 Characters
        sendpdu.pdl = len(sendpdu.pd)
        sendpdu.length = 24+sendpdu.pdl
        sendpdu.calcchecksum()
        return sendpdu
    elif recpdu.cc == defines.CC_Set_command:
        self.device_descriptor.searchdomain = recpdu.pd.decode('utf-8')
        sendpdu = rdmpacket.RDMpacket()
        sendpdu.length = 24
        sendpdu.destuid = recpdu.srcuid
        sendpdu.srcuid = self.device_descriptor.uid
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
        if sensno < len(self.device_descriptor.sensors):
            #Ack and return definition
            sendpdu = rdmpacket.RDMpacket()
            sendpdu.destuid = recpdu.srcuid
            sendpdu.srcuid = self.device_descriptor.uid
            sendpdu.tn = recpdu.tn
            sendpdu.port_resp = 0x00
            sendpdu.mess_cnt = 0x00
            sendpdu.sub_id = 0x0000
            sendpdu.cc = 0x21
            sendpdu.pid = 0x0200
            sendpdu.pd = self.device_descriptor.sensors[sensno].rdmdef(sensno)
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
        if sensno < len(self.device_descriptor.sensors):
            #Ack and return definition
            sendpdu = rdmpacket.RDMpacket()
            self.device_descriptor.sensors[sensno].updateval()
            sendpdu.destuid = recpdu.srcuid
            sendpdu.srcuid = self.device_descriptor.uid
            sendpdu.tn = recpdu.tn
            sendpdu.port_resp = 0x00
            sendpdu.mess_cnt = 0x00
            sendpdu.sub_id = 0x0000
            sendpdu.cc = 0x21
            sendpdu.pid = 0x0201
            sendpdu.pd = bytearray(sensno.to_bytes(1, 'big'))
            sendpdu.pd.extend(pack('!h', self.device_descriptor.sensors[sensno].value))
            sendpdu.pdl = len(sendpdu.pd)
            sendpdu.length = 0x18 + sendpdu.pdl
            sendpdu.calcchecksum()
            return sendpdu
        else:
            #NACK
            return nackreturn(self, recpdu, nackcodes.nack_data_range)

def nackreturn(self, recpdu: rdmpacket.RDMpacket, reasoncode) -> rdmpacket.RDMpacket:
    """Returns a NACK for a given rdmpacket with a reason"""

    print("Nacking PID {:04x}".format(recpdu.pid))
    sendpdu = rdmpacket.RDMpacket()
    sendpdu.length = 0x1a
    sendpdu.destuid = recpdu.srcuid
    sendpdu.srcuid = self.device_descriptor.uid
    sendpdu.tn = recpdu.tn
    sendpdu.port_resp = 0x02
    sendpdu.cc = 0x21
    sendpdu.pid = recpdu.pid
    sendpdu.pdl = 0x02
    sendpdu.pd = reasoncode
    sendpdu.calcchecksum()
    return sendpdu
