#!/usr/bin/env python3
"""
Bangkok Condo Daily Scraper — Chich, 2026-05-20
Pulls PropertyScout __NEXT_DATA__ JSON for vetted buildings.
Hard filters: Floor 8+, 54sqm+, ≤฿45k, not already added.
Scores and auto-appends new best picks to Patrick's Google Sheet.
"""

import json
import pickle
import re
import time
from datetime import datetime
from pathlib import Path

import requests
from googleapiclient.discovery import build

# ── Config ───────────────────────────────────────────────────────────────────
SPREADSHEET_ID = '1J2pMlby90eR4T9ZCiKLc0G2Pc5FWapYiIZMn-WfXdsw'
STATE_FILE     = Path.home() / 'AI/Claude/Infrastructure/bangkok-condo-state.json'
CREDS_PATH     = Path.home() / 'AI/Claude/credentials/google_full_token.pickle'
LOG_FILE       = Path.home() / 'AI/Claude/Outputs/bangkok-condo-scraper.log'

HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/124.0.0.0 Safari/537.36'
    )
}

MIN_FLOOR  = 8
MIN_SQM    = 54.0
MAX_PRICE  = 45000
MIN_SCORE  = 55  # only append if score >= this

# Add more building slugs here to expand the daily watch
BUILDINGS = [
    {
        'slug': 'ideo-mobi-sukhumvit-eastpoint',
        'name': 'Ideo Mobi Eastpoint',
        'beds': 2,
    },
]

# ── Logging ──────────────────────────────────────────────────────────────────
def log(msg):
    ts   = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, 'a') as f:
        f.write(line + '\n')

# ── State ────────────────────────────────────────────────────────────────────
def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {'seen_ids': [], 'added_count': 0, 'last_run': None}

def save_state(state):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2))

# ── Google Sheets ────────────────────────────────────────────────────────────
def get_sheets_service():
    with open(CREDS_PATH, 'rb') as f:
        creds = pickle.load(f)
    return build('sheets', 'v4', credentials=creds, cache_discovery=False)

def append_rows(service, rows):
    result = service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range='Sheet1!A1',
        valueInputOption='RAW',
        insertDataOption='INSERT_ROWS',
        body={'values': rows}
    ).execute()
    return result.get('updates', {}).get('updatedRows', 0)

# ── Floor parser — handles "7", "20+", "21-50", None ─────────────────────────
def parse_floor(raw):
    if raw is None:
        return None
    s = str(raw)
    m = re.search(r'\d+', s)
    return int(m.group()) if m else None

# ── Availability text ─────────────────────────────────────────────────────────
def avail_text(raw):
    if isinstance(raw, dict):
        return raw.get('availabilityLabelText', 'Unknown')
    return str(raw)

# ── Scoring (0–100) ──────────────────────────────────────────────────────────
def score(floor, sqm, price, avail_str):
    s = 0
    # Floor (0–30) — interpolate between 8 and 32
    s += min(30, max(0, round((floor - MIN_FLOOR) / (32 - MIN_FLOOR) * 30)))
    # SQM (0–30)
    if   sqm >= 70: s += 30
    elif sqm >= 65: s += 25
    elif sqm >= 60: s += 22
    elif sqm >= 58: s += 18
    elif sqm >= 54: s += 12
    # Price (0–25, lower = better)
    if   price <= 20000: s += 25
    elif price <= 25000: s += 20
    elif price <= 28000: s += 17
    elif price <= 30000: s += 14
    elif price <= 35000: s += 10
    elif price <= 40000: s +=  5
    # Availability (0–15)
    av = avail_str.lower()
    if any(k in av for k in ['confirmed', 'days ago', 'weeks ago', 'month ago']):
        s += 15
    elif any(k in av for k in ['upon request']):
        s += 10
    elif any(k in av for k in ['aug 2026', 'jul 2026', 'jun 2026']):
        s +=  8
    elif 'rented until' in av:
        s +=  2
    else:
        s +=  5
    return s

# ── Scraper ──────────────────────────────────────────────────────────────────
def scrape_building(building):
    url = (
        f"https://propertyscout.co.th/en/bangkok/condo/{building['slug']}/"
        f"rentals/{building['beds']}-bedrooms/"
    )
    log(f"Fetching {url}")
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
    except Exception as e:
        log(f"  FETCH ERROR: {e}")
        return []

    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', resp.text, re.DOTALL)
    if not m:
        log("  ERROR: no __NEXT_DATA__ found")
        return []

    try:
        data     = json.loads(m.group(1))
        rentals  = data['props']['pageProps']['rentals']['data']
    except Exception as e:
        log(f"  JSON parse error: {e}")
        return []

    listings = []
    for r in rentals:
        lid   = r.get('id')
        floor = parse_floor(r.get('floorLevel'))
        sqm   = r.get('floorSize')
        price = r.get('lowestPrice')
        avail = avail_text(r.get('availabilitySubClusterEn', ''))
        title = r.get('title', {})
        std   = title.get('standard', '') if isinstance(title, dict) else str(title)
        slug  = re.sub(r'[^a-z0-9]+', '-', std.lower()).strip('-')
        url   = f"https://propertyscout.co.th/en/{slug}-{lid}/"

        if lid and floor is not None and sqm and price:
            listings.append({
                'id':       lid,
                'building': building['name'],
                'beds':     building['beds'],
                'floor':    floor,
                'sqm':      float(sqm),
                'price':    int(price),
                'available': avail,
                'url':      url,
            })

    log(f"  Parsed {len(listings)} listings")
    return listings

# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    log("=== Bangkok condo scraper start ===")
    state   = load_state()
    service = get_sheets_service()
    seen    = set(str(i) for i in state.get('seen_ids', []))
    to_add  = []

    for building in BUILDINGS:
        raw = scrape_building(building)
        time.sleep(2)

        for l in raw:
            lid = str(l['id'])

            # Hard filters
            if l['floor'] < MIN_FLOOR:  continue
            if l['sqm']   < MIN_SQM:    continue
            if l['price'] > MAX_PRICE:  continue
            if lid in seen:             continue  # already processed

            s = score(l['floor'], l['sqm'], l['price'], l['available'])
            l['score'] = s
            log(f"  NEW: Floor {l['floor']} | {l['sqm']}sqm | ฿{l['price']:,} | {l['available'][:30]} | score {s}")

            if s >= MIN_SCORE:
                to_add.append(l)

            seen.add(lid)

    to_add.sort(key=lambda x: x['score'], reverse=True)

    if to_add:
        rows = [
            [
                l['building'],
                f"{l['beds']}/1",
                str(int(l['sqm'])),
                str(l['floor']),
                f"{l['price']:,}",
                l['available'],
                f"auto {l['score']}/100",
                l['url'],
            ]
            for l in to_add
        ]
        added = append_rows(service, rows)
        log(f"Sheet updated: +{added} rows")
        state['added_count'] = state.get('added_count', 0) + added
    else:
        log("No new qualifying listings today.")

    state['seen_ids'] = list(seen)
    state['last_run'] = datetime.now().isoformat()
    save_state(state)
    log(f"=== Done. Total ever added: {state.get('added_count', 0)} ===")

if __name__ == '__main__':
    main()
