from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB = 'todos.db'


def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            done BOOLEAN DEFAULT 0
        )''')


@app.route('/')
def index():
    with sqlite3.connect(DB) as conn:
        todos = conn.execute('SELECT * FROM todos').fetchall()
    return render_template('index.html', todos=todos)


@app.route('/add', methods=['POST'])
def add():
    task = request.form.get('task')
    if task:
        with sqlite3.connect(DB) as conn:
            conn.execute('INSERT INTO todos (task) VALUES (?)', (task,))
    return redirect(url_for('index'))


@app.route('/complete/<int:todo_id>')
def complete(todo_id):
    with sqlite3.connect(DB) as conn:
        conn.execute('UPDATE todos SET done=1 WHERE id=?', (todo_id,))
    return redirect(url_for('index'))


@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    with sqlite3.connect(DB) as conn:
        conn.execute('DELETE FROM todos WHERE id=?', (todo_id,))
    return redirect(url_for('index'))


@app.route('/health')
def health():
    return 'Server is up and running', 200


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
