import random
from models import Student, User, Group


BIRTH_YEARS = [2021 - x for x in range(5, 16)]
ENTRY_YEARS = [2021 - x for x in range(1, 4)]
MONTHS = range(1, 13)
DAYS = range(1, 27)
FIRSTNAME = [
    "Lili",
    "Lily",
    "Joan",
    "Anaëlle",
    "Néo",
    "Olivia",
    "Élina",
    "Jeanne",
    "Charly",
    "Livio",
    "Andrew",
    "Livio",
    "Clément",
]
LASTNAME = [
    "Ili",
    "Ily",
    "Oan",
    "Naëlle",
    "Éo",
    "Livia",
    "Lina",
    "Eanne",
    "Harly",
    "Ivio",
    "Drew",
    "Ivio",
    "Lément",
]


def random_date(years):
    year = random.choice(years)
    month = random.choice(MONTHS)
    day = random.choice(DAYS)
    return f"{year}-{month:02d}-{day:02d}"


def random_entry_date():
    return random_date(ENTRY_YEARS)


def random_birthdate():
    return random_date(BIRTH_YEARS)


def random_firstname():
    return random.choice(FIRSTNAME)


def random_lastname():
    return random.choice(LASTNAME)


def main(user_id):
    user = User.get(id=user_id)
    group = Group.get(id=user.group_id)
    for i in range(29):
        print(i)
        Student(
            birthdate=random_birthdate(),
            cycle="c2",
            firstname=random_firstname(),
            lastname=random_lastname(),
            group=group,
            school_entry=random_entry_date(),
        ).save()


if __name__ == "__main__":
    import sys

    main(int(sys.argv[1]))
