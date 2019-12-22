from struct import unpack, pack

class RDMpacket:
    startcode = 0xcc
    ssc = 0x01
    length = 0x00
    destuid = bytes(b'\x00'*6)
    srcuid = bytes(b'\x00'*6)
    tn = 0x00
    port_resp = 0x00
    mess_cnt = 0x00
    sub_id = 0x0000
    cc = 0x00
    pid = 0x0000
    pdl = 0x00
    pd = bytearray()
    checksum = 0x0000

    def artserialise(self):
        retval = bytearray()
        retval.extend(self.ssc.to_bytes(1, 'big'))
        retval.extend(self.length.to_bytes(1, 'big'))
        retval.extend(self.destuid)
        retval.extend(self.srcuid)
        retval.extend(self.tn.to_bytes(1, 'big'))
        retval.extend(self.port_resp.to_bytes(1, 'big'))
        retval.extend(self.mess_cnt.to_bytes(1, 'big'))
        retval.extend(self.sub_id.to_bytes(2, 'big'))
        retval.extend(self.cc.to_bytes(1, 'big'))
        retval.extend(self.pid.to_bytes(2, 'big'))
        retval.extend(self.pdl.to_bytes(1, 'big'))
        retval.extend(self.pd)
        retval.extend(self.checksum.to_bytes(2, 'big'))
        return retval

    def LLRPserialise(self):
        pass

    def RDMNetserialise(self):
        pass

    def fromart(self, data: bytes):
        self.ssc = data[0]
        self.length = data[1]
        self.destuid = data[2:8]
        self.srcuid = data[8:14]
        self.tn = data[14]
        self.port_resp = data[15]
        self.mess_cnt = data[16]
        self.sub_id = unpack('!H', data[17:19])[0]
        self.cc = data[19]
        self.pid = unpack('!H', data[20:22])[0]
        self.pdl = data[22]
        if self.pdl>0:
            self.pd = data[23:24+self.pdl]
        self.checksum = unpack('!H', data[-2:])[0]
        return 

    def calcchecksum(self):
        retval = bytearray()
        retval.extend(self.startcode.to_bytes(1, 'big'))
        retval.extend(self.ssc.to_bytes(1, 'big'))
        retval.extend(self.length.to_bytes(1, 'big'))
        retval.extend(self.destuid)
        retval.extend(self.srcuid)
        retval.extend(self.tn.to_bytes(1, 'big'))
        retval.extend(self.port_resp.to_bytes(1, 'big'))
        retval.extend(self.mess_cnt.to_bytes(1, 'big'))
        retval.extend(self.sub_id.to_bytes(2, 'big'))
        retval.extend(self.cc.to_bytes(1, 'big'))
        retval.extend(self.pid.to_bytes(2, 'big'))
        retval.extend(self.pdl.to_bytes(1, 'big'))
        retval.extend(self.pd)
        calc = 0x00
        for byte in retval:
            calc = calc + byte
        self.checksum = calc