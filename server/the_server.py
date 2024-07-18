from time import time, sleep
from core.network_manager import NetworkManager

class Server:
    def __init__(self) -> None:
        self.network_manager = NetworkManager(is_binded=True)
        self.the_world = []

    def init(self):
        self.network_manager.init()

    def run(self):
        TARGETTPS = 60
        run = True
        delta_time = 0

        print("server start")
        while run:
            start_time = time()
            self.network_manager.handle_con()
            self.network_manager.receive_packet()

            self.network_manager.send_all()
            compute_time = time() - start_time
            sleep(max(1/TARGETTPS - compute_time, 0))
            delta_time = time() - start_time
    
    def clean(self):
        self.network_manager.stop()
        print("server stop")
