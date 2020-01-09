from RDMNet import vectors
from RDM import rdmpacket

class ACNUDPPreamble:
    def __init__(self):
        self.rlp_preamble_size = 0x0010
        self.rlp_postamble_size = 0x0000
        self.acn_packet_id = bytes(b'\x41\x53\x43\x2d\x45\x31\x2e\x31\x37\x00\x00\x00')

class LLRP_RLP:
    def __init__(self):
        self.flags_length = 0xF00000
        self.vector = vectors.vector_root_llrp
        self.senderCID = bytes(b'\x00' * 16)

class LLRP_PDU:
    def __init__(self):
        self.flags_length = 0xF00000
        self.vector = 0x00000000
        self.destCID = bytes(b'\x00' * 16)
        self.tn = 0x00000000

class LLRPRequestPDU:
    def __init__(self):
        self.flags_length = 0xF00000
        self.vector = vectors.vector_probe_request_data
        self.lowerUID = None
        self.upperUID = None
        self.filter = None
        self.knownUIDs = []

class LLRPReplyPDU:
    def __init__(self):
        self.flags_length = 0xF00000
        self.vector = vectors.vector_llrp_probe_reply
        self.uid = bytes(b'\x00' * 6)
        self.hardware_address = bytes(b'\x00' * 6)
        self.component_type = 0x00

class RDMCommandPDU:
    def __init__(self):
        self.flags_length = 0xF00000
        self.vector = vectors.vector_rdm_cmd_rdm_data
        self.rdmpd = rdmpacket.RDMpacket()


def llrp_rpt_pdu(self, rptpd, srcpdu):
    data = bytearray(b'\x00\x10\x00\x00')
    data.extend(vectors.ACNheader)
    data.extend(b'\xF0\x00\x43')
    data.extend(vectors.vector_root_llrp)
    data.extend(self.cid)
    data.extend(b'\xF0\x00\x2c')
    data.extend(vectors.vector_llrp_rdm_cmd)
    data.extend(srcpdu[23:39])
    data.extend(srcpdu[62:66])
    data.extend(b'\xF0\x00\x11')
    data.extend(b'\xcc')
    data.extend(rptpd)
    # Now Do Length Calculations
    rootpdu = len(rptpd)+22+26+6
    llrppdu = len(rptpd)+26+5
    commandpdu = len(rptpd)+4
    data[17:19] = rootpdu.to_bytes(2, 'big')
    data[40:42] = llrppdu.to_bytes(2, 'big')
    data[67:69] = commandpdu.to_bytes(2, 'big')
    return data
