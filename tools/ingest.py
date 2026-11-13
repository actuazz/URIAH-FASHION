#!/usr/bin/env python3
"""Add a photograph to the site, or check whether it is already there.

Check only (prints NEW, DUPLICATE of <id>, or UPDATED <id>):
    python3 tools/ingest.py --check path/to/image.jpg

  UPDATED means it is a photo already on the site but visibly edited, for
  example with the logo removed. Swap in the new version, keeping its place,
  title and chapter:
    python3 tools/ingest.py path/to/image.png --replace <id> --source "canva:DAHIlHPgXMQ:p<N>"

Add (creates web sizes, appends to content/site.json; then run tools/build.py):
    python3 tools/ingest.py path/to/image.jpg --chapter light \
        --title "Late light" --alt "Champagne top beside a pool" --source "canva:DAHIlHPgXMQ:p33"

Chapters are the moods defined in content/site.json ("chapters" -> "key").
Duplicates are found with a perceptual hash, so a re-export or resize of a
photo that is already on the site is recognised and skipped.
"""
import argparse
import json
import os
import sys

from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "content", "site.json")
PHOTOS = os.path.join(ROOT, "assets", "photos")
THRESHOLD = 10  # max differing bits (of 64) to count as the same photograph


def dhash(im, size=8):
    g = im.convert("L").resize((size + 1, size), Image.LANCZOS)
    px = list(g.tobytes())
    bits = 0
    for y in range(size):
        for x in range(size):
            bits = (bits << 1) | (px[y * (size + 1) + x] > px[y * (size + 1) + x + 1])
    return f"{bits:016x}"


def distance(a, b):
    return bin(int(a, 16) ^ int(b, 16)).count("1")


def changed(im, pid):
    """True if `im` differs visibly from the stored version (e.g. a logo was removed)."""
    old = Image.open(os.path.join(PHOTOS, f"{pid}-800.webp")).convert("L")
    new = im.convert("L").resize(old.size, Image.LANCZOS)
    a, b = old.resize((400, round(old.height * 400 / old.width))), new.resize((400, round(new.height * 400 / new.width)))
    diff = sum(1 for x, y in zip(a.tobytes(), b.tobytes()) if abs(x - y) > 40)
    return diff / (a.width * a.height) > 0.002


def save_sizes(im, pid):
    sizes = [800, 1600] + ([2400] if os.path.exists(os.path.join(PHOTOS, f"{pid}-2400.webp")) else [])
    for w in sizes:
        r = im if im.width <= w else im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        r.save(os.path.join(PHOTOS, f"{pid}-{w}.webp"), quality=80 if w < 2400 else 78, method=6)
    return Image.open(os.path.join(PHOTOS, f"{pid}-1600.webp")).size


def find_duplicate(site, h):
    best = min(((distance(h, p["hash"]), p["id"]) for p in site["photos"]), default=(99, None))
    return best[1] if best[0] <= THRESHOLD else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("image")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--chapter")
    ap.add_argument("--title")
    ap.add_argument("--alt")
    ap.add_argument("--source", default="")
    ap.add_argument("--replace", metavar="ID", help="swap in a new version of an existing photo")
    a = ap.parse_args()

    with open(SITE, encoding="utf-8") as f:
        site = json.load(f)
    im = ImageOps.exif_transpose(Image.open(a.image)).convert("RGB")
    # compare at the same scale the stored hashes were made from (800px wide)
    probe = im.resize((800, round(im.height * 800 / im.width)), Image.LANCZOS)
    h = dhash(probe)
    dup = find_duplicate(site, h)
    if a.check:
        if not dup:
            print("NEW")
        else:
            print(f"UPDATED {dup}" if changed(im, dup) else f"DUPLICATE of {dup}")
        return
    if a.replace:
        p = next((x for x in site["photos"] if x["id"] == a.replace), None)
        if not p:
            sys.exit(f"no photo with id {a.replace}")
        p["width"], p["height"] = save_sizes(im, p["id"])
        p["hash"] = h
        if a.source:
            p["source"] = a.source
        with open(SITE, "w", encoding="utf-8") as f:
            json.dump(site, f, indent=1, ensure_ascii=False)
        print(f"replaced {p['id']} ({p['title']}); hand-made crops in assets/craft are not regenerated")
        return
    if dup:
        print(f"skipped: already on the site as {dup}")
        return
    chapters = {c["key"] for c in site["chapters"]}
    if a.chapter not in chapters or not a.title or not a.alt:
        sys.exit(f"--chapter (one of {sorted(chapters)}), --title and --alt are required")
    if im.width < 1200:
        print(f"warning: only {im.width}px wide; it may look soft when opened full-screen")
    pid = f"{max(int(p['id']) for p in site['photos']) + 1:02d}"
    w, hgt = save_sizes(im, pid)
    site["photos"].append({"id": pid, "chapter": a.chapter, "title": a.title, "alt": a.alt,
                           "width": w, "height": hgt, "hash": h, "source": a.source})
    with open(SITE, "w", encoding="utf-8") as f:
        json.dump(site, f, indent=1, ensure_ascii=False)
    print(f"added {pid} to {a.chapter}")


if __name__ == "__main__":
    main()
