import sys
import socket
import ipaddress
from struct import unpack
from threading import Thread, current_thread
from ArtNet import opcodes, packets, handlers, ports

class dummyartnode(Thread):
    """Class Implementing an Art-Net Node, capable of emulating devices on a single port"""

    HOST = None
    ArtNetPort = 6454
    startuniverse = 0
    subsw = 0
    netsw = 0
    portcount = 0
    artnetsocket = None
    artnetunicastsocket = None
    ports = dict() 

    def __init__(self, hostaddress: str, devicestore: dict, startuniverse: int = 0, portcount: int = 4): 
        """Initialise the Art-Net Node with a hostaddress(CIDR notation), startuniverse(optional) and port count(optional)"""

        super().__init__()
        current_thread().name = "Art-Net Engine"
        self.devicestore = devicestore
        self.HOST = ipaddress.IPv4Interface(hostaddress)
        self.startuniverse = startuniverse
        self.portcount = portcount
        self.startuniverse = startuniverse % 16
        self.subsw = startuniverse  % 256 // 16
        self.netsw = startuniverse // 256
        for x in range(portcount):
            self.ports[x] = ports.dummyport(self.startuniverse + x)
        try:
            self.artnetsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        except socket.error:
            print('Failed to open Art-Net Socket, shutting down')
            sys.exit()
        self.artnetsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.artnetsocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.artnetsocket.bind(('', self.ArtNetPort))
        try:
            self.artnetunicastsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        except socket.error:
            print('Failed to open Art-Net Unicast Socket, shutting down')
            sys.exit()
        self.artnetunicastsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.artnetunicastsocket.bind((self.HOST.ip.exploded, self.ArtNetPort))
        self.artnetunicastsocket.setblocking(0)
        print("Artnet Listening on {0}:{1}".format(self.HOST.ip, self.ArtNetPort))
        self.setDaemon(True)
        return
        

    def run(self):
        """Main Method for running a dummyartnode in a separate thread"""

        while True:
            data, addr = self.artnetsocket.recvfrom(1024)
            packet = self.packethandler(data)
            if packet is not None:
                tosend = packet.serialise()
                try:
                    self.artnetsocket.sendto(tosend, (self.HOST.network.broadcast_address.exploded, 6454))
                except socket.error as e:
                    print("Socket error{0}".format(e))
            else:
                # No Processing required
                pass
            #Then Handle Unicast Data Separately
            try:
                unidata, uniaddr = self.artnetunicastsocket.recvfrom(1024)
                unipacket = self.packethandler(unidata)
                if unipacket is not None:
                    tosend = unipacket.serialise()
                    try:
                        self.artnetunicastsocket.sendto(tosend, (uniaddr[0], 6454))
                    except socket.error as e:
                        print("Socket error{0}".format(e))
                else:
                    # No Processing required
                    pass
            except OSError:
                pass

    def packethandler(self, raw_data):
        """Returns a packet if informations has been requested from this node, otherwise returns None"""

        if unpack('!8s', raw_data[:8])[0] != opcodes.ARTNET_HEADER:
            print("None Art-Net Packet")
            return None
        #print("ArtNet Packet Received")
        opcode = unpack('!H', raw_data[8:10])
        opcode = opcode[0] << 8       
        switcher = {
            opcodes.OpPoll: handlers.oppollhandler,
            opcodes.OpPollReply: handlers.oppollreplyhandler,
            opcodes.OpDmx: handlers.opDMXhandler,
            opcodes.OpTodRequest: handlers.opTodRequesthandler,
            opcodes.OpTodData: handlers.opTodDatahandler,
            opcodes.OpRdm: handlers.opRdmHandler,
        }
        func = switcher.get(opcode, "Invalid Opcode")
        if func is not "Invalid Opcode":
            return func(self, raw_data)
        else:
            print("None-handled Opcode: {:02X}".format(opcode))
            return None

    def registerdevice(self, deviceposition, port):
        """Registers a device position with the port TOD, not only positions are stored to save copying objects"""
        if port in self.ports:
            self.ports[port].tod.append(deviceposition)
