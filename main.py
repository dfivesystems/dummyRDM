from RDMDevice import rdmdevice
from ArtNet import artnet
from LLRP import llrp
import _thread

#from RDMnet import rdmnet

devicestore = dict()
if __name__ == "__main__":
    artnetengine = artnet.dummyartnode("192.168.1.195/24", devicestore, 0, 14)
    artnetengine.start()
    devicestore[0] = rdmdevice.rdmdevice()
    devicestore[0].start()
    artnetengine.registerdevice(0, 0)
    while True:
        pass
