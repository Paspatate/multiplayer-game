import pygame

class Ghost:
    def __init__(self):
        self.position = [0, 0]
        self.texture = pygame.Surface((50, 50))
        self.texture.fill((200, 100, 100))

    def update(self):
        pass
    
    def draw(self):
        screen = pygame.display.get_surface()
        screen.blit(self.texture, self.position)