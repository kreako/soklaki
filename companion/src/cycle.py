from datetime import date, timedelta


YEARS_6 = timedelta(days=6 * 365 + 1)
YEARS_9 = timedelta(days=9 * 365 + 2)
YEARS_12 = timedelta(days=12 * 365 + 3)


def estimate_cycle(birthdate, evaluation_date):
    # First estimate scholar year of the evaluation
    if evaluation_date.month > 8:
        scholar_year = evaluation_date.year
    else:
        scholar_year = evaluation_date.year - 1

    # the date corresponding to the end of the year in the scholar year
    end_of_year = date(scholar_year, 12, 31)
    age = end_of_year - birthdate
    if age < YEARS_6:
        return "c1"
    elif age < YEARS_9:
        return "c2"
    elif age < YEARS_12:
        return "c3"
    else:
        return "c4"