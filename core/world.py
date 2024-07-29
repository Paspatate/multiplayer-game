import pygame
from .entity import Entity

class World:
    def __init__(self, network_manager) -> None:
        self.entities = {}
        self.entity_type = {1: Entity}

        self.network_manager = network_manager
    
    def create_entity(self, entity_id, position: pygame.Vector2):
        entity_class = self.entity_type.get(entity_id)
        if not entity_class:
            raise KeyError("invalid entity_id")
        net_id = self.network_manager.get_next_net_id()
        self.entities[net_id] = entity_class(position.x, position.y, net_id)
    
    def update(self, delta_time):
        for entity in self.entities.values():
            entity.update(delta_time)
    
    def transmit(self):
        for entity in self.entities.values():
            entity.transmit(self.network_manager)