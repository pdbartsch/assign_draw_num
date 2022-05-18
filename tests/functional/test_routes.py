def test_location_list_page(client):
    response = client.get("/locs/")
    assert response.status_code == 200
    assert b"Location List" in response.data

def test_drawings_page(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/drawings/' page is requested (GET)
    THEN check that the response is valid
    """
    response = client.get("/drawings/")
    assert response.status_code == 200
    # assert b"All Projects:" in response.data, "Home page header check"

def test_home_page_post(client):
    """
    GIVEN a Flask application
    WHEN the '/' page is is posted to (POST)
    THEN check that a '405' status code is returned
    """
    response = client.post("/")
    assert response.status_code == 405, "this home page shouldn't allow post requests"
