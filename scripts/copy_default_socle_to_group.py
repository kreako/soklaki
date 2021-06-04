import logging
import sys
import csv
from models import (
    DefaultSocleCompetency,
    DefaultSocleCompetencyTemplate,
    SocleCompetency,
    SocleCompetencyTemplate,
    database,
)


logger = logging.getLogger("root")
FORMAT = "[%(lineno)s:%(funcName)20s() ] %(message)s"
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.DEBUG)


def copy_default_templates(group_id):
    found = 0
    not_found = 0
    for default_template in DefaultSocleCompetencyTemplate.select():
        default_competency = default_template.competency
        # Search the corresponding competency
        competency = (
            SocleCompetency.select()
            .where(
                SocleCompetency.full_rank == default_competency.full_rank,
                SocleCompetency.cycle == default_competency.cycle,
                SocleCompetency.group_id == group_id,
            )
            .execute()[0]
        )
        # Search for the template
        try:
            template = (
                SocleCompetencyTemplate.select()
                .where(
                    SocleCompetencyTemplate.competency == competency,
                    SocleCompetencyTemplate.group_id == group_id,
                    SocleCompetencyTemplate.text == default_template.text,
                )
                .execute()[0]
            )
            found += 1
        except IndexError:
            # template not found
            SocleCompetencyTemplate.create(
                active=True,
                group_id=group_id,
                competency=competency,
                text=default_template.text,
            )
            not_found += 1

    print(f"found : {found}, not_found: {not_found}")


def main(group_id):
    copy_default_templates(group_id)


if __name__ == "__main__":
    group_id = int(sys.argv[1])
    main(group_id)