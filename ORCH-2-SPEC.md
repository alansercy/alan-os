# ORCH-2 — Parallel Execution

## Goal
Run agents marked `can_run_parallel: true` simultaneously while keeping
sequential agents (those depending on others' outputs) ordered correctly.

## Approach: two-wave execution
ORCH-2 splits each decomposed run into two waves:

1. **Wave 1 — parallel batch.** All agents with `can_run_parallel: true`
   are submitted to a `ThreadPoolExecutor` and run concurrently. Wait
   for *all* of them to finish before moving on.
2. **Wave 2 — sequential batch.** Remaining agents (`can_run_parallel: false`)
   run one at a time, in declaration order. Because wave 1 is fully
   joined before wave 2 starts, sequential agents can read any wave-1
   outputs from disk.

This is a deliberately simple model — no general DAG resolver, no
arbitrary dependency edges. The decomposer's `can_run_parallel` flag
already encodes the dependency: parallel = independent, sequential =
"depends on something earlier."

## Why threads (not asyncio)
Each agent's work is a blocking subprocess (`claude --print`) or HTTP
call (Anthropic SDK). Both are I/O-bound, so the GIL is not a
bottleneck — Python releases it during `subprocess.run` and during
network I/O. `ThreadPoolExecutor` gives us the parallelism we need
without rewriting `run_claude` to be async.

## What is reused vs. new
- **Reused via import** from `orchestrator.py`: `bootstrap`,
  `read_directive`, `decompose`, `generate_agent_spec`, `run_agent`,
  `collect_results`, `log`, `show_status`, and the path constants.
  No changes to `orchestrator.py`.
- **New in `orchestrator_v2.py`**: `execute_waves(agents, max_workers)`,
  the two-wave runner, plus a thin `main()` that wires up CLI flags
  including `--max-workers` (default 4).

## CLI
```
python orchestrator_v2.py                       # reads DIRECTIVE.md
python orchestrator_v2.py --directive "..."     # inline directive
python orchestrator_v2.py --max-workers 8       # thread pool size
python orchestrator_v2.py --dry-run             # decompose only
python orchestrator_v2.py --status              # last results
```

## Concurrency notes
- `log()` writes to `orch.log` in append mode. Concurrent appends from
  multiple threads may produce out-of-order timestamps, but the OS
  guarantees no torn writes for line-sized buffers, so each entry stays
  intact.
- Per-agent output files are unique (`agents/results/<agent_id>_result.md`),
  so wave-1 threads never write the same file.
- A wave-1 agent that raises an exception is recorded as `FAILED` and
  does not abort the rest of the wave; `collect_results` reports it.
- `print()` calls inside `execute_waves` are guarded by `_print_lock`
  to keep wave-1 progress lines from interleaving.

## Out of scope (deferred)
- Arbitrary DAG dependencies (only the two-wave split for now).
- Per-agent timeouts beyond the 120s already in `run_claude`.
- Retries on transient failures.
