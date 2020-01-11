import struct
import socket
import typing
from asyncio.protocols import DatagramProtocol
from asyncio.transports import DatagramTransport
import asyncio
from LLRP import llrp

def _get_sock(transport: typing.Optional[DatagramTransport]) -> typing.Optional[socket.socket]:
    if transport is None or not hasattr(transport, "_extra"):
        return None
    sock: typing.Optional[socket.socket] = transport.get_extra_info('socket', None)
    return sock

class AsyncLLRP(DatagramProtocol):
    def __init__(self, multicast_address: str, bind_address: str, device_descriptor) -> None:
        self.multicast_address = multicast_address
        self.bind_address = bind_address
        self.transport: typing.Optional[DatagramTransport] = None
        self.connected = False
        self.loop = asyncio.get_running_loop()
        self.device_descriptor = device_descriptor

    @property
    def sock(self) -> typing.Optional[socket.socket]:
        return _get_sock(self.transport)

    def get_ttl(self) -> int:
        sock = self.sock
        if sock:
            return sock.getsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL)
        return 0

    def set_ttl(self, ttl: int = 1) -> None:
        sock = self.sock
        if sock:
            sock.setsockopt(
                socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, struct.pack('b', ttl)
            )
        return None

    def connection_made(self, transport: DatagramTransport) -> None:  # type: ignore
        self.transport = transport
        self.connected = True
        return None

    @classmethod
    def create_multicast_socket(cls, bind_address: str) -> socket.socket:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        sock.bind(('0.0.0.0', 5569))
        sock.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_IF,
                                   socket.inet_aton(bind_address))
        mreq = struct.pack("4s4s", socket.inet_aton('239.255.250.133'),
                           socket.inet_aton(bind_address))
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        sock.setblocking(False)
        return sock

    def datagram_received(self, data, addr):
        llrp.handlellrp(self, data)

    def disconnect(self) -> None:
        if self.transport:
            self.transport.close()
        self.connected = False
        return None

async def listenllrp(self, recloop, lan_address: str, device_descriptor):
    loop = recloop
    protocol = None
    try:
        sock: socket.socket = AsyncLLRP.create_multicast_socket(lan_address)
        listen_result: typing.Tuple[asyncio.BaseTransport, asyncio.BaseProtocol] = await loop.create_datagram_endpoint(
            lambda: AsyncLLRP('239.255.250.133', lan_address, device_descriptor), sock=sock
        )
        protocol = listen_result[1]
        assert isinstance(protocol, AsyncLLRP)
    except Exception as err:
        print(err)
    else:
        protocol.set_ttl(1)
    return protocol