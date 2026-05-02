# stack_pack

**Purpose:** VIE evaluation, AI infrastructure, architecture decisions, systematic debug.

**Load when:** starting work on Veritas stack design, evaluating new tools/patterns via VIE, building or migrating Anthropic SDK code, debugging non-trivial issues, or reviewing planned changes before implementation.

## Members

| Skill | Use |
|---|---|
| `vie` | Run `yt_transcribe.py` against a YouTube URL — pattern extraction + ADOPT/EVALUATE/MONITOR/REJECT verdict |
| `claude-api` | Build/migrate Anthropic SDK code — caching, model versions, tool use, batch |
| `superpowers:brainstorming` | Required before creative work — explore intent + requirements before implementation |
| `superpowers:writing-plans` | Multi-step task with spec → write a plan before touching code |
| `superpowers:executing-plans` | Execute a written plan in a separate session with review checkpoints |
| `superpowers:systematic-debugging` | Use on any bug, test failure, or unexpected behavior — before proposing fixes |
| `superpowers:requesting-code-review` | Verify work meets requirements before merging |
| `superpowers:verification-before-completion` | Run verification commands and confirm output before claiming done |
| `superpowers:writing-skills` | Creating, editing, or verifying skills before deployment |
| `gsd-extract-learnings` | Extract decisions, lessons, patterns from completed phase artifacts |
| `gsd-debug` | Systematic debugging with persistent state across context resets |

## Pattern source

Pattern 5 from `memory-bank/VIE_PATTERN_ACTION_LIST.md` — skill packs as pointer-lists. Members live at `~/.claude/skills/<name>/` and are discoverable via the available-skills list. This file is the index, not a relocator.
