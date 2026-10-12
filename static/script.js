async function updateGame() {
    try {
        const response = await fetch("/state");
        const data = await response.json();

        updatePlayer("P1", data.players?.P1);
        updatePlayer("P2", data.players?.P2);

        updateStats("P1", data.stats?.P1);
        updateStats("P2", data.stats?.P2);
        updateConnectionStatus(data.stats);

    } catch (error) {
        console.log("Failed to fetch game state:", error);
    }
}

function updatePlayer(id, player) {
    const element = document.getElementById(id);

    if (!element) return;

    if (!player) {
        element.style.display = "none";
        return;
    }

    element.style.display = "block";

    const x = Number(player.x);
    const y = Number(player.y);

    element.style.left = (x * 10) + "px";
    element.style.top = (y * 10) + "px";
}

function showValue(value, suffix = "") {
    return value === null || value === undefined
        ? "—"
        : `${value}${suffix}`;
}

function updateStats(id, stats) {
    if (!stats) return;

    const fields = {
        total: showValue(stats.total),
        received: showValue(stats.received),
        lost: showValue(stats.lost),
        loss: showValue(stats.loss_percentage, "%"),
        pps: showValue(stats.packet_rate),
        latency: showValue(stats.latency_ms, " ms"),
        avgLatency: showValue(stats.average_latency_ms, " ms"),
        jitter: showValue(stats.jitter_ms, " ms"),
        duplicates: showValue(stats.duplicates),
        outOfOrder: showValue(stats.out_of_order)
    };

    for (const [field, value] of Object.entries(fields)) {
        const element = document.getElementById(`${id}-${field}`);

        if (element) {
            element.textContent = value;
        }
    }

    const status = document.getElementById(`${id}-status`);

    if (status) {
        status.textContent = stats.online ? "Online" : "Offline";
        status.className = stats.online
            ? "status online"
            : "status offline";
    }
}

function updateConnectionStatus(stats) {
    const status = document.getElementById("connection-status");

    if (!status) return;

    const online = stats &&
        Object.values(stats).some(player => player.online);

    status.textContent = online
        ? "UDP server connected"
        : "Waiting for players";

    status.className = online
        ? "status online"
        : "status offline";
}

setInterval(updateGame, 200);
updateGame();
