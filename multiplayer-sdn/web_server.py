from flask import Flask, render_template, jsonify
import json
from pathlib import Path

app = Flask(__name__)
STATE_FILE = Path(__file__).resolve().parent / "state.json"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/state")
def state():
    try:
        with open(STATE_FILE, "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {
            "players": {"P1": None, "P2": None},
            "stats": {},
            "updated_at": None
        }

    return jsonify(data)


if __name__ == "__main__":
    app.run(port=8000, debug=True)
