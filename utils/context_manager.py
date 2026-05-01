"""Context-window hygiene helpers for Claude Code sessions.

Goal: surface compact/clear recommendations at task boundaries before the
context fills up and the harness force-compacts mid-stream.

Usage:
    from utils.context_manager import checkpoint, run_with_context_check

    checkpoint("after-router-build")             # log + maybe suggest /compact
    run_with_context_check(my_fn, "task-name")   # wraps fn with begin/end checkpoints

Context-percent source — Claude Code does not expose a session API that a
subprocess script can read. We fall back through:
  1. env var CLAUDE_CONTEXT_PCT (e.g. "0.62")
  2. ~/.lux/data/claude_context.json {"pct": 0.62, ...} (a watcher could write this)
  3. None — unknown. should_compact/should_clear stay False so we never
     suggest compacting on a fake reading.
"""
from __future__ import annotations

import json
import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

# ── Paths ─────────────────────────────────────────────────────────────────────
_REPO_ROOT = Path(__file__).resolve().parent.parent
_DEFAULT_SESSION_LOG = _REPO_ROOT / "memory-bank" / "session-log.md"
SESSION_LOG_PATH = Path(os.environ.get("ALAN_OS_SESSION_LOG", str(_DEFAULT_SESSION_LOG)))
CONTEXT_SIGNAL_FILE = Path.home() / ".lux" / "data" / "claude_context.json"

# ── Thresholds ────────────────────────────────────────────────────────────────
COMPACT_THRESHOLD = 0.70
CLEAR_THRESHOLD = 0.90


def get_context_pct() -> float | None:
    """Return current context fill as 0.0–1.0, or None if unknown.

    Spec asked for `-> float`; returning None is the honest answer when no
    source has populated the value. Downstream `should_*` helpers treat None
    as "do not recommend any action" so an unknown reading never false-fires.
    """
    raw = os.environ.get("CLAUDE_CONTEXT_PCT")
    if raw:
        try:
            v = float(raw)
            if 0.0 <= v <= 1.0:
                return v
        except ValueError:
            pass

    if CONTEXT_SIGNAL_FILE.exists():
        try:
            data = json.loads(CONTEXT_SIGNAL_FILE.read_text(encoding="utf-8"))
            v = float(data.get("pct"))
            if 0.0 <= v <= 1.0:
                return v
        except (json.JSONDecodeError, OSError, TypeError, ValueError):
            pass

    return None


def should_compact(threshold: float = COMPACT_THRESHOLD) -> bool:
    pct = get_context_pct()
    return pct is not None and pct >= threshold


def should_clear(threshold: float = CLEAR_THRESHOLD) -> bool:
    pct = get_context_pct()
    return pct is not None and pct >= threshold


def _git_commit_working_state(task_name: str) -> str | None:
    """Stage + commit any uncommitted changes. Returns short hash or None.

    No-op if the working tree is clean. Runs at repo root so we don't depend
    on caller cwd.
    """
    try:
        status = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=_REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=15,
        )
        if status.returncode != 0 or not status.stdout.strip():
            return None
    except (subprocess.SubprocessError, FileNotFoundError):
        return None

    msg = f"auto-checkpoint: {task_name} pre-compact"
    try:
        subprocess.run(["git", "add", "-A"], cwd=_REPO_ROOT, check=True, timeout=15)
        subprocess.run(
            ["git", "commit", "-m", msg],
            cwd=_REPO_ROOT,
            check=True,
            capture_output=True,
            text=True,
            timeout=30,
        )
        sha = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=_REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=15,
        )
        return sha.stdout.strip() or None
    except subprocess.CalledProcessError:
        return None


def _append_session_log(task_name: str, pct: float | None, action: str | None) -> None:
    SESSION_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    pct_str = f"{pct:.0%}" if pct is not None else "unknown"
    line = f"\n## {ts} auto-checkpoint: {task_name}\n- context_pct: {pct_str}\n"
    if action:
        line += f"- recommended: {action}\n"
    with SESSION_LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(line)


def checkpoint(task_name: str) -> None:
    """Mark a task boundary. Log + (if context filling) commit + suggest action.

    Action logic:
      pct >= CLEAR_THRESHOLD  → commit working state, print /clear instruction
      pct >= COMPACT_THRESHOLD→ commit working state, print /compact instruction
      otherwise               → just log the boundary
    """
    pct = get_context_pct()

    action: str | None = None
    if pct is not None and pct >= CLEAR_THRESHOLD:
        action = "/clear"
    elif pct is not None and pct >= COMPACT_THRESHOLD:
        action = "/compact"

    sha = _git_commit_working_state(task_name) if action else None
    _append_session_log(task_name, pct, action)

    if action == "/clear":
        msg = (
            f"\n[context_manager] context at {pct:.0%} (>= {CLEAR_THRESHOLD:.0%}) — "
            f"recommend `/clear`. Working state committed: {sha or 'clean'}.\n"
        )
        print(msg)
    elif action == "/compact":
        msg = (
            f"\n[context_manager] context at {pct:.0%} (>= {COMPACT_THRESHOLD:.0%}) — "
            f"recommend `/compact`. Working state committed: {sha or 'clean'}.\n"
        )
        print(msg)


def run_with_context_check(
    task_fn: Callable[..., Any],
    task_name: str,
    *args: Any,
    **kwargs: Any,
) -> Any:
    """Wrap a task function with checkpoints on entry and exit."""
    checkpoint(f"{task_name} (start)")
    try:
        return task_fn(*args, **kwargs)
    finally:
        checkpoint(f"{task_name} (end)")
