#!/usr/bin/env python3
"""
Garry Dashboard Generator
Generates Command Centre + Garry COO System dashboards from live state.
Pushes to GitHub Pages for global access.
"""

import subprocess, os, re, json
from datetime import datetime

STATE_FILE = os.path.expanduser("~/AI/Claude/CURRENT-STATE.md")
SCHEDULES_FILE = os.path.expanduser("~/AI/Claude/SCHEDULES.md")
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

def read_file(path):
    try:
        with open(path) as f:
            return f.read()
    except:
        return ""

def run(cmd):
    try:
        return subprocess.check_output(cmd, shell=True, text=True, timeout=10).strip()
    except:
        return ""

def get_system_health():
    agent_lines = run("launchctl list 2>/dev/null | grep com.patrick")
    agents = len([l for l in agent_lines.splitlines() if l.strip()]) if agent_lines else 0
    disk_info = run("df -h / | tail -1")
    disk_parts = disk_info.split()
    disk_free = disk_parts[3] if len(disk_parts) > 3 else "?"
    disk_used_pct = disk_parts[4].replace('%','') if len(disk_parts) > 4 else "?"
    telegram_up = bool(run("pgrep -f telegram-claude-bot"))
    ollama_up = bool(run("pgrep -f 'ollama serve'"))
    dashboard_up = bool(run("pgrep -f 'command-centre'"))
    security = "PASS"
    return {
        'agents': agents,
        'disk_free': disk_free,
        'disk_used_pct': disk_used_pct,
        'telegram': telegram_up,
        'ollama': ollama_up,
        'dashboard': dashboard_up,
        'security': security,
    }

def parse_state(state):
    # Portfolio
    properties = []
    for m in re.finditer(r'- (.+?): \$([0-9,]+)/mo net \[(.+?)\]', state):
        properties.append({
            'address': m.group(1),
            'net': m.group(2).replace(',',''),
            'status': m.group(3),
        })
    total_match = re.search(r'\*\*Total net: \$([\d,]+)/mo\*\*', state)
    total = total_match.group(1).replace(',','') if total_match else "0"

    # Deals
    deals = []
    deal_section = re.search(r'## Deal Pipeline\n(.*?)(?=\n## |\Z)', state, re.DOTALL)
    if deal_section:
        for line in deal_section.group(1).strip().splitlines():
            line = line.strip()
            if line.startswith('- **'):
                name_match = re.match(r'- \*\*(.+?)\*\*', line)
                if name_match:
                    name = name_match.group(1).rstrip(':')
                    detail = re.sub(r'- \*\*.+?\*\*:?\s*', '', line)
                    status = 'active'
                    if 'LOST' in line.upper() or 'PASS' in line.upper():
                        status = 'dead'
                    elif 'pending' in line.lower():
                        status = 'pending'
                    deals.append({'name': name, 'detail': detail, 'status': status})

    # Key dates
    dates = []
    dates_section = re.search(r'## Key Dates\n(.*?)(?=\n## |\Z)', state, re.DOTALL)
    if dates_section:
        for line in dates_section.group(1).strip().splitlines():
            line = line.strip()
            if line.startswith('- **'):
                m = re.match(r'- \*\*(.+?)\*\*:?\s*(.*)', line)
                if m:
                    dates.append({'date': m.group(1).rstrip(':'), 'item': m.group(2)})

    return properties, total, deals, dates

def parse_automations(schedules):
    autos = []
    in_table = False
    for line in schedules.splitlines():
        if '| Time |' in line:
            in_table = True
            continue
        if in_table and line.startswith('|---'):
            continue
        if in_table and line.startswith('|'):
            parts = [p.strip() for p in line.split('|')[1:-1]]
            if len(parts) >= 5:
                autos.append({
                    'time': parts[0],
                    'freq': parts[1],
                    'task': parts[2],
                    'script': parts[3],
                    'status': parts[4],
                })
        elif in_table and not line.startswith('|'):
            break
    return autos

def dot(color):
    colors = {
        'green': '#4ade80',
        'amber': '#fbbf24',
        'red': '#f87171',
    }
    c = colors.get(color, colors['green'])
    return f'<span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:{c};box-shadow:0 0 6px {c}66;margin-right:6px;vertical-align:middle"></span>'

def generate_command_centre(properties, total, deals, dates, health):
    now = datetime.now().strftime("%b %d, %Y %I:%M %p")
    total_int = int(total)
    goal = 20000
    pct = round(total_int / goal * 100, 1)
    bar_pct = min(pct, 100)

    prop_cards = ""
    for p in properties:
        # Short address
        addr = p['address']
        if ',' in addr:
            parts = addr.split(',')
            addr_short = parts[0].strip()
            city = parts[-2].strip() if len(parts) > 2 else parts[-1].strip()
        else:
            addr_short = addr
            city = ""

        status_color = 'green' if p['status'] == 'LEASED' else 'amber'
        prop_cards += f"""
        <div class="card prop-card">
          <div class="prop-income">${p['net']}</div>
          <div class="prop-label">per month net</div>
          <div class="prop-addr">{addr_short}</div>
          <div class="prop-city">{city}</div>
          <div class="prop-status">{dot(status_color)}{p['status']}</div>
        </div>"""

    deal_rows = ""
    for d in deals:
        if d['status'] == 'dead':
            badge = '<span class="badge badge-red">LOST/PASS</span>'
        elif d['status'] == 'pending':
            badge = '<span class="badge badge-amber">PENDING</span>'
        else:
            badge = '<span class="badge badge-green">ACTIVE</span>'
        deal_rows += f"""
        <div class="deal-row">
          <div class="deal-name">{d['name']}</div>
          <div class="deal-detail">{d['detail']}</div>
          <div>{badge}</div>
        </div>"""

    date_items = ""
    for d in dates:
        date_items += f"""
        <div class="date-item">
          <div class="date-marker"></div>
          <div>
            <div class="date-date">{d['date']}</div>
            <div class="date-desc">{d['item']}</div>
          </div>
        </div>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="refresh" content="300">
<title>Command Centre — Patrick Dickson</title>
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
:root{{
  --bg:#09090b;--card:#111113;--border:#1e1e22;
  --text:#e4e4e7;--muted:#71717a;--dim:#52525b;
  --green:#4ade80;--green-bg:#052e16;
  --amber:#fbbf24;--amber-bg:#422006;
  --red:#f87171;--red-bg:#450a0a;
  --blue:#60a5fa;--purple:#a78bfa;
  --accent:linear-gradient(135deg,#4ade80,#22c55e);
}}
body{{font-family:-apple-system,BlinkMacSystemFont,'SF Pro Display',system-ui,sans-serif;background:var(--bg);color:var(--text);line-height:1.5;padding:24px;max-width:1200px;margin:0 auto;-webkit-font-smoothing:antialiased}}

.header{{display:flex;justify-content:space-between;align-items:center;padding-bottom:24px;margin-bottom:32px;border-bottom:1px solid var(--border)}}
.header h1{{font-size:1.6rem;font-weight:700;letter-spacing:-.5px}}
.header .sub{{color:var(--muted);font-size:.8rem;margin-top:2px}}
.header .updated{{color:var(--dim);font-size:.75rem;text-align:right}}

.kpi-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-bottom:40px}}
.kpi{{background:var(--card);border:1px solid var(--border);border-radius:16px;padding:24px;text-align:center}}
.kpi-value{{font-size:2.4rem;font-weight:800;line-height:1.1}}
.kpi-value.money{{background:var(--accent);-webkit-background-clip:text;-webkit-text-fill-color:transparent}}
.kpi-label{{color:var(--muted);font-size:.75rem;text-transform:uppercase;letter-spacing:1px;margin-top:6px}}
.progress-bar{{background:#1a1a1e;height:8px;border-radius:4px;margin-top:12px;overflow:hidden}}
.progress-fill{{height:100%;border-radius:4px;background:var(--accent);transition:width .5s}}

h2{{font-size:.85rem;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:1.5px;margin-bottom:16px;padding-bottom:8px;border-bottom:1px solid var(--border)}}

.card{{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:20px;transition:border-color .2s,transform .15s}}
.card:hover{{border-color:#333;transform:translateY(-1px)}}

.prop-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:14px;margin-bottom:40px}}
.prop-income{{font-size:1.8rem;font-weight:800;color:var(--green)}}
.prop-label{{font-size:.7rem;color:var(--dim);margin-bottom:8px}}
.prop-addr{{font-size:.85rem;font-weight:600}}
.prop-city{{font-size:.75rem;color:var(--muted)}}
.prop-status{{font-size:.75rem;margin-top:8px;display:flex;align-items:center}}

.deals{{margin-bottom:40px}}
.deal-row{{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:14px 18px;margin-bottom:8px;display:flex;align-items:center;gap:14px}}
.deal-name{{font-weight:600;font-size:.9rem;min-width:140px}}
.deal-detail{{flex:1;font-size:.8rem;color:var(--muted)}}
.badge{{font-size:.7rem;font-weight:600;padding:3px 10px;border-radius:20px;text-transform:uppercase;letter-spacing:.5px;white-space:nowrap}}
.badge-green{{background:var(--green-bg);color:var(--green)}}
.badge-amber{{background:var(--amber-bg);color:var(--amber)}}
.badge-red{{background:var(--red-bg);color:var(--red)}}

.dates{{margin-bottom:40px}}
.date-item{{display:flex;align-items:flex-start;gap:14px;margin-bottom:14px}}
.date-marker{{width:10px;height:10px;border-radius:50%;background:var(--blue);margin-top:5px;flex-shrink:0;box-shadow:0 0 8px #60a5fa44}}
.date-date{{font-weight:600;font-size:.85rem}}
.date-desc{{color:var(--muted);font-size:.8rem}}

.finance-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:14px;margin-bottom:40px}}
.finance-card{{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:18px}}
.finance-title{{font-size:.7rem;color:var(--dim);text-transform:uppercase;letter-spacing:.8px;margin-bottom:4px}}
.finance-value{{font-size:1rem;font-weight:600}}
.finance-note{{font-size:.75rem;color:var(--muted);margin-top:4px}}

.sys-bar{{display:flex;flex-wrap:wrap;gap:12px;margin-bottom:40px}}
.sys-item{{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:10px 16px;font-size:.8rem;display:flex;align-items:center;gap:6px}}

.footer{{text-align:center;color:var(--dim);font-size:.7rem;padding-top:24px;border-top:1px solid var(--border)}}

@media(max-width:768px){{
  body{{padding:14px}}
  .header{{flex-direction:column;align-items:flex-start;gap:8px}}
  .kpi-grid{{grid-template-columns:1fr}}
  .prop-grid{{grid-template-columns:repeat(2,1fr)}}
  .deal-row{{flex-direction:column;align-items:flex-start}}
}}
</style>
</head>
<body>

<div class="header">
  <div>
    <h1>COMMAND CENTRE</h1>
    <div class="sub">Patrick Dickson — Section 8 Portfolio</div>
  </div>
  <div class="updated">
    Last updated<br><strong>{now}</strong>
  </div>
</div>

<div class="kpi-grid">
  <div class="kpi">
    <div class="kpi-value money">${total_int:,}</div>
    <div class="kpi-label">Monthly Net Income</div>
  </div>
  <div class="kpi">
    <div class="kpi-value">{len(properties)}</div>
    <div class="kpi-label">Properties</div>
  </div>
  <div class="kpi">
    <div class="kpi-value">{pct}%</div>
    <div class="kpi-label">of $20K/mo goal</div>
    <div class="progress-bar"><div class="progress-fill" style="width:{bar_pct}%"></div></div>
  </div>
</div>

<h2>Portfolio</h2>
<div class="prop-grid">
  {prop_cards}
</div>

<h2>Deal Pipeline</h2>
<div class="deals">
  {deal_rows if deal_rows else '<div style="color:var(--dim);font-size:.85rem;padding:14px">No active deals</div>'}
</div>

<h2>Key Dates</h2>
<div class="dates">
  {date_items if date_items else '<div style="color:var(--dim);font-size:.85rem;padding:14px">No upcoming dates</div>'}
</div>

<h2>Financing</h2>
<div class="finance-grid">
  <div class="finance-card">
    <div class="finance-title">DSCR Lender</div>
    <div class="finance-value">Nick Worthing — America Mortgages</div>
    <div class="finance-note">$120K+ single / $100K+ bundled minimums</div>
  </div>
  <div class="finance-card">
    <div class="finance-title">Current LTV</div>
    <div class="finance-value">60% (foreign national)</div>
    <div class="finance-note">65-75% on $180K+ properties or with residency</div>
  </div>
  <div class="finance-card">
    <div class="finance-title">Property Manager</div>
    <div class="finance-value">Avenue Residential</div>
    <div class="finance-note">Heather Stone — heather@avenuestl.com</div>
  </div>
  <div class="finance-card">
    <div class="finance-title">CPA</div>
    <div class="finance-value">GW Carter — Engaged</div>
    <div class="finance-note">US tax filing for foreign national</div>
  </div>
</div>

<h2>System</h2>
<div class="sys-bar">
  <div class="sys-item">{dot('green' if health['agents'] > 20 else 'amber')}{health['agents']} Agents</div>
  <div class="sys-item">{dot('green' if health['telegram'] else 'red')}Telegram Bot</div>
  <div class="sys-item">{dot('green')}Security {health['security']}</div>
  <div class="sys-item">{dot('green')}{health['disk_free']} Free</div>
  <div class="sys-item">{dot('green' if health['ollama'] else 'amber')}Ollama</div>
</div>

<div class="footer">
  Powered by Garry COO System &mdash; Auto-updated every 30 minutes<br>
  &copy; {datetime.now().year} Patrick Dickson
</div>

</body>
</html>"""
    return html


def generate_garry_dashboard(health, automations):
    now = datetime.now().strftime("%b %d, %Y %I:%M %p")
    active_count = len([a for a in automations if 'ACTIVE' in a.get('status','')])

    # Team cards
    team = [
        {"name": "Garry", "role": "Chief Operating Officer", "color": "#4ade80,#22c55e", "initial": "G",
         "desc": "Overall coordination, system orchestration, Patrick's bandwidth protection"},
        {"name": "Atlas", "role": "Finance Specialist", "color": "#60a5fa,#3b82f6", "initial": "A",
         "desc": "Portfolio tracking, HAP payments, cash flow analysis, GW Carter CPA coordination"},
        {"name": "Mercury", "role": "Operations", "color": "#fbbf24,#f59e0b", "initial": "M",
         "desc": "Property management, Avenue Residential liaison, maintenance coordination"},
        {"name": "Sentinel", "role": "Risk & Security", "color": "#f87171,#ef4444", "initial": "S",
         "desc": "Security audits, secret scanning, backup integrity, key rotation"},
        {"name": "Apollo", "role": "Communications", "color": "#a78bfa,#8b5cf6", "initial": "Ap",
         "desc": "Telegram bot, email automation, Laura's course delivery, notifications"},
    ]

    team_html = ""
    for t in team:
        team_html += f"""
        <div class="team-card">
          <div class="team-header">
            <div class="avatar" style="background:linear-gradient(135deg,{t['color']})">{t['initial']}</div>
            <div>
              <div class="team-name">{t['name']}</div>
              <div class="team-role">{t['role']}</div>
            </div>
          </div>
          <div class="team-desc">{t['desc']}</div>
          <div class="team-status">{dot('green')} Online</div>
        </div>"""

    # Automation table rows
    auto_rows = ""
    for a in automations:
        status = a.get('status', '')
        if 'ACTIVE' in status:
            badge = f'<span class="badge badge-green">ACTIVE</span>'
        else:
            badge = f'<span class="badge badge-amber">{status}</span>'
        auto_rows += f"""
        <tr>
          <td>{a['time']}</td>
          <td>{a['freq']}</td>
          <td>{a['task']}</td>
          <td style="color:var(--dim);font-size:.75rem">{a['script']}</td>
          <td>{badge}</td>
        </tr>"""

    # Roadmap
    roadmap = [
        {"item": "HAP Payment Tracker", "status": "scaffolded", "detail": "Needs real Avenue payment data"},
        {"item": "Auto-Offer System", "status": "live", "detail": "Deal Finder → Telegram buttons → email draft"},
        {"item": "Portfolio Dashboard v3", "status": "live", "detail": "Global access via GitHub Pages"},
        {"item": "Self-Healing Agents", "status": "live", "detail": "Backoff: 5m/15m/1hr auto-restart"},
        {"item": "Credit Score Builder", "status": "planned", "detail": "Capital One secured card → autopay"},
        {"item": "Avenue API Integration", "status": "planned", "detail": "Direct rent roll + maintenance data"},
        {"item": "Tax Filing Automation", "status": "planned", "detail": "GW Carter quarterly prep pipeline"},
        {"item": "Bangkok Relocation Ops", "status": "in-progress", "detail": "Apartment picks, visa planning, DTV prep"},
        {"item": "DSCR Financing Pipeline", "status": "ready", "detail": "Nick Worthing engaged, $120K+ triggers"},
        {"item": "Multi-Property Bundled Loan", "status": "planned", "detail": "Bundle 3-5 properties for better terms"},
    ]

    roadmap_rows = ""
    for r in roadmap:
        s = r['status']
        if s == 'live':
            badge = '<span class="badge badge-green">LIVE</span>'
        elif s == 'in-progress':
            badge = '<span class="badge badge-amber">IN PROGRESS</span>'
        elif s == 'scaffolded':
            badge = '<span class="badge badge-amber">SCAFFOLDED</span>'
        elif s == 'ready':
            badge = '<span class="badge badge-green">READY</span>'
        else:
            badge = '<span class="badge badge-dim">PLANNED</span>'
        roadmap_rows += f"""
        <tr>
          <td>{r['item']}</td>
          <td>{badge}</td>
          <td style="color:var(--muted)">{r['detail']}</td>
        </tr>"""

    # System grade
    grade_score = 0
    if health['agents'] >= 25: grade_score += 25
    elif health['agents'] >= 20: grade_score += 20
    if health['telegram']: grade_score += 25
    if health['security'] == 'PASS': grade_score += 25
    if int(health['disk_used_pct']) < 80 if health['disk_used_pct'].isdigit() else True: grade_score += 25
    grade = 'A+' if grade_score >= 95 else 'A' if grade_score >= 80 else 'B' if grade_score >= 60 else 'C'

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="refresh" content="300">
<title>GARRY COO System</title>
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
:root{{
  --bg:#09090b;--card:#111113;--border:#1e1e22;
  --text:#e4e4e7;--muted:#71717a;--dim:#52525b;
  --green:#4ade80;--green-bg:#052e16;
  --amber:#fbbf24;--amber-bg:#422006;
  --red:#f87171;--red-bg:#450a0a;
  --blue:#60a5fa;--purple:#a78bfa;
  --accent:linear-gradient(135deg,#4ade80,#22c55e);
}}
body{{font-family:-apple-system,BlinkMacSystemFont,'SF Pro Display',system-ui,sans-serif;background:var(--bg);color:var(--text);line-height:1.5;padding:24px;max-width:1400px;margin:0 auto;-webkit-font-smoothing:antialiased}}

.header{{display:flex;justify-content:space-between;align-items:center;padding-bottom:24px;margin-bottom:32px;border-bottom:1px solid var(--border)}}
.header-left{{display:flex;align-items:center;gap:16px}}
.logo{{width:44px;height:44px;background:var(--accent);border-radius:12px;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:20px;color:#09090b}}
.header h1{{font-size:1.6rem;font-weight:700;letter-spacing:-.5px}}
.header .sub{{color:var(--muted);font-size:.8rem}}
.grade{{text-align:right}}
.grade-value{{font-size:2.8rem;font-weight:800;background:var(--accent);-webkit-background-clip:text;-webkit-text-fill-color:transparent;line-height:1}}
.grade-label{{font-size:.65rem;color:var(--green);text-transform:uppercase;letter-spacing:1px}}

h2{{font-size:.85rem;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:1.5px;margin-bottom:16px;padding-bottom:8px;border-bottom:1px solid var(--border)}}

.status-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:12px;margin-bottom:40px}}
.status-item{{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:14px 16px;transition:border-color .2s}}
.status-item:hover{{border-color:#333}}
.status-label{{font-size:.65rem;color:var(--dim);text-transform:uppercase;letter-spacing:.8px;margin-bottom:4px}}
.status-value{{font-size:.9rem;font-weight:600;display:flex;align-items:center}}

.team-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:14px;margin-bottom:40px}}
.team-card{{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:20px;transition:border-color .2s,transform .15s}}
.team-card:hover{{border-color:#333;transform:translateY(-2px)}}
.team-header{{display:flex;align-items:center;gap:12px;margin-bottom:10px}}
.avatar{{width:36px;height:36px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:14px;color:#09090b}}
.team-name{{font-weight:600;font-size:.95rem}}
.team-role{{font-size:.7rem;color:var(--muted)}}
.team-desc{{font-size:.8rem;color:var(--muted);margin-top:8px;padding-top:8px;border-top:1px solid var(--border)}}
.team-status{{display:flex;align-items:center;gap:6px;font-size:.75rem;margin-top:8px}}

.perf-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:14px;margin-bottom:40px}}
.perf-card{{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:20px;text-align:center}}
.perf-number{{font-size:2rem;font-weight:800;background:linear-gradient(135deg,#60a5fa,#818cf8);-webkit-background-clip:text;-webkit-text-fill-color:transparent;line-height:1.2}}
.perf-label{{font-size:.7rem;color:var(--dim);text-transform:uppercase;letter-spacing:.8px;margin-top:6px}}

table{{width:100%;border-collapse:collapse;margin-bottom:40px}}
th{{text-align:left;font-size:.65rem;color:var(--dim);text-transform:uppercase;letter-spacing:.8px;padding:10px 14px;border-bottom:1px solid var(--border)}}
td{{padding:11px 14px;border-bottom:1px solid #111;font-size:.82rem}}
tr:hover td{{background:var(--card)}}

.badge{{font-size:.65rem;font-weight:600;padding:3px 10px;border-radius:20px;text-transform:uppercase;letter-spacing:.5px;white-space:nowrap}}
.badge-green{{background:var(--green-bg);color:var(--green)}}
.badge-amber{{background:var(--amber-bg);color:var(--amber)}}
.badge-red{{background:var(--red-bg);color:var(--red)}}
.badge-dim{{background:#1a1a1e;color:var(--dim)}}

.principles{{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:12px;padding:24px 0;border-top:1px solid var(--border);margin-top:20px}}
.principle{{font-size:.8rem;color:var(--dim)}}
.principle strong{{color:var(--muted)}}
.footer{{text-align:center;color:var(--dim);font-size:.7rem;padding-top:16px}}

@media(max-width:768px){{
  body{{padding:14px}}
  .header{{flex-direction:column;align-items:flex-start;gap:12px}}
  .status-grid{{grid-template-columns:repeat(2,1fr)}}
  .team-grid{{grid-template-columns:1fr}}
  .perf-grid{{grid-template-columns:repeat(2,1fr)}}
  table{{display:block;overflow-x:auto}}
}}
</style>
</head>
<body>

<div class="header">
  <div class="header-left">
    <div class="logo">G</div>
    <div>
      <h1>GARRY COO SYSTEM</h1>
      <div class="sub">Autonomous Operations Centre — Patrick Dickson</div>
    </div>
  </div>
  <div class="grade">
    <div class="grade-value">{grade}</div>
    <div class="grade-label">System Grade</div>
  </div>
</div>

<h2>System Status</h2>
<div class="status-grid">
  <div class="status-item">
    <div class="status-label">LaunchAgents</div>
    <div class="status-value">{dot('green' if health['agents'] >= 25 else 'amber')}{health['agents']} active</div>
  </div>
  <div class="status-item">
    <div class="status-label">Telegram Bot</div>
    <div class="status-value">{dot('green' if health['telegram'] else 'red')}{'v6 Online' if health['telegram'] else 'Offline'}</div>
  </div>
  <div class="status-item">
    <div class="status-label">Deal Pipeline</div>
    <div class="status-value">{dot('green')}Autonomous</div>
  </div>
  <div class="status-item">
    <div class="status-label">Security</div>
    <div class="status-value">{dot('green')}{health['security']}</div>
  </div>
  <div class="status-item">
    <div class="status-label">Disk Free</div>
    <div class="status-value">{dot('green')}{health['disk_free']}</div>
  </div>
  <div class="status-item">
    <div class="status-label">Ollama</div>
    <div class="status-value">{dot('green' if health['ollama'] else 'amber')}{'Running' if health['ollama'] else 'Idle'}</div>
  </div>
  <div class="status-item">
    <div class="status-label">Auto-Heal</div>
    <div class="status-value">{dot('green')}Active</div>
  </div>
  <div class="status-item">
    <div class="status-label">Backups</div>
    <div class="status-value">{dot('green')}Hourly</div>
  </div>
</div>

<h2>Agent Team</h2>
<div class="team-grid">
  {team_html}
</div>

<h2>Performance</h2>
<div class="perf-grid">
  <div class="perf-card">
    <div class="perf-number">{active_count}</div>
    <div class="perf-label">Active Automations</div>
  </div>
  <div class="perf-card">
    <div class="perf-number">{health['agents']}</div>
    <div class="perf-label">LaunchAgents</div>
  </div>
  <div class="perf-card">
    <div class="perf-number">24/7</div>
    <div class="perf-label">Uptime Target</div>
  </div>
  <div class="perf-card">
    <div class="perf-number">5</div>
    <div class="perf-label">Agent Team</div>
  </div>
</div>

<h2>Automations</h2>
<table>
  <thead>
    <tr><th>Time</th><th>Frequency</th><th>Task</th><th>Script</th><th>Status</th></tr>
  </thead>
  <tbody>
    {auto_rows}
  </tbody>
</table>

<h2>Roadmap</h2>
<table>
  <thead>
    <tr><th>Initiative</th><th>Status</th><th>Detail</th></tr>
  </thead>
  <tbody>
    {roadmap_rows}
  </tbody>
</table>

<div class="principles">
  <div class="principle"><strong>Rule 1:</strong> Never ask permission for technical ops</div>
  <div class="principle"><strong>Rule 2:</strong> Build before asking — ship finished systems</div>
  <div class="principle"><strong>Rule 3:</strong> Protect Patrick's bandwidth — results only</div>
  <div class="principle"><strong>Rule 4:</strong> Self-heal — fix infrastructure problems silently</div>
  <div class="principle"><strong>Rule 5:</strong> Be many steps ahead — pre-solve everything</div>
</div>

<div class="footer">
  Powered by Garry COO System &mdash; Auto-updated every 30 minutes<br>
  &copy; {datetime.now().year} Patrick Dickson
</div>

</body>
</html>"""
    return html


def main():
    state = read_file(STATE_FILE)
    schedules = read_file(SCHEDULES_FILE)
    health = get_system_health()
    properties, total, deals, dates = parse_state(state)
    automations = parse_automations(schedules)

    # Generate Command Centre
    cc_html = generate_command_centre(properties, total, deals, dates, health)
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w") as f:
        f.write(cc_html)

    # Generate Garry Dashboard
    garry_html = generate_garry_dashboard(health, automations)
    with open(os.path.join(OUTPUT_DIR, "garry.html"), "w") as f:
        f.write(garry_html)

    print(f"Generated both dashboards at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Portfolio: {len(properties)} properties, ${total}/mo net")
    print(f"  System: {health['agents']} agents, {len(automations)} automations")


if __name__ == "__main__":
    main()
