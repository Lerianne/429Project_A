import requests
import pytest

BASE_URL = "http://localhost:4567/todos/1/tasksof"

# Test GET /todos/1/tasksof success (fetch all project items related to the todo by relationship "tasksof")
def test_get_tasksof_success():
    response = requests.get(BASE_URL)
    assert response.status_code == 200
    # Assuming response contains an array of task objects
    assert isinstance(response.json(), list)  # Ensure it is a list
    assert len(response.json()) > 0  # At least one task should be related to the todo

# Test GET /todos/1/tasksof failure (when no tasks are associated with the todo)
def test_get_tasksof_fail():
    response = requests.get("http://localhost:4567/todos/999/tasksof")  # Assuming this todo doesn't exist
    assert response.status_code == 404  # Not Found

# Test PUT /todos/1/tasksof failure (PUT is not allowed)
def test_put_tasksof_fail():
    response = requests.put(BASE_URL)
    assert response.status_code == 405  # Method Not Allowed

# Test POST /todos/1/tasksof success (create a task relationship between the todo and a project)
def test_post_tasksof_success():
    task_data = {"project_id": 2}  # Assuming we are creating a relationship with a project with ID 2
    response = requests.post(BASE_URL, json=task_data)
    assert response.status_code == 200  # Successfully created the relationship
    assert "tasksof" in response.json()  # Check the relationship exists

# Test POST /todos/1/tasksof failure (invalid data or missing project ID)
def test_post_tasksof_fail():
    task_data = {}  # Missing project ID
    response = requests.post(BASE_URL, json=task_data)
    assert response.status_code == 400  # Bad Request

# Test DELETE /todos/1/tasksof failure (DELETE is not allowed)
def test_delete_tasksof_fail():
    response = requests.delete(BASE_URL)
    assert response.status_code == 405  # Method Not Allowed

# Test OPTIONS /todos/1/tasksof failure (OPTIONS is not allowed)
def test_options_tasksof_fail():
    response = requests.options(BASE_URL)
    assert response.status_code == 405  # Method Not Allowed

# Test PATCH /todos/1/tasksof failure (PATCH is not allowed)
def test_patch_tasksof_fail():
    response = requests.patch(BASE_URL, json={"project_id": 3})  # Trying to update the relationship
    assert response.status_code == 405  # Method Not Allowed

# Test HEAD /todos/1/tasksof success (headers for project items related to todo by tasksof relationship)
def test_head_tasksof_success():
    response = requests.head(BASE_URL)
    assert response.status_code == 200  # Should be successful (headers returned)
    assert response.headers.get("Content-Length") is not None  # Ensure content-length header is present

# Test HEAD /todos/1/tasksof failure (wrong todo ID)
def test_head_tasksof_fail():
    response = requests.head("http://localhost:4567/todos/999/tasksof")  # Invalid todo ID
    assert response.status_code == 404  # Not Found

# Boundary Test: POST with a valid but minimal data (only project ID)
def test_post_tasksof_minimal_data():
    task_data = {"project_id": 1}  # Minimal valid data (project ID only)
    response = requests.post(BASE_URL, json=task_data)
    assert response.status_code == 200  # Successfully created the relationship

# Boundary Test: POST with maximum data (check large project ID or other constraints)
def test_post_tasksof_maximum_data():
    task_data = {"project_id": 999999999}  # Very large project ID to check limits
    response = requests.post(BASE_URL, json=task_data)
    assert response.status_code == 200  # Successfully created the relationship
    assert response.json()["project_id"] == 999999999
