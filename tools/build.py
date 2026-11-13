#!/usr/bin/env python3
"""Build index.html from content/site.json.

Run from the repository root:  python3 tools/build.py

Every photo in content/site.json belongs to a chapter (a mood). The chapter's
`layout` decides how its photos are composed on the page:
  exhibition  floating, asymmetric pairs and solos
  horizontal  a sideways-scrolling sequence
  layered     overlapping silhouettes on black
Photos used by the hero, the signature viewer or a full-bleed moment are not
repeated inside their chapter.
"""
import html
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = "assets/photos"
FB = "https://www.facebook.com/Uriah.FashionHouse/"
e = html.escape


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


def img(p, sizes, cls="", lazy=True, extra=""):
    pid = p["id"]
    return (f'<img{f" class={chr(34)}{cls}{chr(34)}" if cls else ""} src="{P}/{pid}-1600.webp" '
            f'srcset="{srcset(pid)}" sizes="{sizes}" width="{p["width"]}" height="{p["height"]}"'
            f'{" loading=" + chr(34) + "lazy" + chr(34) if lazy else ""} decoding="async" alt="{e(p["alt"])}"{extra}>')


def figure(p, cls, sizes, speed=None, chapter=None):
    sp = f' data-speed="{speed}"' if speed else ""
    return (f'<figure class="piece {cls} reveal"{sp} data-full="{P}/{p["id"]}-1600.webp" data-title="{e(p["title"])}" '
            f'data-chapter="{e(chapter or "")}" data-no="{p["id"]}" tabindex="0">'
            f'<div class="piece-img">{img(p, sizes)}</div>'
            f'<figcaption><span>{p["id"]}</span>{e(p["title"])}</figcaption></figure>')


# ---------- sections ----------

def header():
    return f'''<header class="site-header" data-header>
  <button class="menu-toggle" aria-label="Open menu" aria-expanded="false" data-menu-open><span></span><span></span><em>Menu</em></button>
  <a class="brand" href="#top" aria-label="URIAH home">
    <img class="brand-mark" src="assets/uriah-va-mark.png" alt="">
    <img class="brand-word brand-word--light" src="assets/logo-white.png" alt="URIAH">
    <img class="brand-word brand-word--dark" src="assets/wordmark-black.png" alt="" aria-hidden="true">
  </a>
  <a class="header-enquire" href="{FB}" target="_blank" rel="noopener">Enquire</a>
</header>'''


def menu(site):
    items = "".join(
        f'<li><a href="#ch-{c["key"]}"><span>{c["numeral"]}</span>{e(c["title"])}</a></li>' for c in site["chapters"])
    return f'''<div class="menu" id="menu" hidden data-menu>
  <button class="menu-close" aria-label="Close menu" data-menu-close>Close</button>
  <nav aria-label="Chapters"><p class="eyebrow">{e(site["story"]["title"])}</p><ol>{items}</ol>
  <div class="menu-links"><a href="#signature">The Signature Look</a><a href="#craft">Held Close</a><a href="{FB}" target="_blank" rel="noopener">Enquire ↗</a></div></nav>
</div>'''


def hero(site, by_id):
    ids = site["features"]["hero"]
    first = next(c for c in site["chapters"] if c["key"] == by_id[ids[0]]["chapter"])
    panes = "".join(
        f'<div class="hero-pane hero-pane--{i}">{img(by_id[pid], "100vw", lazy=False)}</div>'
        for i, pid in enumerate(ids))
    return f'''<section class="hero" id="top" aria-label="Introduction">
  {panes}
  <div class="hero-text">
    <p class="eyebrow eyebrow--light">{first["numeral"]} &nbsp;·&nbsp; {e(first["title"])}</p>
    <h1>A Day,<br><i>Considered</i></h1>
  </div>
  <a class="hero-scroll" href="#story" aria-label="Scroll to the story"><span>Scroll</span><i></i></a>
</section>'''


def story(site):
    idx = "".join(f'<li><a href="#ch-{c["key"]}"><span>{c["numeral"]}</span>{e(c["title"])}</a></li>'
                  for c in site["chapters"])
    return f'''<section class="story" id="story">
  <p class="eyebrow reveal">The URIAH Point of View</p>
  <p class="story-lede reveal">{e(site["story"]["intro"])}</p>
  <ol class="story-index reveal">{idx}</ol>
</section>'''


def signature(site, by_id):
    s = site["features"]["signature"]
    frames = [by_id[f] for f in s["frames"]]
    labels = s.get("labels") or [f"View {i+1}" for i in range(len(frames))]
    imgs = "".join(
        f'<img class="sig-frame" src="{P}/{p["id"]}-1600.webp" srcset="{srcset(p["id"])}" sizes="(max-width:760px) 90vw, 46vw" '
        f'width="{p["width"]}" height="{p["height"]}" alt="{e(p["alt"])}" data-label="{e(labels[i])}"{" loading=" + chr(34) + "lazy" + chr(34) if i else ""} draggable="false">'
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
    <a class="line-link" href="{FB}" target="_blank" rel="noopener">Enquire about this look <span>↗</span></a>
  </div>
  <div class="sig-viewer reveal">
    <div class="sig-stage" tabindex="0" role="slider" aria-label="Turn the look: drag, or use the arrow keys" aria-valuemin="1" aria-valuemax="{len(frames)}" aria-valuenow="1" style="aspect-ratio:{w}/{h}" data-sig>
      {imgs}
      <span class="sig-hint" aria-hidden="true"><i>⟷</i> Drag to turn</span>
    </div>
    <div class="sig-ui"><span class="sig-label" data-sig-label>{e(labels[0])}</span><div class="sig-stops">{stops}<i class="sig-progress" data-sig-progress></i></div><span class="sig-count" data-sig-count>01 / {len(frames):02d}</span></div>
  </div>
</section>'''


def chapter_head(c, light=False):
    return f'''<header class="chapter-head{" chapter-head--light" if light else ""} reveal">
    <span class="chapter-no">{c["numeral"]}</span>
    <h2>{e(c["title"])}</h2>
    <p>{e(c["line"])}</p>
  </header>'''


# floating, asymmetric rows: (slot classes, how many photos)
ROWS = [("x-a1 x-a2", 2), ("x-b1", 1), ("x-c1 x-c2", 2), ("x-d1", 1)]
SIZES = {"x-a1": "(max-width:760px) 80vw, 40vw", "x-a2": "(max-width:760px) 62vw, 22vw",
         "x-b1": "(max-width:760px) 80vw, 30vw", "x-c1": "(max-width:760px) 62vw, 20vw",
         "x-c2": "(max-width:760px) 80vw, 38vw", "x-d1": "(max-width:760px) 80vw, 34vw",
         "x-w": "(max-width:760px) 92vw, 58vw"}
SPEEDS = {"x-a1": "0.04", "x-a2": "0.12", "x-b1": "0.07", "x-c1": "0.14", "x-c2": "0.05", "x-d1": "0.08"}


def exhibition(c, photos):
    out, i, r = [], 0, 0
    while i < len(photos):
        if photos[i]["width"] > photos[i]["height"]:  # landscape frames get a wide row of their own
            out.append(f'<div class="ex-row">{figure(photos[i], "x-w", SIZES["x-w"], "0.05", c["title"])}</div>')
            i += 1
            continue
        slots, n = ROWS[r % len(ROWS)]
        slots = slots.split()
        chunk = []
        for p in photos[i:i + n]:  # a pair stops before a landscape frame
            if p["width"] > p["height"]:
                break
            chunk.append(p)
        if len(chunk) < n:  # last row short: fall back to a solo
            slots = ["x-d1"] * len(chunk)
        figs = "".join(figure(p, s, SIZES[s], SPEEDS[s], c["title"]) for p, s in zip(chunk, slots))
        out.append(f'<div class="ex-row">{figs}</div>')
        i += len(chunk)
        r += 1
    return f'''<section class="chapter chapter--exhibition" id="ch-{c["key"]}">
  {chapter_head(c)}
  <div class="exhibition">{"".join(out)}</div>
</section>'''


H_SHAPES = ["h-1", "h-2", "h-3", "h-4"]


def horizontal(c, photos):
    figs = "".join(figure(p, H_SHAPES[i % len(H_SHAPES)], "(max-width:760px) 70vw, 34vw", None, c["title"])
                   for i, p in enumerate(photos))
    return f'''<section class="chapter chapter--horizontal" id="ch-{c["key"]}" data-hscroll>
  <div class="h-sticky">
    <div class="h-track" data-htrack>
      <div class="h-intro">{chapter_head(c)}<span class="h-cue">Continue <i></i></span></div>
      {figs}
    </div>
    <div class="h-progress" aria-hidden="true"><i data-hprogress></i></div>
  </div>
</section>'''


def layered(c, photos):
    groups = [photos[i:i + 4] for i in range(0, len(photos), 4)]
    stacks = "".join(
        '<div class="layers">' + "".join(
            figure(p, f"l-{j % 4 + 1}", "(max-width:760px) 70vw, 30vw", ("0.04", "0.12", "0.07", "0.15")[j % 4], c["title"])
            for j, p in enumerate(g)) + "</div>" for g in groups)
    return f'''<section class="chapter chapter--layered" id="ch-{c["key"]}">
  {chapter_head(c, light=True)}
  {stacks}
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
        f'<figure class="craft-item craft-item--{i + 1} reveal" data-speed="{("0.03", "0.09", "0.05", "0.11")[i % 4]}">'
        f'<div class="piece-img"><img src="assets/{it["file"]}" loading="lazy" decoding="async" alt="{e(it["label"])}: close-up detail"></div>'
        f'<figcaption><b>{e(it["label"])}</b>{e(it["text"])}</figcaption></figure>'
        for i, it in enumerate(items))
    return f'''<section class="craft" id="craft" aria-label="Fabric and craft">
  <div class="craft-head reveal">
    <p class="eyebrow">Fabric &amp; Craft</p>
    <h2>Held<br><i>close.</i></h2>
    <p>We begin with how a piece feels against the skin, then how it falls when you move. The details below are where that thinking lives.</p>
  </div>
  <div class="craft-grid">{figs}</div>
</section>'''


def enquiry_and_footer():
    return f'''<section class="enquiry" id="contact">
  <p class="eyebrow reveal">A Personal Enquiry</p>
  <h2 class="reveal">Something caught<br><i>your eye?</i></h2>
  <p class="reveal">For sizing, availability and orders, speak with us directly.</p>
  <a class="button reveal" href="{FB}" target="_blank" rel="noopener">Message URIAH <span>↗</span></a>
</section>
<footer class="footer">
  <div class="footer-top">
    <a class="footer-brand" href="#top"><img src="assets/uriah-va-mark.png" alt=""><img src="assets/wordmark-black.png" alt="URIAH"></a>
    <p class="footer-sign">Elevated wear.<br><i>Everyday essentials.</i></p>
  </div>
  <div class="footer-cols">
    <div><b>Explore</b><a href="#story">The story</a><a href="#signature">Signature look</a><a href="#craft">Fabric &amp; craft</a></div>
    <div><b>Connect</b><a href="{FB}" target="_blank" rel="noopener">Facebook ↗</a><a href="#contact">Enquiries</a></div>
    <div><b>House</b><p>Considered style for everyday living. Philippines.</p></div>
  </div>
  <div class="footer-base"><span>© <span data-year></span> URIAH</span><a href="#top">Back to top ↑</a></div>
</footer>'''


def lightbox():
    return f'''<div class="lightbox" id="lightbox" hidden role="dialog" aria-modal="true" aria-label="Photograph viewer" data-lightbox>
  <div class="lb-top"><span data-lb-count></span><button data-lb-close>Close</button></div>
  <figure class="lb-figure"><img src="" alt="" data-lb-img></figure>
  <div class="lb-bottom"><div><span class="eyebrow" data-lb-chapter></span><b data-lb-title></b></div>
  <div class="lb-nav"><button data-lb-prev aria-label="Previous photograph">←</button><button data-lb-next aria-label="Next photograph">→</button><a class="line-link" href="{FB}" target="_blank" rel="noopener">Enquire about this look <span>↗</span></a></div></div>
</div>'''


def build():
    site = load()
    by_id = {p["id"]: p for p in site["photos"]}
    f = site["features"]
    used = set(f["hero"]) | set(f["signature"]["frames"]) | {b["id"] for b in f["fullbleed"]}
    body = [hero(site, by_id), story(site), signature(site, by_id)]
    bleeds_after = {}
    for b in f["fullbleed"]:
        bleeds_after.setdefault(b["after"], []).append(b)
    craft_done = False
    for c in site["chapters"]:
        photos = [p for p in site["photos"] if p["chapter"] == c["key"] and p["id"] not in used]
        if c["layout"] in ("horizontal", "layered") and not craft_done:
            body.append(craft(site))  # the craft pause sits between the two halves of the day
            craft_done = True
        if photos:
            body.append({"exhibition": exhibition, "horizontal": horizontal, "layered": layered}[c["layout"]](c, photos))
        for b in bleeds_after.get(c["key"], []):
            body.append(bleed(b, by_id))
    if not craft_done:
        body.append(craft(site))
    doc = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#ffffff">
<meta name="description" content="URIAH — Elevated wear. Everyday essentials. {e(site["story"]["title"])}: a private exhibition of considered dressing.">
<title>URIAH — {e(site["story"]["title"])}</title>
<link rel="icon" type="image/png" href="assets/uriah-va-mark.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,400;0,6..96,500;1,6..96,400&family=Jost:wght@300;400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css">
</head>
<body>
<!-- Generated by tools/build.py from content/site.json. Edit those, not this file. -->
{header()}
{menu(site)}
<main>
{chr(10).join(body)}
{enquiry_and_footer()}
</main>
{lightbox()}
<script src="script.js"></script>
</body>
</html>
'''
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(doc)
    counts = {}
    for p in site["photos"]:
        counts[p["chapter"]] = counts.get(p["chapter"], 0) + 1
    print("built index.html:", len(site["photos"]), "photos", counts)


if __name__ == "__main__":
    build()
