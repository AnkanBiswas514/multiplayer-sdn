import socket
import time
import json

HOST = "127.0.0.1"
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((HOST, PORT))

players = {
    "P1": None,
    "P2": None
}

def save_state():
    with open("state.json", "w") as file:
        json.dump(players, file)

addresses = {}

stats = {
    "P1": {
        "last_sequence": 0,
        "total": 0,
        "received": 0,
        "lost": 0,
        "duplicates": 0,
        "out_of_order": 0,
        "packet_rate": 0,
        "rate_start": time.time(),
        "rate_packets": 0
    },
    "P2": {
        "last_sequence": 0,
        "total": 0,
        "received": 0,
        "lost": 0,
        "duplicates": 0,
        "out_of_order": 0,
        "packet_rate": 0,
        "rate_start": time.time(),
        "rate_packets": 0
    }
}

print("UDP Game Server started")
print("Waiting for players...")

while True:
    data, address = server.recvfrom(1024)

    message = data.decode()
    parts = message.split(",")

    player_id = parts[0]
    sequence = int(parts[1])
    x = parts[2]
    y = parts[3]
    action = parts[4]
    timestamp = float(parts[5])

    if player_id not in players:
        continue

    player_stats = stats[player_id]

    player_stats["total"] += 1

    player_stats["rate_packets"] += 1

    current_time = time.time()
    elapsed = current_time - player_stats["rate_start"]

    if elapsed >= 1:
        player_stats["packet_rate"] = player_stats["rate_packets"] / elapsed
        player_stats["rate_packets"] = 0
        player_stats["rate_start"] = current_time

    if sequence > player_stats["last_sequence"]:
        if player_stats["last_sequence"] > 0:
            if sequence > player_stats["last_sequence"] + 1:
                lost = sequence - player_stats["last_sequence"] - 1
                player_stats["lost"] += lost

        player_stats["received"] += 1
        player_stats["last_sequence"] = sequence

        players[player_id] = {
            "sequence": sequence,
            "x": x,
            "y": y,
            "action": action,
            "timestamp": timestamp
        }

        save_state()

        addresses[player_id] = address

        packet_status = "New packet"

    elif sequence == player_stats["last_sequence"]:
        player_stats["duplicates"] += 1
        packet_status = "Duplicate packet"

    else:
        player_stats["out_of_order"] += 1
        packet_status = "Out-of-order packet"

    latency = time.time() - timestamp

    print("\nReceived from", player_id)
    print("Sequence:", sequence)
    print("Status:", packet_status)
    print("Address:", address)
    print("Latency:", round(latency * 1000, 2), "ms")

    print("\nCurrent Game State:")
    print("P1:", players["P1"])
    print("P2:", players["P2"])

    print("\nPacket Statistics:")

    for player in ["P1", "P2"]:
        player_stats = stats[player]

        total_expected = player_stats["received"] + player_stats["lost"]

        if total_expected > 0:
            loss_percentage = player_stats["lost"] / total_expected * 100
        else:
            loss_percentage = 0

        print(
            player,
            "- Total:", player_stats["total"],
            "Received:", player_stats["received"],
            "Lost:", player_stats["lost"],
            "Duplicates:", player_stats["duplicates"],
            "Out-of-order:", player_stats["out_of_order"],
            "Loss:", round(loss_percentage, 2), "%",
            "PPS:", round(player_stats["packet_rate"], 2)
        )

    game_state = str(players)

    for player in addresses:
        server.sendto(game_state.encode(), addresses[player])

    print("Game state sent to", len(addresses), "player(s)")
