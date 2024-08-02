import pygame
from core.network_manager import NetworkManager
from core.packets import AskConPacket, DisconnectPacket
from core.packet import stringify_bytes
import socket

pygame.init()

class Client:
    def __init__(self) -> None:
        self.network_manager = NetworkManager(is_binded = False)
        # self.window_size = pygame.Vector2(600, 400)
        # self.screen = pygame.display.set_mode(self.window_size.xy)
    
    def init(self):
        # self.network_manager.init()
        pass
        
    def run(self):
        
        delta_time = 0
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)

        packet = AskConPacket()
        deco_packet = DisconnectPacket()

        s.sendto(packet.serialize(), ("127.0.0.1", 9876))
        run = True
        while run:
            try:
                received = s.recv(4096)
                print(stringify_bytes(received))
            except KeyboardInterrupt:
                run = False

        s.sendto(deco_packet.serialize(), ("127.0.0.1", 9876))

    def clean(self):
        pass
