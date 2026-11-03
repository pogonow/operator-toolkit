#!/usr/bin/env python3
"""Weekly brain sweep over your own Claude Code sessions on this computer.

Claude Code keeps every session as a local file (~/.claude/projects/*/*.jsonl). This script takes the
last N days of those sessions, keeps only the ones that touch marketing, and hands the excerpts to
`claude -p` inside your marketing brain repo. Claude then saves what belongs in the brain as files in
inbox/ on a branch and opens one pull request. Nothing leaves your computer except through Claude Code
itself, and nothing goes into the brain without the usual review.

Usage:
    python3 brain_sweep_local.py --repo ~/code/acme-marketing-brain [--days 7] [--dry-run]

Run it weekly with launchd (Mac) or cron (Linux): see the brain-digest skill, "Local sweep".
Needs: Python 3.9+, Claude Code (`claude`) logged in, git and the GitHub CLI (`gh`) logged in.
Chats in the claude.ai app are not on your computer, so they are not covered here: the Monday
Brain Bot message covers those.
"""
import argparse
import datetime as dt
import json
import os
import pathlib
import re
import subprocess
import sys
import tempfile

KEYWORDS = re.compile(
    r"\b(marketing|customer|positioning|competitor|pricing|campaign|channel|webinar|outbound|inbound|"
    r"linkedin|seo|ads?|newsletter|launch|icp|persona|messaging|brand|demo|lead|pipeline|churn|"
    r"case study|testimonial|brain update)\b",
    re.I,
)
MAX_CHARS_PER_SESSION = 6000
MAX_TOTAL_CHARS = 60000


def text_of(content):
    """Pull plain text out of a Claude Code message content field (string or list of blocks)."""
    if isinstance(content, str):
        return content
    out = []
    if isinstance(content, list):
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                out.append(block.get("text", ""))
    return "\n".join(out)


def read_session(path, since):
    lines = []
    for raw in path.open(encoding="utf-8", errors="ignore"):
        try:
            rec = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if rec.get("type") not in ("user", "assistant"):
            continue
        ts = rec.get("timestamp")
        if ts:
            try:
                when = dt.datetime.fromisoformat(ts.replace("Z", "+00:00"))
                if when < since:
                    continue
            except ValueError:
                pass
        msg = rec.get("message") or {}
        txt = text_of(msg.get("content")).strip()
        if txt:
            who = "Founder/marketer" if rec["type"] == "user" else "Claude"
            lines.append(f"{who}: {txt}")
    return "\n".join(lines)


def collect(days, brain_repo):
    root = pathlib.Path.home() / ".claude" / "projects"
    since = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=days)
    picked, total = [], 0
    if not root.exists():
        return picked
    files = sorted(root.glob("*/*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)
    for f in files:
        if dt.datetime.fromtimestamp(f.stat().st_mtime, dt.timezone.utc) < since:
            continue
        body = read_session(f, since)
        if not body:
            continue
        hits = len(KEYWORDS.findall(body))
        if "🧠 Brain update" not in body and hits < 3:
            continue
        # keep the Brain update blocks whole, then as much of the rest as fits
        blocks = re.findall(r"🧠 Brain update.*?(?:\n\n|$)", body, re.S)
        excerpt = "\n".join(blocks) + "\n---\n" + body
        excerpt = excerpt[:MAX_CHARS_PER_SESSION]
        if total + len(excerpt) > MAX_TOTAL_CHARS:
            break
        total += len(excerpt)
        picked.append((f.parent.name, f.stem, excerpt))
    return picked


PROMPT = """You are the local weekly sweep for this marketing brain repo. Read CLAUDE.md and brain.yml first and follow their rules.
The file {notes} holds excerpts from my Claude Code sessions of the last {days} days on this computer.
Find what belongs in the marketing brain but isn't there yet: every "🧠 Brain update" block, and anything else that clearly is brain material (a new competitor, a customer's words, a test result, why something flopped, a decision, a new belief).
Check the brain first and skip anything it already says. Never invent: every line must point to the session excerpt it came from, with its date.
Save each topic as inbox/YYYY-MM-DD-[short-topic].md in the 🧠 Brain update format from CLAUDE.md, on one branch named sweep-local/YYYY-MM-DD, commit, push and open ONE pull request titled "From my Claude Code sessions, week of YYYY-MM-DD". Never merge it.
If there is nothing new, say so and change nothing."""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", required=True, help="path to your local clone of the marketing brain repo")
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--dry-run", action="store_true", help="show what would be sent, change nothing")
    a = ap.parse_args()
    repo = pathlib.Path(os.path.expanduser(a.repo)).resolve()
    if not (repo / "CLAUDE.md").exists():
        sys.exit(f"{repo} doesn't look like a marketing brain repo (no CLAUDE.md).")
    picked = collect(a.days, repo)
    print(f"{len(picked)} Claude Code sessions from the last {a.days} days look like marketing.")
    if not picked:
        return
    notes = tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8")
    for proj, sid, ex in picked:
        notes.write(f"## Session {sid} (project folder {proj})\n\n{ex}\n\n")
    notes.close()
    if a.dry_run:
        print(f"Dry run: excerpts in {notes.name}, nothing sent.")
        return
    subprocess.run(["git", "-C", str(repo), "pull", "--quiet"], check=False)
    cmd = [
        "claude", "-p", PROMPT.format(notes=notes.name, days=a.days),
        "--allowedTools", "Read,Write,Edit,Glob,Grep,Bash(git:*),Bash(gh:*),Bash(date:*)",
        "--add-dir", os.path.dirname(notes.name),
    ]
    res = subprocess.run(cmd, cwd=repo)
    os.unlink(notes.name)
    sys.exit(res.returncode)


if __name__ == "__main__":
    main()
