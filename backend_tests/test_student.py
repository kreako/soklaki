from . import client


def test_students(login):
    code, data = client.post("students", {}, login["token"])
    assert code == 200
    assert "students" in data


def test_insert_students(login):
    code, data = client.post("students", {}, login["token"])
    assert code == 200
    before_students = data["students"]

    code, data = client.post(
        "insert-student",
        {
            "birthdate": "2015-11-02",
            "firstname": "Bibou",
            "group_id": login["group_id"],
            "lastname": "Babou",
            "school_entry": "2019-03-14",
            "school_exit": None,
        },
        login["token"],
    )
    assert code == 200
    student_id = data["insert_student_one"]["id"]

    code, data = client.post("students", {}, login["token"])
    assert code == 200
    after_students = data["students"]

    assert len(before_students) + 1 == len(after_students)

    for student in after_students:
        if student["id"] == student_id:
            assert student["birthdate"] == "2015-11-02"
            assert student["firstname"] == "Bibou"
            assert student["group_id"] == login["group_id"]
            assert student["lastname"] == "Babou"
            assert student["school_entry"] == "2019-03-14"
            assert student["school_exit"] == None
            break
    else:
        print(after_students)
        # I should have break from the for loop
        # It means my student was not found :(
        assert 1 == 0

    client.admin_gql(
        """mutation DeleteStudent($student_id: bigint!) {
        delete_student_by_pk(id: $student_id) {
            id
        }
    }""",
        {"student_id": student_id},
    )


def check(login, students, patch_id, patch_prop, patch_value):
    # List and check
    code, data = client.post("students", {}, login["token"])
    assert code == 200
    after_students = data["students"]
    assert len(students["students"]) == len(after_students)
    for i, student in enumerate(after_students):
        print("i", i, "student", student)
        ref = students["by_id"][student["id"]]
        for prop in student:
            print("prop", prop)
            if prop == patch_prop and student["id"] == patch_id:
                assert student[prop] == patch_value
            else:
                assert student[prop] == ref[prop]


def test_update_student_birthdate(login, students):
    # Patch Néo - younger so c1 do not change
    # Warning this test will maybe break in 2 years when Néo won't be in C1 anymore
    neo = students["by_firstname"]["Néo"]
    assert neo["birthdate"] == "2016-04-11"

    code, data = client.post(
        "update-student-birthdate",
        {"student_id": neo["id"], "birthdate": "2017-03-14"},
        login["token"],
    )
    assert code == 200

    # List and check
    check(login, students, neo["id"], "birthdate", "2017-03-14")

    # Patch back
    code, data = client.post(
        "update-student-birthdate",
        {"student_id": neo["id"], "birthdate": "2016-04-11"},
        login["token"],
    )
    assert code == 200

    # List and check
    check(login, students, None, None, None)


def test_update_student_lastname(login, students):
    # Patch Charly
    charly = students["by_firstname"]["Charly"]
    assert charly["lastname"] == "Maou"

    code, data = client.post(
        "update-student-lastname",
        {"student_id": charly["id"], "lastname": "Miaou"},
        login["token"],
    )
    assert code == 200

    # List and check
    check(login, students, charly["id"], "lastname", "Miaou")

    # Patch back
    code, data = client.post(
        "update-student-lastname",
        {"student_id": charly["id"], "lastname": "Maou"},
        login["token"],
    )
    assert code == 200

    # List and check
    check(login, students, None, None, None)


def test_update_student_firstname(login, students):
    # Patch Olivia
    olivia = students["by_firstname"]["Olivia"]
    assert olivia["firstname"] == "Olivia"

    code, data = client.post(
        "update-student-firstname",
        {"student_id": olivia["id"], "firstname": "Olivier"},
        login["token"],
    )
    assert code == 200

    # List and check
    check(login, students, olivia["id"], "firstname", "Olivier")

    # Patch back
    code, data = client.post(
        "update-student-firstname",
        {"student_id": olivia["id"], "firstname": "Olivia"},
        login["token"],
    )
    assert code == 200

    # List and check
    check(login, students, None, None, None)


def test_update_student_school_entry(login, students):
    # Patch Anaëlle
    anaelle = students["by_firstname"]["Anaëlle"]
    assert anaelle["school_entry"] == "2020-07-02"

    code, data = client.post(
        "update-student-school-entry",
        {"student_id": anaelle["id"], "school_entry": "2018-03-15"},
        login["token"],
    )
    assert code == 200

    # List and check
    check(login, students, anaelle["id"], "school_entry", "2018-03-15")

    # Patch back
    code, data = client.post(
        "update-student-school-entry",
        {"student_id": anaelle["id"], "school_entry": "2020-07-02"},
        login["token"],
    )
    assert code == 200

    # List and check
    check(login, students, None, None, None)


def test_update_student_school_exit(login, students):
    # Patch Anaëlle
    anaelle = students["by_firstname"]["Anaëlle"]
    assert anaelle["school_exit"] == "2022-06-30"

    code, data = client.post(
        "update-student-school-exit",
        {"student_id": anaelle["id"], "school_exit": "2020-07-30"},
        login["token"],
    )
    assert code == 200

    # List and check
    check(login, students, anaelle["id"], "school_exit", "2020-07-30")

    # Patch to None (school_exit is nullable)
    code, data = client.post(
        "update-student-school-exit",
        {"student_id": anaelle["id"], "school_exit": None},
        login["token"],
    )
    assert code == 200

    # List and check
    check(login, students, anaelle["id"], "school_exit", None)

    # Patch back
    code, data = client.post(
        "update-student-school-exit",
        {"student_id": anaelle["id"], "school_exit": "2022-06-30"},
        login["token"],
    )
    assert code == 200

    # List and check
    check(login, students, None, None, None)
