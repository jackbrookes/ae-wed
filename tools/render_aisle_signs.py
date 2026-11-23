"""Render the A4 aisle signs and impose the same pages on a single A1 sheet."""
import argparse
from pathlib import Path

import fitz
from fontTools.pens.boundsPen import BoundsPen
from fontTools.ttLib import TTFont
from reportlab import rl_config
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont as ReportLabFont
from reportlab.pdfgen.canvas import Canvas

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / 'references/aisle-signs'
OUTPUT = ROOT / 'output/pdf'
A4_FILE = OUTPUT / 'aisle-signs-a4.pdf'
SIGNS = [
    ('Love', 'is', 'Patient'),
    ('Love', 'is', 'Kind'),
    ('Love', 'does not', 'Envy'),
    ('Love', 'does not', 'Boast'),
    ('Love', 'Believes', 'all', 'Things'),
    ('Love', 'Rejoices', 'in the', 'Truth'),
    ('Love', 'Always', 'Protects'),
    ('Love', 'Always', 'Perseveres'),
    ('Love', 'Hopes', 'all', 'Things'),
    ('Love', 'Never', 'Fails'),
]


def ink_bounds(font, text):
    """Measure visible ink, including swashes outside a glyph's advance width."""
    glyphs = font.getGlyphSet()
    cmap = font.getBestCmap()
    left, bottom, right, top = float('inf'), float('inf'), -float('inf'), -float('inf')
    advance = 0
    for letter in text:
        glyph = glyphs[cmap[ord(letter)]]
        pen = BoundsPen(glyphs)
        glyph.draw(pen)
        if pen.bounds:
            x0, y0, x1, y1 = pen.bounds
            left, bottom = min(left, advance+x0), min(bottom, y0)
            right, top = max(right, advance+x1), max(top, y1)
        advance += glyph.width
    return left, bottom, right, top


def draw_signs(path):
    pdfmetrics.registerFont(ReportLabFont('HelloSweety', str(path)))
    font = TTFont(path)
    rl_config.useA85 = False
    canvas = Canvas(str(A4_FILE), pagesize=A4, initialFontName='HelloSweety', invariant=True)
    canvas.setTitle('Aisle signs | Anthony & Eunice')
    for lines in SIGNS:
        canvas.scale(mm, mm)
        canvas.drawImage(str(ART/'aisle-sign-template-a4.jpg'), 0, 0, 210, 297)
        sizes = []
        for line in lines:
            left, bottom, right, top = ink_bounds(font, line)
            target_height = 29 if line in ('is', 'in the', 'all', 'does not') else 48
            scale = min(163/(right-left), target_height/(top-bottom))
            sizes.append((left, bottom, right, top, scale))
        gap = 11 if len(lines) == 3 else 8
        block_height = sum((top-bottom)*scale for _, bottom, _, top, scale in sizes) + gap*(len(lines)-1)
        y = 162 + block_height/2
        canvas.setFillColor(HexColor('#FBF8F1'))
        for line, (left, bottom, right, top, scale) in zip(lines, sizes):
            canvas.setFont('HelloSweety', scale * font['head'].unitsPerEm)
            canvas.drawString(105 - (left+right)*scale/2, y-top*scale, line)
            y -= (top-bottom)*scale + gap
        canvas.showPage()
    canvas.save()


def draw_sheet():
    with fitz.open(A4_FILE) as signs, fitz.open() as sheet:
        page = sheet.new_page(width=841*mm, height=594*mm)
        width, gutter = 162, 4
        height = width*297/210
        left = (841 - 5*width - 4*gutter)/2
        top = (594 - 2*height - gutter)/2
        for index in range(len(signs)):
            row, col = divmod(index, 5)
            x = left + col*(width+gutter)
            y = top + row*(height+gutter)
            page.show_pdf_page(fitz.Rect(x*mm, y*mm, (x+width)*mm, (y+height)*mm), signs, index)
            for cx, dx in [(x,-1), (x+width,1)]:
                for cy, dy in [(y,-1), (y+height,1)]:
                    for ax, ay in [(dx,0),(0,dy)]:
                        p1 = ((cx+ax*.45)*mm,(cy+ay*.45)*mm)
                        p2 = ((cx+ax*1.7)*mm,(cy+ay*1.7)*mm)
                        page.draw_line(p1,p2,color=(.35,.35,.35),width=.35)
        sheet.set_metadata({'title': 'Aisle signs | A1 cut sheet'})
        sheet.save(OUTPUT/'aisle-signs-a1-cut-sheet.pdf', garbage=4, deflate=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("font", type=Path, help="Path to the supplied HelloSweety.ttf")
    draw_signs(parser.parse_args().font)
    draw_sheet()
