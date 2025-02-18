import requests
import pytest

BASE_URL = "http://localhost:4567/todos/1/categories"

# Test GET /todos/1/categories success (fetch all category items related to the todo by relationship "categories")
def test_get_categories_success():
    response = requests.get(BASE_URL)
    assert response.status_code == 200
    # Assuming response contains an array of category objects
    assert isinstance(response.json(), list)  # Ensure it is a list
    assert len(response.json()) > 0  # At least one category should be related to the todo

# Test GET /todos/1/categories failure (when no categories are associated with the todo)
def test_get_categories_fail():
    response = requests.get("http://localhost:4567/todos/999/categories")  # Assuming this todo doesn't exist
    assert response.status_code == 404  # Not Found

# Test PUT /todos/1/categories failure (PUT is not allowed)
def test_put_categories_fail():
    response = requests.put(BASE_URL)
    assert response.status_code == 405  # Method Not Allowed

# Test POST /todos/1/categories success (create a category relationship between the todo and a category)
def test_post_categories_success():
    category_data = {"category_id": 2}  # Assuming we are creating a relationship with a category with ID 2
    response = requests.post(BASE_URL, json=category_data)
    assert response.status_code == 200  # Successfully created the relationship
    assert "categories" in response.json()  # Check the relationship exists

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
    assert response.status_code == 405  # Method Not Allowed

# Test PATCH /todos/1/categories failure (PATCH is not allowed)
def test_patch_categories_fail():
    response = requests.patch(BASE_URL, json={"category_id": 3})  # Trying to update the relationship
    assert response.status_code == 405  # Method Not Allowed

# Test HEAD /todos/1/categories success (headers for category items related to todo by categories relationship)
def test_head_categories_success():
    response = requests.head(BASE_URL)
    assert response.status_code == 200  # Should be successful (headers returned)
    assert response.headers.get("Content-Length") is not None  # Ensure content-length header is present

# Test HEAD /todos/1/categories failure (wrong todo ID)
def test_head_categories_fail():
    response = requests.head("http://localhost:4567/todos/999/categories")  # Invalid todo ID
    assert response.status_code == 404  # Not Found

# Boundary Test: POST with a valid but minimal data (only category ID)
def test_post_categories_minimal_data():
    category_data = {"category_id": 1}  # Minimal valid data (category ID only)
    response = requests.post(BASE_URL, json=category_data)
    assert response.status_code == 200  # Successfully created the relationship

# Boundary Test: POST with maximum data (check large category ID or other constraints)
def test_post_categories_maximum_data():
    category_data = {"category_id": 999999999}  # Very large category ID to check limits
    response = requests.post(BASE_URL, json=category_data)
    assert response.status_code == 200  # Successfully created the relationship
    assert response.json()["category_id"] == 999999999

HELLO