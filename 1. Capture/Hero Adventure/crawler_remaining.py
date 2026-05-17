import requests
from bs4 import BeautifulSoup, Tag
import json
import os
import time
import re
import sys
from urllib.parse import urljoin

sys.stdout.reconfigure(encoding="utf-8")

BASE_URL = "https://heros-adventure-wiki.xd.cn"
OUTPUT_DIR = r"C:\Projects\Dashboard\1. Capture\Hero Adventure"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
session = requests.Session()
session.headers.update(HEADERS)

def fetch(path):
    try:
        r = session.get(urljoin(BASE_URL, path), timeout=30)
        r.encoding = "utf-8"
        return r.text if r.status_code == 200 else None
    except Exception as e:
        print(f"  ERROR: {e}")
        return None

def extract_title(html):
    s = BeautifulSoup(html, "html.parser")
    t = s.select_one("#page-title")
    return t.get_text(strip=True) if t else ""

def parse_companions(html):
    soup = BeautifulSoup(html, "html.parser")
    content = soup.select_one("#page-content")
    if not content: return []
    companions = []
    all_section_h1s = content.select("h1")
    for section_h1 in all_section_h1s:
        section_name = section_h1.get_text(strip=True)
        table = section_h1.find_next_sibling("table", class_="wiki-content-table")
        while table:
            if table.find_previous_sibling("h1") != section_h1:
                for h1 in all_section_h1s:
                    if h1 == section_h1: continue
                    if table == h1.find_next_sibling("table", class_="wiki-content-table"):
                        table = None
                        break
                if table is None: break
            rows = table.select("tr")
            for row in rows:
                cells = row.select("td")
                if len(cells) < 5: continue
                first = cells[0].get_text(strip=True)
                if not first.strip().isdigit(): continue
                a = cells[1].select_one("a")
                name = a.get_text(strip=True) if a else cells[1].get_text(strip=True)
                href = a.get("href", "") if a else ""
                npc_id = ""
                m = re.search(r"npc:(\d+)", href)
                if m: npc_id = m.group(1)
                companions.append({
                    "section": section_name,
                    "id": int(first),
                    "npc_id": npc_id,
                    "name": name,
                    "gender": cells[2].get_text(strip=True),
                    "faction": cells[3].get_text(strip=True),
                    "notes": cells[4].get_text(strip=True)
                })
            table = table.find_next_sibling("table", class_="wiki-content-table")
    return companions

def parse_generic(html):
    soup = BeautifulSoup(html, "html.parser")
    c = soup.select_one("#page-content")
    if not c: return {"text": ""}
    text = c.get_text("\n", strip=True)
    return {"text": text[:50000]}

def get_guide_links():
    html = fetch("/start")
    if not html: return []
    soup = BeautifulSoup(html, "html.parser")
    links = set()
    for a in soup.select("a[href]"):
        h = a["href"]
        if h.startswith("/") and not h.startswith("/#") and not h.startswith("//"):
            p = h.rstrip("/")
            if p and p != "/start" and "." not in p.split("/")[-1]:
                links.add(p)
    exclude = {
        "/start", "/weapons", "/equipments", "/martial-arts", "/items",
        "/items-material", "/items-other",
        "/huobanjieyuan", "/chengjiu", "/traits", "/canyubianji",
        "/wiki-editing", "/wiki-bug", "/bianji", "/gonglve",
        "/xinshourumen", "/diqutansuo", "/menpaishili", "/youxijieju",
        "/wuxueliupai", "/qitagonglve", "/huobanyujieyuan"
    }
    return sorted(links - exclude)

# 1) Companions
print("[1/3] Crawling companions...")
html = fetch("/huobanjieyuan")
if html:
    c = parse_companions(html)
    title = extract_title(html)
    saved = {"title": title, "count": len(c), "items": c}
    with open(os.path.join(OUTPUT_DIR, "companions.json"), "w", encoding="utf-8") as f:
        json.dump(saved, f, ensure_ascii=False, indent=2)
    print(f"  -> {len(c)} companions saved")
else:
    print("  FAILED")

# 2) Guides
print("\n[2/3] Crawling guide pages...")
links = get_guide_links()
print(f"  Found {len(links)} pages")
guides = {}
for i, path in enumerate(links):
    print(f"  [{i+1}/{len(links)}] {path}")
    html = fetch(path)
    if html:
        title = extract_title(html)
        data = parse_generic(html)
        guides[path.strip("/")] = {"url": urljoin(BASE_URL, path), "title": title, "text": data["text"]}
    else:
        print("  FAILED")
    time.sleep(0.5)

with open(os.path.join(OUTPUT_DIR, "guides.json"), "w", encoding="utf-8") as f:
    json.dump(guides, f, ensure_ascii=False, indent=2)
print(f"  Saved {len(guides)} guides")

# 3) Combined
print("\n[3/3] Writing all_data.json...")
codex = json.load(open(os.path.join(OUTPUT_DIR, "codex.json"), encoding="utf-8"))
traits = json.load(open(os.path.join(OUTPUT_DIR, "traits.json"), encoding="utf-8"))
companions = json.load(open(os.path.join(OUTPUT_DIR, "companions.json"), encoding="utf-8"))

combined = {
    "codex": codex,
    "traits": traits,
    "companions": companions,
    "guides": guides
}
with open(os.path.join(OUTPUT_DIR, "all_data.json"), "w", encoding="utf-8") as f:
    json.dump(combined, f, ensure_ascii=False, indent=2)

total_entries = 0
for k in codex:
    total_entries += codex[k].get("count", 0) if "count" in codex[k] else len(codex[k].get("items", []))
total_entries += companions.get("count", 0)
total_entries += len(guides)

print(f"\nTotal entries: {total_entries}")
print("Done!")
