#!/usr/bin/env python3
"""Report Claude Code token usage from the local session transcripts.

Part of the Period Work Protocol (startup package, Feature 8). Claude cannot see the
account's plan limits or run `/usage` itself, but every API call it makes is recorded,
with its token counts, in the transcripts Claude Code writes under
`~/.claude/projects/<repo-slug>/<session-id>.jsonl` (subagents under
`<session-id>/subagents/`). This script sums them, so usage can be *measured* rather than
guessed.

What it reports:
  - this session (the most recently written transcript for this repo, plus its subagents);
  - optionally a window since a given time (`--since`, e.g. the period start);
  - every project on this machine over the last 5 hours and the last 7 days — the shapes of
    the subscription rate-limit windows, as a rough guide only.

It does NOT know the plan's limits. Convert to a percentage by calibrating against a
`/usage` reading the user pastes in (see PERIOD_WORK_PROTOCOL.md, "Token usage").
Usage on other machines, claude.ai, or the API is invisible to it.

Usage:
  python3 token_usage.py                         # summary for the current repo's session
  python3 token_usage.py --since 2026-09-28T14:05
  python3 token_usage.py --session <session-id>  # a specific session
  python3 token_usage.py --repo /path/to/repo    # a different repo
  python3 token_usage.py --json                  # machine-readable
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path


def projects_root():
    base = os.environ.get("CLAUDE_CONFIG_DIR") or str(Path.home() / ".claude")
    return Path(base) / "projects"


def repo_slug(path):
    # Claude Code names each project directory after the working directory, with every
    # non-alphanumeric character replaced by '-'.
    return re.sub(r"[^A-Za-z0-9]", "-", str(Path(path).resolve()))


def default_repo():
    # Claude Code is normally launched at the repo root, so prefer it over the cwd.
    try:
        return subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True,
                              text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return os.getcwd()


def parse_time(value):
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.astimezone()  # naive input = local time
    return dt.astimezone(timezone.utc)


def read_calls(paths, since=None):
    """One record per API call. Transcripts repeat a call's usage once per content
    block, so calls are de-duplicated on (message id, request id)."""
    calls = {}
    for path in paths:
        try:
            lines = path.open(encoding="utf-8", errors="replace")
        except OSError:
            continue
        with lines:
            for line in lines:
                if '"usage"' not in line:
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue
                msg = entry.get("message") or {}
                usage = msg.get("usage")
                if entry.get("type") != "assistant" or not usage:
                    continue
                stamp = entry.get("timestamp")
                when = parse_time(stamp) if stamp else None
                if since and (when is None or when < since):
                    continue
                key = (msg.get("id"), entry.get("requestId"))
                calls[key] = {"when": when, "usage": usage, "model": msg.get("model")}
    return list(calls.values())


def summarise(calls):
    total = {"calls": len(calls), "input": 0, "cache_write": 0, "cache_read": 0, "output": 0}
    for c in calls:
        u = c["usage"]
        total["input"] += u.get("input_tokens", 0) or 0
        total["cache_write"] += u.get("cache_creation_input_tokens", 0) or 0
        total["cache_read"] += u.get("cache_read_input_tokens", 0) or 0
        total["output"] += u.get("output_tokens", 0) or 0
    total["all"] = total["input"] + total["cache_write"] + total["cache_read"] + total["output"]
    # The last call's prompt size approximates how full the context window is now.
    timed = [c for c in calls if c["when"]]
    if timed:
        u = max(timed, key=lambda c: c["when"])["usage"]
        total["context_now"] = sum(u.get(k, 0) or 0 for k in
                                   ("input_tokens", "cache_creation_input_tokens",
                                    "cache_read_input_tokens"))
        total["first"] = min(c["when"] for c in timed).isoformat()
        total["last"] = max(c["when"] for c in timed).isoformat()
    return total


def session_files(project_dir, session_id):
    main = project_dir / f"{session_id}.jsonl"
    subs = sorted((project_dir / session_id).glob("**/*.jsonl"))
    return ([main] if main.exists() else []) + subs


def fmt(n):
    return f"{n / 1e6:.2f}M" if n >= 1e6 else f"{n / 1e3:.1f}k" if n >= 1e3 else str(n)


def line(label, s, show_context=True):
    ctx = f" | context now ~{fmt(s['context_now'])}" if show_context and "context_now" in s else ""
    return (f"{label:<22} {s['calls']:>5} calls | output {fmt(s['output']):>7} | "
            f"fresh input {fmt(s['input'] + s['cache_write']):>7} | "
            f"cache read {fmt(s['cache_read']):>7}{ctx}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--repo", default=default_repo(),
                    help="directory Claude Code was launched in (default: git root, else cwd)")
    ap.add_argument("--session", help="session id (default: most recently written in this repo)")
    ap.add_argument("--since", help="also report usage since this time (ISO, local if no zone)")
    ap.add_argument("--json", action="store_true", help="print JSON instead of a table")
    args = ap.parse_args()

    root = projects_root()
    project_dir = root / repo_slug(args.repo)
    report = {}

    if project_dir.is_dir():
        session = args.session
        if not session:
            latest = max(project_dir.glob("*.jsonl"), key=lambda p: p.stat().st_mtime, default=None)
            session = latest.stem if latest else None
        if session:
            files = session_files(project_dir, session)
            report["session"] = {"id": session, **summarise(read_calls(files))}
            if args.since:
                report["since"] = {"from": args.since,
                                   **summarise(read_calls(files, parse_time(args.since)))}
    else:
        print(f"note: no transcripts for this repo at {project_dir}", file=sys.stderr)

    now = datetime.now(timezone.utc)
    everything = sorted(root.glob("**/*.jsonl")) if root.is_dir() else []
    week = read_calls(everything, now - timedelta(days=7))
    report["all_projects_5h"] = summarise([c for c in week if c["when"] >= now - timedelta(hours=5)])
    report["all_projects_7d"] = summarise(week)

    if args.json:
        print(json.dumps(report, indent=2))
        return
    if "session" in report:
        print(line(f"session {report['session']['id'][:8]}", report["session"]))
    if "since" in report:
        print(line(f"since {args.since}", report["since"]))
    print(line("all projects, 5h", report["all_projects_5h"], False))
    print(line("all projects, 7d", report["all_projects_7d"], False))
    print("(local transcripts only; no plan limits — calibrate against a /usage reading)")


if __name__ == "__main__":
    main()
