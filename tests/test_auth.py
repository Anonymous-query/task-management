import pytest
from fastapi.testclient import TestClient

def test_register_user(client):
    user_data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "password123",
        "role": "user"
    }
    response = client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == user_data["username"]
    assert data["email"] == user_data["email"]
    assert "password" not in data

def test_register_duplicate_user(client, test_user_data):
    # Register first user
    client.post("/api/v1/auth/register", json=test_user_data)
    
    # Try to register same user again
    response = client.post("/api/v1/auth/register", json=test_user_data)
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]

def test_login_valid_credentials(client, test_user_data):
    # Register user
    client.post("/api/v1/auth/register", json=test_user_data)
    
    # Login with username
    response = client.post("/api/v1/auth/login", json={
        "username_or_email": test_user_data["username"],
        "password": test_user_data["password"]
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials(client, test_user_data):
    # Register user
    client.post("/api/v1/auth/register", json=test_user_data)
    
    # Login with wrong password
    response = client.post("/api/v1/auth/login", json={
        "username_or_email": test_user_data["username"],
        "password": "wrongpassword"
    })
    assert response.status_code == 401