"""Centralized model selection, cost estimation, and usage logging.

VIE-impl-A / Pattern 1 (memory-bank/VIE_PATTERN_ACTION_LIST.md). Single source
of truth for which Claude model handles which task type, what it costs, and
what was actually spent. Callers route by task name; model IDs and pricing
live here.

Pricing source: published Anthropic rates current as of 2026-04. Update the
COST_PER_1K_TOKENS table when rates change.
"""
from __future__ import annotations

import json
import os
import threading
from datetime import datetime, timezone
from pathlib import Path

# ── Models ────────────────────────────────────────────────────────────────────
OPUS   = "claude-opus-4-7"
SONNET = "claude-sonnet-4-6"
HAIKU  = "claude-haiku-4-5-20251001"

# Task type → model. Add new task types here, not in callers.
TASK_MODEL_MAP: dict[str, str] = {
    # Haiku — triage / classification / labeling
    "triage":         HAIKU,
    "classification": HAIKU,
    "labeling":       HAIKU,
    # Sonnet — code, file ops, evaluation, summarization (default tier)
    "code_gen":       SONNET,
    "file_ops":       SONNET,
    "stack_eval":     SONNET,
    "summarization":  SONNET,
    # Opus — architecture / strategy / ambiguous evaluation
    "architecture":    OPUS,
    "strategy":        OPUS,
    "ambiguous_eval":  OPUS,
}

_DEFAULT_MODEL = SONNET

# ── Pricing (USD per 1K tokens) ───────────────────────────────────────────────
COST_PER_1K_TOKENS: dict[str, dict[str, float]] = {
    OPUS:   {"input": 0.015, "output": 0.075},
    SONNET: {"input": 0.003, "output": 0.015},
    HAIKU:  {"input": 0.001, "output": 0.005},
}

# ── Usage log location ────────────────────────────────────────────────────────
USAGE_LOG_PATH = Path(os.environ.get(
    "MODEL_USAGE_LOG",
    str(Path.home() / ".lux" / "data" / "model_usage.json"),
))

_log_lock = threading.Lock()


def get_model(task_type: str) -> str:
    """Return the model ID for a task type. Falls back to Sonnet on unknown."""
    return TASK_MODEL_MAP.get(task_type, _DEFAULT_MODEL)


def estimate_cost(task_type: str, input_tokens: int, output_tokens: int) -> dict:
    """Project the USD cost of a call before making it.

    Returns {model, input_tokens, output_tokens, projected_cost_usd}.
    Unknown models silently cost 0 — surface that by checking `model` is in
    COST_PER_1K_TOKENS at the call site if you need a hard guarantee.
    """
    model = get_model(task_type)
    rates = COST_PER_1K_TOKENS.get(model, {"input": 0.0, "output": 0.0})
    cost = (input_tokens / 1000.0) * rates["input"] + \
           (output_tokens / 1000.0) * rates["output"]
    return {
        "model": model,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "projected_cost_usd": round(cost, 6),
    }


def log_usage(
    task_type: str,
    model: str,
    input_tokens: int,
    output_tokens: int,
    actual_cost: float,
) -> None:
    """Append a usage record to the canonical JSON log, keyed by ISO timestamp.

    File shape: {"<ISO-8601 UTC>": {task_type, model, input_tokens,
    output_tokens, actual_cost_usd}, ...}. Threadsafe within a process via
    a module-level lock; cross-process writers race on the file rewrite.
    """
    USAGE_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).isoformat()
    record = {
        "task_type": task_type,
        "model": model,
        "input_tokens": int(input_tokens),
        "output_tokens": int(output_tokens),
        "actual_cost_usd": round(float(actual_cost), 6),
    }
    with _log_lock:
        if USAGE_LOG_PATH.exists():
            try:
                data = json.loads(USAGE_LOG_PATH.read_text(encoding="utf-8"))
                if not isinstance(data, dict):
                    data = {}
            except (json.JSONDecodeError, OSError):
                data = {}
        else:
            data = {}
        # Two calls in the same microsecond would collide — disambiguate.
        key = ts
        n = 1
        while key in data:
            key = f"{ts}#{n}"
            n += 1
        data[key] = record
        USAGE_LOG_PATH.write_text(
            json.dumps(data, indent=2, sort_keys=True),
            encoding="utf-8",
        )
