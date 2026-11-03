---
name: brain-digest
description: Keeps a founder and their marketing hire up to date on the marketing brain repo after the first two weeks. Writes a daily or weekly digest of what changed, why and based on what (both ways, the founder's changes and the marketer's), merges the minor changes and holds the significant ones for the founder, runs an automatic weekly sweep (a GitHub Action on the founder's Claude subscription, plus an optional local script over Claude Code sessions) that turns caught brain updates and gaps into one pull request, and sets up the Brain Bot that posts the digest and the sweep to Slack. Use when the founder says "set up the brain digest", "brain digest", "what changed in the brain", "set up Brain Bot", "post the digest to Slack" or when a scheduled task says "Run brain-digest for [repo]".
---

Last verified: 2026-11-03 (v0.2.0, weekly sweep)
Companion post: Put Your Marketing Brain on GitHub Before You Hire, https://owneropsguide.substack.com/p/marketing-brain-github-saas-founders
From The Anti-Grind SaaS Manual by Paul Ogonowski.

# Keep the brain fresh

After the first two weeks, nobody should have to ask "what changed?". This skill writes it down every day (or every week): what changed in the brain, who changed it, why and based on what. You see your marketer's changes and they see yours.

It merges only what the gates in `CLAUDE.md` call minor. Everything significant waits for the founder.

Needs the marketing brain repo in `mode: digest` (see **brain-handoff**). If `brain.yml` still says `handoff`, say so and ask whether to switch.

## Pick the mode

- **Setup.** "Set up the brain digest" or "set up Brain Bot". Run once.
- **Run.** "Run brain-digest for [repo]" (usually from the scheduled task) or "what changed in the brain".
- **Weekly sweep.** Runs on its own every Monday once set up (setup steps 7 to 9). By hand: "what's missing from the brain?" or "run the weekly sweep".

## Setup

Walk the founder through it one step at a time and wait for "done" after each. About 15 minutes in total.

1. **Brain Bot in Slack.** Go to api.slack.com/apps, Create New App, From scratch, name it "Brain Bot", pick the workspace (the free Slack plan works). In the app: Incoming Webhooks, switch on, Add New Webhook to Workspace, pick the channel (suggest `#marketing-brain`, with both founder and marketer in it). Copy the webhook URL. It's a secret: never paste it into a chat, a file or the repo.
2. **The secret on GitHub.** In the repo: Settings, Secrets and variables, Actions, New repository secret. Name `SLACK_WEBHOOK_URL`, value the URL from step 1.
3. **The Action.** Add `templates/brain-digest-to-slack.yml` to the repo as `.github/workflows/brain-digest-to-slack.yml` (commit it if you can push, else give the founder the file and the path). From now on every new file in `digests/` gets posted to Slack as Brain Bot. Free private repos include 2,000 Actions minutes a month and a digest takes seconds.
4. **The scheduled task.** Scheduled tasks need a paid Claude plan and live in Claude Code (claude.ai/code/scheduled or Schedule in the desktop app). New task, daily at a time the founder picks (weekly if `brain.yml` says `digest: weekly`), with the brain repo attached and the Claude GitHub app given write access to it. If the task settings offer unrestricted branch pushes for the repo, allow it so the digest can land on main. The prompt, one line: `Run brain-digest for [owner]/[company]-marketing-brain.` One digest task on the founder's account is enough, because the digest covers both people. If the marketer wants their chats checked too, their own task's prompt is `Run brain-digest weekly gaps only for [owner]/[company]-marketing-brain.`: it opens PRs and never writes a digest file.
5. **Test it.** Do one run now. Check the digest file landed in `digests/` and the message showed up in Slack. If Slack stays empty, check the secret name and that the workflow file sits in `.github/workflows/`.
6. Set `slack: true` in `brain.yml`.

**The weekly sweep, so nobody has to remember** (about 10 more minutes):

7. **The sweep Action.** Add `templates/brain-weekly-sweep.yml` as `.github/workflows/brain-weekly-sweep.yml`. Every Monday it runs Claude Code inside GitHub, turns everything in `inbox/` into proposals, lists PRs and open questions waiting over a week and empty or stale files, opens ONE pull request "What's missing, week of [date]" and has Brain Bot post the summary to Slack. It runs on the founder's Claude subscription, not a paid API key: on a computer with Claude Code, run `claude setup-token`, then add the token as the repo secret `CLAUDE_CODE_OAUTH_TOKEN` (never into a chat or a file). In the repo, Settings, Actions, General: "Read and write permissions" and "Allow GitHub Actions to create and approve pull requests". Then Actions, Brain weekly sweep, Run workflow, to test it once. It uses a few minutes of Actions time and a little of the plan's usage per week.
8. **The 30 seconds for claude.ai chats.** Chats in the claude.ai app have no API, so no script can read them. The Monday Slack post ends with a ready prompt. Whoever reads it pastes it into their company Project and Claude collects every `🧠 Brain update` block from the week's chats (past-chat search works inside a Project on paid plans). Slack remembers, people don't have to.
9. **Optional, for Claude Code users: the local sweep.** Claude Code keeps sessions as files on the computer, so `templates/brain_sweep_local.py` can read them. It takes the last 7 days of Claude Code sessions that touch marketing, hands the excerpts to `claude -p` inside a local clone of the brain repo and opens one pull request "From my Claude Code sessions". Try it with `--dry-run` first. To run it weekly on a Mac, fill the three paths in `templates/com.marketingbrain.sweep.plist`, save it to `~/Library/LaunchAgents/` and `launchctl load` it. On Linux, a cron line: `0 8 * * 1 python3 /path/brain_sweep_local.py --repo /path/repo`. Each person runs it on their own computer, over their own sessions only.

If the founder pastes the webhook URL into the chat anyway: don't write it anywhere, tell them it's now in the chat history and to regenerate it in the Slack app (Incoming Webhooks, remove and add again), then use the new one only in the GitHub secret.

No Slack? Skip steps 1 to 3 and 6. The digest still lands in `digests/` and you can get it by email instead: attach a Gmail connector to the scheduled task and add "and email it to [founder] and [marketer]" to the prompt.

## Run

1. Read `brain.yml` and `CLAUDE.md`. Work out the window: on the first run (no digest file yet), everything since `digest_started` (or `handoff_started`). After that, everything since the commit that added the last digest file (use that commit, not the date in the file name). Take commits on main, merged pull requests, closed ones and open ones. Don't count your own digest commits as changes.
2. **Merge the minor ones.** For each open PR, check the gate in `CLAUDE.md`. Minor and not touching a founder-only file: merge it and note it as merged. Anything else: leave it open and list it under "Waiting for [founder]". When in doubt, it's significant.
3. Write `digests/YYYY-MM-DD.md`:

```
# Brain digest, [date]
[n] changed (merged or committed) since [last date] · [n] waiting for [founder]

## Changed
- [file] · by [founder / marketer] · [what changed, one line]
  Why: [one line] · Based on: [call, report, test, chat, with date]

## Waiting for [founder]
- [file] · proposed by [marketer] · [what and why, one line] · [PR link]

## Declined
- [file] · proposed by [who] · no because [reason] · [PR link]

## Open questions
- [question from open-questions.md, if any are older than 2 days]

## Stale
- [file] · last verified [date] (only files over 60 days)
```

Keep it short enough to read in two minutes. No changes since the last run: write a one-line digest ("No changes since [date]") on weekly runs, skip the file on daily runs.

4. Commit the digest. Main if you're allowed to push there, otherwise your working branch: the Action posts any new digest file on any branch, so Slack gets it either way. If you can't merge PRs from here, list the minor ones under "Ready to merge (minor)" with their links for the founder to click.
5. If you can't push to the repo at all, say so plainly in the run output and hand back the digest text. Never pretend it was posted.

## Weekly sweep

Nobody remembers to update a knowledge base later, so the brain is fed in three places that don't depend on memory:

1. **While working.** The rules in `CLAUDE.md` make Claude end any answer that surfaced something new with a `🧠 Brain update` block. Where it can write (Claude Code, Cowork with git) it saves the block to `inbox/` and opens a PR on the spot.
2. **Every Monday, in GitHub** (setup step 7). The sweep Action works through `inbox/`, stale PRs, old open questions and empty or stale files, opens one "What's missing" PR and posts the summary to Slack.
3. **Every Monday, in Slack** (setup step 8). The summary ends with the prompt for the company Project, which picks up the blocks that stayed in claude.ai chats. Optional: the local script (setup step 9) does the same for Claude Code sessions.

When asked by hand ("what's missing from the brain?"):

- In a claude.ai Project: search this week's chats in the project for `🧠 Brain update` blocks and other brain material, check the brain, give one "Proposed change" per file. If you can't search past chats from here, say so in one line. Never guess what was said.
- In Claude Code or Cowork with the repo: do what the sweep Action does (its prompt is in `templates/brain-weekly-sweep.yml`).
- Everything found goes through the gates like any other change and lands in the next digest under "Proposed this week".

## What this skill will not do

- It doesn't merge anything significant, anything in a founder-only file or anything it isn't sure about.
- It doesn't put the Slack webhook URL, a password or a key into a file, a commit or a chat.
- It doesn't read anyone's chats except the account it runs on (the local script reads only that computer's own Claude Code sessions) and it doesn't make up chat content when it can't search.
- It doesn't rewrite the brain to "tidy it up". It reports changes and proposes additions, people decide.

## Where this comes from

- Put Your Marketing Brain on GitHub Before You Hire, https://owneropsguide.substack.com/p/marketing-brain-github-saas-founders
- Scheduled tasks and connectors in Claude: https://code.claude.com/docs/en/web-scheduled-tasks
