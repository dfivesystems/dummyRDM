from RDM import gethandlers, nackcodes, rdmpacket
from LLRP import pdus
from RDMNet import vectors

llrpport = 5569
llrptimeout = 2000
llrp_target_timeout = 500
llrp_multicast_v4_request = '239.255.250.133'
llrp_multicast_v4_response = '239.255.250.134'

llrp_broadcast_cid = b'\xFB\xAD\x82\x2C\xBD\x0C\x4D\x4C\xBD\xC8\x7E\xAB\xEB\xC8\x5A\xFF'

def handlellrp(self, rawdata):
    # Check for ACN Header
    #print("LLRP Handler")
    if rawdata[4:16] != vectors.ACNheader:
        print("Invalid ACN Header")
        return None
    # Check for LLRP Root Vector
    if rawdata[19:23] != vectors.vector_root_llrp:
        print("Non-LLRP Vector")
        return None
    # Check for LLRP PDU Vector
    if rawdata[45] == 1:
        # Probe Request
        #print("Probe Request")
        handlellrprequest(self, rawdata)
    elif rawdata[45] == 2:
        # Probe Reply
        #print("Probe Reply")
        # As we're a device we shall do nothing with the probe reply
        return
    elif rawdata[45] == 3:
        # RDM Command
        #print("LLRP RDM command")
        handlerdm(self, rawdata)
    else:
        # Invalid Vector
        print("Invalid LLRP Vector")
        print(rawdata[45])
        return None
    return

def handlellrprequest(self, pdu):
    request = pdus.LLRPRequestPDU()
    request.senderCID = pdu[23:39]
    request.lowerUID = pdu[70:76]
    request.upperUID = pdu[76:82]
    request.filter = pdu[82]
    kid = pdu[83:]
    # BUG: Doesnt seem to work...
    for x in range(0, len(kid), 6):
        request.knownUIDs.append(kid[x:x+6])
    if request.knownUIDs.__contains__(self.device_descriptor.uid):
        return None
    # Respond to Request
    #TODO: Make this class based for tidyness
    data = bytearray(b'\x00\x10\x00\x00')
    data.extend(vectors.ACNheader)
    data.extend(b'\xF0\x00\x43')
    data.extend(vectors.vector_root_llrp)
    data.extend(self.device_descriptor.cid)
    data.extend(b'\xF0\x00\x2c')
    data.extend(b'\x00\x00\x00\x02')
    data.extend(request.senderCID)
    data.extend(pdu[62:66])
    data.extend(b'\xF0\x00\x11')
    data.extend(b'\x01')
    data.extend(self.device_descriptor.uid)
    data.extend(self.device_descriptor.uid)
    data.extend(b'\x00')
    self.transport.sendto(data, (llrp_multicast_v4_response, 5569))


def handlerdm(self, pdu):
    # Check cid is ours
    if pdu[46:62] != self.device_descriptor.cid:
        print("Incorrect CID - ignoring")
        return None
    # Check UID is ours
    if pdu[72:78] != self.device_descriptor.uid:
        print("Incorrect UID - ignoring")
        return None
    # Process the packet
    #Now we know it's ours, make an RDM packet for the source
    srcpacket = rdmpacket.RDMpacket()
    srcpacket.fromart(pdu[70:])
    if not srcpacket.checkchecksum():
        return None
    func = self.device_descriptor.llrpswitcher.get(srcpacket.pid, "NACK")  
    if func is not "NACK":
        returnpacket = func(self, srcpacket)
        pdu = pdus.llrp_rpt_pdu(self, returnpacket.artserialise(), pdu)
        self.transport.sendto(pdu, (llrp_multicast_v4_response, 5569))
    else:
        print("Device {} does not support PID:0x{:04x} on LLRP target".format(self.uid.hex(), srcpacket.pid))
        returnpacket = gethandlers.nackreturn(self, srcpacket, nackcodes.nack_unknown)
        pdu = pdus.llrp_rpt_pdu(self, returnpacket.artserialise(), pdu)
        self.transport.sendto(pdu, (llrp_multicast_v4_response, 5569))
    return

