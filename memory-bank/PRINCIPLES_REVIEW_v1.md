# Principles Adversarial Review v1

**Date:** 2026-05-01
**Reviewer:** Claude Code (Opus 4.7, 1M context)
**Spec:** `C:\Veritas\repos\memory-bank\VIE_YOUTUBE_INTELLIGENCE_ENGINE.md` (note: spec's self-declared canonical path at line 3 is wrong — file is at `repos/memory-bank/`, not `repos/alan-os/memory-bank/`)
**Scope reviewed:** `alan_os_server.py` (1200 lines), `lux_launcher.py`, `nlm_feed_builder.py` (head), `shorts_researcher.py`, `extract_ai_links.py`, `ai_research_monitor.py`, `norman_inbox_guard.py` (head), `orchestrator.py`, `orchestrator_v2.py`, `agents/agent_{a,b,c}.md`, `workflow_4_1_lead_enrichment.json` (head), `workflow_2_4_video_repurposing.json`, `CLAUDE.md`, `PROJECTS.md`, `HANDOFF_SESSION_MAY01_2026.md`, `docs/veritas-company-narrative.md`, `.lux/` directory tree, `.lux/Data/` (17 JSON files).

This is a brutally honest review per the prompt in the spec. The verdict on every principle: useful direction, not yet sharp enough to produce decisions without interpretation. Every principle has either a vague phrase, a contradicting reality in the codebase, or a missing acceptance test. The biggest risk is **Principle 7** — a YouTube intelligence engine almost identical to what's being specced is *already running* in the codebase under three different filenames.

---

## 1. VAGUE PRINCIPLES

| Principle | Vague phrase | Why two engineers reach different conclusions | Sharper rewrite |
|---|---|---|---|
| **2. Independently Replaceable** | "If removing a tool requires touching more than one other layer, the integration is wrong." | "Layer" is undefined. Is `lux_launcher.py` (orchestrator) one layer with the 5 triage scripts (memory-touchers)? Is the FastAPI server one layer or six (one per endpoint family)? "Touching" is undefined — does logging count? | "Removing a component requires changes to ≤ 2 explicitly named files in `replaces_or_complements`. If more, redesign the contract or accept the coupling explicitly. Every component declares its `removes_breaks` set in a header comment." |
| **3. Token Efficiency is Architecture** | "Reduce token consumption without degrading output quality." | No threshold. A 5% reduction is "efficiency"; a 5% quality drop is "degraded." Without a measurement protocol, every tool can claim either. | "ADOPT only if it reduces tokens-per-completed-task by ≥30% on a representative workload (define workload per context) and Claude eval rubric stays ≥ 90% of baseline. Otherwise EVALUATE. Below 30% with no quality loss = MONITOR." |
| **4. No Human in the Loop by Default** | "Default assumption is no human is in the loop." | The actual codebase has at least four human-gated workflows (`/digest/action`, `/launch`, Nimrat approval gate planned for 3.1, painter SOW review). Either the principle is "no" or "default but with documented exceptions." Current wording forces all those into "violation" status when they're actually deliberate. | "Every workflow declares `human_gate: required \| optional \| none` in a header. Required gates must name the gate type (approval, review, manual-trigger), the human, and an SLA. Optional and none must be runnable end-to-end without human intervention from a cold start." |
| **5. Shared Core, Vertical Config** | "Outsized value in that vertical justifies the additional dependency." | "Outsized" undefined. Workflow 4.1 hard-codes a 2-pipeline allowlist (`mmm_trucking + veritas_bd`, explicitly excluding `loretta_re`). Is that a vertical-config tax (acceptable) or a vertical-fork (violation)? No test. | "Shared engine + per-vertical config dict in code. Forks (separate engine code per vertical) require explicit ADR justifying the split with a 6-month maintenance projection. Pipeline allowlists are config, not forks." |
| **6. Local Where Sensitive, Cloud Where Scalable** | "Sensitive" undefined. | Are MMM prospect emails "sensitive"? They're client data. They're already in Google Sheets (cloud) AND Outlook MAPI (local) AND `.lux/Data/leads.json` (local). Same data, three layers. No principle telling us which is canonical. | "Tag every data class as `sensitive_local`, `sensitive_controlled` (Drive/GitHub private), or `public_cloud`. Each class names *one* canonical store. Cross-store copies must declare a sync direction and a reconciliation schedule." |
| **7. Build Only What Doesn't Exist** | "Exhaust existing components first." | "Exhaust" is unmeasurable. The proposed `yt_transcribe.py` overlaps 60% with three existing scripts (see §3) — does that count as exhausted? No threshold. | "Before any new file, write a `BUILD_OR_EXTEND.md` (≤ 1 page) listing every existing component touching the same domain, the % overlap, and either (a) a justification for new file, or (b) the extension PR plan. ≥40% overlap = extend, not new." |
| **9. Revenue or Capability — 30 days** | "Demonstrably accelerate a revenue-generating workflow within 30 days or it gets cut." | "Demonstrably" — by what metric? "Cut" — by whom, against what budget? Norman Inbox Guard, ApexBot, and the Lollie & Lovie Lou website fit neither bucket as written. The principle would force them out of scope. | "Three buckets: REVENUE (named client/product, billable in 90 days), CAPABILITY (named operator KPI, ≥10% lift in 30 days, e.g. emails/hour, leads enriched/week), and FAMILY/PERSONAL (carved out — separately budgeted, not subject to the 30-day rule). Anything that fits none of the three is archived." |

**Plus a structural gap:** none of the nine principles defines an *acceptance test*. ADOPT/EVALUATE/MONITOR/REJECT decisions need pass/fail criteria, not narrative. Without that, two operators applying the same principles to the same tool will reach different verdicts.

---

## 2. CONTRADICTIONS

### Contradiction A — Principle 1 (API-First, No Lock-In) vs. the actual stack

**Reality:** the live stack is roughly 70% closed-API or COM-bound:
- **Outlook COM** drives 5 triage scripts + `ai_research_monitor.py` + `/digest/action` (line 980 of `alan_os_server.py`). Windows-only, GUI-dependent (`lux_launcher.py` lines 63–91 *kill and restart Outlook* every run).
- **Lofty CRM** owns the `loretta_re` pipeline — explicitly documented as system-of-record, not API-pulled into `leads.json` (HANDOFF Apr 30).
- **Buffer**, **Twilio**, **n8n cloud** (open-core but proprietary), **Google Sheets/Docs** — all closed APIs with OAuth lock-in. Three Google creds revoked refresh tokens in April; recovery required browser-only re-auth.
- **NotebookLM** — explicitly marked an exception in Principle 8, but the principle stating "no proprietary UIs that can't be automated" doesn't have a matching exception clause.

If Principle 1 is read literally, every existing tool is a violation. If it's read as "prefer open APIs *when the closed alternative is equally good*," it's not enforceable.

**Resolution needed:** either rewrite as "prefer open-API alternatives *when ≥90% feature parity exists*" with named exceptions, or split into two: (1) "data must be exportable in a standard format on demand" (tighter, enforceable) and (2) "automation surface preferred over GUI" (looser, with explicit exceptions).

### Contradiction B — Principle 4 (No Human in Loop) vs. the operator-in-the-loop reality

The operator (Alan) is *deliberately* in the loop on:
- **`/digest/action` endpoint** (`alan_os_server.py` 970–1022) — operator clicks move/delete/leave per email.
- **`/launch` endpoint** (1082–1135) — operator triggers session start; the relay page injects context into claude.ai.
- **Nimrat approval gate** for Workflow 3.1 (planned, see PROJECTS.md TIER 1 row) — auto-send replaced with human-reviewed draft.
- **Painter SOW**, **health enthusiast SOW**, **digital presence websites** — all human-reviewed before send.

These aren't accidents; they're the operating model. The principle as written says these are violations. They aren't.

**Resolution needed:** rewrite to "*default* assumption is no human in the loop, but every human gate must be declared in the workflow header with type/SLA/owner." Allows the same code to be audited mechanically (no surprise gates) without rejecting the legitimate ones.

### Contradiction C — Principle 5 (Shared Core, Vertical Config) vs. Workflow 4.1

`workflow_4_1_lead_enrichment.json` explicitly excludes `loretta_re` (HANDOFF: "Do NOT wire loretta_re leads into leads.json or SalesOS"). That's a vertical-specific *exclusion*, which is fine — but the spec narrative says "build one engine with swappable context/prompts/credentials per vertical." A 2-pipeline allowlist enforced in JSON node config is *closer* to a config (good) than a fork (bad), but the principle gives no language for "deliberately scoped to N pipelines." Reads as a violation when it isn't.

### Contradiction D — Principle 8 (Four Memory Layers, No Fifth) vs. existing shadow stores

Counted today, the codebase has **at least eight** memory surfaces, not four. See §3 violation 3 for the full list.

### Contradiction E — Principle 9 (Revenue or Capability) vs. Family/Personal scope

Norman Inbox Guard, ApexBot, the Lollie & Lovie Lou website, and the family property hit list are all in PROJECTS.md TIER 3. None of them generate Veritas revenue. None of them accelerate a Veritas revenue workflow inside 30 days. By the principle as written, they all get cut. That's wrong — they're carved out from the business stack on purpose.

---

## 3. VIOLATIONS IN CURRENT STACK

### Violation 1 — Principle 7 (Build Only What Doesn't Exist) — **CRITICAL, blocks the VIE YouTube build**

The proposed `yt_transcribe.py` overlaps with **at least four existing scripts**:

| Existing script | Lines | What it does | Overlap with proposed `yt_transcribe.py` |
|---|---|---|---|
| `shorts_researcher.py` | 154 | Scans `ai_research_links.txt`, extracts YouTube Shorts URLs, fetches title+channel via HTTP, calls Claude API for topic/category/notebook/best-channel, writes `notebooklm_ready_urls.txt`. | **High** — same input source domain (YouTube Shorts), same enrichment pattern (Claude), same output goal (categorized actionable URLs). Differences: no transcript extraction; uses YouTube search results instead of full transcripts; outputs to text file instead of JSON. |
| `extract_ai_links.py` | 187 | Outlook COM scan of MSN inbox + Filing/AI Research folder, regex URL extraction, 14-category classifier (YouTube, Anthropic, GitHub, etc — same enum as `AI_STACK_CATEGORIES_ENUM` in `alan_os_server.py:628–630`), persistent dedup via `ai_links_seen.txt`. | **Medium** — proposed engine ingests the same URL stream this already produces. Should be the *upstream* of yt_transcribe, not duplicated. |
| `ai_research_monitor.py` | 295 | Daily Outlook COM monitor → Claude Haiku summarize → append to Veritas Research Feed Doc. Already does email→Claude→Drive. | **Medium-high** — same shape as proposed pipeline, different content type. The proposed engine should plug into this, not parallel it. |
| `nlm_feed_builder.py` | 1059 | Per-folder URL extraction with YouTube-specific handling (`extract_youtube_url` at line 119), routing to 5 NotebookLM notebooks, **already has a VIE V1 sink** (`AI_STACK_API_URL = "http://localhost:8000/ai_stack"`, line 90). | **High** — this is the canonical VIE V1 ingestor and explicitly POSTs to the `/ai_stack` endpoint that already exists in `alan_os_server.py` (lines 693–729). |

Plus the destination `/ai_stack` endpoint is **already built** with a wrapped JSON schema, dedup, status workflow (new/reviewed/saved/dismissed), and a digest endpoint (`/ai_stack/digest`). The proposed engine targets a different destination (`vie_stack_log.jsonl`), creating a second, parallel VIE store.

**Decision needed:** is the YouTube engine (a) a transcript-extracting *extension* of `shorts_researcher.py`/`nlm_feed_builder.py` that POSTs to the existing `/ai_stack` endpoint with a richer payload, or (b) a *replacement* of those four scripts? Either is fine — but building a parallel fifth is the violation.

**Recommendation:** the build should be:
1. A small `yt_transcribe.py` that *only* does yt-dlp transcript extraction + the principles-rubric Claude eval, and
2. A 30-line patch to `nlm_feed_builder.py` that — when it detects a YouTube URL — calls `yt_transcribe` and POSTs the enriched record to the existing `/ai_stack` endpoint with the new principles-rubric fields.

That's an extension that respects Principle 2 (replaceable behind contract), Principle 7 (don't duplicate), and Principle 8 (single memory layer).

### Violation 2 — Principle 1 (API-First) — **acknowledged exception**

`/admin/write-file` (`alan_os_server.py` 1149–1163) accepts a base64 payload and writes anywhere on disk including absolute paths (`if req.path.startswith('/') or req.path.startswith('C:'): target = Path(req.path)`). That's not API-first — that's an unrestricted RCE primitive. Today it's behind localhost. With Cloudflare Tunnel coming live next session (HANDOFF priority 2), this becomes a public RCE the moment the tunnel is up. **Fix priority: before Cloudflare Tunnel goes live.** See also Violation 4 (Principle 6).

### Violation 3 — Principle 8 (Four Memory Layers) — **structural**

Five+ shadow surfaces exist beyond the four canonical layers:

1. **`~/.lux/ai_links_seen.txt`** (line 13 of `extract_ai_links.py`) — plain-text URL registry, not in any of the four layers.
2. **`~/.lux/Data/backfill_tracker.json`** — has its own `processed_ids` separate from `nlm_processed_ids.json`, separate from n8n's dedup. Three independent dedup stores for overlapping data.
3. **`~/.lux/Data/google_token.json`**, **`google_credentials.json`**, **`~/.lux/credentials/service_account.json`** — three separate auth caches; rotation cadence undefined.
4. **Log files in `~/.lux/`**: `digest_log.txt`, `triage_log.txt`, `triage_gmail_log.txt`, `triage_keys_log.txt`, `outbound_campaign_log.txt`, `nlm_feed_builder_log.txt`, `shorts_researcher_log.txt` — append-only state, no rotation policy, holds stack history.
5. **Outlook MAPI store** — read-only by triage, *mutated* by `/digest/action` (move/delete). It's a memory layer the principles don't name.
6. **`~/.lux/.env`** + **`alan-os/.env`** + **`loretta-os/.env`** — three `.env` files with overlapping keys (per session-log Apr 29 incident report).
7. **`backfill_tracker.json`**, **`automation_log.json`**, **`digest_history.json`**, **`nlm_processed_ids.json`** — overlapping run-history stores; relationship undefined.
8. **Browser localStorage** — `/launch` endpoint persists session state via `localStorage.setItem('alan_os_session_msg', MSG)` (line 1122). Not in any layer.

The "four layers, no fifth" rule needs either to expand to capture this reality or to define which surfaces are exceptions.

### Violation 4 — Principle 6 (Local Where Sensitive) — **HIGH RISK with Cloudflare Tunnel pending**

Two endpoints in `alan_os_server.py` blur the local/cloud boundary:

- **`/admin/write-file`** (1149) — base64 payload, arbitrary path, no auth. (See Violation 2.)
- **`/admin/restart`** (1165) — kills any process by PID, then re-spawns. No auth.
- **`/digest/action`** (970) — accepts arbitrary `account/subject/sender/action` and triggers Outlook MAPI mutations.

With `localhost:8000` exposed at `api.veritasaipartners.com` once Cloudflare Tunnel is up, these become public-facing attack surfaces. The principle says "never mix sensitive and public data in the same pipeline path" — these endpoints are exactly that mixing.

**Fix before tunnel:** add auth (shared bearer token in env) or move to a separate listener bound only to localhost.

### Violation 5 — Principle 9 — **scope drift across the script floor**

`.lux/workflows/` holds **70+ Python files**. Survey by purpose:

| Bucket | Files | Status |
|---|---|---|
| **REVENUE-adjacent** (triage, digest, lead, sheets) | ~12 files | Live, named, owned. |
| **CAPABILITY** (orchestrator, dashboard, launcher, NLM feed) | ~8 files | Live, named, owned. |
| **DEBUG / one-off probes** (`probe_*.py`, `find_pdf_script*.py`, `patch_*.py`, `check_*.py`, `read_*.py`, `verify_*.py`) | ~30 files | No clear ownership. Half are dated artifacts of bug-hunts (e.g. `find_pdf_script4.py` — fourth attempt at the same problem). |
| **VERSIONED OLD COPIES** (`daily_digest.py` + `daily_digest_v2.py` + `daily_digest_v3.py`, `triage_loretta.py` + `triage_loretta_v2.py` + `triage_loretta_batch.py`) | ~10 files | Multiple live versions; only one is wired via `lux_launcher.py` SCRIPTS table. |
| **BACKUPS** (`alan_os_server_backup_20260421_121943.py`, `claude_usage_dashboard_backup.py`) | ~3 files | Snapshot copies. Should be in `~/.lux/backups/`, some are. |
| **EXPERIMENTAL** (`shorts_researcher.py`, `outbound_campaign.py`, `setup_autonomy.py`, `setup_tasks.py`) | ~7 files | Run history unclear. |

By Principle 9, ~50% of `.lux/workflows/` does not have a named REVENUE or CAPABILITY path. Most of those should be archived to `.lux/workflows/_archive/` and the active set kept ≤ 20 files.

### Violation 6 — Principle 2 (Defined Contract) — **lux_launcher tightly couples Outlook + 5 triage scripts**

`lux_launcher.py` lines 63–91 *kill and restart Outlook* every run, then sleeps 120s for it to load, then runs 5 triage scripts that all share the COM session, with 30s spacing each. If any one script hangs Outlook, the rest of the chain fails. This is the opposite of "swap the implementation behind a contract" — there is no contract; there's a shared mutable session state that all 5 scripts depend on. Removing one script doesn't simplify the chain because the chain is structured around Outlook's lifecycle, not the scripts'.

**Fix path:** isolate each triage to its own subprocess with its own Outlook spawn, OR move triage off COM to IMAP (Norman Inbox Guard already uses IMAP — `imaplib`, line 14 of `norman_inbox_guard.py` — proving it's possible).

### Violation 7 — Principle 5 (Shared Core, Vertical Config) — **agent specs are duplicated, not config-driven**

`agents/agent_a.md`, `agent_b.md`, `agent_c.md` each contain ~80 lines of identical SHARED_RULES + CONTEXT.json content (compare lines 17–55 across all three — verbatim duplication of the system context block). When CONTEXT.json changes, all three agent specs go stale. Should be templated (one shared rules block, one context block, agent-specific job line) — but the orchestrator regenerates these on every run (`generate_agent_spec` in `orchestrator.py:157`), so the duplication is *transient*. The CONTEXT.json embedded in the surviving copies on disk is what's stale (Apr 28-vintage `needs_reauth` list when reality is empty per Apr 29 session-log).

**Fix path:** orchestrator should not write CONTEXT.json *into* agent specs — it should pass `CONTEXT.json` as a path the agent reads. Reduces drift to zero.

---

## 4. GAPS — what the principles don't cover

| Gap | Why it matters now | Suggested principle |
|---|---|---|
| **Secret rotation cadence** | Apr 26 leaked `sk-ant-api03-s1gFMM…` was rotated *after* discovery. The only safety net was post-leak rotation. | "Every secret has a declared rotation interval and a `last_rotated` timestamp tracked outside the secret store. Overdue secrets are flagged on dashboard." |
| **Cost ceilings** | Principle 3 talks token *efficiency*; nothing caps total $/month. Claude burn dashboard exists (`daily_burn_rate.py`) but no automatic cutover. | "Every workflow declares a monthly $ budget; sustained burn at >2x budget triggers a circuit breaker (workflow disable + alert)." |
| **Data retention / TTL** | Logs in `.lux/`, `vie_stack_log.jsonl`, `ai_stack_feed.json`, all 5 `*_log.txt` files — no rotation. Disk grows linearly. | "Every persistent data class has a retention policy: keep N days, then archive (Drive) or delete." |
| **Authentication on local endpoints** | `/admin/*`, `/digest/action`, `/launch` have no auth. Only protection is `127.0.0.1` binding. Cloudflare Tunnel removes that. | "Endpoints accepting writes or actions require a bearer token or an explicit `localhost_only` declaration; `localhost_only` endpoints fail to start if listener is bound to 0.0.0.0 or proxied externally." |
| **Cascade-failure isolation** | If Outlook hangs, lux_launcher hangs all 5 triage scripts. If `service_account.json` is invalid, everything Drive-touching fails simultaneously. | "Components must declare `depends_on`. Failure of a dependency must not silently cascade — catch, log, mark unhealthy in `/health`, allow the rest of the system to keep running." |
| **Observability** | No structured logs, no metric emission, no central dashboard for which scripts ran when with what outcomes (the `/log` endpoint reads `automation_log.json` which only logs dashboard-triggered runs). | "Every workflow run emits a structured record (start, end, duration, exit_code, error_class) to a single sink. Dashboard reads from that sink, not from per-script log files." |
| **Versioning rule** | `daily_digest_v3.py` is canonical; v1 and v2 still exist on disk. `nlm_feed_builder.py` (canonical) and `nlm_feed_builder_v2.py` both exist. No rule for "delete the predecessor when the successor is live." | "Versioned files are temporary. Successor proves itself for 14 days, then predecessor moves to `_archive/` or is deleted." |
| **Family / Personal carve-out** | Norman Inbox Guard, ApexBot, Lollie & Lovie Lou are not Veritas revenue. Principle 9 as written rejects them. | (Captured in §1 Principle 9 rewrite.) |
| **Public surface inventory** | When Cloudflare Tunnel is live, Alan should be able to answer "what URLs are public?" in 30 seconds. Today there's no manifest. | "Every component declares its public surface (URL paths exposed externally). Tunnel/proxy config validates against the manifest." |

---

## 5. RANKING — top 3 most-damaging if violated long-term

1. **Principle 7 — Build Only What Doesn't Exist (REWORDED)**
   The codebase already shows the failure mode: `daily_digest.py` + v2 + v3, three triage_loretta variants, 30+ `probe_*` / `find_pdf_script*` / `patch_*` one-offs. Without a "BUILD_OR_EXTEND" gate (with a measurable overlap threshold) the script floor doubles every quarter, and *no one* — Alan or future Claude — can hold the stack in working memory. At ~70 files today, it's already past the threshold where a single operator can audit it in one session. This is the principle that, if violated, makes every other principle harder to enforce because no one knows what's in the stack.

2. **Principle 8 — Four Memory Layers, No Fifth (REWORDED)**
   Eight surfaces exist today (see Violation 3). Each new shadow store creates a place where state can drift — `nlm_processed_ids.json` vs. `backfill_tracker.json` vs. n8n dedup is exactly that drift. When state diverges across stores, recovering from a failure means reconciling N stores instead of restoring 1. The exit thesis (§9 of company narrative) depends on the orchestration engine + dashboards + workflows being *transferable* to a buyer — a stack with 8 undocumented memory surfaces isn't transferable.

3. **Principle 6 — Local Where Sensitive (REWORDED + AUTH)**
   The Cloudflare Tunnel is queued for next session. The moment it's up, `/admin/write-file`, `/admin/restart`, and `/digest/action` become a public RCE + arbitrary inbox-mutation surface. The damage profile is asymmetric: the upside of the tunnel is one workflow (4.1) reaching n8n; the downside of an unauthenticated public RCE on the host that runs Norman Inbox Guard, the dashboard, and all client triage is full operational compromise. **This is the only principle violation that is time-boxed: it must be fixed before the tunnel goes live.**

---

## 6. PRINCIPLE 9 AUDIT — every active workflow / script

Format: **NAME → BUCKET → 30-day path (or flag).**

### REVENUE — direct client / product revenue
- **Workflow 3.1 MMM Gmail Triage** → REVENUE → MMM $3K/mo retainer protection. Live, no flag.
- **Workflow 3.2 MMM Prospect Audit** → REVENUE → Same retainer; on-demand. Live, no flag.
- **Workflow 4.1 Lead Enrichment** → REVENUE (`mmm_trucking + veritas_bd`) → Blocked on Cloudflare Tunnel + Gmail cred patch. **30-day path: clear if priority queue executed this session.**
- **Workflow 2.1 / 2.2 / 2.5 / 2.6 Loretta content engine** → REVENUE → Loretta $5K/mo side-hustle Alan operates. Live (Sheets/Docs OAuth re-auth confirmed Apr 29), no flag.
- **Workflow C Telegram intake** → REVENUE-adjacent → Multiplies Loretta brief throughput. Live.
- **Workflow 2.3 Hot Lead SMS** → REVENUE → MMM lead conversion. **FLAG: Twilio account blocker open >14 days. If Twilio not stood up by 2026-05-15, descope.**
- **Workflow 2.4 Video Repurposing** → REVENUE → Loretta brand reach → AgentOS social proof. Deployed + active Apr 29. **FLAG: end-to-end test still gated on `OPUS_CLIP_API_KEY` + `BUFFER_*` + Loretta source video. 30-day path: clear, but currently zero revenue lift. If no first run by 2026-05-29, descope.**
- **Lollie & Lovie Lou website** → REVENUE → Loretta-owned children's-book brand. Outside Veritas P&L. (Family/Personal carve-out applies.)
- **Painter / health enthusiast websites** → REVENUE → Veritas Digital Presence service line. In progress.

### CAPABILITY — operator multiplier with a 30-day revenue link
- **`alan_os_server.py` + dashboard (Phases 1–4)** → CAPABILITY → Aggregates 5-account triage + project state + Drive into one panel. **Soft 30-day link: enables daily MMM/Loretta operating cadence — measurable in fewer missed deadlines.** Live, no flag.
- **`lux_launcher.py` + 5 triage scripts** → CAPABILITY → ~1 hr/day Alan saves on inbox processing. **Strong link** — that hour is what makes the $3K MMM retainer + $5K Loretta side-hustle operationally feasible solo. No flag.
- **`daily_digest_v3.py`** → CAPABILITY → Daily 8:05 AM Alan digest. Strong link (same operator-time argument). No flag.
- **`norman_inbox_guard.py`** → **FAMILY/PERSONAL** → Carve-out (see §1 / Principle 9 rewrite). Should not be subject to the 30-day revenue rule.
- **`claude_usage_dashboard.py`** → CAPABILITY → Cost-control. Prevents runaway Claude spend. **Strong link — without it, a runaway loop costs more than a month of MMM revenue.** No flag.
- **`orchestrator.py` (ORCH-1)** + **`orchestrator_v2.py` (ORCH-2)** → CAPABILITY → Multi-agent decomposition. **FLAG: built Apr 28; only known production run is the Apr 28 cred re-auth directive. No evidence of additional runs in session-log Apr 29 / Apr 30 / May 1.** Idle CAPABILITY = unproven. **30-day path: name a real directive that ships through ORCH-2 by 2026-05-29 (e.g. weekly MMM prospect cadence run) or descope.**
- **`agents/agent_{a,b,c}.md`** → ARTIFACTS of orchestrator runs (auto-generated specs, not durable code). The CONTEXT.json embedded in them is Apr 28-vintage and stale. (See Violation 7.)
- **`nlm_feed_builder.py` + `ai_research_monitor.py` + `extract_ai_links.py` + `shorts_researcher.py`** → CAPABILITY (AI research throughput). **FLAG: ≥60% functional overlap among the four. By Principle 7, three of these should be consolidated into one. Pick canonical: `nlm_feed_builder.py` already has the VIE V1 sink and is the most complete — make it canonical, archive the other three.**

### CAPABILITY — pre-revenue (waitlist / validation)
- **VIE V1 (Workflow 5.1, `nlm_feed_builder.py` enrichment + `/ai_stack` endpoints + dashboard tab)** → CAPABILITY → Eliminates Alan's manual research loop. **Sellable inside PersonalOS / AgentOS — but no buyer yet.** 30-day path: ship the first end-to-end run against a real AI-research email (already on next-session queue per HANDOFF Step 5).
- **VIE YouTube Engine (this spec)** → CAPABILITY → **FLAG: Build-or-extend decision required (Violation 1) before this passes Principle 7.** 30-day path: extension model has clear path to revenue (improves the same VIE V1 buyers will pay for); a parallel new pipeline does not.

### FAMILY / PERSONAL — carve-out (currently unnamed bucket)
- **`norman_inbox_guard.py`** + whitelist + USAA routing + Marsha forwarding (staged) → Norman & Marsha estate stewardship.
- **ApexBot** (Evony game automation) → Personal/leisure. **FLAG: TIER 2 in PROJECTS.md; outside the business stack scope. RageBot expiry Apr 30 may end this naturally.**
- **Family property hit list, Estate Planning CC, Endurance/Indiana DOI tracker** → Personal/family ops, not Veritas.

### ARTIFACTS — should be archived
- **30+ `probe_*.py`, `find_pdf_script*.py`, `patch_*.py`, `read_*.py`, `verify_*.py`** in `.lux/workflows/` → Move to `.lux/workflows/_archive/2026-04/` or delete. None has a current revenue or capability path; all are debug detritus.
- **`daily_digest.py`, `daily_digest_v2.py`** (v3 is canonical) → Archive or delete.
- **`triage_loretta.py`, `triage_loretta_batch.py`** (v2 is canonical per `lux_launcher.py:40`) → Archive or delete.
- **`nlm_feed_builder_v2.py`** (v1 is canonical per the VIE V1 wiring) → Confirm v1 vs v2 status, archive the loser.

---

## 7. REVISED PRINCIPLES — proposed (for Alan to approve / edit / reject)

These are the principles after the rewrites in §1 plus the gaps in §4. Each principle now has an *acceptance test* — a concrete pass/fail check.

> **Principle 1 — API-First, Exportable Data**
> Every component must (a) expose or consume a documented API/webhook *or* (b) make its data exportable in a standard format on demand. GUI-only tools without an export path are rejected. Closed-API tools (Buffer, Twilio, Lofty) are accepted when the closed alternative is ≥90% feature parity, declared in a `closed_dependencies.md`.
> **Acceptance test:** "Can I export every byte of state from this tool with a documented call within one hour, with no GUI clicks?"

> **Principle 2 — Independently Replaceable, with Declared Coupling**
> Every component declares a `removes_breaks` set in its header (file path list of components that fail if this one is removed). Replacing a component touches files only in that set.
> **Acceptance test:** "If I delete this file, what tests fail? Are those tests in the declared set? If not, the contract is wrong."

> **Principle 3 — Token Efficiency, Measured**
> ADOPT only if a tool reduces tokens-per-completed-task by ≥30% on a representative workload, with Claude eval rubric staying ≥90% of baseline. EVALUATE if reduction is 10–30%. MONITOR if <10%. Workload definitions live per-context.
> **Acceptance test:** Pre-tool baseline tokens vs. post-tool tokens, on a fixed sample of 10 representative tasks per context.

> **Principle 4 — Human Gates Are Declared, Not Default**
> Every workflow declares `human_gate: required | optional | none` in its header. `required` gates name type (approval / review / manual-trigger), the human, and an SLA. `optional` and `none` workflows are runnable end-to-end without human intervention from a cold start.
> **Acceptance test:** "If Alan is on a plane for 24 hours, does this workflow still run, fail explicitly, or hang silently?"

> **Principle 5 — Shared Engine + Vertical Config**
> One engine codebase, per-vertical config dicts. Forks (separate engine code per vertical) require an ADR justifying the split with a 6-month maintenance projection. Pipeline allowlists are config, not forks.
> **Acceptance test:** "Adding a new vertical adds N lines to a config dict, not a new file in `engine/`."

> **Principle 6 — Local for Sensitive, Cloud for Scalable, Auth for Both**
> Tag every data class as `sensitive_local`, `sensitive_controlled` (Drive/GitHub private), or `public_cloud`. Each class names *one* canonical store. Cross-store copies declare a sync direction. Endpoints accepting writes or actions require a bearer token; localhost-only endpoints fail to start if bound to 0.0.0.0 or proxied externally.
> **Acceptance test:** Boot the host with the Cloudflare Tunnel up. Curl every endpoint without a bearer. Every write/action endpoint must return 401.

> **Principle 7 — Build-or-Extend Decision in Writing**
> Before any new file > 50 lines, write a `BUILD_OR_EXTEND.md` listing every existing component touching the same domain, % overlap, and either (a) a justification for new file, or (b) the extension PR plan. ≥40% overlap = extend. ≥60% overlap = no new file.
> **Acceptance test:** Pre-merge gate. Reviewer rejects if the doc is missing or the overlap math is wrong.

> **Principle 8 — Named Memory Surfaces, Single Canonical Store per Class**
> The stack has named memory surfaces: Ephemeral, Working, Structured, Long-term, plus *named* exceptions (Outlook MAPI, NotebookLM, browser localStorage). Each *data class* (e.g. processed-email IDs, lead state) names one canonical store. Shadow stores require explicit reconciliation.
> **Acceptance test:** For every JSON / TXT file in `~/.lux/`, name (a) the data class, (b) the canonical-store flag, (c) the retention policy, (d) the reconciliation procedure if it diverges.

> **Principle 9 — Three Buckets: Revenue, Capability, Family/Personal**
> Every workflow / script declares: REVENUE (named client/product, billable in 90 days) *or* CAPABILITY (named operator KPI, ≥10% lift in 30 days) *or* FAMILY/PERSONAL (separately budgeted, exempt from 30-day rule). Anything fitting none is archived to `_archive/`.
> **Acceptance test:** Quarterly audit. List every script in `.lux/workflows/` and `repos/*/workflows/`. Tag each with bucket + KPI. Untaggable = archive.

> **Principle 10 (NEW) — Secret Rotation, Cost, Retention, Observability**
> Every secret has a declared rotation interval and `last_rotated` timestamp. Every workflow has a declared monthly $ budget; sustained 2x burn triggers circuit breaker. Every persistent data class has a retention policy. Every workflow run emits a structured record to a single sink (`automation_log.json` extended).
> **Acceptance test:** Dashboard surfaces overdue secrets, over-budget workflows, retention-violating files, and missing run records.

---

## 8. IMMEDIATE ACTION ITEMS (independent of VIE YouTube build)

These are pre-existing fixes the review surfaced. Not blocking the VIE build approval — these can ship in parallel or after.

| # | Action | Why | Priority |
|---|---|---|---|
| 1 | Add bearer-token auth to `/admin/write-file`, `/admin/restart`, `/digest/action`. | Cloudflare Tunnel goes live next session → public RCE. | **BEFORE TUNNEL** |
| 2 | Decide canonical: `nlm_feed_builder.py` vs. `nlm_feed_builder_v2.py`; archive the other. Same for `daily_digest` v1/v2. | Versioning hygiene. Reduces stack size by ~5 files. | This week |
| 3 | Move 30+ debug `probe_*` / `find_pdf_script*` / `patch_*` scripts to `.lux/workflows/_archive/2026-04/`. | Principle 7 sprawl. | This week |
| 4 | Decide consolidation: `shorts_researcher.py`, `extract_ai_links.py`, `ai_research_monitor.py` → fold into `nlm_feed_builder.py` or keep as separate "stage 0" extractors with a documented contract. | Principle 7. | Before VIE YouTube build |
| 5 | Pick canonical `.env` location. Currently 3 (`.lux/.env`, `alan-os/.env`, `loretta-os/.env`). Document which keys live where. | Principle 8 + secret hygiene. | This week |
| 6 | Define a real ORCH-2 directive to ship by 2026-05-29 or descope ORCH-2. | Idle capability = unproven. | This month |
| 7 | Spec `closed_dependencies.md` listing Buffer/Twilio/Lofty/Outlook COM/Google Workspace as accepted closed-API exceptions to Principle 1. | Removes the contradiction. | This week |
| 8 | Fix the spec self-pointer: `VIE_YOUTUBE_INTELLIGENCE_ENGINE.md` at line 3 says `repos/alan-os/memory-bank/...`; actual location is `repos/memory-bank/...`. Either move the spec or fix the line. | Documentation hygiene. | Trivial |

---

## 9. RECOMMENDATION TO ALAN (on the VIE YouTube build itself)

**Do not build `yt_transcribe.py` as specced. Build it as an extension instead.**

The principles review surfaces a single architectural decision Alan must make before any code is written:

> **Is the YouTube Intelligence Engine (a) a transcript-extraction extension to the existing VIE V1 pipeline, or (b) a parallel system?**

The spec as written reads as (b). The codebase already has VIE V1 wired (`nlm_feed_builder.py` POSTing to `/ai_stack`), so (b) creates a second, parallel research store (`vie_stack_log.jsonl`) and ignores the existing categorization in `extract_ai_links.py`. That's a Principle 7 + Principle 8 double violation.

**Recommended scope (minimum-violation path):**

1. **`yt_transcribe.py`** — small, single-responsibility module: takes a YouTube URL, returns `(transcript_text, title, duration_seconds)` via yt-dlp. ~80 lines. No Claude call, no JSON write, no Drive — just transcript extraction.
2. **`yt_evaluate.py`** (or merge into `nlm_feed_builder.py`) — runs the principles-rubric Claude eval on a transcript, returns the structured `stack_evaluation` dict. ~60 lines.
3. **Patch `nlm_feed_builder.py`**: when a YouTube URL is detected, call `yt_transcribe.get_transcript()`, then `yt_evaluate.evaluate(...)`, and POST the enriched record to the existing `/ai_stack` endpoint with the new principles-rubric fields. ~30 lines.
4. **Extend `/ai_stack` schema** in `alan_os_server.py` to accept the optional `stack_evaluation` block (recommendation, stack_layer, confidence, reasoning, action_items). Backward compatible — older items just don't have the block. ~20 lines.
5. **`STACK_DESIGN.md`** — yes, build this as the spec says. It's the living document, not a parallel store.

This keeps one VIE pipeline, one memory surface (`/ai_stack`), one canonical research store, and adds principles-rubric evaluation as an *enrichment*, not a fork.

**Total new code: ~190 lines, plus the rubric prompts. Versus the spec's ~360-line standalone module that creates a parallel pipeline.**

Approve, edit, or reject. I will not write a line of `yt_transcribe.py` until Alan has approved (a) revised principles per §7, (b) the build-vs-extend decision per §9, and (c) the immediate actions in §8 that touch shared state.

---

*End of PRINCIPLES_REVIEW_v1.md.*
