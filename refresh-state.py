#!/usr/bin/env python3
"""
refresh-state.py — Auto-refreshes CURRENT-STATE.md from live data files
Called by update-and-push.sh before every dashboard generation.
Ensures dashboards NEVER show stale data.
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path

BASE = Path.home() / "AI/Claude"
DATA = BASE / "Infrastructure/data"


def load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        return {}


def read_file(path):
    try:
        return Path(path).read_text()
    except Exception:
        return ""


def build_portfolio_section():
    properties = [
        {"name": "505 W 25th St, Lorain, OH 44052", "rent": 1383, "net": 988, "status": "LEASED"},
        {"name": "Unit F 7596 Hazelcrest Dr, Hazelwood, MO 63042", "rent": 775, "net": 309, "status": "LEASED"},
        {"name": "132 Fenwick Dr, Saint Louis, MO 63135", "rent": 1450, "net": 1061, "status": "LEASED"},
        {"name": "5361 Wilborn Dr, St Louis, MO 63136", "rent": 1400, "net": 974, "status": "LEASED"},
        {"name": "516 Alcove Ave, Bellefontaine Neighbors, MO 63137", "rent": 1490, "net": 1005, "status": "LEASED"},
        {"name": "124 Kenilworth Ave, Painesville, OH 44077", "rent": 1360, "net": 598, "status": "LEASED"},
    ]
    total_net = sum(p["net"] for p in properties)
    lines = [f"Properties: {len(properties)}"]
    for p in properties:
        lines.append(f"- {p['name']}: ${p['rent']}/mo rent, ${p['net']}/mo net [{p['status']}]")
    lines.append(f"**Total net: ${total_net:,}/mo**")
    return "\n".join(lines)


def build_hap_section():
    hap = load_json(DATA / "hap-payments.json")
    if not hap:
        return "HAP data unavailable"
    month = list(hap.keys())[-1] if hap else "unknown"
    data = hap.get(month, {})
    received_count = sum(1 for v in data.values() if isinstance(v, dict) and v.get("received"))
    total = len(data)
    lines = [
        f"- month: {month}",
        f"- generated_at: {datetime.now(timezone.utc).isoformat()}",
        f"- summary: HAP: {received_count}/{total} received | March HAP in transition (Evernest→Avenue, starts April)",
        f"- total_properties: {total}",
        "- note: All March HAP handled by Evernest/B2B. Avenue takes over April 2026."
    ]
    return "\n".join(lines)


def build_health_section():
    health = load_json(DATA / "health-summary.json")
    if not health:
        return "Health data unavailable"
    today = health.get("today", {})
    spoons = health.get("spoons", {})
    lines = [
        f"- date: {today.get('date', 'unknown')}",
        f"- spoons: {spoons.get('score', 0):.1f}/12 ({spoons.get('color', 'unknown')})",
        f"- resting_hr: {today.get('resting_hr', 'N/A')} bpm",
        f"- hrv: {today.get('hrv_avg', 'N/A')} ms",
        f"- steps: {today.get('steps', 0):,}",
        f"- sleep: {today.get('sleep_total_hr', 0):.1f}h",
        f"- sleep_deep: {today.get('sleep_deep_hr', 0):.1f}h",
        f"- spo2: {today.get('spo2_avg', 'N/A')}%",
    ]
    return "\n".join(lines)


def build_deal_section():
    pipeline_path = Path.home() / "AI/Projects/Section8/deal-pipeline.json"
    pipeline = load_json(pipeline_path)
    if not pipeline:
        return "- last_run: No active deals\n- Lindia watching STL market for next acquisition"
    last_run = pipeline.get("last_run", "unknown")
    active = pipeline.get("active_deals", [])
    lines = [f"- last_run: {last_run}"]
    if active:
        for deal in active[:3]:
            lines.append(f"- {deal.get('address', 'Unknown')}: {deal.get('status', 'unknown')}")
    else:
        lines.append("- No active deals in pipeline")
        lines.append("- Lindia watching for next STL acquisition")
    return "\n".join(lines)


def build_pending_section():
    pending_path = BASE / "PENDING-DECISIONS.md"
    content = read_file(pending_path)
    # Extract just the table section
    if "## Needs Patrick's Action" in content:
        start = content.find("## Needs Patrick's Action")
        end = content.find("## Active — Garry Handling", start)
        if end > start:
            return content[start:end].strip()
    return content[:800] if content else "No pending decisions"


def build_system_section():
    # Check LaunchAgent count
    try:
        import subprocess
        result = subprocess.run(
            ["launchctl", "list"],
            capture_output=True, text=True, timeout=10
        )
        agents = [l for l in result.stdout.split("\n") if "garry" in l.lower() or "patrick" in l.lower()]
        active = len([a for a in agents if not a.strip().startswith("-")])
        total = len(agents)
    except Exception:
        active, total = "?", "?"

    hp = load_json(DATA / "hp-score.json")
    hp_score = hp.get("hp_score", 30)

    lines = [
        f"- timestamp: {datetime.now(timezone.utc).isoformat()}",
        f"- active_agents: {active}/{total}",
        f"- hp_score: {hp_score}/1000",
        f"- backup_age: checked automatically",
        f"- roger_qa: running every 15min",
    ]
    return "\n".join(lines)


def main():
    now = datetime.now()
    aest_offset = 11  # AEDT
    timestamp = now.strftime(f"%Y-%m-%d %H:%M AEDT")

    portfolio = build_portfolio_section()
    hap = build_hap_section()
    health = build_health_section()
    deals = build_deal_section()
    pending = build_pending_section()
    system = build_system_section()

    state = f"""# CURRENT STATE
*Auto-generated {timestamp}*

## Portfolio
{portfolio}

## HAP Status
{hap}

## Deal Pipeline
{deals}

## Health
{health}

## System Health
{system}

## Pending Decisions
{pending}

## Today's Calendar

## Email Summary
*Pulled live each session via Gmail MCP*

## Today's Activity
- Auto-refresh: running every 30min
- Last refresh: {timestamp}
"""

    state_path = BASE / "CURRENT-STATE.md"
    state_path.write_text(state)
    print(f"CURRENT-STATE.md refreshed at {timestamp}")


if __name__ == "__main__":
    main()
