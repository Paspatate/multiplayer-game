from enum import Enum

class PacketType (Enum):
    HELLO = 1
    BYE = 2
    MOVE = 3

class Packet:
    """
    packet header layout:
    | PacketType (1B) | [payload]
    """
    def serialize(self) -> bytes:
        raise NotImplementedError("Method not implemented, implement this method in the child class")
    @staticmethod
    def deserialize(data):
        raise NotImplementedError("Method not implemented, implement this method in the child class")