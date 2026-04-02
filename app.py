import os
from flask import Flask, render_template, request, redirect
from dotenv import load_dotenv

import psycopg2

load_dotenv()

app = Flask(__name__)

# Get database URL from Railway
DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

@app.route("/", methods=["GET", "POST"])
def index():
    conn = get_db_connection()
    cur = conn.cursor()

    # Create table if not exists
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            content TEXT NOT NULL
        )
    """)
    conn.commit()

    if request.method == "POST":
        task = request.form["task"]
        cur.execute("INSERT INTO tasks (content) VALUES (%s)", (task,))
        conn.commit()
        return redirect("/")

    cur.execute("SELECT * FROM tasks")
    tasks = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("index.html", tasks=tasks)

@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM tasks WHERE id = %s", (id,))
    conn.commit()

    cur.close()
    conn.close()

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)