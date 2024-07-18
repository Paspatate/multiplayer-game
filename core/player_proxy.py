import socket

class PlayerProxy:
    def __init__(self, address) -> None:
        self.address = address
    
    def send(self, socket: socket.socket, data):
        socket.sendto(data, self.address)