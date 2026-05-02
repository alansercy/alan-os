# content_pack

**Purpose:** Loretta content engine (MoveWithClarity, Roots & Room) + Veritas marketing copy across all surfaces. Also serves Veritas/MMM BD outreach.

**Load when:** writing or rewriting marketing copy (landing pages, emails, posts), planning content strategy, drafting cold outreach or lifecycle email sequences, planning a launch, or building short-form video pipelines.

**BD note:** the originally-proposed `bd_pack` was dropped because it was a strict subset of content_pack (`cold-email` + `email-sequence` + `launch-strategy`). BD work uses the content_pack member set with a different lens — same skills, different audience and intent. When loading for BD, prioritize `cold-email` (unsolicited outreach) and `email-sequence` (post-reply nurture); when loading for Loretta content, prioritize `copywriting` and `content-strategy`.

## Members

| Skill | Use |
|---|---|
| `copywriting` | Marketing copy for landing pages, homepage, pricing, feature pages |
| `cold-email` | B2B cold outreach to unsolicited prospects (BD primary use) |
| `email-sequence` | Lifecycle emails, drip campaigns, nurture sequences (opted-in subscribers) |
| `content-strategy` | Plan content calendars, topic clusters, blog strategy |
| `launch-strategy` | Phased product launches, GTM plans, Product Hunt, waitlist motion |
| `video-content-strategist` | YouTube channels, video scripts, short-form video pipelines, repurposing |

## Missing capability — `/prospect`

Pattern 3 (slash command wrappers, see `docs/slash_commands.md`) deferred `/prospect <company>` because no per-company research entry point exists. When that capability lands — n8n workflow, Python script, or Claude-driven enrichment lookup — add it here as a member of content_pack with a BD lens.

## Pattern source

Pattern 5 from `memory-bank/VIE_PATTERN_ACTION_LIST.md` — skill packs as pointer-lists. Members live at `~/.claude/skills/<name>/` and are discoverable via the available-skills list. This file is the index, not a relocator.
