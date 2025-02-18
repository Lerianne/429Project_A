import requests
import pytest

BASE_URL = "http://localhost:5000/todos/1"

# Test GET /todos/1 success (fetch a specific todo by ID)
def test_get_todo_by_id_success():
    response = requests.get(BASE_URL)
    assert response.status_code == 200
    assert response.json()["title"] == "scan paperwork"  # Adjust based on DB or mock data

# Test GET /todos/1 failure (invalid ID or non-existing todo)
def test_get_todo_by_id_fail():
    response = requests.get("http://localhost:5000/todos/999")  # Assuming this ID doesn't exist
    assert response.status_code == 404  # Not Found

# Test PUT /todos/1 success (update a todo by ID)
def test_put_todo_by_id_success():
    updated_todo = {"title": "Updated Task", "description": "Updated description"}
    response = requests.put(BASE_URL, json=updated_todo)
    assert response.status_code == 200  # Assuming PUT returns 200 on success
    updated_data = response.json()
    assert updated_data["title"] == "Updated Task"
    assert updated_data["description"] == "Updated description"

# Test PUT /todos/1 failure (invalid data or other issues)
def test_put_todo_by_id_fail():
    invalid_todo = {"description": "Missing title"}
    response = requests.put(BASE_URL, json=invalid_todo)
    assert response.status_code == 400  # Bad Request

# Test POST /todos/1 success (attempt to amend a todo with POST)
def test_post_todo_by_id_success():
    updated_todo = {"title": "Amended Task", "description": "Updated task details"}
    response = requests.post(BASE_URL, json=updated_todo)
    assert response.status_code == 200
    assert response.json()["title"] == "Amended Task"  # Check for update
    assert response.json()["description"] == "Updated task details"

# Test POST /todos/1 failure (incorrect method or incorrect data)
def test_post_todo_by_id_fail():
    updated_todo = {"title": "Amended Task"}  # Assuming we need both title and description
    response = requests.post(BASE_URL, json=updated_todo)
    assert response.status_code == 400  # Bad Request

# Test DELETE /todos/1 failure (delete not allowed)
def test_delete_todo_by_id_fail():
    response = requests.delete(BASE_URL)
    assert response.status_code == 405  # Method Not Allowed

# Test OPTIONS /todos/1 failure (not allowed)
def test_options_todo_by_id_fail():
    response = requests.options(BASE_URL)
    assert response.status_code == 405  # Method Not Allowed

# Test PATCH /todos/1 failure (not allowed)
def test_patch_todo_by_id_fail():
    response = requests.patch(BASE_URL, json={"title": "Partial Update"})
    assert response.status_code == 405  # Method Not Allowed

# Test HEAD /todos/1 success (headers for a specific todo)
def test_head_todo_by_id_success():
    response = requests.head(BASE_URL)
    assert response.status_code == 200
    assert response.headers.get("Content-Length") is not None  # Ensure content-length is in the headers

# Test HEAD /todos/1 failure (wrong endpoint or incorrect request)
def test_head_todo_by_id_fail():
    response = requests.head("http://localhost:5000/todos/999")  # Invalid ID
    assert response.status_code == 404  # Not Found

# Boundary Test: PUT with minimal data (only title)
def test_put_todo_minimal_data():
    minimal_data = {"title": "Minimal Update"}
    response = requests.put(BASE_URL, json=minimal_data)
    assert response.status_code == 200
    assert response.json()["title"] == "Minimal Update"

# Boundary Test: PUT with maximum allowed fields (testing length or other constraints)
def test_put_todo_maximum_data():
    max_data = {
        "title": "A" * 255,  # Example of very long title
        "description": "B" * 1000,  # Long description
    }
    response = requests.put(BASE_URL, json=max_data)
    assert response.status_code == 200
    assert response.json()["title"] == "A" * 255
    assert response.json()["description"] == "B" * 1000
