import socket
from core.packets import AskConPacket, DisconnectPacket
from core.packet import stringify_bytes

print("start client")

# SIMPLE CLIENT TO TEST CONNECTION


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)

packet = AskConPacket()
deco_packet = DisconnectPacket()

s.sendto(packet.serialize(), ("127.0.0.1", 9876))

received = s.recv(4096)

print(stringify_bytes(received))

s.sendto(deco_packet.serialize(), ("127.0.0.1", 9876))

