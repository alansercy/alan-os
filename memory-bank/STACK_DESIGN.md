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
  1. ✅ **DONE 2026-05-01.** Added `## 7. Gotchas (negative-example log)` to `CLAUDE.md` with 8 entries seeded from session-log: n8n PUT metadata-strip, n8n Anthropic HTTP-node typeVersion 4.2, Sheets `__rl` wrapper, MMM tracker row-3 header, Windows bash curl heredoc, headless-Chrome `cygpath -w`, Desktop OAuth `run_local_server(port=0)`, and "verify before recommending extend-not-build" (Alan-corrected from VIE session — `shorts_researcher.py` was metadata-only, not transcript extraction).
  2. ⛔ **Out-of-scope-for-this-repo.** This action targets Claude Code skill files at the system level (`~/.claude/skills/`), not files in `alan-os`. The repo has no `.claude/skills/` directory and no single-file skills to convert. Convention is documented in §8 of CLAUDE.md so future skill authoring follows the pattern; a global skill audit is deferred until that work is on the queue.
  3. ✅ **DONE 2026-05-01.** Added `## 8. Skill File Convention (folder-as-skill)` to `CLAUDE.md`. Documents the `prompt.md + /scripts + /examples + /templates` structure, the why (progressive disclosure, single canonical store, explicit asset coupling), and the scope note that this repo doesn't host skills.

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

## 2.C Groups 5-7 Batch — 2026-05-01 (pre-warm + parallel, 20 URLs)

**Run shape:** 1 sync pre-warm URL (max-workers=1) followed by a 19-URL parallel batch (max-workers=4). User directive: "Pre-warm cache with one synchronous call first." Goal: test whether pre-warming resolves the cache_read=0 anomaly seen in Groups 2-4.

**Result:** 20 URLs / 19 transcripts pulled / 1 yt-dlp metadata error / 19 evaluated / 19 posted to `/ai_stack`.
**Verdict distribution:** **0 ADOPT · 0 EVALUATE · 1 MONITOR · 18 REJECT · 1 ERROR.**

**Caching anomaly — REVISED 2026-05-01 PM after rerun (deduped on /ai_stack but fresh SDK telemetry):** SDK 0.94.0 *does* surface cache_write — the prior conclusion ("SDK not surfacing cache fields") is wrong. Observed pattern across 20 calls in this session's rerun: `cache_write` fired on ~7 calls with real values (2247-2520 tokens; 11,791 total in the parallel batch), but `cache_read=0` on every single call. Refined hypothesis: Anthropic's prompt cache is per-node and TTL-bound. Each request lands on a node where either (a) no cache exists for the system-prompt hash → cache_write fires, or (b) a cache exists from a different request that isn't shared with this session. cache_read requires the same node within TTL — and we never hit that. **Cost implication:** observed cost is approximately the *uncached* cost. cache_write tokens (~$3.75/MTok) are paid without amortization across the batch. If cache_read worked, per-URL cost would drop ~80%. **Action:** stop investigating in-band. If cache costs become material, revisit by either filing with Anthropic support or testing single-process long-lived clients (vs yt_transcribe.py's per-batch Anthropic-instance pattern). Functional behavior unaffected — defer indefinitely.

**yt-dlp ERROR — `4nXxY_AaXuY`:** `WARNING: [youtube] No supported JavaScript runtime could be found. Only deno is enabled by default; to use another runtime add --js-runtimes RUNTIME[:PATH] to your command/config. YouTube extraction without a JS runtime has been deprecated.` This is a yt-dlp upstream change requiring a JS runtime (Deno default) for some YouTube format extraction. Not a `yt_transcribe.py` bug. Fix options: (a) install Deno on host, (b) pin yt-dlp to a pre-deprecation version, (c) handle the error gracefully and continue the batch (current behavior — 1 URL skipped, 19 succeeded). Logged as new stack gap §4.4.

### MONITOR × 1

#### `youtube.com/shorts/LXB_dBvDSOE` — "Redesign Claude Design?" (Jake Van Clief, ~60s) — score 4, layer **orchestration**, confidence **LOW**
- **Pattern surfaced:** Ordered-markdown skill files read in sequence by Claude Code. Creator claims materially lower token usage than Anthropic's own "Claude Design" plugin.
- **Why MONITOR (not ADOPT, not REJECT):** This is a **testable P3 claim** (the creator names a specific token-efficiency advantage over a named competitor) — exactly the kind of measurable lift the rubric rewards. **But zero benchmarks, no code, no methodology** in the 60s short, so P3 cannot be scored. P7 also flags risk: directly adjacent to the §2 Group 1 ADOPT (folder-as-skill from AI Honeycove) — the same pattern from a different creator. The Group 1 ADOPT was based on the *pattern* being extend-in-place (no file > 50 lines needed); this MONITOR mentions the same pattern with an unverified efficiency claim attached.
- **Re-eval gate:** if a code repo or methodology surfaces (creator's GitHub, a follow-up technical post, or an independent benchmark on the ordered-skill-file pattern vs Claude Design), promote to EVALUATE. Until then, the pattern is already partially covered by §8 of CLAUDE.md (folder-as-skill convention) — no new action needed.

### REJECT × 18

For each REJECT, failing principles cited so we don't re-evaluate without new technical information.

#### HIGH PRIORITY block (4 URLs, all REJECT)

**`youtube.com/shorts/251Xs-sIy8U` (pre-warm)** — "Free Tool / Claude Cowork" (Hasan Toor) — score 2, layer none. Fails **P1** (gated behind DM, no documented API), **P3** (zero token data), **P7** (≥60% overlap with Alan OS + VIE pipeline), and **Anthropic-only constraint** (multi-LLM pitch — Ollama, GPT). *Re-eval gate:* none — multi-LLM is architecturally incompatible.

**`youtube.com/shorts/f_o-_LZyldo`** — "Claude Can Now Control Your Computer" (Nick Puru) — score 2, layer orchestration. Fails **P3** (no token data, no comparison vs existing Outlook COM + n8n workflows), **P7** (computer use overlaps existing automation layer; needs BUILD_OR_EXTEND that this video can't seed). Engagement-bait. *Re-eval gate:* none — underlying Anthropic capability already known; ADD if Anthropic ships a stable computer-use SDK with token-efficiency data.

**`youtube.com/shorts/yaBDLroG0Lo`** — "Claude Code Agentic OS Is The Future" (Chase AI) — score 1, layer none. Fails **P3** (zero data), **P7** (≥90% conceptual overlap with Alan OS + AgentOS + Lux Command Center), **P8** (Obsidian as memory store conflicts with declared canonical stores). *Re-eval gate:* none — no new capability.

**`youtube.com/shorts/337Qc9vOxwY`** — "Stop building Agents and start building something that lasts" (Jake Van Clief) — score 2, layer none. Fails **P3** (no rubric), **P7** (markdown-as-orchestration ≥90% overlap with CLAUDE.md + alan_os_server.py). Motivational framing of a pattern Veritas already ships. *Re-eval gate:* none.

#### REMAINDER block (14 REJECTs from the parallel batch)

**`youtube.com/shorts/AQ_ca27ftQs`** — "Claude Just Made Marketing Agencies IRRELEVANT" (Zack the AI Guy) — score 1. GUI-clicks workflow, "skill" concept >60% overlap with CLAUDE.md system prompts. Fails **P1, P3, P7**.

**`youtube.com/shorts/DKg_fMLKpd4`** — "SECRET Million Dollar App Idea" (Jonathan Acuña) — score 1. Pasting App Store screenshots into Claude — no integration work. Fails **P3, P7, P9**.

**`youtube.com/shorts/1F-Bww76qB0`** — "This is the one tool that actually gets smarter" (Maverick) — score 2. Closed SaaS Chrome extension, multi-LLM (GPT, Gemini), RAG ≥60% overlap with existing VIE pipeline. Fails **P1, P6 (data residency), P7, Anthropic-only constraint**.

**`youtube.com/shorts/2bvuLxj6nT4`** — "How to build a Second Brain (prompt)" (Don't Sleep On AI) — score 2, layer memory. Paid black-box prompt; Obsidian GUI-only; replicates existing CLAUDE.md + session-log. Fails **P1, P3, P7**.

**`youtube.com/shorts/-CO3ohQqloA`** — "5 Secret Claude Hacks" (Nick Puru) — score 1. Undocumented prompt "codes" with no eval. Fails **P1, P3, P7**.

**`youtube.com/shorts/iUV5LJqHXeY`** — "Top Claude Code Plugins to 10X" (Prajwal Tomar) — score 2, layer orchestration. Mentions `claude mem` again (already REJECTED in §3). No benchmarks, lead-gen teaser. Fails **P3, P7, P10**.

**`youtube.com/shorts/M9qgd_KJkWc`** — "Claude Code Just Killed $10,000 Websites" (Duncan Rogoff) — score 1. UI kit wrapper around already-stack-resident Claude Code. Fails **P3, P7, P9**.

**`youtube.com/shorts/FtBezgCu0vo`** — "I have never hit a usage limit and still make over 30 grand" (Jake Van Clief) — score 1. Community-acquisition funnel, structured-folder pattern ≥60% overlap with CLAUDE.md. Fails **P3, P7**.

**`youtube.com/shorts/2chpu6Ma1MY`** — "How to Clone Applications with AI in SECONDS" (Brennan Wells) — score 1. CopyCod GUI-only, redundant with Lux Command Center. Fails **P1, P3, P7**.

**`youtube.com/shorts/UmRw3BlANK0`** — "Free AI second brain" (Alex Tavi) — score 1, layer memory. Obsidian GUI-only; concept already covered by CLAUDE.md + session-log + Drive long-term. Prompt withheld behind comment-farming gate. Fails **P1, P3, P7**.

**`youtube.com/shorts/yRHPmrVeC24`** — "Clone any app with AI in 30 sec" (Nate Gold) — score 1. Bolt.new + Copy Coder AI thin-wrapper >60% overlap with direct Claude vision prompting. Fails **P1, P3, P7**.

**`youtube.com/shorts/O92SF2TYidQ`** — "If you want to become a millionaire" (Dan Martell) — score 0. Motivational book recommendations, zero technical signal. Fails everything by default. Not even MONITOR-grade. *Channel pattern:* Dan Martell now 2× REJECT (Group 4 + here) — deprioritize.

**`youtube.com/shorts/VXtAXAhY8uw`** — "Get AI to Recommend Your Business!" (JakeOnGrowth) — score 2. 99-cent book ad disguised as insight. GEO concept worth monitoring through better sources. Fails **P3, P7**.

**`youtube.com/shorts/9JrU0tXo_yg`** — "PROVEN AI Avatar System" (Jonathan Acuña) — score 1. Closed SaaS GUI workflow; Buffer + Claude API already cover scheduling. Fails **P1, P3, P7**.

#### Channel-level recurrence (Groups 5-7)

- **Jake Van Clief — 2× (337Qc9vOxwY REJECT + LXB_dBvDSOE MONITOR).** Mixed signal: technical patterns surface but without measurement. Keep monitoring; do not deprioritize.
- **Nick Puru | AI Automation — 2× (f_o-_LZyldo + -CO3ohQqloA, both REJECT).** Plus prior NCzV-CerZuI (Group 2). Now 3× REJECT total. **Deprioritize** unless title indicates benchmark or API spec.
- **Jonathan Acuña - Doctor AI — 2× (DKg_fMLKpd4 + 9JrU0tXo_yg, both REJECT).** Lead-gen pattern. **Deprioritize.**
- **Dan Martell — now 2× total (LXSxrLIxoaA Group 4 + O92SF2TYidQ here, both REJECT).** Motivational/strategy content, no technical depth. **Deprioritize.**

---

## 2.D VIE v2 Three-Lens Re-Evaluation — 2026-05-01 PM

**Run shape:** Patched `yt_transcribe.py` `PRINCIPLES_RUBRIC` with the v2 three-lens prompt per `memory-bank/VIE_PROMPT_PATCH.md` (canonical at `C:/Veritas/repos/memory-bank/VIE_PROMPT_PATCH.md`). Dry-run test on Group 1 ADOPT URL (`3E59wf8RA8Y`) confirmed `pattern_extraction` and `strategic_signal` blocks present and the summary tracked actual transcript content. Then re-evaluated all 33 previously-processed URLs (1 sync pre-warm + 32 parallel max-workers=4, all `--dry-run` so `/ai_stack` was NOT touched). Skipped `4nXxY_AaXuY` (yt-dlp JS-runtime ERROR, deferred until deno install).

**The headline number:** **22 of the original 30 REJECT verdicts flipped to ADOPT or EVALUATE under the new prompt** — 14 to ADOPT, 8 to EVALUATE. Two more REJECTs flipped to MONITOR. Six REJECTs held. Both original MONITORs upgraded (one to ADOPT, one to EVALUATE). The single original ADOPT held.

**Old vs new totals (across the same 33 URLs):**

| Verdict | v1 | v2 | Change |
|---|---:|---:|---:|
| ADOPT | 1 | 16 | +15 |
| EVALUATE | 0 | 9 | +9 |
| MONITOR | 2 | 2 | 0 |
| REJECT | 30 | 6 | −24 |

**Token cost (33 URLs + 1 dry-run validation):** input ~52,600 · output ~31,800 · cache_write 0 · cache_read 0. ≈ $0.66 at Sonnet 4.6 base-context rates.

### What the v1 rubric missed — sample patterns extracted by v2

Each entry below is a pattern Claude flagged as `priority: immediate` from a video the v1 rubric REJECTed. Cited verbatim from `pattern_extraction.patterns[].description`.

1. **`xM99M7aLFhQ` (GSD plugin, REJECT→ADOPT)** — "Three-stage project protocol: discovery (deep questions) → phase planning → phase execution, enforced as distinct commands rather than a single agent loop." Plus: "Phase-gated execution: generate full phased roadmap first, then require explicit phase selection before any code runs." *Note: the GSD repo was independently installed and is now in production per VIE_PROMPT_PATCH.md preamble — v2 correctly catches what v1 missed.*

2. **`8BZupIIVhjs` (Nick Automates, REJECT→ADOPT)** — "Route planning to stronger model (Opus), execution to faster/cheaper model (Sonnet) via explicit model-tier switching." Plus the `ultra think` prefix as an extended-reasoning trigger.

3. **`M9lAIBQerUI` (Sabrina Ramonov "marketing dept", REJECT→ADOPT)** — "Slash command shortcuts (/post, /script, etc.) as a user-facing interface layer on top of Claude — reducing prompt friction to a single trigger." Plus "Teach Claude platform-specific voice and format rules as persistent instructions rather than re-prompting each session."

4. **`yaBDLroG0Lo` (Chase AI "Agentic OS", REJECT→ADOPT)** — "Skill packs as named, modular capability bundles (research pack, content pack, custom pack) — discrete deployable units rather than monolithic prompts." Plus "Frame agentic OS as a client deliverable from day one — productization mindset baked into architecture decisions, not retrofitted."

5. **`337Qc9vOxwY` (Jake Van Clief, REJECT→ADOPT)** — "Use a markdown file (CLAUDE.md) as the primary orchestration layer, with scripts routed through it rather than building explicit agent graphs." Plus "Folder structure as the organizing framework for agent capabilities — folders ARE the architecture, not a convenience."

6. **`AQ_ca27ftQs` (Zack the AI Guy "marketing irrelevant", REJECT→ADOPT)** — "Public GitHub repo of 29 marketing skill files provides a ready-made library of prompt engineering patterns." Plus "Skill-as-file convention: each capability gets its own versioned .md file with a defined name."

7. **`2bvuLxj6nT4` (Don't Sleep On AI "second brain", REJECT→ADOPT)** — "End-of-session write protocol: instruct Claude to write a detailed structured log to a designated persistent location before session ends." Plus "Vault pointer in agent bootstrap: CLAUDE.md or agent system prompt explicitly names where the memory store lives so the agent self-orients on resume."

8. **`-CO3ohQqloA` (Nick Puru "5 secret hacks", REJECT→ADOPT)** — "Use 'OODA' as a prompt prefix or instruction to invoke Observe-Orient-Decide-Act decision framework analysis." Plus the `scaffold` prefix as a task decomposition trigger.

9. **`UfYP7t903Pc` (Duncan Rogoff "stop building start posting", REJECT→ADOPT)** — "Post about what you're building while building it — the build log itself is marketing content, not just internal documentation." *Adjacent to LinkedIn Authority Track planning in `PROJECTS.md`.*

10. **`LXB_dBvDSOE` (Jake Van Clief "Redesign Claude Design", MONITOR→ADOPT)** — same skill-file ordering pattern that drove the original MONITOR, now scored ADOPT/HIGH because v2's pattern lens treats the pattern itself as adoptable even without a full benchmark.

### Held REJECTs (6 URLs)

These cleared the new "all three lenses produce zero value" bar — the v2 rubric is bias-correctly preserving genuine rejection grounds. URLs: `251Xs-sIy8U` (Robote multi-LLM follower-farm), `DKg_fMLKpd4` (App ideation hack, no actionable depth), `1F-Bww76qB0` (Recall Chrome ext multi-LLM), `2chpu6Ma1MY` (Bolt no-code clone), `O92SF2TYidQ` (Dan Martell book recommendations — fully off-topic), `9JrU0tXo_yg` (AI avatar DM funnel, no tools named).

### Schema break — known degradation in dry-run results

The v2 schema dropped `relevance_score`, `fit_pipeline`, and `fit_rationale` from the top-level output (these were v1-only). `process_url()` and `post_to_ai_stack()` in `yt_transcribe.py` still read those keys via `.get()` defaults, so:
- `result["score"]` is **always 0** in v2 stdout/JSON
- `result["fit_pipeline"]` is **always "none"** in v2 stdout/JSON
- The `pattern_extraction` and `strategic_signal` blocks ARE captured (under `result["eval"]`)
- Real POST to `/ai_stack` (non-dry-run) would post degraded fields

**Action:** before running v2 in non-dry-run mode, patch `process_url()` to extract `relevance_score` from a derived metric (e.g. `len(pattern_extraction.patterns)` × `confidence_weight`) and either keep `fit_pipeline` in the prompt schema OR derive from `stack_layer`. Out of scope for this prompt-replacement patch.

### Caveat — these results are a hot rubric run, not the final story

- **`/ai_stack` was NOT updated** — all 33 calls used `--dry-run`. The store still holds v1 verdicts. To replace them, PATCH each existing record to `status=dismissed` and re-run without `--dry-run` (after the schema-break patch above).
- **22 flips to ADOPT/EVALUATE in one prompt change** is a strong signal that v1 was over-rejecting — but it also means the ADOPT-bar moved. Some of the 16 new ADOPTs are pattern-only (Lens 1 drove the verdict) where the original tool would still REJECT under Lens 2. Action items in those entries should be evaluated for "extend-in-place" feasibility before any `BUILD_OR_EXTEND.md` work.
- **Cache observation:** all 33 v2 calls reported `cache_read=0` AND `cache_write=0`. New system prompt; per the per-node-routing hypothesis from §2.C, cache may form across calls but never re-hit in this batching pattern.

### Action items (sorted by quick-win priority)

These are the patterns the v1 rubric would have left on the table indefinitely. Treat as candidates, not commitments — vet against `BUILD_OR_EXTEND.md` (still missing — see §4.1) before any new file > 50 lines.

- **Immediate (low effort, extend-in-place):**
  1. End-of-session write protocol — extend the §4 session-close checklist in `CLAUDE.md` so Claude writes a structured `session-log` entry as a hard rule, not a soft expectation. (`2bvuLxj6nT4`)
  2. Vault pointer in agent bootstrap — confirm `CLAUDE.md` already names the canonical memory stores; if any agent prompt doesn't, add the pointer. (`2bvuLxj6nT4`)
  3. Slash command interface for high-frequency ops (`/post`, `/script`, `/triage`, etc.) on top of `alan_os_server.py` — already partially implemented in Lux Command Center; consider a `~/.claude/commands/` shortcut layer. (`M9lAIBQerUI`)
  4. Model tier routing (Opus plan / Sonnet execute) — already standard in Claude Code; document the convention in `CLAUDE.md` so it's explicit. (`8BZupIIVhjs`)
- **Next-session (medium effort, requires design call):**
  5. Skill packs as modular capability bundles — formalize a `skill-pack/` convention sitting on top of the existing folder-as-skill structure (CLAUDE.md §8). Bundles get their own README and inter-pack contracts. (`yaBDLroG0Lo`)
  6. Phase-gated execution protocol — if GSD's three-stage discovery → phase plan → phase execute pattern isn't fully wired into the current Claude Code session flow, add it as a discipline doc. (`xM99M7aLFhQ`)
  7. Build-log-as-marketing — ties to the LinkedIn Authority Track in `PROJECTS.md`. Lightweight first step: each significant `alan-os` commit gets a one-paragraph LinkedIn-draft entry that can later be collated. (`UfYP7t903Pc`)
- **Backlog (defer, low signal-to-effort):**
  8. `OODA` / `scaffold` / `ultra think` prefixes — informal prompt prefixes with no documented Anthropic behavior; tag and try in next prompt iteration only if a measurable lift is testable. (`-CO3ohQqloA`)

---

## 3. Pending Evaluations

**Spec batch complete + Groups 5-7 ad-hoc batch complete (34/34 URLs across 7 groups, 2026-05-01).** Queue empty.

Standing follow-up watch list (from MONITOR + flagged REJECT re-eval gates):
- ⛔ **`notebookmation` — REJECTED 2026-05-01.** No GitHub repo exists under that exact name (likely the video misnamed the tool, or it's an obscure fork). Investigated the broader category of NotebookLM↔Claude-Code bridges as a stand-in. **Finding: Google does not publish an official NotebookLM API.** Every tool in this space falls into one of two categories, both fragile: (a) undocumented-internal-API reverse engineering — e.g. `teng-lin/notebooklm-py` README explicitly discloses "undocumented Google APIs that can change without notice"; (b) browser automation — e.g. `PleasePrompto/notebooklm-mcp` runs Patchright Chrome automation (`"via": "chrome-automation"`). Fails **P1** (no documented API surface), **P3** (no token/benchmark data anywhere in the category), **P4** (cold-start runability not guaranteed — internal endpoints break, UI redesigns break). No impact on existing stack: `nlm_feed_builder.py` does not use NotebookLM API at all (writes to local JSON + `/ai_stack`); NotebookLM stays on the manual-surface list per `STACK_DESIGN.md` §1 MEMORY exceptions. **Re-eval gate:** revisit only if Google ships a published, supported NotebookLM API.
- **`Whisper Flow`** — re-evaluate when a PersonalOS dictation use case becomes active.
- **Jake Van Clief ordered-skill-file pattern (`LXB_dBvDSOE`)** — promote to EVALUATE if a code repo, methodology, or independent benchmark surfaces showing measurable token reduction vs Anthropic's Claude Design plugin. Until then, the underlying pattern is already partially captured by §8 of CLAUDE.md (folder-as-skill convention) so no immediate action.
- ⛔ **`Claude Mem` — REJECTED 2026-05-01.** Repo: [`thedotmack/claude-mem`](https://github.com/thedotmack/claude-mem) (46.1K stars). Claude-Code-IDE plugin: 5 lifecycle hooks (SessionStart, UserPromptSubmit, PostToolUse, Stop, SessionEnd) + Worker Service on port 37777 with 10 REST endpoints + 3 MCP tools (`search`, `timeline`, `get_observations`) + Web Viewer UI. Storage: SQLite + Chroma vector DB. **README claims "~10x token savings by filtering before fetching details" but provides ZERO supporting data — no benchmark, no eval rubric, no measured comparison.** Fails **P3** decisively (P3 ADOPT requires ≥30% reduction with eval rubric ≥90% baseline; "10x with no rubric" is anecdotal). Fails **P8** — would create a SECOND parallel memory surface alongside the existing `~/.claude/projects/.../memory/MEMORY.md` auto-memory index + `memory-bank/session-log.md` + `~/.lux/Data/*.json`. Same Principle 8 violation that the 2026-05-01 digest-dashboard reconcile session just fixed. Fails **P7** — high overlap with existing memory architecture: Claude Code already has progressive-disclosure auto-memory (typed feedback/user/project/reference files indexed by `MEMORY.md`), and `session-log.md` provides the hand-curated "What worked / Blockers / Next step" record. Migrating to SQLite + Chroma would lose git-versionability of memory and drop the hand-curated readability that makes `session-log.md` useful for human session-resume. Also fails **P4** subsidy: adds 4 new dependencies (Bun runtime, Worker Service, SQLite, Chroma) to cold-start. **46.1K stars is social proof, not technical proof — the rubric requires technical proof.** **Re-eval gate:** revisit only if (a) a third-party benchmark publishes a measured token-reduction number against a defined task corpus, AND (b) Alan independently decides the existing manual session-log + auto-memory pattern has become a bottleneck rather than an asset.
- **Channel deprioritization (cumulative across all 7 groups):**
  - **Charlie Automates** (2× Group 1, Graphify promo) — deprioritize unless title indicates technical depth.
  - **Nick Puru | AI Automation** (3× total: G2 + G5-7 ×2, all REJECT) — deprioritize unless title indicates benchmark or API spec.
  - **Jonathan Acuña - Doctor AI** (2× G5-7, lead-gen pattern) — deprioritize.
  - **Dan Martell** (2× G4 + G5-7, motivational/strategy) — deprioritize unless title indicates technical depth.

---

## 4. Stack Gaps Identified (from Group 1 evaluations)

The batch surfaced two real architectural gaps that `yt_transcribe.py` itself cannot fix — they're principle-level concerns the rubric kept flagging:

1. **No `BUILD_OR_EXTEND.md` template exists** — P7 cited 5/6 times in REJECT reasonings. Without a template + worked example, any future "should I build or extend?" decision still requires reasoning from first principles. **Action:** create `templates/BUILD_OR_EXTEND.md` with the overlap-math format the principle requires.
2. **`closed_dependencies.md` is referenced but not written** — P1's exception clause (closed APIs accepted at ≥90% feature parity) names Buffer/Twilio/Lofty but no file documents the exceptions. **Action:** write the doc, naming each closed dependency, the open alternative it was weighed against, and the decision rationale.
3. **No "channel-level" signal layer in `/ai_stack`** — multiple creators have now surfaced 2-3× across batches (Charlie Automates, Nick Puru, Jonathan Acuña, Dan Martell). The rubric evaluates URLs in isolation; channel-level patterns (this creator does X% promotional / Y% technical) would let the engine deprioritize entire creators. **Future enhancement, not blocking.**
4. **yt-dlp JS-runtime dependency** (added Groups 5-7) — recent yt-dlp versions warn that "YouTube extraction without a JS runtime has been deprecated" and require Deno (or another runtime) for full format extraction. One URL in Groups 5-7 (`4nXxY_AaXuY`) failed at the metadata step with this exact warning. **Action options:** (a) install Deno on host (recommended path per yt-dlp), (b) pin yt-dlp to a pre-deprecation version, (c) catch the metadata error gracefully so the batch continues (already happens — batch processed 19/20). Mid-priority since the batch survives, but adoption rate of the deprecation will increase failure rates on future batches.

---

## 5. Principles in Practice — what 34 URLs across 7 groups taught us

**v1 aggregate verdicts (kept here for delta context — superseded by v2 totals below):**
- 1 ADOPT (3%) — a *pattern* (skill-file authoring from Group 1), not a tool
- 0 EVALUATE
- 2 MONITOR (6%) — `notebookmation` (subsequently REJECTED in §3) + `LXB_dBvDSOE` Jake Van Clief
- 30 REJECT (88%)
- 1 ERROR (3%) — `4nXxY_AaXuY` yt-dlp JS-runtime

**v2 aggregate verdicts (after three-lens prompt re-eval, dry-run only — see §2.D):**
- **16 ADOPT (47%)** — most are pattern-only (Lens 1 drove the verdict); the original ADOPT held
- **9 EVALUATE (26%)** — pattern + tool combinations needing one test session
- **2 MONITOR (6%)** — `RmT2H4J-5A0`, `VXtAXAhY8uw`
- **6 REJECT (18%)** — held the line on multi-LLM, off-topic, or zero-actionable-content
- **1 ERROR (3%)** — `4nXxY_AaXuY` (unchanged, deno install pending)

**Pattern-level findings (revised after v2 rerun):**
- **The v1 rubric was over-rejecting.** v2's three-lens design lifted REJECT from 88% to 18% on the same 33 URLs by adding pattern extraction (Lens 1) and strategic signal (Lens 3) as primary evaluation surfaces alongside tool fit (Lens 2). 22 URLs flipped REJECT → ADOPT/EVALUATE under v2. The cost of a wrong v1 REJECT was real: patterns like "GSD three-stage protocol", "model tier routing", "skill packs as bundles", "build-log-as-marketing" were all left on the table by v1 and surfaced cleanly by v2. v1's bias toward measurable token-efficiency benchmarks made every short look like noise; v2 treats actionable patterns and strategic signals as first-class outcomes.
- **P7 remains the most-cited principle.** "Already exists in the stack" or "would require BUILD_OR_EXTEND analysis" was the killer in the vast majority of REJECTs across all 7 groups. Confirms `PRINCIPLES_REVIEW_v1.md` §5 ranking — P7 is the most-load-bearing principle long-term, and `BUILD_OR_EXTEND.md` (still missing — see §4.1) is increasingly the load-bearing template.
- **The one ADOPT was a *pattern*, not a tool.** All three skill-building patterns (gotchas, folder-as-skill, context+constraints) are extend-in-place changes to files Veritas already owns. Zero new files, zero new dependencies. Now landed in `CLAUDE.md` §7 + §8 (commit `053b256`).
- **Memory-pattern over-saturation.** Across 34 URLs, ≥6 different "second brain" / "Claude memory" / "Obsidian-as-memory" tools were pitched. All REJECTED on P7 + P8 grounds (overlap with existing CLAUDE.md + session-log + auto-memory + JSON stores). Strong signal that the AI-content economy is creating tools for problems already solved by the existing memory architecture; the stack should remain stable here, not chase the next plugin.
- **Anthropic-only constraint repeatedly violated by surfaced tools.** At least 4 of 34 URLs pitched multi-LLM systems (Ollama / GPT / Gemini integrations). All auto-REJECTED. Confirms the constraint is doing real filtering work.
- **Channel-level signal accumulating — deprioritize unless future titles show benchmarks or API specs.** Across 7 groups, four creators have surfaced ≥2× with consistent low-technical-depth patterns:
  - **Nick Puru | AI Automation** — 3× REJECT, no benchmarks
  - **Dan Martell** — 2× REJECT, opinion / motivational content
  - **Charlie Automates** — 2× REJECT, Graphify promoter
  - **Jonathan Acuña - Doctor AI** — 2× REJECT, no technical depth
  Operational watch list mirrored in §3 for next-batch URL filtering.
- **Caching anomaly — narrowed to per-node cache routing** (revised 2026-05-01 PM). The Groups 5-7 rerun (with deduped /ai_stack but fresh telemetry) showed SDK 0.94.0 DOES surface cache_write — ~7/20 calls wrote 2247-2520 tokens each (11,791 total in the parallel batch). The persistent `cache_read=0` is therefore not an SDK reporting bug. Most likely root cause: Anthropic's prompt cache is per-node and TTL-bound; each request lands on a node where either no cache exists yet (write fires) or the cache lives on a different node (no read possible). Caching is paying nothing in current usage — we get the write costs (~$3.75/MTok) without amortization. **Open item:** test in single-process long-lived client to see if same-session calls hit cache. Functional impact: zero. Cost impact: ~80% potential savings unrealized. Defer until cache costs become material.
- **No vertical-domain content surfaced.** Groups 1-7 were Claude / AI-stack focused per the spec's batch grouping, not vertical-focused. Zero videos relevant to FinanceOS, MMM Trucking workflows, or AgentOS real-estate operations. Future batches sourced from MMM-relevant or AgentOS-relevant content streams (rather than the general AI-influencer feed) would test the engine's verticality and probably surface the first ADOPT in many batches.

---

## 6. Operating notes

- **Adding a verdict to this file is automatic** in the sense that `/ai_stack` is the source of truth — but a human curates STACK_DESIGN.md from `vie_group1_results.json` (or the next batch's equivalent) for narrative + action items. This file is the human-readable distillation; `/ai_stack` is the queryable store.
- **Re-running a batch on the same URLs** will hit `/ai_stack`'s URL-dedup and return `dedup: true` — items don't double-post. To re-evaluate, PATCH the existing item to `status=dismissed` first, then re-run.
- **Group sizing:** ThreadPool default is 4 workers. For groups > 6, raise `--max-workers` proportionally (rubric ≈ 2.3K tokens cached, marginal cost is just transcript tokens after first request).

---

*Living document. Update on every batch. First seeded 2026-05-01 (Group 1).*
