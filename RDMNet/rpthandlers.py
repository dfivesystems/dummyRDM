from RDMNet import pdus, vectors

def handle(self, data):
    if data[42:46] == vectors.vector_rpt_request:
        rptrequest(self, data)
        return
    elif data[42:46] == vectors.vector_rpt_status:
        rptstatus(self, data)
        return
    elif data[42:46] == vectors.vector_rpt_notification:
        rptnotification(self, data)
        return
    else:
        print("Unrecongnised RPT Vector")

def rptrequest(self, data):
    pass

def rptstatus(self, data):
    pass

def rptnotification(self, data):
    pass