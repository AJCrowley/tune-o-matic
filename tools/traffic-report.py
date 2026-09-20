#!/usr/bin/python3
"""tune-o-matic traffic report from the local privacy-friendly access log.
Counts PAGE LOADS: GET / (plus www variants), excluding assets, bots/crawlers,
and our own health checks. No IP data exists in the log by design."""
import glob, os, re, sys
from collections import Counter
from datetime import datetime

LOG_DIR = "/home/crowley/projects/tuneomatic/.traffic"
BOT = re.compile(r"bot|crawl|spider|slurp|curl|wget|python-requests|monitor|uptime|headless|preview|facebookexternal|lighthouse", re.I)
ASSET = re.compile(r"\.(?:png|css|js|ico|svg|webmanifest|yml|json|txt|md|map)(?:\?|$)", re.I)

def parse(path):
    rows = []
    rx = re.compile(r'^\S+ \S+ \S+ \[([^]]+)\] "([^"]*)" (\d+) (\S+) "([^"]*)"')
    for line in open(path, encoding="utf-8", errors="replace"):
        m = rx.match(line)
        if not m:
            continue
        stamp, req, code, size, ua = m.groups()
        method, _, url = req.partition(" ")
        when = datetime.strptime(stamp, "%d/%b/%Y:%H:%M:%S %z")
        rows.append({"t": when, "url": url, "code": int(code), "size": size, "ua": ua})
    return rows

def summarise():
    files = sorted(glob.glob(os.path.join(LOG_DIR, "access-*.log")))
    if not files:
        print("no access logs yet")
        return
    all_rows, per_day = [], Counter()
    uas, urls = Counter(), Counter()
    for f in files:
        for r in parse(f):
            all_rows.append(r)
            per_day[r["t"].strftime("%a %d %b")] += 1
    loads = [r for r in all_rows
             if r["url"].rstrip("?") in ("/", "/?", "/index.html")
             and r["code"] in (200, 304)
             and not BOT.search(r["ua"])]
    human_day = Counter(r["t"].strftime("%a %d %b") for r in loads)
    print(f"=== tuneomatic.app traffic ({all_rows[0]['t']:%d %b} -> {all_rows[-1]['t']:%d %b %Y}, UTC) ===")
    print(f"page loads (GET / by humans, 200/304): {len(loads)}")
    for day, n in sorted(human_day.items()):
        print(f"  {day}: {n}")
    assets = sum(1 for r in all_rows if ASSET.search(r["url"]))
    bots = sum(1 for r in all_rows if BOT.search(r["ua"]))
    print(f"(raw total requests {len(all_rows)}: assets {assets}, bots/monitors {bots}, errors {sum(1 for r in all_rows if r['code'] >= 400)})")
    print("top user agents:")
    for ua, n in Counter(r["ua"] for r in loads).most_common(5):
        print(f"  {n:3d}  {ua[:70]}")

if __name__ == "__main__":
    summarise()
