from core.packet import Packet, PacketType
import struct

class HelloPacket(Packet):
    def serialize(self) -> bytes:
        data = struct.pack("!B", PacketType.HELLO.value)
        return data
    
    @staticmethod
    def deserialize(data):
        return "hello"

class ByePacket(Packet):
    def serialize(self) -> bytes:
        data = struct.pack("!B", PacketType.BYE.value)
        return data
    
    @staticmethod
    def deserialize(data):
        return "bye"

class MovePacket(Packet):
    """
    packet memory layout:
    | packetType (header) (1B)| newX (4B)| newY (4B)|
    """
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
        return MovePacket(x, y)


if __name__ == "__main__":
    hp = HelloPacket()
    mp = MovePacket(1004.5, 1)
    d = mp.serialize()
    d2 = hp.serialize()
    print(MovePacket.deserialize(d).newX)
    print(struct.unpack("!Bff", d))