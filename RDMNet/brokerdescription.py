"""Broker Description"""
import ipaddress
class BrokerDescription:
    """Placeholder for our broker information for further processing"""
    def __init__(self):
        self.hostname = None
        self.address = None
        self.server = None
        self.scope = None
        self.vers = None
        self.cid = None
        self.model = None
        self.manuf = None
        self.port = None

    def fromzconfinfo(self, info):
        """Creates a broker description from a zconf info object"""
        self.hostname = info.name
        self.address = ipaddress.ip_address(info.address)
        self.port = info.port
        self.server = info.server
        self.scope = info.properties[b'ConfScope'].decode("utf-8")
        self.vers = info.properties[b'E133Vers'].decode("utf-8")
        self.cid = info.properties[b'CID'].decode("utf-8")
        self.model = info.properties[b'Model'].decode("utf-8")
        self.manuf = info.properties[b'Manuf'].decode("utf-8")
