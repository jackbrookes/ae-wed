"""Build A1 programme posters from the catalogue. Requires ReportLab, fontTools and PyMuPDF."""
from io import BytesIO
from pathlib import Path
import re
from xml.etree import ElementTree

import fitz
from fontTools.ttLib import TTFont as OpenTypeFont
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A1
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas

ROOT = Path(__file__).resolve().parents[1]
WIDTH, HEIGHT = 594, 841  # Design coordinates in millimetres, measured from the top.
IVORY, NAVY, GOLD, BRONZE = '#FBF8F1', '#172B42', '#A18343', '#745B2B'
# Original outline motifs, drawn on a common 32-unit grid.
MOTIFS = {
    'sprig': 'M6 27 Q16 17 25 4 M12 20 Q3 19 6 11 Q13 12 12 20 Z M17 15 Q15 7 19 4 Q23 9 17 15 Z M16 17 Q23 11 28 14 Q24 21 16 17 Z',
    'book': 'M16 9 Q10 5 3 7 L3 23 Q10 21 16 25 Q22 21 29 23 L29 7 Q22 5 16 9 Z M16 9 V25 M6 11 Q10 10 13 12 M19 12 Q23 10 26 11 M6 15 Q10 14 13 16 M19 16 Q23 14 26 15',
    'rings': 'M18 18 A7 7 0 1 1 4 18 A7 7 0 1 1 18 18 Z M28 18 A7 7 0 1 1 14 18 A7 7 0 1 1 28 18 Z M15 9 L12 5 L16 2 L20 5 L17 9',
    'goblet': 'M8 4 H24 L23 13 Q22 19 16 19 Q10 19 9 13 Z M9 8 H23 M16 19 V25 Q16 27 10 28 H22 Q16 27 16 25',
    'lyre': 'M8 4 Q3 8 7 15 Q10 20 9 23 Q9 27 16 28 Q23 27 23 23 Q22 20 25 15 Q29 8 24 4 M8 4 Q12 3 10 8 H22 Q20 3 24 4 M12 10 L13 22 M16 10 V24 M20 10 L19 22 M10 23 Q16 27 22 23',
    'bell': 'M7 22 Q10 19 10 13 Q10 7 16 7 Q22 7 22 13 Q22 19 25 22 Z M7 24 H25 M13 26 Q16 30 19 26 M14 7 V5 Q16 2 18 5 V7',
    'flower': 'M15 27 Q18 19 16 14 M16 22 Q8 22 7 16 Q14 16 16 22 M17 19 Q20 13 26 13 Q25 19 17 19 M16 11 C7 16 4 9 11 8 C6 2 14 0 16 6 C19 -1 25 3 21 8 C29 8 26 16 19 12 Q17 17 15 13 Z',
    'camera': 'M3 10 H9 L12 6 H20 L23 10 H29 V25 H3 Z M21 17 A5 5 0 1 1 11 17 A5 5 0 1 1 21 17 Z M24 13 H26',
    'cake': 'M4 26 H28 M6 25 V16 H26 V25 M10 16 V9 H22 V16 M6 18 Q9 22 12 18 Q16 22 20 18 Q23 22 26 18 M16 8 Q11 5 13 3 Q15 2 16 4 Q19 1 20 4 Q20 6 16 8',
}
PROGRAMMES = [
    ('patlo-magadi', 'Patlo & Magadi programme', 'sprig book sprig sprig rings goblet bell flower'),
    ('wedding-celebration', 'Wedding celebration', 'sprig rings camera bell book sprig goblet goblet lyre lyre lyre lyre cake flower sprig lyre'),
    ('kgoroso', 'Kgoroso programme', 'sprig camera bell book sprig goblet goblet lyre rings bell flower lyre'),
]


def vector_pdf(svg):
    with fitz.open('svg', svg.encode()) as drawing:
        return fitz.open('pdf', drawing.convert_to_pdf())


def place(page, drawing, x, y, size):
    page.show_pdf_page(fitz.Rect(x*mm, y*mm, (x+size)*mm, (y+size)*mm), drawing, 0)


def build(section, slug, title, motifs):
    date = re.search(r'\*\*(.+?)\*\*', section)[1]
    entries = re.findall(r'^\| (\d\d:\d\d) \| (.*?) \|', section, re.M)
    data = BytesIO()
    c = Canvas(data, pagesize=A1, initialFontName='Sans', invariant=True)
    c.setTitle(f'{title} | Anthony & Eunice')
    c.scale(mm, mm)
    c.setFillColor(HexColor(IVORY))
    c.rect(0, 0, WIDTH, HEIGHT, stroke=0, fill=1)
    c.setStrokeColor(HexColor(GOLD))
    for inset, weight in [(12, .65), (17, .35)]:
        c.setLineWidth(weight)
        c.rect(inset, inset, WIDTH-2*inset, HEIGHT-2*inset)
    def text(s, x, y, font, size, colour, align):
        c.setFont(font, size)
        c.setFillColor(HexColor(colour))
        align(x, HEIGHT-y, s)
    text(title, WIDTH/2, 66, 'Serif', 28, NAVY, c.drawCentredString)
    text('Anthony & Eunice', WIDTH/2, 126, 'Script', 56, NAVY, c.drawCentredString)
    text(date, WIDTH/2, 181, 'Sans', 13, BRONZE, c.drawCentredString)
    event_size = 24 if len(entries) < 16 else 22.5
    labels = [label.capitalize().replace(' & dance floor', '\n& dance floor').splitlines()
              for _, label in entries]
    spinex = 190  # Common timeline position in mm on all three posters.
    first, last = 232, 747
    pitch = (last-first)/(len(entries)-1)
    c.setLineWidth(.55)
    c.line(spinex, HEIGHT-first, spinex, HEIGHT-last-21)
    end = c.beginPath()
    y = HEIGHT-last-21
    end.moveTo(spinex, y+2.8)
    for dx, dy in [(2.1,0),(0,-2.8),(-2.1,0)]:
        end.lineTo(spinex+dx,y+dy)
    end.close()
    c.setFillColor(HexColor(GOLD))
    c.drawPath(end, stroke=0, fill=1)
    positions = []
    for i, ((time, label), motif) in enumerate(zip(entries, motifs.split(), strict=True)):
        cy = first+i*pitch
        c.setFillColor(HexColor(IVORY))
        c.circle(spinex, HEIGHT-cy, 9.7, stroke=0, fill=1)
        positions.append((motif, spinex-8, cy-8))
        text(time, spinex-20, cy+4.6, 'Time', 15, BRONZE, c.drawRightString)
        for j, line in enumerate(labels[i]):
            text(line, spinex+20, cy+6+j*20, 'Serif', event_size, NAVY, c.drawString)
    c.showPage()
    c.save()
    with fitz.open('pdf', data.getvalue()) as doc:
        page = doc[0]
        icons = {}
        for motif, x, y in positions:
            if motif not in icons:
                icons[motif] = vector_pdf(f'<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32"><path d="{MOTIFS[motif]}" fill="none" stroke="{BRONZE}" stroke-width="1.35" stroke-linejoin="round" stroke-linecap="round"/></svg>')
            place(page, icons[motif], x, y, 16)
        ornament = ElementTree.parse(ROOT/'assets/regency-corner-complete.svg').getroot()
        content = ''.join(ElementTree.tostring(child, encoding='unicode') for child in ornament)
        for right, bottom in [(False,False),(True,False),(False,True),(True,True)]:
            transform = f'translate({200 if right else 0} {200 if bottom else 0}) scale({-1 if right else 1} {-1 if bottom else 1}) translate(200 0) rotate(90)'
            with vector_pdf(f'<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200"><g transform="{transform}">{content}</g></svg>') as corner:
                place(page, corner, WIDTH-81 if right else 17, HEIGHT-81 if bottom else 17, 64)
        doc.save(ROOT/f'output/pdf/{slug}-a1.pdf', garbage=4, deflate=True)


if __name__ == '__main__':
    for alias, filename in [('Sans','Montserrat-Medium'), ('Script','PinyonScript-Regular'), ('Serif','CormorantGaramond-Regular')]:
        pdfmetrics.registerFont(TTFont(alias, str(ROOT/f'assets/fonts/{filename}.ttf')))
    # ReportLab uses the default cmap. Select Montserrat's tabular figures for time text.
    with OpenTypeFont(ROOT/'assets/fonts/Montserrat-Medium.ttf') as font:
        cmap = font.getBestCmap()
        figures = {ord(d): cmap[ord(d)] + '.tf' for d in '0123456789'}
        for table in font['cmap'].tables:
            if table.isUnicode():
                table.cmap.update(figures)
        for record in font['name'].names:
            if record.nameID == 6:
                record.string = 'Montserrat-Medium-Tabular'.encode(record.getEncoding())
        tabular = BytesIO()
        font.save(tabular)
        tabular.seek(0)
        pdfmetrics.registerFont(TTFont('Time', tabular))
    catalogue = (ROOT/'references/wedding-programmes.md').read_text()
    for section, programme in zip(catalogue.split('## Day ')[1:], PROGRAMMES, strict=True):
        build(section, *programme)
