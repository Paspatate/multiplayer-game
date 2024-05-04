from collections import deque
import socket
import json

BUFFER_SIZE = 2048

class NetworkManager:
    def __init__(self) -> None:
        self.upd_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        self.upd_socket.setblocking(False)
        self.packetQueue = deque()
        
        settingsFile = open("client_settings.json", "r")
        settings = json.load(settingsFile)
        self.server_addr = settings["server_addr"]
        self.server_port = settings["server_port"]
    
    def queue_packet(self, packet):
        print("packet queued :", type(packet))
        self.packetQueue.append(packet)
    
    def send_all(self):
        while len(self.packetQueue) > 0:
            packet = self.packetQueue.popleft()
            print("sending packet", type(packet))
            self.send(packet)
    
    def send(self, packet):
        data = packet.serialize()
        self.upd_socket.sendto(data, (self.server_addr, self.server_port))
    
    def receive(self):
        data = bytearray()
        buffer = bytearray()

        while True:
            try:
                data = self.upd_socket.recv(BUFFER_SIZE)
            except:
                data = bytearray()

            if not data:
                break
            buffer += data

        return buffer
    

            

