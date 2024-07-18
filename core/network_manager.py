import socket
import struct
from collections import deque
from .packets import AskConPacket, AckConPacket
from .packet import Packet
from .player_proxy import PlayerProxy

BUFFER_SIZE = 4096

class NetworkManager:
    def __init__(self, is_binded: bool) -> None:
        self.players_proxy = {}
        self.listening_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)

        self.out_packet_queue = deque()
        self.is_binded = is_binded
    
    def init(self):
        ADDR = "127.0.0.1"
        PORT = 9876
        self.listening_socket.setblocking(False)
        if self.is_binded:
            self.listening_socket.bind((ADDR, PORT))
        

    def parse_packet(self, data) -> Packet:
        packets = []
        end_of_packets = False
        start = 0
        while not end_of_packets:
            packet_type_value = struct.unpack("!B", data[start:start+1])
            packet = None
            p_len = 0
            match packet_type_value[0]:
                case AskConPacket.packet_id:
                    p_len = AskConPacket.packet_length
                    packet = AskConPacket.deserialize(data[start:start+p_len])
                case AckConPacket.packet_id:
                    p_len = AckConPacket.packet_length
                    packet = AckConPacket.deserialize(data[start:start+p_len])
            
            start = start + p_len

            if packet is not None: # packet not identified
                packets.append(packet)
            
            if start == len(data): # no more data to parse
                end_of_packets = True
        return packets
            
    def handle_con(self):
        try:
            data, addr = self.listening_socket.recvfrom(BUFFER_SIZE)
        except:
            data = bytes()

        if len(data) == 0:
            return
        print("addr: ", addr)

        packets = self.parse_packet(data)
        for p in packets:
            if isinstance(p, AskConPacket):
                self.players_proxy[addr] = PlayerProxy(addr)
                self.queue_packet(AckConPacket(True))
        
    def queue_packet(self, packet: Packet):
        self.out_packet_queue.appendleft(packet)
    
    def receive(self) -> list:     
        return []
    
    def receive_packet(self):
        packets = self.receive()
        if len(packets) > 0:
            self.incoming_packet = packets
    
    def send_all(self):
        while len(self.out_packet_queue) > 0:
            packet = self.out_packet_queue.pop()
            for proxy in self.players_proxy.values():
                proxy.send(self.listening_socket, packet.serialize())
    
    def stop(self):
        self.listening_socket.close()
        self.connection_socket.close()