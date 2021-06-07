from collections import defaultdict
from zipfile import ZipFile
from datetime import date
import re
from pydantic import BaseModel, Field
from fastapi.responses import FileResponse
from typing import Optional
from fpdf import FPDF
from path import Path
import jwt

from gql_client import GqlClientException

CURRENT_DIR = Path(__file__).abspath().dirname()


class HasuraHeaders(BaseModel):
    x_hasura_user_id: int = Field(alias="x-hasura-user-id")
    x_hasura_user_group: int = Field(alias="x-hasura-user-group")


class ReportData(BaseModel):
    student_id: int
    period_id: int


class ReportInput(BaseModel):
    input: ReportData
    session_variables: HasuraHeaders


class ReportOutput(BaseModel):
    report_id: int
    pdf_path: str
    json_path: str


async def report(gql_client, reports_dir, input: ReportInput):
    # Check permissions
    user_id = input.session_variables.x_hasura_user_id
    group_id = (await gql_client.user_by_id(user_id))["group_id"]
    period, student = await gql_period(
        gql_client, input.input.period_id, input.input.student_id
    )
    if group_id != period["group_id"]:
        return None
    if group_id != student["group_id"]:
        return None
    if not period["active"]:
        return None
    if not student["active"]:
        return None

    # Gather data
    data = await gql_report(
        gql_client, period["end"], student["id"], student["cycle"], group_id
    )

    # Now generation
    pdf = PDF()
    # Header
    pdf.add_page()
    with pdf.edit().font_bold().text_lg().text_black() as e:
        e.write("Rapport d'évaluation du socle commun")
        e.write(
            f"{student['firstname']} {student['lastname']} - {student['cycle']}",
            align="R",
        )
        e.write(f"{period['group']['name']}", align="R")
        e.empty_line()

    with pdf.edit().style_label() as e:
        e.write("Date du rapport")
    with pdf.edit().style_normal() as e:
        e.write(f"{period['end']}")
    with pdf.edit().style_label() as e:
        e.write("Nom")
    with pdf.edit().style_normal() as e:
        e.write(f"{student['lastname']}")
    with pdf.edit().style_label() as e:
        e.write("Prénom")
    with pdf.edit().style_normal() as e:
        e.write(f"{student['firstname']}")
    with pdf.edit().style_label() as e:
        e.write("Cycle")
    with pdf.edit().style_normal() as e:
        e.write(f"Cycle {student['cycle'][-1]}")
    with pdf.edit().style_label() as e:
        e.write("Date d'anniversaire")
    with pdf.edit().style_normal() as e:
        e.write(f"{student['birthdate']}")
    with pdf.edit().style_label() as e:
        e.write("Date d'entrée à l'école")
    with pdf.edit().style_normal() as e:
        e.write(f"{student['school_entry']}")
    if student["school_exit"]:
        with pdf.edit().style_label() as e:
            e.write("Date de sortie de l'école")
        with pdf.edit().style_normal() as e:
            e.write(f"{student['school_exit']}")

    # Graphics data
    # Compute competencies -> domain
    domains = {}
    # domain -> nb competencies
    total = defaultdict(int)
    for l1 in data["socle"]:
        for l2 in l1["children"]:
            for c in l2["competencies"]:
                domains[c["id"]] = l1["id"]
                total[l1["id"]] += 1
        for c in l1["competencies"]:
            domains[c["id"]] = l1["id"]
            total[l1["id"]] += 1
    # Now sort evaluations count by domain and status
    evaluations = {
        l1["id"]: {
            "NotAcquired": 0,
            "InProgress": 0,
            "Acquired": 0,
            "TipTop": 0,
        }
        for l1 in data["socle"]
    }
    for evaluation in data["evaluations"]:
        domain = domains[evaluation["competency_id"]]
        status = evaluation["status"]
        evaluations[domain][status] += 1

    # Now to draw
    pdf.set_y(pdf.get_y() + 20)
    # Per domains
    for l1 in data["socle"]:
        domain = data["container_by_id"][l1["id"]]
        with pdf.edit().style_label() as e:
            e.write(f"{domain['full_rank']} {domain['text']}")
        output_bar_progression(
            pdf,
            evaluations[l1["id"]]["NotAcquired"],
            evaluations[l1["id"]]["InProgress"],
            evaluations[l1["id"]]["Acquired"],
            evaluations[l1["id"]]["TipTop"],
            total[l1["id"]],
        )
        pdf.set_y(pdf.get_y() + 1)

    # Total
    with pdf.edit().style_label() as e:
        e.write("Total")
    total = len(data["competencies"])
    output_bar_progression(
        pdf,
        data["evaluations_by_status"]["NotAcquired"],
        data["evaluations_by_status"]["InProgress"],
        data["evaluations_by_status"]["Acquired"],
        data["evaluations_by_status"]["TipTop"],
        total,
    )

    # Legend
    pdf.set_y(pdf.get_y() + 20)
    with pdf.edit() as e:
        y = pdf.get_y()
        e.fill_red_600()
        e.rect(190, y + 1, 10, 4)
        pdf.cell(w=170, h=e.line_height, txt="Maîtrise insuffisante", ln=1, align="R")

        y = pdf.get_y()
        e.fill_yellow_600()
        e.rect(190, y + 1, 10, 4)
        pdf.cell(w=170, h=e.line_height, txt="Maîtrise fragile", ln=1, align="R")

        y = pdf.get_y()
        e.fill_green_600()
        e.rect(190, y + 1, 10, 4)
        pdf.cell(w=170, h=e.line_height, txt="Maîtrise satisfaisante", ln=1, align="R")

        y = pdf.get_y()
        e.fill_pink_600()
        e.rect(190, y + 1, 10, 4)
        pdf.cell(w=170, h=e.line_height, txt="Très bonne maîtrise", ln=1, align="R")

    # Main body
    for l1_raw in data["socle"]:
        l1_id = l1_raw["id"]
        l1 = data["container_by_id"][l1_id]
        pdf.add_page()

        with pdf.edit().font_bold().text_sm().text_gray_700() as e:
            e.write(f"{l1['full_rank']} {l1['text'].upper()}")

        for l2_raw in l1_raw["children"]:
            l2_id = l2_raw["id"]
            l2 = data["container_by_id"][l2_id]

            with pdf.edit().text_sm().text_gray_700() as e:
                e.write(f"{l2['full_rank']} {l2['text']}", indent=1)

            for competency_raw in l2_raw["competencies"]:
                competency_id = competency_raw["id"]
                output_competency(pdf, competency_id, data, 2)

        for competency_raw in l1_raw["competencies"]:
            competency_id = competency_raw["id"]
            output_competency(pdf, competency_id, data, 1)

    # Eval comments
    pdf.add_page()
    with pdf.edit().font_bold().text_lg().text_black() as e:
        e.write("Commentaire")
        e.empty_line()
    if data["comments"]:
        with pdf.edit().style_normal().font_mono() as e:
            e.write(f"{data['comments'][0]['text']}")

    # Observations
    pdf.add_page()
    with pdf.edit().font_bold().text_lg().text_black() as e:
        e.write("Annexe - Les observations")
        e.empty_line()
    for observation in data["observations"]:
        with pdf.edit().style_normal() as e:
            e.write(f"{observation['date']}")
        with pdf.edit().style_label() as e:
            for c in observation["competencies"]:
                competency_id = c["competency_id"]
                competency = data["competency_by_id"][competency_id]
                e.write(f"{competency['full_rank']} {competency['text']}", indent=1)
        with pdf.edit().style_normal() as e:
            e.write(f"{observation['text']}")
            e.empty_line()

    # Output
    pdf_fname = f"{period['group']['name']}_{period['name']}_{student['cycle']}_{student['firstname']}_{student['lastname']}.pdf"
    pdf_fname = make_safe_filename(pdf_fname)
    dirname = Path(reports_dir) / f"{group_id}" / f"{input.input.period_id}"
    dirname.makedirs_p()
    pdf_path = dirname / pdf_fname
    pdf.output(pdf_path)
    json_path = "invalid"

    # Make older report inactive
    await inactivate_old_report(
        gql_client, input.input.student_id, input.input.period_id
    )
    # Add the report to the database
    today = date.today().isoformat()
    id = await insert_report(
        gql_client,
        input.input.student_id,
        student["cycle"],
        today,
        json_path,
        pdf_path,
    )

    return ReportOutput(
        report_id=id,
        pdf_path=pdf_path,
        json_path=json_path,
    )


def output_bar_progression(pdf, not_acquired, in_progress, acquired, tiptop, total):
    y = pdf.get_y()
    x = 10
    with pdf.edit() as e:
        e.fill_gray_700()
        e.rect(10, y, 190, 8)

        l = 190 * not_acquired / total
        e.fill_red_600()
        e.rect(x, y + 1, l, 6)
        x += l

        l = 190 * in_progress / total
        e.fill_yellow_600()
        e.rect(x, y + 1, l, 6)
        x += l

        l = 190 * acquired / total
        e.fill_green_600()
        e.rect(x, y + 1, l, 6)
        x += l

        l = 190 * tiptop / total
        e.fill_pink_600()
        e.rect(x, y + 1, l, 6)
    pdf.set_y(y + 10)


def output_competency(pdf, competency_id, data, indent):
    competency = data["competency_by_id"][competency_id]
    with pdf.edit().text_gray_700() as e:
        e.write(f"{competency['full_rank']} {competency['text']}", indent=indent)
    observations = data["observations_by_competency_id"][competency_id]
    len_observations = len(observations)
    evaluations = data["evaluations_by_competency_id"][competency_id]
    len_evaluations = len(evaluations)
    if evaluations:
        evaluation = evaluations[0]
    else:
        evaluation = None
    with pdf.edit().style_normal().font_mono() as e:
        e.empty_line()

        if len_observations > 1:
            observations_count = f"{len_observations} observations"
        elif len_observations == 1:
            observations_count = f"1 observation"
        else:
            observations_count = ""

        if len_evaluations > 1:
            evaluations_count = f"{len_evaluations} évaluations"
        elif len_evaluations == 1:
            evaluations_count = f"1 évaluation"
        else:
            evaluations_count = ""

        if evaluation:
            status = evaluation["status"]
            if status == "NotAcquired":
                e.fill_red_600()
                status_line = "Maîtrise insuffisante"
            elif status == "InProgress":
                e.fill_yellow_600()
                status_line = "Maîtrise fragile"
            elif status == "Acquired":
                e.fill_green_600()
                status_line = "Maîtrise satisfaisante"
            elif status == "TipTop":
                e.fill_pink_600()
                status_line = "Très bonne maîtrise"
            else:
                e.fill_white()
                status_line = ""
            e.write_with_marker(
                f"{status_line:<30} {evaluations_count:<30} {observations_count:<30}"
            )
            if evaluation["comment"]:
                e.write(f"{evaluation['comment']}")
            e.empty_line()
            e.empty_line()


class PDF(FPDF):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_font("dejavu", fname=CURRENT_DIR / "DejaVuSerif.ttf", uni=True)
        self.add_font(
            "dejavu-bold", fname=CURRENT_DIR / "DejaVuSerif-Bold.ttf", uni=True
        )

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # helvetica italic 8
        self.set_font("helvetica", "I", 8)
        # Page number
        self.cell(0, 10, "Page " + str(self.page_no()) + "/{nb}", 0, 0, "C")

    def edit(self):
        return PdfWriter(self)


class PdfWriter(object):
    def __init__(self, pdf):
        self.pdf = pdf
        self.line_height = 10
        self.font_normal()
        self.text_base()
        self.text_black()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def write(self, txt, indent=0, align="L"):
        # 10 is the default left margin
        self.pdf.set_x(10 + indent * 10)
        self.pdf.multi_cell(w=0, h=self.line_height, txt=txt, ln=1, align=align)

    def write_with_marker(self, txt):
        self.pdf.rect(
            self.pdf.get_x(),
            self.pdf.get_y() + self.line_height / 4,
            10,
            self.line_height / 2,
            "F",
        )
        self.pdf.set_x(self.pdf.get_x() + 20)
        self.pdf.multi_cell(w=0, h=self.line_height, txt=txt, ln=1)

    def empty_line(self):
        self.pdf.cell(w=0, h=self.line_height, txt="", ln=1)

    def rect(self, x, y, w, h):
        self.pdf.rect(x, y, w, h, "F")

    def style_label(self):
        return self.font_normal().text_sm().text_gray_700()

    def style_normal(self):
        return self.font_normal().text_base().text_black()

    def font_normal(self):
        self.pdf.set_font("dejavu")
        return self

    def font_bold(self):
        self.pdf.set_font("dejavu-bold")
        return self

    def font_mono(self):
        self.pdf.set_font("Courier")
        return self

    def text_lg(self):
        self.pdf.set_font_size(14)
        self.line_height = 10
        return self

    def text_xl(self):
        self.pdf.set_font_size(12)
        self.line_height = 8
        return self

    def text_base(self):
        self.pdf.set_font_size(10)
        self.line_height = 6
        return self

    def text_sm(self):
        self.pdf.set_font_size(8)
        self.line_height = 4
        return self

    def text_gray_700(self):
        self.pdf.set_text_color(0x37, 0x41, 0x51)
        return self

    def text_black(self):
        self.pdf.set_text_color(0x11, 0x18, 0x27)
        return self

    def text_red_600(self):
        self.pdf.set_text_color(0xDC, 0x26, 0x26)
        return self

    def text_yellow_600(self):
        self.pdf.set_text_color(0xD9, 0x77, 0x06)
        return self

    def text_green_600(self):
        self.pdf.set_text_color(0x05, 0x96, 0x69)
        return self

    def text_blue_600(self):
        self.pdf.set_text_color(0x25, 0x63, 0xEB)
        return self

    def text_pink_600(self):
        self.pdf.set_text_color(0xDB, 0x27, 0x77)
        return self

    def fill_white(self):
        self.pdf.set_fill_color(0xFF, 0xFF, 0xFF)
        return self

    def fill_gray_700(self):
        self.pdf.set_fill_color(0x37, 0x41, 0x51)
        return self

    def fill_black(self):
        self.pdf.set_fill_color(0x11, 0x18, 0x27)
        return self

    def fill_red_600(self):
        self.pdf.set_fill_color(0xDC, 0x26, 0x26)
        return self

    def fill_yellow_600(self):
        self.pdf.set_fill_color(0xD9, 0x77, 0x06)
        return self

    def fill_green_600(self):
        self.pdf.set_fill_color(0x05, 0x96, 0x69)
        return self

    def fill_blue_600(self):
        self.pdf.set_fill_color(0x25, 0x63, 0xEB)
        return self

    def fill_pink_600(self):
        self.pdf.set_fill_color(0xDB, 0x27, 0x77)
        return self


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
    student["cycle"] = cycle
    return (period, student)


async def gql_report(gql_client, period_end, student_id, cycle, group_id):
    r = await gql_client.run_query(
        """
query Report(
    $student_id: bigint!,
    $cycle: cycle!,
    $period_end: date!,
    $group_id: bigint!,
) {
    evaluations: eval_evaluation(
        where: {
            active: {_eq: true}
            student_id: {_eq: $student_id}
            competency: {cycle: {_eq: $cycle}}
            date: {_lte: $period_end}
        }
        order_by: {date: desc}
    ) {
        id
        created_at
        updated_at
        date
        competency_id
        status
        user_id
        comment
    }
    observations: eval_observation(
        where: {
            active: {_eq: true}
            competencies: {competency: {cycle: {_eq: $cycle}}}
            complete: {complete: {_eq: true}}
            date: {_lte: $period_end}
            students: {student_id: {_eq: $student_id}}
        },
        order_by: {date: desc}
    ) {
        id
        created_at
        updated_at
        date
        competencies {
            competency_id
        }
        text
        user_id
    }
    comments: eval_comment(
        where: {
            active: {_eq: true},
            student_id: {_eq: $student_id},
            date: {_lte: $period_end}
        }
        order_by: {updated_at: desc},
    ) {
        id
        date
        created_at
        updated_at
        text
        user_id
    }
    socle: socle_container(
        where: {
            cycle: { _eq: $cycle }
            container_id: { _is_null: true }
            active: { _eq: true }
            group_id: { _eq: $group_id }
        }
        order_by: { alpha_full_rank: asc }
    ) {
        id
        children(
            where: {
                active: { _eq: true }
                group_id: { _eq: $group_id }
            }
            order_by: { alpha_full_rank: asc }
        ) {
            id
            competencies(
                where: {
                    active: { _eq: true }
                    group_id: { _eq: $group_id }
                }
                order_by: { alpha_full_rank: asc }
            ) {
                id
            }
        }
        competencies(
            where: {
                active: { _eq: true }
                group_id: { _eq: $group_id }
            }
            order_by: { alpha_full_rank: asc }
        ) {
            id
        }
    }
    competencies: socle_competency(
        where: {
            active: { _eq: true }
            group_id: { _eq: $group_id }
        }
    ) {
        container_id
        cycle
        full_rank
        id
        rank
        text
    }
    containers: socle_container(
        where: {
            active: { _eq: true }
            group_id: { _eq: $group_id }
        }
    ) {
        id
        container_id
        full_rank
        cycle
        rank
        text
    }
}
        """,
        {
            "period_end": period_end,
            "student_id": student_id,
            "cycle": cycle,
            "group_id": group_id,
        },
    )
    data = r["data"]

    data["container_by_id"] = {
        container["id"]: container for container in data["containers"]
    }
    data["competency_by_id"] = {
        competency["id"]: competency for competency in data["competencies"]
    }

    if data["comments"]:
        data["comment"] = data["comments"][0]
    else:
        data["comment"] = None

    data["observations_by_competency_id"] = defaultdict(list)
    for observation in data["observations"]:
        for competency in observation["competencies"]:
            data["observations_by_competency_id"][competency["competency_id"]].append(
                observation
            )

    data["evaluations_by_competency_id"] = defaultdict(list)
    for evaluation in data["evaluations"]:
        data["evaluations_by_competency_id"][evaluation["competency_id"]].append(
            evaluation
        )

    data["evaluations_by_status"] = {
        "NotAcquired": 0,
        "InProgress": 0,
        "Acquired": 0,
        "TipTop": 0,
    }
    for evaluation in data["evaluations"]:
        data["evaluations_by_status"][evaluation["status"]] += 1
    return data


def make_safe_filename(s):
    def safe_char(c):
        if c.isalnum() or c == ".":
            return c
        else:
            return "_"

    fname = "".join(safe_char(c) for c in s).rstrip("_")
    fname = re.sub("_{2,}", "_", fname)
    return fname


async def inactivate_old_report(gql_client, student_id, period_id):
    r = await gql_client.run_query(
        """
mutation Inactivate($student_id: Int!, $period_id: Int!) {
    update_report(
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
    return r["data"]["update_report"]["affected_rows"]


async def insert_report(gql_client, student_id, cycle, date, json_path, pdf_path):
    r = await gql_client.run_query(
        """
mutation InsertReport($student_id: Int!, $cycle: cycle!, $date: date!, $json_path: String!, $pdf_path: String!) {
    insert_report_one(
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
    return r["data"]["insert_report_one"]["id"]


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