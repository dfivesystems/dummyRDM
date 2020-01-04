import ipaddress
import socket
from ArtNet import packets
from struct import unpack


def oppollhandler(self, raw_data):
    """Takes an OpPollPacket and returns an OpPollReplyPacket"""
    opcode = unpack('!H', raw_data[8:10])
    opcode = opcode[0] << 8
    packet = packets.ArtNetPollPacket()
    packet.opcode = opcode
    if self.portcount <= 4:
        returnpacket = packets.ArtNetPollReplyPacket()
        returnpacket.ipaddr = self.HOST.ip
        returnpacket.NumportsLo = self.portcount
        returnpacket.NetSw = self.netsw
        returnpacket.SubSw = self.subsw
        for x in range(self.portcount):
            returnpacket.SwIn[x] = self.ports[x].universe 
            returnpacket.SwOut[x] = self.ports[x].universe 
        return returnpacket
    else:
        for x in range(self.portcount):
            returnpacket = packets.ArtNetPollReplyPacket()
            returnpacket.ipaddr = self.HOST.ip
            returnpacket.NumportsLo = 0x01
            returnpacket.NetSw = self.netsw
            returnpacket.SubSw = self.subsw
            returnpacket.SwIn[0] = self.ports[x].universe 
            returnpacket.SwOut[0] = self.ports[x].universe
            if(x>0):
                returnpacket.BindIndex = x+1
                returnpacket.BindIp = self.HOST.ip
            try:
                self.artnetsocket.sendto(returnpacket.serialise(), (self.HOST.network.broadcast_address.exploded, 6454))
            except socket.error as e:
                print("Socket error{0}".format(e))

def oppollreplyhandler(self, raw_data):
    #TODO: maybe we build a table of nearby devices with this information
    pass

def opDMXhandler(self, raw_data):
    """Checks if universe is in the node's range and places the DMX data into the buffer if appropriate, and returns None"""
    opcode = unpack('!H', raw_data[8:10])
    opcode = opcode[0] << 8
    packet = packets.ArtNetDataPacket()
    packet.opcode = opcode
    (packet.length,) = unpack('!H', raw_data[16:18])
    (packet.universe,) = unpack('<H', raw_data[14:16])
    (packet.data,) = unpack('{0}s'.format(512), raw_data[18:18 + 512])
    #TODO: Place data into buffer if required
    return None

def opTodRequesthandler(self, raw_data):
    #TODO: Add options for greater than 200 UIDs in the TOD
    opcode = unpack('!H', raw_data[8:10])
    opcode = opcode[0] << 8
    packet = packets.ArtTodRequestPacket()
    packet.opcode = opcode
    packet.net = int(raw_data[21])
    packet.command = int(raw_data[22])
    packet.addcount = int(raw_data[23])
    for x in range(packet.addcount):
        packet.address.append(int(raw_data[24+x]))
    for address in packet.address:
        for portnum in range(self.portcount):
            if self.ports[portnum].universe+(self.subsw*16) == address:
                returnpacket = packets.ArtTodDataPacket()
                returnpacket.Net = self.netsw
                returnpacket.port = portnum
                returnpacket.Address = address
                returnpacket.uidtotal = len(self.ports[portnum].tod)
                returnpacket.blockcount = len(self.ports[portnum].tod) // 200
                returnpacket.uidcount = len(self.ports[portnum].tod)
                for deviceid in self.ports[portnum].tod:
                    returnpacket.tod.append(self.devicestore[deviceid].uid)
            #Send the return packet for this address
                tosend = returnpacket.serialise()
                try:
                    self.artnetsocket.sendto(tosend, (self.HOST.network.broadcast_address.exploded, 6454))
                except socket.error as e:
                            print("Socket error{0}".format(e))

def opTodDatahandler(self, raw_data):
    #TODO: Maybe build a table of other devices?
    pass

def opRdmHandler(self, raw_data):
    opcode = unpack('!H', raw_data[8:10])
    opcode = opcode[0] << 8
    packet = None
    packet = packets.ArtRDMPacket()
    packet.opcode = opcode
    packet.net = raw_data[21]
    packet.command = raw_data[22]
    packet.address = raw_data[23]
    packet.rdmpd.fromart(raw_data[24:])
    if not packet.rdmpd.checkchecksum():
        return None
    for x in self.devicestore:
        if self.devicestore[x].uid == packet.rdmpd.destuid:
            #Process the PID
            pd = self.devicestore[x].getpid(packet.rdmpd.pid, packet.rdmpd)
            if pd is not None:
                #Attach the PD to an ArtRDM packet and send
                returnpacket = packets.ArtRDMPacket()
                returnpacket.opcode = opcode
                returnpacket.net = packet.net
                returnpacket.command = packet.command
                returnpacket.address = packet.address
                returnpacket.rdmpd = pd
                tosend = returnpacket.serialise()
                try:
                    self.artnetsocket.sendto(tosend, (self.HOST.network.broadcast_address.exploded, 6454))
                except socket.error as e:
                            print("Socket error{0}".format(e))
                return None
        else:
            pass
            #print("Not known at this address")
    return None