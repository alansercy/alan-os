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
