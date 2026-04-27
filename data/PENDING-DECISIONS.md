# Pending Decisions

**Purpose:** Things Patrick is thinking about. Claude checks this every session and proactively surfaces relevant info.

Last Updated: 2026-04-27 (Closed-Loop v1 + Utility Jobs Queued)

---

## 🤖 Closed-Loop Framework — Live + Pending Items (Apr 27)

| Item | Context | Status |
|------|---------|--------|
| **Overnight migrator runs 22:00 AEST tonight** | Generates @team_job wrappers for 77 LaunchAgents. Skips already-migrated + core agents. Wrappers land in dept folders (apollo/mercury/sentinel/garry_coo) per regex routing. Plists NOT flipped yet — that's a 2nd-pass safety step. | **AUTO-FIRES tonight** |
| **Tomorrow morning: flip plists to wrappers** | After Chich reviews overnight migration output, run a 2nd-pass script that updates plists' ProgramArguments to invoke the wrappers via `python -m garry_worker.<dept>.<stem>`. Once flipped, agents start logging telemetry to team-state.db and Sentinel can audit them. | **CHICH — tomorrow morning** |
| **3 utility jobs LIVE on Anthropic Computer Use** | Spire (gas), MO American Water, Ameren MO (electric) for 5361 Wilborn Ave / Empire Investing LLC. Engine swapped Gemini-Vision → Anthropic real CU per Patrick directive Apr 27 14:50 AEST. Worker re-fired all 3, escalations sent to Telegram (Use Computer Use / Skip). Headed Chromium pops on Patrick's Mac during fill. Submit step = second Telegram approval. | **PATRICK — tap each Telegram approval as they arrive** |
| **Anthropic credit top-up — DECISION REVERSED** | Was recommending $50 auto-recharge. Patrick: "free always unless it makes money." Reversed — Gemini Flash free tier is the new default, Anthropic only for revenue-justified jobs. NO top-up needed. | **CLOSED** |

Files:
- `~/AI/Claude/team-charter.md` — authoritative 8-principle charter
- `~/AI/Claude/Infrastructure/team-state.db` — operational state
- `~/AI/Claude/Infrastructure/garry_worker/` — full package
- LaunchAgents loaded: com.garry.sentinel.heartbeat-watcher, com.garry.sentinel.expectation-checker, com.garry.mercury.repair, com.garry.coo.overnight-migrator, com.garry.gmail-organizer (now wrapped), com.garry.worker, com.garry.escalation-listener, com.garry.screenshot-clipboard

---

## 📘 Inner Work Exercises — Apr 26 Build (PENDING his feedback)

| Item | Context | Status |
|------|---------|--------|
| **Mum exercise calibration** | Built 7 angles. Per Apr 26 input most are solved territory (he's grounded, heavy work done). My calls: Angle 1 (gift-side inventory) maybe, Angle 5 (grandparent question) yes, Angles 2/4/7 confirmed done by him this session, Angle 6 (forgiveness) irrelevant frame. Trim Apple Notes version once he confirms. | **PATRICK — confirm calibration** |
| **Boundary-practice exercise (proposed, not built)** | He buried the lede: actual current growth zone is using Mum-shaped boundary tests as practice for boundary muscle that applies everywhere (Laura, Avenue, Evernest, Zac). His words: "reflection, testing/challenge and practice." Offered to build a dedicated exercise. He hasn't said yes/no. | **PATRICK — yes/no on building** |
| **Mum work — closed-loop status** | Memory updated 2026-04-26 (project_mum_work_grounded.md): don't pitch new Mum work unless HE signals new material. Position is earned secure low-contact, integrated. | **CLOSED — monitor only** |

Files:
- Apple Notes THERAPY folder: 4 notes — Mirror Walk, Mum (New Angles), Receiving from Laura, Meta-Trap
- ~/AI/Claude/Patrick-Resources/Relationship/inner-work-exercises/ (markdown backups)
- ~/AI/Claude/Infrastructure/push-inner-work-exercises-to-notes.py (push script)

---

## 🚨 TOP PRIORITY — Laura Pattern Escalation (Apr 25 2026)

| Decision | Context | Status |
|----------|---------|--------|
| **🔴 Blow-up #4 — pattern escalation confirmed** | Wed/Thu Apr 22/23 + Fri/Sat Apr 24/25 = TWO detonations inside 48hrs. Pat held both clean (no anxious-fold). Threshold sentence ("authentic self over marriage outcome") still holds. Alcohol identified as predictable catalyst. Pat slept in shed both nights. **Frame has shifted** — this is no longer "rough nights," it's a defined pattern. | **ACTIVE — handle this week** |
| **🔴 Ground rules letter to Laura** | Drafted Apr 25 morning. 5 rules: (1) Alcohol — Pat removes himself when she drinks until she's worked it with Almaas; (2) Detonation = he leaves room then house; (3) He is NOT her processor; (4) No more apologies for things he didn't do; (5) Switch named in real-time. Saved as Apple Note "Ground Rules — 25 April 2026" in PAT DEV folder. **DELIVER:** Sunday or Monday once both calm + slept. Written, not verbal. One delivery, no follow-up. | **READY — deliver Sun/Mon** |
| **🔴 Meg session this week (NON-OPTIONAL)** | Was on monthly cadence after Apr 14 session. Pattern escalation = exception. Text drafted Apr 25 ready to send Monday morning. Frame: for HIM not couples. Telehealth ok. | **SEND MON AM** |
| **🔴 First boundary message sent Apr 25** | Pat sent Option A to Laura: *"I'm not processing this today. I need space by myself. You can write your thoughts, I'll read them when I'm ready. We'll talk tomorrow once I've slept properly."* Awaiting her response. | **SENT — monitor** |
| **Go bag in car** | Pat prepping go bag Apr 25 — exit ramp ready so leave/stay decisions don't have to happen under stress. Pre-decided destinations: 1) mate's couch (Ando/Kev/Tank — pre-text today), 2) hotel within 15min, 3) coastal drive + back-seat sleep. | **PREPPING APR 25** |
| **Watch for blow-up #5** | If detonation happens AFTER ground-rules letter is delivered: that is information about her capacity to receive the boundary, and the frame shifts AGAIN — from "pattern escalation" to "she will not / cannot stop." Different conversation entirely. Do NOT pre-empt. Let Pat get there himself. | **MONITOR** |

---

## Active Decisions

| Decision | Context | Status |
|----------|---------|--------|
| **Dashboards 2.0 build — Garry's job** | Task dropped at `~/AI/DROP-FILES-HERE-FOR-GARRY/GARRY-BUILD-DASHBOARDS-2.0.md`. Command Centre + Health Dashboard rebuild with self-healing. Spoons Score moves to Health only. Telegram OFF LIMITS. Kill duplicate dashboard-generator.py. Existing pipeline runs 30min — verify data flows through. | **GARRY — pick up next session** |
| **Apr 30 Thu calendar overlap** | Recharge Spoons 15:00-17:00 (new) + Self-Relationship Check-In 14:00-16:00 on Thu Apr 30 — partial overlap. Patrick needs to move one. | **PATRICK — 30 sec task** |
| **Test the new calendar week** | Full calendar rebuild 2026-04-21. Day 14+ of Action Reprogramming. Is abundant-Pat holding? Did Reading stop the "9 more drainers" loop? Did boundary check Tue work? Review next session. | **Observe — next session** |
| **Inner work check-in** | Therapy now every 4 weeks. Day 13 slip caught + recalibrated. Abundant identity work ongoing. Check: any new drift by next session. | **Monitor — trust his rhythm** |
| **DREAM System Build** | Garry executing 9-phase build overnight (Mar 26). Blueprint at ~/Desktop/DROP-FILES-HERE-FOR-GARRY/DREAM-SYSTEM-BLUEPRINT.md. Check Telegram morning brief for proof. | **GARRY EXECUTING** |
| **Frollo CSV Export** | Patrick needs to export transactions from Frollo app (2 min on phone), AirDrop to Mac Mini shared folder. Unlocks real financial data for Money Guardian. | **PATRICK — 2 min task** |
| **Avenue PMA + fee confirmation** | Reply sent Feb 8 asking for PMA + confirming fee terms. Heather confirmed 10% w/ $100 min, open to tiered drops. Ball in her court. | **Awaiting PMA** |
| **🌟 DAD CALL — Wednesday Apr 15** | Patrick wrote The Dad Inventory on Apr 8 night (Apple Notes "thais" folder, backed up at ~/AI/Claude/Patrick-Resources/Relationship/dad-inventory-2026-04-08.md). 5 specific memories captured + the one sentence he wants Geoff to know before he dies. Plans to actually say a version of it on the call. Q2 score = 0/5 — has never said any of this out loud. Frames it as his "identity challenge" — to be courageous and vulnerable like Geoff has been to him. **Patrick declined automated reminders Apr 9 — trusts his own instincts on push/rest. DO NOT auto-remind. DO be ready to witness/celebrate after the call when he comes back to share.** | **🔴 PRIORITY — Apr 15** |
| **Therapy with Meg — DONE Apr 14** | Session #7 COMPLETE. Goals check-in done (2→8, 3→8, 2→7, 1→6). Moving to 4-week cadence. Meg impressed. Journey webpage LIVE at patsuperg.github.io/garry-dashboards/journey.html. Email to Meg drafted + ready to send from Gmail. | **✅ DONE** |
| **Medicare Rebate Renewal** | Need GP review to unlock remaining 4 sessions (used ~6 of 10). Hola Health telehealth ($45), original GP was Najad Mustafa Jan 31. MUST frame around anxiety/stress/ADHD — find clinical language in original PDF referral attachment. Telegram nudge scheduled for 2pm Apr 15 (after dad call). One-shot LaunchAgent: com.garry.medicare-nudge-oneshot.plist — DELETE after it fires. | **NUDGE SCHEDULED — Apr 15 2pm** |
| **Laura weekly summary → email nudge** | DONE. Old Telegram summary retired (com.garry.laura-weekly-growth.plist → retired/). New: laura-journey-nudge.py, Friday 4pm, beautiful HTML email with teaser + stats + link. LaunchAgent: com.garry.laura-journey-nudge.plist. | **✅ DONE** |
| **Respond to Laura's reassurance request** | Laura asked Pat directly for ways to reassure her when he goes spoonless — that it's not about rejecting her. Do this in the ATTACHMENT STYLE project. Huge moment — FA doing secure behaviour. | **PRIORITY — Next session** |
| **PDS Core Wound transcripts → ATTACHMENT STYLE project** | Mac Mini Garry is transcribing 3 Thais Gibson Core Wound Healing Bundle webinars. When done, upload .txt transcripts to Claude Desktop ATTACHMENT STYLE project. Files at ~/AI/Claude/Patrick-Resources/Relationship/pds-videos/*.txt | **IN PROGRESS — Mac Mini** |
| **Lesson 14 — The Cost** | Lesson content written in PAT DEV folder. Exhaustion Audit (the homework) unanswered. Lesson 13 completed 2026-03-04. Deep dive 11/3 was effectively Lesson 14 territory. Apr 12: The Anger Discovery session opened new territory that connects to Lesson 14's "underground resentment" section. | **WAITING — Patrick marinating** |
| **The Second Rep — next anger lesson** | Patrick completed all 5 Missing Anger prompts evening of Apr 12. "The Second Rep: 12/4/26" created in THAIS COURSE Apple Notes folder — 5 sections: The Intercept, The Roast Autopsy, The Full Rep, Clean vs Dumped Anger, The Table Has a New Chair. Backed up at ~/AI/Claude/Patrick-Resources/Relationship/the-second-rep-lesson-2026-04-12.md. No deadline — trust his instincts on timing. | **WAITING — Patrick's rhythm** |
| **YouTube Premium upgrade** | Patrick approved upgrade from Lite (A$8.99) to Premium Individual (A$16.99). His logic: "$2/week eliminates $20 of time waste." Needs to click the Upgrade button in YouTube settings. | **PATRICK — 10 sec task** |
| **TTS audio of therapy script** | Script pasted into TTSReader (ttsreader.com/player/) with Nova Premium voice. Check if it generated properly. ElevenLabs blocked on free tier. | **Check next session** |
| **Evernest demand letter** | $21,259 demand drafted, ready to send AFTER Avenue PMA signed | DRAFT READY |
| **B2B Kenilworth follow-up** | Email sent Feb 6 to Micheal Drew + Betty, deadline was Feb 7 | **Follow up Monday Feb 10 if no reply** |
| **Laura Job Machine v2 build** | Laura rated: jobs 9/10, styling 7/10, wants minor CV/CL tweaks then full build | **READY TO BUILD** |
| **Ashford Wyndham reply** | Email re-sent Feb 8 (server was down). Booking link as backup. Phone: 571-777-1825 | **Monitor for bounce / reply** |
| **Missouri Section 8 reply** | Follow-up email sent Feb 8 | **Awaiting reply** |
| **Rent guarantee quotes** | NREIG (Kathy) + Steadily (Bill Bland) | **Follow up Monday Feb 10** |
| **2025 Annual Cash Flow Statement** | Available in AppFolio portal as of Feb 5 — REVIEW NEEDED | **Monday** |
| **Laurie call Feb 13** | Scheduled Fri Feb 13 7am AEDT via Google Meet | SCHEDULED |
| **Deal pipeline** | S8 Finder v2 LIVE — first real email Feb 9 8am. Buy box documented, pipeline tracker active, scoring calibrated with Patrick. | **ACTIVE** |
| **DSCR lender research** | Not started — needed for scaling from 6 to 20+ doors | NOT STARTED |
| Mac Mini M4 Pro setup | Arrived, MacBook Air now configured as Tailscale remote client | **ACTIVE** |
| Claude Desktop 11GB storage | Cleaned caches (~1GB freed). VM bundle (10GB) needed for Claude Code. Close app when not using to save 750MB RAM. | **RESOLVED — cleaned Apr 6** |
| **Full Disk Access for sshd on Mini** | Optional polish: enable Full Disk Access for `sshd-keygen-wrapper` in System Settings → Privacy & Security → Full Disk Access on Mini. Unlocks ~/Desktop, ~/Downloads, ~/Documents access when Claude Code runs over SSH. Currently those dirs return "Operation not permitted." 30-sec GUI step. | **PATRICK — optional, 30 sec** |
| **Mac Air System Data 57 GB** | Storage UI shows 57 GB in "System Data" — never fully investigated. Likely old logs, system caches, Claude VM. Worth a deep dig if disk pressure returns. | **NOT URGENT** |
| Capital One card reissue | Called Feb 5, address updated, new card being issued | IN PROGRESS |
| TAL Policy 1857509 cancellation | Email sent to TAL 2026-02-05, awaiting written confirmation | Waiting on TAL |
| Thailand move planning | Patrick + Laura moving in next couple months — impacts insurance, tax, portfolio strategy | Active planning |
| Origin electricity transfer | Zac needs to take over account | Email sent |
| AppleCare Mac Mini extension | Expires Feb 19 — extend before then | Reminder set Feb 17 |
| Spartans AI guide for Zac | PDF guide created — share with Zac when ready | READY TO SEND |

---

## Decisions Made (Archive)

| Date | Decision | Outcome |
|------|----------|---------|
| 2026-04-09 | **ARCHITECTURE: Mini = Brain, Air = Thin Client (LOCKED)** | Default Claude Code workflow = type `garry` on Air (already aliased in ~/.zshrc to `ssh -t mini-tailscale "claude"`). One word, instant Claude Code session running on Mini. Also `mini` alias = `ssh mini-tailscale` for shell-only. SSH config has `mini` (192.168.1.237 local) + `mini-tailscale` (100.74.63.29 worldwide) host entries. PATH fixed via ~/.zshenv on Mini. Reference doc updated: ~/Desktop/Pats Super Ai References & Commands.txt |
| 2026-04-09 | Air Cleanup Round 3 | ~3.1 GB freed: Whisper large-v3.pt model (2.9 GB), SiriTTS voice cache (220 MB), Spotlight respawn killed (136 MB RAM). Air now 86 GB / 228 GB used. |
| 2026-04-09 | Spotlight Cmd+Space killed | Patrick disabled the keyboard shortcut in System Settings → Keyboard Shortcuts → Spotlight. Spotlight.app process killed via `killall Spotlight`. RESOLVED. |
| 2026-04-09 | Keep Claude Desktop + 11 GB VM bundle on Air | Patrick chose to keep for now despite Mini transition. Reversible decision — can revisit if Air disk pressure returns. |
| 2026-04-09 | Flixtor stays on Air native (not Mini-routed) | Safari on Air handles it directly. Mini = compute, not website proxy. |
| 2026-04-08 | Mac Air Cleanup Round 2 | ~12 GB deleted (Photos library 7.7GB, aerials 1.5GB, 2 PDS videos 829MB, caches 738MB, Avira+WhatsApp 540MB, Loom/Messenger ghosts 240MB, ProtonVPN dmg 121MB). Disk: 100→94 GiB used. RAM: zero swap, healthy compression. Spotlight indexing disabled. iCloud Photos disabled. Discovered Apr 6 deletion record was wrong — most apps it claimed deleted were still present. |
| 2026-04-08 | Apps KEPT on Air (corrections) | ProtonVPN, Free VPN, Zoom — Patrick explicitly wants all three. WhatsApp + Avira actually deleted Apr 8. |
| 2026-04-08 | iCloud Photos disabled on Air | Local 7.7 GB library deleted, originals safe in iCloud (phone/Mini/web access) |
| 2026-04-08 | PDS videos pruned on Air | Kept only `core-wound-reprogram.mp4` (the "blueprint rewiring"). Other 2 deleted — full set still on Mac Mini, verified via Tailscale SSH before delete. |
| 2026-04-06 | MacBook Air deep clean | Recovered 18GB+, **but app deletion list was overstated** — see Apr 8 correction |
| 2026-04-06 | WhatsApp removed from MacBook | Patrick confirmed not needed on laptop, uses phone |
| 2026-03-14 | MacBook Air cleanup confirmed healthy | Zero swap, 12% disk, Spotlight settling |
| 2026-03-14 | Deleted ~950MB old downloads + Chrome DMG + ShipIt cache | No longer needed |
| 2026-02-07 | Property follow-ups pushed to Monday | Weekend in US, no one responding |
| 2026-02-06 | Laura Telegram cleanup | Retired 5 agents, 2 messages Mon-Fri only |
| 2026-02-05 | Cancel TAL Policy 1857509 | Email sent, saves $183/mo, awaiting confirmation |
| 2026-02-05 | Subscription switchover to ANZ Black | All done except Ozicare (renewal Sep) + water (manual) |
| 2026-02-05 | Zac's Spartans operations calendar | Built 27 events, emailed to Zac with SOPs |
| 2026-02-05 | Telegram bot architecture overhaul | Single consumer, context tracking, callback support |
| 2026-02-01 | Mac Mini M4 Pro 48GB | Ordered ~$3,299 AUD |
| 2026-01-31 | Laura's holding space course | Built and deployed |
| 2026-01-30 | Full autonomous Claude system | Active |

---

*Claude updates this automatically. Patrick never needs to manage this file.*
