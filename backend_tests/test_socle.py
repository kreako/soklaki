from . import client


def test_socle(login, socle):
    assert "c1" in socle
    assert "c2" in socle
    assert "c3" in socle
    assert "c4" in socle
    assert "competencies" in socle
    assert "containers" in socle
    assert "subjects" in socle
