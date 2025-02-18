import requests
import pytest

BASE_URL = "http://localhost:4567/todos"

# Test GET /todos success (fetch all todos)
def test_get_todos_success():
    response = requests.get(BASE_URL)
    assert response.status_code == 200
    assert len(response.json()) == 2  # Adjust depending on  database (or mock data)

# Test GET /todos failure (when it doesn't exist or connection issues)
def test_get_todos_fail():
    response = requests.get(f"{BASE_URL}?invalid_param=test")
    assert response.status_code == 400  # Change to match expected error code

# Test PUT /todos (not allowed)
def test_put_todos_fail():
    response = requests.put(BASE_URL, json={"title": "Test Todo"})
    assert response.status_code == 405  # Method Not Allowed

# Test POST /todos success (create a new todo without ID)
def test_post_todos_success():
    new_todo = {"title": "New Todo", "description": "Description of new todo"}
    response = requests.post(BASE_URL, json=new_todo)
    assert response.status_code == 201  # Created successfully
    assert "id" in response.json()  # Ensure the response contains an ID

# Test POST /todos failure (missing required fields like title)
def test_post_todos_fail():
    new_todo = {"description": "Missing title"}
    response = requests.post(BASE_URL, json=new_todo)
    assert response.status_code == 400  # Bad Request
    assert "title" in response.text  # Check for validation error

# Test DELETE /todos (not allowed)
def test_delete_todos_fail():
    response = requests.delete(BASE_URL, json={"id": 1})
    assert response.status_code == 405  # Method Not Allowed

# Test OPTIONS /todos (not allowed)
def test_options_todos_fail():
    response = requests.options(BASE_URL)
    assert response.status_code == 405  # Method Not Allowed

# Test PATCH /todos (not allowed)
def test_patch_todos_fail():
    response = requests.patch(BASE_URL, json={"id": 1, "title": "Updated Todo"})
    assert response.status_code == 405  # Method Not Allowed

# Test HEAD /todos success (Check existence of todos)
def test_head_todos_success():
    response = requests.head(BASE_URL)
    assert response.status_code == 200  # Expecting a valid response (headers)
    assert response.headers.get("Content-Length") is not None  # Ensure content-length is in the headers

# Test HEAD /todos failure (when no todos available or incorrect URL)
def test_head_todos_fail():
    response = requests.head(f"{BASE_URL}?invalid_param=test")
    assert response.status_code == 400  # Bad Request or appropriate error code

# Boundary Test: Creating a Todo with minimum data (only title)
def test_post_todos_minimum_data():
    new_todo = {"title": "Minimal Todo"}
    response = requests.post(BASE_URL, json=new_todo)
    assert response.status_code == 201
    assert "id" in response.json()

# Boundary Test: Creating a Todo with maximum allowed fields (testing length or other constraints)
def test_post_todos_maximum_data():
    new_todo = {
        "title": "A" * 255,  # Example of very long title
        "description": "B" * 1000,  # Long description
    }
    response = requests.post(BASE_URL, json=new_todo)
    assert response.status_code == 201
    assert "id" in response.json()

# Test GET /todos success when no todos exist (empty list returned)
def test_get_todos_empty():
    # You would need to ensure no todos exist in the DB before running this test
    response = requests.get(BASE_URL)
    assert response.status_code == 200
    assert len(response.json()) == 0

# Test GET /todos with specific query (for filtering)
def test_get_todos_with_query():
    response = requests.get(f"{BASE_URL}?title=Test Todo")
    assert response.status_code == 200
    # Assuming the title 'Test Todo' exists
    assert all(todo['title'] == 'Test Todo' for todo in response.json())
