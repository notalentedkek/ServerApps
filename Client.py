import socket
import threading
import time
MULTICAST_GROUP = '233.0.0.1'
UDP_PORT = 1502
TCP_IP = '0.0.0.0'
TCP_PORT = 1600
last_message_content = None
last_messages = []  

clients = []

def udp_listener():
    global last_message_content, last_messages
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', UDP_PORT))
    mreq = socket.inet_aton(MULTICAST_GROUP) + socket.inet_aton('0.0.0.0')
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    
    print("UDP слушатель запущен и присоединился к мультикаст-группе.")
    
    while True:
        data, addr = sock.recvfrom(1024)
        message = data.decode('utf-8')
        if message != last_message_content:
            print(f"Новое сообщение: {message}")
            last_message_content = message
            if message not in last_messages:
                last_messages.append(message)
                if len(last_messages) > 5:
                    last_messages.pop(0)

def tcp_server():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((TCP_IP, TCP_PORT))
    server_sock.listen()
    print("TCP сервер запущен, ожидает клиентов...")
    while True:
        client_sock, addr = server_sock.accept()
        print(f"Клиент подключился: {addr}")
        try:
            for msg in last_messages:
                client_sock.sendall((msg + '\n').encode('utf-8'))
            clients.append(client_sock)
        except Exception as e:
            print(f"Ошибка при подключении клиента: {e}")

def broadcast_message(message):
    for c in clients[:]:
        try:
            c.sendall((message + '\n').encode('utf-8'))
        except:
            clients.remove(c)
            c.close()

def main():
    threading.Thread(target=udp_listener, daemon=True).start()
    threading.Thread(target=tcp_server, daemon=True).start()
    print("Промежуточный клиент запущен.")
    prev_message = None
    while True:
        if last_message_content != prev_message:
            broadcast_message(last_message_content)
            prev_message = last_message_content
        time.sleep(1)

main()