import struct
from threading import Thread
from RDM import gethandlers, sethandlers, nackcodes
from RDM import sethandlers
from LLRP import pdus
from RDMNetCommon import vectors

llrpport = 5569
llrptimeout = 2000
llrp_target_timeout = 500
llrp_multicast_v4_request = '239.255.250.133'
llrp_multicast_v4_response = '239.255.250.134'

class dummyllrp(Thread):
    """Provides an LLRP Handler for a set of DummyRDMdevices"""
    """    # Sockets
    llrpsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    # ACN Parameters
    ACNheader = b'\x41\x53\x43\x2d\x45\x31\x2e\x31\x37\x00\x00\x00'

    llrp_broadcast_cid = b'\xFB\xAD\x82\x2C\xBD\x0C\x4D\x4C\xBD\xC8\x7E\xAB\xEB\xC8\x5A\xFF'

    def rundevice(self):
        self.llrpsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.llrpsocket.bind(("0.0.0.0", llrp.llrpport))
        mreq = struct.pack("4sl", socket.inet_aton(llrp.llrp_multicast_v4_request), socket.INADDR_ANY)
        self.llrpsocket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        print("LLRP Listening")
        while True:
            data, addr = self.llrpsocket.recvfrom(1024)
            llrp.handlellrp(self, data)"""
    def __init__(self):
        super().__init__()
        pass

    def run(self):
        pass

class LLRPRequestPDU:
    def __init__(self):
        self.senderCID = None
        self.lowerUID = None
        self.upperUID = None
        self.filter = None
        self.knownUIDs = []


def handlellrp(self, rawdata):
    # Check for ACN Header
    print("LLRP Handler")
    if rawdata[4:16] != self.ACNheader:
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
    request = LLRPRequestPDU()
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
    data = bytearray(b'\x00\x10\x00\x00')
    data.extend(self.ACNheader)
    data.extend(b'\xF0\x00\x43')
    data.extend(vectors.vector_root_llrp)
    data.extend(self.cid.bytes)
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
    if pdu[46:62] != self.cid.bytes:
        print("Incorrect CID - ignoring")
        return None
    # Check UID is ours
    if pdu[72:78] != self.uid:
        print("Incorrect UID - ignoring")
        return None
    # Check Checksum
    # TODO: Add Checksum Check
    # Process the packet
    pid = struct.unpack('!H', pdu[90: 92])[0]
    commandclass = pdu[89]
    if pid not in self.llrppidlist:
        print("PID not in device llrppidlist")
        rdmpacket = gethandlers.nackreturn(self, pid, nackcodes.nack_unknown, pdu)
        pdu = pdus.llrp_rpt_pdu(self, rdmpacket, pdu)
        self.llrpsocket.sendto(pdu, (llrp_multicast_v4_response, 5569))
        return
    if commandclass == 0x20:
        if pid == 0x0060:
            rdmpacket = gethandlers.devinfo(self, pdu)
            pdu = pdus.llrp_rpt_pdu(self, rdmpacket, pdu)
            self.llrpsocket.sendto(pdu, (llrp_multicast_v4_response, 5569))
        elif pid == 0x0081:
            rdmpacket = gethandlers.devmanufacturer(self, pdu)
            pdu = pdus.llrp_rpt_pdu(self, rdmpacket, pdu)
            self.llrpsocket.sendto(pdu, (llrp_multicast_v4_response, 5569))
        elif pid == 0x0080:
            rdmpacket = gethandlers.devmodel(self, pdu)
            pdu = pdus.llrp_rpt_pdu(self, rdmpacket, pdu)
            self.llrpsocket.sendto(pdu, (llrp_multicast_v4_response, 5569))
        elif pid == 0x7FEF:
            rdmpacket = gethandlers.devscope(self, pdu)
            pdu = pdus.llrp_rpt_pdu(self, rdmpacket, pdu)
            self.llrpsocket.sendto(pdu, (llrp_multicast_v4_response, 5569))
        elif pid == 0x1001:
            # NACK get of device reset
            rdmpacket = gethandlers.nackreturn(self, pid, nackcodes.nack_unsupported_cc, pdu)
            pdu = pdus.llrp_rpt_pdu(self, rdmpacket, pdu)
            self.llrpsocket.sendto(pdu, (llrp_multicast_v4_response, 5569))
        elif pid == 0x0090:
            # NACK get of factory reset
            rdmpacket = gethandlers.nackreturn(self, pid, nackcodes.nack_unsupported_cc, pdu)
            pdu = pdus.llrp_rpt_pdu(self, rdmpacket, pdu)
            self.llrpsocket.sendto(pdu, (llrp_multicast_v4_response, 5569))
        elif pid == 0x0082:
            rdmpacket = gethandlers.devlabel(self, pdu)
            pdu = pdus.llrp_rpt_pdu(self, rdmpacket, pdu)
            self.llrpsocket.sendto(pdu, (llrp_multicast_v4_response, 5569))
        elif pid == 0x1000:
            print("PID: Identify Device")
            # TODO: Return Status
        elif pid == 0x7FE0:
            rdmpacket = gethandlers.devsearch(self, pdu)
            pdu = pdus.llrp_rpt_pdu(self, rdmpacket, pdu)
            self.llrpsocket.sendto(pdu, (llrp_multicast_v4_response, 5569))
        else:
            print("Non-recognised PID (LLRP, GET)")
            rdmpacket = gethandlers.nackreturn(self, pid, nackcodes.nack_unknown, pdu)
            pdu = pdus.llrp_rpt_pdu(self, rdmpacket, pdu)
            self.llrpsocket.sendto(pdu, (llrp_multicast_v4_response, 5569))
    elif commandclass == 0x30:
        print("Set Command")
        if pid == 0x0060:
            print("PID: Device Info")
            rdmpacket = gethandlers.nackreturn(self, pid, nackcodes.nack_unsupported_cc, pdu)
            pdu = pdus.llrp_rpt_pdu(self, rdmpacket, pdu)
            self.llrpsocket.sendto(pdu, (llrp_multicast_v4_response, 5569))
        elif pid == 0x0081:
            print("PID: Device Manufacturer")
            rdmpacket = gethandlers.nackreturn(self, pid, nackcodes.nack_unsupported_cc, pdu)
            pdu = pdus.llrp_rpt_pdu(self, rdmpacket, pdu)
            self.llrpsocket.sendto(pdu, (llrp_multicast_v4_response, 5569))
        elif pid == 0x0080:
            print("PID: Device Model")
            rdmpacket = gethandlers.nackreturn(self, pid, nackcodes.nack_unsupported_cc, pdu)
            pdu = pdus.llrp_rpt_pdu(self, rdmpacket, pdu)
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
            rdmpacket = gethandlers.nackreturn(self, pid, nackcodes.nack_unknown, pdu)
            pdu = pdus.llrp_rpt_pdu(self, rdmpacket, pdu)
            self.llrpsocket.sendto(pdu, (llrp_multicast_v4_response, 5569))
    return None
