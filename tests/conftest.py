import pytest
from flaskdraw import create_app

@pytest.fixture
def app():
    app = create_app()
    yield app