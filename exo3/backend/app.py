from flask import Flask, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

TOR_PROXY = {
    "http": "socks5h://tor:9050",
    "https": "socks5h://tor:9050"
}

@app.route("/api/users", methods=["GET"])
def get_users():
    try:
        response = requests.get(
            "https://randomuser.me/api/?results=5",
            proxies=TOR_PROXY,
            timeout=20
        )
        response.raise_for_status()
        data = response.json()

        users = [{"name": f"{u['name']['first']} {u['name']['last']}",
                  "picture": u["picture"]["medium"]} for u in data["results"]]

        return jsonify(users)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
