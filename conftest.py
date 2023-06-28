from pytest import fixture
from server import app
from flask.testing import FlaskClient

@fixture
def client() -> FlaskClient:
    with app.test_client() as client:
        yield client

