#!/usr/bin/env python3
"""Build index.html (home) and looks.html (the journal of every look) from
content/site.json.

Run from the repository root:  python3 tools/build.py

- Home: full-screen opening, the edits (one per mood of the day), the looks,
  the details, and how to order. Curated in site.json -> "features".
- Looks: every photograph at its natural shape with its caption, filterable
  by look. New photos land here automatically. Hidden photos are not listed
  (a feature may still use one on the home page).
"""
import html
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = "assets/photos"
FB = "https://www.facebook.com/Uriah.FashionHouse/"
MSG = "https://m.me/Uriah.FashionHouse"
e = html.escape


def load():
    with open(os.path.join(ROOT, "content", "site.json"), encoding="utf-8") as f:
        return json.load(f)


def srcset(pid):
    parts = [f"{P}/{pid}-800.webp 800w", f"{P}/{pid}-1600.webp 1600w"]
    if os.path.exists(os.path.join(ROOT, P, f"{pid}-2400.webp")):
        parts.append(f"{P}/{pid}-2400.webp 2400w")
    return ", ".join(parts)


def img(p, sizes, focus=None, lazy=True):
    style = f' style="object-position:{focus}"' if focus else ""
    lz = ' loading="lazy"' if lazy else ""
    return (f'<img src="{P}/{p["id"]}-1600.webp" srcset="{srcset(p["id"])}" sizes="{sizes}" width="{p["width"]}" '
            f'height="{p["height"]}"{lz} decoding="async" alt="{e(p["alt"])}"{style}>')


def num(look):
    return look["key"].split("-")[1]


def two_line(t):
    a, b = t.split("|")
    return f"{e(a)}<br><i>{e(b)}</i>"


# ---------- shared ----------

def head(title):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#f8f7f3">
<meta name="description" content="URIAH — Elevated wear. Everyday essentials. A Day, Considered.">
<title>{e(title)}</title>
<link rel="icon" type="image/png" href="assets/va-black.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500&family=Italiana&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css">
</head>'''


def header(over_photo):
    return f'''<header class="site-header{"" if over_photo else " is-solid is-fixed-solid"}" data-header>
  <button class="menu-toggle" aria-label="Open menu" aria-expanded="false" data-menu-open><span></span>Menu</button>
  <a class="brand" href="index.html" aria-label="URIAH home">
    <img class="on-photo" src="assets/va-white.png" alt=""><img class="on-photo brand-word" src="assets/logo-white.png" alt="URIAH">
    <img class="on-paper" src="assets/va-black.png" alt="" aria-hidden="true"><img class="on-paper brand-word" src="assets/wordmark-black.png" alt="" aria-hidden="true">
  </a>
  <a class="header-link" href="{MSG}" target="_blank" rel="noopener">Enquire</a>
</header>'''


def menu():
    return f'''<div class="menu" hidden data-menu>
  <button class="menu-close" data-menu-close>Close</button>
  <nav aria-label="Main">
    <a href="index.html#edits">The Edits</a><a href="looks.html">The Looks</a><a href="index.html#details">The Details</a><a href="index.html#order">How to Order</a>
  </nav>
  <p class="menu-foot"><a href="{FB}" target="_blank" rel="noopener">Facebook ↗</a></p>
</div>'''


def footer(site):
    return f'''<footer class="footer">
  <div class="footer-main">
    <div class="footer-brand"><a href="index.html"><img src="assets/va-black.png" alt=""><img src="assets/wordmark-black.png" alt="URIAH"></a><p>Elevated wear.<br>Everyday essentials.</p></div>
    <div class="footer-col"><b>Explore</b><a href="index.html#edits">The edits</a><a href="looks.html">The looks</a><a href="index.html#order">How to order</a></div>
    <div class="footer-col"><b>Connect</b><a href="{MSG}" target="_blank" rel="noopener">Message us ↗</a><a href="{FB}" target="_blank" rel="noopener">Facebook ↗</a></div>
    <div class="footer-col"><b>A note from the house</b><p>Thoughtful style, considered for everyday life.</p></div>
  </div>
  <div class="footer-bottom"><span>© <span data-year></span> URIAH</span><span>Philippines</span><a href="#top">Back to top ↑</a></div>
</footer>'''


def lightbox():
    return f'''<div class="lightbox" hidden role="dialog" aria-modal="true" aria-label="Photograph" data-lightbox>
  <div class="lb-top"><span data-lb-count></span><button data-lb-close>Close</button></div>
  <figure class="lb-figure"><img src="" alt="" data-lb-img></figure>
  <div class="lb-bottom"><div><span class="kicker" data-lb-kicker></span><b data-lb-title></b></div>
  <div class="lb-nav"><button data-lb-prev aria-label="Previous photograph">←</button><button data-lb-next aria-label="Next photograph">→</button><a class="text-link" href="{MSG}" target="_blank" rel="noopener">Ask about this look <span>↗</span></a></div></div>
</div>'''


def page(title, over_photo, body, site):
    return f'''{head(title)}
<body>
<!-- Generated by tools/build.py from content/site.json. Edit those, not this file. -->
{header(over_photo)}
{menu()}
<main id="top">
{body}
</main>
{footer(site)}
{lightbox()}
<script src="script.js"></script>
</body>
</html>
'''


# ---------- home ----------

def hero(site, by_id):
    panes = "".join(f'<div class="hero-pane hero-pane--{i}">{img(by_id[pid], "100vw", lazy=False)}</div>'
                    for i, pid in enumerate(site["features"]["hero"]))
    return f'''<section class="hero" aria-label="Introduction">
  {panes}
  <div class="hero-text">
    <p class="kicker kicker--light">The collection</p>
    <h1>A Day,<br><i>Considered</i></h1>
  </div>
  <a class="hero-scroll" href="#edits" aria-label="Scroll to the edits"><span>Scroll</span><i></i></a>
</section>'''


def edits(site, by_id, looks):
    f = site["features"]
    h = f["edits_head"]
    rows = []
    for i, ed in enumerate(f["edits"]):
        p, look = by_id[ed["photo"]], looks[ed["look"]]
        image = (f'<div class="edit-image reveal"><a href="looks.html#{look["key"]}" aria-label="See {e(look["name"])}">'
                 f'{img(p, "(max-width:760px) 100vw, 44vw")}</a><span class="image-no">Look {num(look)}</span></div>')
        copy = f'''<div class="edit-copy reveal">
      <span class="overline">{e(ed["overline"])} / {i + 1:02d}</span>
      <h3>{two_line(ed["title"])}</h3>
      <p>{e(ed["text"])}</p>
      <a href="looks.html#{look["key"]}" class="text-link">View the look <span>↗</span></a>
      <span class="edit-aside">{e(ed["aside"])}</span>
    </div>'''
        flip = i % 2 == 1
        rows.append(f'<article class="edit-row{" edit-row--flip" if flip else ""}">{copy + image if flip else image + copy}</article>')
    return f'''<section class="edits" id="edits">
  <div class="section-head">
    <div><p class="kicker">{e(h["kicker"])}</p><h2>{two_line(h["title"])}</h2></div>
    <p class="section-note">{e(h["note"])}</p>
  </div>
  {"".join(rows)}
</section>'''


def looks_grid(site, shown):
    focus = site["features"].get("focus", {})
    cards = []
    for look in site["looks"]:
        photos = [p for p in shown if p["look"] == look["key"]]
        if not photos:
            continue
        lead = photos[0]
        cards.append(f'<a class="look-card reveal" href="looks.html#{look["key"]}"><div class="ph">{img(lead, "(max-width:760px) 45vw, 23vw", focus.get(lead["id"]))}</div>'
                     f'<span class="look-no">Look {num(look)}</span><span class="look-name">{e(look["name"])}</span></a>')
    cards.append('<a class="look-card look-card--all reveal" href="looks.html"><span>All looks</span><em>→</em></a>')
    return f'''<section class="looks-index" id="looks">
  <div class="section-head section-head--tight"><div><p class="kicker">{len(cards) - 1} looks</p><h2>The Looks</h2></div></div>
  <div class="look-grid">{"".join(cards)}</div>
</section>'''


def details(site):
    items = "".join(
        f'<a class="closeup reveal" href="looks.html#{c["look"]}"><div class="ph ph--square"><img src="assets/{c["file"]}" loading="lazy" decoding="async" alt="{e(c["label"])}, close-up"></div>'
        f'<b>{e(c["label"])}</b><span>{e(c["text"])}</span></a>' for c in site["features"]["closeups"])
    return f'''<section class="details" id="details">
  <div class="house-mark"><img src="assets/va-black.png" alt=""></div>
  <p class="kicker">The details</p>
  <h2>Elevated wear.<br><i>Everyday essentials.</i></h2>
  <div class="closeups">{items}</div>
</section>'''


def order():
    return f'''<section class="order" id="order">
  <div><p class="kicker">A personal enquiry</p><h2>How to<br><i>order.</i></h2></div>
  <div class="order-steps">
    <ol>
      <li><span>01</span><div><b>Choose a look</b><p>Note its number, for example Look 02.</p></div></li>
      <li><span>02</span><div><b>Send us a message</b><p>Tell us the look and your usual size. We reply with sizing and availability.</p></div></li>
      <li><span>03</span><div><b>We confirm with you</b><p>Details, payment and delivery are arranged directly in the conversation.</p></div></li>
    </ol>
    <a class="message-button" href="{MSG}" target="_blank" rel="noopener">Message URIAH <span>↗</span></a>
  </div>
</section>'''


# ---------- looks page (the journal) ----------

def journal(site, shown):
    total = len(shown)
    looks = [l for l in site["looks"] if any(p["look"] == l["key"] for p in shown)]
    filters = [f'<button class="filter is-active" data-filter="all">All frames <sup>{total}</sup></button>'] + [
        f'<button class="filter" data-filter="{l["key"]}">Look {num(l)} <sup>{sum(1 for p in shown if p["look"] == l["key"]):02d}</sup></button>'
        for l in looks]
    panels = "".join(f'''<div class="look-panel" data-panel="{l["key"]}" hidden>
    <p class="kicker">Look {num(l)}</p><h2>{e(l["name"])}</h2>
    <ul>{"".join(f"<li>{e(x)}</li>" for x in l["pieces"])}</ul>
    <a class="text-link" href="{MSG}" target="_blank" rel="noopener">Ask about Look {num(l)} <span>↗</span></a>
  </div>''' for l in looks)
    lk = {l["key"]: l for l in looks}
    cards = "".join(
        f'<figure class="journal-card" data-kind="{p["look"]}" data-full="{P}/{p["id"]}-1600.webp" '
        f'data-kicker="{p["id"]} / Look {num(lk[p["look"]])}" data-title="{e(p["title"])}" tabindex="0">'
        f'{img(p, "(max-width:760px) 46vw, 24vw")}'
        f'<figcaption><span>{p["id"]} / Look {num(lk[p["look"]])}</span><b>{e(p["title"])}</b></figcaption></figure>'
        for p in shown)
    return f'''<section class="journal">
  <div class="journal-head">
    <div><p class="kicker">{e(site["story"]["title"])}</p><h1>The<br><i>Looks.</i></h1></div>
    <p>Every frame, arranged by look. Select a look to see its pieces, or a photograph to see it in full.</p>
  </div>
  <div class="journal-filters" aria-label="Filter by look" data-filters>{"".join(filters)}</div>
  {panels}
  <div class="journal-grid" data-masonry>{cards}</div>
  <div class="journal-foot"><span>The URIAH visual journal</span><span>{total} photographs / {len(looks):02d} looks</span></div>
</section>'''


def build():
    site = load()
    by_id = {p["id"]: p for p in site["photos"]}
    looks = {l["key"]: l for l in site["looks"]}
    shown = [p for p in site["photos"] if not p.get("hidden")]
    home = "\n".join([hero(site, by_id), edits(site, by_id, looks), looks_grid(site, shown), details(site), order()])
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(page(f'URIAH — {site["story"]["title"]}', True, home, site))
    with open(os.path.join(ROOT, "looks.html"), "w", encoding="utf-8") as fh:
        fh.write(page("URIAH — The Looks", False, journal(site, shown), site))
    print(f"built index.html + looks.html: {len(shown)} photos, {len(site['looks'])} looks, {len(site['features']['edits'])} edits")


if __name__ == "__main__":
    build()
