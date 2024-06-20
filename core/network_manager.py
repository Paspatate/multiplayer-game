from collections import deque
import socket
import json
import struct
from core.packet import PacketType
from core.packets.C2SConnect import C2SHello
from core.packets.C2SDisconnect import C2SBye
from core.packets.C2SMove import C2SMovePacket

BUFFER_SIZE = 2048

class NetworkManager:
    nextid = 0
    def __init__(self) -> None:
        self.upd_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        self.upd_socket.setblocking(False)
        self.packetQueue = deque()
        self.incoming_packets = []
        self.network_ids = {}
                
        settingsFile = open("client_settings.json", "r")
        settings = json.load(settingsFile)
        self.server_addr = settings["server_addr"]
        self.server_port = settings["server_port"]

    def add_to_network_elem(self, elem):
        NetworkManager.nextid += 1
        self.network_ids[NetworkManager.nextid] = elem
        return NetworkManager.nextid
    
    def bind(self, addr, port):
        self.upd_socket.bind((addr, port))

    def queue_packet(self, packet):
        # print("packet queued :", type(packet))
        self.packetQueue.append(packet)
    
    def get_in_packet(self):
        return self.incoming_packets

    def get_packets(type):
        pass
    
    def send_all(self):
        while len(self.packetQueue) > 0:
            packet = self.packetQueue.popleft()
            #print("sending packet", type(packet))
            self.__send(packet)
    
    def __send(self, packet):
        data = packet.serialize()
        self.upd_socket.sendto(data, (self.server_addr, self.server_port))
    
    def receive_all(self):
        p = self.receive_packet()
        if len(p) > 0:
            self.incoming_packets = p

    def receive_packet(self):
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

        if len(buffer) == 0:
            return []

        packets = []
        endofpacket = False
        start = 0
        while not endofpacket:
            packet_type_value = struct.unpack("!B", buffer[start:start+1])
            p_type = PacketType(packet_type_value[0])
            packet = None
            p_len = 0
            match p_type:
                case PacketType.CONNECT:
                    p_len = C2SHello.PacketLength
                    packet = C2SHello.deserialize(buffer[start:start+p_len])
                case PacketType.DISCONNECT:
                    p_len = C2SBye.PacketLength
                    packet = C2SBye.deserialize(buffer[start:start+p_len])
                case PacketType.MOVE:
                    p_len = C2SMovePacket.PacketLength
                    packet = C2SMovePacket.deserialize(buffer[start:start+p_len])
            
            start = start + p_len
            if packet is not None:
                packets.append(packet)
            
            if start == len(buffer):
                endofpacket = True         
        return packets
    

            

