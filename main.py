from RDMDevice import rdmdevice
from ArtNet import artnet
from LLRP import llrp
import _thread
from WebEngine import webengine

#from RDMnet import rdmnet

devicestore = dict()
def main():
    artnetengine = artnet.dummyartnode("192.168.1.195/24", devicestore, 0, 14)
    artnetengine.start()
    devicestore[0] = rdmdevice.rdmdevice()
    devicestore[0].start()
    artnetengine.registerdevice(0, 0)
    web = webengine.WebServer()
    web.run()

if __name__ == "__main__":
    main()
