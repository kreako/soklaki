from . import client


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
