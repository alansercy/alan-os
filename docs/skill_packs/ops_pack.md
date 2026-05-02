# ops_pack

**Purpose:** Daily Veritas operations — email triage, digest, handoff, task capture, scheduled work, harness configuration.

**Load when:** running the daily ops loop (triage → digest → tasks), capturing work into `tasks.json`, scheduling recurring agents, configuring Claude Code permissions/hooks, or closing a session.

## Members

| Skill | Use |
|---|---|
| `digest` | Run `daily_digest_v3.py` — morning email summary from `tasks.json` + `projects.json` |
| `triage` | Run `lux_launcher.py` — sequential email triage across MSN/Gmail/Loretta/Keys/MMM + AI Research Monitor |
| `handoff` | Run `push_handoff.py` — push session handoff doc to Drive (CLAUDE.md §4 step 4) |
| `task` | POST `localhost:8000/tasks` — capture work surfaced mid-session before context is lost |
| `schedule` | Create/manage cron-scheduled remote agents (one-time or recurring) |
| `loop` | Run a prompt or slash command on a recurring interval (or self-paced) |
| `update-config` | Configure the Claude Code harness — settings.json, hooks, env vars, permissions |
| `fewer-permission-prompts` | Scan transcripts and add a prioritized allowlist to `.claude/settings.json` |

## Pattern source

Pattern 5 from `memory-bank/VIE_PATTERN_ACTION_LIST.md` — skill packs as pointer-lists. Members live at `~/.claude/skills/<name>/` and are discoverable via the available-skills list. This file is the index, not a relocator.
