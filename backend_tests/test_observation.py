from datetime import date, timedelta
from . import client

# TODO
# observations-by-user
# observations-incomplete
# observations-sorted-created-at


def insert_observation(text, user_id, period_id, dt, token):
    status, data = client.post(
        "insert-observation",
        {
            "text": text,
            "user_id": user_id,
            "eval_period_id": period_id,
            "date": str(dt),
        },
        token,
    )
    assert status == 200
    return data["insert_eval_observation_one"]


def insert_observation_student(observation_id, student_id, token):
    status, data = client.post(
        "insert-observation-student",
        {
            "observation_id": observation_id,
            "student_id": student_id,
        },
        token,
    )
    assert status == 200
    return data["insert_eval_observation_student_one"]["observation"]


def insert_observation_competency(observation_id, competency_id, token):
    status, data = client.post(
        "insert-observation-competency",
        {
            "observation_id": observation_id,
            "competency_id": competency_id,
        },
        token,
    )
    assert status == 200
    return data["insert_eval_observation_competency_one"]["observation"]


def delete_observation_student(observation_id, student_id, token):
    status, data = client.post(
        "delete-observation-student",
        {
            "observation_id": observation_id,
            "student_id": student_id,
        },
        token,
    )
    assert status == 200
    return data["delete_eval_observation_student"]["returning"][0]["observation"]


def delete_observation_competency(observation_id, competency_id, token):
    status, data = client.post(
        "delete-observation-competency",
        {
            "observation_id": observation_id,
            "competency_id": competency_id,
        },
        token,
    )
    assert status == 200
    return data["delete_eval_observation_competency"]["returning"][0]["observation"]


def admin_delete_observation(observation_id):
    client.admin_gql(
        """mutation DeleteObservation($observation_id: bigint!) {
        delete_eval_observation_by_pk(id: $observation_id) {
            id
        }
    }""",
        {"observation_id": observation_id},
    )


def test_insert_observation(login, periods):
    # Insert
    today = date.today()
    current_period_id = periods["current_period"]["id"]
    data = insert_observation(
        "Babou le bibi baba", login["user_id"], current_period_id, today, login["token"]
    )
    id = data["id"]

    assert data["text"] == "Babou le bibi baba"
    assert data["user_id"] == login["user_id"]
    assert data["period_id"] == current_period_id
    assert data["date"] == str(today)
    assert data["complete"]["complete"] == False
    assert data["competencies"] == []
    assert data["students"] == []
    assert data["last_evaluations"] == []

    # Get the observation by id
    status, data_by_pk = client.post("observation", {"id": id}, login["token"])
    assert status == 200

    data_by_pk = data_by_pk["eval_observation_by_pk"]
    assert data["text"] == data_by_pk["text"]
    assert data["user_id"] == data_by_pk["user_id"]
    assert data["period_id"] == data_by_pk["period_id"]
    assert data["date"] == data_by_pk["date"]
    assert data["complete"]["complete"] == data_by_pk["complete"]["complete"]
    assert data["competencies"] == data_by_pk["competencies"]
    assert data["students"] == data_by_pk["students"]
    assert data["last_evaluations"] == data_by_pk["last_evaluations"]

    # Cleanup
    admin_delete_observation(id)


def test_update_observation_date(login, periods, students):
    # Insert
    today = date.today()
    current_period_id = periods["current_period"]["id"]
    data = insert_observation(
        "Babou le bibi baba", login["user_id"], current_period_id, today, login["token"]
    )
    id = data["id"]

    assert data["text"] == "Babou le bibi baba"
    assert data["user_id"] == login["user_id"]
    assert data["period_id"] == current_period_id
    assert data["date"] == str(today)
    assert data["complete"]["complete"] == False
    assert data["competencies"] == []
    assert data["students"] == []
    assert data["last_evaluations"] == []

    # Insert student
    anaelle = students["by_firstname"]["Anaëlle"]
    data_student = insert_observation_student(data["id"], anaelle["id"], login["token"])

    assert data_student["text"] == "Babou le bibi baba"
    assert data_student["user_id"] == login["user_id"]
    assert data_student["period_id"] == current_period_id
    assert data_student["date"] == str(today)
    assert data_student["complete"]["complete"] == False
    assert data_student["competencies"] == []
    assert data_student["students"] == [{"student_id": anaelle["id"], "cycle": "c4"}]
    assert data_student["last_evaluations"] == []

    # Update date - check that student cycle is updated accordingly
    d = today - timedelta(days=365 * 3)
    status, data_after = client.post(
        "update-observation-date",
        {
            "id": data["id"],
            "date": str(d),
            "eval_period_id": data["period_id"],
        },
        login["token"],
    )
    data_after = data_after["update_eval_observation_by_pk"]

    assert data_after["text"] == "Babou le bibi baba"
    assert data_after["user_id"] == login["user_id"]
    assert data_after["period_id"] == current_period_id
    assert data_after["date"] == str(d)
    assert data_after["complete"]["complete"] == False
    assert data_after["competencies"] == []
    assert data_after["students"] == [{"student_id": anaelle["id"], "cycle": "c3"}]
    assert data_after["last_evaluations"] == []

    # Cleanup
    admin_delete_observation(id)


def test_update_observation_text(login, periods):
    # Insert
    today = date.today()
    current_period_id = periods["current_period"]["id"]
    data = insert_observation(
        "Babou le bibi baba", login["user_id"], current_period_id, today, login["token"]
    )
    id = data["id"]

    assert data["text"] == "Babou le bibi baba"
    assert data["user_id"] == login["user_id"]
    assert data["period_id"] == current_period_id
    assert data["date"] == str(today)
    assert data["complete"]["complete"] == False
    assert data["competencies"] == []
    assert data["students"] == []
    assert data["last_evaluations"] == []

    # Update text
    status, data_update = client.post(
        "update-observation-text",
        {"id": data["id"], "text": "Babou le bibi bobo"},
        login["token"],
    )
    data_update = data_update["update_eval_observation_by_pk"]

    assert data["id"] == data_update["id"]

    # Get the observation by id
    status, data_by_pk = client.post("observation", {"id": id}, login["token"])
    assert status == 200

    data_by_pk = data_by_pk["eval_observation_by_pk"]
    assert "Babou le bibi bobo" == data_by_pk["text"]
    assert data["user_id"] == data_by_pk["user_id"]
    assert data["period_id"] == data_by_pk["period_id"]
    assert data["date"] == data_by_pk["date"]
    assert data["complete"]["complete"] == data_by_pk["complete"]["complete"]
    assert data["competencies"] == data_by_pk["competencies"]
    assert data["students"] == data_by_pk["students"]
    assert data["last_evaluations"] == data_by_pk["last_evaluations"]

    # Cleanup
    admin_delete_observation(id)


def select_a_competency(socle, cycle):
    for container1 in socle[cycle]:
        if container1["competencies"]:
            return container1["competencies"][0]["id"]
        for container2 in container1["children"]:
            return container2["competencies"][0]["id"]


def test_incomplete_complete(login, periods, students, socle):
    token = login["token"]
    neo = students["by_firstname"]["Néo"]
    anaelle = students["by_firstname"]["Anaëlle"]

    # Insert
    today = date.today()
    current_period_id = periods["current_period"]["id"]
    data = insert_observation(
        "Babou le bibi baba",
        login["user_id"],
        current_period_id,
        today,
        token,
    )
    observation_id = data["id"]
    assert data["complete"]["complete"] == False

    # Add a student
    d = insert_observation_student(observation_id, neo["id"], token)
    assert d["complete"]["complete"] == False
    assert len(d["students"]) == 1
    assert d["students"][0]["student_id"] == neo["id"]
    cycle = d["students"][0]["cycle"]

    # Add corresponding competency
    competency_id_1 = select_a_competency(socle, cycle)
    d = insert_observation_competency(observation_id, competency_id_1, token)
    assert d["complete"]["complete"] == True
    assert len(d["competencies"]) == 1
    assert d["competencies"][0]["competency_id"] == competency_id_1

    # Add another student
    d = insert_observation_student(observation_id, anaelle["id"], token)
    assert d["complete"]["complete"] == False
    assert len(d["students"]) == 2
    assert d["students"][0]["student_id"] == anaelle["id"]
    cycle = d["students"][0]["cycle"]
    assert d["students"][1]["student_id"] == neo["id"]

    # Add corresponding competency
    competency_id_2 = select_a_competency(socle, cycle)
    d = insert_observation_competency(observation_id, competency_id_2, token)
    assert d["complete"]["complete"] == True
    assert len(d["competencies"]) == 2

    # Remove 1 competency
    d = delete_observation_competency(observation_id, competency_id_1, token)
    assert d["complete"]["complete"] == False
    assert len(d["competencies"]) == 1
    assert len(d["students"]) == 2

    # Remove Néo
    d = delete_observation_student(observation_id, neo["id"], token)
    assert d["complete"]["complete"] == True
    assert len(d["competencies"]) == 1
    assert len(d["students"]) == 1

    # Cleanup
    admin_delete_observation(observation_id)
