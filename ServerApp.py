import socket
import time

UDP_IP = "233.0.0.1"
UDP_PORT = 1502
TEXT = 'Text.txt'

def Msg():
    with open(TEXT,'r',encoding='utf-8') as f:
        return f.read().strip()

def IDK():
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
    while True:
        Msgg = Msg()
        sock.sendto(Msgg.encode('utf-8'),(UDP_IP,UDP_PORT))
        print(f"Sent message: {Msgg}")
        time.sleep(10)
        

IDK()