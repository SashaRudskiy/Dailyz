from flask import Flask, jsonify, request, send_from_directory
import psycopg2
from db import init_db

try:
    from flask_cors import CORS
    cors_enabled = True
except ImportError:
    cors_enabled = False

app = Flask(__name__)
if cors_enabled:
    CORS(app)

def get_db_connection():
    conn = psycopg2.connect(
        dbname='dailyz',
        user='dailyz_user',
        password='dailyz_pass',
        host='localhost'
    )
    return conn

# 1. Получение всех задач (GET)
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, task, done, created_at, updated_at FROM tasks ORDER BY id')
    tasks = [
        {
            "id": row[0], "task": row[1], "done": row[2],
            "created_at": row[3].isoformat(), "updated_at": row[4].isoformat()
        }
        for row in cursor.fetchall()
    ]
    cursor.close()
    conn.close()
    return jsonify(tasks)

# 2. Создание новой задачи (POST)
@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    if not data or 'task' not in data:
        return jsonify({"error": "Необходимо указать задачу"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO tasks (task, done) VALUES (%s, %s) RETURNING id, task, done, created_at, updated_at',
        (data['task'], False)
    )
    new_task = cursor.fetchone()
    conn.commit()
    task = {
        "id": new_task[0], "task": new_task[1], "done": new_task[2],
        "created_at": new_task[3].isoformat(), "updated_at": new_task[4].isoformat()
    }
    cursor.close()
    conn.close()
    return jsonify(task), 201

# 3. Получение одной задачи (GET)
@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, task, done, created_at, updated_at FROM tasks WHERE id = %s', (task_id,))
    task = cursor.fetchone()
    cursor.close()
    conn.close()
    if not task:
        return jsonify({"error": "Задача не найдена"}), 404

    return jsonify({
        "id": task[0], "task": task[1], "done": task[2],
        "created_at": task[3].isoformat(), "updated_at": task[4].isoformat()
    })

# 4. Обновление задачи (PUT)
@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    if not data or 'task' not in data or 'done' not in data:
        return jsonify({"error": "Необходимо указать и задачу, и статус"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE tasks SET task = %s, done = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s RETURNING id, task, done, created_at, updated_at',
        (data['task'], data['done'], task_id)
    )
    updated = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()

    if not updated:
        return jsonify({"error": "Задача не найдена"}), 404

    return jsonify({
        "id": updated[0], "task": updated[1], "done": updated[2],
        "created_at": updated[3].isoformat(), "updated_at": updated[4].isoformat()
    })

# 5. Удаление задачи (DELETE)
@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = %s RETURNING id', (task_id,))
    deleted = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()

    if not deleted:
        return jsonify({"error": "Задача не найдена"}), 404

    return jsonify({"message": "Задача удалена"}), 200

# Отдача index.html из папки static как главной страницы
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
