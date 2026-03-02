from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)

def get_db():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "db"),
        database=os.environ.get("DB_NAME", "tododb"),
        user=os.environ.get("DB_USER", "postgres"),
        password=os.environ.get("DB_PASSWORD", "postgres")
    )

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id SERIAL PRIMARY KEY,
            task TEXT NOT NULL
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

@app.route("/todos", methods=["GET"])
def get_todos():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, task FROM todos")
    todos = [{"id": row[0], "task": row[1]} for row in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify(todos)

@app.route("/todos", methods=["POST"])
def add_todo():
    task = request.json.get("task")
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO todos (task) VALUES (%s) RETURNING id", (task,))
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"id": new_id, "task": task}), 201

# ---- CHANGED: delete route ----
@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM todos WHERE id = %s", (todo_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"deleted": todo_id})
# -------------------------------

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)