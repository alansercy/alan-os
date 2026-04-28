# Claude Code — session close prompt

> Paste the block below into Claude Code at the end of a session. Claude Code will produce a fresh `SESSION_NOTES.md` in repo root and report back.

---

```
Close out this session.

1. Run `git status` and `git log --oneline -20` to see what changed since the last commit and across this session.
2. Review the working tree and any uncommitted edits.
3. Write a fresh SESSION_NOTES.md to the repo root (overwriting the previous one) with these sections:
   - Date (YYYY-MM-DD)
   - Session focus — one line
   - What changed — concrete files modified and why, grouped by topic
   - Decisions made — non-obvious choices the next session should not relitigate
   - Open threads — what is still in flight, with enough context to resume cold
   - Next action — single most important next step, one sentence
   - Blockers — anything waiting on me (Alan), an external system, or a credential
4. If there are uncommitted changes that belong with this session's work, list them and ask whether to commit before closing. Do not commit on your own.
5. Update PROJECTS.md and CONTEXT.json only if their current contents are factually wrong after this session's work. Do not rewrite them stylistically.
6. Report the SESSION_NOTES.md path and a one-paragraph summary of where we landed.

Keep SESSION_NOTES.md short and operational — it is a breadcrumb for the next session, not a journal. History lives in git.
```
