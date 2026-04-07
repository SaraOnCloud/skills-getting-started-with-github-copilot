def test_root_redirects_to_index_html(client):
    # Arrange
    url = "/"

    # Act
    response = client.get(url)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_all_activities(client):
    # Arrange
    url = "/activities"

    # Act
    response = client.get(url)
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert "Chess Club" in data
    assert data["Chess Club"]["description"] == "Learn strategies and compete in chess tournaments"
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_for_activity_adds_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "test.student@mergington.edu"
    signup_url = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(signup_url, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"

    # Act (verify update)
    activities_response = client.get("/activities")
    activities_data = activities_response.json()

    # Assert (verify participant stored)
    assert email in activities_data[activity_name]["participants"]


def test_signup_for_activity_already_registered_returns_400(client):
    # Arrange
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"
    signup_url = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(signup_url, params={"email": existing_email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_for_unknown_activity_returns_404(client):
    # Arrange
    signup_url = "/activities/Unknown Activity/signup"
    unknown_email = "student@mergington.edu"

    # Act
    response = client.post(signup_url, params={"email": unknown_email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
