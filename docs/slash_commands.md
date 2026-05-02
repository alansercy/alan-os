# Slash Command Skill Wrappers

**Pattern 3 from `memory-bank/VIE_PATTERN_ACTION_LIST.md`** — Claude Code skill wrappers that map common Veritas workflows to a slash-command interface. No Python orchestrator layer per Alan's 2026-05-02 confirmation; each wrapper is a thin SKILL.md that invokes its target script via Bash.

**Skill location:** `~/.claude/skills/<name>/SKILL.md` — global, outside any repo. This file is the canonical inventory; the skill files themselves are not version-controlled.

## Active wrappers (6)

| Slash command | Skill folder | Target |
|---|---|---|
| `/digest` | `~/.claude/skills/digest/` | `python ~/.lux/workflows/daily_digest_v3.py` |
| `/triage` | `~/.claude/skills/triage/` | `python ~/.lux/workflows/lux_launcher.py` (long-running — runs in background) |
| `/vie <url> [--dry-run]` | `~/.claude/skills/vie/` | `python alan-os/workflows/yt_transcribe.py <url>` |
| `/task <title>` | `~/.claude/skills/task/` | `POST http://localhost:8000/tasks` (status=todo, HEREDOC body per gotcha #5) |
| `/handoff` | `~/.claude/skills/handoff/` | `python ~/.lux/workflows/push_handoff.py` |
| `/prospect <company>` | `~/.claude/skills/prospect/` | Claude inline research — no script, no external API. Returns MMM prospect brief from training data. |

## Recreating the skills

The 5 SKILL.md files are not in any repo. To recreate on a fresh host:

1. `mkdir -p ~/.claude/skills/{digest,triage,vie,task,handoff}`
2. Write each `SKILL.md` with the frontmatter `name` + `description` shown in the live available-skills list
3. Body is a single Bash invocation block — see this doc's table for targets

## Convention drift note

CLAUDE.md §8 says folder-as-skill uses `prompt.md` as the canonical filename. The actual ecosystem (GSD, alireza, obra superpowers, and these 5 wrappers) all use `SKILL.md`. CLAUDE.md §8 should be updated to match — flagged as carry-forward.
