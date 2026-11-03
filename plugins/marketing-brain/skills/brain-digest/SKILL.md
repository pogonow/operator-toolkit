---
name: brain-digest
description: Keeps a founder and their marketing hire up to date on the marketing brain repo after the first two weeks. Writes a daily or weekly digest of what changed, why and based on what (both ways, the founder's changes and the marketer's), merges the minor changes and holds the significant ones for the founder, once a week looks for what should be in the brain but isn't and sets up the Brain Bot that posts each digest to Slack through a GitHub Action. Use when the founder says "set up the brain digest", "brain digest", "what changed in the brain", "set up Brain Bot", "post the digest to Slack" or when a scheduled task says "Run brain-digest for [repo]".
---

Last verified: 2026-11-03
Companion post: Put Your Marketing Brain on GitHub Before You Hire, https://owneropsguide.substack.com/p/marketing-brain-github-saas-founders
From The Anti-Grind SaaS Manual by Paul Ogonowski.

# Keep the brain fresh

After the first two weeks, nobody should have to ask "what changed?". This skill writes it down every day (or every week): what changed in the brain, who changed it, why and based on what. You see your marketer's changes and they see yours.

It merges only what the gates in `CLAUDE.md` call minor. Everything significant waits for the founder.

Needs the marketing brain repo in `mode: digest` (see **brain-handoff**). If `brain.yml` still says `handoff`, say so and ask whether to switch.

## Pick the mode

- **Setup.** "Set up the brain digest" or "set up Brain Bot". Run once.
- **Run.** "Run brain-digest for [repo]" (usually from the scheduled task) or "what changed in the brain".
- **Weekly gaps.** Part of the run on the first run of each week, when asked "what's missing from the brain?" or when the prompt says "weekly gaps only" (then skip the digest file).

## Setup

Walk the founder through it one step at a time and wait for "done" after each. About 15 minutes in total.

1. **Brain Bot in Slack.** Go to api.slack.com/apps, Create New App, From scratch, name it "Brain Bot", pick the workspace (the free Slack plan works). In the app: Incoming Webhooks, switch on, Add New Webhook to Workspace, pick the channel (suggest `#marketing-brain`, with both founder and marketer in it). Copy the webhook URL. It's a secret: never paste it into a chat, a file or the repo.
2. **The secret on GitHub.** In the repo: Settings, Secrets and variables, Actions, New repository secret. Name `SLACK_WEBHOOK_URL`, value the URL from step 1.
3. **The Action.** Add `templates/brain-digest-to-slack.yml` to the repo as `.github/workflows/brain-digest-to-slack.yml` (commit it if you can push, else give the founder the file and the path). From now on every new file in `digests/` gets posted to Slack as Brain Bot. Free private repos include 2,000 Actions minutes a month and a digest takes seconds.
4. **The scheduled task.** Scheduled tasks need a paid Claude plan and live in Claude Code (claude.ai/code/scheduled or Schedule in the desktop app). New task, daily at a time the founder picks (weekly if `brain.yml` says `digest: weekly`), with the brain repo attached and the Claude GitHub app given write access to it. If the task settings offer unrestricted branch pushes for the repo, allow it so the digest can land on main. The prompt, one line: `Run brain-digest for [owner]/[company]-marketing-brain.` One digest task on the founder's account is enough, because the digest covers both people. If the marketer wants their chats checked too, their own task's prompt is `Run brain-digest weekly gaps only for [owner]/[company]-marketing-brain.`: it opens PRs and never writes a digest file.
5. **Test it.** Do one run now. Check the digest file landed in `digests/` and the message showed up in Slack. If Slack stays empty, check the secret name and that the workflow file sits in `.github/workflows/`.
6. Set `slack: true` in `brain.yml`.

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

## Weekly gaps

On the first run of each week (or when asked):

1. **Chats.** This works best when run by hand inside the company Claude Project ("what's missing from the brain?"). A scheduled run usually can't see Project chats, so expect it to skip this step. If you can search past chats, look through the last 7 days of chats in the company's Claude Project for things that sound like brain material: a new competitor, a customer's words, a test result, a decision, a new belief. Each person's task only sees their own chats. The marketer's task runs weekly gaps only (setup step 4), so there's never a second digest file. If you can't search chats from here, skip this step and say so in one line. Never guess what was said.
2. **Missing files.** List files still full of `[not given yet]` or `[recording needed]`.
3. Turn what you found into proposals: one pull request per topic, with what, why and based on what (the chat date). They go through the gates like any other change.
4. Add a "Proposed from this week's chats" section to the digest with the PR links.

## What this skill will not do

- It doesn't merge anything significant, anything in a founder-only file or anything it isn't sure about.
- It doesn't put the Slack webhook URL, a password or a key into a file, a commit or a chat.
- It doesn't read anyone's chats except the account it runs on and it doesn't make up chat content when it can't search.
- It doesn't rewrite the brain to "tidy it up". It reports changes and proposes additions, people decide.

## Where this comes from

- Put Your Marketing Brain on GitHub Before You Hire, https://owneropsguide.substack.com/p/marketing-brain-github-saas-founders
- Scheduled tasks and connectors in Claude: https://code.claude.com/docs/en/web-scheduled-tasks
