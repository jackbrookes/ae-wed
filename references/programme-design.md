# Anthony & Eunice programme design

## Original Word layouts

All three programmes use portrait pages with a centred heading, the couple’s names in 30 pt Segoe Script, and a bold 10 pt date with spaced numerals. The timeline sits in a centred, borderless table with two equal event columns and a narrow middle column. Read each pair left to right, then move down. The left event aligns right and the right event aligns left, so both face the centre. A diamond starts the timeline, and each pair has a filled diamond and a short vertical segment in the middle column. Each event stacks its time, uppercase label, and icon.

The cells are white and the main ink is charcoal (`#2D3034`). Most times and event labels are bold 8 pt. The event symbols use Segoe UI Symbol, with emoji appearance dependent on the renderer. The [programme catalogue](wedding-programmes.md) records the icon for every entry, including the paired symbols on day 3.

| Programme | Source page and layout | Distinctive details |
| --- | --- | --- |
| Patlo & Magadi | US Letter, 1-inch margins, 4 event pairs | Freestyle Script heading, Aptos schedule, and person, woman, couple, glasses, and heart icons. |
| Wedding celebration | A4, approximately 12 mm vertical and 15 mm horizontal margins, 8 event pairs | Cambria theme font, letter-spaced welcome heading, two-line final event, and an outlined sparkle beneath the timeline. |
| Kgoroso | US Letter, 1-inch margins, 6 event pairs | Calibri theme font, with notes and hearts together on three entries near the end. |

## Refined print proof

The [three-page PDF proof](../output/pdf/anthony-eunice-programmes-proof.pdf) uses A4 portrait throughout. Each page retains the source heading, couple’s names, date, opposing event columns, diamonds, event labels, and individual icons. The wedding celebration also retains its separate end ornament as an open diamond.

| Element | Proof specification |
| --- | --- |
| Paper and ink | Light ivory `#FBF8F1` background, deep navy `#172B42` headings and event labels, antique gold `#A18343` timeline, and dark gold `#745B2B` dates, times, and line-art symbols. |
| Heading | 14 pt Cormorant Garamond, 54 pt Pinyon Script for the names, and a tracked 10 pt Montserrat date. |
| Event text | 11 pt Montserrat times above 10 pt Montserrat Medium uppercase labels. Times use `HH:MM`, and the wedding’s final entry retains its two-line label. |
| Timeline | Continuous 0.65 pt centre rule, filled diamonds at the opening and each event pair, and 29 pt from the rule to each inside text edge. Row baselines are 100 pt apart for Patlo & Magadi, 69 pt for the wedding celebration, and 81 pt for Kgoroso. |
| Icons | 12 pt gold line-art symbols and colour emoji in a 12 pt box. Icons retain their original assignments and sit under each event label. |

## A1 portrait programmes

The [Patlo & Magadi](../output/pdf/patlo-magadi-a1.pdf), [wedding celebration](../output/pdf/wedding-celebration-a1.pdf), and [Kgoroso](../output/pdf/kgoroso-a1.pdf) posters each occupy one 594 × 841 mm page. The double gold border and botanical corners use the invitation artwork. Each event has its own stop, with a Montserrat time on the left and a Cormorant Garamond event label on the right. The wedding celebration sets its event labels in smaller, lightly letter-spaced capitals beneath title-case venue headings. The Pinyon Script names sit above a written-out date. All three posters use the same time column, with fixed-width Montserrat numerals aligned at the colon. The timeline sits 190 mm from the left edge and closes with a filled gold diamond.

The original vector icons include a sprig for arrivals, an open book for prayers, a goblet for meals and toasts, and a lyre for music and dance. All artwork scales to the printer’s resolution. Each PDF embeds the three typefaces as subsets.

Run `python tools/render_programme_posters.py` with ReportLab, fontTools and PyMuPDF installed to rebuild the posters from the programme catalogue.
