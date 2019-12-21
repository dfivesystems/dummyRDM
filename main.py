from RDMDevice import rdmdevice
from ArtNet import artnet
from LLRP import llrp
import _thread

#from RDMnet import rdmnet

devicestore = dict()
#TODO: Document everything correctly
if __name__ == "__main__":
    llrpengine = llrp.dummyllrp()
    llrpengine.start()
    artnetengine = artnet.dummyartnode("192.168.3.2/24", devicestore, 30)
    artnetengine.start()
    devicestore[0] = rdmdevice.rdmdevice()
    artnetengine.registerdevice(0, 0)
    while True:
        pass
