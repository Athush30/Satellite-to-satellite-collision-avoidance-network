import socket
import threading
import queue

priority_queue = queue.PriorityQueue()

def send_message(priority, message, ip, port):
    priority_queue.put((priority, message, ip, port))

def handle_sending():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        if not priority_queue.empty():
            priority, message, ip, port = priority_queue.get()
            s.sendto(message.encode(), (ip, port))

def receive_alerts(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', port))
    while True:
        data, addr = s.recvfrom(1024)
        print(f"[RECEIVED from {addr}]:", data.decode())
