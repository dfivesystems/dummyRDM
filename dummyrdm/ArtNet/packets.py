import ipaddress
from ArtNet import opcodes
from RDM import rdmpacket

#TODO: Add remaining relevant opcodes
class ArtNetDataPacket:
    def __init__(self):
        self.opcode = None
        self.ver = None
        self.sequence = None
        self.physical = None
        self.universe = None
        self.length = None
        self.data = None

class ArtNetPollPacket:
    """A Class for storing information received in a ArtPoll packet"""
    def __init__(self):
        self.opcode = None
        self.ver = None
        self.talktome = None
        self.priority = None

class ArtNetPollReplyPacket:
    """A class for the ArtPollReply packet - Set values as
    appropriate and then use serialise() for sending to the
    network, or serialisev4(portid) for artnetv4 devices"""

    def __init__(self):
        self.opcode = 0x2100
        self.ipaddr = ipaddress.ip_address("0.0.0.0")
        self.port = 0x1936
        self.ver = 0x0101
        self.NetSw = 0x00
        self.SubSw = 0x00
        self.Oem = 0x2986
        self.UBEA = 0x00
        self.Status1 = 0x00
        self.EstaMan = 0x7ff0
        self.Shortname = "Dummy ArtRDM Node"
        self.Longname = "D5 Systems Dummy ArtRDM Node"
        self.NodeReport = "Running"
        self.NumportsHi = 0x00
        self.NumportsLo = 0x00
        self.PortTypes = [0xc0, 0xc0, 0xc0, 0xc0]
        self.GoodInput = [0x00, 0x00, 0x00, 0x00]
        self.GoodOutput =[0x00, 0x00, 0x00, 0x00]
        self.SwIn = [0x00, 0x00, 0x00, 0x00]
        self.SwOut = [0x00, 0x00, 0x00, 0x00]
        self.SwVideo = 0x00
        self.SwMacro = 0x00
        self.SwRemote = 0x00
        self.Spare = [0x00, 0x00, 0x00]
        self.Style = 0x00
        self.Mac = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        self.BindIp = ipaddress.ip_address("0.0.0.0")
        self.BindIndex = 0x01
        self.Status2 = 0x00
        self.Filler = [0x00] * 26

    def serialise(self) -> bytearray:
        """Returns a ByteArray object for sending over the network"""

        tosend = bytearray()
        tosend.extend(b'Art-Net\x00')
        tosend.extend(self.opcode.to_bytes(2, 'little'))
        tosend.extend(self.ipaddr.packed)
        tosend.extend(self.port.to_bytes(2, 'big'))
        tosend.extend(self.ver.to_bytes(2, 'big'))
        tosend.append(self.NetSw)#NetSw
        tosend.append(self.SubSw)#SubSw
        tosend.extend(self.Oem.to_bytes(2, 'big'))
        tosend.extend(self.UBEA.to_bytes(1, 'big'))#UBEA
        tosend.extend(self.Status1.to_bytes(1, 'big'))
        tosend.extend(self.EstaMan.to_bytes(2, 'big'))
        tosend.extend(bytes('{:<18}'.format(self.Shortname), 'utf8'))
        tosend.extend(bytes('{:<64}'.format(self.Longname), 'utf8'))
        tosend.extend(bytes('{:<64}'.format(self.NodeReport), 'utf8'))
        tosend.append(self.NumportsHi)
        tosend.append(self.NumportsLo)
        tosend.extend(self.PortTypes)
        tosend.extend(self.GoodInput)
        tosend.extend(self.GoodOutput)
        tosend.extend(self.SwIn)
        tosend.extend(self.SwOut)
        tosend.extend(b'\x00'*6)
        tosend.extend(self.Style.to_bytes(1, 'big'))
        tosend.extend(self.Mac)
        tosend.extend(self.BindIp.packed)
        tosend.extend(self.BindIndex.to_bytes(1, 'big'))
        tosend.extend(b'\x00'*27)
        return tosend

class ArtTodRequestPacket:
    """A Class for holding the data contained within an ArtTodRequest"""
    
    def __init__(self):
        self.opcode = 0x0000
        self.net = 0x00
        self.command = 0x00
        self.addcount = 0x00
        self.address = list()

class ArtTodDataPacket:
    """A class for holding the data for an ArtTodData packet

    Use serialise() to convert to bytes for sending over network"""

    def __init__(self):
        self.opcode = 0x8100
        self.ver = 0x0101
        self.rdmver = 0x01
        self.port = 0x01
        self.spare = [0x00] *6
        self.BindIndex = 0x00
        self.Net = 0x00
        self.CommandResponse = 0x00
        self.Address = 0x00
        self.uidtotal = 0x0000
        self.blockcount = 0x00
        self.uidcount = 0x00
        self.tod = list()

    def serialise(self):
        """Returns a Byte array representation of ArtTodDatapacket for network transport"""
        
        tosend = bytearray()
        tosend.extend(b'Art-Net\x00')
        tosend.extend(self.opcode.to_bytes(2, 'little'))
        tosend.extend(self.ver.to_bytes(2, 'big'))
        tosend.extend(self.rdmver.to_bytes(1, 'big'))
        tosend.extend((self.port+1).to_bytes(1, 'big'))
        tosend.extend(b'\x00'*6)
        tosend.extend(self.BindIndex.to_bytes(1, 'big'))
        tosend.extend(self.Net.to_bytes(1, 'big'))
        tosend.extend(self.CommandResponse.to_bytes(1, 'big'))
        tosend.extend(self.Address.to_bytes(1, 'big'))
        tosend.extend(self.uidtotal.to_bytes(2, 'big'))
        tosend.extend(self.blockcount.to_bytes(1, 'big'))
        tosend.extend(self.uidcount.to_bytes(1, 'big'))
        for todentry in self.tod:
            tosend.extend(todentry)
        return tosend

class ArtRDMPacket:
    """A class for holding the data for an ArtRDM packet

    Use serialise() to convert to bytes for sending over network"""

    def __init__(self):
        self.opcode = 0x8300
        self.ver = 0x0101
        self.rdmver =0x01
        self.net = 0x00
        self.command = 0x00
        self.address = 0x00
        self.rdmpd = rdmpacket.RDMpacket()

    def serialise(self) -> bytearray:
        tosend = bytearray()
        tosend.extend(b'Art-Net\x00')
        tosend.extend(self.opcode.to_bytes(2, 'little'))
        tosend.extend(self.ver.to_bytes(2, 'big'))
        tosend.extend(self.rdmver.to_bytes(1, 'big'))
        tosend.extend(b'\x00' * 8)
        tosend.extend(self.net.to_bytes(1, 'big'))
        tosend.extend(self.command.to_bytes(1, 'big'))
        tosend.extend(self.address.to_bytes(1, 'big'))
        tosend.extend(self.rdmpd.artserialise())
        
        return tosend
    