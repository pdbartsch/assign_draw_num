import os
import pytest
from flaskdraw import create_app
from flaskdraw.config import TestConfig
from flaskdraw.models import User, Drawfile, Drawings, Drawloc


@pytest.fixture
def app():
    app = create_app(TestConfig)

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture(scope="module")
def new_user():
    user = User(
        username="testuser", email="testuser@testing.com", password="FlaskIsAwesome"
    )
    return user


@pytest.fixture(scope="module")
def new_location():
    ilp_bldg = Drawloc(locnum=506, locdescrip="Interactive Learning Pavillion")
    return ilp_bldg
