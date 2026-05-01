"""
ORCH-1 — Alan OS Orchestration Engine
======================================
Drop a directive in DIRECTIVE.md, run: python orchestrator.py
Claude Code reads it, decomposes it, spawns sub-agents, collects results.

Usage:
    python orchestrator.py                  # reads DIRECTIVE.md
    python orchestrator.py --directive "your directive here"
    python orchestrator.py --status         # show last run results
"""

import os
import json
import subprocess
import argparse
import datetime
import sys
from pathlib import Path

# ── Paths (all relative to alan-os root) ──────────────────────────────────────
ROOT        = Path(__file__).parent
DIRECTIVE   = ROOT / "DIRECTIVE.md"
CONTEXT     = ROOT / "CONTEXT.json"
SHARED_RULES= ROOT / "SHARED_RULES.md"
AGENTS_DIR  = ROOT / "agents"
RESULTS     = ROOT / "RESULTS.md"
LOG         = ROOT / "orch.log"

# Model selection routes through utils.model_router (single source of truth
# for task → model + pricing + usage logging). Decompose is plan-tier.
from utils.model_router import get_model

# ── Bootstrap: create dirs and starter files if missing ──────────────────────
def bootstrap():
    AGENTS_DIR.mkdir(exist_ok=True)

    if not DIRECTIVE.exists():
        DIRECTIVE.write_text(
            "# DIRECTIVE\n\n"
            "Write your directive here in one clear sentence.\n"
            "Example: Wire the 3 pending Google creds in n8n and confirm each workflow is green.\n"
        )
        print(f"[orch] Created {DIRECTIVE} — edit it and rerun.")
        sys.exit(0)

    if not CONTEXT.exists():
        default_context = {
            "version": "1.0",
            "updated": str(datetime.date.today()),
            "system": {
                "host": "localhost",
                "n8n_url": "https://n8n.lorettasercy.com",
                "dashboard_url": "http://localhost:8000/dashboard",
                "repos": ["alan-os", "loretta-os", "lux-os"],
                "vm": "SecureAI-W11"
            },
            "workflows": {
                "live": ["2.1", "2.2", "3.1", "3.2"],
                "needs_reauth": ["google_cred_1", "google_cred_2", "google_cred_3"],
                "queued": ["2.3", "2.4"]
            },
            "projects": "See PROJECTS.md",
            "active_clients": ["MMM Trucking", "Veritas Digital Presence x2"],
            "notes": "Edit this file to reflect current system state before running directives."
        }
        CONTEXT.write_text(json.dumps(default_context, indent=2))
        print(f"[orch] Created {CONTEXT} — review and update system state.")

    if not SHARED_RULES.exists():
        SHARED_RULES.write_text(
            "# SHARED_RULES — Agent Operating Agreement\n\n"
            "Every sub-agent spawned by ORCH-1 must follow these rules:\n\n"
            "## What agents MAY do\n"
            "- Read any file in this repo\n"
            "- Write output to their designated output file\n"
            "- Make API calls to services listed in CONTEXT.json\n"
            "- Commit changes with a descriptive message\n"
            "- Report errors clearly in their output file\n\n"
            "## What agents MAY NOT do\n"
            "- Delete files\n"
            "- Modify CONTEXT.json, SHARED_RULES.md, or orchestrator.py\n"
            "- Send emails or messages without explicit directive permission\n"
            "- Spawn additional sub-agents\n"
            "- Take irreversible production actions without flagging for human review\n\n"
            "## Output contract\n"
            "Each agent writes a single output file: agents/results/agent_X_result.md\n"
            "Format: STATUS: [DONE|FAILED|NEEDS_REVIEW], then findings.\n"
        )
        print(f"[orch] Created {SHARED_RULES}")


# ── Read directive ────────────────────────────────────────────────────────────
def read_directive(override=None):
    if override:
        return override.strip()
    text = DIRECTIVE.read_text().strip()
    lines = [l for l in text.splitlines() if l.strip() and not l.startswith("#")]
    if not lines:
        print("[orch] DIRECTIVE.md is empty. Add your directive and rerun.")
        sys.exit(1)
    return " ".join(lines).strip()


# ── Decompose directive into agent specs via Claude Code ─────────────────────
def decompose(directive: str) -> list[dict]:
    """
    Asks Claude Code to break the directive into discrete agent tasks.
    Returns a list of agent spec dicts: {id, job, context_keys, output_file}
    """
    context = json.loads(CONTEXT.read_text())
    rules   = SHARED_RULES.read_text()

    decompose_prompt = f"""You are the ORCH-1 decomposition engine for Alan OS.

DIRECTIVE: {directive}

SYSTEM CONTEXT:
{json.dumps(context, indent=2)}

SHARED RULES:
{rules}

Your job: Break this directive into the minimum number of discrete, parallelizable agent tasks needed to complete it.

Return ONLY a JSON array. No preamble, no explanation. Each element:
{{
  "id": "agent_a",
  "job": "One sentence — exactly what this agent does",
  "inputs": ["list of files or data this agent needs"],
  "output_file": "agents/results/agent_a_result.md",
  "can_run_parallel": true
}}

Rules:
- Minimum agents needed. Don't over-decompose.
- Each agent does exactly one thing.
- If a task depends on another agent's output, set can_run_parallel: false and note the dependency in the job description.
- Max 5 agents per directive. If the directive needs more, flag it as too broad.
"""

    result = run_claude(decompose_prompt)
    
    # Strip markdown code fences if present
    result = result.strip()
    if result.startswith("```"):
        result = "\n".join(result.split("\n")[1:])
    if result.endswith("```"):
        result = "\n".join(result.split("\n")[:-1])

    try:
        agents = json.loads(result.strip())
        return agents
    except json.JSONDecodeError as e:
        log(f"Decomposition parse error: {e}\nRaw output: {result}")
        print(f"[orch] Failed to parse agent specs. Check {LOG}")
        sys.exit(1)


# ── Generate agent spec file ──────────────────────────────────────────────────
def generate_agent_spec(agent: dict, directive: str) -> Path:
    context = CONTEXT.read_text()
    rules   = SHARED_RULES.read_text()
    spec_path = AGENTS_DIR / f"{agent['id']}.md"

    spec = f"""# Agent Spec — {agent['id']}
Generated: {datetime.datetime.now().isoformat()}
Parent directive: {directive}

## Your job
{agent['job']}

## Inputs available
{chr(10).join(f'- {i}' for i in agent.get('inputs', []))}

## Output contract
Write your result to: {agent['output_file']}
First line must be: STATUS: [DONE|FAILED|NEEDS_REVIEW]
Then: brief summary of what you did and what you found.

## System context
{context}

## Rules you must follow
{rules}

## Important
Do your job. Write your output. Do not do anything outside your job description.
"""
    spec_path.write_text(spec)
    return spec_path


# ── Run a single agent ────────────────────────────────────────────────────────
def run_agent(agent: dict, spec_path: Path) -> dict:
    output_path = ROOT / agent['output_file']
    output_path.parent.mkdir(parents=True, exist_ok=True)

    log(f"Spawning {agent['id']}: {agent['job']}")
    print(f"  → {agent['id']}: {agent['job']}")

    result = run_claude(spec_path.read_text())

    output_path.write_text(result, encoding='utf-8')
    log(f"{agent['id']} complete. Output: {output_path}")

    # Parse status
    first_line = result.strip().splitlines()[0] if result.strip() else ""
    status = "UNKNOWN"
    if "STATUS:" in first_line:
        status = first_line.split("STATUS:")[-1].strip()

    return {
        "id": agent['id'],
        "job": agent['job'],
        "status": status,
        "output_file": str(output_path),
        "result_preview": result[:300]
    }


# ── Run Claude Code non-interactively ─────────────────────────────────────────
def run_claude(prompt: str) -> str:
    """
    Calls Claude Code via CLI in non-interactive (--print) mode.
    Falls back to Anthropic API if claude CLI not available.
    """
    # Try claude CLI first (Claude Code)
    try:
        proc = subprocess.run(
            ["claude", "--print", prompt],
            capture_output=True, text=True, timeout=120
        )
        if proc.returncode == 0 and proc.stdout.strip():
            return proc.stdout.strip()
        else:
            log(f"claude CLI error: {proc.stderr}")
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        log(f"claude CLI not available: {e}. Falling back to API.")

    # Fallback: Anthropic API direct call
    try:
        import anthropic
        client = anthropic.Anthropic()
        msg = client.messages.create(
            model=get_model("architecture"),
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}]
        )
        return msg.content[0].text
    except Exception as e:
        log(f"API fallback failed: {e}")
        print(f"[orch] Both claude CLI and API failed. Check {LOG}")
        sys.exit(1)


# ── Collect results and write RESULTS.md ─────────────────────────────────────
def collect_results(directive: str, agent_results: list[dict]):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    
    done    = [r for r in agent_results if "DONE" in r['status']]
    failed  = [r for r in agent_results if "FAILED" in r['status']]
    review  = [r for r in agent_results if "NEEDS_REVIEW" in r['status']]
    unknown = [r for r in agent_results if r['status'] == "UNKNOWN"]

    lines = [
        f"# ORCH-1 Results — {now}",
        f"\n## Directive\n{directive}",
        f"\n## Summary\n- Total agents: {len(agent_results)}",
        f"- Done: {len(done)}  |  Failed: {len(failed)}  |  Needs review: {len(review)}  |  Unknown: {len(unknown)}",
        "\n## Agent Results"
    ]

    for r in agent_results:
        lines.append(f"\n### {r['id']} — {r['status']}")
        lines.append(f"**Job:** {r['job']}")
        lines.append(f"**Output:** `{r['output_file']}`")
        lines.append(f"**Preview:**\n```\n{r['result_preview']}\n```")

    if failed or review:
        lines.append("\n## Action needed")
        for r in failed + review:
            lines.append(f"- [ ] {r['id']}: {r['job']} — check `{r['output_file']}`")

    RESULTS.write_text("\n".join(lines))
    print(f"\n[orch] Results written to {RESULTS}")
    return len(failed) + len(review)


# ── Logging ───────────────────────────────────────────────────────────────────
def log(msg: str):
    timestamp = datetime.datetime.now().isoformat()
    with open(LOG, "a") as f:
        f.write(f"[{timestamp}] {msg}\n")


# ── Status: show last results ─────────────────────────────────────────────────
def show_status():
    if RESULTS.exists():
        print(RESULTS.read_text())
    else:
        print("[orch] No results yet. Run a directive first.")


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="ORCH-1 — Alan OS Orchestration Engine")
    parser.add_argument("--directive", type=str, help="Override DIRECTIVE.md with inline directive")
    parser.add_argument("--status",    action="store_true", help="Show last run results")
    parser.add_argument("--dry-run",   action="store_true", help="Decompose only, don't execute agents")
    args = parser.parse_args()

    bootstrap()

    if args.status:
        show_status()
        return

    directive = read_directive(args.directive)
    print(f"\n[orch] Directive: {directive}")
    print(f"[orch] Decomposing into agent tasks...\n")
    log(f"New run — directive: {directive}")

    agents = decompose(directive)
    print(f"[orch] {len(agents)} agent(s) identified:\n")
    for a in agents:
        parallel = "parallel" if a.get("can_run_parallel") else "sequential"
        print(f"  {a['id']} [{parallel}]: {a['job']}")

    if args.dry_run:
        print("\n[orch] Dry run — stopping before execution.")
        return

    print(f"\n[orch] Generating agent specs and executing...\n")

    # Generate spec files
    for agent in agents:
        generate_agent_spec(agent, directive)

    # Execute agents (sequential for now; parallel support coming in ORCH-2)
    agent_results = []
    for agent in agents:
        spec_path = AGENTS_DIR / f"{agent['id']}.md"
        result = run_agent(agent, spec_path)
        agent_results.append(result)

    # Collect and report
    needs_attention = collect_results(directive, agent_results)

    print(f"\n[orch] Run complete.")
    if needs_attention:
        print(f"[orch] {needs_attention} item(s) need your attention — check RESULTS.md")
    else:
        print(f"[orch] All agents completed successfully.")


if __name__ == "__main__":
    main()
