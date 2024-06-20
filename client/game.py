import pygame
from client.player import Player
from core.network_manager import NetworkManager
from core.packets.C2SConnect import C2SHello

class Game:
    def __init__(self) -> None:
        self.WIN_WIDTH = 1280
        self.WIN_HEIGHT = 720
        self.WIN_TITLE = "Multiplayer game"
        self.TARGET_FPS = 0

        self.screen = pygame.display.set_mode(size=(self.WIN_WIDTH, self.WIN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.networkManager = NetworkManager()
        self.player = Player(10, 10, self)
        self.entities = []
        self.entities.append(self.player)

    
    def start(self):
        self.networkManager.queue_packet(C2SHello())

        pygame.display.set_caption(self.WIN_TITLE)

        deltaTime = 0
        run = True
        while run:
            pygame.display.set_caption(self.WIN_TITLE + "fps:" + str(self.clock.get_fps()))
            # pygame event managment
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        self.networkManager.queue_packet(C2SHello())
                
            self.networkManager.receive_all()
            # world update
            self.player.update(deltaTime)

            # sending to server
            self.networkManager.send_all()

            # screen rendering
            self.screen.fill((0, 0, 0))
            self.player.draw()

            pygame.display.update()
            deltaTime = self.clock.tick(self.TARGET_FPS) / 1000