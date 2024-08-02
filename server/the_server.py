from time import time, sleep
from pygame.math import Vector2
from core.network_manager import NetworkManager
from core.world import World


class Server:
    def __init__(self) -> None:
        self.network_manager = NetworkManager(is_binded=True)
        # self.the_world = {} # key: network id; value: entity object
        self.the_world = World(self.network_manager)

    def init(self):
        self.network_manager.init()

    def run(self):
        TARGETTPS = 60
        run = True
        delta_time = 0

        print("server start")
        self.the_world.create_entity(1, Vector2(10, 10))
        while run:
            start_time = time()
            self.network_manager.receive_packet()
            self.network_manager.handle_con()

            self.the_world.update(delta_time)

            self.the_world.transmit()
            
            self.network_manager.send_all()
            compute_time = time() - start_time
            sleep(max(1/TARGETTPS - compute_time, 0))
            delta_time = time() - start_time
    
    def clean(self):
        self.network_manager.stop()
        print("server stop")
