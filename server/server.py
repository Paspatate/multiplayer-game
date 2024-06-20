from core.network_manager import NetworkManager
from core.packets.C2SConnect import C2SHello
import time

class Server:
    def __init__(self) -> None:
        self.connectedPlayer = list()
        self.networkManger = NetworkManager()
        self.networkManger.bind("127.0.0.1", 9876)
        self.world = []

    def start(self):
        running = True
        deltaTime = 0
        while running:
            start_time = time.time()
            # get incoming packet
            self.networkManger.receive_all()

            self.connect_player()
            # run simulation 

            for game_object in self.world:
                game_object.update(deltaTime)
            # send movement packet
            
            deltaTime = start_time - time.time()
    
    def connect_player(self):
        packets = self.networkManger.get_in_packet()
        for p in packets:
            if isinstance(p, C2SHello):
                print("connect player")
                self.connectedPlayer.append("player")

