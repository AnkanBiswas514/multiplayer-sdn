import socket
import time

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

player_id = "P1"
x = 10
y = 20
action = "MOVE"
sequence = 1

UPDATE_RATE = 0.1

while True:
    timestamp = time.time()

    message = f"{player_id},{sequence},{x},{y},{action},{timestamp}"

    client.sendto(message.encode(), (SERVER_IP, SERVER_PORT))

    data, address = client.recvfrom(1024)

    x += 1

    if x>55:
        x=0
    sequence += 1

    time.sleep(UPDATE_RATE)
