"""RDMNet RPT Handlers.
A selection of functions for handling E1.33 RDMNet RPT PDUS.
Where appropriate, functions pass to RDM handlers to modify/exchange
device attributes.

It is expected that data will be passed to these handlers in their full
form, including the RLP preamble and RLP PDU.

"""

from RDMNet import vectors, pdus
from RDM import rdmpacket, gethandlers, nackcodes

def handle(self, data: bytearray) -> None:
    """Switches handler based on RPT PDU vector.

    There may be multiple RPT PDUS enclosed within the RLP Data segment
    """
    print("RPT PDU")
    #Strip the RLP PDU from data
    data = data[23:]
    #Loop through the remaining PDUs
    length = (data[0] << 16) | (data[1] << 8) | data[2]
    pdudata = data[:length]
    if pdudata[3:7] == vectors.vector_rpt_request:
        rptrequest(self, pdudata[:])
    elif pdudata[3:7] == vectors.vector_rpt_status:
        rptstatus(self, pdudata)
    elif pdudata[3:7] == vectors.vector_rpt_notification:
        rptnotification(self, pdudata)
    else:
        print("Unrecognised RPT Vector")
    data = data[length:]
    print("All PDUs processed")

def rptrequest(self, data: bytearray) -> None:
    """Processes an RPT Request PDU.

    RPT Request PDUs can only contain ONE RDM payload.
    """
    #TODO: Handle invalid data
    print("RPT Request")
    sourceuid = data[7:13]
    sourceendpoint = data[13:15]
    destuid = data[15:21]
    destendpoint = data[21:23]
    sequence = data[23:27]
    payload = rdmpacket.RDMpacket()
    payload.fromart(data[39:])
    retpacket = None
    func = self.device_descriptor.llrpswitcher.get(payload.pid, "NACK")
    if func is "NACK":
        func = self.device_descriptor.getswitcher.get(payload.pid, "NACK")
    if func is not "NACK":
        retpacket = func(self, payload)
    else:
        retpacket = gethandlers.nackreturn(self, payload, nackcodes.nack_unknown)

    # Now we have a RDMPacket - add that to a notification PDU and return to sender
    packet = pdus.ACNTCPPreamble()
    rlppacket = pdus.RLPPDU(vectors.vector_root_rpt, self.device_descriptor.cid)
    rptpacket = pdus.RptPdu(vectors.vector_rpt_notification, sourceuid,
                            sourceendpoint, destuid, destendpoint, sequence)
    notifpacket = pdus.RPTNotificationPDU()
    cmdpacket = pdus.RDMCommandPDU()

    cmdpacket.message = retpacket
    notifpacket.message = cmdpacket
    rptpacket.message = notifpacket
    rlppacket.message = rptpacket
    packet.message = rlppacket
    retval = packet.serialise()
    self.writer.write(retval)


def rptstatus(self, data: bytearray) -> None:
    """Processes an RPT Status PDU"""
    print("RPT Status")

def rptnotification(self, data: bytearray) -> None:
    """Processes an RPT Notification PDU

    RPT Notification PDUs contain multiple RDM Command PDUs
    """
    print("RPT Notification")
