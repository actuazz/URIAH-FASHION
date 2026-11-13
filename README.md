# URIAH — House Website

A private-exhibition homepage for URIAH: *A Day, Considered*. White gallery
space, deep black and a single champagne accent; Bodoni Moda headlines with
Jost for navigation and details.

## The story

The photographs are grouped by mood into five chapters that follow one day:

| | Chapter | Mood | Layout |
|---|---|---|---|
| I | Morning | bright, open streets | full-screen hero + floating exhibition |
| II | In Transit | movement, crossings | floating exhibition, then a full-bleed moment |
| III | A Pause | stillness, shopfronts, monochrome | floating exhibition, then a full-bleed moment |
| IV | Soft Light | satin, florals, poolside | horizontal scrolling sequence |
| V | Evening | lamplight, woven detail | layered silhouettes on black |

Between them sit **The Signature Look**, a drag-to-turn multi-angle viewer, and
**Held Close**, a fabric and craft section built from close-up crops.

## How it is built

- `content/site.json` holds everything: chapters, photo order, titles, alt
  text, and the hand-picked features (hero, signature frames, full-bleed
  moments, craft crops).
- `python3 tools/build.py` generates `index.html` from it. Do not edit
  `index.html` by hand.
- `python3 tools/ingest.py` adds a new photograph (web sizes + manifest entry)
  and detects duplicates.
- `SYNC.md` describes the automatic Canva → website sync.
- Photos live in `assets/photos/` as WebP at 800 px and 1600 px wide (2400 px
  for full-screen images); craft crops are in `assets/craft/`.

## Preview and publish

Run `python3 -m http.server` in this folder and open http://localhost:8000.
To publish, push to GitHub and enable GitHub Pages (Settings → Pages → deploy
from the default branch, root folder).

## Commerce scope

A brand and catalogue site: no cart, checkout or payments. Enquiries go to the
official URIAH Facebook page.
