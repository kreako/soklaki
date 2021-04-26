import os
from . import client


def test_boot(login, test_email):
    status_code, data = client.post(
        "boot", {"group_id": login["group_id"]}, login["token"]
    )
    assert status_code == 200

    # Assert only defaults immutable things
    # Because other tests may have kicked in to fill data

    # Group
    groups = data["group"]
    assert len(groups) == 1
    group = groups[0]
    assert group["id"] == login["group_id"]
    assert len(group["users"]) == 1
    assert group["users"][0]["id"] == login["user_id"]

    # Users
    users = data["users"]
    assert len(users) == 1
    assert users[0]["email"] == test_email
    assert users[0]["id"] == login["user_id"]

    # Current period
    assert "current_period" in data

    # Periods
    assert "periods" in data

    # Students
    assert "students" in data
