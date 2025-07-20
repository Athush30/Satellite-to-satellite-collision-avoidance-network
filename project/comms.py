import socket
import threading
import queue

# Priority queue for sending messages
priority_queue = queue.PriorityQueue()

def send_message(priority, message, ip, port):
    """
    Add a message to the priority queue for sending.
    Args:
        priority: Message priority (lower number = higher priority)
        message: Message string to send
        ip: Destination IP address
        port: Destination port
    """
    priority_queue.put((priority, message, ip, port))

def handle_sending():
    """Thread to send messages from the priority queue via UDP."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        if not priority_queue.empty():
            priority, message, ip, port = priority_queue.get()
            try:
                s.sendto(message.encode('utf-8'), (ip, port))
                print(f"Sent message to {ip}:{port}: {message}")
            except OSError as e:
                print(f"Error sending to {ip}:{port}: {e}")

def receive_alerts(port, sat_name):
    """
    Thread to receive UDP messages on the specified port.
    Args:
        port: Port to listen on
        sat_name: Name of the satellite (for logging)
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow port reuse
    s.settimeout(2.0)  # 2-second timeout
    # Try binding to the port or alternatives
    for attempt in range(10):  # Try 10 ports
        try_port = port + attempt * 1000  # Wider spacing
        try:
            s.bind(('', try_port))
            print(f"Successfully bound {sat_name} to port {try_port}")
            break
        except OSError as e:
            print(f"Error binding {sat_name} to port {try_port}: {e}")
            if attempt == 9:
                print(f"Failed to bind {sat_name} after 10 attempts. Exiting thread for {sat_name}.")
                return
    while True:
        try:
            data, addr = s.recvfrom(1024)
            message = data.decode('utf-8')
            print(f"[RECEIVED from {addr} for {sat_name}]: {message}")
        except socket.timeout:
            print(f"Timeout on port {try_port} for {sat_name}. Continuing...")
        except UnicodeDecodeError:
            print(f"[RECEIVED from {addr} for {sat_name}]: Error decoding message (invalid characters)")
        except OSError as e:
            print(f"Error receiving on port {try_port} for {sat_name}: {e}")
