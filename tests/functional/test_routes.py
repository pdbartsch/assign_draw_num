import os
from urllib import response
from flask import url_for


def test_landing_aliases(client):
    # tests that aliases return same results
    landing = client.get("/")
    assert client.get(url_for("main.index")).data == landing.data


def test_home_page(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    response = client.get(url_for("main.index"))
    html = response.data.decode()
    # test for successful request
    assert response.status_code == 200
    # test navbar links when logged out
    assert 'href="/locs/">Location Index</a>' in html, "location navbar link check"
    assert (
        'href="/search_drawings/">Search Drawings</a>' in html
    ), "search drawings navbar link check"
    assert 'href="/login">Admin Login</a>' in html, "login navbar link check"
    # assert "href=\"/register\">Register</a>" in html, "register navbar link check"
    # test navbar classes
    assert "nav-item nav-link" in html, "navbar class check"
    # test homepage content
    assert "All Projects" in html, "Header check"
    # test search results
    assert "Filter by title" in html, "search bar title check"
    assert "Filter by location" in html, "search bar location check"


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
    assert (
        b"Projects Associated with Title like library" in response.data
    ), "Header check"


def test_home_page_lnum_parameter(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/?lnum=525' page is requested (GET)
    THEN check that the response is valid
    """
    response = client.get(url_for("main.index", lnum=525))
    assert response.status_code == 200
    assert b"Projects Associated with Location 525" in response.data, "Header check"


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
    WHEN the locations (/locs/) page is requested (GET)
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


# requires login
def test_register_page_get(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the register page is requested (GET)
    THEN check that the response is valid
    """

    response = client.get(url_for("users.register"))
    assert response.status_code == 200


def test_register_page_post(client):
    response = client.post(url_for("users.register"), follow_redirects=True)
    assert response.status_code == 200


def test_login_page_get(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the login page is requested (GET)
    THEN check that the response is valid
    """

    response = client.get(url_for("users.login"))
    assert response.status_code == 200


def test_login_page_post(client):
    response = client.post(url_for("users.login"), follow_redirects=True)
    assert response.status_code == 200


def test_not_logged_in(client):
    """
    GIVEN a Flask application configured for testing and no user logged in
    WHEN the '/' page is requested (GET)
    THEN check that the response doesn't contain protected links
    """
    response = client.get(url_for("main.index"))
    assert (
        b"Assign Drawing Number" not in response.data
    ), "Protected Navbar Link Check 01"
    assert b"Add Drawing" not in response.data, "Protected Navbar Link Check 02"
    assert b"Add Location" not in response.data, "Protected Navbar Link Check 03"


def test_assign_drawing_number(client):
    response = client.get(url_for("drawproj.create"), follow_redirects=True)
    assert response.status_code == 200


def test_add_drawing(client):
    response = client.get(url_for("drawproj.add_drawing"), follow_redirects=True)
    assert response.status_code == 200


def test_add_location(client):
    response = client.get(url_for("drawproj.add_loc"), follow_redirects=True)
    assert response.status_code == 200


def test_logout(client):
    response = client.get(url_for("users.logout"), follow_redirects=True)
    assert response.status_code == 200


def test_drawproj_page(client):
    response = client.get(
        url_for("drawproj.location_set", locnum=525), follow_redirects=True
    )
    assert response.status_code == 200


def test_drawproj_drawings_locnum(client):
    response = client.get(
        url_for("drawproj.drawings", locnum=525), follow_redirects=True
    )
    assert response.status_code == 200


def test_drawproj_drawings_drawnum(client):
    response = client.get(
        url_for("drawproj.drawings", drawnum=101), follow_redirects=True
    )
    assert response.status_code == 200
    assert (
        b"Your query returned no results" in response.data
    ), "Should NOT return results"


def test_drawproj_drawings_draw_n_locnums(client):
    response = client.get(
        url_for("drawproj.drawings", drawnum=101, locnum=525), follow_redirects=True
    )
    assert response.status_code == 200
    assert (
        b"Your query returned no results" not in response.data
    ), "Should return results"


def test_drawproj_drawings_nonsense(client):
    response = client.get(
        url_for("drawproj.drawings", nonsense=101), follow_redirects=True
    )
    assert response.status_code == 200
    assert (
        b"Your query returned no results" in response.data
    ), "Should NOT return results"
