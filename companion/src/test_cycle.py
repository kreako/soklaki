from datetime import date
from cycle import estimate_cycle


def test_estimate_cycle_c1_1():
    birthdate = date(2015, 11, 2)
    evaluation_date = date(2020, 12, 31)
    assert estimate_cycle(birthdate, evaluation_date) == "c1"


def test_estimate_cycle_c1_2():
    birthdate = date(2015, 11, 2)
    evaluation_date = date(2021, 6, 30)
    assert estimate_cycle(birthdate, evaluation_date) == "c1"


def test_estimate_cycle_c2_1():
    birthdate = date(2015, 11, 2)
    evaluation_date = date(2021, 12, 31)
    assert estimate_cycle(birthdate, evaluation_date) == "c2"


def test_estimate_cycle_c2_2():
    birthdate = date(2015, 11, 2)
    evaluation_date = date(2022, 6, 30)
    assert estimate_cycle(birthdate, evaluation_date) == "c2"


def test_estimate_cycle_c2_3():
    birthdate = date(2015, 11, 2)
    evaluation_date = date(2022, 12, 31)
    assert estimate_cycle(birthdate, evaluation_date) == "c2"


def test_estimate_cycle_c2_4():
    birthdate = date(2015, 11, 2)
    evaluation_date = date(2023, 6, 30)
    assert estimate_cycle(birthdate, evaluation_date) == "c2"


def test_estimate_cycle_c2_5():
    birthdate = date(2015, 11, 2)
    evaluation_date = date(2023, 12, 31)
    assert estimate_cycle(birthdate, evaluation_date) == "c2"


def test_estimate_cycle_c2_6():
    birthdate = date(2015, 11, 2)
    evaluation_date = date(2024, 6, 30)
    assert estimate_cycle(birthdate, evaluation_date) == "c2"


def test_estimate_cycle_c3_1():
    birthdate = date(2015, 11, 2)
    evaluation_date = date(2024, 12, 31)
    assert estimate_cycle(birthdate, evaluation_date) == "c3"


def test_estimate_cycle_c3_2():
    birthdate = date(2015, 11, 2)
    evaluation_date = date(2025, 6, 30)
    assert estimate_cycle(birthdate, evaluation_date) == "c3"


def test_estimate_cycle_c3_3():
    birthdate = date(2015, 11, 2)
    evaluation_date = date(2025, 12, 31)
    assert estimate_cycle(birthdate, evaluation_date) == "c3"


def test_estimate_cycle_c3_4():
    birthdate = date(2015, 11, 2)
    evaluation_date = date(2026, 6, 30)
    assert estimate_cycle(birthdate, evaluation_date) == "c3"


def test_estimate_cycle_c3_5():
    birthdate = date(2015, 11, 2)
    evaluation_date = date(2026, 12, 31)
    assert estimate_cycle(birthdate, evaluation_date) == "c3"


def test_estimate_cycle_c3_6():
    birthdate = date(2015, 11, 2)
    evaluation_date = date(2027, 6, 30)
    assert estimate_cycle(birthdate, evaluation_date) == "c3"


def test_estimate_cycle_c4_1():
    birthdate = date(2015, 11, 2)
    evaluation_date = date(2027, 12, 31)
    assert estimate_cycle(birthdate, evaluation_date) == "c4"


def test_estimate_cycle_c4_2():
    birthdate = date(2015, 11, 2)
    evaluation_date = date(2028, 6, 30)
    assert estimate_cycle(birthdate, evaluation_date) == "c4"