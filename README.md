# URIAH — House Website

*A Day, Considered*: seven looks, presented simply. Warm paper, ink, Cormorant
Garamond for titles and Jost for text. The photographs carry the page.

## Pages

- **Home** (`index.html`): the collection title, *Coffee, then onwards*, the
  seven looks, close-up details, and how to order.
- **The Looks** (`looks.html`): every photograph, look by look, with the
  pieces in each look and a direct "Ask about Look 0N" message link.

Photos are shown in a consistent 4:5 frame with one gentle colour treatment so
different shoots sit together; selecting a photo opens it in full, uncropped.

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
