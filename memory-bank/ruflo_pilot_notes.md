# Ruflo Pilot — Pre-Install Scan + Verdict

**Date:** 2026-05-02
**Owner:** Alan Sercy
**Verdict:** **REJECT-overlap. Did NOT install.**
**Outcome:** Skipped `npx ruflo@latest init --wizard` after web scan revealed direct overlap with `utils/model_router.py` (`0c60c1e`) and `utils/context_manager.py` (`91c4a40`) shipped 2026-05-01, plus undocumented CLAUDE.md overwrite behavior.

---

## What Ruflo is

Ruflo (formerly `claude-flow`) by ruvnet — multi-agent orchestration platform for Claude Code. As of 2026-05-02, npm `claude-flow@3.6.12`, GitHub `ruvnet/ruflo`. Ships as either a Claude Code plugin (`/plugin install ruflo-core@ruflo`) or via `npx ruflo@latest init --wizard`. Stack includes 314 MCP tools, 16 agent roles, 19 AgentDB controllers, 21 native plugins, ReasoningBank WASM, SONA neural-pattern self-learning, AgentDB+HNSW vector storage.

## Pre-install scan — 4 questions, 4 findings

| # | Question | Finding | Overlap risk |
|---|---|---|---|
| 1 | Own model routing layer? | YES — "intelligent 3-tier model routing system, saves up to 75% on API costs." Multi-provider failover (Claude/GPT/Gemini/Cohere/local). | **HIGH** — direct collision with `utils/model_router.py` (3-tier haiku/sonnet/opus, shipped `0c60c1e` 2026-05-01) |
| 2 | Own context/memory manager? | YES — AgentDB with HNSW vector indexing + ReasoningBank WASM for embeddings. Persistent cross-session memory. | **HIGH** — same problem space as `utils/context_manager.py` + `memory-bank/session-log.md` + `MEMORY.md`; different paradigm (binary SQLite/vector vs markdown/git) |
| 3 | Modify or replace CLAUDE.md? | YES — "creates a CLAUDE.md file that Claude Code will read as context." Behavior on existing CLAUDE.md (overwrite vs merge vs backup) **NOT specified anywhere in README, USERGUIDE, or wiki Installation Guide.** | **CRITICAL** — our 287-line CLAUDE.md holds n8n gotchas, project state, session protocol earned over months. Silent overwrite would be catastrophic. Undocumented = unsafe even on a test branch. |
| 4 | Conflict with `session-log.md` / memory-bank pattern? | YES — AgentDB persistent memory (binary DB) is a different paradigm than markdown-based `session-log.md` + `MEMORY.md` index (git-versioned, plaintext-grep-able, no DB dependency). | **MEDIUM** — coexistence possible but creates two sources of truth for "what happened in past sessions." |

## What IS genuinely additive (not in our stack)

These would be net-new capability — but they're coupled to the routing+memory+CLAUDE.md infrastructure we'd be replacing, so we cannot adopt them without taking the overlapping pieces:

- Auto-organized agent swarms with consensus (vs our manual ORCH-1/2 sequential+parallel waves)
- 12 auto-triggered workers (audit, test-gaps, optimization) on hooks
- SONA neural patterns + trajectory learning (self-learning from successful runs)
- 5-provider failover (we are Anthropic-only by design — not a feature we want)

## Why REJECT-overlap was the call

Per Principle 7 (Build Only What Doesn't Exist) + gotcha #8 (verify before extending) + the user's stated criterion: *"If Ruflo overlaps significantly with model_router.py and context_manager.py we already shipped — verdict is REJECT-overlap without installing."*

Adopting Ruflo would mean discarding `model_router.py` (`0c60c1e`) + `context_manager.py` (`91c4a40`) shipped one day prior, replacing the markdown memory-bank with a binary AgentDB, and risking silent CLAUDE.md overwrite — all in exchange for orchestration features (swarms, neural patterns) we have no current use case for. ORCH-1/2 covers the parallelization we have.

## Re-evaluation gates (do not adopt unless these flip)

1. **Real multi-agent swarm need** — e.g., AgentOS Platinum buildouts where 5+ clients need parallel autonomous work AND ORCH-2's two-wave parallel model proves insufficient.
2. **Documented CLAUDE.md merge behavior** — if Ruflo ships an explicit `--preserve-claude-md` flag or a documented merge mode that does not clobber existing content.
3. **Lighter-weight install path** — a pattern-only install (drop in skills + agents only, skip routing/memory/CLAUDE.md) would change the calculus.

## Pattern extraction (without installing)

Worth a 30-min STACK_DESIGN.md addition next session: study Ruflo's SONA trajectory-learning concept and the 12-auto-triggered-workers hook pattern as design inputs for VIE-impl-B. Steal the ideas, do not adopt the framework.

## References

- [GitHub — ruvnet/ruflo](https://github.com/ruvnet/ruflo)
- [ruflo/README.md](https://github.com/ruvnet/ruflo/blob/main/README.md)
- [Installation Guide wiki](https://github.com/ruvnet/ruflo/wiki/Installation-Guide)
- [Claude Flow (Ruflo) v3.5 multi-agent guide](https://pasqualepillitteri.it/en/news/774/claude-flow-ruflo-multi-agent-orchestration-guide)
- [npm claude-flow](https://www.npmjs.com/package/claude-flow)
