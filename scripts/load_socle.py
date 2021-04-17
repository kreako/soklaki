import logging
import csv
from models import (
    SocleContainer,
    SocleSubject,
    SocleCompetency,
    SocleCompetencySubject,
    database,
)


logger = logging.getLogger("root")
FORMAT = "[%(lineno)s:%(funcName)20s() ] %(message)s"
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.DEBUG)


def parse_container(cycle, container, line):
    if line[0] != "" and line[1] != "" and line[2] == "" and line[3] == "":
        # level 1 container
        rank = int(line[0])
        text = line[1]
        c = SocleContainer(
            container=None,
            cycle=cycle,
            rank=rank,
            full_rank=f"{rank}.",
            alpha_full_rank=f"{rank:02d}.",
            text=text,
        )
        c.save()
        return c
    if line[0] == "" and line[1] != "" and line[2] != "" and line[3] == "":
        # level 2 container
        rank = int(line[1])
        text = line[2]
        if container.container is not None:
            # root container is not yet a level 1
            container = container.container
        full_rank = f"{container.rank}.{rank}."
        alpha_full_rank = f"{container.rank:02d}.{rank:02d}."
        c = SocleContainer(
            container=container,
            cycle=cycle,
            rank=rank,
            full_rank=full_rank,
            alpha_full_rank=alpha_full_rank,
            text=text,
        )
        c.save()
        return c
    raise ValueError(line)


def parse_competency(cycle, container, line):
    rank = int(line[2])
    text = line[3]
    if line[0] != "" or line[1] != "":
        logger.debug(str(line))
        raise ValueError(line)
    full_rank = f"{container.full_rank}{rank}."
    alpha_full_rank = f"{container.alpha_full_rank}{rank:02d}."
    competency = SocleCompetency(
        container=container,
        full_rank=full_rank,
        alpha_full_rank=alpha_full_rank,
        rank=rank,
        text=text,
        cycle=cycle,
    )
    competency.save()
    return competency


def parse_subjects(competency, line):
    subjects = [s.strip() for s in line[3].split(",")]
    for subject in subjects:
        s, _ = SocleSubject.get_or_create(title=subject)
        SocleCompetencySubject(competency=competency, subject=s).save()


def main(cycle, input_filename):
    with open(input_filename, "r") as f:
        reader = csv.reader(f)
        container = None
        try:
            while True:
                line = next(reader)
                print(line)
                try:
                    container = parse_container(cycle, container, line)
                except ValueError:
                    # on 2 lines
                    competency = parse_competency(cycle, container, line)
                    line = next(reader)
                    parse_subjects(competency, line)
        except StopIteration:
            return


if __name__ == "__main__":
    main("c1", "data/cycle_1.csv")
    main("c2", "data/cycle_2.csv")
    main("c3", "data/cycle_3.csv")
    main("c4", "data/cycle_4.csv")
