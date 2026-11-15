#!/usr/bin/env python3
"""Print today's Facebook post (image URL + caption) as JSON.

Usage: python3 tools/next_post.py [YYYY-MM-DD]   (defaults to today in Asia/Manila)
"""
import json, os, sys, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
s = json.load(open(os.path.join(ROOT, "content", "social.json"), encoding="utf-8"))
if len(sys.argv) > 1:
    day = datetime.date.fromisoformat(sys.argv[1])
else:
    day = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=8)).date()   # Manila is UTC+8
n = (day - datetime.date.fromisoformat(s["start_date"])).days
post = s["posts"][n % len(s["posts"])]
print(json.dumps({"date": day.isoformat(), "day": n, "page_id": s["page_id"],
                  "image_url": s["image_base"] + post["image"], "photo": post["photo"],
                  "caption": post["caption"]}, ensure_ascii=False, indent=1))
