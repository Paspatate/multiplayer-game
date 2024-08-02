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

class DisconnectPacket(Packet):
    """
    packet type (1B) | 
    """
    packet_id = 3
    packet_length = 1
    _format = "!B"
    def __init__(self) -> None:
        super().__init__()
    def serialize(self) -> bytes:
        data = struct.pack(DisconnectPacket._format, DisconnectPacket.packet_id)
        return data
    @staticmethod
    def deserialize(data: bytes):
        return DisconnectPacket()

class SpawnEntityPacket(Packet):
    """
    packet type (1B) | entity_type_id: int (4B) | network id: int (4B)
    """
    packet_id = 11
    packet_length = 9
    _format = "!BII"
    def __init__(self, entity_type_id: int, network_id: int) -> None:
        super().__init__()
        self.entity_type_id = entity_type_id
        self.network_id = network_id
    
    def serialize(self) -> bytes:
        data = struct.pack(SpawnEntityPacket._format, self.packet_id, self.entity_type_id,self.network_id)
        return data

    @staticmethod
    def deserialize(data: bytes) -> "SpawnEntityPacket":
        deserialized_data = struct.unpack(SpawnEntityPacket._format, data)
        return SpawnEntityPacket(deserialized_data[1], deserialized_data[2])

class ReplicateEntityPacket(Packet):
    """
    packet type (1B) | network id: int (4B) | x: float (4B) | y: float (4B)
    """
    packet_id = 12
    packet_length = 13
    _format = "!BIff"
    def __init__(self, network_id: int, x: float, y: float) -> None:
        super().__init__()
        self.network_id = network_id
        self.x = x
        self.y = y
    
    def serialize(self) -> bytes:
        data = struct.pack(ReplicateEntityPacket._format, self.packet_id, self.network_id, self.x, self.y)
        return data

    @staticmethod
    def deserialize(data: bytes) -> "ReplicateEntityPacket":
        deserialized_data = struct.unpack(ReplicateEntityPacket._format, data)
        return ReplicateEntityPacket(deserialized_data[1], deserialized_data[2], deserialized_data[3])

class CommandPacket(Packet):
    """
    packet type (1B) | up pressed: bool (1B) | down pressed: bool (1B) | right pressed: bool (1B) | left pressed: bool (1B)
    """
    packet_id = 13
    packet_length = 5
    _format = "!B????"
    def __init__(self, ) -> None:
        super().__init__()