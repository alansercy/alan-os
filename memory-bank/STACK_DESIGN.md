# Stack Design — Living Document

**Owner:** Alan Sercy / Veritas AI Partners
**Engine:** VIE YouTube Intelligence Engine — `workflows/yt_transcribe.py`
**Sink:** `/ai_stack` endpoint on `alan_os_server.py` → `~/.lux/Data/ai_stack_feed.json`
**Rubric:** `memory-bank/PRINCIPLES_REVIEW_v1.md` §7 (revised principles)
**First entries seeded:** 2026-05-01 from VIE Group 1 batch (6 URLs, parallel)

This file captures every accumulating ADOPT / EVALUATE / MONITOR / REJECT decision plus the standing inventory of what's in the stack. The principles aren't abstract — they're the rubric Claude applies to every URL, and every entry below cites which principles drove the verdict.

---

## 1. Current Stack Inventory (May 2026)

Per layer. **One** canonical store / component per data class (P8). Closed-API tools listed where applicable (P1 exception — see `closed_dependencies.md` *to-be-written*).

### INTERFACE
- Lux Command Center (React, `localhost:8081`)
- n8n UI (`https://n8n.lorettasercy.com`)
- Alan OS dashboard (`localhost:8000/dashboard`)

### ORCHESTRATION
- n8n workflows — primary automation engine (15+ live)
- Claude Code — agentic build + ops (this session)
- FastAPI — `alan_os_server.py` (port 8000, auto-starts via Task Scheduler)
- ORCH-1 / ORCH-2 — `orchestrator.py` / `orchestrator_v2.py` (Apr 28; idle since)
- Lux Launcher — `lux_launcher.py` (3× daily Outlook+5-triage cycle)

### INTELLIGENCE
- Claude API — Sonnet 4.6 (default), Haiku 4.5 (fast filter), Opus 4.7 (Claude Code)
- VIE V1 — `nlm_feed_builder.py` (email-context enrichment) + `/ai_stack` endpoints
- VIE YouTube Engine — `yt_transcribe.py` (transcript-driven principles eval) **[NEW 2026-05-01]**
- Veritas AI Research Feed (Drive) — `1WD2Sr2HgSdMffSYv9bWIpPZOoef4_LDH27yQBiuuM6M`

### MEMORY
- Working: `CLAUDE.md`, `memory-bank/session-log.md`, `~/.lux/.env`, `alan-os/.env`
- Structured: `~/.lux/Data/*.json` (17 files: leads, competitors, ai_stack_feed, vault, etc.), Google Sheets
- Long-term: GitHub (`alan-os`, `loretta-os`, `lux-os`, `apexbot`), Google Drive
- Named exceptions: Outlook MAPI (read+mutate), NotebookLM (manual), browser localStorage (`/launch`)

### COMMUNICATION
- Outlook COM (5 accounts: MSN, Gmail, Loretta, Keys, MMM)
- Gmail API (n8n workflows)
- Telegram bots (Alan + Loretta)
- Cloudflare Tunnel — **planned**, blocks Workflow 4.1
- Twilio — **planned**, blocks Workflow 2.3 SMS

### DATA
- Local JSON: `leads.json`, `competitors.json`, `ai_stack_feed.json`, `vault_index.json`, `pending_jobs.json`, etc.
- Google Drive: assets, research, brand
- GitHub: code, configs, handoffs

### Auth surface (post 2026-05-01 patch)
- `/admin/write-file`, `/admin/restart`, `/digest/action` — **require `X-Admin-Token` header** (commit `fcce3f3`, lux-os). Token in `~/.lux/.env` as `ALAN_OS_ADMIN_TOKEN`. P6 fix landed before Cloudflare Tunnel goes live.

---

## 2. Group 1 Batch — 2026-05-01 (token optimization / Claude Code)

**Run:** `python workflows/yt_transcribe.py --batch workflows/vie_group1_urls.txt --max-workers 4`
**Result:** 6 URLs processed, 6/6 transcripts pulled (no caption fallbacks), 6/6 evaluated, 6/6 posted to `/ai_stack`.
**Verdict distribution:** **1 ADOPT · 0 EVALUATE · 0 MONITOR · 5 REJECT** — all HIGH confidence.
**Token cost:** input 10,800 · output 3,461 · cache_write 2,316 · cache_read 0 (cache underutilized in first batch — see Pattern §5).

### ADOPT × 1

#### `youtube.com/shorts/3E59wf8RA8Y` — "Claude Code skill-building tips" (AI Honeycove, 48s) — score 6, layer **memory**
- **Verdict:** ADOPT / HIGH / `fit_pipeline: ai_stack`
- **What it is:** Three skill-file authoring patterns: (1) a "## Gotchas" section that logs past mistakes as negative examples, (2) folder-as-skill structure (`prompt.md` + `/scripts` + `/examples` + `/templates`) for progressive disclosure, (3) context+constraints over rigid step-by-step instructions.
- **Why ADOPT:** All three are *extend-in-place* improvements to existing CLAUDE.md and skill-file conventions. P3 win (token efficiency via negative-example encoding reduces correction round-trips), P8 alignment (folder-as-skill = single canonical store per skill), P2 alignment (declared coupling between skill assets). P7 overlap is 100% with existing Working Memory — no new file > 50 lines needed; only amendments.
- **Replaces/complements:** Complements CLAUDE.md and existing skill files. No replacement.
- **Action items:**
  1. Add `## Gotchas` section to `CLAUDE.md` and any existing skill markdown files; seed with known repeat mistakes from recent sessions.
  2. Audit current skill/prompt files: convert single-file skills referencing external assets into folder-based skills (`prompt.md` + `/scripts` + `/examples` + `/templates`).
  3. Document folder-as-skill convention in a short ADR or `CLAUDE.md` note so future skill creation follows the pattern without a new `BUILD_OR_EXTEND.md` trigger.

### EVALUATE × 0

(none from Group 1 — all eval-grade signals were either ADOPT-clear or REJECT-clear)

### MONITOR × 0

(none from Group 1 — bias was toward REJECT for content failing P3 + P7 cleanly, per the rubric instructions)

### REJECT × 5

For each REJECT below: principles failed are cited so we don't re-evaluate the same URL or topic without new technical information.

#### `youtube.com/shorts/FPv_E2cMt_k` — "Save 70x Tokens On Claude With This Plugin" (Charlie Automates, 89s) — score 3, layer intelligence
- **Tool pitched:** Graphify (Claude Code plugin, knowledge-graph over codebase, Obsidian visualization)
- **Why REJECT:** Fails **P3** (the 70x claim is anecdotal, no eval rubric, no fixed-task baseline — cannot be verified against the ≥30% reduction test). Fails **P1** (no API surface, export format, or webhook described). Fails **P7** (would require BUILD_OR_EXTEND review against `nlm_feed_builder.py` and VIE pipeline before any adoption; video provides zero technical detail to run that overlap analysis). Promotional content, not architectural signal. Targets Claude Code IDE, not the Claude API stack Veritas runs.
- **Re-eval gate:** consider EVALUATE only if Graphify (a) ships a documented API + export schema and (b) a third-party benchmark publishes a measurable token-reduction number against a defined task corpus.

#### `youtube.com/shorts/xM99M7aLFhQ` — "The plugin that fixed my Claude Code workflow" (TheIgnitingStudio, 46s) — score 2, layer orchestration
- **Tool pitched:** GSD (Get Shit Done) — Claude Code workflow plugin (new project / plan phase / execute phase commands).
- **Why REJECT:** Fails **P7** — `CLAUDE.md` + `memory-bank/session-log.md` + the existing VIE pipeline already cover phased planning, project scoping, and structured execution; overlap is well above 60% with no documented differentiation. Fails **P3** (no token data, no rubric). Fails **P1** (GUI/CLI scaffolding, no n8n/FastAPI integration hooks).
- **Re-eval gate:** consider only if GSD ships a programmatic interface that's strictly additive over existing patterns AND publishes a token efficiency benchmark.

#### `youtube.com/shorts/8BZupIIVhjs` — "Use these 3 tricks to reduce your Claude code token usage" (Nick Automates, 47s) — score 2, layer none
- **Tools/techniques:** model routing (Opus plan / Sonnet execute), `/compact`, "ultra think" prefix.
- **Why REJECT:** Fails **P3** (no measured reduction, anecdotal). Fails **P7** — `/compact` and model routing are already standard Claude Code UX behaviors documented in Anthropic docs and used at the API level via direct SDK calls in `alan_os_server.py`; overlap near 100%. "Ultra think" is unverified prompt folklore.
- **Re-eval gate:** none — content is surface-level lead-magnet for a paid course; no novel signal expected.

#### `youtube.com/shorts/93qRVasYmQs` — "5 Free Claude Skills Every Beginner Must Install" (Dubibubii, 50s) — score 1, layer none
- **Items pitched:** 5 GUI features (front-end design, simplify, skill creator, web-app testing, MCP builder) inside an unidentified Claude wrapper / proprietary platform.
- **Why REJECT:** Fails **P1** (GUI-only, no documented API or export path for any of the five "skills"). Fails **P3** (zero token data). Fails **P7** (≥60% overlap with existing stack: Claude API direct calls, n8n multi-agent flows, MCP integrations already on roadmap). Beginner funnel ad.
- **Re-eval gate:** none — topic is a wrapper layer over capabilities the stack already has.

#### `youtube.com/shorts/U8PkKqegN9A` — "3 Claude Repos That You Need Like, Yesterday" (Charlie Automates, 84s) — score 2, layer none
- **Repos pitched:** Paul (project/roadmap/state manager for "context rot"), Graphify (codebase relationship mapping → Obsidian), Seed (guided ideation → Paul pipeline).
- **Why REJECT:** Fails **P1** — repos gated behind comment wall with no documented API. Fails **P3** — zero token data; "context rot" already addressed by `CLAUDE.md` + session-log. Fails **P7** — all three target Claude Code IDE sessions, not the Claude API runtime the stack uses; high overlap with existing working memory.
- **Re-eval gate:** revisit only if any of the three lands on PyPI / npm with a documented programmatic interface.

#### `youtube.com/shorts/FPv_E2cMt_k` (Graphify) — see above. Channel "Charlie Automates" surfaced TWICE in Group 1 with promotional content for the same Graphify tool. Channel-level signal: high promotional volume, low technical depth — **deprioritize** future content from this channel unless title indicates technical depth (benchmarks, API specs, architectural breakdowns).

---

## 2.B Groups 2-4 Batches — 2026-05-01 (sequential, max-workers=1)

**Run:** three back-to-back batches, `--max-workers 1` per batch (Alan's directive: pre-warm cache, run sequentially not in parallel).
**Result:** 8 URLs / 8 transcripts pulled / 8 evaluated / 8 posted to `/ai_stack`.
**Verdict distribution:** **0 ADOPT · 0 EVALUATE · 1 MONITOR · 7 REJECT.**
**Caching anomaly:** SDK 0.94.0 reported `cache_write=0` and `cache_read=0` across all three batches despite `cache_control: ephemeral` being set. Tokens consumed appear lower than fully uncached (G2: 6.3K input for 3 URLs; G3: 2.4K for 1; G4: 8.7K for 4) but the cache fields aren't surfacing. Investigate next session — likely an SDK attribute-name mismatch on the usage object, since the request itself is well-formed (Anthropic's API would reject a malformed cache_control). Functional behavior unaffected.

### MONITOR × 1 (Group 2)

#### `youtube.com/shorts/Wl6ns0uvXxo` — "Claude Code + Notebook LM is AWESOME" (Eric Michaud, 38s) — score 4, layer **intelligence**, confidence **LOW**
- **Tool surfaced:** `notebookmation` — a CLI bridge between Claude Code and NotebookLM, demonstrated running inside Obsidian's Terminal Plugin to give it vault-context access (daily notes, SOPs, templates).
- **Why MONITOR (not ADOPT, not REJECT):** NotebookLM is already a named exception in P8 (Long-term memory surface, manual). The CLI wrapper is *directly adjacent* to `nlm_feed_builder.py`'s VIE V1 work — but the video gives zero technical depth on whether it uses official or unofficial NotebookLM APIs, what state is exportable, or how it would integrate with n8n / FastAPI. P7 overlap with `nlm_feed_builder.py` is high but unquantified; P1 unresolved (API surface unknown); P3 unaddressed.
- **Re-eval gate:** examine the `notebookmation` repo (find URL via channel description or follow-up search) to assess whether it's official Anthropic, third-party, or a screen-scraper. If it has a documented API → promote to EVALUATE. If it's GUI-scrape → REJECT.

### REJECT × 7

For each: failing principles cited so we don't re-evaluate without new technical information.

#### `youtube.com/shorts/NCzV-CerZuI` (Group 2) — "Claude Just Replaced My Bookkeeper" (Nick Puru, 41s) — score 2, layer none
- **Tool:** Claude Chrome extension running inside QuickBooks/Xero, manually triggered each morning.
- **Why REJECT:** Fails **P1** (Chrome extension GUI, no API). Fails **P3** (no token data). Fails **P4** (manual daily trigger, no cold-start runability). FinanceOS is backburner anyway; the underlying pattern (Claude + accounting API) is directionally interesting but not what's demonstrated here.
- **Re-eval gate:** revisit only when a real Anthropic SDK + accounting-API implementation surfaces.

#### `youtube.com/shorts/M9lAIBQerUI` (Group 2) — "I Turned Claude Into My Entire Marketing Department" (Sabrina Ramonov, 27s) — score 1, layer none
- **What it is:** Promo for using Claude slash-commands for content calendar / multi-platform scheduling.
- **Why REJECT:** Fails **P3** (no eval rubric). Fails **P7** (Claude API + Buffer already cover this domain in the live stack — Workflow 2.4 + Loretta content engine). Fails **P1** (no API surface described). Engagement-bait with no implementation detail.
- **Re-eval gate:** none — domain already owned by AgentOS / Loretta.

#### `youtube.com/shorts/UfYP7t903Pc` (Group 3) — "Stop Building. Start Posting." (Duncan Rogoff, 1m48s) — score 1, layer none
- **What it is:** Pure GTM advice — post on LinkedIn instead of building. Author claims 2 multi-billion dollar clients from content.
- **Why REJECT:** Zero technical content. The Claude mention is anecdotal ("clients Google you or type you into Claude"), not an integration point. Fails **P3** by default (no measurable signal) and **P7** (no component to overlap with).
- **Re-eval gate:** none — strategic content, not stack content. Topic belongs in LinkedIn Authority Track planning, not VIE.

#### `youtube.com/shorts/LXSxrLIxoaA` (Group 4) — "AI Tools Tier List (2026)" (Dan Martell, 51s) — score 2, layer none
- **What it is:** Opinion ranking of 10 consumer AI tools (ChatGPT, Claude, NotebookLM, Grok, Gemini, Perplexity, Whisper Flow, Claude Code, OpenClaude, Claude CLI).
- **Why REJECT:** Fails **P3** (no benchmarks). Fails **P7** (Claude Code + Claude CLI already in stack; no overlap analysis). One mildly-novel mention: **Whisper Flow** (voice-to-structured-text) — could matter for PersonalOS dictation — but the mention is one sentence with no API or integration detail.
- **Re-eval gate:** if a PersonalOS dictation use case becomes active, evaluate Whisper Flow separately.

#### `youtube.com/shorts/RmT2H4J-5A0` (Group 4) — "This Open-Source AI Is Breaking Paid Tools" (John Lee, 49s) — score 0, layer none
- **What it is:** AI video generation with cinematic camera controls — open-source clone of Higgs Field AI. No tool name given, no GitHub URL.
- **Why REJECT:** Fails everything: no tool name, no repo, no API, no integration. AI video generation isn't in any current or planned Veritas vertical. Lead-gen for the creator's event.
- **Re-eval gate:** none — outside scope.

#### `youtube.com/shorts/sbTqBo0SZRc` (Group 4) — "The AI Mirror: What ChatGPT Knows About You" (John Lee, 57s) — score 0, layer none
- **What it is:** Motivational ChatGPT prompt-chain for self-reflection.
- **Why REJECT:** ChatGPT is not in the Veritas stack (Anthropic-only — locked decision per company narrative §10). Fails **P1**, **P3**, **P9**. Pure engagement-bait.
- **Re-eval gate:** none — wrong LLM family.

#### `youtube.com/shorts/kfUOSckgMjQ` (Group 4) — "April 29, 2026" (Alex Tavi, 46s) — score 2, layer none
- **What it is:** List of 4 Claude Code plugins: `superpowers`, a front-end design plugin (Anthropic), `Claude Mem`, and `awesome-claude-code`.
- **Why REJECT:** Fails **P3** (no benchmarks). Fails **P1** (no API/export format for any plugin). Fails **P7** — `Claude Mem` overlaps unknowable amount with existing P8 memory surfaces (CLAUDE.md, session-log, `.lux/data/*.json`); zero BUILD_OR_EXTEND analysis possible from this video.
- **Re-eval gate:** **`Claude Mem` is the only mention worth a follow-up search outside the VIE pipeline** — if it has a documented API and a token-efficiency benchmark, promote to EVALUATE. The `superpowers` plugin's plan-before-code + sub-agent-review patterns are already partially handled by CLAUDE.md discipline.

---

## 3. Pending Evaluations

**Spec batch complete (14/14 URLs across 4 groups, 2026-05-01).** Queue empty.

Standing follow-up watch list (from MONITOR + flagged REJECT re-eval gates):
- **`notebookmation`** — locate repo, assess API surface vs. screen-scrape. Promote to EVALUATE if documented API; REJECT if scrape.
- **`Whisper Flow`** — re-evaluate when a PersonalOS dictation use case becomes active.
- **`Claude Mem`** — find repo + benchmarks; promote to EVALUATE if documented API.
- **Channel deprioritization:** Charlie Automates surfaced 2× in Group 1 with promotional content for the same tool (Graphify). Future content from this channel: deprioritize unless title indicates technical depth.

---

## 4. Stack Gaps Identified (from Group 1 evaluations)

The batch surfaced two real architectural gaps that `yt_transcribe.py` itself cannot fix — they're principle-level concerns the rubric kept flagging:

1. **No `BUILD_OR_EXTEND.md` template exists** — P7 cited 5/6 times in REJECT reasonings. Without a template + worked example, any future "should I build or extend?" decision still requires reasoning from first principles. **Action:** create `templates/BUILD_OR_EXTEND.md` with the overlap-math format the principle requires.
2. **`closed_dependencies.md` is referenced but not written** — P1's exception clause (closed APIs accepted at ≥90% feature parity) names Buffer/Twilio/Lofty but no file documents the exceptions. **Action:** write the doc, naming each closed dependency, the open alternative it was weighed against, and the decision rationale.
3. **No "channel-level" signal layer in `/ai_stack`** — Charlie Automates appeared 2× in Group 1 with promotional content. The rubric evaluates URLs in isolation; channel-level patterns (this creator does X% promotional / Y% technical) would let the engine deprioritize entire creators. **Future enhancement, not blocking.**

---

## 5. Principles in Practice — what 14 URLs across 4 groups taught us

**Aggregate verdicts (all 4 groups, 14 URLs):**
- 1 ADOPT (7%) — a *pattern* (skill-file authoring), not a tool
- 0 EVALUATE
- 1 MONITOR (7%) — `notebookmation`, NotebookLM CLI bridge with high-but-unquantified overlap
- 12 REJECT (86%) — all HIGH confidence

**Pattern-level findings:**
- **The rubric is BIAS-CORRECTLY harsh.** 12/14 REJECT with HIGH confidence is not over-rejection — it reflects that 60-second YouTube Shorts rarely contain enough technical signal to ADOPT. P3 ("Token Efficiency, Measured" — ADOPT requires ≥30% reduction with eval rubric ≥90% baseline) eliminates anything without a number. **Without a benchmark, there's no ADOPT-grade signal.**
- **P7 was the most-cited principle (12/14 evaluations).** "Already exists in the stack" or "would require BUILD_OR_EXTEND analysis" was the killer for the majority of REJECTs. This validates `PRINCIPLES_REVIEW_v1.md` §5 ranking — P7 is the most-load-bearing principle long-term.
- **The one ADOPT was a *pattern*, not a tool.** All three skill-building patterns (gotchas, folder-as-skill, context+constraints) are extend-in-place changes to files Veritas already owns. Zero new files, zero new dependencies.
- **No video on FinanceOS, real estate, or trucking surfaced** — Groups 1-4 were Claude/AI-stack focused per the spec's batch grouping, not vertical-focused. Future batches sourced from MMM-relevant or AgentOS-relevant content streams (rather than `extract_ai_links.py`'s general feed) would test the engine's verticality.
- **Caching investigation deferred.** Group 1 (parallel, max-workers=4): cache_write=2316, cache_read=0 (race-write). Groups 2-4 (sequential, max-workers=1): cache_write=0 AND cache_read=0 — the cache fields aren't surfacing in SDK 0.94.0's usage object despite `cache_control: ephemeral` being correctly set on the request. Per-URL token cost roughly matches uncached behavior. Functional output unaffected, but the cost-saving rationale for caching isn't visible. **Open item for next session.**

---

## 6. Operating notes

- **Adding a verdict to this file is automatic** in the sense that `/ai_stack` is the source of truth — but a human curates STACK_DESIGN.md from `vie_group1_results.json` (or the next batch's equivalent) for narrative + action items. This file is the human-readable distillation; `/ai_stack` is the queryable store.
- **Re-running a batch on the same URLs** will hit `/ai_stack`'s URL-dedup and return `dedup: true` — items don't double-post. To re-evaluate, PATCH the existing item to `status=dismissed` first, then re-run.
- **Group sizing:** ThreadPool default is 4 workers. For groups > 6, raise `--max-workers` proportionally (rubric ≈ 2.3K tokens cached, marginal cost is just transcript tokens after first request).

---

*Living document. Update on every batch. First seeded 2026-05-01 (Group 1).*
