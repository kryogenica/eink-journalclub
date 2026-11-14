#!/usr/bin/env python3
"""Fetch the newest episode title from journalclub.io's public episodes page.

Writes episode.json, which the e-ink dashboard reads. No login is used: the
episodes page lists every title publicly. The page has no dates and is not in
date order, so the newest episode is picked by its ID, whose first 8 hex digits
are the creation time in seconds since 1970.
"""
import html
import json
import re
import sys
import urllib.request
from datetime import datetime, timezone

URL = "https://journalclub.io/episodes"
OUT = "episode.json"


def main() -> int:
    req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0 (compatible; eink-dashboard)"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        page = resp.read().decode("utf-8", errors="replace")

    episodes = []
    for ep_id, row in re.findall(r'<tr class="episode-card"[^>]*data-episode-id="([0-9a-f]{24})"[^>]*>(.*?)</tr>', page, flags=re.S):
        cell = re.search(r"<td[^>]*>(.*?)</td>", row, flags=re.S)
        if not cell:
            continue
        title = " ".join(html.unescape(re.sub(r"<[^>]+>", " ", cell.group(1))).split())
        if title:
            episodes.append((int(ep_id[:8], 16), ep_id, title))

    if not episodes:
        print("No episodes found; the page layout may have changed.", file=sys.stderr)
        return 1

    created, ep_id, title = max(episodes)
    data = {
        "title": title,
        "episode_id": ep_id,
        "published_utc": datetime.fromtimestamp(created, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": URL,
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"{len(episodes)} episodes; newest: {title} ({data['published_utc']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
