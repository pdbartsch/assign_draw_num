from urllib import response
from flask import url_for, request


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


def test_register_page(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the register page is requested (GET)
    THEN check that the response is valid
    """

    response = client.get(url_for("users.register"))
    assert response.status_code == 200


def test_logging_in_test_user(client):
    """Login helper function"""
    return client.post(
        url_for("users.login"),
        data=dict(email="osospdb@gmail.com", password="testing"),
        follow_redirects=True,
    )


# the following tests require user to be logged in:
# def test_create_project(client):
#     """
#     GIVEN a Flask application configured for testing
#     WHEN the create new project page is requested (GET)
#     THEN check that the response is valid
#     """
#     login(client)
#     response = client.get(url_for("drawproj.create"))
#     assert response.status_code == 200
