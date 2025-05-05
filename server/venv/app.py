from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)  # исправлено здесь

def get_db_connection():
    conn = psycopg2.connect(
        dbname='dailyz',
        user='dailyz__user',
        password='dailyz_pass',
        host='localhost'
    )
    return conn

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT id, task, done FROM tasks')
    rows = c.fetchall()
    tasks = [{"id": r[0], "task": r[1], "done": r[2]} for r in rows]
    c.close()
    conn.close()
    return jsonify(tasks)

@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.json
    task = data.get("task")
    if not task:
        return jsonify({"error": "Пустое поле задачи"}), 400
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(
        'INSERT INTO tasks (task, done) VALUES (%s, %s) RETURNING id, task, done',
        (task, False)
    )
    new_task = c.fetchone()
    conn.commit()
    c.close()
    conn.close()
    return jsonify({"id": new_task[0], "task": new_task[1], "done": new_task[2]}), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.json
    done = data.get("done")
    if done is None:
        return jsonify({"error": "Не передан статус"}), 400
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(
        'UPDATE tasks SET done=%s WHERE id=%s RETURNING id, task, done',
        (done, task_id)
    )
    updated = c.fetchone()
    conn.commit()
    c.close()
    conn.close()
    if not updated:
        return jsonify({"error": "Задача не найдена"}), 404
    return jsonify({"id": updated[0], "task": updated[1], "done": updated[2]})

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('DELETE FROM tasks WHERE id=%s RETURNING id', (task_id,))
    deleted = c.fetchone()
    conn.commit()
    c.close()
    conn.close()
    if not deleted:
        return jsonify({"error": "Задача не найдена"}), 404
    return jsonify({"result": "deleted"})

if __name__ == '__main__': 
    app.run(debug=True)