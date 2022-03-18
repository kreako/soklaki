import logging
import csv
from models import (
    SocleCompetency,
    SocleContainer,
    database,
)

def emit_container1(writer, container):
    writer.writerow([container.rank, container.text, "", ""])


def emit_container2(writer, container):
    writer.writerow(["", container.rank, container.text, ""])


def emit_competency(writer, competency):
    subjects = [s.subject.title for s in competency.soclecompetencysubject_set]
    writer.writerow(["", "", competency.rank, competency.text])
    writer.writerow(["", "", "", ", ".join(subjects)])


def emit_cycle(writer, cycle, group_id):
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


def main(input_filename, cycle, group_id):
    with open(input_filename, "w") as f:
        writer = csv.writer(f)
        emit_cycle(writer, cycle, group_id)


if __name__ == "__main__":
    main("export/cycle_1.csv", "c1", 1)
    main("export/cycle_2.csv", "c2", 1)
    main("export/cycle_3.csv", "c3", 1)
    main("export/cycle_4.csv", "c4", 1)