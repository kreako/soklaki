from datetime import date
from collections import defaultdict
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


@pytest.fixture(scope="session")
def students(login):
    # TODO : make them cycle independant of today using date.today()
    # Anaëlle - C4
    code, data = client.post(
        "insert-student",
        {
            "firstname": "Anaëlle",
            "lastname": "Eanne",
            "birthdate": "2007-05-17",
            "group_id": login["group_id"],
            "school_entry": "2020-07-02",
            "school_exit": "2022-06-30",
        },
        login["token"],
    )
    assert code == 200
    # Charly - C4
    code, data = client.post(
        "insert-student",
        {
            "firstname": "Charly",
            "lastname": "Maou",
            "birthdate": "2006-07-26",
            "group_id": login["group_id"],
            "school_entry": "2020-04-12",
            "school_exit": None,
        },
        login["token"],
    )
    assert code == 200
    # Andrew - C3
    code, data = client.post(
        "insert-student",
        {
            "firstname": "Andrew",
            "lastname": "Éone",
            "birthdate": "2010-06-18",
            "group_id": login["group_id"],
            "school_entry": "2020-06-01",
            "school_exit": None,
        },
        login["token"],
    )
    assert code == 200
    # Clément - C3
    code, data = client.post(
        "insert-student",
        {
            "firstname": "Clément",
            "lastname": "Lilith",
            "birthdate": "2011-12-21",
            "group_id": login["group_id"],
            "school_entry": "2019-06-25",
            "school_exit": None,
        },
        login["token"],
    )
    assert code == 200
    # Élina - C2
    code, data = client.post(
        "insert-student",
        {
            "firstname": "Élina",
            "lastname": "Livia",
            "birthdate": "2012-10-25",
            "group_id": login["group_id"],
            "school_entry": "2020-11-09",
            "school_exit": None,
        },
        login["token"],
    )
    assert code == 200
    # Lili - C2
    code, data = client.post(
        "insert-student",
        {
            "firstname": "Lili",
            "lastname": "Illy",
            "birthdate": "2014-05-15",
            "group_id": login["group_id"],
            "school_entry": "2020-11-06",
            "school_exit": None,
        },
        login["token"],
    )
    assert code == 200
    # Néo - C1
    code, data = client.post(
        "insert-student",
        {
            "firstname": "Néo",
            "lastname": "Drew",
            "birthdate": "2016-04-11",
            "group_id": login["group_id"],
            "school_entry": "2018-07-01",
            "school_exit": None,
        },
        login["token"],
    )
    assert code == 200
    # Olivia - C1
    code, data = client.post(
        "insert-student",
        {
            "firstname": "Olivia",
            "lastname": "Lément",
            "birthdate": "2016-09-09",
            "group_id": login["group_id"],
            "school_entry": "2020-02-04",
            "school_exit": None,
        },
        login["token"],
    )
    assert code == 200

    code, data = client.post(
        "students", {"group_id": login["group_id"]}, login["token"]
    )
    assert code == 200
    students = data["students"]
    by_cycle = defaultdict(list)
    by_id = {}
    by_firstname = {}
    for student in students:
        by_cycle[student["current_cycle"]["current_cycle"]].append(student)
        by_id[student["id"]] = student
        by_firstname[student["firstname"]] = student
    return {
        "students": students,
        "by_cycle": by_cycle,
        "by_id": by_id,
        "by_firstname": by_firstname,
    }


@pytest.fixture(scope="session")
def periods(login):
    return create_periods(login["group_id"], login["token"])


@pytest.fixture(scope="session")
def socle(login):
    status_code, data = client.post("socle", {}, login["token"])
    assert status_code == 200
    return data


@pytest.fixture(scope="session")
def coworker(login):
    data = client.admin_gql(
        """mutation InsertUser($group_id: bigint!) {
        insert_user_one(object: {firstname: "CoWorker",
                                 lastname: "Doe",
                                 active: true,
                                 manager: false,
                                 group_id: $group_id,
                                 hash: "meuh",
                                 email: "coworker@meuh.fr",
                                 email_confirmed: true}) {
            id
        }
    }""",
        {"group_id": login["group_id"]},
    )
    return data["data"]["insert_user_one"]["id"]


@pytest.fixture(scope="session")
def socle(login):
    status, data = client.post(
        "load-socle", {"group_id": login["group_id"]}, login["token"]
    )
    assert data["load_socle"] == {
        "errorNonEmptySocle": False,
        "errorUnknown": False,
        "errorUnknownGroupId": False,
    }

    status_code, socle = client.post("socle", {}, login["token"])
    assert status == 200
    return socle


@pytest.fixture(scope="session")
def schools_credentials():
    return [
        ("school1@school1.fr", "password"),
        ("school2@school2.fr", "password"),
        ("school3@school3.fr", "password"),
        ("school4@school4.fr", "password"),
        ("school5@school5.fr", "password"),
    ]


@pytest.fixture(scope="session")
def schools(schools_credentials):
    """Create other schools"""

    login_data = []
    for (email, password) in schools_credentials:
        # If user exists remove it
        data = client.admin_gql(
            """query TestEmail($email: String!) {
            user(where: {email: {_eq: $email}}) {
                group_id
            }
        }""",
            {"email": email},
        )
        for user in data["data"]["user"]:
            # OK for loop not necessary, but this is how graphql API works
            delete_group_by_pk(user["group_id"])

        # Signup
        status_code, data = client.anonymous_post(
            "signup", {"email": email, "password": password}
        )
        assert status_code == 200
        l_data = {}
        l_data["user_id"] = data["signup"]["id"]
        l_data["group_id"] = data["signup"]["group"]
        l_data["token"] = data["signup"]["token"]
        login_data.append(l_data)

    # MAke sure they have a socle
    for l_data in login_data:
        status, data = client.post(
            "load-socle", {"group_id": l_data["group_id"]}, l_data["token"]
        )
        assert data["load_socle"] == {
            "errorNonEmptySocle": False,
            "errorUnknown": False,
            "errorUnknownGroupId": False,
        }

    # And periods
    for l_data in login_data:
        create_periods(l_data["group_id"], l_data["token"])

    yield login_data

    for l_data in login_data:
        # Now Remove the group and the user
        delete_group_by_pk(l_data["group_id"])


def create_periods(group_id, token):
    today = date.today()
    for year in range(today.year - 3, today.year + 2):
        code, data = client.post(
            "insert-period",
            {
                "group_id": group_id,
                "name": f"{year-1}/{year} S1",
                "start": f"{year-1}-08-31",
                "end": f"{year}-01-31",
            },
            token,
        )
        assert code == 200
        code, data = client.post(
            "insert-period",
            {
                "group_id": group_id,
                "name": f"{year-1}/{year} S2",
                "start": f"{year}-02-01",
                "end": f"{year}-07-31",
            },
            token,
        )
        assert code == 200
    code, data = client.post("boot", {"group_id": group_id}, token)
    assert code == 200
    periods = data["periods"]
    current_period_id = data["current_period"][0]["id"]
    for period in periods:
        if period["id"] == current_period_id:
            current_period = period
            break
    else:
        print(periods)
        print(current_period_id)
        assert False
    return {"periods": periods, "current_period": current_period}