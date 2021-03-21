import logging
import csv
from models import SocleDomain, SocleSubject, SocleComponent, SocleCompetency, SocleCompetencySubject, database


logger = logging.getLogger('root')
FORMAT = "[%(lineno)s:%(funcName)20s() ] %(message)s"
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.DEBUG)


def parse_domain(line):
    rank = int(line[0])
    title = line[1]
    if line[2] != "" or line[3] != "":
        logger.debug(str(line))
        raise ValueError(line)
    domain = SocleDomain(rank=rank, title=title)
    domain.save()
    return domain


def parse_component(domain, line):
    rank = int(line[1])
    title = line[2]
    if line[0] != "" or line[3] != "":
        logger.debug(str(line))
        raise ValueError(line)
    component = SocleComponent(domain=domain, rank=rank, title=title)
    component.save()
    return component


def parse_competency(cycle, component, line):
    rank = int(line[2])
    text = line[3]
    if line[0] != "" or line[1] != "":
        logger.debug(str(line))
        raise ValueError(line)
    competency = SocleCompetency(component=component, rank=rank, text=text, cycle=cycle)
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
        domain = None
        component = None
        while True:
            try:
                line = next(reader)
            except StopIteration:
                break
            try:
                domain = parse_domain(line)
            except ValueError:
                try:
                    component = parse_component(domain, line)
                except ValueError:
                    # on 2 lines
                    competency = parse_competency(cycle, component, line)
                    line = next(reader)
                    parse_subjects(competency, line)


if __name__ == "__main__":
    import sys
    main(sys.argv[1], sys.argv[2])