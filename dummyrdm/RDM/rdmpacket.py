from struct import unpack, pack

class RDMpacket:

    def __init__(self):
        self.startcode = 0xcc
        self.ssc = 0x01
        self.length = 0x00
        self.destuid = bytes(b'\x00'*6)
        self.srcuid = bytes(b'\x00'*6)
        self.tn = 0x00
        self.port_resp = 0x00
        self.mess_cnt = 0x00
        self.sub_id = 0x0000
        self.cc = 0x00
        self.pid = 0x0000
        self.pdl = 0x00
        self.pd = bytearray()
        self.checksum = 0x0000

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
        if self.pdl > 0:
            retval.extend(self.pd)
        retval.extend(self.checksum.to_bytes(2, 'big'))
        return retval

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
        else:
            self.pd = None
        self.checksum = unpack('!H', data[-2:])[0]
        return 

    def calcchecksum(self):
        """ Calculates and appends the checksum of the RDM packet """

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
        if(self.pdl > 0):
            retval.extend(self.pd)
        calc = sum(retval)
        self.checksum = calc

    def checkchecksum(self) -> bool:
        """Checks the checksum of a received RDM Packet 

        Returns:
            correct: A bool of whether the checksum is correct or not
        """
        calc = 0
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
        if(self.pdl > 0):
            retval.extend(self.pd)
        calc = sum(retval[:-1])
        
        if calc == self.checksum:
            return True
        else:
            print("RDM Checksum Failed, PID:{:04x} Calc'ed Checksum: {:04x} Sent Checksum {:04x}, difference: {}".format(self.pid, calc, self.checksum, calc - self.checksum))
            return False
        