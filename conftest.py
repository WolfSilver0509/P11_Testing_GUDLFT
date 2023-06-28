from server import app
import pytest

@pytest.fixture
def client():
    client = app.test_client()
    yield client

