import struct
from core.packet import Packet, PacketType

class C2SBye(Packet):
    PacketLength = 1
    def serialize(self) -> bytes:
        data = struct.pack("!B", PacketType.DISCONNECT.value)
        return data
    
    @staticmethod
    def deserialize(data):
        return C2SBye()