# URIAH — House Website

A private-exhibition homepage for URIAH: *A Day, Considered*. White gallery
space, deep black and a single champagne accent; Bodoni Moda headlines with
Jost for navigation and details.

## The story

The photographs are grouped by mood into five chapters that follow one day:
I Morning, II In Transit, III A Pause, IV Soft Light, V Evening.

**Homepage** (calm, curated by hand): a full-screen opening scene, the story
in one line, **The Signature Look** (a drag-to-turn multi-angle viewer),
**Five Moods** (one photograph per chapter, each leading into the
collection), one full-bleed moment, **Held Close** (fabric and craft
close-ups), a short horizontal sequence of selected frames, and a quiet close.

**Collection** (`collection.html`): every photograph, chapter by chapter,
with filters and a full-screen viewer.

## How it is built

- **Two pages.** `index.html` is the calm, hand-curated homepage;
  `collection.html` holds every photograph, filterable by chapter. New photos
  only ever appear on the collection page.
- `content/site.json` holds everything: chapters, photo order, titles, alt
  text, and the hand-picked features (hero, signature frames, full-bleed
  moments, craft crops).
- `python3 tools/build.py` generates both pages from it. Do not edit
  the HTML files by hand.
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
