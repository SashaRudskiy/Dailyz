from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify([{"id": 1, "task": "Пример задачи", "done": False}])

if __name__ == '__main__':
    app.run(debug=True)
