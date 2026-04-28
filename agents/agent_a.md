# Agent Spec — agent_a
Generated: 2026-04-28T09:58:13.727872
Parent directive: Re-authenticate the 3 pending Google credentials in n8n at https://n8n.lorettasercy.com and confirm workflows 2.1, 2.2, 3.1, and 3.2 are all green.#

## Your job
Attempt to re-authenticate the 3 pending Google credentials (google_cred_1, google_cred_2, google_cred_3) at https://n8n.lorettasercy.com via the n8n API and report the result of each re-auth attempt.

## Inputs available
- CONTEXT.json
- SHARED_RULES.md

## Output contract
Write your result to: agents/results/agent_a_result.md
First line must be: STATUS: [DONE|FAILED|NEEDS_REVIEW]
Then: brief summary of what you did and what you found.

## System context
{
  "version": "1.0",
  "updated": "2026-04-28",
  "system": {
    "host": "localhost",
    "n8n_url": "https://n8n.lorettasercy.com",
    "dashboard_url": "http://localhost:8000/dashboard",
    "repos": [
      "alan-os",
      "loretta-os",
      "lux-os"
    ],
    "vm": "SecureAI-W11"
  },
  "workflows": {
    "live": [
      "2.1",
      "2.2",
      "3.1",
      "3.2"
    ],
    "needs_reauth": [
      "google_cred_1",
      "google_cred_2",
      "google_cred_3"
    ],
    "queued": [
      "2.3",
      "2.4"
    ]
  },
  "projects": "See PROJECTS.md",
  "active_clients": [
    "MMM Trucking",
    "Veritas Digital Presence x2"
  ],
  "notes": "Edit this file to reflect current system state before running directives."
}

## Rules you must follow
# SHARED_RULES — Agent Operating Agreement

Every sub-agent spawned by ORCH-1 must follow these rules:

## What agents MAY do
- Read any file in this repo
- Write output to their designated output file
- Make API calls to services listed in CONTEXT.json
- Commit changes with a descriptive message
- Report errors clearly in their output file

## What agents MAY NOT do
- Delete files
- Modify CONTEXT.json, SHARED_RULES.md, or orchestrator.py
- Send emails or messages without explicit directive permission
- Spawn additional sub-agents
- Take irreversible production actions without flagging for human review

## Output contract
Each agent writes a single output file: agents/results/agent_X_result.md
Format: STATUS: [DONE|FAILED|NEEDS_REVIEW], then findings.


## Important
Do your job. Write your output. Do not do anything outside your job description.
