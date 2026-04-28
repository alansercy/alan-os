"""
ORCH-2 — Parallel Execution Engine
==================================
Extends ORCH-1 with parallel agent execution.

Agents marked ``can_run_parallel: true`` run simultaneously in a
ThreadPoolExecutor. Agents marked ``can_run_parallel: false`` run
sequentially after the parallel batch completes, so they can read
wave-1 outputs from disk.

No changes to ``orchestrator.py`` — v1 functions are imported and reused.

Usage:
    python orchestrator_v2.py                    # reads DIRECTIVE.md
    python orchestrator_v2.py --directive "..."  # inline directive
    python orchestrator_v2.py --max-workers 8    # thread pool size (default 4)
    python orchestrator_v2.py --dry-run          # decompose only
    python orchestrator_v2.py --status           # show last results
"""

import argparse
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

from orchestrator import (
    AGENTS_DIR,
    bootstrap,
    collect_results,
    decompose,
    generate_agent_spec,
    log,
    read_directive,
    run_agent,
    show_status,
)

_print_lock = threading.Lock()


def _safe_print(msg: str):
    with _print_lock:
        print(msg)


def execute_waves(agents: list[dict], max_workers: int) -> list[dict]:
    """
    Two-wave execution:
      Wave 1 — agents with can_run_parallel=True run concurrently.
      Wave 2 — agents with can_run_parallel=False run sequentially,
               after wave 1 has fully joined.

    Returns results in the original agent ordering.
    """
    parallel_agents   = [a for a in agents if a.get("can_run_parallel")]
    sequential_agents = [a for a in agents if not a.get("can_run_parallel")]

    results_by_id: dict[str, dict] = {}

    if parallel_agents:
        _safe_print(f"[orch-2] Wave 1 — {len(parallel_agents)} parallel agent(s)")
        with ThreadPoolExecutor(max_workers=max_workers) as pool:
            futures = {
                pool.submit(run_agent, a, AGENTS_DIR / f"{a['id']}.md"): a
                for a in parallel_agents
            }
            for fut in as_completed(futures):
                agent = futures[fut]
                try:
                    results_by_id[agent['id']] = fut.result()
                    _safe_print(f"  ✓ {agent['id']} complete")
                except Exception as e:
                    log(f"[parallel] {agent['id']} crashed: {e}")
                    _safe_print(f"  ✗ {agent['id']} crashed: {e}")
                    results_by_id[agent['id']] = {
                        "id": agent['id'],
                        "job": agent['job'],
                        "status": "FAILED",
                        "output_file": str(AGENTS_DIR / "results" / f"{agent['id']}_result.md"),
                        "result_preview": f"Thread crashed: {e}",
                    }

    if sequential_agents:
        _safe_print(f"[orch-2] Wave 2 — {len(sequential_agents)} sequential agent(s)")
        for agent in sequential_agents:
            spec_path = AGENTS_DIR / f"{agent['id']}.md"
            results_by_id[agent['id']] = run_agent(agent, spec_path)

    return [results_by_id[a['id']] for a in agents]


def main():
    parser = argparse.ArgumentParser(description="ORCH-2 — Parallel Execution Engine")
    parser.add_argument("--directive",   type=str, help="Inline directive (overrides DIRECTIVE.md)")
    parser.add_argument("--status",      action="store_true", help="Show last run results")
    parser.add_argument("--dry-run",     action="store_true", help="Decompose only, don't execute")
    parser.add_argument("--max-workers", type=int, default=4, help="Max concurrent threads (default 4)")
    args = parser.parse_args()

    bootstrap()

    if args.status:
        show_status()
        return

    directive = read_directive(args.directive)
    print(f"\n[orch-2] Directive: {directive}")
    print(f"[orch-2] Decomposing into agent tasks...\n")
    log(f"ORCH-2 run — directive: {directive}")

    agents = decompose(directive)
    print(f"[orch-2] {len(agents)} agent(s) identified:\n")
    for a in agents:
        mode = "parallel" if a.get("can_run_parallel") else "sequential"
        print(f"  {a['id']} [{mode}]: {a['job']}")

    if args.dry_run:
        print("\n[orch-2] Dry run — stopping before execution.")
        return

    print(f"\n[orch-2] Generating agent specs and executing...\n")
    for agent in agents:
        generate_agent_spec(agent, directive)

    agent_results = execute_waves(agents, args.max_workers)

    needs_attention = collect_results(directive, agent_results)
    print(f"\n[orch-2] Run complete.")
    if needs_attention:
        print(f"[orch-2] {needs_attention} item(s) need your attention — check RESULTS.md")
    else:
        print(f"[orch-2] All agents completed successfully.")


if __name__ == "__main__":
    main()
