# claude.ai — session start prompt

> Paste the block below into a fresh claude.ai chat to resume work. Replace `<GITHUB_RAW_PROJECTS_URL>` with the real raw GitHub URL for `PROJECTS.md` once the repo has a remote (see `SESSION_PROTOCOL.md` → Setup). Then paste the contents of the most recent `HANDOFF_YYYY-MM-DD.md` below the prompt where indicated.

---

```
You are picking up work on alan-os, my operating system repo. Two sources of truth:

1. PROJECTS.md — live status board. Fetch the current version from:
   <GITHUB_RAW_PROJECTS_URL>

2. The most recent claude.ai handoff, pasted below this prompt.

Do this:
- Fetch and read PROJECTS.md from the URL above.
- Read the HANDOFF block below.
- Tell me: what's the current state, what was last worked on in claude.ai, and what's the most important next action.
- Flag any inconsistency between PROJECTS.md and the handoff.
- Do not start work until I confirm the direction.

--- HANDOFF BEGIN ---

<paste contents of HANDOFF_YYYY-MM-DD.md here>

--- HANDOFF END ---
```
