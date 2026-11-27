#!/usr/bin/env python3
"""TikTok photo posts for @uriahfashionhouse, from URIAH's own photos only.

Uses the same rotation as the Facebook daily post (content/social.json), so a
look appears on both platforms the same day.

    python3 tools/tiktok.py build          # writes assets/tiktok/NN.jpg (fits 1080x1920)
    python3 tools/tiktok.py plan 2026-11-27 10   # JSON list of the next 10 posts
"""
import datetime, json, os, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOCIAL = json.load(open(os.path.join(ROOT, "content", "social.json"), encoding="utf-8"))
BASE = SOCIAL["image_base"]
TAGS = "#URIAH #OOTD #FashionTikTok #OOTDph #PHFashion #FilipinoFashion #StyleInspo #ElevatedWear"


def build():
    for p in SOCIAL["posts"]:
        src = os.path.join(ROOT, p["image"])
        out = os.path.join(ROOT, "assets", "tiktok", os.path.basename(p["image"]))
        im = Image.open(src).convert("RGB")
        im.thumbnail((1080, 1920), Image.LANCZOS)
        im.save(out, "JPEG", quality=88)
    print("built", len(SOCIAL["posts"]))


def post_for(day):
    start = datetime.date.fromisoformat(SOCIAL["start_date"])
    p = SOCIAL["posts"][(day - start).days % len(SOCIAL["posts"])]
    lines = p["caption"].split("\n")
    hook, look = lines[0], lines[2]
    num = look.split("·")[0].strip()  # "Look 03"
    caption = (f"{hook}\n\n{look}\n\nElevated wear. Everyday essentials.\n"
               f"Message us to order. Ask for {num}. Full lookbook: link in bio.\n\n{TAGS}")
    return {"date": day.isoformat(), "photo": p["photo"], "title": hook,
            "image_url": BASE + "assets/tiktok/" + os.path.basename(p["image"]),
            "alt": f"URIAH {look}", "caption": caption}


if __name__ == "__main__":
    if sys.argv[1] == "build":
        build()
    else:
        d = datetime.date.fromisoformat(sys.argv[2])
        n = int(sys.argv[3]) if len(sys.argv) > 3 else 1
        print(json.dumps([post_for(d + datetime.timedelta(i)) for i in range(n)], ensure_ascii=False, indent=1))
