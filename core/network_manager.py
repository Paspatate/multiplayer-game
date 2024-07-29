import socket
import struct
from collections import deque
from .packets import AskConPacket, AckConPacket, DisconnectPacket
from .packet import Packet
from .player_proxy import PlayerProxy

BUFFER_SIZE = 4096

class NetworkManager:
    next_net_id = 0
    def __init__(self, is_binded: bool) -> None:
        self.players_proxy = {}
        self.listening_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)

        self.out_packet_queue = deque()
        self.is_binded = is_binded

        self.incoming_packet = dict()
    
    def init(self):
        ADDR = "127.0.0.1"
        PORT = 9876
        self.listening_socket.setblocking(False)
        if self.is_binded:
            self.listening_socket.bind((ADDR, PORT))
        

    def parse_packet(self, data: bytes) -> Packet:
        
        packet_type_value = struct.unpack("!B", data[0:1])
        packet = None
        match packet_type_value[0]:
            case AskConPacket.packet_id:
                packet = AskConPacket.deserialize(data)
            case AckConPacket.packet_id:
                packet = AckConPacket.deserialize(data)
            case DisconnectPacket.packet_id:
                packet = DisconnectPacket.deserialize(data)
        return packet
            
    def handle_con(self):
        for addr in self.incoming_packet.keys():
            for packt in self.incoming_packet.get(addr):
                if isinstance(packt, AskConPacket):
                    self.players_proxy[addr] = PlayerProxy(addr)
                    self.queue_packet(AckConPacket(True))
                    print("added player at address: ", addr)
                
                if isinstance(packt, DisconnectPacket):
                    self.players_proxy.pop(addr)
                    print("removed player at addr ", addr, " from the server")
        
    def queue_packet(self, packet: Packet):
        self.out_packet_queue.appendleft(packet)
    
    def receive(self) -> dict[tuple[str, int], list[Packet]]: 
        raw_packets: dict[tuple, list] = dict()

        while True:
            try:
                data, addr = self.listening_socket.recvfrom(BUFFER_SIZE)
            except:
                data = bytes()
                addr = ("", 0)
            
            if not data:
                break
            
            if raw_packets.get(addr) is None:
                raw_packets[addr] = []
            
            raw_packets[addr].append(data)
        
        packets: dict[tuple, list] = dict()
        for addr, r_ps in raw_packets.items():
            for r_p in r_ps:
                p = self.parse_packet(r_p)
                if p is not None:
                    packets[addr] = []
                    packets[addr].append(p)
        
        return packets
    
    def receive_packet(self):
        self.incoming_packet = dict()
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
    
    def get_next_net_id(self) -> int:
        NetworkManager.next_net_id += 1
        return NetworkManager.next_net_id