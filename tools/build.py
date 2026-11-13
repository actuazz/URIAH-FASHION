#!/usr/bin/env python3
"""Build index.html (the homepage) and collection.html (the full catalogue)
from content/site.json.

Run from the repository root:  python3 tools/build.py

- The homepage is curated by hand in site.json -> "features". New photos do
  not change it, so it stays calm.
- The collection page shows every photo, grouped by chapter (mood), in the
  order they appear in site.json. New photos land here automatically.
"""
import html
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = "assets/photos"
FB = "https://www.facebook.com/Uriah.FashionHouse/"
e = html.escape
q = chr(34)


def load():
    with open(os.path.join(ROOT, "content", "site.json"), encoding="utf-8") as f:
        return json.load(f)


def has(path):
    return os.path.exists(os.path.join(ROOT, path))


def srcset(pid):
    parts = [f"{P}/{pid}-800.webp 800w", f"{P}/{pid}-1600.webp 1600w"]
    if has(f"{P}/{pid}-2400.webp"):
        parts.append(f"{P}/{pid}-2400.webp 2400w")
    return ", ".join(parts)


def img(p, sizes, lazy=True, extra="", cls=""):
    c = f" class={q}{cls}{q}" if cls else ""
    lz = f" loading={q}lazy{q}" if lazy else ""
    return (f'<img{c} src="{P}/{p["id"]}-1600.webp" srcset="{srcset(p["id"])}" sizes="{sizes}" '
            f'width="{p["width"]}" height="{p["height"]}"{lz} decoding="async" alt="{e(p["alt"])}"{extra}>')


def piece(p, cls, sizes, chapter, speed=None):
    """A photograph that opens in the full-screen viewer."""
    sp = f' data-speed="{speed}"' if speed else ""
    return (f'<figure class="piece {cls} reveal"{sp} data-full="{P}/{p["id"]}-1600.webp" data-title="{e(p["title"])}" '
            f'data-chapter="{e(chapter)}" tabindex="0">'
            f'<div class="piece-img">{img(p, sizes)}</div>'
            f'<figcaption><span>{p["id"]}</span>{e(p["title"])}</figcaption></figure>')


# ---------- shared chrome ----------

def head(title, desc):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#ffffff">
<meta name="description" content="{e(desc)}">
<title>{e(title)}</title>
<link rel="icon" type="image/png" href="assets/va-black.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,400;0,6..96,500;1,6..96,400&family=Jost:wght@300;400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css">
</head>'''


def header(on_photo):
    right = '<a class="header-link" href="collection.html">Collection</a>' if on_photo else \
        '<a class="header-link" href="index.html">Home</a>'
    return f'''<header class="site-header{"" if on_photo else " is-solid is-fixed-solid"}" data-header>
  <button class="menu-toggle" aria-label="Open menu" aria-expanded="false" data-menu-open><span></span><em>Menu</em></button>
  <a class="brand" href="index.html" aria-label="URIAH home">
    <img class="brand-mark brand-word--light" src="assets/va-white.png" alt="">
    <img class="brand-mark brand-word--dark" src="assets/va-black.png" alt="" aria-hidden="true">
    <img class="brand-word brand-word--light" src="assets/logo-white.png" alt="URIAH">
    <img class="brand-word brand-word--dark" src="assets/wordmark-black.png" alt="" aria-hidden="true">
  </a>
  {right}
</header>'''


def menu(site):
    items = "".join(
        f'<li><a href="collection.html#ch-{c["key"]}"><span>{c["numeral"]}</span>{e(c["title"])}</a></li>'
        for c in site["chapters"])
    return f'''<div class="menu" id="menu" hidden data-menu>
  <button class="menu-close" aria-label="Close menu" data-menu-close>Close</button>
  <nav aria-label="Site"><p class="eyebrow">{e(site["story"]["title"])}</p><ol>{items}</ol>
  <div class="menu-links"><a href="index.html">Home</a><a href="collection.html">The full collection</a><a href="index.html#signature">The signature look</a><a href="{FB}" target="_blank" rel="noopener">Enquiries ↗</a></div></nav>
</div>'''


def footer():
    return f'''<footer class="footer">
  <div class="footer-top">
    <a class="footer-brand" href="index.html"><img src="assets/va-black.png" alt=""><img src="assets/wordmark-black.png" alt="URIAH"></a>
    <p class="footer-sign">Elevated wear.<br><i>Everyday essentials.</i></p>
  </div>
  <div class="footer-cols">
    <div><b>Explore</b><a href="index.html">Home</a><a href="collection.html">The collection</a><a href="index.html#signature">Signature look</a></div>
    <div><b>Enquiries</b><p>For sizing, availability and orders, message us directly.</p><a href="{FB}" target="_blank" rel="noopener">Facebook ↗</a></div>
    <div><b>House</b><p>Considered style for everyday living. Philippines.</p></div>
  </div>
  <div class="footer-base"><span>© <span data-year></span> URIAH</span><a href="#top">Back to top ↑</a></div>
</footer>'''


def lightbox():
    return f'''<div class="lightbox" id="lightbox" hidden role="dialog" aria-modal="true" aria-label="Photograph viewer" data-lightbox>
  <div class="lb-top"><span data-lb-count></span><button data-lb-close>Close</button></div>
  <figure class="lb-figure"><img src="" alt="" data-lb-img></figure>
  <div class="lb-bottom"><div><span class="eyebrow" data-lb-chapter></span><b data-lb-title></b></div>
  <div class="lb-nav"><button data-lb-prev aria-label="Previous photograph">←</button><button data-lb-next aria-label="Next photograph">→</button><a class="line-link" href="{FB}" target="_blank" rel="noopener">Ask about this look <span>↗</span></a></div></div>
</div>'''


def page(title, desc, body, on_photo, site):
    return f'''{head(title, desc)}
<body class="{"page-home" if on_photo else "page-collection"}">
<!-- Generated by tools/build.py from content/site.json. Edit those, not this file. -->
{header(on_photo)}
{menu(site)}
<main id="top">
{body}
</main>
{footer()}
{lightbox()}
<script src="script.js"></script>
</body>
</html>
'''


# ---------- homepage sections ----------

def hero(site, by_id):
    ids = site["features"]["hero"]
    first = next(c for c in site["chapters"] if c["key"] == by_id[ids[0]]["chapter"])
    panes = "".join(f'<div class="hero-pane hero-pane--{i}">{img(by_id[pid], "100vw", lazy=False)}</div>'
                    for i, pid in enumerate(ids))
    return f'''<section class="hero" aria-label="Introduction">
  {panes}
  <div class="hero-text">
    <p class="eyebrow eyebrow--light">{first["numeral"]} &nbsp;·&nbsp; {e(first["title"])}</p>
    <h1>A Day,<br><i>Considered</i></h1>
  </div>
  <a class="hero-scroll" href="#story" aria-label="Scroll to the story"><span>Scroll</span><i></i></a>
</section>'''


def story(site):
    return f'''<section class="story" id="story">
  <p class="eyebrow reveal">The URIAH Point of View</p>
  <p class="story-lede reveal">{e(site["story"]["intro"])}</p>
</section>'''


def signature(site, by_id):
    s = site["features"]["signature"]
    frames = [by_id[f] for f in s["frames"]]
    labels = s.get("labels") or [f"View {i + 1}" for i in range(len(frames))]
    imgs = "".join(
        f'<img class="sig-frame" src="{P}/{p["id"]}-1600.webp" srcset="{srcset(p["id"])}" sizes="(max-width:760px) 90vw, 46vw" '
        f'width="{p["width"]}" height="{p["height"]}" alt="{e(p["alt"])}" data-label="{e(labels[i])}" draggable="false">'
        for i, p in enumerate(frames))
    stops = "".join(f'<button class="sig-stop" data-stop="{i}" aria-label="{e(l)}"></button>' for i, l in enumerate(labels))
    details = "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in s["details"])
    w, h = frames[0]["width"], frames[0]["height"]
    return f'''<section class="signature" id="signature" aria-label="{e(s["kicker"])}">
  <div class="sig-copy reveal">
    <p class="eyebrow">{e(s["kicker"])}</p>
    <h2>{e(s["title"])}</h2>
    <p class="sig-text">{e(s["text"])}</p>
    <dl class="sig-details">{details}</dl>
  </div>
  <div class="sig-viewer reveal">
    <div class="sig-stage" tabindex="0" role="slider" aria-label="Turn the look: drag, or use the arrow keys" aria-valuemin="1" aria-valuemax="{len(frames)}" aria-valuenow="1" style="aspect-ratio:{w}/{h}" data-sig>
      {imgs}
      <span class="sig-hint" aria-hidden="true"><i>⟷</i> Drag to turn</span>
    </div>
    <div class="sig-ui"><span class="sig-label" data-sig-label>{e(labels[0])}</span><div class="sig-stops">{stops}<i class="sig-progress" data-sig-progress></i></div><span class="sig-count" data-sig-count>01 / {len(frames):02d}</span></div>
  </div>
</section>'''


def moods(site, by_id):
    m = site["features"]["moods"]
    focus = m.get("focus", {})
    panels = []
    for c in site["chapters"]:
        pid = m["picks"].get(c["key"])
        if not pid:
            continue
        p = by_id[pid]
        fp = focus.get(c["key"], "50% 60%")
        panels.append(
            f'<a class="mood" href="collection.html#ch-{c["key"]}">'
            f'<div class="mood-img">{img(p, "(max-width:760px) 72vw, 40vw", extra=f' style="object-position:{fp}"')}</div>'
            f'<span class="mood-cap"><span>{c["numeral"]}</span><b>{e(c["title"])}</b><em>{e(c["line"])}</em></span></a>')
    return f'''<section class="moods" id="moods" aria-label="{e(m["title"])}">
  <header class="section-head reveal"><p class="eyebrow">{e(m["title"])}</p><h2>{m["heading"]}</h2></header>
  <div class="mood-row reveal">{"".join(panels)}</div>
</section>'''


def bleed(f, by_id):
    p = by_id[f["id"]]
    return f'''<section class="bleed" aria-label="{e(f["caption"])}">
  <div class="bleed-img" data-bleed>{img(p, "100vw", extra=f' style="object-position:{f["focus"]}"')}</div>
  <p class="bleed-caption"><span>{p["id"]}</span>{e(f["caption"])}</p>
</section>'''


def craft(site):
    items = site["features"]["craft"]
    figs = "".join(
        f'<figure class="craft-item craft-item--{i + 1} reveal">'
        f'<div class="piece-img"><img src="assets/{it["file"]}" loading="lazy" decoding="async" alt="{e(it["label"])}: close-up detail"></div>'
        f'<figcaption><b>{e(it["label"])}</b>{e(it["text"])}</figcaption></figure>'
        for i, it in enumerate(items))
    return f'''<section class="craft" id="craft" aria-label="Fabric and craft">
  <div class="craft-head reveal">
    <p class="eyebrow">Fabric &amp; Craft</p>
    <h2>Held<br><i>close.</i></h2>
    <p>We begin with how a piece feels against the skin, then how it falls when you move. The details here are where that thinking lives.</p>
  </div>
  <div class="craft-grid">{figs}</div>
</section>'''


H_SHAPES = ["h-1", "h-2", "h-3", "h-4"]


def selected(site, by_id, chapter_title):
    s = site["features"]["selected"]
    figs = "".join(piece(by_id[pid], H_SHAPES[i % 4], "(max-width:760px) 70vw, 34vw", chapter_title(by_id[pid]))
                   for i, pid in enumerate(s["picks"]))
    return f'''<section class="chapter--horizontal" id="selected" data-hscroll aria-label="{e(s["title"])}">
  <div class="h-sticky">
    <div class="h-track" data-htrack>
      <div class="h-intro"><header class="section-head"><p class="eyebrow">{e(s["title"])}</p><h2>Kept<br><i>close.</i></h2><p>{e(s["line"])}</p></header><span class="h-cue">Continue <i></i></span></div>
      {figs}
      <a class="h-end" href="collection.html"><span class="eyebrow">The full collection</span><b>See every<br><i>frame</i></b><em>→</em></a>
    </div>
    <div class="h-progress" aria-hidden="true"><i data-hprogress></i></div>
  </div>
</section>'''


def closing():
    return '''<section class="closing">
  <p class="eyebrow reveal">The end of the day</p>
  <p class="closing-line reveal">Until<br><i>tomorrow.</i></p>
</section>'''


# ---------- collection page ----------

def collection(site):
    shown = [p for p in site["photos"] if not p.get("hidden")]
    total = len(shown)
    filters = [f'<button class="filter is-active" data-filter="all">All <sup>{total}</sup></button>'] + [
        f'<button class="filter" data-filter="{c["key"]}"><span>{c["numeral"]}</span> {e(c["title"])} '
        f'<sup>{sum(1 for p in shown if p["chapter"] == c["key"]):02d}</sup></button>'
        for c in site["chapters"]]
    sections = []
    for c in site["chapters"]:
        photos = [p for p in shown if p["chapter"] == c["key"]]
        if not photos:
            continue
        cards = "".join(piece(p, "cat-card", "(max-width:760px) 46vw, (max-width:1100px) 31vw, 24vw", c["title"]) for p in photos)
        sections.append(f'''<section class="cat-chapter" id="ch-{c["key"]}" data-chapter="{c["key"]}">
  <header class="cat-head reveal"><span class="chapter-no">{c["numeral"]}</span><h2>{e(c["title"])}</h2><p>{e(c["line"])}</p><span class="cat-count">{len(photos):02d} frames</span></header>
  <div class="cat-grid" data-masonry>{cards}</div>
</section>''')
    return f'''<section class="cat-intro">
  <p class="eyebrow">{e(site["story"]["title"])}</p>
  <h1>The<br><i>Collection</i></h1>
  <p>Every frame, arranged by the mood of the day it belongs to. Select a photograph to see it in full.</p>
</section>
<nav class="cat-filters" aria-label="Filter by chapter" data-filters>{"".join(filters)}</nav>
{"".join(sections)}'''


def build():
    site = load()
    by_id = {p["id"]: p for p in site["photos"]}
    ch = {c["key"]: c for c in site["chapters"]}
    f = site["features"]
    home = "\n".join([
        hero(site, by_id), story(site), signature(site, by_id), moods(site, by_id),
        *[bleed(b, by_id) for b in f["fullbleed"]], craft(site),
        selected(site, by_id, lambda p: ch[p["chapter"]]["title"]), closing(),
    ])
    desc = f'URIAH — Elevated wear. Everyday essentials. {site["story"]["title"]}.'
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(page(f'URIAH — {site["story"]["title"]}', desc, home, True, site))
    with open(os.path.join(ROOT, "collection.html"), "w", encoding="utf-8") as fh:
        fh.write(page("URIAH — The Collection", desc, collection(site), False, site))
    counts = {}
    for p in site["photos"]:
        counts[p["chapter"]] = counts.get(p["chapter"], 0) + 1
    print("built index.html + collection.html:", len(site["photos"]), "photos", counts)


if __name__ == "__main__":
    build()
