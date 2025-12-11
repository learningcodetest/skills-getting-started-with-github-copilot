import sys
import os
import uuid
from urllib.parse import quote

from fastapi.testclient import TestClient

# Ensure src is on path so tests can import the app module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from app import app  # noqa: E402

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_unregister_cycle():
    activity = "Chess Club"
    safe_activity = quote(activity, safe="")
    email = f"test+{uuid.uuid4().hex[:8]}@example.com"

    # Sign up
    resp = client.post(f"/activities/{safe_activity}/signup?email={email}")
    assert resp.status_code == 200

    # Verify participant was added
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert email in data[activity]["participants"]

    # Unregister
    resp = client.delete(f"/activities/{safe_activity}/unregister?email={email}")
    assert resp.status_code == 200

    # Verify participant was removed
    resp = client.get("/activities")
    data = resp.json()
    assert email not in data[activity]["participants"]
