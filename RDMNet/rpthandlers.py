"""RDMNet RPT Handlers.
A selection of functions for handling E1.33 RDMNet RPT PDUS.
Where appropriate, functions pass to RDM handlers to modify/exchange
device attributes.

It is expected that data will be passed to these handlers in their full
form, including the RLP preamble and RLP PDU.

"""

from RDMNet import vectors

def handle(self, data):
    """Switches handler based on RPT PDU vector."""
    if data[42:46] == vectors.vector_rpt_request:
        rptrequest(self, data)
    elif data[42:46] == vectors.vector_rpt_status:
        rptstatus(self, data)
    elif data[42:46] == vectors.vector_rpt_notification:
        rptnotification(self, data)
    else:
        print("Unrecongnised RPT Vector")

def rptrequest(self, data):
    """Processes an RPT Request PDU"""
    print("RPT Request")

def rptstatus(self, data):
    """Processes an RPT Status PDU"""
    print("RPT Status")

def rptnotification(self, data):
    """Processes an RPT Notification PDU"""
    print("RPT Notification")