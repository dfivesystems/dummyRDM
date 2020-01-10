
"""Asynchronous RDMNet Implementation.

This module is an asynchronus implementation of E1.33 RDMNet.

Example:
    This module is intended to be used as part of an RDMDevice,
    which is running the Asynio event loop. When calling listenRDMNet,
    it is expected that there will be a DeviceDescriptor and a
    BrokerDescriptor for passing to the relevant handlers

"""

from struct import unpack
import asyncio
from RDMNet import vectors, pdus, brokerhandlers, rpthandlers

class AsyncRDMNet(asyncio.Protocol):
    """Re-implementation of Asyncio streaming protocol for RDMNet.

    """

    def __init__(self, on_con_lost, device_descriptor):
        """Initialise the RDMNet Protocol.

        Args:
            on_con_lost (asyncio.future): Asyncio future for determining
                the state of the connection nad closing when appropriate.
            device_descriptor (RDMDevice.devicedescriptor.DeviceDescriptor):
                The descriptor of the RDMDevice this RDMNet responder is
                attached to, for passing to relevant handlers

        """

        self.on_con_lost = on_con_lost
        self.transport = None
        self.device_descriptor = device_descriptor
        self.heartbeat = None
        self.buffer = bytearray()

    def connection_made(self, transport: asyncio.transports.Transport):
        self.transport = transport
        #Send init connect packet

        packet = pdus.ACNTCPPreamble()

        rlppacket = pdus.RLPPDU(vectors.vector_root_broker, self.device_descriptor.cid)

        clientpacket = pdus.ClientConnect(self.device_descriptor.scope,
                                          self.device_descriptor.searchdomain)
        clientpacket.vector = vectors.vector_broker_connect
        cliententry = pdus.ClientEntry()
        cliententry.UID = self.device_descriptor.uid
        cliententry.CID = self.device_descriptor.cid
        cliententry.vector = vectors.vector_root_rpt

        packet.message = rlppacket
        rlppacket.message = clientpacket
        clientpacket.message = cliententry
        retval = packet.serialise()
        self.transport.write(retval)
        self.heartbeat = asyncio.create_task(self.sendtcpheartbeat())

    def data_received(self, data):
        #Decode RDMNet Packet
        self.buffer.extend(data)
        if self.buffer[:12] != vectors.ACNheader:
            print("Incorrect ACN Header")
            self.buffer.clear()
            return
        if unpack("!L", self.buffer[12:16])[0] != len(self.buffer[16:]):
            #Read the remaining buffer
            self.transport.resume_reading()
            return
        #Assuming those checks passed, let's start looking at things
        if self.buffer[22] == 0x09:
            brokerhandlers.handle(self, self.buffer)
        elif self.buffer[22] == 0x05:
            print("RPT Packet")
            rpthandlers.handle(self, self.buffer)
        elif self.buffer[22] == 0x0B:
            print("EPT Packet - Not Implemented")
            #EPT Not yet implemented
        else:
            print("Unrecognised Packet")
        #Clear the buffer for next use
        self.buffer.clear()

    def connection_lost(self, exc):
        print('The broker closed the connection')
        self.heartbeat.cancel()
        self.on_con_lost.set_result(True)

    async def sendtcpheartbeat(self):
        """Sends RDMNet heartbeat.

        Sends a vector_broker_null packet every 15s as defined by E.133
        to keep the TCP connection alive.

        """

        while True:
            packet = pdus.ACNTCPPreamble()

            rlppacket = pdus.RLPPDU(vectors.vector_root_broker, self.device_descriptor.cid)
            nullpacket = pdus.BrokerNull()

            packet.message = rlppacket
            rlppacket.message = nullpacket
            retval = packet.serialise()

            self.transport.write(retval)
            await asyncio.sleep(15)

async def listenRDMNet(self, device_descriptor, broker_descriptor):
    """Creates the RDMNet listener task within an existing event loop.

    Creates an RDMNet listener in an event loop derived from get_running_loop()
    On a loss of connection of the connection endpoint, the transport will close
    and the task will be cancelled.

    Args:
        device_descriptor (RDMDevice.devicedescriptor.DeviceDescriptor):
            A device descriptor to pass to the Protocol for handling.
        broker_descriptor (RDMNet.brokerdescription.BrokerDescriptor):
            A broker descriptor for initiating the connection.

    """

    loop = asyncio.get_running_loop()

    on_con_lost = loop.create_future()

    transport, protocol = await loop.create_connection(
        lambda: AsyncRDMNet(on_con_lost, device_descriptor),
        broker_descriptor.address.compressed, broker_descriptor.port)

    # Wait until the protocol signals that the connection
    # is lost and close the transport.
    try:
        await on_con_lost
    finally:
        transport.close()
