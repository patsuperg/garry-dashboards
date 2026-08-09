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
- **The $2,636 Evernest HAP — BOOKED AS INCOME 2026-08-09.** Superseded the 8 Aug "cash only"
  entry. The blocker was Avenue's un-attributed $3,954 lump of 2026-03-20; it is **Sep+Oct+Nov
  2025 arrears**, not Mar/Apr 2026 — settled by month-elimination from statements already on the
  Mini, no chase to Avenue. Fenwick settled 2025-08-29 with `Rent Adjustment 0.00`, so the series
  is Sep-25→Jun-26 = 10 months; every other month is individually named in a primary source.
  `operating_income` 64,458.83 → **67,094.83**; recognised rent = **exactly 10 × $1,318**.

## ⛔ NEEDS PATRICK — added 2026-08-09, in consequence order

**A. 🔴 VERIFY MISSOURI FOREIGN-LLC REGISTRATION — before any Missouri eviction step.**
Empire Investing is an **Ohio** entity owning **four Missouri doors**. **RSMo 347.163** bars an
unregistered foreign LLC from *maintaining any action* in Missouri — **including an eviction** —
plus a fine of not less than $1,000, and Missouri's version is **not** framed as curable mid-suit
the way Ohio's is. **516 Alcove has a live eviction and an $11,428.02 judgment.**
⚠️ **Status is UNVERIFIED — do not assert either way.** Missouri SOS business search settles it.

**B. 🔴 City of Lorain $92.71 — due 2026-08-17, and he flies ~11 Aug.**
ACH autopay is 4–6 weeks out, so **this cycle is manual**. Faster than the paper form, same
sitting: `ipn2.paymentus.com/cp/lora`, acct **20830310-007**, switch on Auto Pay.

**C. ⏳ Segregate the pre-2027 pool — HARD EXPIRY 31 Dec 2026.**
Worth **7.5 years of Bangkok, tax-free. Costs $0.** Nothing else on this list has a cliff.

## 🟢 DECIDED 2026-08-09 — do not re-derive

- **TARGET REVISED: US$20,000/mo → US$14,000/mo net.** $20k is not reachable from A$1.2M by any
  structure modelled (crosses $20k nominal in year 31, never in today's money inside 40 years).
- **The portfolio ALONE never reaches $14k** — 40 years. $168k/yr ÷ 9.5% = **US$1.77M needed**
  against **US$804,038** controlled. **Gap ≈ US$970,000 of OUTSIDE capital.** With $100k/yr from
  ORION it is **16 years**; at $200k/yr, **10 years**. **The vessels are the tank; ORION is the fuel.**
- **PATHWAY LOCKED: P1 → P2, gated on measured collection.** Year-20 US$8,562/mo (88/100).
  Year one lifts him $1,098 → **$3,203/mo**. New doors **OHIO ONLY** — ⅓ the Missouri tax burden,
  and Ohio ceilings ROSE FY25→FY26 while 3 of 4 Missouri ZIPs FELL.
- **DEAD, do not re-propose:** the **Isle of Man bond / P3** (he said no return to Australia,
  ever) and the **A$45,000 term-deposit leg** (uncompensated FX risk).
- **The "no Android phone" screening rule is WITHDRAWN** — disparate-impact exposure under
  24 CFR 100.500. **The 500 credit floor stands.**

## ⛔ NEW — CARRIED FROM 2026-08-09, needs Patrick

**5. 🔴 City of Lorain utility $92.71 — due 2026-08-17, and you fly ~11 Aug.**
Approval alert delivered (empinv `19fe185d6248d31b`). ACH autopay is 4–6wk processing so it will
NOT be live for this cycle — **this one is manual, pay it before you fly.**
Faster than the paper form, same sitting: register at `ipn2.paymentus.com/cp/lora` under acct
**20830310-007** and switch on Auto Pay there — instant, no voided cheque.

**6. MSD sewer Fenwick $227.31 — due 2026-08-24.**
Acct 1505083-4. SmartPay enrolment started 27 Jul and stalled at the payment-method step; the
account is already registered and on eBill, it **only needs a card**.

**7. Wilborn MSD — $264.80 credit vs a collection agency chasing $265.09 on the SAME account.**
Acct 1507873. CCM / EvokePay code 14246853. **Do NOT pay them.** One call to MSD
1-866-281-5737 settles whether the credit is a refundable overpayment or a rate adjustment.

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

---

## ▶ ADDED 2026-08-09 20:50 (King, interactive-model window)

**THE INTERACTIVE MODEL IS LIVE — no decision needed, but he should open it.**
https://claude.ai/code/artifact/8c65dceb-20eb-4e20-837a-fa2f0a598674
13 sliders, 40-year projection, works on his phone. Emailed to pat@empinv.com only (his instruction),
read-back confirmed. The JS reconciles to `synthesis_model.py` to the dollar across 12 checkpoints and
re-runs that self-test live in the footer.

**❓ THE ONE QUESTION THAT SETS THE WHOLE TIMELINE — how fast can ORION realistically clear
US$100–200k/yr?**
Years to $14k/mo in today's money: $0→40 · $50k→23 · $100k→16 · $150k→12 · $200k→10.
Nothing in the structure work moves that number; only the business does. **If ORION is 2–3 years out,
the real question becomes how much of the A$1.2M funds the BUSINESS rather than door #7** — and that
is a different plan from the one currently modelled.

**Also now settled and needing no further work:** P3 / Isle of Man bond is DEAD (no AU return ever, so
ITAA s26AH — its entire thesis — can never pay). The A$45,000 AUD term-deposit leg is DEAD
(uncompensated FX risk against a currency he will never spend again).

---

## ▶ ADDED 2026-08-09 22:15 (Golf R listing photos)

**❓ Blur the number plate (1UH2EK) on the Golf R listing photos, or leave it visible?**
Most Melbourne Marketplace car ads leave it. Blurred copies not produced pending his call —
it's a 2-minute job either way, but the hero photo can't go live until this is answered.

**Not a decision, just so it's not lost:** 5 real photos are already in `~/Downloads/GOLF R PHOTOS/`
and the ad can go live on the two front 3/4 shots. Missing rear 3/4, side profile, **odometer total km**,
boot/rear seats, engine bay, damage — ~15 min with the car once he lands 13 Aug.

<!-- HAP-OVERDUE-MARKER -->
| 🟡 | **HAP overdue — 2026-08** | 4 properties unconfirmed as of day 9: 7596 Hazelcrest Dr Unit F, 5361 Wilborn Dr, 505 W 25th St, 124 Kenilworth Ave. Auto-flagged by avenue-payment-parser.py; clears itself once payment posts. | — |
<!-- /HAP-OVERDUE-MARKER -->
