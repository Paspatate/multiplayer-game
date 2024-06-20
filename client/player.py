import pygame
from core.packets.C2SMove import C2SMovePacket

class Player:
    def __init__(self, x, y, game):
        self.texture = pygame.Surface((50, 50))
        self.texture.fill((100, 200, 100))

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)

        self.speed = 500
        self.networkManager = game.networkManager

    def update(self, dt):
        self.velocity.xy = (0, 0)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_z]:
            self.velocity.y -= 1
        if keys[pygame.K_s]:
            self.velocity.y += 1
        if keys[pygame.K_q]:
            self.velocity.x -= 1
        if keys[pygame.K_d]:
            self.velocity.x += 1
        
        if (self.velocity.xy != (0,0)):
            self.velocity.normalize_ip()
            self.velocity.x *= self.speed * dt
            self.velocity.y *= self.speed * dt

        newPosition = self.position.copy()
        newPosition += self.velocity
        self.networkManager.queue_packet(C2SMovePacket(newPosition.x, newPosition.y))

    def draw(self):
        screen = pygame.display.get_surface()

        screen.blit(self.texture, self.position)
