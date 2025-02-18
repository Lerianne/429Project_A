import requests
import pytest

BASE_URL = "http://localhost:5000/todos/1/categories/1"

# Test GET /todos/1/categories/1 failure (GET is not allowed)
def test_get_categories_1_fail():
    response = requests.get(BASE_URL)
    assert response.status_code == 405  # Method Not Allowed

# Test PUT /todos/1/categories/1 failure (PUT is not allowed)
def test_put_categories_1_fail():
    response = requests.put(BASE_URL)
    assert response.status_code == 405  # Method Not Allowed

# Test POST /todos/1/categories/1 failure (POST is not allowed)
def test_post_categories_1_fail():
    response = requests.post(BASE_URL)
    assert response.status_code == 405  # Method Not Allowed

# Test DELETE /todos/1/categories/1 success (delete the instance of the relationship between todo and category)
def test_delete_categories_1_success():
    response = requests.delete(BASE_URL)
    assert response.status_code == 200  # Successfully deleted the relationship
    assert "categories" not in response.json()  # Ensure relationship is deleted

# Test DELETE /todos/1/categories/1 failure (trying to delete a non-existing relationship)
def test_delete_categories_1_fail():
    response = requests.delete("http://localhost:5000/todos/999/categories/1")  # Assuming this todo doesn't exist
    assert response.status_code == 404  # Not Found

# Test OPTIONS /todos/1/categories/1 failure (OPTIONS is not allowed)
def test_options_categories_1_fail():
    response = requests.options(BASE_URL)
    assert response.status_code == 405  # Method Not Allowed

# Test PATCH /todos/1/categories/1 failure (PATCH is not allowed)
def test_patch_categories_1_fail():
    response = requests.patch(BASE_URL, json={"category_id": 2})  # Trying to update the relationship
    assert response.status_code == 405  # Method Not Allowed

# Test HEAD /todos/1/categories/1 failure (HEAD is not allowed)
def test_head_categories_1_fail():
    response = requests.head(BASE_URL)
    assert response.status_code == 405  # Method Not Allowed
