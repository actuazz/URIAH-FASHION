# URIAH — House Website

*A Day, Considered.* Elevated wear. Everyday essentials.

## Pages

- **Home** (`index.html`): a full-screen opening, **the edits** (six moods of
  the day, each a photograph beside a short caption and a link to its look),
  **the looks** (one card per outfit), **the details** under the tagline, and
  **how to order**.
- **The Looks** (`looks.html`): the visual journal. Every photograph at its
  natural shape with its caption, filterable by look; filtering shows the
  look's pieces and an "Ask about Look 0N" link.

Italiana for headings, DM Sans for text, warm off-white and muted gold.

## How it is built

- `content/site.json` holds the looks, the photos (each belongs to one look),
  titles, alt text and the homepage picks. Hidden photos (the two collages)
  are kept but not shown.
- `python3 tools/build.py` generates both pages. Do not edit the HTML by hand.
- `python3 tools/ingest.py` adds or replaces a photograph and detects
  duplicates. `SYNC.md` describes the Canva → website sync.

## Preview and publish

Run `python3 -m http.server` in this folder and open http://localhost:8000.
To publish, push to GitHub and enable GitHub Pages (Settings → Pages → deploy
from the default branch, root folder).

## Commerce scope

A brand and catalogue site: no cart, checkout or payments. Enquiries go to the
official URIAH Facebook page.
