import requests
from bs4 import BeautifulSoup, Tag
import json
import os
import time
import re
import sys
from urllib.parse import urljoin, urlparse

sys.stdout.reconfigure(encoding="utf-8")

BASE_URL = "https://heros-adventure-wiki.xd.cn"
OUTPUT_DIR = r"C:\Projects\Dashboard\1. Capture\Hero Adventure"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

session = requests.Session()
session.headers.update(HEADERS)

def fetch_page(path):
    url = urljoin(BASE_URL, path)
    try:
        resp = session.get(url, timeout=30)
        resp.encoding = "utf-8"
        if resp.status_code == 200:
            return resp.text
        else:
            print(f"  [WARN] {url} -> status {resp.status_code}")
            return None
    except Exception as e:
        print(f"  [ERROR] {url} -> {e}")
        return None

def extract_page_name(html):
    soup = BeautifulSoup(html, "html.parser")
    title_el = soup.select_one("#page-title")
    return title_el.get_text(strip=True) if title_el else ""

def extract_nav_links(html):
    soup = BeautifulSoup(html, "html.parser")
    links = set()
    for a in soup.select("a[href]"):
        href = a["href"]
        if href.startswith("/") and not href.startswith("/#") and not href.startswith("//"):
            path = href.rstrip("/")
            if path and path != "/start" and "." not in path.split("/")[-1]:
                links.add(path)
    return sorted(links)

def safe_text(el, sep="\n"):
    if not el:
        return ""
    texts = []
    for child in el.children:
        if isinstance(child, Tag):
            if child.name == "br":
                texts.append(sep)
            else:
                t = child.get_text(strip=True)
                if t:
                    texts.append(t)
        elif child.string and child.string.strip():
            texts.append(child.string.strip())
    return " ".join(texts) if not sep else (" " + sep + " ").join(texts)

# ── Codex parsers ──

def parse_weapons_table(html):
    soup = BeautifulSoup(html, "html.parser")
    table = soup.select_one("table.item-table")
    if not table:
        return []
    items = []
    rows = table.select("tr[data-title]")
    current_type = None
    for row in rows:
        td_list = row.select("td")
        if len(td_list) < 5:
            continue
        type_cell = td_list[0]
        if type_cell.get("rowspan") or (type_cell.get_text(strip=True) and type_cell.get_text(strip=True) not in ("", " ", "\n")):
            current_type = type_cell.get_text(strip=True)
        name_cell = td_list[1]
        a_tag = name_cell.select_one("a")
        if not a_tag:
            continue
        name = a_tag.get_text(strip=True).split("\n")[0]
        img = a_tag.select_one("img")
        img_src = img["src"] if img else ""
        href = a_tag.get("href", "")
        item_id_raw = safe_text(td_list[2])
        item_id = item_id_raw if not item_id_raw.startswith("{$") else ""
        stats = safe_text(td_list[3])
        effects = safe_text(td_list[4]) if len(td_list) > 4 else ""
        obtain = safe_text(td_list[5]) if len(td_list) > 5 else ""
        obtain = obtain.replace("{$obtain}", "").replace("{$craft}", "").replace("{$limit}", "").strip()
        description = ""
        next_row = row.find_next_sibling("tr")
        if next_row:
            desc_cells = next_row.select("td")
            if len(desc_cells) == 1 and desc_cells[0].get("colspan") == "6":
                description = desc_cells[0].get_text(strip=True)
        rarity = ""
        for cls in name_cell.get("class", []):
            if cls.startswith("rarity-"):
                rarity = cls.replace("rarity-", "")
                break
        if name and not name.startswith("{$"):
            items.append({
                "type": current_type,
                "name": name,
                "id": item_id,
                "image": img_src,
                "rarity": rarity,
                "stats": stats,
                "effects": effects,
                "obtain": obtain,
                "description": description
            })
    return items

def parse_martial_arts_table(html):
    soup = BeautifulSoup(html, "html.parser")
    table = soup.select_one("table.item-table")
    if not table:
        return []
    items = []
    rows = table.select("tr[data-title]")
    for row in rows:
        a_tag = row.select_one("td a")
        if not a_tag:
            continue
        name = a_tag.get_text(strip=True).split("\n")[0]
        if name.startswith("{$"):
            continue
        img = a_tag.select_one("img")
        img_src = img["src"] if img else ""
        href = a_tag.get("href", "")
        item_id = ""
        if href:
            m = re.search(r"kungfu:(\d+)", href)
            if m:
                item_id = m.group(1)
        td_list = row.select("td")
        ma_type = td_list[0].get_text(strip=True) if td_list else ""
        stats = safe_text(td_list[3]) if len(td_list) > 3 else ""
        effects = safe_text(td_list[4]) if len(td_list) > 4 else ""
        obtain = safe_text(td_list[5]) if len(td_list) > 5 else ""
        obtain = obtain.replace("{$obtain}", "").strip()
        rarity = ""
        if a_tag.parent:
            for cls in a_tag.parent.get("class", []):
                if cls.startswith("rarity-"):
                    rarity = cls.replace("rarity-", "")
                    break
        items.append({
            "type": ma_type,
            "name": name,
            "id": item_id,
            "image": img_src,
            "rarity": rarity,
            "stats": stats,
            "effects": effects,
            "obtain": obtain
        })
    return items

def parse_items_table(html):
    soup = BeautifulSoup(html, "html.parser")
    table = soup.select_one("table.item-table")
    if not table:
        return {"text": soup.select_one("#page-content").get_text("\n", strip=True) if soup.select_one("#page-content") else ""}
    items = []
    rows = table.select("tr[data-title]")
    for row in rows:
        td_list = row.select("td")
        if len(td_list) < 4:
            continue
        item_type = td_list[0].get_text(strip=True)
        name_cell = td_list[1]
        name = name_cell.get_text(strip=True).split("\n")[0]
        img = name_cell.select_one("img")
        img_src = img["src"] if img else ""
        item_id = td_list[2].get_text(strip=True) if len(td_list) > 2 else ""
        effect = td_list[3].get_text(strip=True) if len(td_list) > 3 else ""
        obtain = td_list[4].get_text(strip=True) if len(td_list) > 4 else ""
        obtain = obtain.replace("{$obtain}", "").strip()
        rarity = ""
        for cls in name_cell.get("class", []):
            if cls.startswith("rarity-"):
                rarity = cls.replace("rarity-", "")
                break
        if name and not name.startswith("{$"):
            items.append({
                "type": item_type,
                "name": name,
                "id": item_id,
                "image": img_src,
                "rarity": rarity,
                "effect": effect,
                "obtain": obtain
            })
    return items

def parse_achievements_table(html):
    soup = BeautifulSoup(html, "html.parser")
    table = soup.select_one("table.wiki-content-table")
    if not table:
        return []
    items = []
    for row in table.select("tr")[1:]:
        cells = row.select("td")
        if len(cells) >= 6:
            img = cells[0].select_one("img")
            a = {
                "icon": img["src"] if img else "",
                "id": cells[1].get_text(strip=True),
                "name": cells[2].get_text(strip=True),
                "description": cells[3].get_text(strip=True),
                "reward": cells[4].get_text(strip=True),
                "points": cells[5].get_text(strip=True),
                "note": cells[6].get_text(strip=True) if len(cells) > 6 else ""
            }
            if a["id"].isdigit():
                items.append(a)
    return items

def parse_companions_page(html):
    soup = BeautifulSoup(html, "html.parser")
    content = soup.select_one("#page-content")
    if not content:
        return []
    companions = []
    categories = content.select("h1")
    for cat in categories:
        section_name = cat.get_text(strip=True)
        tables = cat.find_all_next("table", class_="wiki-content-table")
        for table in tables:
            if table.find_previous_sibling("h1") and table.find_previous_sibling("h1").get_text(strip=True) != section_name:
                continue
            rows = table.select("tr")
            for i, row in enumerate(rows):
                cells = row.select("td")
                if len(cells) < 2:
                    continue
                first = cells[0].get_text(strip=True)
                if first.isdigit() or re.match(r"^\d+$", first):
                    a_tag = cells[1].select_one("a")
                    npc_name = a_tag.get_text(strip=True) if a_tag else cells[1].get_text(strip=True)
                    npc_href = a_tag.get("href", "") if a_tag else ""
                    gender = cells[2].get_text(strip=True) if len(cells) > 2 else ""
                    faction = cells[3].get_text(strip=True) if len(cells) > 3 else ""
                    notes = cells[4].get_text(strip=True) if len(cells) > 4 else ""
                    npc_id = ""
                    if npc_href:
                        m = re.search(r"npc:(\d+)", npc_href)
                        if m:
                            npc_id = m.group(1)
                    companion = {
                        "section": section_name,
                        "id": first,
                        "npc_id": npc_id,
                        "name": npc_name,
                        "gender": gender,
                        "faction": faction,
                        "notes": notes,
                    }
                    companions.append(companion)
    details = content.select("table.wiki-content-table + table.wiki-content-table")
    return companions

def parse_traits_page(html):
    soup = BeautifulSoup(html, "html.parser")
    content = soup.select_one("#page-content")
    if not content:
        return {}
    result = {}
    for h1 in content.select("h1"):
        section = h1.get_text(strip=True)
        collapsible = h1.find_next_sibling("div", class_="collapsible-block")
        if collapsible:
            inner = collapsible.select_one(".collapsible-block-content")
            if inner:
                tables = inner.select("table.wiki-content-table")
            else:
                tables = collapsible.select("table.wiki-content-table")
        else:
            tables = h1.find_all_next("table", class_="wiki-content-table")
        section_data = []
        for table in tables:
            trs = table.select("tr")
            for tr in trs[1:]:
                cells = tr.select("td")
                if len(cells) >= 3:
                    name = safe_text(cells[0])
                    effect = safe_text(cells[1])
                    obtain = safe_text(cells[2]) if len(cells) > 2 else ""
                    name = re.sub(r"\s+", " ", name).strip()
                    effect = re.sub(r"\s+", " ", effect).strip()
                    obtain = re.sub(r"\s+", " ", obtain).strip()
                    if name:
                        section_data.append({
                            "name": name,
                            "effect": effect,
                            "obtain": obtain
                        })
        if section_data:
            result[section] = section_data
    return result

def parse_generic_content(html):
    soup = BeautifulSoup(html, "html.parser")
    content = soup.select_one("#page-content")
    if not content:
        return {"text": ""}
    text = content.get_text("\n", strip=True)
    tables_data = []
    for table in content.select("table"):
        rows = table.select("tr")
        headers = [th.get_text(strip=True) for th in rows[0].select("th, td")] if rows else []
        data_rows = []
        for row in rows[1:]:
            cells = [td.get_text("\n", strip=True) for td in row.select("td")]
            if cells:
                data_rows.append(cells)
        if headers and data_rows:
            tables_data.append({"headers": headers, "rows": data_rows})
    return {"text": text, "tables": tables_data}

# ── Crawl functions ──

def crawl_codex_pages():
    codex = {
        "weapons": {"path": "/weapons"},
        "equipments": {"path": "/equipments"},
        "martial_arts": {"path": "/martial-arts"},
        "achievements": {"path": "/chengjiu"},
        "items": {"path": "/items"},
        "items_material": {"path": "/items-material"},
        "items_other": {"path": "/items-other"},
        "companions": {"path": "/huobanjieyuan"}
    }
    results = {}
    for key, info in codex.items():
        print(f"  Crawling {key} ({info['path']})...")
        html = fetch_page(info["path"])
        if not html:
            print("    -> FAILED")
            continue
        title = extract_page_name(html)
        if key in ("weapons", "equipments"):
            data = parse_weapons_table(html)
            print(f"    -> {len(data)} items")
            results[key] = {"title": title, "count": len(data), "items": data}
        elif key == "martial_arts":
            data = parse_martial_arts_table(html)
            print(f"    -> {len(data)} items")
            results[key] = {"title": title, "count": len(data), "items": data}
        elif key == "achievements":
            data = parse_achievements_table(html)
            print(f"    -> {len(data)} items")
            results[key] = {"title": title, "count": len(data), "items": data}
        elif key in ("items", "items_material", "items_other"):
            data = parse_items_table(html)
            print(f"    -> {len(data)} items")
            results[key] = {"title": title, "count": len(data), "items": data}
        elif key == "companions":
            data = parse_companions_page(html)
            print(f"    -> {len(data)} items")
            results[key] = {"title": title, "count": len(data), "items": data}
        else:
            data = parse_generic_content(html)
            results[key] = {"title": title, "data": data}
        time.sleep(1)
    return results

def crawl_traits():
    print("  Crawling traits (/traits)...")
    html = fetch_page("/traits")
    if not html:
        return {}
    title = extract_page_name(html)
    data = parse_traits_page(html)
    print(f"    -> {len(data)} sections")
    return {"title": title, "count": len(data), "sections": data}

def crawl_guide_pages():
    html = fetch_page("/start")
    if not html:
        return {}
    all_links = extract_nav_links(html)
    exclude = {
        "/start", "/weapons", "/equipments", "/martial-arts", "/items",
        "/items-material", "/items-other",
        "/huobanjieyuan", "/chengjiu", "/traits", "/canyubianji",
        "/wiki-editing", "/wiki-bug", "/bianji", "/gonglve",
        "/xinshourumen", "/diqutansuo", "/menpaishili", "/youxijieju",
        "/wuxueliupai", "/qitagonglve", "/huobanyujieyuan"
    }
    guide_links = sorted(set(all_links) - exclude)
    print(f"  Found {len(guide_links)} guide pages...")
    results = {}
    for i, path in enumerate(guide_links):
        print(f"  [{i+1}/{len(guide_links)}] {path}...", end=" ")
        html = fetch_page(path)
        if not html:
            print("FAILED")
            continue
        title = extract_page_name(html)
        data = parse_generic_content(html)
        results[path.strip("/")] = {"url": urljoin(BASE_URL, path), "title": title, "data": data}
        print(title)
        time.sleep(1)
    return results

def save_json(data, filename):
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Saved: {path}")

def main():
    print("=" * 60)
    print("HERO'S ADVENTURE WIKI CRAWLER")
    print("=" * 60)
    all_data = {}
    print("\n[1/4] Crawling codex pages...")
    codex = crawl_codex_pages()
    all_data["codex"] = codex
    save_json(codex, "codex.json")
    print("\n[2/4] Crawling traits...")
    traits = crawl_traits()
    all_data["traits"] = traits
    save_json(traits, "traits.json")
    print("\n[3/4] Crawling guide pages...")
    guides = crawl_guide_pages()
    all_data["guides"] = guides
    save_json(guides, "guides.json")
    print("\n[4/4] Writing master index...")
    save_json(all_data, "all_data.json")
    print("\nDone!")

if __name__ == "__main__":
    main()
