import pytest
from . import client


@pytest.fixture(scope="session")
def test_email():
    return "meuh@meuh.fr"


@pytest.fixture(scope="session")
def test_password():
    return "M30H42"


def delete_group_by_pk(group_id):
    data = client.admin_gql(
        """mutation DeleteGroup($group_id: bigint!) {
        delete_group_by_pk(id: $group_id) {
            id
        }
    }""",
        {"group_id": group_id},
    )
    assert data["data"]["delete_group_by_pk"]["id"] == group_id


@pytest.fixture(scope="session")
def login(test_email, test_password):
    # If user exists (previous test crashed), remove it
    data = client.admin_gql(
        """query TestEmail($email: String!) {
        user(where: {email: {_eq: $email}}) {
            group_id
        }
    }""",
        {"email": test_email},
    )
    for user in data["data"]["user"]:
        # OK for loop not necessary, but this is how graphql API works
        delete_group_by_pk(user["group_id"])

    # Signup
    status_code, data = client.anonymous_post(
        "signup", {"email": test_email, "password": test_password}
    )
    assert status_code == 200
    login_data = {}
    login_data["user_id"] = data["signup"]["id"]
    login_data["group_id"] = data["signup"]["group"]
    login_data["token"] = data["signup"]["token"]
    yield login_data

    # Now Remove the group and the user
    delete_group_by_pk(login_data["group_id"])
