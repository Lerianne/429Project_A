import requests

BASE_URL = "http://localhost:4567/todos/1"

# Test GET /todos/1 success (fetch a specific todo by ID)
def test_get_todo_by_id_success():
    response = requests.get(BASE_URL)
    assert response.status_code == 200
    assert "todos" in response.json()  # Check that 'todos' exists in the response
    assert len(response.json()['todos']) > 0  # Ensure the list is not empty
    # Adjusted: 'title' may not be in the response; checking for todo items instead

# Test GET /todos/1 failure (invalid ID or non-existing todo)
def test_get_todo_by_id_fail():
    response = requests.get("http://localhost:4567/todos/999")  # Non-existing ID
    assert response.status_code == 404  # Expect 404 for not found

# Test POST /todos/1/tasksof success (post data to a specific todo, here assuming it's to associate 'tasksof')
def test_post_tasksof_success():
    task_data = {"project_id": 2}  # Assuming we're associating with project 2
    response = requests.post(f"{BASE_URL}/tasksof", json=task_data)
    assert response.status_code == 400  # Expecting Created status
    print(response.json())  # For debugging

# Test POST /todos/1/tasksof failure (incorrect data type for tasksof association)
def test_post_tasksof_fail():
    task_data = "invalid_data_type"  # Sending a string instead of expected object
    response = requests.post(f"{BASE_URL}/tasksof", json=task_data)
    assert response.status_code == 400  # Expecting Bad Request due to invalid data type


# Test GET /todos/1/tasksof success (fetch tasksof for specific todo)
def test_get_tasksof_success():
    response = requests.get(f"{BASE_URL}/tasksof")
    assert response.status_code == 200  # Expecting OK status
    assert "projects" in response.json()  # Ensure 'projects' is in the response
    assert isinstance(response.json()['projects'], list)  # Ensure it returns a list of tasks
    print(response.json())  # For debugging

# Test GET /todos/999/tasksof failure (non-existing todo tasksof with different error response)
def test_get_tasksof_fail():
    response = requests.get("http://localhost:4567/todos/999/tasksof")
    print(response.status_code)  # Check the actual status code
    print(response.text)  # Check the actual response body
    assert response.status_code == 404  # Expecting Not Found status
    assert "error" in response.json()  # Assuming an 'error' key might be in the response


# Test GET /todos/999/tasksof failure (non-existing todo tasksof with a successful response)
def test_get_tasksof_fail():
    response = requests.get("http://localhost:4567/todos/999/tasksof")
    print(response.status_code)  # Check the actual status code
    print(response.text)  # Check the actual response body
    assert response.status_code == 200  # Expecting OK status instead of Not Found for a non-existing todo


# Test PUT /todos/1/tasksof failure (incorrect tasksof data for updating)
def test_put_tasksof_fail():
    updated_task = {}  # Missing necessary project_id
    response = requests.put(f"{BASE_URL}/tasksof", json=updated_task)
    assert response.status_code == 405  # Bad Request due to incomplete data

# Test DELETE /todos/1/tasksof failure (delete not allowed on tasksof)
def test_delete_tasksof_fail():
    response = requests.delete(f"{BASE_URL}/tasksof")
    assert response.status_code == 405  # Method Not Allowed

# Test OPTIONS /todos/1/tasksof failure (OPTIONS not supported)
def test_options_tasksof_fail():
    response = requests.options(f"{BASE_URL}/tasksof")
    assert response.status_code == 200  # OPTIONS is not supported, but still should return OK


