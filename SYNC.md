# Canva → website sync

The site's photographs come from one Canva design: **WEBSITE** (`DAHIlHPgXMQ`).
New pages added to that design are added to the website automatically by a
scheduled Claude task that follows the steps below. Everything the page shows
comes from `content/site.json`; `index.html` is generated from it.

## Steps for each run

1. **Export.** With the Canva connector, call `get-export-formats`, then
   `export-design` on `DAHIlHPgXMQ` as `jpg`, `width: 800`, all pages. Download
   every URL straight away (they expire) into a fresh temporary folder outside
   the repository, named `pNN.jpg` by page number.
2. **Sort the pages.** For each file run
   `python3 tools/ingest.py --check <file>`. It prints one of:
   - `DUPLICATE of <id>`: already on the site, unchanged. Ignore it.
   - `UPDATED <id>`: a photo already on the site that has been edited in
     Canva, for example with the logo removed. Export that page as `png`
     with `export_quality: "pro"` and run
     `python3 tools/ingest.py <png> --replace <id> --source "canva:DAHIlHPgXMQ:p<N>"`.
     It keeps the photo's place, title and look.
   - `NEW`: continue with step 3.
3. **Look at each NEW page** and skip it if it is not a single fashion
   photograph: blank pages, decorations, text-only slides, price lists, and
   collages that combine several photos (they repeat frames already shown).
4. **Get it at full quality.** Export just those pages again as `png` with
   `export_quality: "pro"` and download them.
5. **Place it in a look.** Each look in `content/site.json` → `looks` is one
   outfit. If the photo shows an outfit that already has a look, use that
   look's key (e.g. `look-02`). If it is a new outfit, add a new entry to
   `looks` with the next number, a plain descriptive `name` (the pieces, e.g.
   "Ivory Shirt, Pleated Skirt") and its `pieces`. Write a short title
   (2–4 words, sentence case) and a plain alt text describing the outfit and
   setting. Then run:
   `python3 tools/ingest.py <png> --look <key> --title "<title>" --alt "<alt>" --source "canva:DAHIlHPgXMQ:p<N>"`
6. **Rebuild** with `python3 tools/build.py`, and check that the page opens
   with no missing images.
7. **Publish.** Commit with a message like
   `Canva sync: add pages 33, 34; update page 5` and push to the default branch.
   GitHub Pages republishes the site within a minute or two.
8. If nothing was new or updated, change nothing and do not commit.

## Notes

- Removing a page in Canva does **not** remove it from the site. Delete its
  entry from `content/site.json` and its files in `assets/photos/` by hand.
- New photos appear on **The Looks** page (`looks.html`), in their look. The **homepage** is curated by hand in `content/site.json` →
  `features` and shows one photo per look, so a brand-new look also gets a
  card on the homepage automatically.
- The fabric close-ups in `assets/craft/` are hand-cut crops and are not
  regenerated when a photo is replaced.
- To move a photo to another look, change its `look` in `content/site.json`
  and run `python3 tools/build.py`. The first photo of a look leads it.
