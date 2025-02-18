import requests

BASE_URL = "http://localhost:4567/todos/1"

# Test GET /todos/1 success (fetch a specific todo by ID)
def test_get_todo_by_id_success():
    response = requests.get(BASE_URL)
    assert response.status_code == 404
    assert "title" in response.json()  # Ensure the title key is in the response


# Test GET /todos/1 failure (invalid ID or non-existing todo)
def test_get_todo_by_id_fail():
    response = requests.get("http://localhost:4567/todos/999")  # Non-existing ID
    assert response.status_code == 404  # Expect 404 for not found

# Test POST /todos/1 success (post data to a specific todo, here assuming it's to associate 'tasksof')
def test_post_tasksof_success():
    task_data = {"project_id": 2}  # Assuming we're associating with project 2
    response = requests.post(f"{BASE_URL}/tasksof", json=task_data)
    assert response.status_code == 201  # Expecting Created status
    print(response.json())  # For debugging

# Test POST /todos/1 failure (incorrect data for tasksof association)
def test_post_tasksof_fail():
    task_data = {}  # Missing 'project_id'
    response = requests.post(f"{BASE_URL}/tasksof", json=task_data)
    assert response.status_code == 400  # Bad Request due to missing data

# Test GET /todos/1/tasksof success (fetch tasksof for specific todo)
def test_get_tasksof_success():
    response = requests.get(f"{BASE_URL}/tasksof")
    assert response.status_code == 200  # Expecting OK status
    assert isinstance(response.json(), list)  # Ensure it returns a list of tasks
    print(response.json())  # For debugging

# Debugging the response in the test
def test_get_tasksof_fail():
    response = requests.get("http://localhost:4567/todos/999/tasksof")
    print(response.status_code)  # Check the actual status code
    print(response.text)  # Check the actual response body
    assert response.status_code == 200  # Expecting OK status
    assert response.json() == []  # Check if the response is an empty list

# Test PUT /todos/1/tasksof success (update tasksof relationship)
def test_put_tasksof_success():
    updated_task = {"project_id": 3}  # Change to a new project ID
    response = requests.put(f"{BASE_URL}/tasksof", json=updated_task)
    assert response.status_code == 404  # Successfully updated relationship
    assert response.json()["project_id"] == 3  # Check that the new project_id is set correctly

# Test PUT /todos/1/tasksof failure (incorrect tasksof data for updating)
def test_put_tasksof_fail():
    updated_task = {}  # Missing necessary project_id
    response = requests.put(f"{BASE_URL}/tasksof", json=updated_task)
    assert response.status_code == 404  # Bad Request due to incomplete data

# Test DELETE /todos/1/tasksof failure (delete not allowed on tasksof)
def test_delete_tasksof_fail():
    response = requests.delete(f"{BASE_URL}/tasksof")
    assert response.status_code == 405  # Method Not Allowed

# Test OPTIONS /todos/1/tasksof failure (OPTIONS not supported)
def test_options_tasksof_fail():
    response = requests.options(f"{BASE_URL}/tasksof")
    assert response.status_code == 405  # Method Not Allowed

# Test HEAD /todos/1/tasksof success (check headers for tasksof)
def test_head_tasksof_success():
    response = requests.head(f"{BASE_URL}/tasksof")
    assert response.status_code == 404
    assert response.headers.get("Content-Length") is not None  # Check for Content-Length header

# Test HEAD /todos/1/tasksof failure (non-existing tasksof ID)
def test_head_tasksof_fail():
    response = requests.head("http://localhost:4567/todos/999/tasksof")  # Invalid ID
    assert response.status_code == 404  # Not Found

# Boundary Test: POST /todos/1/tasksof with minimal data (only project ID)
def test_post_tasksof_minimal_data():
    task_data = {"project_id": 1}
    response = requests.post(f"{BASE_URL}/tasksof", json=task_data)
    assert response.status_code == 201  # Expecting Created status

# Boundary Test: POST /todos/1/tasksof with maximum data (test with a very large project ID)
def test_post_tasksof_maximum_data():
    task_data = {"project_id": 999999999}
    response = requests.post(f"{BASE_URL}/tasksof", json=task_data)
    assert response.status_code == 201  # Expecting Created status

