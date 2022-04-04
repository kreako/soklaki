from collections import defaultdict
from random import randint
from zipfile import ZipFile
from datetime import date
import json
import re
from pydantic import BaseModel, Field
from fastapi.responses import FileResponse
from fastapi.exceptions import HTTPException
from typing import Optional
from path import Path
import jwt

from pdf import PDF, RIGHT_STOP, MARKER_WIDTH, make_safe_filename
from gql_client import GqlClientException


class HasuraHeaders(BaseModel):
    x_hasura_user_id: int = Field(alias="x-hasura-user-id")
    x_hasura_user_group: int = Field(alias="x-hasura-user-group")


class SummaryReportData(BaseModel):
    student_id: int
    period_id: int


class SummaryReportInput(BaseModel):
    input: SummaryReportData
    session_variables: HasuraHeaders


class SummaryReportOutput(BaseModel):
    report_id: int
    pdf_path: str
    json_path: str


async def report(gql_client, reports_dir, input: SummaryReportInput):
    # Gather data - will check permissions and raise HTTPException(500) if necessary
    data = await gql_report(
        gql_client,
        input.input.student_id,
        input.input.period_id,
        input.session_variables.x_hasura_user_id,
        input.session_variables.x_hasura_user_group,
    )

    # Now generation
    pdf = PDF()
    # Header
    pdf.add_page()
    with pdf.edit().font_bold().text_lg().text_black() as e:
        e.write("Rapport d'évaluation du socle commun", align="C")
        e.write(f"{data['period']['group']['name']}", align="C")
        e.write(
            f"{data['student']['firstname']} {data['student']['lastname']} - {data['student']['cycle']['cycle']}",
            align="C",
        )
        e.empty_line()

    # y_start_general_info = pdf.get_y()
    output_general_info(pdf, data)
    # y_end_general_info = pdf.get_y()

    # pdf.set_y(y_start_general_info)
    # output_legend(pdf)
    # pdf.set_y(y_end_general_info)

    output_evolution_boxes(pdf, data)
    pdf.vertical_margin(16)
    output_general_comment(pdf, data)

    # Output file
    prefix = f"{data['period']['group']['name']}_{data['period']['name']}_{data['student']['cycle']['cycle']}_{data['student']['firstname']}_{data['student']['lastname']}"
    prefix = make_safe_filename(prefix)
    pdf_fname = f"{prefix}.pdf"
    dirname = (
        Path(reports_dir) / f"{data['period']['group_id']}" / f"{input.input.period_id}"
    )
    dirname.makedirs_p()
    pdf_path = dirname / pdf_fname
    pdf.output(pdf_path)
    json_fname = f"{prefix}.json"
    json_path = dirname / json_fname
    with open(json_path, "w") as f:
        f.write(json.dumps(data, indent=2, default=str))

    # Make older report inactive
    await inactivate_old_report(
        gql_client, input.input.student_id, input.input.period_id
    )
    # Add the report to the database
    id = await insert_report(
        gql_client,
        input.input.student_id,
        data["student"]["cycle"]["cycle"],
        data["period"]["end"],
        json_path,
        pdf_path,
    )

    return SummaryReportOutput(
        report_id=id,
        pdf_path=pdf_path,
        json_path=json_path,
    )


def output_legend(pdf):
    with pdf.edit().fill_gray_200().text_sm() as e:
        y = pdf.get_y()
        e.rect(118, y, 85, e.line_height * 12)
        pdf.set_y(y + e.line_height / 2)

    with pdf.edit().text_sm().font_bold() as e:
        pdf.set_x(120)
        pdf.cell(w=0, h=e.line_height, txt="Légende", ln=1, align="L")

    with pdf.edit().text_sm() as e:
        # Color codes
        y = pdf.get_y()
        e.fill_red_600()
        e.rect(188, y, 10, e.line_height)
        pdf.cell(w=176, h=e.line_height, txt="Maîtrise insuffisante", ln=1, align="R")

        y = pdf.get_y()
        e.fill_yellow_600()
        e.rect(188, y, 10, e.line_height)
        pdf.cell(w=176, h=e.line_height, txt="Maîtrise fragile", ln=1, align="R")

        y = pdf.get_y()
        e.fill_green_600()
        e.rect(188, y, 10, e.line_height)
        pdf.cell(w=176, h=e.line_height, txt="Maîtrise satisfaisante", ln=1, align="R")

        y = pdf.get_y()
        e.fill_pink_600()
        e.rect(188, y, 10, e.line_height)
        pdf.cell(w=176, h=e.line_height, txt="Très bonne maîtrise", ln=1, align="R")

        # spacer
        e.empty_line()
        e.empty_line()

        # Time diagram legend - fake diagram
        y = pdf.get_y()
        e.fill_gray_50()
        e.rect(150, y - 1, 50, 6)  # basis
        level_to_fill_color(12, e)
        e.rect(152, y + 4, 7, 1)
        level_to_fill_color(24, e)
        e.rect(162, y + 3, 7, 2)
        level_to_fill_color(43, e)
        e.rect(172, y + 2, 7, 3)
        level_to_fill_color(43, e)
        e.rect(182, y + 2, 7, 3)
        level_to_fill_color(76, e)
        e.rect(192, y, 7, 5)

        # Legend of time diagram
        pdf.set_y(y + 8)
        pdf.set_x(120)
        pdf.cell(
            w=0,
            h=e.line_height,
            txt="Évolution de l'évaluation dans le cycle",
            ln=1,
            align="R",
        )

    with pdf.edit().text_xs() as e:
        pdf.cell(
            w=0,
            h=e.line_height,
            txt="depuis le début du cycle à l'école",
            ln=1,
            align="R",
        )
        pdf.cell(
            w=0,
            h=e.line_height,
            txt="jusqu'à la date du rapport",
            ln=1,
            align="R",
        )


def output_general_info(pdf, data):
    with pdf.edit().style_label() as e:
        e.write("Date du rapport")
    with pdf.edit().style_normal() as e:
        e.write(f"{data['period']['end']}")
    with pdf.edit().style_label() as e:
        e.write("Nom")
    with pdf.edit().style_normal() as e:
        e.write(f"{data['student']['lastname']}")
    with pdf.edit().style_label() as e:
        e.write("Prénom")
    with pdf.edit().style_normal() as e:
        e.write(f"{data['student']['firstname']}")
    with pdf.edit().style_label() as e:
        e.write("Cycle")
    with pdf.edit().style_normal() as e:
        e.write(f"Cycle {data['student']['cycle']['cycle'][-1]}")
    with pdf.edit().style_label() as e:
        e.write("Date d'anniversaire")
    with pdf.edit().style_normal() as e:
        e.write(f"{data['student']['birthdate']}")
    with pdf.edit().style_label() as e:
        e.write("Date d'entrée à l'école")
    with pdf.edit().style_normal() as e:
        e.write(f"{data['student']['school_entry']}")
    if data["student"]["school_exit"]:
        with pdf.edit().style_label() as e:
            e.write("Date de sortie de l'école")
        with pdf.edit().style_normal() as e:
            e.write(f"{data['student']['school_exit']}")


def level_to_fill_color(level, writer):
    if level < 25:
        writer.fill_red_600()
    elif level < 50:
        writer.fill_yellow_600()
    elif level < 75:
        writer.fill_green_600()
    else:
        writer.fill_pink_600()


def level_to_draw_color(level, writer):
    if level < 25:
        writer.draw_red_600()
    elif level < 50:
        writer.draw_yellow_600()
    elif level < 75:
        writer.draw_green_600()
    else:
        writer.draw_pink_600()


def level_to_label(level):
    if level is None:
        return ""
    if level < 25:
        return "Maîtrise insuffisante"
    elif level < 50:
        return "Maîtrise fragile"
    elif level < 75:
        return "Maîtrise satisfaisante"
    else:
        return "Très bonne maîtrise"


# Basis
EVOL_BOX_LEVELS_WIDTH = 30
EVOL_BOX_LEVEL_HEIGHT = 6
EVOL_BOX_HEIGHT = EVOL_BOX_LEVEL_HEIGHT * 4
EVOL_BOX_WIDTH = 190 - EVOL_BOX_LEVELS_WIDTH


def _evolution_box_background(pdf):
    x = 10
    y = pdf.get_y()
    with pdf.edit().text_xs() as e:
        e.fill_gray_100()
        e.rect(x, y + e.line_height + 2, EVOL_BOX_WIDTH, EVOL_BOX_HEIGHT)


def _evolution_box_levels(pdf):
    initial_y = pdf.get_y()

    # Horizontal line for level split
    with pdf.edit().draw_gray_300().text_xs() as e:
        y = pdf.get_y() + 4
        pdf.dashed_line(10, y, 10 + EVOL_BOX_WIDTH, y)
        y = pdf.get_y() + 4 + EVOL_BOX_LEVEL_HEIGHT
        pdf.dashed_line(10, y, 10 + EVOL_BOX_WIDTH, y)
        y = pdf.get_y() + 4 + 2 * EVOL_BOX_LEVEL_HEIGHT
        pdf.dashed_line(10, y, 10 + EVOL_BOX_WIDTH, y)
        y = pdf.get_y() + 4 + 3 * EVOL_BOX_LEVEL_HEIGHT
        pdf.dashed_line(10, y, 10 + EVOL_BOX_WIDTH, y)
        y = pdf.get_y() + 4 + 4 * EVOL_BOX_LEVEL_HEIGHT
        pdf.dashed_line(10, y, 10 + EVOL_BOX_WIDTH, y)

    def _label(text):
        e.vertical_margin((EVOL_BOX_LEVEL_HEIGHT / 2) - 1)
        pdf.set_x(10 + EVOL_BOX_WIDTH)
        pdf.cell(
            w=EVOL_BOX_LEVELS_WIDTH,
            h=e.line_height,
            txt=text,
            align="L",
            ln=0,
        )
        e.vertical_margin((EVOL_BOX_LEVEL_HEIGHT / 2) + 1)

    with pdf.edit().text_xs() as e:
        e.vertical_margin(4)
        _label("Très bonne maîtrise")
        _label("Maîtrise satisfaisante")
        _label("Maîtrise fragile")
        _label("Maîtrise insuffisante")

    # Reset initial vertical position
    pdf.set_y(initial_y)


def _evolution_box_date(pdf, cycle_start):
    width_6_months = EVOL_BOX_WIDTH / 6

    def _label(x, text):
        pdf.set_x(x)
        pdf.cell(
            w=20,
            h=e.line_height,
            txt=text,
            align="L",
            ln=0,
        )

    # Vertical line for date split
    y = pdf.get_y()
    with pdf.edit().draw_gray_300().text_xs() as e:
        for i in range(1, 6):
            x = 10 + i * width_6_months  # 10 is left margin
            pdf.dashed_line(
                x,
                y + e.line_height + 2,
                x,
                y + EVOL_BOX_HEIGHT + 4,
            )

    # top cycle date
    year = cycle_start.year
    with pdf.edit().font_normal().text_xs().text_gray_700() as e:
        center_correct = 2  # to center date label
        _label(10, f"{year}-09-01")  # 10 because of the left margin
        _label(width_6_months + center_correct, f"{year + 1}-03-01")
        _label(2 * width_6_months + center_correct, f"{year + 1}-09-01")
        _label(3 * width_6_months + center_correct, f"{year + 2}-03-01")
        _label(4 * width_6_months + center_correct, f"{year + 2}-09-01")
        _label(5 * width_6_months + center_correct, f"{year + 3}-03-01")
        _label(EVOL_BOX_WIDTH - 4, f"{year + 3}-09-01")


def date_to_x(cycle_start, date):
    dtX = (date - cycle_start).days
    x = 10 + (EVOL_BOX_WIDTH * dtX) / (365 * 3)
    return x


def level_to_y(pdf, level):
    h = EVOL_BOX_HEIGHT - level * EVOL_BOX_HEIGHT / 100
    y = pdf.get_y() + 4 + h
    return y


def _evolution_box_level_point(pdf, cycle_start, date, level):
    x = date_to_x(cycle_start, date)
    y = level_to_y(pdf, level)
    with pdf.edit() as e:
        e.fill_gray_900()
        e.rect(x - 1, y - 1, 2, 2)


def _evolution_box_level_lines(pdf, cycle_start, levels):
    previous = None
    for level in levels:
        lvl = level["level"]
        if lvl is not None:
            if previous is not None:
                x1 = date_to_x(cycle_start, level["date"])
                y1 = level_to_y(pdf, lvl)
                x2 = date_to_x(cycle_start, previous["date"])
                y2 = level_to_y(pdf, previous["level"])
                with pdf.edit() as e:
                    e.draw_gray_900()
                    e.line(x1, y1, x2, y2)
            _evolution_box_level_point(pdf, cycle_start, level["date"], lvl)
            previous = level


def output_evolution_box(pdf, cycle_start, cycle_end, subject, levels):
    # First let's estimate the height needed for this box
    with pdf.edit().style_normal() as e:
        lines = len(
            pdf.multi_cell(
                w=0,  # -10 -10 for page left and right margins
                h=e.line_height,
                txt=subject["comment"],
                split_only=True,
            )
        )
        comment_height = lines * e.line_height
    with pdf.edit().text_xs() as e:
        graph_height = e.line_height + 2 + EVOL_BOX_HEIGHT
    with pdf.edit().style_label() as e:
        labels_height = 2 + e.line_height + 1 + e.line_height
    box_height = comment_height + graph_height + labels_height
    y = pdf.get_y()
    if y + box_height >= 297 - 15 - 10:  # 10 margin, 15 footer
        pdf.add_page()

    with pdf.edit().style_normal().font_bold() as e:
        e.write(subject["subject"])

    with pdf.edit().style_label() as e:
        e.vertical_margin(2)
        e.write("Évolution")
        e.vertical_margin(1)

    _evolution_box_background(pdf)
    _evolution_box_date(pdf, cycle_start)
    _evolution_box_levels(pdf)

    _evolution_box_level_lines(pdf, cycle_start, levels)

    pdf.vertical_margin(EVOL_BOX_HEIGHT + 4 + 2)

    with pdf.edit().style_label() as e:
        e.write("Commentaire")

    with pdf.edit().style_normal() as e:
        e.write(subject["comment"])


def output_evolution_boxes(pdf, data):
    pdf.vertical_margin(15)
    cycle_start = data["student"]["cycle"]["start"]
    cycle_end = data["student"]["cycle"]["end"]
    for subject in data["subjects"]:
        output_evolution_box(pdf, cycle_start, cycle_end, subject, subject["levels"])
        pdf.vertical_margin(8)


def output_general_comment(pdf, data):
    comment = data["comment"]
    # First let's estimate the height needed for the comment and its header
    with pdf.edit().style_normal() as e:
        lines = len(
            pdf.multi_cell(
                w=190,  # -10 -10 for page left and right margins
                h=e.line_height,
                txt=comment,
                split_only=True,
            )
        )
        comment_height = lines * e.line_height
        header_height = e.line_height
        vertical_margin = 2

    y = pdf.get_y()
    if (
        y + comment_height + header_height + vertical_margin >= 297 - 15 - 10
    ):  # 10 margin, 15 footer
        pdf.add_page()

    with pdf.edit().style_normal().font_bold() as e:
        e.write("Commentaire général")

    pdf.vertical_margin(vertical_margin)

    with pdf.edit().style_normal() as e:
        e.write(comment)


async def gql_period(gql_client, period_id, student_id):
    r = await gql_client.run_query(
        """
query Period($student_id: bigint!, $period_id: Int!) {
  period: eval_period_by_pk(id: $period_id) {
    active
    end
    group_id
    group {
        name
    }
    id
    name
    start
    students(where: {student_id: {_eq: $student_id}}) {
      cycle
      student {
        id
        active
        birthdate
        firstname
        group_id
        lastname
        school_entry
        school_exit
      }
    }
  }
}
""",
        {"student_id": student_id, "period_id": period_id},
    )
    period = r["data"]["period"]
    relation = period["students"][0]
    cycle = relation["cycle"]
    student = relation["student"]
    student["cycle"] = {
        "cycle": cycle,
        "start": date(2019, 9, 1),
        "end": date(2022, 8, 31),
    }
    student["firstname"] = "Prénom"
    student["lastname"] = "Nom"
    student["birthdate"] = "2010-05-22"
    student["school_entry"] = "2019-10-03"

    return (period, student)


SUBJECTS = [
    "Français",
    "Langues étrangères",
    "Arts et culture",
    "Maths",
    "Numérique",
    "Citoyenneté ",
    "Sciences du vivant ",
    "Géographie",
    "Histoire",
    "Corps et Sport",
    "Connaissance de soi et relations aux autres",
    "Ingénierie",
    "Méthode et outils pour apprendre",
]


def fake_levels():
    levels = [randint(1, 27)]
    for _ in range(5):
        levels.append(levels[-1] + randint(-5, 34))
        if levels[-1] > 100:
            # Clamp it to 100
            levels[-1] = 100
        if levels[-1] < 1:
            # Clamp it to 1
            levels[-1] = 1
    # return [1] * 6
    return levels


LOREM_IPSUM = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."


def fake_comment():
    size = randint(0, len(LOREM_IPSUM.split()))
    return " ".join(LOREM_IPSUM.split()[0:size])


def fake_subject_comment(subject):
    return f"Commentaire/Évaluation sur '{subject}'. " + fake_comment()


def fake_general_comment():
    return f"Commentaire/Évaluation générale. " + fake_comment()


async def gql_report(
    gql_client, student_id, period_id, x_hasura_user_id, x_hasura_user_group
):
    # Check permissions and gather first info
    group_id = (await gql_client.user_by_id(x_hasura_user_id))["group_id"]
    if group_id != x_hasura_user_group:
        raise HTTPException(500)
    period, student = await gql_period(gql_client, period_id, student_id)
    if group_id != period["group_id"]:
        raise HTTPException(500)
    if group_id != student["group_id"]:
        raise HTTPException(500)
    if not period["active"]:
        raise HTTPException(500)
    if not student["active"]:
        raise HTTPException(500)

    data = {}

    data["subjects"] = []
    for subject in SUBJECTS:
        levels = fake_levels()
        data["subjects"].append(
            {
                "subject": subject,
                "comment": fake_subject_comment(subject),
                "levels": [
                    {"date": date(2019, 9, 1), "level": None},
                    {"date": date(2020, 1, 31), "level": levels[0]},
                    {"date": date(2020, 6, 30), "level": levels[1]},
                    {"date": date(2021, 1, 31), "level": levels[2]},
                    {"date": date(2021, 6, 30), "level": levels[3]},
                    {"date": date(2022, 1, 31), "level": levels[4]},
                ],
            }
        )
    data["period"] = period
    data["student"] = student
    data["comment"] = fake_general_comment()

    return data


async def inactivate_old_report(gql_client, student_id, period_id):
    r = await gql_client.run_query(
        """
mutation Inactivate($student_id: Int!, $period_id: Int!) {
    update_summary_report(
        where: {
            student_id: {_eq: $student_id},
            period: {eval_period_id: {_eq: $period_id}}
        }
        _set: {active: false}
    ) {
        affected_rows
    }
}""",
        {"student_id": student_id, "period_id": period_id},
    )
    return r["data"]["update_summary_report"]["affected_rows"]


async def insert_report(gql_client, student_id, cycle, date, json_path, pdf_path):
    r = await gql_client.run_query(
        """
mutation InsertReport($student_id: Int!, $cycle: cycle!, $date: date!, $json_path: String!, $pdf_path: String!) {
    insert_summary_report_one(
        object: {
            active: true,
            cycle: $cycle,
            date: $date,
            json_path: $json_path,
            pdf_path: $pdf_path,
            student_id: $student_id
        }
    ) {
        id
    }
}
""",
        {
            "student_id": student_id,
            "cycle": cycle,
            "date": date,
            "json_path": json_path,
            "pdf_path": pdf_path,
        },
    )
    return r["data"]["insert_summary_report_one"]["id"]


async def dl_report(
    reports_dir,
    group_id: int,
    period_id: int,
    filename: str,
    token: str,
    hasura_graphql_jwt_secret,
):
    t = jwt.decode(token, hasura_graphql_jwt_secret, algorithms=["HS256"])
    token_group_id = int(t["https://hasura.io/jwt/claims"]["x-hasura-user-group"])
    if group_id != token_group_id:
        return None
    file_path = Path(reports_dir) / f"{group_id}" / f"{period_id}" / filename
    return FileResponse(file_path, media_type="application/pdf")


async def dl_zip_reports(
    gql_client,
    reports_dir,
    group_id: int,
    period_id: int,
    token: str,
    hasura_graphql_jwt_secret,
):
    t = jwt.decode(token, hasura_graphql_jwt_secret, algorithms=["HS256"])
    token_group_id = int(t["https://hasura.io/jwt/claims"]["x-hasura-user-group"])
    if group_id != token_group_id:
        return None
    dir_path = Path(reports_dir) / f"{group_id}" / f"{period_id}"
    group = await gql_client.group_by_id(group_id)
    period = await gql_client.period_by_id(period_id)
    zip_fname = make_safe_filename(f"{group['name']}_{period['name']}.zip")
    virtual_path = Path(make_safe_filename(f"{group['name']}_{period['name']}"))
    zip_path = dir_path / zip_fname
    with ZipFile(zip_path, "w") as myzip:
        for pdf in dir_path.listdir("*.pdf"):
            myzip.write(pdf, arcname=virtual_path / pdf.basename())
    return FileResponse(zip_path, media_type="application/zip", filename=zip_fname)
