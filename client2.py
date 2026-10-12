import socket
import time

SERVER_IP = "10.0.0.1"
SERVER_PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

player_id = "P2"
x = 30
y = 15
action = "SHOOT"
sequence = 1

UPDATE_RATE = 0.1

y_direction = -1

while True:
    timestamp = time.time()

    message = f"{player_id},{sequence},{x},{y},{action},{timestamp}"

    client.sendto(message.encode(), (SERVER_IP, SERVER_PORT))

    data, address = client.recvfrom(1024)

    x -= 1
    y += y_direction

    if x < 0:
        x = 55

    if y >= 35 or y <= 2:
        y_direction *= -1

    sequence += 1
    time.sleep(UPDATE_RATE)
