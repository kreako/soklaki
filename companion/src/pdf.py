from fpdf import FPDF, HTMLMixin
from path import Path
import re


CURRENT_DIR = Path(__file__).abspath().dirname()

MARKER_WIDTH = 8
RIGHT_STOP = 200 - 4 * MARKER_WIDTH  # 10 for page right margin


def make_safe_filename(s):
    def safe_char(c):
        if c.isalnum() or c == ".":
            return c
        else:
            return "_"

    fname = "".join(safe_char(c) for c in s).rstrip("_")
    fname = re.sub("_{2,}", "_", fname)
    return fname


class PDF(FPDF, HTMLMixin):
    def __init__(self, total_pages=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.total_pages = total_pages
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
        if self.total_pages:
            self.cell(0, 10, "Page " + str(self.page_no()) + "/{nb}", 0, 0, "C")
        else:
            self.cell(0, 10, "Page " + str(self.page_no()), 0, 0, "C")

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

    def line(self, x1, y1, x2, y2):
        self.pdf.line(x1, y1, x2, y2)

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

    def text_xs(self):
        self.pdf.set_font_size(6)
        self.line_height = 2
        return self

    def text_xxs(self):
        self.pdf.set_font_size(5)
        self.line_height = 1
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

    def draw_gray_300(self):
        self.pdf.set_draw_color(0xD1, 0xD5, 0xDB)
        return self

    def draw_gray_400(self):
        self.pdf.set_draw_color(0x9C, 0xA3, 0xAF)
        return self

    def draw_gray_500(self):
        self.pdf.set_draw_color(0x6B, 0x72, 0x80)
        return self

    def draw_gray_600(self):
        self.pdf.set_draw_color(0x4B, 0x55, 0x63)
        return self

    def draw_gray_900(self):
        self.pdf.set_draw_color(0x11, 0x18, 0x27)
        return self

    def draw_red_600(self):
        if self.pdf.black_and_white:
            return self.draw_gray_600()
        self.pdf.set_draw_color(0xDC, 0x26, 0x26)
        return self

    def draw_yellow_600(self):
        if self.pdf.black_and_white:
            return self.draw_gray_500()
        self.pdf.set_draw_color(0xD9, 0x77, 0x06)
        return self

    def draw_green_600(self):
        if self.pdf.black_and_white:
            return self.draw_gray_400()
        self.pdf.set_draw_color(0x05, 0x96, 0x69)
        return self

    def draw_pink_600(self):
        if self.pdf.black_and_white:
            return self.draw_gray_300()
        self.pdf.set_draw_color(0xDB, 0x27, 0x77)
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
