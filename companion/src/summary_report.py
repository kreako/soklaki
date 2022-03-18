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

    output_general_info(pdf, data)

    output_summary_table(pdf, data)

    # Now subjects with comments
    pdf.add_page()
    output_subjects_comments(pdf, data)

    # Output
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
        e.rect(153, y, 47, e.line_height * 5)
        pdf.set_y(y + e.line_height / 2)

    with pdf.edit().text_sm() as e:
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


def output_summary_table(pdf, data):
    pdf.set_y(pdf.get_y() + 5)
    with pdf.edit().font_normal().text_xs().text_gray_700() as e:
        pdf.set_x(110)
        pdf.cell(
            w=20,
            h=e.line_height,
            txt=str(data["student"]["cycle"]["start"]),
            align="L",
            ln=0,
        )
        pdf.set_x(180)
        pdf.cell(
            w=20,
            h=e.line_height,
            txt=str(data["student"]["cycle"]["end"]),
            align="R",
            ln=1,
        )
    pdf.set_y(pdf.get_y() + 1)
    with pdf.edit().style_normal() as e:
        for subject in data["subjects"]:
            pdf.cell(
                w=90,
                h=e.line_height,
                txt=subject["subject"],
                align="L",
                ln=0,
            )
            x = pdf.get_x() + 10
            y = pdf.get_y()
            # Basis
            height = 10
            width = 90
            years_3 = 365 * 3
            e.fill_gray_100()
            e.rect(x, y - 1, width, height + 2)
            pdf.set_y(pdf.get_y() + 13)
            # Now the line with levels
            start_cycle = data["student"]["cycle"]["start"]
            # First connecting line
            previous = None
            e.draw_gray_500()
            for level in subject["levels"]:
                if level["level"] is None:
                    continue
                lx = (level["date"] - start_cycle).days * width / years_3
                ly = height - ((level["level"] * height) / 100)
                if previous:
                    e.line(previous[0], previous[1], x + lx, y + ly)
                previous = (x + lx, y + ly)
            # Now evaluation points
            e.fill_gray_500()
            for level in subject["levels"]:
                if level["level"] is None:
                    continue
                lx = (level["date"] - start_cycle).days * width / years_3
                ly = height - ((level["level"] * height) / 100)
                # level_to_fill_color(level["level"], e)
                e.rect(x + lx - 0.25, y + ly - 0.25, 0.5, 0.5)


def output_subjects_comments(pdf, data):
    for subject in data["subjects"]:
        with pdf.edit().font_bold().text_base().text_black() as e:
            pdf.cell(
                w=90,
                h=e.line_height,
                txt=subject["subject"],
                align="L",
                ln=0,
            )
        with pdf.edit().style_label() as e:
            pdf.cell(
                w=90,
                h=e.line_height,
                txt=level_to_label(subject["levels"][-1]["level"]),
                align="L",
                ln=1,
            )
        with pdf.edit().style_normal() as e:
            e.empty_line()
            pdf.set_x(20)
            pdf.multi_cell(
                w=180,  # -10 for page right margin
                h=e.line_height,
                txt=subject["comment"],
                ln=1,
                align="L",
            )
            e.empty_line()


def output_competency_legend(pdf):
    ANGLE = 60
    y = pdf.get_y()
    pdf.set_y(y)
    pdf.set_x(RIGHT_STOP + 0 * MARKER_WIDTH + 2)
    with pdf.rotation(angle=ANGLE):
        with pdf.edit().text_xs() as e:
            pdf.cell(
                w=0,
                h=e.line_height,
                txt="Insuffisante",
                align="L",
                ln=1,
            )
    pdf.set_y(y)
    pdf.set_x(RIGHT_STOP + 1 * MARKER_WIDTH + 2)
    with pdf.rotation(angle=ANGLE):
        with pdf.edit().text_xs() as e:
            pdf.cell(
                w=0,
                h=e.line_height,
                txt="Fragile",
                align="L",
                ln=1,
            )
    pdf.set_y(y)
    pdf.set_x(RIGHT_STOP + 2 * MARKER_WIDTH + 2)
    with pdf.rotation(angle=ANGLE):
        with pdf.edit().text_xs() as e:
            pdf.cell(
                w=0,
                h=e.line_height,
                txt="Satisfaisante",
                align="L",
                ln=1,
            )
    pdf.set_y(y)
    pdf.set_x(RIGHT_STOP + 3 * MARKER_WIDTH + 2)
    with pdf.rotation(angle=ANGLE):
        with pdf.edit().text_xs() as e:
            pdf.cell(
                w=0,
                h=e.line_height,
                txt="Bonne",
                align="L",
                ln=1,
            )
    # pdf.set_y(pdf.get_y() + 5)
    # pdf.set_x(10)


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
        "end": date(2022, 9, 1),
    }
    student["firstname"] = "Prénom"
    student["lastname"] = "Nom"
    student["birthdate"] = "2010-05-22"
    student["school_entry"] = "2019-10-03"

    return (period, student)


SUBJECTS = [
    "Français",
    "Langues étrangères",
    "Arts et culture" "Maths",
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
                "comment": f"Commentaire/Évaluation sur '{subject}'",
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
