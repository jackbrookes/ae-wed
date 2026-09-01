# Anthony & Eunice Wedding

A shared design project for Anthony and Eunice's wedding celebrations in November 2026. The main deliverable is a wedding invitation website, supported by coordinated print and packaging pieces that use the same visual language.

## Planned deliverables

- Responsive wedding invitation website
- Downloadable or print-ready wedding programme (PDF)
- Wedding food and drinks menu
- Custom labels for bottled or packaged drinks
- Other matching day-of stationery as needed

## Event details

| Event | Date |
| --- | --- |
| Patlo / Magadi | 26 November 2026 |
| Wedding ceremony | 28 November 2026 |
| Kgoroso ya Ngwetsi | 30 November 2026 |

Venues, times, directions, RSVP details, dress code, registry information, and final wording are still to be confirmed.

## Design direction

The supplied invitation reference establishes the initial art direction:

- Warm ivory or cream background
- Muted antique-gold linework and ornament
- Deep navy for selected headings and key information
- Refined serif typography paired with an expressive calligraphic script
- A crowned `A / E` monogram surrounded by a botanical wreath
- Fine double-line borders, decorative corner flourishes, dividers, and small architectural icons
- Formal, romantic, elegant, and lightly vintage in character

These motifs should be translated thoughtfully across screen and print. The website should preserve the spacious, ceremonial feel of the reference while remaining readable, accessible, responsive, and easy to navigate. Print pieces should share the same colour palette, typography, monogram, borders, and ornament system.

## Project structure

```text
.
├── index.html
├── styles.css
├── script.js
├── favicon.svg
├── README.md
├── assets/
│   ├── monogram-crest.png
│   ├── monogram-crest.svg
│   └── regency-corner-complete.svg
└── references/
    └── anthony-eunice-invitation-reference.png
```

## Preview the website

The invitation is a dependency-free static site. From this directory, run:

```powershell
python -m http.server 4173 --bind 127.0.0.1
```

Then open [http://127.0.0.1:4173](http://127.0.0.1:4173). The Google Fonts,
placeholder photographs, and map embeds need an internet connection; graceful visual
fallbacks are included for offline previews.

The event times and venue pins are deliberately marked as placeholders until the final
logistics are confirmed.

## Reference material

The original visual reference is stored at [`references/anthony-eunice-invitation-reference.png`](references/anthony-eunice-invitation-reference.png). It is a source of art direction, not yet a production-ready asset. Any reusable monogram, borders, flourishes, or icons should be recreated as clean vector artwork for consistent scaling and print quality.

## Production notes

- Establish shared colour values and licensed typefaces before building individual pieces.
- Keep editable source artwork separate from compressed web assets and print-ready exports.
- Prepare print documents with the printer's required page size, bleed, safe area, and colour profile.
- Export the programme as an accessible PDF where practical.
- Proof all names, Setswana wording, dates, venues, and timings before publication or print.
- Optimise website imagery and provide useful alternative text without using the reference image as a substitute for live text.

## Next steps

1. Confirm the content, venues, timings, RSVP flow, and required website sections.
2. Define the shared brand kit: colours, typefaces, monogram, borders, ornaments, and icons.
3. Create the responsive website structure and a reusable component system.
4. Apply the same system to the programme, menu, and drink-label layouts.
5. Review digital and printed proofs together for visual consistency and accuracy.
