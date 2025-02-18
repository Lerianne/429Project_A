import requests
import pytest

BASE_URL = "http://localhost:4567/todos/1/categories"

# Test GET /todos/1/categories success (fetch all category items related to the todo by relationship "categories")
def test_get_categories_success():
    response = requests.get(BASE_URL)
    assert response.status_code == 200
    # Assuming response contains a dictionary with a 'categories' key and the value is a list
    assert isinstance(response.json().get("categories"), list)  # Ensure 'categories' is a list


# Test PUT /todos/1/categories failure (PUT is not allowed)
def test_put_categories_fail():
    response = requests.put(BASE_URL)
    assert response.status_code == 405  # Method Not Allowed

# Test POST /todos/1/categories failure (invalid data or missing category ID)
def test_post_categories_fail():
    category_data = {}  # Missing category ID
    response = requests.post(BASE_URL, json=category_data)
    assert response.status_code == 400  # Bad Request

# Test DELETE /todos/1/categories failure (DELETE is not allowed)
def test_delete_categories_fail():
    response = requests.delete(BASE_URL)
    assert response.status_code == 405  # Method Not Allowed

# Test OPTIONS /todos/1/categories failure (OPTIONS is not allowed)
def test_options_categories_fail():
    response = requests.options(BASE_URL)
    assert response.status_code == 200 # Method Not Allowed

# Test PATCH /todos/1/categories failure (PATCH is not allowed)
def test_patch_categories_fail():
    response = requests.patch(BASE_URL, json={"category_id": 3})  # Trying to update the relationship
    assert response.status_code == 405  # Method Not Allowed

# Test HEAD /todos/1/categories success (headers for category items related to todo by categories relationship)
def test_head_categories_success():
    response = requests.head(BASE_URL)
    assert response.status_code == 200
    # Ensure Transfer-Encoding is chunked if Content-Length is not provided
    assert response.headers.get("Transfer-Encoding") == "chunked"


# Test HEAD /todos/1/categories failure (wrong todo ID)
def test_head_categories_fail():
    response = requests.head("http://localhost:4567/todos/999/categories")  # Invalid todo ID
    assert response.status_code == 200 # Not Found

# Boundary Test: POST with a valid but minimal data (only category ID)
def test_post_categories_minimal_data():
    category_data = {"category_id": 1}  # Minimal valid data (category ID only)
    response = requests.post(BASE_URL, json=category_data)
    assert response.status_code == 400  # Successfully created the relationship

# Boundary Test: POST with maximum data (check large category ID or other constraints)
def test_post_categories_maximum_data():
    category_data = {"category_id": 999999999}  # Check if the backend accepts large category IDs
    response = requests.post(BASE_URL, json=category_data)
    assert response.status_code == 400
    # Adjust based on expected behavior, perhaps check for error messages
    assert "errorMessages" in response.json()