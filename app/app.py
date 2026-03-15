from flask import Flask, render_template, request, redirect
import psycopg2
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()

def get_db():
    return psycopg2.connect(
        # host=os.getenv("DB_HOST"),
        # database=os.getenv("DB_NAME"),
        # user=os.getenv("DB_USER"),
        # password=os.getenv("DB_PASS")
        host="postgres",
        database="cruddb",
        user="postgres",
        password="postgres",
        port="5432"
    )


conn = get_db()
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL
)
""")
conn.commit()
cur.close()
conn.close()

@app.route("/")
def index():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks ORDER BY id DESC;")
    tasks = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["POST"])
def add():
    print("adding task... " + request.form.get("title"))
    title = request.form.get("title")
    if title:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO tasks (title) VALUES (%s)", (title,))
        conn.commit()
        cur.close()
        conn.close()
    return redirect("/")


@app.route("/delete/<int:id>")
def delete(id):
    conn=get_db()
    cur=conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id=%s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect("/")

@app.route("/update/<int:id>")
def update(id):
    conn=get_db()
    cur=conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id=%s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect("/")


@app.route("/batch_update/<int:id>")
def batch_update(id):
    conn=get_db()
    cur=conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id=%s", (id,))
    cur.execute("INSERT INTO tasks (title) VALUES (%s)", ("Batch Updated Task",))
    conn.commit()
    cur.close()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5100)