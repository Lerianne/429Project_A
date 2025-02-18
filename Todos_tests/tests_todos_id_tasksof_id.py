import requests
import pytest

BASE_URL = "http://localhost:4567/todos/1/tasksof/1"

# Test GET /todos/1/tasksof/1 failure (GET is not allowed)
def test_get_tasksof_relationship_fail():
    response = requests.get(BASE_URL)
    assert response.status_code == 405  # Method Not Allowed

# Test PUT /todos/1/tasksof/1 failure (PUT is not allowed)
def test_put_tasksof_relationship_fail():
    response = requests.put(BASE_URL)
    assert response.status_code == 405  # Method Not Allowed

# Test POST /todos/1/tasksof/1 failure (POST is not allowed)
def test_post_tasksof_relationship_fail():
    response = requests.post(BASE_URL)
    assert response.status_code == 405  # Method Not Allowed

# Test DELETE /todos/1/tasksof/1 success (delete the instance of tasksof relationship)
def test_delete_tasksof_relationship_success():
    response = requests.delete(BASE_URL)
    assert response.status_code == 200  # Successfully deleted the relationship
    assert "tasksof" not in response.json()  # Ensure the relationship is deleted

# Test DELETE /todos/1/tasksof/1 failure (trying to delete a non-existent relationship)
def test_delete_tasksof_relationship_fail():
    response = requests.delete("http://localhost:4567/todos/1/tasksof/999")  # Non-existent relationship
    assert response.status_code == 404  # Not Found

# Test OPTIONS /todos/1/tasksof/1 failure (OPTIONS is not allowed)
def test_options_tasksof_relationship_fail():
    response = requests.options(BASE_URL)
    assert response.status_code == 405  # Method Not Allowed

# Test PATCH /todos/1/tasksof/1 failure (PATCH is not allowed)
def test_patch_tasksof_relationship_fail():
    response = requests.patch(BASE_URL, json={"project_id": 2})  # Trying to patch relationship
    assert response.status_code == 405  # Method Not Allowed

# Test HEAD /todos/1/tasksof/1 failure (HEAD is not allowed)
def test_head_tasksof_relationship_fail():
    response = requests.head(BASE_URL)
    assert response.status_code == 405  # Method Not Allowed

# Boundary Test: DELETE with a valid but minimal relationship
def test_delete_tasksof_relationship_minimal():
    response = requests.delete(BASE_URL)  # Delete relationship for a valid pair
    assert response.status_code == 200  # Successfully deleted the relationship
    assert "tasksof" not in response.json()  # Relationship is deleted

# Boundary Test: DELETE with a non-existent relationship
def test_delete_tasksof_relationship_nonexistent():
    response = requests.delete("http://localhost:4567/todos/1/tasksof/999")
    assert response.status_code == 404  # Not Found
