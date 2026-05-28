#!/usr/bin/env python3
"""
sync-data.py — Garry Dashboard Data Sync
Single source of truth for deals-data.json and portfolio-data.json.

Runs as part of update-and-push.sh pipeline.

Reads from authoritative sources:
  - ~/AI/Claude/Infrastructure/data/warm-deals.json   → deals warm leads
  - ~/AI/Claude/Infrastructure/data/deal-finder-v4-results.json → fresh picks
  - ~/AI/Claude/Infrastructure/data/portfolio-v2.json  → property statuses

Writes:
  - deals-data.json   (in this folder, pushed to GitHub Pages)
  - portfolio-data.json (in this folder, pushed to GitHub Pages)
"""

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

DIR = Path(__file__).parent
DATA = Path.home() / "AI/Claude/Infrastructure/data"


def load(path):
    try:
        return json.loads(Path(path).read_text())
    except Exception:
        return {}


def zillow_url(address):
    """Generate Zillow URL from address string like '6814 Frostview Ln, Saint Louis, MO, 63134'"""
    parts = [p.strip() for p in address.split(",")]
    if len(parts) >= 4:
        street = parts[0].replace(" ", "-")
        city = parts[1].replace(" ", "-")
        state = parts[2].strip()
        zipcode = parts[3].strip()
        return f"https://www.zillow.com/homes/{street}--{city}--{state}--{zipcode}_rb/"
    return ""


def sync_deals():
    """Build deals-data.json from warm-deals.json + deal-finder results."""
    warm_raw = load(DATA / "warm-deals.json")
    finder_raw = load(DATA / "deal-finder-v4-results.json")

    # ── 1. Under contract ──
    under_contract = [
        {
            "address": "1020 Farmview Drive, Unincorporated, MO 63138",
            "tier": "under_contract",
            "price": 97000,
            "bedrooms": 4,
            "fmr": 1710,
            "projected_cf": 530,
            "cap_rate": 13.4,
            "coc_pct": 29.7,
            "dscr": 1.96,
            "garry_score": 88.0,
            "inspection_date": "2026-06-02",
            "closing_date": "2026-06-22",
            "note": "Inspection June 2 (Evergreen — general + septic). Earnest $1K paid ✅. Closing June 22.",
            "ai_summary": "4BR in 63138. Accepted $97K. DSCR 1.96, CF $530/mo. Septic inspection required.",
            "zillow_url": "https://www.zillow.com/homes/1020-Farmview-Dr--Unincorporated--MO--63138_rb/",
            "s8pro_url": "",
        }
    ]

    # ── 2. Warm deals from warm-deals.json ──
    warm_deals = []
    for wd in warm_raw.get("warm_deals", []):
        addr = wd.get("address", "")
        entry = {
            "address": addr,
            "status": wd.get("status", "warm_lead"),
            "cf_mo": wd.get("cf_mo", 0),
            "score": wd.get("score", 0),
            "beds": wd.get("beds", 3),
            "price": wd.get("price", 0),
            "fmr": wd.get("fmr", 0),
            "offer": wd.get("offer", ""),
            "added": wd.get("added", ""),
            "zillow_url": wd.get("zillow_url") or zillow_url(addr),
            "s8pro_url": wd.get("s8pro_url", ""),
        }
        warm_deals.append(entry)

    # ── 3. Fresh deal-finder picks (top 6, exclude under-contract addresses) ──
    exclude_addrs = {d["address"].lower() for d in under_contract}
    warm_addrs = {d["address"].lower() for d in warm_deals}
    exclude_all = exclude_addrs | warm_addrs

    top_props = finder_raw.get("top_properties", [])
    fresh_deals = []
    for p in top_props:
        if p.get("address", "").lower() in exclude_all:
            continue
        ai_data = p.get("ai_analysis") or {}
        ai_scores = ai_data.get("scores") or p.get("ai_scores") or {}
        ai_summary = (
            ai_data.get("summary")
            or p.get("ai_summary")
            or ""
        )
        fresh_deals.append({
            "address": p.get("address", ""),
            "price": p.get("price", 0),
            "bedrooms": p.get("bedrooms", 0),
            "fmr": p.get("fmr", 0),
            "cashflow": p.get("cashflow", 0),
            "projected_cf": p.get("projected_cf", 0),
            "cap_rate": p.get("cap_rate", 0),
            "coc_pct": p.get("coc_pct", 0),
            "dscr": p.get("dscr", 0),
            "garry_score": p.get("garry_score", 0),
            "hqs_score": p.get("hqs_score", 0),
            "crime_score": p.get("crime_score", 0),
            "in_avenue_zip": p.get("in_avenue_zip", False),
            "dscr_eligible": p.get("dscr_eligible", False),
            "ai_summary": ai_summary[:300] if ai_summary else "",
            "ai_scores": ai_scores,
            "zillow_url": p.get("zillow_url", ""),
            "s8pro_url": p.get("url", ""),
            "scraped_at": p.get("scraped_at", ""),
        })
        if len(fresh_deals) >= 8:
            break

    # ── 4. Build output ──
    deals_out = {
        "generated": datetime.now(timezone.utc).isoformat(),
        "total_found": len(fresh_deals),
        "deals": under_contract + fresh_deals,
        "warm_deals": warm_deals,
    }

    out_path = DIR / "deals-data.json"
    out_path.write_text(json.dumps(deals_out, indent=2))
    print(f"[sync-data] deals-data.json: {len(under_contract)} contract + {len(warm_deals)} warm + {len(fresh_deals)} fresh")


def sync_portfolio():
    """Build portfolio-data.json from portfolio-v2.json + known overrides for live issues."""
    pv2 = load(DATA / "portfolio-v2.json")
    existing = load(DIR / "portfolio-data.json")

    USD_AUD = 1.58

    # Status overrides — these reflect ACTUAL current state from THREADS.md
    # Update this dict when property status changes (Garry maintains it)
    STATUS_OVERRIDES = {
        "505 W 25th": {
            "status": "critical",
            "status_label": "HAP Abated",
            "gross_rent": 0,
            "net_income": 0,
            "issues": ["HAP abatement — reinspection May 27 result pending"],
            "status_note": "HAP abatement since Oct 2025. Reinspection May 27 1pm. Result pending.",
        },
        "5361 Wilborn": {
            "status": "zero",
            "status_label": "Vacant — Listed",
            "gross_rent": 0,
            "net_income": 0,
            "issues": ["Vacant — listed $1,420/mo S8", "7 contractors sourced for punch list"],
            "status_note": "Vacant. Listed $1,420/mo. Rehab in progress.",
        },
        "124 Kenilworth": {
            "status": "critical",
            "status_label": "Non-Paying",
            "gross_rent": 0,
            "net_income": 0,
            "issues": ["$903 outstanding — May rent + late fee", "Lease expires Jul 31, 2026"],
            "status_note": "Non-paying. $903 outstanding. Lease Jul 31.",
        },
    }

    properties = existing.get("properties", [])

    def match_override(short_addr):
        for key, override in STATUS_OVERRIDES.items():
            if key.lower() in short_addr.lower():
                return override
        return None

    updated_props = []
    for prop in properties:
        short = prop.get("short", "")
        override = match_override(short)
        if override:
            prop.update(override)
        updated_props.append(prop)

    # Recalculate summary
    active_net = sum(
        p.get("net_income", 0)
        for p in updated_props
        if p.get("status") not in ("forsale",)
    )
    goal = 20000 / USD_AUD  # $20K AUD in USD

    summary = existing.get("summary", {})
    summary["net_monthly"] = active_net
    summary["gross_monthly"] = sum(p.get("gross_rent", 0) for p in updated_props)
    summary["progress_pct"] = round((active_net / goal) * 100, 1) if goal else 0
    summary["last_updated"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    out = dict(existing)
    out["properties"] = updated_props
    out["summary"] = summary
    out["generated"] = datetime.now(timezone.utc).isoformat()

    out_path = DIR / "portfolio-data.json"
    out_path.write_text(json.dumps(out, indent=2))
    print(f"[sync-data] portfolio-data.json: {len(updated_props)} properties, net ${active_net}/mo USD")


if __name__ == "__main__":
    sync_deals()
    sync_portfolio()
    print("[sync-data] Done.")
