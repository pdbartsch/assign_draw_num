import os
import pytest
from flaskdraw import create_app

try:
    from .temp_env_var import TEMP_ENV_VARS, ENV_VARS_TO_SUSPEND
except ImportError:
    TEMP_ENV_VARS = {}
    ENV_VARS_TO_SUSPEND = []

# possible scopes are session, function, class, module and package
# Autouse fixtures are a convenient way to make all tests automatically request them.
@pytest.fixture(scope="session", autouse=True)
def setup_and_teardown():
    # Will be executed before the first test
    old_environ = dict(os.environ)
    os.environ.update(TEMP_ENV_VARS)
    for env_var in ENV_VARS_TO_SUSPEND:
        os.environ.pop(env_var, default=None)

    yield
    # Will be executed after the last test
    os.environ.clear()
    os.environ.update(old_environ)


@pytest.fixture
def app():
    app = create_app()

    return app


@pytest.fixture
def client(app):
    """Configures the app for testing
    Sets app configs
    :return: App for testing
    """
    app.config.update({"TESTING": True, "SECRET_KEY": "testingkey"})
    client = app.test_client()

    yield client
