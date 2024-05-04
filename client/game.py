import pygame
from client.player import Player
from core.network_manager import NetworkManager
from core.packets import HelloPacket

class Game:
    def __init__(self) -> None:
        self.WIN_WIDTH = 1280
        self.WIN_HEIGHT = 720
        self.WIN_TITLE = "Multiplayer game"
        self.TARGET_FPS = 0

        self.player = Player(10, 10)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(size=(self.WIN_WIDTH, self.WIN_HEIGHT))
        self.networkManager = NetworkManager()

    
    def start(self):
        self.networkManager.queue_packet(HelloPacket())

        pygame.display.set_caption(self.WIN_TITLE)

        deltaTime = 0
        run = True
        while run:
            pygame.display.set_caption(self.WIN_TITLE + "fps:" + str(self.clock.get_fps()))
            # pygame event managment
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            # world update
            self.player.update(deltaTime)

            # sending to server
            self.networkManager.send_all()

            # screen rendering
            self.screen.fill((0, 0, 0))
            self.player.draw()

            pygame.display.update()
            deltaTime = self.clock.tick(self.TARGET_FPS) / 1000