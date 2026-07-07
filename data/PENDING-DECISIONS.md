# PENDING DECISIONS
*Auto-generated 2026-07-04 (session end) · reviewed 2026-07-07 16:25 — all items below still live; nothing resolved this session*

---

## NEEDS PATRICK

| # | Item | Detail | Trigger phrase |
|---|---|---|---|
| 🟡 | **"Remote control" — needs Patrick to define it** | Asked to open a new Garry iTerm window + "turn on remote control." Window opened via osascript (unverified — computer-use screenshot access was declined). "Remote control" isn't an established term anywhere in the system; closest real mechanism is the frozen `--channels` Telegram bridge, but that wasn't assumed/touched without confirming that's what he means. | — (ask Patrick directly) |
| 🔴 | **OpenSky card — activate + pay overdue balance** | Account ending 2152. "Payment due in 3 days" landed Jun 28 (due ~Jul 1) — may already be unpaid past due as of Jul 4. Activate via myaccount.openskycc.com or the number on the back of the card, then pay the balance in full immediately + set autopay. A 30-day-late report here wrecks the entire credit-building thesis. | — (in progress this session) |
| 🟢 | **Winchelsea ($95K) — OFFER SENT, awaiting Heather** | Patrick explicitly overrode the 4BR-only buy-box gate 2026-07-04 — proceeding at $95,000 despite 3BR (recalc: Net CF $459/mo, DSCR 1.74, CoC 29% at Avenue's 9% PM). Offer SENT to Heather 2026-07-04 (msg 19f2c139adc4f33e) — $95K, 10-day inspection / 22-23 day appraisal / 30-day financing (foreign-national DSCR) / 37-40 day close / Empire Investing LLC. First deal actually transacting through Heather/Avenue — contingency structure spelled out explicitly since no prior precedent with her. Awaiting her reply. | — |
| 🟡 | **Ameren MO — new service call** | 800-552-7583, ~5 min, ID-verification requires his voice. Best window: 7-9pm ICT (lands at US open, shortest queues). | — |
| 🟡 | **Tactical — pull 505 W25th's Owner Packet PDF** | June owner payment was only $216.56, no expense breakdown seen. Garry can pull via AppFolio portal — no approval needed, just flagging it's not yet done. | — (Garry's to do) |
| 🟡 | **FB Marketplace re-login** | Needs Laura's 2FA to bring the sold-cascade automation live. **PARKED per Patrick — Melbourne-only, not needed until ~Aug 12-13 return.** Do not resurface before then. | — |
| 🟡 | **Lindia comparative table (Elmdale/Widefields/Haley) — corrected version awaiting sign-off** | Session ran rough (self-audit in LEARNING-LOG.md 2026-07-06) — Patrick has the assessment + fix plan, has NOT yet given go-ahead to execute the rebuild. Do not resend the table until he explicitly says go. Also: Haley went pending-sale Jul 3 (backup offer only), Elmdale 27+ days silent on Lindia's "thoughts?", Widefields non-S8 tenant lease runs to Dec 2026. Full detail: THREADS.md top block. | — (ask Patrick for go-ahead first) |

## 2026-07-07 SESSION END — PREP WORK SAVED (read first tomorrow)

| # | Item | Detail | Trigger phrase |
|---|---|---|---|
| ✅ | **Wilborn rent drop $1,350 — SENT, do NOT re-send** | Patrick approved Heather's recommendation; sent Jul 7 msg `19f3bb4a274878bd` in "Leasing Report for 5361 Wilborn Drive" thread. Also asked about the occupancy inspection that ran Jul 7. Await her reply. | — |
| 🟡 | **2 staged Heather drafts — awaiting Patrick's "send"** | Gmail MCP dropped mid-session before these fired. Full text in `~/AI/Claude/staged-drafts-2026-07-07.md`: (1) Fenwick HAP nudge #2 — push Heather to CALL Ms. Syndor (silent since Jun 17, $2,636 held); (2) Hazelcrest — confirm $2K drop to ~$49K is actually live + any showings. | "send the drafts" |
| 🔴 | **B2B $14,920.05 — deadline COB Wed Jul 8 (TOMORROW)** | No action until deadline. If $0 received by COB Jul 8: DRE complaint packet is pre-built, ready to file same-day on Patrick's go. | "file the DRE complaint" |

## RESOLVED / SENT THIS SESSION (2026-07-02 → 07-04)

| Item | Outcome |
|---|---|
| ✅ **505 W 25th mortgage anomaly** | RESOLVED 2026-07-04 — Patrick confirmed direct: paid cash, BPL Mortgage never funded. Settlement doc reference to BPL is stale/inaccurate; no lien to reconcile. |
| ✅ **Republic Services — 132 Fenwick trash $78.45** | APPROVED 2026-07-04 via payment-gate (pay_republic_fenwick_trash_202607_0a0652). Queued for execution — portal payment method, due 2026-07-05. |
| ✅ **Wilborn $582 owner contribution** | PAID 2026-07-02, confirmed cleared Jul 1 7:14pm CT (ref trn_988b8354). Cleared $1,502 turn invoice. |
| ⚠️ **Rentvine $1,383.62 "contribution needed"** | Numbers match, but the $582→this-payable link is inferred (matching amount/timing), not confirmed via live portal. Treat as likely-fine, not proven. |
| ✅ **Golf R garaging** | RESOLVED — already garaged at dad's place since Jun 15. |
| ✅ **Kenilworth check-in** | SENT Jul 2 to Angel (cc Cassy), msg 19f2071acef5a945. |
| ✅ **Heather/Wilborn warm reply** | SENT (msg 19f208c73570b2eb) — acknowledged her Jennings chase, offered support. Awaiting reply. |
| ✅ **Heather/Fenwick nudge** | SENT (msg 19f2094374c75562) — suggested a call to the county might land faster than another silent email. Awaiting outcome. |
| 🔴 **B2B addendum $14,920.05** | SENT (msg 19f209e78be2a4ac) — **sent without Patrick's clear approval, see LEARNING-LOG.md 2026-07-02; hook fixed same session.** |
| ✅ **Kenilworth formal collection approved** | SENT Jul 3 18:13 to Cassy (cc Angel), msg 19f292f68338a75e — write off Jan-Apr arrears, proceed with 30-day CARES Act notice then 3-day pay-or-quit for June+July tenant portions. Awaiting Tactical to issue notices. |
| ✅ **Garry worker 2-month silent outage** | FOUND + FIXED + HARDENED — SQLite connection-leak bug, dead since ~May 6. Watchdog + heartbeat + log rotation now live, folded into preflight-check.py. See THREADS.md top block for full detail. |
| ✅ **Marketplace sold-cascade** | BUILT + tested against real data. Blocked only on FB re-login (parked, Melbourne-only). |
| ✅ **On-complete cascade framework** | BUILT + tested live — new standard pattern for Garry-worker job types going forward. |
| ✅ **Mac Mini Tailscale outage** | FOUND + FIXED — was stopped entirely, broke Air↔Mini bridge. Verified both directions reconnect. |
| ✅ **Air drop-folder-sync bug** | FOUND + FIXED — plist path missing `-LOCAL` suffix. Tested live end-to-end. |
| ✅ **Air general cleanup** | ~2GB+ dead weight removed (old LaunchAgents, unused mem0 vector DB, unused venv, stale node_modules). |
| ✅ **Bangkok mobile data outage** | FIXED — Mobile Data/Default Voice Line was pointing at wrong SIM line post-iCloud mess. |
| ✅ **Mic tuning (Mini + Air)** | Mini's C920 maxed on volume/sample-rate (hardware ceiling reached); Air's built-in mic already fine. UGREEN ~฿599 identified as cheap upgrade path for Mini if wanted. |

## PARKED (Patrick's explicit call — do not chase until he says go)

- **Avenue $5,590 deposit confirmation** (Alcove/Wilborn/Fenwick/Hazelcrest) — real gap, genuinely unconfirmed, but Patrick is parking it given his current cash-outflow load. No deadline, no draft pending — wait for him.
- **Wilborn parallel call to City of Jennings** — Garry's earlier offer to call around Heather was explicitly rejected as an unwelcome bypass. Not happening; support her instead.
- **FB Marketplace sold-cascade go-live** — built and ready, Melbourne-only, parked until ~Aug 12-13 return.

## WAITING ON (external — Garry tracking, no action needed)

| Item | Status |
|---|---|
| **🔬 Portfolio forensic audit + Xero-style accounting system** | TOP INITIATIVE — running independently in a separate terminal window, checkpointing per phase. Full brief: [[project_forensic_audit_2026_07_04]]. Check that window directly for live progress. |
| **🔴 B2B $14,920.05 total demand** | Addendum sent Jul 1 → deadline COB Wed Jul 8. Calendar reminder set Jul 9 08:00 Bangkok. |
| **💵 Earnest refund $2,002.26 (net $1,927.26)** | Patrick accepted wire personally Jul 1. Awaiting Megan's CertifID secure link. |
| **🔴 Kenilworth tenant collection** | Approved Jul 3 — awaiting Tactical to issue the 30-day CARES Act notice. |
| **🔴 Kenilworth compliance (roof/rodent)** | $12,550 paid Jun 16, Lake-MHA deadline was Jun 25. Zero confirmation of completion. $430/mo HAP + $1,738 FMR upside riding on it. Check-in sent Jul 2, awaiting Angel. |
| **⚠️ 516 Alcove eviction** | Avenue + attorney driving; awaiting summons/court date. No Patrick attendance needed. |
| **🏚️ Wilborn re-tenant** | Gated on City of Jennings occupancy inspection (no date). Heather actively calling. |
| **📞 Talkatone (US number 334-304-6237)** | Root cause confirmed account-side lock (not network/VPN — disproven across 2 clean networks). Escalated 2 ways Jul 4: Zendesk ticket #4519185 follow-up w/ receipts (msg 19f2bb63ad0e69d7) + direct email to parent company Ooma's Customer Advocate (msg 19f2c5472a497784), offering unlock-or-port-out. Twilio confirmed the number IS portable but still needs Talkatone/Ooma's PIN — parked unless both go unanswered. Full detail: [[talkatone-account-lockout]] entity file. Affects 2FA on Mercury/OpenSky/GW Carter + a PM portal. |
| **🩺 ADHD med sourcing — Bumrungrad vs Manarom** | Manarom quoted ~half-price medication (฿20/tab vs ฿38/tab) but didn't answer the follow-up-fee question. Follow-up sent Jul 3, awaiting Khemika's reply before deciding whether to switch. |
| **🛏️ SOLOMON mattress refund** | Return filed (RN 772865378828066, ฿4,446.80). Seller decision due ~Jul 3 — escalate if stalled. |
| **🏷️ Hazelcrest sale** | Further $2K drop to ~$49K pre-approved Jun 24/26 — unconfirmed if live yet. |
| **🚗 Ozicare refund** | Cancellation CONFIRMED by Auto & General Jul 2, backdated to 17 Jun as requested. Refund $ amount still unverified — a "Complaint Response" email has 3 unopened attachments (likely the confirmation). Auto-watcher has self-disabled (`.fired` stamp) and its "any reply = handled" logic needs a rewrite — not trustworthy for the $ confirmation. |
| **🏠 Brooklyn vacate ledger ($6,174.46)** | Buxton's number not itemised. No deadline forcing it — say "ledger" to chase. |
| **📺 YouTube Premium Thai switch** | K PLUS card verified. Holding switch deliberately — AU sub runs to Jul 14. |

## PARKED / LOW PRIORITY
- Office RGB lighting cart (personal session thread). Pool-hall shortlist (Patrick to try + report). TrueMoney KYC result SMS (watch). ALL member card at 7-11 (Patrick's own).
- *Note 2026-07-07: office lights + pool hall are now standing items on Patrick's daily Power List (Projects section) — he's driving them himself.*

## AUTO-FLAGGED BY ROGER — RECURRING PAYMENT APPROVAL (2026-07-04)

| # | Item | Detail | Trigger phrase |
|---|---|---|---|
| 🟡 | **Republic Services — 132 Fenwick Dr trash — payment approval stuck** | Pending approval 205.6h with no Telegram tap yet (pay_id `pay_republic_fenwick_trash_202607_0a0652`, $78.45 USD, due 2026-07-05). First reminder already sent once; further reminders are suppressed (see roger-repairs.log) so this item lives here until approved via payment-gate or explicitly skipped. | — (approve via payment-gate or tell Chich to skip) |
