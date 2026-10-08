async function updateGame() {
    try {
        const response = await fetch("/state");
        const players = await response.json();

        updatePlayer("P1", players.P1);
        updatePlayer("P2", players.P2);

    } catch (error) {
        console.log("Failed to fetch game state");
    }
}

function updatePlayer(id, player) {
    const element = document.getElementById(id);

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

setInterval(updateGame, 200);

updateGame();
