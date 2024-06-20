from core.packet import Packet, PacketType
import struct


class C2SHello(Packet):
    PacketLength = 1
    def serialize(self) -> bytes:
        data = struct.pack("!B", PacketType.CONNECT.value) 
        return data
    @staticmethod
    def deserialize(data):
        return C2SHello()
