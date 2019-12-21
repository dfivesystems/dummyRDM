from RDMNetCommon import vectors

def llrp_rpt_pdu(self, rptpd, srcpdu):
    data = bytearray(b'\x00\x10\x00\x00')
    data.extend(self.ACNheader)
    data.extend(b'\xF0\x00\x43')
    data.extend(vectors.vector_root_llrp)
    data.extend(self.cid.bytes)
    data.extend(b'\xF0\x00\x2c')
    data.extend(b'\x00\x00\x00\x03')
    data.extend(srcpdu[23:39])
    data.extend(srcpdu[62:66])
    data.extend(b'\xF0\x00\x11')
    data.extend(rptpd)
    # Now Do Length Calculations
    rootpdu = len(rptpd)+22+26+5
    llrppdu = len(rptpd)+26+4
    commandpdu = len(rptpd)+3
    data[17:19] = rootpdu.to_bytes(2, 'big')
    data[40:42] = llrppdu.to_bytes(2, 'big')
    data[67:69] = commandpdu.to_bytes(2, 'big')
    return data
