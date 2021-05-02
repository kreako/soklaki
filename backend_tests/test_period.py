from datetime import date
from . import client

# TODO
# insert-period
# periods


def test_insert_period(login):
    code, data = client.post("periods", {"group_id": login["group_id"]}, login["token"])
    assert code == 200
    before_periods = data["periods"]

    code, data = client.post(
        "insert-period",
        {
            "group_id": login["group_id"],
            "name": "ma période",
            "start": "2014-06-01",
            "end": "2015-09-01",
        },
        login["token"],
    )
    assert code == 200
    id = data["insert_eval_period_one"]["id"]

    code, data = client.post("periods", {"group_id": login["group_id"]}, login["token"])
    assert code == 200
    after_periods = data["periods"]

    assert len(before_periods) + 1 == len(after_periods)

    for period in after_periods:
        if period["id"] == id:
            assert period["name"] == "ma période"
            assert period["start"] == "2014-06-01"
            assert period["end"] == "2015-09-01"
            break
    else:
        print(after_periods)
        # If I'm here, it means that my new period is not in periods
        assert 1 == 0


def test_current_period(login, periods):
    today = date.today()
    period = periods["current_period"]
    assert date.fromisoformat(period["start"]) <= today
    assert today <= date.fromisoformat(period["end"])
