from flask import Flask, request, jsonify
from models.task import Task

app = Flask(__name__)
task_list = []
task_id_control = 1

@app.route("/tasks", methods=["POST"])
def add_task():
    global task_id_control

    user_payload = request.get_json()
    
    new_task = Task(
        id=task_id_control,
        title=user_payload["title"], 
        description=user_payload["description"] or ""
    )
    task_id_control += 1
    task_list.append(new_task)
    
    return jsonify({"message": "Task created successfully!", "id": new_task.id})

@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = [task.to_dict() for task in task_list]
    
    output = {
        "tasks": tasks,
        "total_tasks": len(tasks)
    }
    
    return jsonify(output)

@app.route("/tasks/<int:id>", methods=["GET"])
def get_task(id):
    for task in task_list:
        if task.id == id:
            return jsonify(task.to_dict())
    
    return jsonify({"message": "Task not found"}), 404

@app.route("/tasks/<int:id>", methods=["PUT"])
def update_task(id):
    user_payload = request.get_json()
    print(user_payload)

    for task in task_list:
        if task.id == id:
            task.title = user_payload["title"]
            task.description = user_payload["description"]
            task.completed = user_payload["completed"]
        return jsonify({"message": "Task updated successfully!"})

    return jsonify({"message": "Task not found!"}), 404

@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    for task in task_list:
        if task.id == id:
            task_list.remove(task)
            return jsonify({"message": "Task deleted successfully!"})

    return jsonify({"message": "Task not found!"}), 404

if __name__ == "__main__":
    app.run(debug=True)