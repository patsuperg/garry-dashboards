# PENDING DECISIONS — auto-generated
_Generated 2026-08-08 04:50 BKK (King, tab 4 session end). Extracted from THREADS.md._

## ⛔ NEEDS PATRICK

**1. 🔴 The inbox-monitor that emailed humans as you — off, or narrowed?**
`com.garry.inbox-monitor` sent **116 LLM-drafted replies from `patrick@spartansuppz.com` to
external humans**, 28 Apr → 6 Aug, then marked the threads read so neither side reached you.
Recipients included **support@sleek.com (your accountant, on the UHF Director Penalty Notice
remission)** and live Steadily policy threads. Iron rule #2. It is **contained, not deleted**:
the draft is still written and now escalates to you *with the draft inline*; sending is gated on
`data/inbox-monitor-autosend.json` and fails closed on 8/8 fault injections. Default stays OFF.
**Your call: off permanently, or narrowed to a named sender list.** Evidence:
`logs/autonomous-actions.jsonl` (`reply_sent=true`), commit `10bfd46`.

**2. Ciatto $532.24/mo — move off Wise onto Mercury.**
Largest recurring LLC payment, running on the rail you banned (Wise = FX only, never LLC money).
**Blocked on one thing only: the bank details exist solely inside Wise, so you have to read them
out once.** Build the Mercury instruction first, cancel the Wise transfer second — that order.

**3. The autopay arms + one 5-minute Ameren call — ~20-minute sitting, and the clock is on.**
Every click-path is written and staged: `Infrastructure/upgrade-findings/one-minute-taps.md`.
Money order: Ciatto $532.24 · Hazelcrest HOA **$264** (not $256) · MSD SmartPay ×3 · **City of
Lorain $92.71, due 2026-08-17** · Missouri American Water. Arming is iron-four, so it is your tap.
The Ameren MO one needs your voice for ID verification and cannot be automated — and per the
6 May evidence it should be **RETIRED, not fixed**: the account is deliberately in Avenue's name
and self-terminates at tenant placement. **You fly ~11 Aug; Lorain falls due after that.**

**4. 24 DocuSign signatures pending, oldest 87 days.**
1,204 escalations were raised and demoted to a board file; 0 emails reached you. The money route
is open now — the remaining call is whether signing joins the money markers. **King's answer: yes.**

## 🟢 RESOLVED SINCE LAST FILE — do not re-raise

- **✅ The $2,636 Evernest HAP is PAID.** Wise, **2026-08-05 22:01 UTC**, ref `081006167897406`.
  Receipt in **both** mailboxes (spartansuppz `19fd3f1ff9fcd4cb`, empinv `19fd3f208ac244cd`),
  body read by hand. Tim Hamilton confirmed the release ~1h *before* the bank credit
  (`19fd3b61a69ddd36`) — claim and bank agree independently. **There is no escalation to fire,
  and the one the watcher had armed for 9 Aug is disarmed.** It would have recommended an MREC
  complaint and small claims against a PM who had paid in full. Commit `99520b7`.

## 🟡 DECIDED EARLIER — still closed
- **`sales@spartansuppz.com` (36 GiB) dies with the domain.** Patrick: *"Nothing relevant there in
  sales inbox."* Closed. Never re-raise.
- **Allowlist:** gateway + Fenwick watcher enabled, money and dated deadlines only. Verified
  delivered (empinv `19fdc23e74ea532d`).
- **PDF/email deliverables** → `~/Desktop/Section 8 Empire Builder/` on the Mini. Standard, flat folder.

## ✅ CLOSED 2026-08-08 — three items retired on live evidence, none needed Patrick

- **Republic/Fenwick trash $78.45 — PAID, 2026-07-04.** Republic Services online bill pay, ref
  `558755124052`, account 303460526194, biller confirmation gmail `19f2bc15f03ee678`. Patrick paid
  it himself **ten minutes after** the gate recorded his approval; nothing wrote back, because until
  today no verb existed that could. The receipt is in **spartansuppz only** — that is why it read as
  unpaid for 35 days. Now: `payment-gate.py settle` exists and refuses without a receipt; the bill is
  `active: false`; and `scan_bills()` structurally refuses any bill carrying an `autopay` block, so
  the ~5 Oct quarterly cannot be put in front of Patrick on top of the autopay pull. **21 tests pass.**
- **Wilborn tax — PAID, 2026-04-20, $1,309.15.** Point & Pay order **#195993117** (gmail
  `19da98bfcd0376c1`): parcel `14G310103` $1,309.15 + parcel `11E520130` (Alcove) $1,900.11 + $27.28
  fee = $3,236.54, Visa ****4918. **One receipt, two parcels — only the Alcove line was ever read.**
  ⚠️ **The VOID is lifted, and it was wrong.** Confirmation #195993117 was recorded on 7 Aug as a
  *fabricated* receipt number. It is real. The subagent could not show its work and retracted its
  whole batch; the retraction swept up a claim that happened to be TRUE, and the void was then
  treated as proof of the opposite. Everything else in that VOID list still stands.
  **There is no remaining MO property-tax gap in the portfolio.**
- **The $2,636 Evernest HAP — booked, cash only.** The EVIDENCE-GAPS query was run and **neither
  branch applied**: Avenue's statements carry one Fenwick income line dated 2026-03 ($3,954.00 =
  exactly 3 × $1,318, payer "Resident") and **none** dated 2026-04 — but the statement prints no
  month against the $3,954 and Avenue never answered which months it covered. So the cash is booked
  to `Equity:Unattributed-Receipts`, not income. `owner_net_cash` 19,198.88 → 21,834.88 (+$2,636
  exactly); `operating_income` is now understated by exactly $2,636 and `metrics.py` says so every
  run. **Closes properly with one document: an Evernest statement covering 2026-04 → 2026-08.**

## ⚠️ NAMED UNVERIFIED — never upgrade these into assertions
- **Alcove judgment** — the watch file says none exists, memory says one was signed at $11,428.02.
  Neither mailbox holds the document. **Not asserting either way.**
- **Lorain tax** — the $1,467.26 **total** is receipt-verified; the split into components is a
  reconstruction and is not. Quote the total only.
- **15 of the 40 migration items** have no evidence in either direction — recorded as unverified,
  never as undone.
- **Mercury physical debit card** — absence of an arrival *email* is proven; the card may still be
  sitting unopened in the LegalZoom virtual mailbox. Those are different claims.
- **Drive / spartansuppz.com death date** — no termination notice exists in either mailbox; the
  deadline lives in the sale agreement, not in any readable system. **Do not move files.**

- [ ] 2026-08-08 · HAP share RED: alcove at 17% (observed_receipt, eff 2025-12-01). North-star is 90%+ — re-exam / re-tenant / confirm payee.  <!--HAP-RED-alcove-2025-12-01-->

- [ ] 2026-08-08 · HAP share RED: kenilworth at 29% (observed_receipt, eff 2025-01-01). North-star is 90%+ — re-exam / re-tenant / confirm payee.  <!--HAP-RED-kenilworth-2025-01-01-->

<!-- HAP-OVERDUE-MARKER -->
| 🟡 | **HAP overdue — 2026-08** | 4 properties unconfirmed as of day 8: 7596 Hazelcrest Dr Unit F, 5361 Wilborn Dr, 505 W 25th St, 124 Kenilworth Ave. Auto-flagged by avenue-payment-parser.py; clears itself once payment posts. | — |
<!-- /HAP-OVERDUE-MARKER -->
