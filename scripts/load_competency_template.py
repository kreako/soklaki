import logging
import csv
from models import (
    DefaultSocleCompetency,
    DefaultSocleCompetencyTemplate,
    database,
)


logger = logging.getLogger("root")
FORMAT = "[%(lineno)s:%(funcName)20s() ] %(message)s"
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.DEBUG)


def main(cycle, input_filename):
    with open(input_filename, "r") as f:
        reader = csv.reader(f)
        try:
            while True:
                line = next(reader)
                rank = line[0].strip()
                competency = (
                    DefaultSocleCompetency.select()
                    .where(
                        DefaultSocleCompetency.full_rank == rank,
                        DefaultSocleCompetency.cycle == cycle,
                    )
                    .execute()[0]
                )
                line = next(reader)
                templates = [t.strip() for t in line[1].split(";")]
                for template in templates:
                    if not template:
                        continue
                    DefaultSocleCompetencyTemplate.create(
                        competency=competency, text=template
                    )
        except StopIteration:
            return


if __name__ == "__main__":
    main("c2", "data/templates_cycle_2.csv")