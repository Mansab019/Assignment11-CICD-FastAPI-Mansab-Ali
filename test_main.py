from fastapi.testclient import TestClient
from main import app, tasks

client = TestClient(app)


def setup_function():
    """Clear tasks list before each test to ensure clean state."""
    tasks.clear()


def test_health():
    """GET /health returns 200 and correct status message."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_task():
    """POST /tasks with valid payload returns 201 and the created task."""
    payload = {"title": "Write tests", "done": False}
    response = client.post("/tasks", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Write tests"
    assert data["done"] is False


def test_get_tasks_grows():
    """GET /tasks list grows after a task is created."""
    response = client.get("/tasks")
    assert response.status_code == 200
    initial_count = len(response.json())
    client.post("/tasks", json={"title": "Buy groceries"})
    response = client.get("/tasks")
    assert response.status_code == 200
    updated = response.json()
    assert len(updated) == initial_count + 1
    assert updated[-1]["title"] == "Buy groceries"


def test_create_task_empty_title_fails():
    """POST /tasks with empty title returns 400 Bad Request."""
    response = client.post("/tasks", json={"title": "   "})
    assert response.status_code == 400
    assert "detail" in response.json()


def test_create_task_default_done_is_false():
    """POST /tasks without 'done' field defaults done to False."""
    response = client.post("/tasks", json={"title": "Default done test"})
    assert response.status_code == 201
    assert response.json()["done"] is False
