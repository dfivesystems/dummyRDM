"""A zeroconf listener for an RDMNet device."""
from RDMNet import brokerdescription

class ZConfListener:
    """The Zeroconf listener class as required by py-zeroconf."""
    def __init__(self, devicestore: list) -> None:
        self.devicestore = devicestore

    def remove_service(self, zeroconf, srvtype, name) -> None:
        """Removal of a service from the browser.

        Loops through the devices and disconnects

        """

        for i in self.devicestore:
            self.devicestore[i].disconnectbroker()

    def add_service(self, zeroconf, srvtype, name) -> None:
        """Adding of a service to the broker.

        Loops through devices in devicestore and runs the
        connect function

        """
        info = zeroconf.get_service_info(srvtype, name)
        desc = brokerdescription.BrokerDescription()
        desc.fromzconfinfo(info)
        for i in self.devicestore:
            self.devicestore[i].newbroker(desc)
