import pytest
import requests

API_URL = "http://localhost:4567"

# Documented Capabilities Tests

def ensure_system_ready():
    try:
        response = requests.get(API_URL)
        assert response.status_code == 200, "API is not active"
    except requests.exceptions.ConnectionError:
        raise AssertionError("API is not active or could not connect")
    
#### PROJECTS/:ID/CATEGORIES ####

def test_post_projects_id_categories():
    project_id = create_project("Test Project for POST Categories")

    category_data = {"title": "Test Category", "description": "Category description"}
    response = requests.post(API_URL + f"/projects/{project_id}/categories", json=category_data)
    assert response.status_code == 201, f"POST /projects/{project_id}/categories failed"

    # Cleanup
    delete_project(project_id)


def test_get_projects_id_categories():
    project_id = create_project("Test Project for GET Categories")

    response = requests.get(API_URL + f"/projects/{project_id}/categories")
    assert response.status_code == 200, f"GET /projects/{project_id}/categories failed"

    # Cleanup
    delete_project(project_id)

### Testing Unsupported HTTP Methods for /projects/:id/categories

def test_put_projects_id_categories():
    # Attempt to PUT a category to a project, which is not allowed
    response = requests.put(API_URL + "/projects/1/categories")
    assert response.status_code == 405, "PUT /projects/1/categories should not be allowed"


def test_patch_projects_id_categories():
    # Attempt to PATCH a category to a project, which is not allowed
    response = requests.patch(API_URL + "/projects/1/categories")
    assert response.status_code == 405, "PATCH /projects/1/categories should not be allowed"


def test_options_projects_id_categories():
    response = requests.options(API_URL + "/projects/1/categories")
    assert response.status_code == 200, "OPTIONS /projects/1/categories failed"

def test_summary():
    ensure_system_ready()

    test_functions = [
        test_post_projects_id_categories,
        test_get_projects_id_categories,
        test_put_projects_id_categories,
        test_patch_projects_id_categories,
        test_options_projects_id_categories,
    ]

    passed_tests = 0
    failed_tests = 0

    print("\nExecuting tests:\n")
    for test in test_functions:
        try:
            test()
            print(f"Test {test.__name__}: PASSED")
            passed_tests += 1
        except AssertionError as e:
            print(f"Test {test.__name__}: FAILED - {e}")
            failed_tests += 1

    print("\nSummary:")
    print(f"Total tests run: {len(test_functions)}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {failed_tests}")


# Running all the tests
if __name__ == "__main__":
    try:
        ensure_system_ready()
        run_tests = True
    except AssertionError as e:
        print(f"System not ready: {e}")
        run_tests = False

    if run_tests:
        test_summary()
# run the tests and shut down after
    if run_tests:
        pytest.main([__file__, "-s"])
        response = requests.get(API_URL)
        assert response.status_code == 200, "API is already shutdown"
        try:
            response = requests.get(API_URL + "/shutdown")
        except requests.exceptions.ConnectionError:
            assert True
    else:
        print("Tests skipped: API is not running or could not be reached.")