from pydantic import BaseModel, Field
from path import Path

from report import PDF, RIGHT_STOP, MARKER_WIDTH


class TemplateReportData(BaseModel):
    cycle: str


class TemplateReportInput(BaseModel):
    input: TemplateReportData


class TemplateReportOutput(BaseModel):
    cycle: str


async def generate(gql_client, reports_dir, input: TemplateReportInput):
    cycle = input.input.cycle
    data = await gql_report(gql_client, cycle)

    # Now generation
    pdf = PDF(total_pages=False)
    # Header
    pdf.add_page()
    with pdf.edit().font_bold().text_lg().text_black() as e:
        e.write("Rapport d'évaluation du socle commun", align="C")
        e.empty_line()
    with pdf.edit().font_normal().text_lg() as e:
        e.write("École :")
        e.empty_line()
        e.write("Date du rapport :")
        e.empty_line()
        e.write("Nom :")
        e.empty_line()
        e.write("Prénom :")
        e.empty_line()
        e.write("Cycle :")
        e.empty_line()
        e.write("Date d'anniversaire :")
        e.empty_line()
        e.write("Date d'entrée à l'école :")
        e.empty_line()
        e.write("Date de sortie de l'école :")
        e.empty_line()

    for l1_raw in data["socle"]:
        l1_id = l1_raw["id"]
        l1 = data["container_by_id"][l1_id]
        pdf.add_page()

        with pdf.edit().font_bold().text_gray_700() as e:
            txt = f"{l1['full_rank']} {l1['text'].upper()}"
            pdf.multi_cell(
                w=RIGHT_STOP - 10,  # -10 for page left margin
                h=e.line_height,
                txt=txt,
                ln=1,
                align="L",
            )

        for l2_idx, l2_raw in enumerate(l1_raw["children"]):
            l2_id = l2_raw["id"]
            l2 = data["container_by_id"][l2_id]

            with pdf.edit().text_gray_700() as e:
                if pdf.get_y() >= 219:
                    pdf.add_page()
                if l2_idx > 0:
                    e.empty_line()
                txt = f"{l2['full_rank']} {l2['text']}"
                pdf.multi_cell(
                    w=RIGHT_STOP - 10,  # -10 for page left margin
                    h=e.line_height,
                    txt=txt,
                    ln=1,
                    align="L",
                )
                e.empty_line()

            if l2_raw["competencies"]:
                output_competency_legend(pdf)

            for competency_raw in l2_raw["competencies"]:
                competency_id = competency_raw["id"]
                output_competency_table(pdf, competency_id, data)

        if l1_raw["competencies"]:
            output_competency_legend(pdf)

        for competency_raw in l1_raw["competencies"]:
            competency_id = competency_raw["id"]
            output_competency_table(pdf, competency_id, data)

    pdf.add_page()
    with pdf.edit().font_bold().text_lg().text_black() as e:
        e.write("Commentaire", align="C")
        e.empty_line()

    pdf.add_page()
    with pdf.edit().font_bold().text_lg().text_black() as e:
        e.write("Notice", align="C")
        e.empty_line()

    with pdf.edit().font_normal() as e:
        e.write(
            "Le socle commun de connaissances, de compétences et de culture est divisé en domaines. "
            "Les domaines sont eux-même divisés en sous-domaines, puis en compétences."
        )
        e.empty_line()
        e.write(
            "Chaque compétence possède un numéro et un titre, suivie de quatre petites cases, une pour chaque niveau d'évaluation, avec de gauche à droite :"
        )
        e.write("· Maîtrise insuffisante")
        e.write("· Maîtrise fragile")
        e.write("· Maîtrise satisfaisante")
        e.write("· Très bonne maîtrise")
        e.empty_line()
        e.write(
            "Pour chaque compétence, vous pouvez cocher une case pour indiquer un niveau, puis utiliser l'espace en dessous pour ajouter un commentaire."
        )
        e.empty_line()
        e.empty_line()
        e.write("Par exemple :")
        e.empty_line()
        e.empty_line()
        output_competency_legend(pdf)
        _output_competency_table(
            pdf,
            "2.1.9. Manipuler avec soin",
            check_last_case=True,
            add_space_after=False,
        )
    with pdf.edit().font_mono() as e:
        e.empty_line()
        e.write(
            "  Clémence fait de la sculpture sur grain de riz, la manipulation avec soin n'a aucun secret pour elle."
        )
        e.empty_line()
        e.empty_line()

    with pdf.edit().font_normal() as e:
        e.write(
            "La dernière page avec le titre \"Commentaire\" est là pour vous permettre d'écrire un commentaire général sur l'élève."
        )
        e.empty_line()
        e.write("C'est un texte libre qui peut parler, par exemple, de :")
        e.write(
            "· L'engagement, l'implication dans le groupe et le fonctionnement de l'école"
        )
        e.write("· Le rapport aux apprentissages")
        e.write("· Le rapport aux autres")
        e.write("· Les intérêts, les projets de l'élève")
        e.write("· Les forces et les difficultés de l'élève")
        e.empty_line()
        e.empty_line()
        e.empty_line()
        e.empty_line()
        e.empty_line()
        e.empty_line()
        e.empty_line()

    with pdf.edit().font_normal().text_xs() as e:
        e.write(
            "Ce modèle de rapport ne contient pas les observations que vous remplissez toute l'année et que vous pouvez utiliser comme \"preuves\" d'évaluation."
        )
        e.empty_line()
        e.write(
            "Ce modèle de rapport a été produit avec les données de soklaki produite par l'école démocratique du Tarn."
        )
        e.empty_line()
        e.empty_line()
        pdf.write_html(
            'Pour plus d\'informations, et un logiciel qui vous aide à évaluer le socle, visitez <A HREF="https://soklaki.fr">soklaki.fr</A>'
        )
    output_dir = Path(reports_dir) / "template"
    output_dir.makedirs_p()
    output_fname = f"template_{cycle}.pdf"
    output_path = output_dir / output_fname
    pdf.output(output_path)


def _output_competency_table(pdf, txt, check_last_case=False, add_space_after=True):
    with pdf.edit().text_gray_700().draw_gray_900() as e:
        lines = len(
            pdf.multi_cell(
                w=RIGHT_STOP - 10,  # -10 for page left margin
                h=e.line_height,
                txt=txt,
                split_only=True,
            )
        )
        y = pdf.get_y()
        if y + (lines + 3) * e.line_height >= 297 - 15 - 10:  # 10 margin, 15 footer
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

        e.fill_white()
        e.rect(RIGHT_STOP + 0 * MARKER_WIDTH, y, MARKER_WIDTH, e.line_height * lines)
        e.borders(RIGHT_STOP + 0 * MARKER_WIDTH, y, MARKER_WIDTH, e.line_height * lines)

        e.fill_white()
        e.rect(RIGHT_STOP + 1 * MARKER_WIDTH, y, MARKER_WIDTH, e.line_height * lines)
        e.borders(RIGHT_STOP + 1 * MARKER_WIDTH, y, MARKER_WIDTH, e.line_height * lines)

        e.fill_white()
        e.rect(RIGHT_STOP + 2 * MARKER_WIDTH, y, MARKER_WIDTH, e.line_height * lines)
        e.borders(RIGHT_STOP + 2 * MARKER_WIDTH, y, MARKER_WIDTH, e.line_height * lines)

        e.fill_white()
        e.rect(RIGHT_STOP + 3 * MARKER_WIDTH, y, MARKER_WIDTH, e.line_height * lines)
        e.borders(RIGHT_STOP + 3 * MARKER_WIDTH, y, MARKER_WIDTH, e.line_height * lines)
        if check_last_case:
            pdf.set_y(y)
            pdf.set_x(RIGHT_STOP + 3 * MARKER_WIDTH + 2)
            pdf.cell(
                w=0,
                h=e.line_height,
                txt="x",
                align="L",
            )
        if add_space_after:
            e.empty_line()
            e.empty_line()
            e.empty_line()


def output_competency_table(pdf, competency_id, data):
    competency = data["competency_by_id"][competency_id]
    txt = f"{competency['full_rank']} {competency['text']}"
    _output_competency_table(pdf, txt)


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


async def gql_report(gql_client, cycle):
    r = await gql_client.run_query(
        """
query Report(
    $cycle: cycle!,
) {
    socle: default_socle_container(
        where: {
            cycle: { _eq: $cycle }
            container_id: { _is_null: true }
        }
        order_by: { alpha_full_rank: asc }
    ) {
        id
        children(
            order_by: { alpha_full_rank: asc }
        ) {
            id
            competencies(
                order_by: { alpha_full_rank: asc }
            ) {
                id
            }
        }
        competencies(
            order_by: { alpha_full_rank: asc }
        ) {
            id
        }
    }
    competencies: default_socle_competency {
        container_id
        full_rank
        id
        rank
        text
    }
    containers: default_socle_container {
        id
        container_id
        full_rank
        rank
        text
    }
}
        """,
        {
            "cycle": cycle,
        },
    )
    data = r["data"]
    data["container_by_id"] = {
        container["id"]: container for container in data["containers"]
    }
    data["competency_by_id"] = {
        competency["id"]: competency for competency in data["competencies"]
    }
    return data