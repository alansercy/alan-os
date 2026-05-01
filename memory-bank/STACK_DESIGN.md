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

## 3. Pending Evaluations

(none yet — Groups 2, 3, 4 not yet processed)

Queued URLs from spec for the next batch run:
- **Group 2 (Use Cases):** `NCzV-CerZuI`, `M9lAIBQerUI`, `Wl6ns0uvXxo` (Bookkeeper / Marketing / NotebookLM workflows)
- **Group 3 (Strategy):** `UfYP7t903Pc` ("Stop Building. Start Posting.")
- **Group 4 (General AI Intel):** `LXSxrLIxoaA`, `RmT2H4J-5A0`, `sbTqBo0SZRc`, `kfUOSckgMjQ` (AI Tools Tier List 2026, open-source AI, etc.)

---

## 4. Stack Gaps Identified (from Group 1 evaluations)

The batch surfaced two real architectural gaps that `yt_transcribe.py` itself cannot fix — they're principle-level concerns the rubric kept flagging:

1. **No `BUILD_OR_EXTEND.md` template exists** — P7 cited 5/6 times in REJECT reasonings. Without a template + worked example, any future "should I build or extend?" decision still requires reasoning from first principles. **Action:** create `templates/BUILD_OR_EXTEND.md` with the overlap-math format the principle requires.
2. **`closed_dependencies.md` is referenced but not written** — P1's exception clause (closed APIs accepted at ≥90% feature parity) names Buffer/Twilio/Lofty but no file documents the exceptions. **Action:** write the doc, naming each closed dependency, the open alternative it was weighed against, and the decision rationale.
3. **No "channel-level" signal layer in `/ai_stack`** — Charlie Automates appeared 2× in Group 1 with promotional content. The rubric evaluates URLs in isolation; channel-level patterns (this creator does X% promotional / Y% technical) would let the engine deprioritize entire creators. **Future enhancement, not blocking.**

---

## 5. Principles in Practice — what this batch taught us

- **The rubric is BIAS-CORRECTLY harsh.** 5/6 REJECT with HIGH confidence is not a calibration problem — it reflects that 60-second YouTube Shorts about token-saving tricks rarely contain enough technical signal to ADOPT. The principle that drove this is P3 ("Token Efficiency, Measured" — ADOPT requires ≥30% reduction with eval rubric ≥90% baseline). Without a number, there's no ADOPT-grade signal.
- **P7 was the most-cited principle.** "Already exists in the stack" was the killer for 4 of 5 REJECTs. This validates §1 of `PRINCIPLES_REVIEW_v1.md` (the build-or-extend gate is the highest-leverage principle long-term).
- **The one ADOPT was a *pattern*, not a tool.** All three skill-building patterns (gotchas section, folder-as-skill, context+constraints) are extend-in-place changes to files Veritas already owns. Zero new files, zero new dependencies. This is exactly what P7 wants.
- **Caching needs a sequential pre-warm pass.** Cache_read = 0 across 6 parallel calls means the 4-worker ThreadPool race-wrote the cache and didn't wait for any one to finish. Fix in next batch: send the first URL synchronously to warm the cache, then parallel-process the remainder. Single-line change.

---

## 6. Operating notes

- **Adding a verdict to this file is automatic** in the sense that `/ai_stack` is the source of truth — but a human curates STACK_DESIGN.md from `vie_group1_results.json` (or the next batch's equivalent) for narrative + action items. This file is the human-readable distillation; `/ai_stack` is the queryable store.
- **Re-running a batch on the same URLs** will hit `/ai_stack`'s URL-dedup and return `dedup: true` — items don't double-post. To re-evaluate, PATCH the existing item to `status=dismissed` first, then re-run.
- **Group sizing:** ThreadPool default is 4 workers. For groups > 6, raise `--max-workers` proportionally (rubric ≈ 2.3K tokens cached, marginal cost is just transcript tokens after first request).

---

*Living document. Update on every batch. First seeded 2026-05-01 (Group 1).*
