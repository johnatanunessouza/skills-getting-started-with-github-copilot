import pytest


def test_get_activities(client):
    # Arrange: client fixture provides a fresh app instance

    # Act
    resp = client.get("/activities")

    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert len(data) >= 1


def test_signup_and_duplicate_and_remove(client):
    # Arrange
    resp = client.get("/activities")
    activities = resp.json()
    activity_name = list(activities.keys())[0]
    test_email = "test.student@example.com"

    # Act: sign up the student
    signup_resp = client.post(f"/activities/{activity_name}/signup", params={"email": test_email})

    # Assert: signup succeeded and participant present
    assert signup_resp.status_code == 200
    participants_after_signup = client.get("/activities").json()[activity_name]["participants"]
    assert test_email in participants_after_signup

    # Arrange (repeat): same email to trigger duplicate behavior

    # Act: sign up again
    duplicate_resp = client.post(f"/activities/{activity_name}/signup", params={"email": test_email})

    # Assert: allowed duplicate appended
    assert duplicate_resp.status_code == 200
    participants = client.get("/activities").json()[activity_name]["participants"]
    assert participants.count(test_email) >= 2

    # Act: remove one occurrence
    remove_resp = client.delete(f"/activities/{activity_name}/participants", params={"email": test_email})

    # Assert: removal succeeded and count decreased by one
    assert remove_resp.status_code == 200
    participants_after = client.get("/activities").json()[activity_name]["participants"]
    assert participants_after.count(test_email) == participants.count(test_email) - 1


def test_remove_nonexistent_returns_404(client):
    # Arrange
    resp = client.get("/activities")
    activity_name = list(resp.json().keys())[0]
    missing_email = "noone@nowhere.example"

    # Act
    remove_resp = client.delete(f"/activities/{activity_name}/participants", params={"email": missing_email})

    # Assert
    assert remove_resp.status_code == 404
