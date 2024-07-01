import pytest
import requests

BASE_URL = "http://127.0.0.1:5000"
task_ids = []

def test_create_task():
    user_payload = {
        "title": "create a task",
        "description": "description of a task"
    }
    
    response = requests.post(f"{BASE_URL}/tasks", json=user_payload)
    response_json = response.json()

    assert response.status_code == 200
    assert "message" in response_json
    assert "id" in response_json
    
    task_ids.append(response_json["id"])

def test_get_tasks():
    response = requests.get(f"{BASE_URL}/tasks")
    response_json = response.json()

    assert response.status_code == 200
    assert "tasks" in response_json
    assert "total_tasks" in response_json

def test_get_task():
   if task_ids:
       first_task_id = task_ids[0]
       response = requests.get(f"{BASE_URL}/tasks/{first_task_id}")
       response_json = response.json()

       assert response.status_code == 200
       assert first_task_id ==  response_json["id"]

def test_update_task():
    if task_ids:
        first_task_id = task_ids[0]
        user_payload = {
            "title": "updated task",
            "description": "updated description of a task",
            "completed": True,
        }

        response = requests.put(f"{BASE_URL}/tasks/{first_task_id}", json=user_payload)
        response_json = response.json()

        assert response.status_code == 200
        assert "message" in response_json

        response = requests.get(f"{BASE_URL}/tasks/{first_task_id}")
        response_json = response.json()

        assert response_json["title"] == user_payload["title"]
        assert response_json["description"] == user_payload["description"]
        assert response_json["completed"] == user_payload["completed"]

def test_delete_task():
    if task_ids:
        first_task_id = task_ids[0]

        response = requests.delete(f"{BASE_URL}/tasks/{first_task_id}")
        assert response.status_code == 200

        response = requests.get(f"{BASE_URL}/tasks/{first_task_id}")
        assert response.status_code == 404
