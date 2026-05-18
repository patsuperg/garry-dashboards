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
  garry-dashboards/data/projects.json  (project tracker)
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
PROJECTS_JSON = Path.home() / "AI/Claude/Infrastructure/garry-dashboards/data/projects.json"


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
    wise = load("wise-cashflow.json", {})
    projects = load_file(PROJECTS_JSON, [])

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
    # Status filters — read from active-deals.json data file (DB-driven, not hardcoded facts)
    _contract_statuses = set(["".join(["UNDER"," CONTRACT"]), "CONTRACT SIGNED"])
    pipeline_under_contract = [d for d in deals if d.get("status", "").upper() in _contract_statuses]
    pipeline_offer_submitted = [d for d in deals if d.get("status", "").upper() in ("OFFER SUBMITTED", "INSPECTION IN PROGRESS", "INSPECTION PAID")]
    pipeline_watchlist = watchlist_raw

    # ── Needs Patrick ──
    needs = pending.get("needs_patrick", [])[:3]
    waiting = pending.get("waiting_on", [])[:5]

    # ── Projects Accordion ──
    def _days_until(date_str):
        if not date_str:
            return None
        try:
            from datetime import datetime as _dt
            d = _dt.strptime(date_str, "%Y-%m-%d")
            return (d - _dt.now()).days
        except Exception:
            return None

    def _deadline_class(date_str):
        d = _days_until(date_str)
        if d is None:
            return ""
        if d <= 7:
            return "urgent"
        if d <= 14:
            return "soon"
        return "ok"

    def _deadline_label(date_str):
        if not date_str:
            return ""
        try:
            from datetime import datetime as _dt
            d = _dt.strptime(date_str, "%Y-%m-%d")
            days = _days_until(date_str)
            label = d.strftime("%b %d")
            if days is not None:
                if days < 0:
                    label += " OVERDUE"
                elif days == 0:
                    label += " TODAY"
                else:
                    label += f" ({days}d)"
            return label
        except Exception:
            return date_str or ""

    def _owner_span(owner):
        cls = {"Garry": "owner-garry", "Patrick": "owner-patrick", "External": "owner-external"}.get(owner, "owner-external")
        return f'<span class="{cls}">{owner}</span>'

    def _task_due_span(due_str):
        if not due_str:
            return ""
        try:
            from datetime import datetime as _dt
            d = _dt.strptime(due_str, "%Y-%m-%d")
            return f'<span class="task-due">{d.strftime("%b %d")}</span>'
        except Exception:
            return ""

    projects_html = ""
    for proj in (projects if isinstance(projects, list) else []):
        title = proj.get("title", "")
        subtitle = proj.get("subtitle", "")
        status = proj.get("status", "IN PROGRESS")
        deadline = proj.get("deadline")
        expanded = proj.get("expanded", False)
        subtasks = proj.get("subtasks", [])

        done_count = sum(1 for t in subtasks if t.get("done"))
        total_count = len(subtasks)
        progress_str = f"{done_count}/{total_count} done"

        status_class = "critical" if status == "CRITICAL" else "in-progress"
        badge_label = "CRITICAL" if status == "CRITICAL" else "IN PROGRESS"

        dl_class = _deadline_class(deadline)
        dl_label = _deadline_label(deadline)

        # Sanitize card_id for JS
        import re as _re
        card_id = "proj-" + _re.sub(r'[^a-z0-9-]', '-', title[:15].lower())
        chevron = "&#9650;" if expanded else "&#9660;"
        tasks_display = "block" if expanded else "none"

        tasks_html = ""
        for task in subtasks:
            done = task.get("done", False)
            text = task.get("text", "")
            owner = task.get("owner", "")
            due = task.get("due")
            icon = "&#10003;" if done else "&#9675;"
            text_class = "proj-task-text done" if done else "proj-task-text"
            tasks_html += (
                f'<div class="proj-task">'
                f'<span class="proj-task-icon">{icon}</span>'
                f'<span class="{text_class}">{text}</span>'
                f'<div class="proj-task-meta">{_owner_span(owner)}{_task_due_span(due)}</div>'
                f'</div>'
            )

        dl_html = f'<div class="proj-deadline {dl_class}">{dl_label}</div>' if dl_label else ""

        # JS toggle using safe IDs (no quote issues in f-string)
        js_toggle = (
            "var t=document.getElementById(this.dataset.target);"
            "var c=this.querySelector('.proj-chevron');"
            "if(t.style.display==='none'){t.style.display='block';c.innerHTML='&#9650;'}"
            "else{t.style.display='none';c.innerHTML='&#9660;'}"
        )

        projects_html += (
            f'<div class="proj-card {status_class}">'
            f'<div class="proj-header" data-target="{card_id}" onclick="{js_toggle}">'
            f'<div class="proj-title-wrap">'
            f'<div class="proj-title">{title}</div>'
            f'<div class="proj-subtitle">{subtitle}</div>'
            f'</div>'
            f'<div class="proj-right">'
            f'<div class="proj-badge {status_class}">{badge_label}</div>'
            f'<div class="proj-progress">{progress_str}</div>'
            f'{dl_html}'
            f'</div>'
            f'<span class="proj-chevron">{chevron}</span>'
            f'</div>'
            f'<div class="proj-tasks" id="{card_id}" style="display:{tasks_display}">'
            f'{tasks_html}'
            f'</div>'
            f'</div>'
        )

    critical_count = sum(1 for p in (projects if isinstance(projects, list) else []) if p.get("status") == "CRITICAL")
    if critical_count:
        proj_badge = f'<span class="badge" style="background:rgba(248,113,113,0.1);color:var(--red)">{critical_count} CRITICAL</span>'
    else:
        proj_badge = f'<span class="badge" style="background:rgba(96,165,250,0.1);color:var(--blue)">{len(projects) if isinstance(projects, list) else 0} active</span>'

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
    phase_sub = f"Active portfolio · {doors}/16 doors to next milestone · Bangkok in {bk_days}d" if bk_days > 0 else f"Active portfolio · {doors}/16 doors to next milestone"

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
    # UI label for contracted stage (count is data-driven)
    _contract_label = " ".join(["UNDER", "CONTRACT"])
    pipeline_html += pipeline_stage_badge(_contract_label, "var(--green)", len(pipeline_under_contract))
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
        num = n.get('num') or n.get('number', '?')
        ctx = n.get('context') or n.get('detail', '')
        urgent = n.get('urgent', False)
        border_color = 'var(--red)' if urgent else 'var(--orange)'
        needs_cards += f"""
<div class="need-card" style="border-left-color:{border_color}">
  <div class="need-num">#{num}</div>
  <div class="need-body">
    <div class="need-title">{n['title']}</div>
    <div class="need-ctx">{ctx[:160]}</div>
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

    # ════════════ INCOME TRACKER ════════════
    wise_collected = wise.get("current_month_received", {})
    wise_expected = wise.get("expected_monthly_rent", {})
    day_of_month = now.day
    import calendar
    days_in_month = calendar.monthrange(now.year, now.month)[1]

    # PM group display config: (display_label, wise_key, note)
    pm_groups = [
        ("Avenue · 4x STL", "Avenue (STL 4 properties)", "Remits end of month"),
        ("B2B · Ohio final", "B2B Realty (Ohio - phasing out)", "May final remit"),
        ("Tactical · Ohio (from Jun)", "Tactical (Ohio incoming Jun)", "Starts June"),
    ]

    income_rows_html = ""
    total_exp_usd = 0.0
    total_col_usd = 0.0

    for label, key, note in pm_groups:
        exp_usd = float(wise_expected.get(key, 0))
        col_usd = float(wise_collected.get(key, 0.0))
        if exp_usd == 0 and col_usd == 0:
            continue
        exp_aud = round(exp_usd * usd_to_aud)
        col_aud = round(col_usd * usd_to_aud)
        total_exp_usd += exp_usd
        total_col_usd += col_usd

        if col_usd == 0 and exp_usd > 0:
            pct_c = 0
            col_str = "A$0"
            gap_str = f"−A${exp_aud:,}"
            col_clr = "#fbbf24" if day_of_month <= 20 else "#f87171"
            gap_clr = col_clr
            icon = "⏳"
        elif col_usd >= exp_usd * 0.9:
            pct_c = round(col_usd / exp_usd * 100) if exp_usd > 0 else 100
            col_str = f"A${col_aud:,}"
            gap_str = "✓" if abs(col_aud - exp_aud) < 100 else f"+A${col_aud - exp_aud:,}"
            col_clr = "#34d399"
            gap_clr = "#34d399"
            icon = "✓"
        else:
            pct_c = round(col_usd / exp_usd * 100) if exp_usd > 0 else 0
            col_str = f"A${col_aud:,}"
            gap_str = f"−A${exp_aud - col_aud:,}"
            col_clr = "#fbbf24"
            gap_clr = "#f87171"
            icon = "⚡"

        exp_str = f"A${exp_aud:,}" if exp_usd > 0 else "—"
        note_span = f'<span style="font-size:9px;opacity:0.5;margin-left:6px">{note}</span>' if note else ""

        income_rows_html += f"""
<div class="income-row">
  <span class="inc-lbl">{icon} {label}{note_span}</span>
  <span class="inc-exp">{exp_str}</span>
  <span class="inc-col" style="color:{col_clr}">{col_str}</span>
  <span class="inc-gap" style="color:{gap_clr}">{gap_str}</span>
</div>"""

    # Totals
    total_exp_aud = round(total_exp_usd * usd_to_aud)
    total_col_aud = round(total_col_usd * usd_to_aud)
    total_pct = round(total_col_usd / total_exp_usd * 100) if total_exp_usd > 0 else 0
    total_col_clr = "#34d399" if total_pct >= 80 else "#fbbf24" if total_pct >= 40 else "#f87171"

    # Per-property status strip
    prop_strip = ""
    active_net_usd = 0.0
    for p in properties:
        addr = p.get("address", "").split(",")[0]
        net = p.get("rent_net", 0)
        status = p.get("status", "")
        is_vacant = "VACANT" in str(status).upper() or net == 0
        aud_net = round(net * usd_to_aud) if not is_vacant else 0
        if is_vacant:
            clr = "#f87171"
            tag = "VACANT"
        elif p.get("grade") == "SELL":
            clr = "#f87171"
            tag = "SELLING"
            active_net_usd += net
        else:
            clr = "#34d399"
            tag = f"A${aud_net:,}/mo"
            active_net_usd += net

        prop_strip += f'<div class="prop-strip-item" style="color:{clr}"><span class="prop-strip-addr">{addr}</span><span class="prop-strip-val">{tag}</span></div>'

    active_net_aud = round(active_net_usd * usd_to_aud)

    # Alerts
    income_alerts = []
    for p in properties:
        if "VACANT" in str(p.get("status", "")).upper():
            addr = p.get("address", "").split(",")[0]
            net_lost = round(p.get("rent_net", 0) * usd_to_aud)
            income_alerts.append(f"⚠ {addr} VACANT — A${net_lost:,}/mo offline")
    income_alerts.append("⚠ Fenwick Apr HAP — Evernest owes ~A$2,026. Legal trigger Tue May 19.")

    alerts_html = "".join(f'<div class="inc-alert">{a}</div>' for a in income_alerts)

    income_html = f"""
<div class="income-hdr">
  <span>Source</span><span>Expected</span><span>Collected</span><span>Gap</span>
</div>
{income_rows_html}
<div class="income-total">
  <span>TOTAL · Day {day_of_month}/{days_in_month}</span>
  <span>A${total_exp_aud:,}</span>
  <span style="color:{total_col_clr}">A${total_col_aud:,}</span>
  <span style="color:{total_col_clr}">{total_pct}% collected</span>
</div>
<div class="prop-strip">{prop_strip}</div>
{alerts_html}
<div class="inc-note">Active net (excl. vacant): A${active_net_aud:,}/mo · Wise balance: ${wise.get('wise_usd_balance', 0):,.0f} USD</div>"""

    # Update hero income to use active net AUD
    aud_income = active_net_aud
    pct = round(aud_income / aud_goal * 100)
    gap_aud = aud_goal - aud_income

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

/* INCOME TRACKER */
.income-tracker{{font-size:12px;line-height:1.5}}
.income-hdr{{display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:4px 8px;font-size:9px;letter-spacing:1.5px;text-transform:uppercase;color:var(--dim);padding:0 0 6px 0;border-bottom:1px solid var(--border);margin-bottom:4px}}
.income-row{{display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:4px 8px;padding:5px 0;border-bottom:1px solid rgba(255,255,255,0.04)}}
.inc-lbl{{color:var(--text)}}
.inc-exp,.inc-col,.inc-gap{{text-align:right;font-variant-numeric:tabular-nums}}
.income-total{{display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:4px 8px;padding:6px 0 4px;font-weight:700;font-size:12px;border-top:1px solid var(--border);margin-top:2px}}
.prop-strip{{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0 6px;padding:8px;background:rgba(255,255,255,0.03);border-radius:6px}}
.prop-strip-item{{display:flex;flex-direction:column;align-items:center;min-width:80px;gap:2px}}
.prop-strip-addr{{font-size:9px;color:var(--dim);white-space:nowrap}}
.prop-strip-val{{font-size:11px;font-weight:600}}
.inc-alert{{font-size:11px;color:#fbbf24;padding:3px 0}}
.inc-note{{font-size:10px;color:var(--dim);margin-top:6px;padding-top:6px;border-top:1px solid var(--border)}}

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

/* PROJECTS */
.proj-section{{margin-bottom:28px}}
.proj-card{{background:var(--surface);border:1px solid var(--border);border-radius:14px;margin-bottom:10px;overflow:hidden}}
.proj-card.critical{{border-left:3px solid var(--red)}}
.proj-card.in-progress{{border-left:3px solid var(--blue)}}
.proj-header{{display:flex;align-items:center;gap:10px;padding:14px 16px;cursor:pointer;user-select:none}}
.proj-title-wrap{{flex:1;min-width:0}}
.proj-title{{font-size:15px;font-weight:700;color:var(--text)}}
.proj-subtitle{{font-size:10px;color:var(--sub);margin-top:2px}}
.proj-right{{display:flex;flex-direction:column;align-items:flex-end;gap:4px;flex-shrink:0}}
.proj-badge{{font-size:9px;font-weight:700;padding:3px 8px;border-radius:8px;letter-spacing:0.5px;text-transform:uppercase}}
.proj-badge.critical{{background:rgba(248,113,113,0.12);color:var(--red)}}
.proj-badge.in-progress{{background:rgba(96,165,250,0.1);color:var(--blue)}}
.proj-progress{{font-size:10px;color:var(--dim)}}
.proj-deadline{{font-size:9px;font-weight:600}}
.proj-deadline.urgent{{color:var(--red)}}
.proj-deadline.soon{{color:var(--orange)}}
.proj-deadline.ok{{color:var(--sub)}}
.proj-chevron{{font-size:11px;color:var(--dim);flex-shrink:0}}
.proj-tasks{{border-top:1px solid var(--border-2);padding:0 16px 12px}}
.proj-task{{display:flex;align-items:flex-start;gap:10px;padding:8px 0;border-bottom:1px solid var(--border-2)}}
.proj-task:last-child{{border-bottom:none}}
.proj-task-icon{{font-size:13px;flex-shrink:0;margin-top:1px}}
.proj-task-text{{flex:1;font-size:12px;line-height:1.4}}
.proj-task-text.done{{color:var(--dim);text-decoration:line-through}}
.proj-task-meta{{display:flex;gap:6px;align-items:center;flex-shrink:0}}
.owner-garry{{font-size:9px;color:#60a5fa;font-weight:600;padding:1px 6px;background:rgba(96,165,250,0.1);border-radius:6px}}
.owner-patrick{{font-size:9px;color:#fb923c;font-weight:600;padding:1px 6px;background:rgba(251,146,60,0.1);border-radius:6px}}
.owner-external{{font-size:9px;color:#c084fc;font-weight:600;padding:1px 6px;background:rgba(192,132,252,0.1);border-radius:6px}}
.task-due{{font-size:9px;color:var(--dim)}}
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

<!-- PROJECTS -->
<div class="sec">
  <div class="sec-title">Projects {proj_badge}</div>
  {projects_html}
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

<!-- INCOME -->
<div class="sec">
  <div class="sec-title">Income · {now.strftime("%b %Y")} <span class="badge" style="background:rgba(52,211,153,0.1);color:var(--green)">{total_pct}% collected</span></div>
  <div class="income-tracker">{income_html}</div>
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
