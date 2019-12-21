from RDM import checksums, rdmpacket

def devinfo(self, recpdu: rdmpacket.RDMpacket) -> rdmpacket.RDMpacket:
    """Returns an device info rdmpacket for the given device
    """
    sendpdu = rdmpacket.RDMpacket()
    sendpdu.length = 0x2b
    sendpdu.destuid = recpdu.srcuid
    sendpdu.srcuid = self.uid
    sendpdu.tn = recpdu.tn
    sendpdu.port_resp = 0x21
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
    sendpdu.pd.extend(b'\x00')  # TODO: Add Sensors
    sendpdu.calcchecksum()
    return sendpdu


def devsoftwareversion(self, recpdu: rdmpacket.RDMpacket) -> rdmpacket.RDMpacket:
    """Returns a Device Software Version rdmpacket for the given device"""
    sendpdu = rdmpacket.RDMpacket()
    sendpdu.length = 0x38
    sendpdu.destuid = recpdu.srcuid
    sendpdu.srcuid = self.uid
    sendpdu.tn = recpdu.tn
    sendpdu.port_resp = 0x21
    sendpdu.mess_cnt = 0x00
    sendpdu.sub_id = 0x0000
    sendpdu.cc = 0x21
    sendpdu.pid = 0x00C0
    sendpdu.pdl = 32
    sendpdu.pd = (bytes('{:<32}'.format(self.softwareverslabel), 'utf8'))
    sendpdu.calcchecksum()
    return sendpdu

def devmanufacturer(self, recpdu: rdmpacket.RDMpacket) -> rdmpacket.RDMpacket:
    """Returns a Device Manufacturer rdmpacket for the given device"""
    sendpdu = rdmpacket.RDMpacket()
    sendpdu.length = 0x38
    sendpdu.destuid = recpdu.srcuid
    sendpdu.srcuid = self.uid
    sendpdu.tn = recpdu.tn
    sendpdu.port_resp = 0x21
    sendpdu.mess_cnt = 0x00
    sendpdu.sub_id = 0x0000
    sendpdu.cc = 0x21
    sendpdu.pid = 0x0081
    sendpdu.pdl = 32
    sendpdu.pd = (bytes('{:<32}'.format(self.mfr), 'utf8'))
    sendpdu.calcchecksum()
    return sendpdu


def devmodel(self, recpdu: rdmpacket.RDMpacket) -> rdmpacket.RDMpacket:
    """Returns a Device Model Description rdmpacket for the given device"""
    sendpdu = rdmpacket.RDMpacket()
    sendpdu.length = 0x38
    sendpdu.destuid = recpdu.srcuid
    sendpdu.srcuid = self.uid
    sendpdu.tn = recpdu.tn
    sendpdu.port_resp = 0x21
    sendpdu.mess_cnt = 0x00
    sendpdu.sub_id = 0x0000
    sendpdu.cc = 0x21
    sendpdu.pid = 0x0080
    sendpdu.pdl = 32
    sendpdu.pd = (bytes('{:<32}'.format(self.model), 'utf8'))
    sendpdu.calcchecksum()
    return sendpdu

def devlabel(self, recpdu: rdmpacket.RDMpacket) -> rdmpacket.RDMpacket:
    """Returns a Device label rdmpacket for the given device"""
    sendpdu = rdmpacket.RDMpacket()
    sendpdu.length = 0x38
    sendpdu.destuid = recpdu.srcuid
    sendpdu.srcuid = self.uid
    sendpdu.tn = recpdu.tn
    sendpdu.port_resp = 0x21
    sendpdu.mess_cnt = 0x00
    sendpdu.sub_id = 0x0000
    sendpdu.cc = 0x21
    sendpdu.pid = 0x0082
    sendpdu.pdl = 32
    sendpdu.pd = (bytes('{:<32}'.format(self.devlabel), 'utf8'))
    sendpdu.calcchecksum()
    return sendpdu

def dmxaddress(self, recpdu: rdmpacket.RDMpacket) -> rdmpacket.RDMpacket:
    """Returns a dmx address rdmpacket for the given device"""
    sendpdu = rdmpacket.RDMpacket()
    sendpdu.length = 0x1a
    sendpdu.destuid = recpdu.srcuid
    sendpdu.srcuid = self.uid
    sendpdu.tn = recpdu.tn
    sendpdu.port_resp = 0x21
    sendpdu.mess_cnt = 0x00
    sendpdu.sub_id = 0x0000
    sendpdu.cc = 0x21
    sendpdu.pid = 0x00f0
    sendpdu.pdl = 0x02
    sendpdu.pd = self.dmxaddress.to_bytes(2, 'big')
    sendpdu.calcchecksum()
    return sendpdu

def devhours(self, recpdu: rdmpacket.RDMpacket) -> rdmpacket.RDMpacket:
    """Returns a device hours rdmpacket for the given device"""
    sendpdu = rdmpacket.RDMpacket()
    sendpdu.length = 0x1c
    sendpdu.destuid = recpdu.srcuid
    sendpdu.srcuid = self.uid
    sendpdu.tn = recpdu.tn
    sendpdu.port_resp = 0x21
    sendpdu.mess_cnt = 0x00
    sendpdu.sub_id = 0x0000
    sendpdu.cc = 0x21
    sendpdu.pid = 0x0400
    sendpdu.pdl = 0x04
    sendpdu.pd = self.devhours.to_bytes(4, 'big')
    sendpdu.calcchecksum()
    return sendpdu

def lamphours(self, recpdu: rdmpacket.RDMpacket) -> rdmpacket.RDMpacket:
    """Returns a lamp hours rdmpacket for the given device"""
    sendpdu = rdmpacket.RDMpacket()
    sendpdu.length = 0x1c
    sendpdu.destuid = recpdu.srcuid
    sendpdu.srcuid = self.uid
    sendpdu.tn = recpdu.tn
    sendpdu.port_resp = 0x21
    sendpdu.mess_cnt = 0x00
    sendpdu.sub_id = 0x0000
    sendpdu.cc = 0x21
    sendpdu.pid = 0x0401
    sendpdu.pdl = 0x04
    sendpdu.pd = self.lamphours.to_bytes(4, 'big')
    sendpdu.calcchecksum()
    return sendpdu

def lampstrikes(self, recpdu: rdmpacket.RDMpacket) -> rdmpacket.RDMpacket:
    """Returns a lamp strikes rdmpacket for the given device"""
    sendpdu = rdmpacket.RDMpacket()
    sendpdu.length = 0x1c
    sendpdu.destuid = recpdu.srcuid
    sendpdu.srcuid = self.uid
    sendpdu.tn = recpdu.tn
    sendpdu.port_resp = 0x21
    sendpdu.mess_cnt = 0x00
    sendpdu.sub_id = 0x0000
    sendpdu.cc = 0x21
    sendpdu.pid = 0x0402
    sendpdu.pdl = 0x04
    sendpdu.pd = self.lamphours.to_bytes(4, 'big')
    sendpdu.calcchecksum()
    return sendpdu

def powercycles(self, recpdu: rdmpacket.RDMpacket) -> rdmpacket.RDMpacket:
    """Returns a power cycles rdmpacket for the given device"""
    sendpdu = rdmpacket.RDMpacket()
    sendpdu.length = 0x1c
    sendpdu.destuid = recpdu.srcuid
    sendpdu.srcuid = self.uid
    sendpdu.tn = recpdu.tn
    sendpdu.port_resp = 0x21
    sendpdu.mess_cnt = 0x00
    sendpdu.sub_id = 0x0000
    sendpdu.cc = 0x21
    sendpdu.pid = 0x0405
    sendpdu.pdl = 0x04
    sendpdu.pd = self.powercycles.to_bytes(4, 'big')
    sendpdu.calcchecksum()
    return sendpdu

def supportedpids(self, recpdu: rdmpacket.RDMpacket) -> rdmpacket.RDMpacket:
    """Returns an rdmpacket containing a list of supported pids
     for the given device"""
    sendpdu = rdmpacket.RDMpacket()
    sendpdu.destuid = recpdu.srcuid
    sendpdu.srcuid = self.uid
    sendpdu.tn = recpdu.tn
    sendpdu.port_resp = 0x21
    sendpdu.mess_cnt = 0x00
    sendpdu.sub_id = 0x0000
    sendpdu.cc = 0x21
    sendpdu.pid = 0x0050  
    keylist = list(self.getswitcher.keys())
    sendpdu.pdl = len(keylist)*2
    keybytes = bytearray()
    for key in keylist:
         keybytes.extend(key.to_bytes(2, byteorder='big'))
    sendpdu.pd = keybytes
    sendpdu.length = 24+sendpdu.pdl
    sendpdu.calcchecksum()
    return sendpdu


def devscope(self, pdu):
    print("Get Device Scope")
    length = 24 + len(self.scope)
    data = bytearray(b'\xcc\x01')
    data.extend(length.to_bytes(1, 'big'))
    data.extend(pdu[78:84])
    data.extend(self.uid)
    data.extend(b'\x00\x00\x00\x00\x00')
    data.extend(b'\x21')
    data.extend(b'\x7F\xEF')
    data.extend(bytes([len(self.scope)+2]))
    data.extend(b'\x00\x00')
    data.extend(bytes(self.scope, 'utf-8'))
    data = checksums.rdmCheckSum(data)
    return data


def devsearch(self, pdu):
    print("Get Device Search Domain")
    length = 24 + len(self.searchdomain)
    data = bytearray(b'\xcc\x01')
    data.extend(length.to_bytes(1, 'big'))
    data.extend(pdu[78:84])
    data.extend(self.uid)
    data.extend(b'\x00\x00\x00\x00\x00')
    data.extend(b'\x21')
    data.extend(b'\x7F\xE0')
    data.extend(bytes([len(self.searchdomain)]))
    data.extend(bytes(self.searchdomain, 'utf-8'))
    data = checksums.rdmCheckSum(data)
    return data

def nackreturn(self,pid, reasoncode, recpdu: rdmpacket.RDMpacket) -> rdmpacket.RDMpacket:
    print("Nacking PID %x" % pid)
    sendpdu = rdmpacket.RDMpacket()
    sendpdu.length = 0x1a
    sendpdu.destuid = recpdu.srcuid
    sendpdu.srcuid = self.uid
    sendpdu.tn = recpdu.tn
    sendpdu.port_resp = 0x02
    sendpdu.cc = 0x21
    sendpdu.pid = pid
    sendpdu.pdl = 0x02
    sendpdu.pd = reasoncode
    sendpdu.calcchecksum()
    return sendpdu
