"""Render the Anthony & Eunice bottle label as a print-ready vector PDF.

The finished page is exactly 70 x 55 mm. All live lettering is drawn with
embedded TrueType fonts from ``assets/fonts``.

Run from the repository root:

    python tools/render_bottle_label.py

An optional output path can be supplied as the first argument.
"""

from __future__ import annotations

import sys
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas


ROOT = Path(__file__).resolve().parents[1]
FONT_DIR = ROOT / "assets" / "fonts"
DEFAULT_OUTPUT = ROOT / "output" / "pdf" / "anthony-eunice-bottle-label-70x55mm-revised.pdf"

PAGE_WIDTH = 70 * mm
PAGE_HEIGHT = 55 * mm

PAPER_LIGHT = HexColor("#FBF8F1")
NAVY = HexColor("#172B42")
GOLD_DARK = HexColor("#745B2B")


def register_fonts() -> None:
    fonts = {
        "PinyonScript": FONT_DIR / "PinyonScript-Regular.ttf",
        "CormorantGaramond": FONT_DIR / "CormorantGaramond-Regular.ttf",
        "MontserratMedium": FONT_DIR / "Montserrat-Medium.ttf",
    }
    missing = [str(path) for path in fonts.values() if not path.exists()]
    if missing:
        raise FileNotFoundError("Missing bundled font files:\n  " + "\n  ".join(missing))
    for name, path in fonts.items():
        pdfmetrics.registerFont(TTFont(name, str(path)))


def draw_tracking_text(
    canvas: Canvas,
    text: str,
    center_x: float,
    baseline_y: float,
    font_name: str,
    font_size: float,
    tracking: float,
    colour,
) -> None:
    """Draw centered text with explicit tracking, preserving live type."""
    canvas.setFont(font_name, font_size)
    canvas.setFillColor(colour)
    widths = [pdfmetrics.stringWidth(char, font_name, font_size) for char in text]
    total_width = sum(widths) + tracking * max(0, len(text) - 1)
    x = center_x - total_width / 2
    for char, width in zip(text, widths):
        canvas.drawString(x, baseline_y, char)
        x += width + tracking


def render(output_path: Path) -> None:
    register_fonts()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    canvas = Canvas(str(output_path), pagesize=(PAGE_WIDTH, PAGE_HEIGHT), pageCompression=1)
    canvas.setTitle("Anthony & Eunice - Thank You Bottle Label")
    canvas.setAuthor("Anthony & Eunice")
    canvas.setSubject("70 x 55 mm wedding bottle label")

    # Warm, unframed paper ground.
    canvas.setFillColor(PAPER_LIGHT)
    canvas.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)

    # Clean typographic hierarchy from the bottle reference.
    canvas.setFillColor(NAVY)
    thank_you_size = 37.0
    max_thank_you_width = 53 * mm
    natural_width = pdfmetrics.stringWidth("Thank you", "PinyonScript", thank_you_size)
    thank_you_size *= min(1.0, max_thank_you_width / natural_width)
    canvas.setFont("PinyonScript", thank_you_size)
    canvas.drawCentredString(PAGE_WIDTH / 2, 29.0 * mm, "Thank you")

    draw_tracking_text(
        canvas,
        "FOR CELEBRATING            WITH US",
        PAGE_WIDTH / 2,
        24.1 * mm,
        "MontserratMedium",
        5.6,
        1.15,
        GOLD_DARK,
    )
    draw_tracking_text(
        canvas,
        "ANTHONY & EUNICE",
        PAGE_WIDTH / 2,
        7.8 * mm,
        "CormorantGaramond",
        9.2,
        1.0,
        NAVY,
    )

    canvas.showPage()
    canvas.save()


if __name__ == "__main__":
    destination = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else DEFAULT_OUTPUT
    render(destination)
    print(destination)
