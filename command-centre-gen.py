#!/usr/bin/env python3
"""
command-centre-gen.py — Elite Command Centre renderer.

Replaces the Command Centre block in generate.py. Reads:
  data/portfolio-v2.json  (+ lease windows injected by extras)
  data/hap-payments.json
  data/active-deals.json
  data/threads-active.json
  data/pending-decisions.json
  data/capital.json
  data/bangkok.json
  data/fx-rate.json
  data/recent-wins.json
  ~/AI/Projects/Section8/deal-pipeline.json  (watchlist)

Writes:
  garry-dashboards/command-centre.html
  garry-live/command-centre.html
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path

BASE = Path.home() / "AI/Claude"
DATA = BASE / "Infrastructure/data"
OUT_PAGES = BASE / "Infrastructure/garry-dashboards/command-centre.html"
OUT_LOCAL = BASE / "Infrastructure/garry-live/command-centre.html"
PIPELINE_JSON = Path.home() / "AI/Projects/Section8/deal-pipeline.json"


def load(name, default=None):
    p = DATA / name
    if not p.exists():
        return default if default is not None else {}
    try:
        return json.loads(p.read_text())
    except Exception:
        return default if default is not None else {}


def load_file(path, default=None):
    p = Path(path)
    if not p.exists():
        return default if default is not None else {}
    try:
        return json.loads(p.read_text())
    except Exception:
        return default if default is not None else {}


def render():
    fx = load("fx-rate.json", {"usd_to_aud": 1.58, "stale": True})
    portfolio = load("portfolio-v2.json", {"properties": [], "totals": {}})
    hap = load("hap-payments.json", {})
    active_deals = load("active-deals.json", {"deals": []})
    threads = load("threads-active.json", {"threads": []})
    pending = load("pending-decisions.json", {"needs_patrick": [], "waiting_on": []})
    capital = load("capital.json", {})
    bangkok = load("bangkok.json", {})
    wins = load("recent-wins.json", {"wins": []})

    usd_to_aud = fx.get("usd_to_aud", 1.58)
    fx_stale = fx.get("stale", False)

    now = datetime.now()
    now_str = now.strftime("%a %b %d %Y · %I:%M %p").replace(" 0", " ")

    # ── Portfolio ──
    properties = portfolio.get("properties", [])
    total_net_usd = portfolio.get("totals", {}).get("net_monthly", 4935)
    aud_income = round(total_net_usd * usd_to_aud)
    aud_goal = 20000
    pct = round(aud_income / aud_goal * 100)
    doors = len(properties) or 6
    gap_aud = aud_goal - aud_income

    # ── HAP current month ──
    ym = now.strftime("%Y-%m")
    hap_month = {k: v for k, v in hap.get(ym, {}).items() if isinstance(v, dict)}
    hap_received = sum(1 for v in hap_month.values() if v.get("status") == "RECEIVED")
    hap_total = len(hap_month) or 6

    # ── Active deals ──
    deals = active_deals.get("deals", [])

    # ── Deal Pipeline (watchlist from deal-pipeline.json + active-deals stages) ──
    pipeline_raw = load_file(PIPELINE_JSON, {})
    watchlist_raw = pipeline_raw.get("watchlist", [])
    # Build unified pipeline stages from active-deals + watchlist
    pipeline_under_contract = [d for d in deals if d.get("status", "").upper() in ("UNDER CONTRACT", "CONTRACT SIGNED")]
    pipeline_offer_submitted = [d for d in deals if d.get("status", "").upper() in ("OFFER SUBMITTED", "INSPECTION IN PROGRESS", "INSPECTION PAID")]
    pipeline_watchlist = watchlist_raw

    # ── Needs Patrick ──
    needs = pending.get("needs_patrick", [])[:3]
    waiting = pending.get("waiting_on", [])[:5]

    # ── Threads ──
    active_threads = threads.get("threads", [])[:4]

    # ── Capital ──
    cap_working = capital.get("working_capital_usd", 180000)
    cap_total = capital.get("total_deployable_usd", 205000)

    # ── Bangkok ──
    bk_days = bangkok.get("days_until", 0)
    bk_status = bangkok.get("status", "PLANNED")

    # ── Recent wins ──
    recent = wins.get("wins", [])[:5]

    # ── Phase ──
    phase_label = "ACQUISITION PHASE"
    phase_sub = f"272 Elmdale under contract · {doors}/16 doors to next milestone · Bangkok in {bk_days}d" if bk_days > 0 else f"272 Elmdale under contract · {doors}/16 doors to next milestone"

    # ════════════ DEAL CARDS ════════════
    deal_cards = ""
    for d in deals:
        badge_bg = {"red": "rgba(248,113,113,0.12)", "orange": "rgba(251,146,60,0.12)", "green": "rgba(52,211,153,0.12)"}.get(
            d.get("badge_color", "orange"), "rgba(251,146,60,0.12)"
        )
        badge_color = {"red": "#f87171", "orange": "#fb923c", "green": "#34d399"}.get(d.get("badge_color", "orange"), "#fb923c")
        lenders_str = " · ".join(f"{l['name']} {l['status'].replace('PRE-APPROVED','✓').replace('PENDING','⋯')}" for l in d.get("lenders", []))
        deal_cards += f"""
<div class="deal-card">
  <div class="deal-head">
    <div class="deal-addr">{d['name']} <span class="deal-sub">· {d.get('address','')}</span></div>
    <div class="deal-badge" style="background:{badge_bg};color:{badge_color}">{d.get('badge','')} · {d.get('status','')}</div>
  </div>
  <div class="deal-line">
    <span class="deal-k">Price</span><span class="deal-v">${(d.get('price') or 0):,}</span>
    <span class="deal-k">FMR</span><span class="deal-v">${(d.get('fmr') or 0):,}</span>
    <span class="deal-k">Target rent</span><span class="deal-v">${(d.get('retenant_target') or 0):,}</span>
    <span class="deal-k">CF (opt)</span><span class="deal-v">${(d.get('optimised_cf_per_month') or 0):,}/mo</span>
  </div>
  <div class="deal-stage">Stage: <b>{d.get('stage','')}</b> · Close target: {d.get('close_target','')} · T-{d.get('days_to_close','?')}d</div>
  <div class="deal-lenders">{lenders_str}</div>
  <div class="deal-action">Next: {d.get('next_action','')}</div>
</div>"""
    if not deal_cards:
        deal_cards = '<div class="empty">No active deals — Lindia watching 63135/36/37</div>'

    # ════════════ DEAL PIPELINE ════════════
    def pipeline_stage_badge(label, color_var, count):
        return f'<div class="pipe-stage-label" style="color:{color_var}">{label} <span class="pipe-count">{count}</span></div>'

    def pipeline_contract_row(d):
        close_target = d.get("close_target", "TBD")
        signed = d.get("signed_date", "")
        notes = d.get("notes", "")
        # Inspection window: 10 days from signed date
        insp_note = ""
        if signed:
            try:
                from datetime import timedelta
                sd = datetime.strptime(signed, "%Y-%m-%d")
                insp_end = sd + timedelta(days=10)
                days_left = (insp_end - datetime.now()).days
                insp_note = f' · Inspection window: {"OPEN" if days_left >= 0 else "CLOSED"} ({max(0,days_left)}d left)'
            except Exception:
                pass
        return f"""<div class="pipe-row pipe-contract">
  <div class="pipe-row-top">
    <div class="pipe-addr">{d.get('name','')}</div>
    <div class="pipe-price">${(d.get('price') or 0):,}</div>
  </div>
  <div class="pipe-meta">Close: {close_target}{insp_note}</div>
  <div class="pipe-next">Next: {d.get('next_action','')}</div>
  {f'<div class="pipe-note">{notes[:140]}</div>' if notes else ''}
</div>"""

    def pipeline_offer_row(d):
        return f"""<div class="pipe-row pipe-offer">
  <div class="pipe-row-top">
    <div class="pipe-addr">{d.get('name','')}</div>
    <div class="pipe-price">${(d.get('price') or 0):,}</div>
  </div>
  <div class="pipe-meta">Stage: {d.get('stage','')}</div>
  <div class="pipe-next">Next: {d.get('next_action','')}</div>
</div>"""

    def pipeline_watchlist_row(w):
        addr = w.get("address", "").split(",")[0]
        asking = w.get("asking", 0)
        beds = w.get("beds", "?")
        status_detail = w.get("status_detail", "")
        pros = w.get("pros", "")
        cons = w.get("cons", "")
        min_rent = w.get("minimum_rent_needed")
        notes = w.get("notes", "")
        min_rent_str = f' · Min rent needed: ${min_rent:,}/mo' if min_rent else ''
        return f"""<div class="pipe-row pipe-watch">
  <div class="pipe-row-top">
    <div class="pipe-addr">{addr}</div>
    <div class="pipe-price">${asking:,} · {beds}BR</div>
  </div>
  {f'<div class="pipe-pros">+ {pros[:120]}</div>' if pros else ''}
  {f'<div class="pipe-cons">- {cons[:120]}</div>' if cons else ''}
  {f'<div class="pipe-meta">{status_detail}{min_rent_str}</div>' if status_detail or min_rent else ''}
  {f'<div class="pipe-note">{notes[:120]}</div>' if notes else ''}
</div>"""

    pipeline_html = ""
    # Under Contract
    pipeline_html += pipeline_stage_badge("UNDER CONTRACT", "var(--green)", len(pipeline_under_contract))
    if pipeline_under_contract:
        for d in pipeline_under_contract:
            pipeline_html += pipeline_contract_row(d)
    else:
        pipeline_html += '<div class="pipe-empty">Nothing under contract</div>'

    # Offer Submitted / Inspection
    pipeline_html += pipeline_stage_badge("OFFER SUBMITTED / INSPECTION", "var(--orange)", len(pipeline_offer_submitted))
    if pipeline_offer_submitted:
        for d in pipeline_offer_submitted:
            pipeline_html += pipeline_offer_row(d)
    else:
        pipeline_html += '<div class="pipe-empty">No active offers</div>'

    # Watchlist
    pipeline_html += pipeline_stage_badge("WATCHLIST", "var(--blue)", len(pipeline_watchlist))
    if pipeline_watchlist:
        for w in pipeline_watchlist:
            pipeline_html += pipeline_watchlist_row(w)
    else:
        pipeline_html += '<div class="pipe-empty">Watchlist clear</div>'

    # ════════════ NEEDS PATRICK ════════════
    needs_cards = ""
    for n in needs:
        needs_cards += f"""
<div class="need-card">
  <div class="need-num">#{n['num']}</div>
  <div class="need-body">
    <div class="need-title">{n['title']}</div>
    <div class="need-ctx">{n['context'][:140]}</div>
  </div>
</div>"""
    if not needs_cards:
        needs_cards = '<div class="empty-good">All clear. Nothing needs you right now.</div>'

    # ════════════ WAITING ON ════════════
    waiting_rows = ""
    for w in waiting:
        waiting_rows += f"""
<div class="wait-row">
  <div class="wait-item">{w['item']}</div>
  <div class="wait-from">{w['from']}</div>
</div>"""

    # ════════════ PORTFOLIO ────── with lease windows ────
    prop_tiles = ""
    for p in properties:
        net = p.get("rent_net", 0)
        aud = round(net * usd_to_aud)
        addr_short = p.get("address", "").split(",")[0]
        grade = p.get("grade", "?")
        months_left = p.get("months_to_lease_end")
        retenant_gap = (p.get("retenant_target", 0) or 0) - (p.get("current_gross", 0) or 0)
        grade_color = {"A": "#34d399", "B": "#fbbf24", "C": "#f87171", "SELL": "#f87171"}.get(grade, "#5a5a64")
        retenant_line = (
            f'<div class="prop-retenant">+${retenant_gap}/mo at re-tenant · {months_left}mo left</div>'
            if months_left is not None and retenant_gap > 0
            else f'<div class="prop-retenant" style="color:#f87171">SELLING</div>'
            if grade == "SELL"
            else ""
        )
        prop_tiles += f"""
<div class="prop-tile">
  <div class="prop-top">
    <div class="prop-net">A${aud:,}</div>
    <div class="prop-grade" style="color:{grade_color}">{grade}</div>
  </div>
  <div class="prop-addr">{addr_short}</div>
  {retenant_line}
</div>"""

    # ════════════ HAP GRID ════════════
    hap_tiles = ""
    for key, v in hap_month.items():
        status = v.get("status", "PENDING")
        expected = v.get("expected", 0)
        name = v.get("property", key).split(",")[0].split(" ")[-1][:10]
        color = {"RECEIVED": "#34d399", "PENDING": "#fbbf24", "LATE": "#f87171", "EVERNEST_TRANSITION": "#5a5a64"}.get(status, "#fbbf24")
        hap_tiles += f"""
<div class="hap-tile">
  <div class="hap-name">{name}</div>
  <div class="hap-amt" style="color:{color}">${expected}</div>
  <div class="hap-status" style="color:{color}">{status[:10]}</div>
</div>"""
    if not hap_tiles:
        hap_tiles = '<div class="empty">HAP data pending</div>'

    # ════════════ THREADS ════════════
    thread_rows = ""
    for t in active_threads:
        thread_rows += f"""
<div class="thread-row">
  <div class="thread-name">🔥 {t['name']}</div>
  <div class="thread-status">{t['status_text'][:110]}</div>
</div>"""
    if not thread_rows:
        thread_rows = '<div class="empty">No active threads</div>'

    # ════════════ RECENT WINS ════════════
    wins_rows = ""
    for w in recent:
        wins_rows += f'<div class="win-row">✓ {w.get("line","")[:100]}</div>'
    if not wins_rows:
        wins_rows = '<div class="empty">Building win cache...</div>'

    # ════════════ FRESHNESS ════════════
    fx_badge = (
        f'<span style="color:#fbbf24">● FX stale</span>'
        if fx_stale
        else f'<span style="color:#34d399">● FX live</span>'
    )

    # Data age heartbeat
    portfolio_mtime = (DATA / "portfolio-v2.json").stat().st_mtime if (DATA / "portfolio-v2.json").exists() else 0
    age_min = int((now.timestamp() - portfolio_mtime) / 60) if portfolio_mtime else 999
    heartbeat_color = "#34d399" if age_min < 35 else "#fbbf24" if age_min < 90 else "#f87171"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<meta http-equiv="refresh" content="300">
<meta http-equiv="cache-control" content="no-cache, no-store, must-revalidate">
<title>Command Centre · Patrick</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
:root{{--bg:#050508;--surface:#0c0c10;--surface-2:#141418;--border:#18181c;--border-2:#24242a;
  --text:#f0f0f2;--sub:#a0a0a8;--dim:#5a5a64;
  --green:#34d399;--gold:#daa520;--red:#f87171;--orange:#fb923c;--blue:#60a5fa}}
body{{background:var(--bg);color:var(--text);font-family:'SF Pro Display',-apple-system,BlinkMacSystemFont,system-ui,sans-serif;
  -webkit-font-smoothing:antialiased;min-height:100vh;padding:env(safe-area-inset-top) 18px 40px}}
.wrap{{max-width:560px;margin:0 auto}}

/* PHASE HERO */
.phase-hero{{background:linear-gradient(135deg,rgba(52,211,153,0.08),rgba(96,165,250,0.05));
  border:1px solid rgba(52,211,153,0.15);border-radius:18px;padding:22px;margin:24px 0 20px}}
.phase-label{{font-size:10px;letter-spacing:3px;color:var(--green);font-weight:700;text-transform:uppercase}}
.phase-title{{font-size:22px;font-weight:800;margin-top:6px;letter-spacing:-0.5px}}
.phase-sub{{font-size:12px;color:var(--sub);margin-top:8px;line-height:1.5}}

/* HERO GRID */
.hero-grid{{display:grid;grid-template-columns:2fr 1fr;gap:12px;margin-bottom:20px}}
.hero-main{{background:var(--surface);border:1px solid var(--border);border-radius:16px;padding:20px;text-align:center}}
.hero-num{{font-size:44px;font-weight:800;line-height:1;letter-spacing:-1.5px}}
.hero-num .cur{{font-size:20px;color:var(--gold);vertical-align:top;margin-right:3px}}
.hero-goal{{font-size:11px;color:var(--dim);margin-top:4px}}
.hero-bar{{width:100%;height:6px;background:#151518;border-radius:3px;margin-top:14px;overflow:hidden}}
.hero-fill{{height:100%;background:linear-gradient(90deg,var(--gold),#f0c040);border-radius:3px}}
.hero-pct{{font-size:11px;color:var(--gold);margin-top:6px;font-weight:700}}
.hero-side{{display:flex;flex-direction:column;gap:10px}}
.side-tile{{background:var(--surface);border:1px solid var(--border);border-radius:14px;padding:14px;text-align:center;flex:1}}
.side-v{{font-size:20px;font-weight:800}}
.side-l{{font-size:9px;color:var(--dim);text-transform:uppercase;letter-spacing:1.2px;margin-top:3px}}

/* SECTIONS */
.sec{{margin-bottom:28px}}
.sec-title{{font-size:10px;letter-spacing:2.5px;text-transform:uppercase;color:var(--dim);font-weight:700;margin-bottom:12px;display:flex;justify-content:space-between}}
.sec-title .badge{{font-size:10px;background:rgba(251,146,60,0.1);color:var(--orange);padding:2px 8px;border-radius:10px;letter-spacing:0.5px}}

/* DEAL CARD */
.deal-card{{background:var(--surface);border:1px solid var(--border);border-radius:14px;padding:18px;margin-bottom:12px}}
.deal-head{{display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;gap:10px}}
.deal-addr{{font-size:16px;font-weight:700}}
.deal-sub{{font-size:11px;color:var(--sub);font-weight:400}}
.deal-badge{{font-size:9px;font-weight:700;padding:4px 10px;border-radius:10px;letter-spacing:0.5px;white-space:nowrap}}
.deal-line{{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;font-size:11px;margin-bottom:10px}}
.deal-k{{color:var(--dim);font-size:9px;text-transform:uppercase;letter-spacing:0.8px}}
.deal-v{{color:var(--text);font-weight:700;font-size:13px;margin-bottom:4px}}
.deal-stage{{font-size:11px;color:var(--sub);padding:8px 0;border-top:1px solid var(--border)}}
.deal-lenders{{font-size:11px;color:var(--sub);padding-top:6px}}
.deal-action{{font-size:12px;color:var(--gold);font-weight:500;margin-top:8px}}

/* NEEDS */
.need-card{{display:flex;background:var(--surface);border:1px solid var(--border);border-left:3px solid var(--orange);border-radius:12px;padding:14px;margin-bottom:10px}}
.need-num{{font-size:22px;font-weight:800;color:var(--orange);margin-right:14px;min-width:26px}}
.need-body{{flex:1}}
.need-title{{font-size:14px;font-weight:600;margin-bottom:4px}}
.need-ctx{{font-size:11px;color:var(--sub);line-height:1.5}}
.empty-good{{background:var(--surface);border:1px solid rgba(52,211,153,0.15);border-radius:12px;padding:18px;text-align:center;color:var(--green);font-size:13px}}
.empty{{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:18px;text-align:center;color:var(--dim);font-size:12px}}

/* WAITING */
.wait-row{{display:flex;justify-content:space-between;background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:10px 14px;margin-bottom:6px;font-size:12px}}
.wait-item{{color:var(--text);font-weight:500;flex:1}}
.wait-from{{color:var(--dim);font-size:11px}}

/* PORTFOLIO */
.props{{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}}
.prop-tile{{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:12px}}
.prop-top{{display:flex;justify-content:space-between;align-items:center}}
.prop-net{{font-size:16px;font-weight:800;color:var(--green)}}
.prop-grade{{font-size:10px;font-weight:800;padding:1px 6px;border-radius:4px;background:rgba(255,255,255,0.05)}}
.prop-addr{{font-size:10px;color:var(--sub);margin-top:6px;line-height:1.3}}
.prop-retenant{{font-size:9px;color:var(--orange);margin-top:4px}}

/* HAP */
.hap-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:6px}}
.hap-tile{{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:10px;text-align:center}}
.hap-name{{font-size:10px;color:var(--dim)}}
.hap-amt{{font-size:14px;font-weight:700;margin-top:4px}}
.hap-status{{font-size:8px;margin-top:3px;text-transform:uppercase;letter-spacing:0.5px}}

/* THREADS */
.thread-row{{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:12px;margin-bottom:6px}}
.thread-name{{font-size:13px;font-weight:600}}
.thread-status{{font-size:11px;color:var(--sub);margin-top:4px;line-height:1.4}}

/* PIPELINE */
.pipe-stage-label{{font-size:10px;letter-spacing:1.5px;text-transform:uppercase;font-weight:700;margin:14px 0 6px 2px}}
.pipe-count{{background:rgba(255,255,255,0.07);border-radius:8px;padding:1px 7px;font-size:10px;margin-left:4px}}
.pipe-row{{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:14px;margin-bottom:8px}}
.pipe-contract{{border-left:3px solid var(--green)}}
.pipe-offer{{border-left:3px solid var(--orange)}}
.pipe-watch{{border-left:3px solid var(--blue)}}
.pipe-row-top{{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:6px}}
.pipe-addr{{font-size:15px;font-weight:700;color:var(--text)}}
.pipe-price{{font-size:12px;color:var(--gold);font-weight:600}}
.pipe-meta{{font-size:11px;color:var(--sub);margin-bottom:4px}}
.pipe-next{{font-size:12px;color:var(--gold);font-weight:500}}
.pipe-pros{{font-size:11px;color:var(--green);margin-bottom:2px;line-height:1.4}}
.pipe-cons{{font-size:11px;color:var(--red);margin-bottom:4px;line-height:1.4}}
.pipe-note{{font-size:10px;color:var(--dim);margin-top:6px;font-style:italic;line-height:1.4}}
.pipe-empty{{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:10px 14px;font-size:11px;color:var(--dim);text-align:center;margin-bottom:8px}}

/* WINS */
.win-row{{font-size:11px;color:var(--sub);padding:6px 0;border-bottom:1px solid var(--border);line-height:1.4}}

/* FOOTER */
.foot{{text-align:center;font-size:10px;color:var(--dim);margin-top:24px;letter-spacing:0.8px;line-height:1.6}}
.dot{{display:inline-block;width:6px;height:6px;border-radius:50%;margin:0 4px;vertical-align:middle}}
@media(max-width:540px){{
  .hero-grid{{grid-template-columns:1fr}}
  .props,.deal-line{{grid-template-columns:repeat(2,1fr)}}
}}
</style>
</head>
<body>
<div class="wrap">

<!-- PHASE HERO -->
<div class="phase-hero">
  <div class="phase-label">Current Phase</div>
  <div class="phase-title">{phase_label}</div>
  <div class="phase-sub">{phase_sub}</div>
</div>

<!-- HERO NUMBERS -->
<div class="hero-grid">
  <div class="hero-main">
    <div class="hero-num"><span class="cur">A$</span>{aud_income:,}</div>
    <div class="hero-goal">of A${aud_goal:,}/mo · North Star</div>
    <div class="hero-bar"><div class="hero-fill" style="width:{min(pct,100)}%"></div></div>
    <div class="hero-pct">{pct}% · Gap A${gap_aud:,}/mo</div>
  </div>
  <div class="hero-side">
    <div class="side-tile">
      <div class="side-v" style="color:var(--green)">${cap_working//1000}K</div>
      <div class="side-l">Deployable USD</div>
    </div>
    <div class="side-tile">
      <div class="side-v" style="color:var(--blue)">{bk_days}d</div>
      <div class="side-l">Bangkok</div>
    </div>
  </div>
</div>

<!-- NEEDS PATRICK -->
<div class="sec">
  <div class="sec-title">Needs Patrick {f'<span class="badge">{len(needs)} open</span>' if needs else ''}</div>
  {needs_cards}
</div>

<!-- DEAL PIPELINE -->
<div class="sec">
  <div class="sec-title">Deal Pipeline <span class="badge" style="background:rgba(96,165,250,0.1);color:var(--blue)">{len(pipeline_under_contract)} contract · {len(pipeline_offer_submitted)} offer · {len(pipeline_watchlist)} watch</span></div>
  {pipeline_html}
</div>

<!-- ACTIVE DEALS -->
<div class="sec">
  <div class="sec-title">Active Deals {f'<span class="badge" style="background:rgba(248,113,113,0.1);color:var(--red)">{len(deals)} HOT</span>' if deals else ''}</div>
  {deal_cards}
</div>

<!-- ACTIVE THREADS -->
<div class="sec">
  <div class="sec-title">Active Workstreams · {len(active_threads)}</div>
  {thread_rows}
</div>

<!-- WAITING ON -->
<div class="sec">
  <div class="sec-title">Waiting On · {len(waiting)} items</div>
  {waiting_rows if waiting_rows else '<div class="empty">No outbound asks pending</div>'}
</div>

<!-- PORTFOLIO -->
<div class="sec">
  <div class="sec-title">Portfolio · {doors} doors · re-tenant windows</div>
  <div class="props">{prop_tiles}</div>
</div>

<!-- HAP -->
<div class="sec">
  <div class="sec-title">HAP {ym} · {hap_received}/{hap_total}</div>
  <div class="hap-grid">{hap_tiles}</div>
</div>

<!-- WINS -->
<div class="sec">
  <div class="sec-title">Recent Wins · 48h</div>
  {wins_rows}
</div>

<!-- FOOTER -->
<div class="foot">
  Auto-updated {now_str} · 1 USD = {usd_to_aud:.4f} AUD<br>
  <span class="dot" style="background:{heartbeat_color}"></span>Data {age_min}min old ·
  {fx_badge} ·
  <span style="color:var(--dim)">Garry 24/7</span>
</div>

</div>
</body>
</html>"""

    OUT_PAGES.parent.mkdir(parents=True, exist_ok=True)
    OUT_LOCAL.parent.mkdir(parents=True, exist_ok=True)
    OUT_PAGES.write_text(html)
    OUT_LOCAL.write_text(html)
    print(f"[cc-gen] rendered · A${aud_income:,} · {doors}d · {len(deals)}deal · {len(needs)}need · FX={usd_to_aud:.3f}")


if __name__ == "__main__":
    render()
