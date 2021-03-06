import sys
from zeroconf import ServiceBrowser, Zeroconf
from RDMDevice import rdmdevice
from ArtNet import artnet
from WebEngine import webengine
from RDMNet import zconflistener

#TODO: Make this ... better

devicestore = dict()
def dummyrdm():
    zeroconf = Zeroconf()
    listener = zconflistener.ZConfListener(devicestore)
    browser = ServiceBrowser(zeroconf, "_rdmnet._tcp.local.", listener)
    artnetengine = artnet.dummyartnode("192.168.3.2/24", devicestore, 0, 14)
    artnetengine.start()
    devicestore[0] = rdmdevice.RdmDevice()
    devicestore[0].start()
    artnetengine.registerdevice(0, 0)
    web = webengine.WebServer()
    web.run()

if __name__ == "__main__":
    try:
        dummyrdm()
    except KeyboardInterrupt:
        sys.exit()
