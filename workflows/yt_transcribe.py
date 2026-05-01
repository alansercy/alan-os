"""
yt_transcribe.py — VIE YouTube Intelligence Engine

Pulls auto-generated YouTube captions via yt-dlp, evaluates the transcript
against the Veritas Stack Design Principles via Claude, and posts the
enriched record to the existing /ai_stack endpoint on alan_os_server.py.

Single canonical store (/ai_stack), no parallel JSONL log. The principles
rubric — not the email context — is what differentiates this from
nlm_feed_builder.py's per-URL enrichment.

Spec: C:\\Veritas\\repos\\memory-bank\\VIE_YOUTUBE_INTELLIGENCE_ENGINE.md
Principles: C:\\Veritas\\repos\\alan-os\\memory-bank\\PRINCIPLES_REVIEW_v1.md §7

Usage:
    python yt_transcribe.py <url>                       # single URL
    python yt_transcribe.py --batch urls.txt            # one URL per line, parallel
    python yt_transcribe.py --dry-run <url>             # transcript+eval only, no POST
    python yt_transcribe.py --context alan_os <url>     # default alan_os
    python yt_transcribe.py --max-workers 4 --batch ... # default 4
"""

import argparse
import io
import json
import os
import re
import subprocess
import sys
import tempfile

# Force UTF-8 stdout on Windows cp1252 consoles so we can print structured output
# without character-set crashes. Idempotent if already UTF-8.
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse, parse_qs

import anthropic
import httpx


# Load ~/.lux/.env so ANTHROPIC_API_KEY + ALAN_OS_ADMIN_TOKEN are visible.
ENV_PATH = Path.home() / ".lux" / ".env"
if ENV_PATH.exists():
    with open(ENV_PATH, encoding="utf-8-sig") as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith("#") and "=" in _line:
                _k, _v = _line.split("=", 1)
                os.environ.setdefault(_k.strip(), _v.strip())

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
AI_STACK_API_URL  = os.environ.get("AI_STACK_API_URL", "http://127.0.0.1:8000/ai_stack")
ADMIN_TOKEN       = os.environ.get("ALAN_OS_ADMIN_TOKEN", "")  # /ai_stack itself isn't admin-gated

CLAUDE_MODEL = "claude-sonnet-4-6"
CLAUDE_MAX_TOKENS = 1500


# ─────────────────────────────────────────────────────────────────────────────
# PRINCIPLES RUBRIC — system prompt (cached). v2 three-lens evaluation per
# memory-bank/VIE_PROMPT_PATCH.md (2026-05-01). Replaces the v1 single-lens
# tool-fit rubric — the v1 over-rejected because it ignored extractable
# patterns (gotchas section, folder-as-skill convention, pre-warm cache
# technique all came from Shorts the v1 rubric would have rejected).
# ─────────────────────────────────────────────────────────────────────────────

PRINCIPLES_RUBRIC = """You are the AI stack architect and pattern extractor for Veritas AI Partners.

Your job is NOT just to evaluate whether a tool belongs in the stack.
Your PRIMARY job is to extract actionable patterns, techniques, and insights
from ANY content — even if the specific tool mentioned doesn't fit.

Real examples of high-value extractions from YouTube Shorts:
- "Add a gotchas section to CLAUDE.md" — no tool, pure pattern, immediately implemented
- "Folder-as-skill structure for Claude Code" — convention, immediately implemented
- "Pre-warm cache before parallel batch runs" — operational technique, immediately applied
- GSD repo — existing work worth installing, 65 skills, now in production
- Memory system architecture patterns — informed how we structure session/working/long-term memory
- GitHub repo patterns — informed repo structure and CLAUDE.md design

EVALUATE USING THREE LENSES IN ORDER:

=== LENS 1: PATTERN & TECHNIQUE EXTRACTION (PRIMARY) ===
Even a 60-second short can contain a workflow pattern, prompt structure,
architectural approach, naming convention, or operational technique worth implementing.
Ask: "What behavior or approach can we extract and adapt — regardless of tool fit?"

Look for:
- Prompt patterns or structures (how they write system prompts, CLAUDE.md conventions)
- Workflow patterns (how they sequence agent tasks, handle errors, manage context)
- Architectural patterns (memory design, orchestration approaches, data flow)
- Operational techniques (token optimization approaches, caching strategies, batching)
- Naming conventions or file organization patterns
- Any "aha" insight that changes how we think about a problem

=== LENS 2: TOOL & INTEGRATION FIT (SECONDARY) ===
Evaluate named tools against Veritas Stack Design Principles:
1. API-First, No Lock-In — clean API, no GUI-only tools
2. Defined Contract, Independently Replaceable — swappable without rebuilding adjacent layers
3. Token Efficiency — measurable reduction, not just claims
4. No Human in the Loop by Default — agents can run it at 2am
5. Shared Core, Vertical Config — works across OS products with config not rewrites
6. Local Where Sensitive, Cloud Where Scalable — right data boundary
7. Build Only What Doesn't Exist — check before building custom
8. Four Memory Layers, No Fifth — ephemeral/working/structured/long-term only
9. Revenue or Capability — name which before building

Current stack: Claude API (Sonnet), n8n, FastAPI (alan_os_server.py:8000),
React dashboard (:8081), Google Drive, GitHub, Cloudflare Tunnel,
yt-dlp, Outlook COM, orchestrator.py + orchestrator_v2.py (ThreadPoolExecutor),
CLAUDE.md + session-log.md + .lux/Data/*.json memory architecture.

=== LENS 3: STRATEGIC SIGNAL (TERTIARY) ===
Does this inform Veritas positioning, product decisions, or market awareness?
Examples: what operators are asking for, competitor moves, pricing signals,
emerging patterns in the market that affect AgentOS/TradeOS/PersonalOS strategy.

=== OUTPUT SCHEMA ===
Return ONLY this JSON object. No preamble. No markdown fences.

{
  "summary": "150 word max — what the video actually says, not what the title implies",
  "tools_mentioned": ["tool1", "tool2"],
  "techniques_mentioned": ["technique1", "technique2"],

  "pattern_extraction": {
    "has_extractable_value": true/false,
    "patterns": [
      {
        "description": "specific extractable pattern or technique in one sentence",
        "apply_to": "where in stack/workflow/CLAUDE.md/session protocol it applies",
        "effort": "low/medium/high",
        "priority": "immediate/next-session/backlog"
      }
    ]
  },

  "stack_evaluation": {
    "recommendation": "ADOPT|EVALUATE|MONITOR|REJECT",
    "stack_layer": "orchestration|intelligence|memory|interface|communication|data|pattern|signal|none",
    "replaces_or_complements": "what it replaces or complements, or 'pattern only — no tool' if Lens 1 only",
    "confidence": "HIGH|MEDIUM|LOW",
    "reasoning": "2-3 sentences — cite which lens drove the verdict",
    "action_items": ["specific next step — only if ADOPT or EVALUATE"]
  },

  "strategic_signal": {
    "has_signal": true/false,
    "signal": "one sentence on what this means for Veritas strategy, product, or positioning — omit if false"
  }
}

REVISED VERDICT DEFINITIONS:
- ADOPT — Clear tool fit OR high-value extractable pattern ready to implement now
- EVALUATE — Promising pattern or tool needing one test session to confirm
- MONITOR — Strategic signal worth tracking, no immediate action
- REJECT — No extractable value across ALL THREE lenses — genuinely nothing here

CRITICAL RULES:
- REJECT only if ALL THREE lenses produce zero value
- A video with a good pattern but a bad tool → ADOPT or EVALUATE on pattern alone
- Cite which lens drove the recommendation in reasoning field
- summary must reflect actual transcript content, not title inference
- If transcript was unavailable and you're working from title only, say so explicitly in summary"""


# ─────────────────────────────────────────────────────────────────────────────
# Transcript extraction via yt-dlp
# ─────────────────────────────────────────────────────────────────────────────

def get_video_metadata(url: str) -> dict:
    """yt-dlp --dump-json for title, duration, channel, description, video_id."""
    proc = subprocess.run(
        ["yt-dlp", "--dump-json", "--no-playlist", url],
        capture_output=True, text=True, timeout=60, encoding="utf-8", errors="replace",
    )
    if proc.returncode != 0:
        raise RuntimeError(f"yt-dlp metadata failed: {proc.stderr.strip()[:300]}")
    info = json.loads(proc.stdout)
    return {
        "video_id":    info.get("id", ""),
        "title":       info.get("title", "Unknown"),
        "channel":     info.get("channel") or info.get("uploader", ""),
        "duration":    int(info.get("duration") or 0),
        "description": info.get("description", "") or "",
        "upload_date": info.get("upload_date", ""),  # YYYYMMDD
    }


def get_transcript(url: str) -> str:
    """
    Pull auto-generated en captions via yt-dlp, return cleaned transcript text.
    Empty string if no captions available — caller decides fallback.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        proc = subprocess.run(
            [
                "yt-dlp",
                "--write-auto-subs",
                "--sub-langs", "en",
                "--sub-format", "vtt",
                "--skip-download",
                "--no-playlist",
                "--output", f"{tmpdir}/%(id)s.%(ext)s",
                url,
            ],
            capture_output=True, text=True, timeout=90, encoding="utf-8", errors="replace",
        )
        # yt-dlp may exit 0 even when no auto-subs are available. Look for the file.
        vtt_files = list(Path(tmpdir).glob("*.vtt"))
        if not vtt_files:
            return ""
        raw = vtt_files[0].read_text(encoding="utf-8", errors="replace")
        return clean_vtt(raw)


def clean_vtt(vtt_text: str) -> str:
    """Strip WEBVTT headers, timestamps, HTML tags, dedup repeated lines."""
    lines = vtt_text.splitlines()
    out, seen = [], set()
    skip_prefixes = ("WEBVTT", "Kind:", "Language:", "NOTE", "STYLE")
    for line in lines:
        s = line.strip()
        if not s:
            continue
        if s.startswith(skip_prefixes):
            continue
        # Timestamp lines like "00:00:01.000 --> 00:00:03.500" or "00:00:01.000"
        if re.match(r"^\d{1,2}:\d{2}", s):
            continue
        # Cue-id lines (just digits)
        if re.match(r"^\d+$", s):
            continue
        # Strip HTML tags + caption-position markers like <c> <00:00:01.000>
        s = re.sub(r"<[^>]+>", "", s).strip()
        if not s:
            continue
        # Auto-captions repeat lines across rolling segments — dedup
        if s in seen:
            continue
        seen.add(s)
        out.append(s)
    return " ".join(out)


# ─────────────────────────────────────────────────────────────────────────────
# Claude evaluation (cached system prompt)
# ─────────────────────────────────────────────────────────────────────────────

# v2 back-compat: confidence -> relevance_score mapping (HIGH=8, MEDIUM=5, LOW=3)
_CONFIDENCE_TO_SCORE = {"HIGH": 8, "MEDIUM": 5, "LOW": 3}

# v2 stack_layer -> v1 fit_pipeline mapping. v2 layers:
#   orchestration|intelligence|memory|interface|communication|data|pattern|signal|none
# v1 pipelines: ai_stack|veritas|agentos|personalos|loretta|mmm|none
# All non-"none" v2 layers map to "ai_stack" — the alan_os context evaluates AI
# stack content. Vertical pipelines (loretta/mmm/etc.) would need a vertical
# domain context to derive correctly; not yet plumbed.
_LAYER_TO_PIPELINE = {
    "orchestration": "ai_stack",
    "intelligence":  "ai_stack",
    "memory":        "ai_stack",
    "interface":     "ai_stack",
    "communication": "ai_stack",
    "data":          "ai_stack",
    "pattern":       "ai_stack",
    "signal":        "ai_stack",
    "none":          "none",
}


def _derive_v1_fields(eval_result: dict) -> None:
    """
    Mutate eval_result in place to add v1-compat top-level fields
    (relevance_score, fit_pipeline, fit_rationale) derived from the v2
    stack_evaluation block. No-op if a v1 field is already present, so this is
    forward-safe if a future schema brings them back.

    Placed in the evaluate() pipeline so process_url() and post_to_ai_stack()
    both read the same enriched dict — single derivation point, no duplication.
    """
    se = eval_result.get("stack_evaluation", {}) or {}
    if "relevance_score" not in eval_result:
        confidence = (se.get("confidence") or "").upper()
        rec        = (se.get("recommendation") or "").upper()
        # REJECT = not relevant — force to 1 regardless of confidence so the
        # digest's relevance_score-desc sort doesn't surface rejections at top.
        eval_result["relevance_score"] = 1 if rec == "REJECT" else _CONFIDENCE_TO_SCORE.get(confidence, 0)
    if "fit_pipeline" not in eval_result:
        layer = (se.get("stack_layer") or "none").lower()
        eval_result["fit_pipeline"] = _LAYER_TO_PIPELINE.get(layer, "none")
    if "fit_rationale" not in eval_result:
        eval_result["fit_rationale"] = se.get("reasoning", "") or ""


def evaluate(client: anthropic.Anthropic, title: str, channel: str, transcript: str, fallback_note: str = "") -> dict:
    """Send transcript+metadata to Claude. System prompt is cached (ephemeral)."""
    user_content = f"Video title: {title}\nChannel: {channel}\n"
    if fallback_note:
        user_content += f"Note: {fallback_note}\n"
    user_content += f"\nTranscript:\n{transcript or '[transcript unavailable]'}"

    msg = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=CLAUDE_MAX_TOKENS,
        system=[{
            "type": "text",
            "text": PRINCIPLES_RUBRIC,
            "cache_control": {"type": "ephemeral"},
        }],
        messages=[{"role": "user", "content": user_content}],
    )
    raw = msg.content[0].text.strip()
    # Strip markdown fences if Claude added them despite instructions
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    parsed = json.loads(raw)

    # v2 back-compat: derive missing v1 top-level fields from v2 stack_evaluation
    _derive_v1_fields(parsed)

    # Token accounting for visibility
    parsed["_usage"] = {
        "input_tokens":              getattr(msg.usage, "input_tokens", 0),
        "output_tokens":             getattr(msg.usage, "output_tokens", 0),
        "cache_creation_input_tokens": getattr(msg.usage, "cache_creation_input_tokens", 0),
        "cache_read_input_tokens":     getattr(msg.usage, "cache_read_input_tokens", 0),
    }
    return parsed


# ─────────────────────────────────────────────────────────────────────────────
# /ai_stack POST
# ─────────────────────────────────────────────────────────────────────────────

VALID_PIPELINES  = {"ai_stack", "veritas", "agentos", "personalos", "loretta", "mmm", "none"}
VALID_CATEGORIES = {"YouTube", "Anthropic", "OpenAI", "GitHub", "n8n / Automation",
                    "AI Research", "HBR / Strategy", "Newsletter", "LinkedIn",
                    "Real Estate", "Other"}


def post_to_ai_stack(url: str, meta: dict, eval_result: dict) -> tuple[bool, bool, str]:
    """
    POST enriched record to /ai_stack. Returns (ok, deduped, message).
    Includes the new stack_evaluation block (server schema extension).
    """
    pipeline = eval_result.get("fit_pipeline", "none")
    if pipeline not in VALID_PIPELINES:
        pipeline = "none"
    score = max(0, min(10, int(eval_result.get("relevance_score", 0))))

    payload = {
        "url":             url,
        "url_category":    "YouTube",
        "title":           meta.get("title", "")[:200],
        "summary":         (eval_result.get("summary", "") or "")[:600],
        "relevance_score": score,
        "fit_pipeline":    pipeline,
        "fit_rationale":   (eval_result.get("fit_rationale", "") or "")[:300],
        "tags":            list(eval_result.get("tools_mentioned", []) or [])[:10],
        "source": {
            "type":       "youtube",
            "email_hash": meta.get("video_id", ""),
            "folder":     "yt_transcribe",
            "subject":    meta.get("title", "")[:200],
            "sender":     meta.get("channel", ""),
            "date":       meta.get("upload_date", ""),
        },
        "stack_evaluation":  eval_result.get("stack_evaluation", {}),
        # v2 three-lens fields. Server-side StackItem accepts these as optional
        # dicts after the lux-os 2026-05-01 schema extension. Pre-extension
        # servers silently drop them (pydantic default extra='ignore').
        "pattern_extraction": eval_result.get("pattern_extraction") or None,
        "strategic_signal":   eval_result.get("strategic_signal") or None,
    }
    try:
        resp = httpx.post(AI_STACK_API_URL, json=payload, timeout=15.0)
    except Exception as e:
        return False, False, f"POST failed: {e}"
    if resp.status_code != 200:
        return False, False, f"HTTP {resp.status_code}: {resp.text[:200]}"
    try:
        data = resp.json()
    except Exception:
        data = {}
    return True, bool(data.get("dedup", False)), "ok"


# ─────────────────────────────────────────────────────────────────────────────
# Per-URL pipeline
# ─────────────────────────────────────────────────────────────────────────────

def process_url(url: str, client: anthropic.Anthropic, dry_run: bool) -> dict:
    """Full pipeline for one URL. Returns a result dict for the report."""
    started = datetime.now()
    result = {"url": url, "status": "ok", "started": started.isoformat()}
    try:
        meta = get_video_metadata(url)
        result["title"]    = meta["title"]
        result["channel"]  = meta["channel"]
        result["duration"] = meta["duration"]
        result["video_id"] = meta["video_id"]

        transcript = get_transcript(url)
        fallback_note = ""
        if not transcript:
            fallback_note = "No auto-captions available; using description as fallback."
            transcript = meta["description"][:3000]
        result["transcript_chars"]   = len(transcript)
        result["used_caption_fallback"] = bool(fallback_note)

        eval_result = evaluate(client, meta["title"], meta["channel"], transcript, fallback_note)
        result["recommendation"] = eval_result.get("stack_evaluation", {}).get("recommendation", "?")
        result["confidence"]     = eval_result.get("stack_evaluation", {}).get("confidence", "?")
        result["fit_pipeline"]   = eval_result.get("fit_pipeline", "none")
        result["score"]          = eval_result.get("relevance_score", 0)
        result["usage"]          = eval_result.get("_usage", {})
        result["eval"]           = {k: v for k, v in eval_result.items() if k != "_usage"}

        if dry_run:
            result["posted"] = "skipped (dry-run)"
        else:
            ok, deduped, msg = post_to_ai_stack(url, meta, eval_result)
            result["posted"] = "deduped" if (ok and deduped) else ("ok" if ok else f"failed: {msg}")
    except Exception as e:
        result["status"] = "error"
        result["error"]  = str(e)[:500]
    result["finished"] = datetime.now().isoformat()
    return result


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

def load_batch(path: str) -> list[str]:
    """One URL per line. Lines starting with # are comments. Blank lines skipped."""
    urls = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        urls.append(s)
    return urls


def print_result(r: dict):
    """One-line summary printed as each URL completes. ASCII-only for cp1252 consoles."""
    if r["status"] == "error":
        print(f"  [ERR] {r['url']}: {r['error']}", flush=True)
        return
    title = (r.get("title", "") or "")[:50]
    fb    = " (FALLBACK)" if r.get("used_caption_fallback") else ""
    print(
        f"  [OK] {r['recommendation']:<8} {r['confidence']:<6} score={r['score']:>2}  "
        f"pipeline={r['fit_pipeline']:<10}  [{r['posted']:<10}]  {title}{fb}",
        flush=True,
    )


def main():
    p = argparse.ArgumentParser(description="VIE YouTube Intelligence Engine")
    p.add_argument("urls", nargs="*", help="One or more YouTube URLs (or use --batch)")
    p.add_argument("--batch", help="Path to a file with one URL per line")
    p.add_argument("--dry-run", action="store_true", help="Skip POST to /ai_stack")
    p.add_argument("--context", default="alan_os", help="Eval context (currently only alan_os)")
    p.add_argument("--max-workers", type=int, default=4, help="ThreadPool size for batch (default 4)")
    p.add_argument("--out", help="Optional JSON path for full results")
    args = p.parse_args()

    if not ANTHROPIC_API_KEY:
        print("ERROR: ANTHROPIC_API_KEY not set in environment or ~/.lux/.env", file=sys.stderr)
        sys.exit(1)

    urls = list(args.urls)
    if args.batch:
        urls.extend(load_batch(args.batch))
    if not urls:
        print("ERROR: provide at least one URL or --batch <file>", file=sys.stderr)
        sys.exit(1)

    if args.context != "alan_os":
        print(f"ERROR: --context {args.context} not supported (only alan_os in V1)", file=sys.stderr)
        sys.exit(1)

    print(f"[yt_transcribe] {len(urls)} URL(s); dry_run={args.dry_run}; workers={args.max_workers}; sink={AI_STACK_API_URL}")
    print(f"[yt_transcribe] Model: {CLAUDE_MODEL} (system prompt cached)")

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    results: list[dict] = []

    if len(urls) == 1:
        r = process_url(urls[0], client, args.dry_run)
        print_result(r)
        results.append(r)
    else:
        with ThreadPoolExecutor(max_workers=args.max_workers) as pool:
            futures = {pool.submit(process_url, u, client, args.dry_run): u for u in urls}
            for fut in as_completed(futures):
                r = fut.result()
                print_result(r)
                results.append(r)
        # Sort by original URL order for the final report
        order = {u: i for i, u in enumerate(urls)}
        results.sort(key=lambda r: order.get(r["url"], 9999))

    # Summary
    by_rec: dict = {}
    total_in = total_out = total_cw = total_cr = 0
    for r in results:
        rec = r.get("recommendation", r.get("status", "?"))
        by_rec[rec] = by_rec.get(rec, 0) + 1
        u = r.get("usage", {}) or {}
        total_in += u.get("input_tokens", 0)
        total_out += u.get("output_tokens", 0)
        total_cw += u.get("cache_creation_input_tokens", 0)
        total_cr += u.get("cache_read_input_tokens", 0)

    print()
    print("=" * 72)
    print(f"Recommendations: {dict(sorted(by_rec.items()))}")
    print(f"Tokens — input: {total_in}  output: {total_out}  cache_write: {total_cw}  cache_read: {total_cr}")
    print("=" * 72)

    if args.out:
        Path(args.out).write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Full results -> {args.out}")


if __name__ == "__main__":
    main()
