# Could be launched with :
# python copy_socle_to_default.py 1 c1 > cycle_1.csv  &&
# python copy_socle_to_default.py 1 c2 > cycle_2.csv &&
# python copy_socle_to_default.py 1 c3 > cycle_3.csv  &&
# python copy_socle_to_default.py 1 c4 > cycle_4.csv

import sys
import logging
import csv
from models import (
    DefaultSocleContainer,
    DefaultSocleSubject,
    DefaultSocleCompetency,
    DefaultSocleCompetencySubject,
    SocleContainer,
    SocleCompetency,
    SocleCompetencySubject,
    SocleSubject,
    database,
)

logger = logging.getLogger("root")
FORMAT = "[%(lineno)s:%(funcName)20s() ] %(message)s"
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.DEBUG)


def emit_container1(writer, container):
    writer.writerow([container.rank, container.text, "", ""])


def emit_container2(writer, container):
    writer.writerow(["", container.rank, container.text, ""])


def emit_competency(writer, competency):
    subjects = [s.subject.title for s in competency.soclecompetencysubject_set]
    writer.writerow(["", "", competency.rank, competency.text])
    writer.writerow(["", "", "", ", ".join(subjects)])


def copy_to_default(cycle, group_id, writer):
    # Copy subjects
    # mapping from original id to default id
    for c1 in (
        SocleContainer.select()
        .where(
            SocleContainer.group_id == group_id,
            SocleContainer.container == None,
            SocleContainer.cycle == cycle,
            SocleContainer.active == True,
        )
        .order_by(SocleContainer.alpha_full_rank)
    ):
        emit_container1(writer, c1)
        for competency in (
            SocleCompetency.select()
            .where(
                SocleCompetency.group_id == group_id,
                SocleCompetency.container_id == c1.id,
                SocleCompetency.active == True,
            )
            .order_by(SocleCompetency.alpha_full_rank)
        ):
            emit_competency(writer, competency)
        for c2 in (
            SocleContainer.select()
            .where(
                SocleContainer.group_id == group_id,
                SocleContainer.group_id == group_id,
                SocleContainer.container_id == c1.id,
                SocleContainer.active == True,
            )
            .order_by(SocleContainer.alpha_full_rank)
        ):
            emit_container2(writer, c2)
            for competency in (
                SocleCompetency.select()
                .where(
                    SocleCompetency.group_id == group_id,
                    SocleCompetency.container_id == c2.id,
                    SocleCompetency.active == True,
                )
                .order_by(SocleCompetency.alpha_full_rank)
            ):
                emit_competency(writer, competency)


def main(group_id, cycle):
    print(f"Copying socle from group {group_id}", file=sys.stderr)
    writer = csv.writer(sys.stdout)
    copy_to_default(cycle, group_id, writer)


if __name__ == "__main__":
    main(int(sys.argv[1]), sys.argv[2])