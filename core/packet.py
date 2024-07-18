class Packet:
    """
    packet header layout:
    | PacketType (1B) | [payload]
    """
    packet_length = 0
    packet_id = 0
    def serialize(self) -> bytes:
        pass

    @staticmethod
    def deserialize(data: bytes):
        pass

def stringify_bytes(p: bytes) -> str:
    value = [hex(x).split('x')[-1] for x in list(p)]
    string = " ".join(value)
    return string