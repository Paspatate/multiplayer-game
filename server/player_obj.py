import pygame
from core.network_manager import NetworkManager

class PlayerObject:
    def __init__(self, server) -> None:
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)

        self.speed = 500
        self.nm: NetworkManager = server.networManager
    
    def update(self, dt):
        self.nm.get_in_packet()
