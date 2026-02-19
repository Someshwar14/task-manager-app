from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

# PostgreSQL connection
conn = psycopg2.connect(
    host="localhost",
    database="taskdb",
    user="postgres",
    password="yourpassword"
)
cur = conn.cursor()

# Create table if not exists
cur.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL
)
""")
conn.commit()

@app.route('/')
def index():
    cur.execute("SELECT * FROM tasks")
    tasks = cur.fetchall()
    return render_template("index.html", tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    task = request.form['task']
    cur.execute("INSERT INTO tasks (title) VALUES (%s)", (task,))
    conn.commit()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    cur.execute("DELETE FROM tasks WHERE id=%s", (id,))
    conn.commit()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
