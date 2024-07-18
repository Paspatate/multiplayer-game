import struct
from .packet import Packet

class AskConPacket(Packet):
    packet_length = 1
    packet_id = 1
    def __init__(self) -> None:
        super().__init__()
    
    def serialize(self) -> bytes:
        data = struct.pack("!B", self.packet_id)
        return data
    
    @staticmethod
    def deserialize(data):
        return AskConPacket()

class AckConPacket(Packet):
    """
    packet type (1B) | ack bool (1B)
    """
    packet_id = 2
    packet_length = 2
    _format = "!B?"
    def __init__(self, is_acknowledged: bool) -> None:
        super().__init__()
        self.is_ack = is_acknowledged

    def serialize(self) -> bytes:
        data = struct.pack(AckConPacket._format, self.packet_id, self.is_ack)
        return data

    @staticmethod
    def deserialize(data: bytes) -> "AckConPacket":
        deser = struct.unpack(AckConPacket._format, data)
        return AckConPacket(deser[1:2])

class SpawnEntityPacket(Packet):
    """
    packet type (1B) | entity_type_id: int (4B) | x pos: float (4B) | y pos: float (4B)
    """
    packet_id = 3
    packet_length = 13
    _format = "!BIff"
    def __init__(self, entity_type_id: int, x_pos: float, y_pos: float) -> None:
        super().__init__()
        self.entity_type_id = entity_type_id
        self.x = x_pos
        self.y = y_pos
    
    def serialize(self) -> bytes:
        data = struct.pack(SpawnEntityPacket._format, self.entity_type_id, self.x, self.y)
        return data

    @staticmethod
    def deserialize(data: bytes) -> "SpawnEntityPacket":
        deserialized_data = struct.unpack(SpawnEntityPacket._format, data)
        return SpawnEntityPacket(deserialized_data[1], deserialized_data[2], deserialized_data[3])
    