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
# PRINCIPLES RUBRIC — system prompt (cached). Sourced from
# PRINCIPLES_REVIEW_v1.md §7 (revised) — NOT the original spec's principles,
# which had vague phrases and unmeasurable thresholds.
# ─────────────────────────────────────────────────────────────────────────────

PRINCIPLES_RUBRIC = """You are the AI stack architect for Veritas AI Partners. Your job is to evaluate \
a single piece of YouTube content (transcript + title + channel) against the \
Veritas Stack Design Principles and return a structured ADOPT / EVALUATE / \
MONITOR / REJECT recommendation.

# Veritas Stack Context

Veritas AI Partners is a fractional CRO/BD practice (CentPenny LLC). The stack:

- Alan OS — personal AI operating system (Python, FastAPI on localhost:8000, Outlook COM, Windows automation, n8n, Claude API)
- AgentOS — commercial AI OS for real estate agents (live for Loretta MoveWithClarity)
- TradeOS — AI BD for trades/logistics SMBs (live for MMM Trucking, $3K/mo)
- PersonalOS — executive + family-steward OS
- SalesAgentOS — outbound BD infrastructure
- VIE — Veritas Intelligence Engine (this engine + nlm_feed_builder.py)
- FinanceOS — backburner

Live infrastructure: Claude API (Sonnet/Haiku), n8n, FastAPI, React dashboard, \
Google Drive, GitHub, yt-dlp, Outlook COM, Cloudflare Tunnel (planned), Buffer, \
Twilio (planned). LLM is Anthropic only — no OpenAI / Gemini / local-LLM.

# Stack Layers (where things live)

- INTERFACE: Lux Command Center (React, localhost:8081), n8n UI
- ORCHESTRATION: n8n workflows, Claude Code, FastAPI (alan_os_server.py)
- INTELLIGENCE: Claude API, VIE pipeline, AI Research Feed (Drive)
- MEMORY: Working (CLAUDE.md, session-log, .env), Structured (.lux/data/*.json, Sheets), Long-term (GitHub, Drive)
- COMMUNICATION: Outlook COM, Gmail API, Cloudflare Tunnel
- DATA: leads.json, competitors.json, vault, Drive assets

# Revised Stack Design Principles (with acceptance tests)

Each principle has a measurable acceptance test. ADOPT requires the tool to \
pass all relevant principles. REJECT means it fails one or more in a way that \
can't be designed around.

**P1 — API-First, Exportable Data.** Every component exposes/consumes a documented API/webhook OR makes its data exportable in a standard format on demand. GUI-only without an export path = reject. Closed-API tools (Buffer, Twilio, Lofty) are accepted at ≥90% feature parity vs. open alternatives.
*Test:* Can I export every byte of state from this tool with a documented call within one hour, with no GUI clicks?

**P2 — Independently Replaceable, with Declared Coupling.** Components declare a `removes_breaks` set. Replacing touches files only in that set.
*Test:* If I delete this file, what tests fail? Are those tests in the declared set?

**P3 — Token Efficiency, Measured.** ADOPT only if a tool reduces tokens-per-completed-task by ≥30% with eval rubric ≥90% baseline. EVALUATE if 10–30%. MONITOR if <10%.
*Test:* Pre-tool baseline tokens vs. post-tool tokens, on a fixed sample of 10 representative tasks per context.

**P4 — Human Gates Are Declared, Not Default.** Every workflow declares `human_gate: required | optional | none`. Required gates name type/SLA/owner. Optional and none are runnable end-to-end from a cold start.
*Test:* If Alan is on a plane for 24 hours, does this workflow run, fail explicitly, or hang silently?

**P5 — Shared Engine + Vertical Config.** One engine, per-vertical config dicts. Forks require an ADR with a 6-month maintenance projection.
*Test:* Adding a new vertical adds N lines to a config dict, not a new file in `engine/`.

**P6 — Local for Sensitive, Cloud for Scalable, Auth for Both.** Tag data classes as `sensitive_local`, `sensitive_controlled`, or `public_cloud`. Each names one canonical store. Endpoints accepting writes/actions require a bearer token.
*Test:* Boot host with public tunnel up. Curl every endpoint without bearer. Every write/action endpoint must return 401.

**P7 — Build-or-Extend Decision in Writing.** Before any new file > 50 lines, write a `BUILD_OR_EXTEND.md` listing every existing component touching the same domain, % overlap, justification or extension plan. ≥40% overlap = extend. ≥60% = no new file.
*Test:* Pre-merge gate. Reviewer rejects if doc missing or overlap math wrong.

**P8 — Named Memory Surfaces, Single Canonical Store per Class.** Named surfaces: Ephemeral, Working, Structured, Long-term, plus named exceptions (Outlook MAPI, NotebookLM, browser localStorage). Each data class names one canonical store.
*Test:* For every JSON/TXT file in ~/.lux/, name (a) data class, (b) canonical-store flag, (c) retention, (d) reconciliation.

**P9 — Three Buckets: Revenue, Capability, Family/Personal.** Every workflow declares REVENUE (named client/product, billable in 90 days) OR CAPABILITY (named operator KPI, ≥10% lift in 30 days) OR FAMILY/PERSONAL (separately budgeted).
*Test:* Quarterly audit. Untaggable = archive.

**P10 — Secret Rotation, Cost, Retention, Observability.** Every secret has rotation interval + last_rotated. Every workflow has monthly $ budget; sustained 2x burn triggers circuit breaker. Every persistent data class has retention. Every run emits a structured record to one sink.
*Test:* Dashboard surfaces overdue secrets, over-budget workflows, retention violations, missing run records.

# Decision Definitions

- **ADOPT** — Fits principles, clear integration path, HIGH confidence. Add this sprint.
- **EVALUATE** — Strong signal, needs testing or more info. Assign a test session.
- **MONITOR** — Interesting but premature, space moving fast, or unclear fit. Re-evaluate in 30 days.
- **REJECT** — Violates principles, redundant with existing component, or not worth complexity cost.

# Output Schema (JSON, no preamble, no markdown fences)

{
  "summary": "<200 words max>",
  "tools_mentioned": ["<tool or repo names>"],
  "techniques_mentioned": ["<patterns or techniques>"],
  "relevance_score": <integer 0-10, where 10 = must-act-now>,
  "fit_pipeline": "<ai_stack|veritas|agentos|personalos|loretta|mmm|none>",
  "fit_rationale": "<one sentence>",
  "stack_evaluation": {
    "recommendation": "<ADOPT|EVALUATE|MONITOR|REJECT>",
    "stack_layer": "<interface|orchestration|intelligence|memory|communication|data|none>",
    "replaces_or_complements": "<what it replaces/complements in the current stack, or 'nothing — new capability'>",
    "confidence": "<HIGH|MEDIUM|LOW>",
    "reasoning": "<2-3 sentences naming which principles drove the verdict>",
    "action_items": ["<concrete next steps if ADOPT or EVALUATE; empty array otherwise>"]
  }
}

Be brutal. If a video is generic AI hype, surface-level news, or a tool that \
duplicates something already in the stack — REJECT it. The cost of a wrong \
ADOPT is integration time; the cost of a wrong REJECT is a 30-day MONITOR \
re-check. Bias toward REJECT or MONITOR for content that doesn't pass P3 (token \
efficiency) AND P7 (overlap with existing components) cleanly."""


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
        "stack_evaluation": eval_result.get("stack_evaluation", {}),
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
