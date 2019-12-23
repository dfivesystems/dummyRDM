import struct
import socket
from threading import Thread
from RDM import gethandlers, sethandlers, nackcodes, rdmpacket
from LLRP import pdus
from RDMNetCommon import vectors

llrpport = 5569
llrptimeout = 2000
llrp_target_timeout = 500
llrp_multicast_v4_request = '239.255.250.133'
llrp_multicast_v4_response = '239.255.250.134'

llrp_broadcast_cid = b'\xFB\xAD\x82\x2C\xBD\x0C\x4D\x4C\xBD\xC8\x7E\xAB\xEB\xC8\x5A\xFF'

def handlellrp(self, rawdata):
    # Check for ACN Header
    print("LLRP Handler")
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
        print("Probe Request")
        handlellrprequest(self, rawdata)
    elif rawdata[45] == 2:
        # Probe Reply
        print("Probe Reply")
        # As we're a device we shall do nothing with the probe reply
        return
    elif rawdata[45] == 3:
        # RDM Command
        print("LLRP RDM command")
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
    for x in range(0, len(kid), 6):
        request.knownUIDs.append(kid[x:x+6])
    if request.knownUIDs.__contains__(self.uid):
        return None
    # Respond to Request
    #TODO: Make this class based for tidyness
    data = bytearray(b'\x00\x10\x00\x00')
    data.extend(vectors.ACNheader)
    data.extend(b'\xF0\x00\x43')
    data.extend(vectors.vector_root_llrp)
    data.extend(self.cid)
    data.extend(b'\xF0\x00\x2c')
    data.extend(b'\x00\x00\x00\x02')
    data.extend(request.senderCID)
    data.extend(b'\x00\x00\x00\x00')
    data.extend(b'\xF0\x00\x11')
    data.extend(b'\x02')
    data.extend(self.uid)
    data.extend(self.uid)
    data.extend(b'\x00')
    self.llrpsocket.sendto(data, (llrp_multicast_v4_response, 5569))


def handlerdm(self, pdu):
    # Check cid is ours
    if pdu[46:62] != self.cid:
        print("Incorrect CID - ignoring")
        return None
    # Check UID is ours
    if pdu[72:78] != self.uid:
        print("Incorrect UID - ignoring")
        return None
    # Process the packet
    #Now we know it's ours, make an RDM packet for the source
    srcpacket = rdmpacket.RDMpacket()
    srcpacket.fromart(pdu[70:])
    if not srcpacket.checkchecksum():
        return None
    pid = struct.unpack('!H', pdu[90: 92])[0]
    commandclass = pdu[89]
    if pid not in self.llrppidlist:
        print("PID not in device llrppidlist")
        returnpacket = gethandlers.nackreturn(self, pid, nackcodes.nack_unknown, srcpacket)
        pdu = pdus.llrp_rpt_pdu(self, returnpacket.artserialise(), pdu)
        self.llrpsocket.sendto(pdu, (llrp_multicast_v4_response, 5569))
        return
    if commandclass == 0x20:
        #TODO: Make this behave similarly to artnet PID handlers
        if pid == 0x0060:
            returnpacket = gethandlers.devinfo(self, srcpacket)
            pdu = pdus.llrp_rpt_pdu(self, returnpacket.artserialise(), pdu)
            self.llrpsocket.sendto(pdu, (llrp_multicast_v4_response, 5569))
        elif pid == 0x0081:
            returnpacket = gethandlers.devmanufacturer(self, srcpacket)
            pdu = pdus.llrp_rpt_pdu(self, returnpacket.artserialise(), pdu)
            self.llrpsocket.sendto(pdu, (llrp_multicast_v4_response, 5569))
        elif pid == 0x0080:
            returnpacket = gethandlers.devmodel(self, srcpacket)
            pdu = pdus.llrp_rpt_pdu(self, returnpacket.artserialise(), pdu)
            self.llrpsocket.sendto(pdu, (llrp_multicast_v4_response, 5569))
        elif pid == 0x0800:
            returnpacket = gethandlers.devscope(self, srcpacket)
            pdu = pdus.llrp_rpt_pdu(self, returnpacket.artserialise(), pdu)
            self.llrpsocket.sendto(pdu, (llrp_multicast_v4_response, 5569))
        elif pid == 0x1001:
            # NACK get of device reset
            returnpacket = gethandlers.nackreturn(self, pid, nackcodes.nack_unsupported_cc, srcpacket)
            pdu = pdus.llrp_rpt_pdu(self, returnpacket.artserialise(), pdu)
            self.llrpsocket.sendto(pdu, (llrp_multicast_v4_response, 5569))
        elif pid == 0x0090:
            # NACK get of factory reset
            returnpacket = gethandlers.nackreturn(self, pid, nackcodes.nack_unsupported_cc, srcpacket)
            pdu = pdus.llrp_rpt_pdu(self, returnpacket.artserialise(), pdu)
            self.llrpsocket.sendto(pdu, (llrp_multicast_v4_response, 5569))
        elif pid == 0x0082:
            returnpacket = gethandlers.devlabel(self, srcpacket)
            pdu = pdus.llrp_rpt_pdu(self, returnpacket.artserialise(), pdu)
            self.llrpsocket.sendto(pdu, (llrp_multicast_v4_response, 5569))
        elif pid == 0x1000:
            print("PID: Identify Device")
            # TODO: Return Status
        elif pid == 0x0801:
            returnpacket = gethandlers.devsearch(self, srcpacket)
            pdu = pdus.llrp_rpt_pdu(self, returnpacket.artserialise(), pdu)
            self.llrpsocket.sendto(pdu, (llrp_multicast_v4_response, 5569))
        else:
            print("Non-recognised PID (LLRP, GET)")
            returnpacket = gethandlers.nackreturn(self, pid, nackcodes.nack_unknown, srcpacket)
            pdu = pdus.llrp_rpt_pdu(self, returnpacket.artserialise(), pdu)
            self.llrpsocket.sendto(pdu, (llrp_multicast_v4_response, 5569))
    elif commandclass == 0x30:
        print("Set Command")
        if pid == 0x0060:
            print("PID: Device Info")
            returnpacket = gethandlers.nackreturn(self, pid, nackcodes.nack_unsupported_cc, srcpacket)
            pdu = pdus.llrp_rpt_pdu(self, returnpacket.artserialise(), pdu)
            self.llrpsocket.sendto(pdu, (llrp_multicast_v4_response, 5569))
        elif pid == 0x0081:
            print("PID: Device Manufacturer")
            returnpacket = gethandlers.nackreturn(self, pid, nackcodes.nack_unsupported_cc, srcpacket)
            pdu = pdus.llrp_rpt_pdu(self, returnpacket.artserialise(), pdu)
            self.llrpsocket.sendto(pdu, (llrp_multicast_v4_response, 5569))
        elif pid == 0x0080:
            print("PID: Device Model")
            returnpacket = gethandlers.nackreturn(self, pid, nackcodes.nack_unsupported_cc, srcpacket)
            pdu = pdus.llrp_rpt_pdu(self, returnpacket.artserialise(), pdu)
            self.llrpsocket.sendto(pdu, (llrp_multicast_v4_response, 5569))
        elif pid == 0x7FEF:
            print("PID: Device Scope")
        elif pid == 0x1001:
            print("PID: Device Reset")
        elif pid == 0x0090:
            print("PID: Factory Reset")
        elif pid == 0x0082:
            print("PID: Device Label")
        elif pid == 0x1000:
            print("PID: Identify Device")
        elif pid == 0x7FE0:
            print("PID: Search Domain")
        else:
            print("Non-recognised PID (LLRP, SET)")
            returnpacket = gethandlers.nackreturn(self, pid, nackcodes.nack_unknown, srcpacket)
            pdu = pdus.llrp_rpt_pdu(self, returnpacket.artserialise(), pdu)
            self.llrpsocket.sendto(pdu, (llrp_multicast_v4_response, 5569))
    return None
