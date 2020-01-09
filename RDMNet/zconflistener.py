from RDMNet import brokerdescription

class ZConfListener:
    def __init__(self, devicestore):
        self.devicestore = devicestore

    def remove_service(self, zeroconf, srvtype, name):
        info = zeroconf.get_service_info(srvtype, name)
        desc = brokerdescription.BrokerDescription()
        desc.fromzconfinfo(info)
        for i in self.devicestore:
            self.devicestore[i].disconnectbroker(desc)

    def add_service(self, zeroconf, srvtype, name):
        info = zeroconf.get_service_info(srvtype, name)
        desc = brokerdescription.BrokerDescription()
        desc.fromzconfinfo(info)
        for i in self.devicestore:
            self.devicestore[i].newbroker(desc)