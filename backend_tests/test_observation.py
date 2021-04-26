from datetime import date, timedelta
from . import client

# TODO
# delete-observation-competency
# delete-observation-student
# insert-observation-competency
# insert-observation-student
# observations-by-user
# observations-incomplete
# observations-sorted-created-at
# update-observation-text


def test_insert_observation(login, periods):
    # Insert
    today = date.today()
    current_period_id = periods["current_period"]["id"]
    status, data = client.post(
        "insert-observation",
        {
            "text": "Babou le bibi baba",
            "user_id": login["user_id"],
            "eval_period_id": current_period_id,
            "date": str(today),
        },
        login["token"],
    )
    assert status == 200

    data = data["insert_eval_observation_one"]
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


def test_update_observation_date(login, periods, students):
    # Insert
    today = date.today()
    current_period_id = periods["current_period"]["id"]
    status, data = client.post(
        "insert-observation",
        {
            "text": "Babou le bibi baba",
            "user_id": login["user_id"],
            "eval_period_id": current_period_id,
            "date": str(today),
        },
        login["token"],
    )
    assert status == 200

    data = data["insert_eval_observation_one"]
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
    status, data_student = client.post(
        "insert-observation-student",
        {
            "observation_id": data["id"],
            "student_id": anaelle["id"],
        },
        login["token"],
    )
    data_student = data_student["insert_eval_observation_student_one"]["observation"]

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
