import pytest
from flaskdraw import create_app


@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True, 
        "SECRET_KEY": "testingkey"
        })
    return app
