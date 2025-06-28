import pytest

def test_create_task(client, user_token):
    task_data = {
        "title": "Test Task",
        "description": "Test Description",
        "status": "pending"
    }
    
    response = client.post(
        "/api/v1/tasks/",
        json=task_data,
        headers={"Authorization": f"Bearer {user_token}"}
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == task_data["title"]
    assert data["description"] == task_data["description"]
    assert data["status"] == task_data["status"]

def test_get_tasks(client, user_token):
    # Create a task first
    task_data = {
        "title": "Test Task",
        "description": "Test Description",
        "status": "pending"
    }
    client.post(
        "/api/v1/tasks/",
        json=task_data,
        headers={"Authorization": f"Bearer {user_token}"}
    )
    
    # Get tasks
    response = client.get(
        "/api/v1/tasks/",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data[0]["title"] == task_data["title"]

def test_unauthorized_access(client):
    response = client.get("/api/v1/tasks/")
    assert response.status_code == 403

def test_user_can_only_see_own_tasks(client, user_token, admin_token):
    # User creates a task
    user_task = {
        "title": "User Task",
        "description": "User Description",
        "status": "pending"
    }
    client.post(
        "/api/v1/tasks/",
        json=user_task,
        headers={"Authorization": f"Bearer {user_token}"}
    )
    
    # Admin creates a task
    admin_task = {
        "title": "Admin Task",
        "description": "Admin Description",
        "status": "pending"
    }
    client.post(
        "/api/v1/tasks/",
        json=admin_task,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    # User should only see their task
    response = client.get(
        "/api/v1/tasks/",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == user_task["title"]
    
    # Admin should see both tasks
    response = client.get(
        "/api/v1/tasks/",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2