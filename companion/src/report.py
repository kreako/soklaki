from collections import defaultdict
from zipfile import ZipFile
from datetime import date
import json
import re
from pydantic import BaseModel, Field
from fastapi.responses import FileResponse
from fastapi.exceptions import HTTPException
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
            f"{data['student']['firstname']} {data['student']['lastname']} - {data['student']['cycle']}",
            align="C",
        )
        e.empty_line()

    y_start_of_general_info = pdf.get_y()

    output_general_info(pdf, data)

    # Graphics data
    pdf.set_y(pdf.get_y() + 30)
    # Per domains
    for l1 in data["socle"]:
        domain = data["container_by_id"][l1["id"]]
        with pdf.edit().style_label() as e:
            e.write(f"{domain['full_rank']} {domain['text']}")
        output_bar_progression(
            pdf,
            data["evaluations_count_by_domain_status"][l1["id"]]["NotAcquired"],
            data["evaluations_count_by_domain_status"][l1["id"]]["InProgress"],
            data["evaluations_count_by_domain_status"][l1["id"]]["Acquired"],
            data["evaluations_count_by_domain_status"][l1["id"]]["TipTop"],
            data["evaluations_count_by_domain"][l1["id"]],
        )
        pdf.set_y(pdf.get_y() + 1)

    # Total
    pdf.set_y(pdf.get_y() + 10)
    with pdf.edit().style_label() as e:
        e.write("Total")
    output_bar_progression(
        pdf,
        data["evaluations_count_by_status"]["not_acquired"],
        data["evaluations_count_by_status"]["in_progress"],
        data["evaluations_count_by_status"]["acquired"],
        data["evaluations_count_by_status"]["tip_top"],
        data["evaluations_count_by_status"]["total"],
    )

    # Legend
    pdf.set_y(y_start_of_general_info)
    output_legend(pdf)

    # Summary by competencies
    for l1_raw in data["socle"]:
        l1_id = l1_raw["id"]
        l1 = data["container_by_id"][l1_id]
        pdf.add_page()

        with pdf.edit().font_bold().text_gray_700() as e:
            e.write(f"{l1['full_rank']} {l1['text'].upper()}")

        for l2_idx, l2_raw in enumerate(l1_raw["children"]):
            l2_id = l2_raw["id"]
            l2 = data["container_by_id"][l2_id]

            with pdf.edit().text_gray_700() as e:
                if l2_idx > 0:
                    e.empty_line()
                e.write(f"{l2['full_rank']} {l2['text']}")
                e.empty_line()

            for competency_raw in l2_raw["competencies"]:
                competency_id = competency_raw["id"]
                output_competency_table(pdf, competency_id, data)

        for competency_raw in l1_raw["competencies"]:
            competency_id = competency_raw["id"]
            output_competency_table(pdf, competency_id, data)

    # Details of competencies
    pdf.add_page()
    for l1_idx, l1_raw in enumerate(data["socle"]):
        l1_id = l1_raw["id"]
        l1 = data["container_by_id"][l1_id]

        output_domain_needed = True

        def output_domain():
            nonlocal output_domain_needed
            if output_domain_needed:
                # pdf.add_page()
                with pdf.edit().font_bold().text_gray_700() as e:
                    if l1_idx > 0:
                        e.empty_line()
                        e.empty_line()
                    e.write(f"{l1['full_rank']} {l1['text'].upper()}")
                output_domain_needed = False

        for l2_idx, l2_raw in enumerate(l1_raw["children"]):
            l2_id = l2_raw["id"]
            l2 = data["container_by_id"][l2_id]

            output_sub_domain_needed = True

            def output_sub_domain():
                nonlocal output_sub_domain_needed
                if output_sub_domain_needed:
                    with pdf.edit().text_gray_700() as e:
                        if l2_idx > 0:
                            e.empty_line()
                        e.write(f"{l2['full_rank']} {l2['text']}")
                        e.empty_line()
                    output_sub_domain_needed = False

            for competency_raw in l2_raw["competencies"]:
                competency_id = competency_raw["id"]
                output_competency(
                    pdf, competency_id, data, output_domain, output_sub_domain
                )

        for competency_raw in l1_raw["competencies"]:
            competency_id = competency_raw["id"]
            output_competency(
                pdf, competency_id, data, output_domain, output_sub_domain
            )

    # Eval comments
    pdf.add_page()
    with pdf.edit().font_bold().text_lg().text_black() as e:
        e.write("Commentaire")
        e.empty_line()
    if data["comments"]:
        with pdf.edit().style_normal() as e:
            e.write(f"{data['comments'][0]['text']}")

    # Observations
    pdf.add_page()
    with pdf.edit().font_bold().text_lg().text_black() as e:
        e.write("Annexe - Les observations")
        e.empty_line()
    for observation in data["observations"]:
        with pdf.edit().style_normal() as e:
            e.write(f"Observation pour :")
        with pdf.edit().style_label() as e:
            for c in observation["competencies"]:
                competency_id = c["competency_id"]
                competency = data["competency_by_id"][competency_id]
                e.write(f"{competency['full_rank']} {competency['text']}", indent=1)
        with pdf.edit().style_normal() as e:
            e.write(f"{observation['text']}")
            e.empty_line()

    # Output
    prefix = f"{data['period']['group']['name']}_{data['period']['name']}_{data['student']['cycle']}_{data['student']['firstname']}_{data['student']['lastname']}"
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
        f.write(json.dumps(data, indent=2))

    # Make older report inactive
    await inactivate_old_report(
        gql_client, input.input.student_id, input.input.period_id
    )
    # Add the report to the database
    today = date.today().isoformat()
    id = await insert_report(
        gql_client,
        input.input.student_id,
        data["student"]["cycle"],
        today,
        json_path,
        pdf_path,
    )

    return ReportOutput(
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
        e.write(f"Cycle {data['student']['cycle'][-1]}")
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


def output_competency_table(pdf, competency_id, data):
    MARKER_WIDTH = 8
    RIGHT_STOP = 200 - 4 * MARKER_WIDTH  # 10 for page right margin
    competency = data["competency_by_id"][competency_id]
    evaluations = data["evaluations_by_competency_id"][competency_id]
    if evaluations:
        status = evaluations[0]["status"]
    else:
        status = "InProgress"
    with pdf.edit().text_gray_700().draw_gray_900() as e:
        txt = f"{competency['full_rank']} {competency['text']}"
        lines = len(
            pdf.multi_cell(
                w=RIGHT_STOP - 10,  # -10 for page left margin
                h=e.line_height,
                txt=txt,
                split_only=True,
            )
        )
        y = pdf.get_y()
        if y + lines * e.line_height >= 297 - 15 - 10:  # 10 margin, 15 footer
            pdf.add_page()
            y = pdf.get_y()

        pdf.multi_cell(
            w=RIGHT_STOP - 10,  # -10 for page left margin
            h=e.line_height,
            txt=txt,
            ln=1,
            align="L",
            border="BTRL",
        )

        if status == "NotAcquired":
            e.fill_red_600()
        else:
            e.fill_white()
        e.rect(RIGHT_STOP + 0 * MARKER_WIDTH, y, MARKER_WIDTH, e.line_height * lines)
        e.borders(RIGHT_STOP + 0 * MARKER_WIDTH, y, MARKER_WIDTH, e.line_height * lines)

        if status == "InProgress":
            e.fill_yellow_600()
        else:
            e.fill_white()
        e.rect(RIGHT_STOP + 1 * MARKER_WIDTH, y, MARKER_WIDTH, e.line_height * lines)
        e.borders(RIGHT_STOP + 1 * MARKER_WIDTH, y, MARKER_WIDTH, e.line_height * lines)

        if status == "Acquired":
            e.fill_green_600()
        else:
            e.fill_white()
        e.rect(RIGHT_STOP + 2 * MARKER_WIDTH, y, MARKER_WIDTH, e.line_height * lines)
        e.borders(RIGHT_STOP + 2 * MARKER_WIDTH, y, MARKER_WIDTH, e.line_height * lines)

        if status == "TipTop":
            e.fill_pink_600()
        else:
            e.fill_white()
        e.rect(RIGHT_STOP + 3 * MARKER_WIDTH, y, MARKER_WIDTH, e.line_height * lines)
        e.borders(RIGHT_STOP + 3 * MARKER_WIDTH, y, MARKER_WIDTH, e.line_height * lines)


def output_competency(pdf, competency_id, data, output_domain, output_sub_domain):
    competency = data["competency_by_id"][competency_id]
    write_needed = False
    observations = data["observations_by_competency_id"][competency_id]
    len_observations = len(observations)
    if len_observations > 0:
        write_needed = True
    evaluations = data["evaluations_by_competency_id"][competency_id]
    len_evaluations = len(evaluations)
    comment = None
    if len_evaluations > 0:
        evaluation = evaluations[0]
        if evaluation["comment"]:
            comment = evaluation["comment"]
            write_needed = True

    if not write_needed:
        return

    output_domain()
    output_sub_domain()

    output_competency_table(pdf, competency_id, data)

    if len_observations > 0:
        with pdf.edit().text_sm().text_gray_700().font_mono() as e:
            e.empty_line()
            if len_observations > 1:
                e.write(f"{len_observations} observations", indent=1)
            else:
                e.write("1 observation", indent=1)
            e.empty_line()

    if comment:
        with pdf.edit().style_normal() as e:
            if len_observations == 0:
                e.empty_line()
            e.write(comment, indent=1)
            e.empty_line()


class PDF(FPDF):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_font("dejavu", fname=CURRENT_DIR / "DejaVuSerif.ttf", uni=True)
        self.add_font(
            "dejavu-bold", fname=CURRENT_DIR / "DejaVuSerif-Bold.ttf", uni=True
        )
        self.add_font("dejavu-mono", fname=CURRENT_DIR / "DejaVuSansMono.ttf", uni=True)
        self.black_and_white = True

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
        self.pdf.cell(w=0, h=self.line_height, txt=txt, ln=1)

    def empty_line(self):
        self.pdf.cell(w=0, h=self.line_height, txt="", ln=1)

    def rect(self, x, y, w, h):
        self.pdf.rect(x, y, w, h, "F")

    def borders(self, x, y, w, h):
        self.pdf.rect(x, y, w, h, "D")

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
        self.pdf.set_font("dejavu-mono")
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

    def draw_gray_900(self):
        self.pdf.set_draw_color(0x11, 0x18, 0x27)
        return self

    def fill_white(self):
        self.pdf.set_fill_color(0xFF, 0xFF, 0xFF)
        return self

    def fill_gray_50(self):
        self.pdf.set_fill_color(0xF9, 0xFA, 0xFB)
        return self

    def fill_gray_100(self):
        self.pdf.set_fill_color(0xF3, 0xF4, 0xF6)
        return self

    def fill_gray_200(self):
        self.pdf.set_fill_color(0xE5, 0xE7, 0xEB)
        return self

    def fill_gray_300(self):
        self.pdf.set_fill_color(0xD1, 0xD5, 0xDB)
        return self

    def fill_gray_400(self):
        self.pdf.set_fill_color(0x9C, 0xA3, 0xAF)
        return self

    def fill_gray_500(self):
        self.pdf.set_fill_color(0x6B, 0x72, 0x80)
        return self

    def fill_gray_600(self):
        self.pdf.set_fill_color(0x4B, 0x55, 0x63)
        return self

    def fill_gray_700(self):
        self.pdf.set_fill_color(0x37, 0x41, 0x51)
        return self

    def fill_gray_800(self):
        self.pdf.set_fill_color(0x1F, 0x29, 0x37)
        return self

    def fill_gray_900(self):
        self.pdf.set_fill_color(0x11, 0x18, 0x27)
        return self

    def fill_black(self):
        self.pdf.set_fill_color(0x11, 0x18, 0x27)
        return self

    def fill_red_600(self):
        if self.pdf.black_and_white:
            return self.fill_gray_600()
        self.pdf.set_fill_color(0xDC, 0x26, 0x26)
        return self

    def fill_yellow_600(self):
        if self.pdf.black_and_white:
            return self.fill_gray_500()
        self.pdf.set_fill_color(0xD9, 0x77, 0x06)
        return self

    def fill_green_600(self):
        if self.pdf.black_and_white:
            return self.fill_gray_400()
        self.pdf.set_fill_color(0x05, 0x96, 0x69)
        return self

    def fill_blue_600(self):
        self.pdf.set_fill_color(0x25, 0x63, 0xEB)
        return self

    def fill_pink_600(self):
        if self.pdf.black_and_white:
            return self.fill_gray_300()
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
            "period_end": period["end"],
            "student_id": student_id,
            "cycle": student["cycle"],
            "group_id": group_id,
        },
    )
    data = r["data"]

    data["period"] = period
    data["student"] = student

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

    # Now move non evaluated to "InProgress"
    for l1_id in evaluations:
        evaluations[l1_id]["InProgress"] += total[l1_id] - (
            evaluations[l1_id]["NotAcquired"]
            + evaluations[l1_id]["InProgress"]
            + evaluations[l1_id]["Acquired"]
            + evaluations[l1_id]["TipTop"]
        )

    data["evaluations_count_by_domain_status"] = evaluations
    data["evaluations_count_by_domain"] = total

    # Grand total
    not_acquired = 0
    in_progress = 0
    acquired = 0
    tip_top = 0
    for l1_id in evaluations:
        not_acquired += evaluations[l1_id]["NotAcquired"]
        in_progress += evaluations[l1_id]["InProgress"]
        acquired += evaluations[l1_id]["Acquired"]
        tip_top += evaluations[l1_id]["TipTop"]

    data["evaluations_count_by_status"] = {
        "not_acquired": not_acquired,
        "in_progress": in_progress,
        "acquired": acquired,
        "tip_top": tip_top,
        "total": not_acquired + in_progress + acquired + tip_top,
    }

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
