from pydantic import BaseModel, Field
from typing import Optional
from fpdf import FPDF
from path import Path

from gql_client import GqlClientException


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
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()
    pdf.set_font("helvetica", "B", 16)
    pdf.cell(40, 10, "Hello World!")
    pdf.output(Path(reports_dir) / "hello.pdf")
    return ReportOutput(
        report_id=-1,
        pdf_path="meuh.pdf",
        json_path="meuh.json",
    )