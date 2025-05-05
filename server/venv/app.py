from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)

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
    cursor.execute('SELECT id, task, done FROM tasks')
    tasks = [
        {"id": row[0], "task": row[1], "done": row[2]}
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
        'INSERT INTO tasks (task, done) VALUES (%s, %s) RETURNING id, task, done',
        (data['task'], False)
    )
    new_task = cursor.fetchone()
    conn.commit()
    task = {"id": new_task[0], "task": new_task[1], "done": new_task[2]}
    cursor.close()
    conn.close()
    return jsonify(task), 201

# 3. Получение одной задачи (GET)
@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, task, done FROM tasks WHERE id = %s', (task_id,))
    task = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if not task:
        return jsonify({"error": "Задача не найдена"}), 404
    
    return jsonify({
        "id": task[0],
        "task": task[1],
        "done": task[2]
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
        'UPDATE tasks SET task = %s, done = %s WHERE id = %s RETURNING id, task, done',
        (data['task'], data['done'], task_id)
    )
    updated = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    
    if not updated:
        return jsonify({"error": "Задача не найдена"}), 404
    
    return jsonify({
        "id": updated[0],
        "task": updated[1],
        "done": updated[2]
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

if __name__ == '__main__':
    app.run(debug=True)