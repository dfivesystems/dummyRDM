from struct import unpack
import asyncio
from RDMNet import vectors, pdus

class AsyncRDMNet(asyncio.Protocol):
    def __init__(self, on_con_lost, device_descriptor):
        self.on_con_lost = on_con_lost
        self.transport = None
        self.device_descriptor = device_descriptor
        self.heartbeat = None

    def connection_made(self, transport):
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
        if data[:12] != vectors.ACNheader:
            print("Incorrect ACN Header")
            return
        if unpack("!L", data[12:16])[0] != len(data[16:]):
            print("Preamble length incorrect, preamble {} len {}".format(unpack("!L", data[12:16])[0], len(data[16:])))
            return

    def connection_lost(self, exc):
        print('The broker closed the connection')
        self.heartbeat.cancel()
        self.on_con_lost.set_result(True)

    async def sendtcpheartbeat(self):
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

