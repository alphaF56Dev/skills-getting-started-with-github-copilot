from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_unregister_participant_removes_email_from_activity():
    activity_name = "Chess Club"
    email = "student@example.edu"

    client.post(f"/activities/{activity_name}/signup?email={email}")
    response = client.delete(f"/activities/{activity_name}/signup?email={email}")

    assert response.status_code == 200
    assert email not in client.get("/activities").json()[activity_name]["participants"]


def test_unregister_returns_404_for_unknown_activity():
    response = client.delete("/activities/Unknown Activity/signup?email=student@example.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_returns_404_for_participant_not_signed_up():
    response = client.delete("/activities/Chess Club/signup?email=missing@example.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found in activity"
