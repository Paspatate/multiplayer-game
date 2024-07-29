import pygame
from .network_manager import NetworkManager
from .packets import ReplicateEntityPacket

class Entity:
    def __init__(self, x: float, y: float, network_id: int) -> None:
        self.network_id = network_id
        self.position = pygame.Vector2(x, y)
        self.speed = 10
    
    def update(self, dt: float):
        self.position.x += self.speed * dt
        
    def transmit(self, network_manager: NetworkManager):
        out_packet = ReplicateEntityPacket(self.network_id, self.position.x, self.position.y)
        network_manager.queue_packet(out_packet)
        
    