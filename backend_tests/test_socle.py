from . import client


def test_socle(login):
    status_code, data = client.post("socle", {}, login["token"])
    assert status_code == 200

    assert "c1" in data
    assert "c2" in data
    assert "c3" in data
    assert "c4" in data
    assert "competencies" in data
    assert "containers" in data
    assert "subjects" in data
