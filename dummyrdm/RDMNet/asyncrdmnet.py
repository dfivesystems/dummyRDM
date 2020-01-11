
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

class AsyncRDMNet():
    """AsyncIO Stream based implementation of RDMNet

    """

    def __init__(self, device_descriptor):
        """Initialise the RDMNet Protocol.

        Args:
            device_descriptor (RDMDevice.devicedescriptor.DeviceDescriptor):
                The descriptor of the RDMDevice this RDMNet responder is
                attached to, for passing to relevant handlers

        """

        self.reader = None
        self.writer = None
        self.device_descriptor = device_descriptor
        self.heartbeat = None

    async def listenRDMNetstreams(self, broker_descriptor):
        self.reader, self.writer = await asyncio.open_connection(broker_descriptor.address.compressed,
                                                       broker_descriptor.port)
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
        self.writer.write(retval)
        await self.writer.drain()

        self.heartbeat = asyncio.create_task(self.sendtcpheartbeat())

        while not self.writer.is_closing():
            #Decode RDMNet Packet
            #TODO: Allow support for multiple RLP blocks
            #Read in 16 bytes for the TCP Preamble
            data = await self.reader.read(16)
            if data[:12] != vectors.ACNheader:
                print("Incorrect ACN Header")
                continue
            preamble_length = unpack("!L", data[12:16])[0]
            #Read the remaining buffer
            rlpdata = await self.reader.read(preamble_length)
            #Process the RLP Buffer
            if rlpdata[6] == 0x09:
                brokerhandlers.handle(self, rlpdata[:])
            elif rlpdata[6] == 0x05:
                rpthandlers.handle(self, rlpdata[:])
            elif rlpdata[6] == 0x0B:
                print("EPT Packet - Not Implemented")
                #EPT Not yet implemented
            else:
                print("Unrecognised RLP Vector")
            await self.writer.drain()
        self.writer.close()

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

            self.writer.write(retval)
            await self.writer.drain()
            await asyncio.sleep(15)
