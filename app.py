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
    searched_task = None
    user_payload = request.get_json()

    for task in task_list:
        if task.id == id:
            searched_task = task
            break
    
    if not searched_task:
        return jsonify({"message": "Task not found!"}), 404

    searched_task.title = user_payload["title"]
    searched_task.description = user_payload["description"]
    searched_task.completed = user_payload["completed"]

    return jsonify({"message": "Task updated successfully!"})


@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    searched_task = None

    for task in task_list:
        if task.id == id:
            searched_task = task
            break
    
    if not searched_task:
        return jsonify({"message": "Task not found!"}), 404

    task_list.remove(searched_task)
    return jsonify({"message": "Task deleted successfully!"})

if __name__ == "__main__":
    app.run(debug=True)