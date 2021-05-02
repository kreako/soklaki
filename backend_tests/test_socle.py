import random
from . import client

CYCLES = ["c1", "c2", "c3", "c4"]


def test_socle(login, socle):
    assert "c1" in socle
    assert "c2" in socle
    assert "c3" in socle
    assert "c4" in socle
    assert "competencies" in socle
    assert "containers" in socle
    assert "subjects" in socle


def test_invalid_group_load_socle(login):
    status, data = client.post(
        "load-socle", {"group_id": login["group_id"] + 2}, login["token"]
    )
    assert data["load_socle"] == {
        "errorNonEmptySocle": False,
        "errorUnknown": False,
        "errorUnknownGroupId": True,
    }

    status, data = client.post("load-socle", {"group_id": -1}, login["token"])
    assert data["load_socle"] == {
        "errorNonEmptySocle": False,
        "errorUnknown": False,
        "errorUnknownGroupId": True,
    }


def test_non_empty_load_socle(login, socle):
    # Now it is already loaded by fixture
    status, data = client.post(
        "load-socle", {"group_id": login["group_id"]}, login["token"]
    )
    assert data["load_socle"] == {
        "errorNonEmptySocle": True,
        "errorUnknown": False,
        "errorUnknownGroupId": False,
    }


def test_load_socle(login, socle):
    assert "c1" in socle
    assert "c2" in socle
    assert "c3" in socle
    assert "c4" in socle
    assert "competencies" in socle
    assert "containers" in socle
    assert "subjects" in socle

    data = client.admin_gql(
        """ query socle_counts($group_id: bigint!) {
                default_socle_subject_aggregate {
                    aggregate {
                        count
                    }
                }
                default_socle_container_aggregate {
                    aggregate {
                        count
                    }
                }
                default_socle_competency_aggregate {
                    aggregate {
                        count
                    }
                }
                default_socle_competency_subject_aggregate {
                    aggregate {
                        count
                    }
                }
                socle_subject_aggregate(where: {group_id: {_eq: $group_id}}) {
                    aggregate {
                        count
                    }
                }
                socle_container_aggregate(where: {group_id: {_eq: $group_id}}) {
                    aggregate {
                        count
                    }
                }
                socle_competency_aggregate(where: {group_id: {_eq: $group_id}}) {
                    aggregate {
                        count
                    }
                }
                socle_competency_subject_aggregate(where: {competency: {group_id: {_eq: $group_id}}}) {
                    aggregate {
                        count
                    }
                }
            }""",
        {"group_id": login["group_id"]},
    )
    data = data["data"]
    assert (
        data["default_socle_subject_aggregate"]["aggregate"]["count"]
        == data["socle_subject_aggregate"]["aggregate"]["count"]
    )
    assert (
        data["default_socle_container_aggregate"]["aggregate"]["count"]
        == data["socle_container_aggregate"]["aggregate"]["count"]
    )
    assert (
        data["default_socle_competency_aggregate"]["aggregate"]["count"]
        == data["socle_competency_aggregate"]["aggregate"]["count"]
    )
    assert (
        data["default_socle_competency_subject_aggregate"]["aggregate"]["count"]
        == data["socle_competency_subject_aggregate"]["aggregate"]["count"]
    )

    assert (
        len(socle["competencies"])
        == data["socle_competency_aggregate"]["aggregate"]["count"]
    )
    assert (
        len(socle["containers"])
        == data["socle_container_aggregate"]["aggregate"]["count"]
    )
    assert (
        len(socle["subjects"]) == data["socle_subject_aggregate"]["aggregate"]["count"]
    )


def test_socle_subject_active(login, socle):
    subject_ids = map(lambda x: x["id"], socle["subjects"])
    subject_id = random.choice(list(subject_ids))
    # assert subject["active"] == True
    status, data = client.post(
        "update-socle-subject-active",
        {"id": subject_id, "active": False},
        login["token"],
    )
    assert status == 200
    assert data["update_socle_subject_by_pk"]["id"] == subject_id

    status_code, socle = client.post("socle", {}, login["token"])
    assert status == 200
    # Check disappearance in subjects
    subject_ids = map(lambda x: x["id"], socle["subjects"])
    assert subject_id not in list(subject_ids)
    # Check disappearance in competencies
    for competency in socle["competencies"]:
        subject_ids = map(lambda x: x["subject_id"], competency["subjects"])
        assert subject_id not in list(subject_ids)
    subject_ids = map(lambda x: x["id"], socle["subjects"])
    # Check disappearance in socle tree structure
    for cycle in CYCLES:
        for l1 in socle[cycle]:
            for competency in l1["competencies"]:
                for subject in competency["subjects"]:
                    # Beautiful 4 level nested for loops
                    # Glory begins now
                    assert subject["subject_id"] != subject_id
            for l2 in socle[cycle]:
                for competency in l2["competencies"]:
                    for subject in competency["subjects"]:
                        # I knew I could do better
                        # Look at this beautiful 5 level nested for loop
                        assert subject["subject_id"] != subject_id

    status, data = client.post(
        "update-socle-subject-active",
        {"id": subject_id, "active": True},
        login["token"],
    )
    assert status == 200
    assert data["update_socle_subject_by_pk"]["id"] == subject_id

    status_code, socle = client.post("socle", {}, login["token"])
    assert status == 200
    subject_ids = map(lambda x: x["id"], socle["subjects"])
    assert subject_id in list(subject_ids)


def test_socle_subject_title(login, socle):
    subject_ids = map(lambda x: x["id"], socle["subjects"])
    subject_id = random.choice(list(subject_ids))
    subject = filter(lambda x: x["id"] == subject_id, socle["subjects"]).__next__()
    old_title = subject["title"]

    status, data = client.post(
        "update-socle-subject-title",
        {"id": subject_id, "title": "meuh"},
        login["token"],
    )
    assert status == 200
    assert data["update_socle_subject_by_pk"]["id"] == subject_id

    status_code, socle = client.post("socle", {}, login["token"])
    assert status == 200
    subject = filter(lambda x: x["id"] == subject_id, socle["subjects"]).__next__()
    assert subject["title"] == "meuh"

    status, data = client.post(
        "update-socle-subject-title",
        {"id": subject_id, "title": old_title},
        login["token"],
    )
    assert status == 200
    assert data["update_socle_subject_by_pk"]["id"] == subject_id

    status_code, socle = client.post("socle", {}, login["token"])
    assert status == 200
    subject = filter(lambda x: x["id"] == subject_id, socle["subjects"]).__next__()
    assert subject["title"] == old_title


def test_socle_competency_subject_active(login, socle):
    # select a link
    link = socle["c4"][0]["children"][0]["competencies"][0]["subjects"][0]
    subject_id = link["subject_id"]
    link_id = link["id"]

    # active = False
    status, data = client.post(
        "update-socle-competency-subject-active",
        {"id": link_id, "active": False},
        login["token"],
    )
    assert status == 200
    assert data["update_socle_competency_subject_by_pk"]["id"] == link_id

    # Disappeared from socle
    status_code, socle = client.post("socle", {}, login["token"])
    assert status == 200
    subjects = socle["c4"][0]["children"][0]["competencies"][0]["subjects"]
    if len(subjects) > 0:
        link = subjects[0]
        assert link["id"] != link_id
    else:
        assert len(subjects) == 0

    # active = True
    status, data = client.post(
        "update-socle-competency-subject-active",
        {"id": link_id, "active": True},
        login["token"],
    )
    assert status == 200
    assert data["update_socle_competency_subject_by_pk"]["id"] == link_id

    # Reappeared
    status_code, socle = client.post("socle", {}, login["token"])
    assert status == 200
    link = socle["c4"][0]["children"][0]["competencies"][0]["subjects"][0]
    assert link["id"] == link_id


def test_socle_competency_active(login, socle):
    competency_ids = map(lambda x: x["id"], socle["competencies"])
    competency_id = random.choice(list(competency_ids))

    # active = False
    status, data = client.post(
        "update-socle-competency-active",
        {"id": competency_id, "active": False},
        login["token"],
    )
    assert status == 200
    assert data["update_socle_competency_by_pk"]["id"] == competency_id

    # Not in socle anymore
    status_code, socle = client.post("socle", {}, login["token"])
    assert status == 200
    competency_ids = list(map(lambda x: x["id"], socle["competencies"]))
    assert competency_id not in competency_ids

    for cycle in CYCLES:
        for l1 in socle[cycle]:
            for competency in l1["competencies"]:
                assert competency["id"] != competency_id
            for l2 in l1["children"]:
                for competency in l2["competencies"]:
                    assert competency["id"] != competency_id

    # active = True
    status, data = client.post(
        "update-socle-competency-active",
        {"id": competency_id, "active": True},
        login["token"],
    )
    assert status == 200
    assert data["update_socle_competency_by_pk"]["id"] == competency_id

    # Back in socle
    status_code, socle = client.post("socle", {}, login["token"])
    assert status == 200
    competency_ids = list(map(lambda x: x["id"], socle["competencies"]))
    assert competency_id in competency_ids


def test_socle_container_active(login, socle):
    container_ids = map(lambda x: x["id"], socle["containers"])
    container_id = random.choice(list(container_ids))

    # active = False
    status, data = client.post(
        "update-socle-container-active",
        {"id": container_id, "active": False},
        login["token"],
    )
    assert status == 200
    assert data["update_socle_container_by_pk"]["id"] == container_id

    # Not in socle
    status_code, socle = client.post("socle", {}, login["token"])
    assert status == 200
    container_ids = list(map(lambda x: x["id"], socle["containers"]))
    assert container_id not in container_ids

    for cycle in CYCLES:
        for l1 in socle[cycle]:
            assert l1["id"] != container_id
            for l2 in l1["children"]:
                assert l2["id"] != container_id

    # active = True
    status, data = client.post(
        "update-socle-container-active",
        {"id": container_id, "active": True},
        login["token"],
    )
    assert status == 200
    assert data["update_socle_container_by_pk"]["id"] == container_id

    # Back in socle
    status_code, socle = client.post("socle", {}, login["token"])
    assert status == 200
    container_ids = list(map(lambda x: x["id"], socle["containers"]))
    assert container_id in container_ids


def test_socle_competency_container_id(login, socle):
    competency_ids = map(lambda x: x["id"], socle["competencies"])
    competency_id = random.choice(list(competency_ids))
    data = client.gql(
        """ query Competency($id: Int!) {
                socle_competency_by_pk(id: $id) {
                    alpha_full_rank
                    full_rank
                    container_id
                }
            }""",
        {"id": competency_id},
        login["token"],
    )
    competency = data["data"]["socle_competency_by_pk"]

    # Select a random container
    container_ids = map(lambda x: x["id"], socle["containers"])
    container_id = None
    while container_id == None or container_id == competency["container_id"]:
        container_id = random.choice(list(container_ids))

    # Set container id
    status, data = client.post(
        "update-socle-competency-container-id",
        {
            "id": competency_id,
            "alpha_full_rank": "ac0",
            "full_rank": "c0",
            "container_id": container_id,
        },
        login["token"],
    )
    assert status == 200
    assert data["update_socle_competency_by_pk"]["id"] == competency_id

    # Modified
    data = client.gql(
        """ query Competency($id: Int!) {
                socle_competency_by_pk(id: $id) {
                    alpha_full_rank
                    full_rank
                    container_id
                }
            }""",
        {"id": competency_id},
        login["token"],
    )
    new_competency = data["data"]["socle_competency_by_pk"]
    assert new_competency["alpha_full_rank"] == "ac0"
    assert new_competency["full_rank"] == "c0"
    assert competency["container_id"] != new_competency["container_id"]
    assert new_competency["container_id"] == container_id

    # Set container id back
    status, data = client.post(
        "update-socle-competency-container-id",
        {
            "id": competency_id,
            "alpha_full_rank": competency["alpha_full_rank"],
            "full_rank": competency["full_rank"],
            "container_id": competency["container_id"],
        },
        login["token"],
    )
    assert status == 200
    assert data["update_socle_competency_by_pk"]["id"] == competency_id

    # Back as before
    data = client.gql(
        """ query Competency($id: Int!) {
                socle_competency_by_pk(id: $id) {
                    alpha_full_rank
                    full_rank
                    container_id
                }
            }""",
        {"id": competency_id},
        login["token"],
    )
    new_competency = data["data"]["socle_competency_by_pk"]
    assert new_competency["alpha_full_rank"] == competency["alpha_full_rank"]
    assert new_competency["full_rank"] == competency["full_rank"]
    assert new_competency["container_id"] == competency["container_id"]


def test_socle_container_container_id(login, socle):
    token = login["token"]
    container_ids = list(map(lambda x: x["id"], socle["containers"]))
    container_id = random.choice(container_ids)
    data = client.gql(
        """ query Container($id: Int!) {
                socle_container_by_pk(id: $id) {
                    alpha_full_rank
                    full_rank
                    container_id
                }
            }""",
        {"id": container_id},
        token,
    )
    container = data["data"]["socle_container_by_pk"]

    # Select a random container as parent
    parent_id = None
    while parent_id == None or parent_id == container_id:
        parent_id = random.choice(container_ids)

    # Set container id
    status, data = client.post(
        "update-socle-container-container-id",
        {
            "id": container_id,
            "alpha_full_rank": "meuha",
            "full_rank": "meuh",
            "container_id": parent_id,
        },
        token,
    )
    assert status == 200
    assert data["update_socle_container_by_pk"]["id"] == container_id

    # Modified
    data = client.gql(
        """ query Container($id: Int!) {
                socle_container_by_pk(id: $id) {
                    alpha_full_rank
                    full_rank
                    container_id
                }
            }""",
        {"id": container_id},
        token,
    )
    new_container = data["data"]["socle_container_by_pk"]
    assert new_container["container_id"] == parent_id
    assert new_container["alpha_full_rank"] == "meuha"
    assert new_container["full_rank"] == "meuh"

    # Set container id as None
    status, data = client.post(
        "update-socle-container-container-id",
        {
            "id": container_id,
            "alpha_full_rank": "remeuha",
            "full_rank": "remeuh",
            "container_id": None,
        },
        token,
    )
    assert status == 200
    assert data["update_socle_container_by_pk"]["id"] == container_id

    # Modified
    data = client.gql(
        """ query Container($id: Int!) {
                socle_container_by_pk(id: $id) {
                    alpha_full_rank
                    full_rank
                    container_id
                }
            }""",
        {"id": container_id},
        token,
    )
    new_container = data["data"]["socle_container_by_pk"]
    assert new_container["container_id"] == None
    assert new_container["alpha_full_rank"] == "remeuha"
    assert new_container["full_rank"] == "remeuh"

    # Set container id back
    status, data = client.post(
        "update-socle-container-container-id",
        {
            "id": container_id,
            "container_id": container["container_id"],
            "alpha_full_rank": container["alpha_full_rank"],
            "full_rank": container["full_rank"],
        },
        token,
    )
    assert status == 200
    assert data["update_socle_container_by_pk"]["id"] == container_id

    # Back as before
    data = client.gql(
        """ query Container($id: Int!) {
                socle_container_by_pk(id: $id) {
                    alpha_full_rank
                    full_rank
                    container_id
                }
            }""",
        {"id": container_id},
        token,
    )
    new_container = data["data"]["socle_container_by_pk"]
    assert new_container["container_id"] == container["container_id"]
    assert new_container["alpha_full_rank"] == container["alpha_full_rank"]
    assert new_container["full_rank"] == container["full_rank"]


def test_socle_competency_rank(login, socle):
    token = login["token"]
    competency_ids = map(lambda x: x["id"], socle["competencies"])
    competency_id = random.choice(list(competency_ids))
    data = client.gql(
        """ query Competency($id: Int!) {
                socle_competency_by_pk(id: $id) {
                    alpha_full_rank
                    full_rank
                    rank
                }
            }""",
        {"id": competency_id},
        token,
    )
    competency = data["data"]["socle_competency_by_pk"]

    # Set rank
    new_rank = 99
    new_full_rank = "98.99"
    new_alpha_full_rank = "0098.0099"
    status, data = client.post(
        "update-socle-competency-rank",
        {
            "id": competency_id,
            "rank": new_rank,
            "full_rank": new_full_rank,
            "alpha_full_rank": new_alpha_full_rank,
        },
        token,
    )
    assert status == 200
    assert data["update_socle_competency_by_pk"]["id"] == competency_id

    # Modified
    data = client.gql(
        """ query Competency($id: Int!) {
                socle_competency_by_pk(id: $id) {
                    alpha_full_rank
                    full_rank
                    rank
                }
            }""",
        {"id": competency_id},
        token,
    )
    new_competency = data["data"]["socle_competency_by_pk"]
    assert new_competency["rank"] == new_rank
    assert new_competency["full_rank"] == new_full_rank
    assert new_competency["alpha_full_rank"] == new_alpha_full_rank

    # Set rank back
    status, data = client.post(
        "update-socle-competency-rank",
        {
            "id": competency_id,
            "rank": competency["rank"],
            "full_rank": competency["full_rank"],
            "alpha_full_rank": competency["alpha_full_rank"],
        },
        token,
    )
    assert status == 200
    assert data["update_socle_competency_by_pk"]["id"] == competency_id

    # Back in socle
    data = client.gql(
        """ query Competency($id: Int!) {
                socle_competency_by_pk(id: $id) {
                    alpha_full_rank
                    full_rank
                    rank
                }
            }""",
        {"id": competency_id},
        token,
    )
    new_competency = data["data"]["socle_competency_by_pk"]
    assert new_competency["rank"] == competency["rank"]
    assert new_competency["full_rank"] == competency["full_rank"]
    assert new_competency["alpha_full_rank"] == competency["alpha_full_rank"]


def test_socle_container_rank(login, socle):
    token = login["token"]
    container_ids = map(lambda x: x["id"], socle["containers"])
    container_id = random.choice(list(container_ids))
    data = client.gql(
        """ query Container($id: Int!) {
                socle_container_by_pk(id: $id) {
                    alpha_full_rank
                    full_rank
                    rank
                }
            }""",
        {"id": container_id},
        token,
    )
    container = data["data"]["socle_container_by_pk"]

    # Set rank
    new_rank = 99
    new_full_rank = "98.99"
    new_alpha_full_rank = "0098.0099"
    status, data = client.post(
        "update-socle-container-rank",
        {
            "id": container_id,
            "rank": new_rank,
            "full_rank": new_full_rank,
            "alpha_full_rank": new_alpha_full_rank,
        },
        token,
    )
    assert status == 200
    assert data["update_socle_container_by_pk"]["id"] == container_id

    # Modified
    data = client.gql(
        """ query Container($id: Int!) {
                socle_container_by_pk(id: $id) {
                    alpha_full_rank
                    full_rank
                    rank
                }
            }""",
        {"id": container_id},
        token,
    )
    new_container = data["data"]["socle_container_by_pk"]
    assert new_container["rank"] == new_rank
    assert new_container["full_rank"] == new_full_rank
    assert new_container["alpha_full_rank"] == new_alpha_full_rank

    # Set rank back
    status, data = client.post(
        "update-socle-container-rank",
        {
            "id": container_id,
            "rank": container["rank"],
            "full_rank": container["full_rank"],
            "alpha_full_rank": container["alpha_full_rank"],
        },
        token,
    )
    assert status == 200
    assert data["update_socle_container_by_pk"]["id"] == container_id

    # Back in socle
    data = client.gql(
        """ query Container($id: Int!) {
                socle_container_by_pk(id: $id) {
                    alpha_full_rank
                    full_rank
                    rank
                }
            }""",
        {"id": container_id},
        token,
    )
    new_container = data["data"]["socle_container_by_pk"]
    assert new_container["rank"] == container["rank"]
    assert new_container["full_rank"] == container["full_rank"]
    assert new_container["alpha_full_rank"] == container["alpha_full_rank"]


def test_socle_competency_text(login, socle):
    token = login["token"]
    competency_ids = map(lambda x: x["id"], socle["competencies"])
    competency_id = random.choice(list(competency_ids))
    competency = filter(
        lambda x: x["id"] == competency_id, socle["competencies"]
    ).__next__()

    # Set text
    status, data = client.post(
        "update-socle-competency-text",
        {
            "id": competency_id,
            "text": "meuh",
        },
        token,
    )
    assert status == 200
    assert data["update_socle_competency_by_pk"]["id"] == competency_id

    # Modified in socle
    status_code, socle = client.post("socle", {}, token)
    assert status == 200
    new_competency = filter(
        lambda x: x["id"] == competency_id, socle["competencies"]
    ).__next__()
    assert new_competency["text"] == "meuh"

    # Set back
    status, data = client.post(
        "update-socle-competency-text",
        {
            "id": competency_id,
            "text": competency["text"],
        },
        token,
    )
    assert status == 200
    assert data["update_socle_competency_by_pk"]["id"] == competency_id

    # back in socle
    status_code, socle = client.post("socle", {}, token)
    assert status == 200
    new_competency = filter(
        lambda x: x["id"] == competency_id, socle["competencies"]
    ).__next__()
    assert new_competency["text"] == competency["text"]


def test_socle_container_text(login, socle):
    token = login["token"]
    container_ids = map(lambda x: x["id"], socle["containers"])
    container_id = random.choice(list(container_ids))
    container = filter(
        lambda x: x["id"] == container_id, socle["containers"]
    ).__next__()

    # Set text
    status, data = client.post(
        "update-socle-container-text",
        {
            "id": container_id,
            "text": "meuh",
        },
        token,
    )
    assert status == 200
    assert data["update_socle_container_by_pk"]["id"] == container_id

    # Modified in socle
    status_code, socle = client.post("socle", {}, token)
    assert status == 200
    new_container = filter(
        lambda x: x["id"] == container_id, socle["containers"]
    ).__next__()
    assert new_container["text"] == "meuh"

    # Set back
    status, data = client.post(
        "update-socle-container-text",
        {
            "id": container_id,
            "text": container["text"],
        },
        token,
    )
    assert status == 200
    assert data["update_socle_container_by_pk"]["id"] == container_id

    # back in socle
    status_code, socle = client.post("socle", {}, token)
    assert status == 200
    new_container = filter(
        lambda x: x["id"] == container_id, socle["containers"]
    ).__next__()
    assert new_container["text"] == container["text"]


def test_socle_insert_container(login, socle):
    token = login["token"]

    # insert
    status, data = client.post(
        "insert-socle-container",
        {
            "alpha_full_rank": "098.099",
            "container_id": None,
            "cycle": "c1",
            "full_rank": "98.99",
            "group_id": login["group_id"],
            "rank": 99,
            "text": "meuh",
        },
        token,
    )
    assert status == 200
    container_id = data["insert_socle_container_one"]["id"]

    # Verify
    data = client.gql(
        """ query Container($id: Int!) {
                socle_container_by_pk(id: $id) {
                    alpha_full_rank
                    container_id
                    cycle
                    full_rank
                    group_id
                    rank
                    text
                }
            }""",
        {"id": container_id},
        token,
    )
    container = data["data"]["socle_container_by_pk"]
    assert container["alpha_full_rank"] == "098.099"
    assert container["container_id"] == None
    assert container["cycle"] == "c1"
    assert container["full_rank"] == "98.99"
    assert container["group_id"] == login["group_id"]
    assert container["rank"] == 99
    assert container["text"] == "meuh"

    # Cleanup
    data = client.admin_gql(
        """ mutation DeleteContainer($id: Int!) {
                delete_socle_container_by_pk(id: $id) {
                    id
                }
            }""",
        {"id": container_id},
    )
    assert data["data"]["delete_socle_container_by_pk"]["id"] == container_id


def test_socle_insert_competency(login, socle):
    token = login["token"]
    container_ids = map(lambda x: x["id"], socle["containers"])
    container_id = random.choice(list(container_ids))

    # insert
    status, data = client.post(
        "insert-socle-competency",
        {
            "alpha_full_rank": "098.099",
            "container_id": container_id,
            "cycle": "c1",
            "full_rank": "98.99",
            "group_id": login["group_id"],
            "rank": 99,
            "text": "meuh",
        },
        token,
    )
    assert status == 200
    competency_id = data["insert_socle_competency_one"]["id"]

    # Verify
    data = client.gql(
        """ query Competency($id: Int!) {
                socle_competency_by_pk(id: $id) {
                    alpha_full_rank
                    container_id
                    cycle
                    full_rank
                    group_id
                    rank
                    text
                }
            }""",
        {"id": competency_id},
        token,
    )
    competency = data["data"]["socle_competency_by_pk"]
    assert competency["alpha_full_rank"] == "098.099"
    assert competency["container_id"] == container_id
    assert competency["cycle"] == "c1"
    assert competency["full_rank"] == "98.99"
    assert competency["group_id"] == login["group_id"]
    assert competency["rank"] == 99
    assert competency["text"] == "meuh"

    # Cleanup
    data = client.admin_gql(
        """ mutation DeleteCompetency($id: Int!) {
                delete_socle_competency_by_pk(id: $id) {
                    id
                }
            }""",
        {"id": competency_id},
    )
    assert data["data"]["delete_socle_competency_by_pk"]["id"] == competency_id


def test_socle_insert_subject(login, socle):
    token = login["token"]

    # insert
    status, data = client.post(
        "insert-socle-subject",
        {
            "title": "meuh",
            "group_id": login["group_id"],
        },
        token,
    )
    assert status == 200
    subject_id = data["insert_socle_subject_one"]["id"]

    # Verify
    data = client.gql(
        """ query Subject($id: Int!) {
                socle_subject_by_pk(id: $id) {
                    group_id
                    title
                }
            }""",
        {"id": subject_id},
        token,
    )
    subject = data["data"]["socle_subject_by_pk"]
    assert subject["group_id"] == login["group_id"]
    assert subject["title"] == "meuh"

    # Cleanup
    data = client.admin_gql(
        """ mutation DeleteCompetency($id: Int!) {
                delete_socle_subject_by_pk(id: $id) {
                    id
                }
            }""",
        {"id": subject_id},
    )
    assert data["data"]["delete_socle_subject_by_pk"]["id"] == subject_id


def test_socle_insert_competency_subject(login, socle):
    token = login["token"]
    competency_ids = list(map(lambda x: x["id"], socle["competencies"]))
    competency_id = random.choice(competency_ids)
    competency = filter(
        lambda x: x["id"] == competency_id, socle["competencies"]
    ).__next__()
    competency_subject_ids = list(
        map(lambda x: x["subject_id"], competency["subjects"])
    )
    print(competency_subject_ids)

    for subject in socle["subjects"]:
        subject_id = subject["id"]
        print(subject_id)
        if subject_id not in competency_subject_ids:
            # found one
            break

    # insert
    status, data = client.post(
        "insert-socle-competency-subject",
        {
            "competency_id": competency_id,
            "subject_id": subject_id,
        },
        token,
    )
    assert status == 200
    link_id = data["insert_socle_competency_subject_one"]["id"]

    # Verify
    status_code, socle = client.post("socle", {}, token)
    assert status == 200
    competency = filter(
        lambda x: x["id"] == competency_id, socle["competencies"]
    ).__next__()
    competency_subject_ids = list(
        map(lambda x: x["subject_id"], competency["subjects"])
    )
    assert subject_id in competency_subject_ids

    # Cleanup
    data = client.admin_gql(
        """ mutation DeleteCompetencySubject($id: Int!) {
                delete_socle_competency_subject_by_pk(id: $id) {
                    id
                }
            }""",
        {"id": link_id},
    )
    assert data["data"]["delete_socle_competency_subject_by_pk"]["id"] == link_id
