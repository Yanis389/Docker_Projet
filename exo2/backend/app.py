from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

DB_PATH = "/data/database.db"

# Créer la table si elle n'existe pas
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# CREATE
@app.route("/api/users", methods=["POST"])
def create_user():
    data = request.get_json()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO user (username, password) VALUES (?, ?)", (data["username"], data["password"]))
    conn.commit()
    user_id = c.lastrowid
    conn.close()
    return jsonify({"id": user_id, "username": data["username"]}), 201

# READ ALL
@app.route("/api/users", methods=["GET"])
def get_users():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, username, password FROM user")
    users = [{"id": row[0], "username": row[1], "password": row[2]} for row in c.fetchall()]
    conn.close()
    return jsonify(users)

# READ ONE
@app.route("/api/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, username, password FROM user WHERE id=?", (user_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return jsonify({"id": row[0], "username": row[1], "password": row[2]})
    return jsonify({"error": "User not found"}), 404

# UPDATE
@app.route("/api/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE user SET username=?, password=? WHERE id=?", (data["username"], data["password"], user_id))
    conn.commit()
    conn.close()
    return jsonify({"message": "User updated"})

# DELETE
@app.route("/api/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM user WHERE id=?", (user_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "User deleted"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
