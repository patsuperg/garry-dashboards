# PENDING DECISIONS — auto-generated
_Generated 2026-08-05 16:05 BKK (Chich)._

## ⛔ NEEDS PATRICK

**Nothing is blocking.** Every open gate from the last generation has been answered.

Resolved this session:
- ~~Second-pass agent cull~~ → **Patrick: "Kill soundbar, keep the rest."** Done, verified, archived.
- ~~Kenilworth rental assistance~~ → **Closed.** Tactical's attorney refused the pre-notice-arrears distinction outright and told Patrick to take it up with his own counsel. Patrick: *"noted, I replied to the Tactical girls already."* Not reopening — the arrears are structurally uncollectable.
- ~~$375 Painesville rental registration~~ → **already approved 29 Jul.** Do not re-ask.
- ~~B2B's proposed resolution~~ → **Patrick's verdict: absurd, waste of time.** Deadline stands at 15 Aug.

Still parked, not blocking:
- **Alcove collections placement** — judgment now signed, but expected recovery is 0–5% (no wages, no voucher once terminated). **Recommendation: don't place it.** Collection costs exceed the return on this profile.
- **Tactical + B2B AppFolio portals** — unreachable; Twilio 334 deletes inbound OTPs. Mine to fix.

## ⏳ WAITING (tracked in ops.db — `obligations.py list`)

| Amount | Who | What | Action date |
|---|---|---|---|
| **$14,920.05** | Seth Alden → Ralph (B2B) | Final position. They accepted the deadline in writing. Offer on the table is **$575 (3.9%)**. | **Chase 14 Aug** |
| **$2,636** | Tim Hamilton / Jenna (Evernest) | Fenwick Mar+Apr HAP. Committed to "EOD Wed 8/5". | **Verify Thu 6 Aug** |
| **$1,278** | Demetia Williams (RU Partners) | 505 Lorain Dec 2025 HAP. Handed over 4 Aug, no substance yet. | **Chase Thu 6 Aug** |
| **$11,428.02** | Avenue / RHF Legal | Alcove consent judgment. Vacate 8/31. | **Occupancy check 9/1** — expect **$0** cash |
| — | Angel Chaney (Tactical) | **Kenilworth 3-Day date still unconfirmed.** Patrick asked 10 Aug; Angel floated 1 Sep. This 3-week slip is the only remaining lever on the property. | **Chase** |

## 📅 DATED, ALREADY BOOKED (Reminders app + Apple Note, both verified)

- **13 Aug — Melbourne landing, 9 tasks.** Golf R: book RWC (~$200–250, allow a re-test — **it is promised in the live ad**), exact odometer, service history into the ad (worth ~$2k), rim + tyre specs, do the original wheels exist, downpipe brand, 6 missing photo angles. Plus: list the Fiat 500. Plus: cancel Ozicare the day the Golf R sells.
- **24 Aug — price review, all Marketplace listings.** All 39 items carry `drop_date 2026-08-24` + a `drop_price`, but nothing was scheduled to action them. Golf R sits outside `items.csv` — review separately (ask $29,990 · target $28,000 · floor $24,000).

## 🔧 CHICH'S TO FIX (do not surface)

- `com.chich.appfolio-reauth` exit 1 — SMS throttled by AppFolio after repeated code requests. Backoff patch applied 5 Aug; the 16:30 run is the test. Self-resolving or I fix it again.
- Root cause of Gem's original SIGKILLs still UNKNOWN. Do NOT assert a cause without swap + jetsam evidence (LEARNING-LOG L-2026-08-05-A).
- One state store, one writer (40 writers currently).
- Facts store w/ provenance · remediation daemon (both approved, not built).

---

## 💰 ADDED 2026-08-05 16:50 (Chich) — portfolio reconciliation

**⛔ NEEDS PATRICK — 1 gate only:**
- **Avenue: what is being terminated, and effective when?** July statement is headed *"Final
  Statement per management termination request"*; Patrick has zero knowledge of it. Swept both
  mailboxes, all 6 statements and the whole portal — nothing corroborates it. Letter **DRAFTED,
  NOT SENT**: `Outputs/Avenue_PMA_Audit_Letter.md`. **Fenwick's lease ends 31 Aug — that is the
  clock.** Say "send it" and it goes.

**🔧 MINE TO CLOSE — not blocking, no approval needed:**
- **~$2,678 of 2025 MO property tax with no payment evidence** (Alcove ~$1,556.69, Wilborn
  ~$1,121.57). Hazelcrest proven paid; Fenwick probably. MO penalty + interest from 1 Jan, then
  a lien. Verify both parcels directly.
- **No Lorain County tax payment for 505 W 25th in any feed, ever** + $574.76 delinquency.
- **Wilborn basement** — vendor now recommending full floor reconstruction. Get written findings
  before anyone scopes it; hold the epoxy/seal decision already made.
- **$734 to Avenue** — reserve top-up, not the repair. Their own staff said no contribution
  needed for the bill. Do not pay before the termination question resolves (escrow is refundable
  within 30 days of termination under PMA cl. 9).
- **20% project fee (~$954)** — confirm it is waived on the $4,420 Wilborn job.

---

## ⚡ ADDED 2026-08-05 17:40 (Chich) — Claude Code perf fix

**⛔ NEEDS PATRICK — 2 items, neither is money:**
- **B6 Bangkok cost-of-living figures** — his ACTUAL dated numbers (condo all-in, transport,
  groceries). **51.3% of the Mikey advantage rests on it and it is currently anecdote.** Lean matt
  will ask in one line; it must not block the Engine build.
- **Restart the two old iTerm windows.** MCP config changes only take effect on a NEW session, so
  those windows stay slow until they cycle. New windows are already fast.

**🔧 MINE TO CLOSE — not blocking:**
- `hooks/block-unapproved-send.py` **false-positives on plain file writes** — it keyword-matched
  "emailed" inside a Bash heredoc writing THREADS.md and blocked it as an outbound send. Guarding a
  money/contact path, so not loosened unilaterally. Should match actual send *tool calls*, not text.
- `~/.claude/CLAUDE.md` RULE 3 cites **`com.chich.session-reconcile` every 15 min — that agent no
  longer exists** (retired in the 140→100 cull). The rule points at a dead service. Correct the doc.
- `com.patrick.section8-daily-deals` exit 1 (new, alongside the known appfolio-reauth).
