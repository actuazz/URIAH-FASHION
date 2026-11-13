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
2. **Find new pages.** For each file run
   `python3 tools/ingest.py --check <file>`. It prints `NEW` or
   `DUPLICATE of <id>`. Ignore duplicates.
3. **Look at each NEW page** and skip it if it is not a fashion photograph
   (blank pages, decorations, text-only slides, price lists).
4. **Get it at full quality.** Export just those pages again as `png` with
   `export_quality: "pro"` and download them.
5. **Place it in the story.** Choose the chapter whose mood fits best. The
   chapters, in story order, are in `content/site.json`:
   - `morning`: bright, open streets, the day beginning
   - `transit`: movement, crossings, travel, the city in motion
   - `pause`: still, quiet, shopfronts, seated, monochrome
   - `light`: soft daylight, satin, florals, poolside, airy
   - `evening`: warm lamplight, interiors, rich detail, night
   Write a short, quiet title (2–4 words, sentence case, e.g. "Late light")
   and a plain alt text describing the outfit and setting. Then run:
   `python3 tools/ingest.py <png> --chapter <key> --title "<title>" --alt "<alt>" --source "canva:DAHIlHPgXMQ:p<N>"`
6. **Rebuild** with `python3 tools/build.py`, and check that the page opens
   with no missing images.
7. **Publish.** Commit with a message like
   `Add 2 photos from Canva (pages 33, 34)` and push to the default branch.
   GitHub Pages republishes the site within a minute or two.
8. If nothing was new, change nothing and do not commit.

## Notes

- Removing a page in Canva does **not** remove it from the site. Delete its
  entry from `content/site.json` and its files in `assets/photos/` by hand.
- The hero, the signature look, the full-bleed moments and the fabric crops
  are chosen by hand in `content/site.json` → `features` and are not changed
  by the sync.
- To move a photo to another chapter, change its `chapter` in
  `content/site.json` and run `python3 tools/build.py`.
