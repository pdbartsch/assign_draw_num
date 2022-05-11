def test_home_page_with_fixture(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get('/')
    assert response.status_code == 200
    assert b"UCSB Drawing Numbers" in response.data, "UCSB Drawing Numbers header check"
    assert b"Location Index" in response.data, "navbar location check"
    assert b"Drawings Example" in response.data, "navbar drawings example check"
    assert b"Search by Title" in response.data, "search bar title check"
    assert b"Search by Location" in response.data, "search bar location check"


def test_home_page_post_with_fixture(test_client):
    """
    GIVEN a Flask application
    WHEN the '/' page is is posted to (POST)
    THEN check that a '405' status code is returned
    """
    response = test_client.post('/')
    assert response.status_code == 405, "this home page shouldn't allow post requests"
    assert b"UCSB Drawing Numbers" not in response.data, "if this failed then the page loaded"

