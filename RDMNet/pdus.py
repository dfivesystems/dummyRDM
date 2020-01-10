"""E1.33 RDMNet PDU definitions
Any PDUs contained here should have a serialise() function and
a self.message object if appropriate (nested PDUs)
Todo:
    * Add Message argument to constructors
    * Allow ACNTCPPreamble to have multiple nested RLP PDUs
    * Implement de-serialise methods
"""
from struct import pack
from RDMNet import vectors
#from RDM import rdmpacket

class ACNTCPPreamble:
    """Container for ACNTCPPreamble data"""
    def __init__(self):
        self.acn_packet_id = bytes(b'\x41\x53\x43\x2d\x45\x31\x2e\x31\x37\x00\x00\x00')
        self.RLP_length = 0x00000000
        self.message = None

    def serialise(self):
        """Serialises the PDU, including any nested PDUs"""
        #Calculate all sub messages before ammending lengths
        retval = bytearray()
        messagebytes = self.message.serialise()
        self.RLP_length += (len(messagebytes))
        retval.extend(self.acn_packet_id)
        retval.extend(pack('!I', self.RLP_length))
        retval.extend(messagebytes)
        return retval

class RLPPDU:
    """Container for an RLP PDU"""
    def __init__(self, vector, CID):
        self.flags_length = 0xF00017
        self.vector = vector
        self.senderCID = CID
        self.message = None

    def serialise(self):
        """Serialises the PDU, including any nested PDUs"""
        #Calculate all sub messages before ammending lengths
        retval = bytearray()
        messagebytes = self.message.serialise()
        self.flags_length += (len(messagebytes))
        retval.extend(pack('!L', self.flags_length)[1:])
        retval.extend(self.vector)
        retval.extend(self.senderCID)
        retval.extend(messagebytes)
        return retval

class BrokerNull:
    """Container for a Broker Null (hearbeat) PDU"""
    def __init__(self):
        self.flags_length = 0xF00005
        self.vector = vectors.vector_broker_null

    def serialise(self):
        """Serialises the PDU, this PDU has no nested options"""
        #Calculate all sub messages before ammending lengths
        retval = bytearray()
        retval.extend(pack('!L', self.flags_length)[1:])
        retval.extend(self.vector)
        return retval

class ConnectReply:
    """Container for a Connect Reply PDU"""
    def __init__(self):
        self.flags_length = 0x000000
        self.vector = vectors.vector_broker_connect_reply
        self.connection_code = 0x0000
        self.E133_vers = 0x0000
        self.brokerUID = bytearray()
        self.clientUID = bytearray()

class ClientConnect:
    """Container for a Client Connect PDU"""
    def __init__(self, scope, searchdomain, connectionflags=0x00):
        self.flags_length = 0xF0015C
        self.vector = vectors.vector_broker_connect
        self.scope = scope
        self.E133vers = 0x0001
        self.searchdomain = searchdomain
        self.connectionflags = connectionflags #Set to 0x80 for Incremental updates
        self.message = None

    def serialise(self):
        """Serialises the PDU, including any nested PDUs"""
        #Calculate all sub messages before amending lengths
        retval = bytearray()
        messagebytes = self.message.serialise()
        retval.extend(pack('!L', self.flags_length)[1:])
        retval.extend(self.vector)
        if len(self.scope) > 63:
            retval.extend(bytes(self.scope[:63], 'utf-8'))
        else:
            retval.extend(bytes(self.scope, 'utf-8')) #Limit 63 Characters
            for i in range(63-len(self.scope)):
                retval.extend(b'\x00')
        retval.extend(pack('!H', self.E133vers))
        if len(self.searchdomain) > 231:
            retval.extend(bytes(self.searchdomain[:231], 'utf-8'))
        else:
            retval.extend(bytes(self.searchdomain, 'utf-8')) #Limit 231 Characters
            for i in range(231-len(self.searchdomain)):
                retval.extend(b'\x00')
        retval.extend(pack('!B', self.connectionflags))
        retval.extend(messagebytes)
        return retval

class ClientEntry:
    """Container for a Client Entry PDU"""
    def __init__(self):
        self.flags_length = 0xF0002E
        self.vector = 0x00000000
        self.CID = bytearray(b'\x00' * 16)
        self.UID = bytearray(b'\x00' * 6)
        self.RPTClientType = 0x00
        self.bindingCID = bytearray(b'\x00' * 16)

    def serialise(self):
        """Serialises the PDU, this PDU has no nested options"""
        retval = bytearray()
        retval.extend(pack('!L', self.flags_length)[1:])
        retval.extend(self.vector)
        retval.extend(self.CID)
        retval.extend(self.UID)
        retval.extend(pack('!B', self.RPTClientType))
        retval.extend(self.bindingCID)
        return retval
