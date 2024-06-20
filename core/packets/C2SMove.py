from core.packet import Packet, PacketType
import struct


class C2SMovePacket(Packet):
    """
    packet memory layout:
    | packetType (header) (1B)| newX (4B)| newY (4B)|
    """
    PacketLength = 9
    def __init__(self, newX:float, newY:float) -> None:
        self.newX = newX
        self.newY = newY
    
    def serialize(self) -> bytes:
        data = bytearray()
        data += PacketType.MOVE.value.to_bytes(1, 'big')
        data += bytes(struct.pack("!f", self.newX))
        data += bytes(struct.pack("!f", self.newY))
        return bytes(data)
    
    @staticmethod
    def deserialize(data):
        x, y = struct.unpack("!ff", data[1:])
        return C2SMovePacket(x, y)


