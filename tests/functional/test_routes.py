from flask import url_for
import os


def test_home_page(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    response = client.get(url_for("main.index"))
    assert response.status_code == 200
    assert b"All Projects" in response.data, "Header check"
    assert b"Location Index" in response.data, "navbar location check"
    assert b"Search Drawings" in response.data, "navbar drawings search check"
    assert b"Filter by title" in response.data, "search bar title check"
    assert b"Filter by location" in response.data, "search bar location check"


def test_home_page_lnum_parameter(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/?lnum=525' page is requested (GET)
    THEN check that the response is valid
    """
    response = client.get(url_for("main.index", lnum=525))
    assert response.status_code == 200


def test_home_page_searched_parameter(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/?searched=library' page is requested (GET)
    THEN check that the response is valid
    """
    response = client.get(url_for("main.index", searched="library"))
    assert response.status_code == 200


def test_home_page_post(client):
    """
    GIVEN a Flask application
    WHEN the '/' page is posted to (POST)
    THEN check that a '405' status code is returned
    """
    response = client.post(url_for("main.index"))
    assert response.status_code == 405, "this home page shouldn't allow post requests"
    assert b"All Projects:" not in response.data, "if this failed then the page loaded"


def test_location_list_page(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the locations page is requested (GET)
    THEN check that the response is valid
    """
    response = client.get(url_for("drawproj.locations"), follow_redirects=True)
    assert response.status_code == 200
    assert b"Location List" in response.data


def test_drawings_page(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the drawings page is requested (GET)
    THEN check that the response is valid
    """
    response = client.get(url_for("drawproj.drawings"), follow_redirects=True)
    assert response.status_code == 200
    assert b"Result of drawing search:" in response.data, "Home page header check"


def test_list_projects_one_locnum(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/locnum' page is requested (GET)
    THEN check that the response is valid
    """
    response = client.get("/525", follow_redirects=True)
    assert response.status_code == 200
    assert b"UCSB Drawing #525-" in response.data, "UCSB Drawing Numbers header check"


def test_list_single_project(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/locnum/drawnum' page is requested (GET)
    THEN check that the response is valid
    """
    response = client.get("/525/120", follow_redirects=True)
    assert response.status_code == 200
    assert (
        b"UCSB Drawing #525-120" in response.data
    ), "UCSB Drawing Numbers header check"


def test_drawing_search_page(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the drawing search page is requested (GET)
    THEN check that the response is valid
    """

    response = client.get(url_for("drawproj.search_drawings"))
    assert response.status_code == 200
    assert b"Search For Drawings:" in response.data, "Home page header check"


def test_login_page(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the login page is requested (GET)
    THEN check that the response is valid
    """

    response = client.get(url_for("users.login"))
    assert response.status_code == 200


def test_register_page_get(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the register page is requested (GET)
    THEN check that the response is valid
    """

    response = client.get(url_for("users.register"))
    assert response.status_code == 200

def test_register_page_post(client):
    response = client.post(
        url_for("users.register"),
        follow_redirects=True
        )
    assert response.status_code == 200

def test_login_page_get(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the register page is requested (GET)
    THEN check that the response is valid
    """

    response = client.get(url_for("users.login"))
    assert response.status_code == 200

def test_login_page_post(client):
    response = client.post(
        url_for("users.login"),
        follow_redirects=True
        )
    assert response.status_code == 200


def test_not_logged_in(client):
    """
    GIVEN a Flask application configured for testing and no user logged in
    WHEN the '/' page is requested (GET)
    THEN check that the response doesn't contain protected links
    """
    response = client.get(url_for("main.index"))
    assert b"Assign Drawing Number" not in response.data, "Protected Navbar Link Check 01"
    assert b"Add Drawing" not in response.data, "Protected Navbar Link Check 02"
    assert b"Add Location" not in response.data, "Protected Navbar Link Check 03"

def test_temp_env_var(client):
    key = os.environ.get("SECRET_KEY")
    assert key == "testingkey"