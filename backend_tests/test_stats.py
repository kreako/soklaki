from . import client


def test_eval_comment_stats(login, periods, students, socle, schools):
    current_period = periods["current_period"]
    token = login["token"]

    data = client.admin_gql(
        """query DefaultSocleCount {
        c1_competencies: default_socle_competency_aggregate(where: { cycle: { _eq: "c1" } }) {
            aggregate { count }
        }
        c2_competencies: default_socle_competency_aggregate(where: { cycle: { _eq: "c2" } }) {
            aggregate { count }
        }
        c3_competencies: default_socle_competency_aggregate(where: { cycle: { _eq: "c3" } }) {
            aggregate { count }
        }
        c4_competencies: default_socle_competency_aggregate(where: { cycle: { _eq: "c4" } }) {
            aggregate { count }
        }
    }""",
        {},
    )
    c1_competencies_count = data["data"]["c1_competencies"]["aggregate"]["count"]
    c2_competencies_count = data["data"]["c2_competencies"]["aggregate"]["count"]
    c3_competencies_count = data["data"]["c3_competencies"]["aggregate"]["count"]
    c4_competencies_count = data["data"]["c4_competencies"]["aggregate"]["count"]

    data = client.admin_gql(
        """query AllSocleCount {
        c1_competencies: socle_competency_aggregate(where: { cycle: { _eq: "c1" } }) {
            aggregate { count }
        }
    }""",
        {},
    )
    all_c1_competencies_count = data["data"]["c1_competencies"]["aggregate"]["count"]

    assert all_c1_competencies_count > c1_competencies_count

    code, data = client.post("stats", {"period_id": current_period["id"]}, token)
    assert code == 200

    assert data["students_c1"]["aggregate"]["count"] == len(students["by_cycle"]["c1"])
    assert data["students_c2"]["aggregate"]["count"] == len(students["by_cycle"]["c2"])
    assert data["students_c3"]["aggregate"]["count"] == len(students["by_cycle"]["c3"])
    assert data["students_c4"]["aggregate"]["count"] == len(students["by_cycle"]["c4"])

    assert data["competencies_c1"]["aggregate"]["count"] == c1_competencies_count
    assert data["competencies_c2"]["aggregate"]["count"] == c2_competencies_count
    assert data["competencies_c3"]["aggregate"]["count"] == c3_competencies_count
    assert data["competencies_c4"]["aggregate"]["count"] == c4_competencies_count