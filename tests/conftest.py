import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import Base, get_db
from app.core.security import security

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def test_user_data():
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123",
        "role": "user"
    }

@pytest.fixture
def test_admin_data():
    return {
        "username": "testadmin",
        "email": "admin@example.com",
        "password": "adminpassword123",
        "role": "admin"
    }

@pytest.fixture
def user_token(client, test_user_data):
    # Register user
    client.post("/api/v1/auth/register", json=test_user_data)
    
    # Login to get token
    response = client.post("/api/v1/auth/login", json={
        "username_or_email": test_user_data["username"],
        "password": test_user_data["password"]
    })
    return response.json()["access_token"]

@pytest.fixture
def admin_token(client, test_admin_data):
    # Register admin
    client.post("/api/v1/auth/register", json=test_admin_data)
    
    # Login to get token
    response = client.post("/api/v1/auth/login", json={
        "username_or_email": test_admin_data["username"],
        "password": test_admin_data["password"]
    })
    return response.json()["access_token"]