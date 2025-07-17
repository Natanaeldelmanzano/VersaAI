import pytest
import asyncio
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.main import app
from src.core.database import get_db, Base

# Test database URL (SQLite for testing)
TEST_DATABASE_URL = "sqlite:///./test_versaai.db"

# Create test engine
test_engine = create_engine(
    TEST_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# Create test session
TestingSessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=test_engine
)

def override_get_db():
    """Override database dependency for testing"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Override the dependency
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test"""
    # Create tables
    Base.metadata.create_all(bind=test_engine)
    
    # Create session
    session = TestingSessionLocal()
    
    try:
        yield session
    finally:
        session.close()
        # Drop tables after test
        Base.metadata.drop_all(bind=test_engine)

@pytest.fixture(scope="function")
def client() -> Generator[TestClient, None, None]:
    """Create a test client"""
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture
def sample_user_data():
    """Sample user data for testing"""
    return {
        "email": "test@example.com",
        "password": "testpassword123",
        "full_name": "Test User",
        "organization_name": "Test Organization"
    }

@pytest.fixture
def sample_chatbot_data():
    """Sample chatbot data for testing"""
    return {
        "name": "Test Chatbot",
        "description": "A test chatbot",
        "system_prompt": "You are a helpful assistant.",
        "model": "mixtral-8x7b-32768",
        "temperature": 0.7,
        "max_tokens": 1000
    }