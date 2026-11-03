---
name: brain-handoff
description: Runs the first two weeks of handing a founder's marketing over to a new marketing hire, on top of the marketing brain repo. Gives the founder a day-one checklist from their own brain files (which access to grant in which tool, which files to flag founder-only, when the daily talk is), reviews the marketer's proposed changes before the daily talk, turns open questions into a talk agenda and switches the brain to digest mode when the two weeks are up. Use when the founder says "my marketer starts Monday, what do I do?", "onboard my new hire", "review the brain changes", "prep my daily with [marketer]", "what did my marketer propose" or "switch the brain to digest mode".
---

Last verified: 2026-11-03
Companion post: Put Your Marketing Brain on GitHub Before You Hire, https://owneropsguide.substack.com/p/marketing-brain-github-saas-founders
From The Anti-Grind SaaS Manual by Paul Ogonowski.

# Hand the brain over

The first two weeks with a new marketer decide whether the brain becomes theirs or stays yours. This skill runs them: everything goes through you, in 10 minutes of review and a 15 to 30 minute talk a day, until your marketer runs out of questions.

It drafts, you decide. It never approves a change for you and it never decides anything about your hire.

Needs the marketing brain repo (built with **brain-build**). If there isn't one, say so and offer to run brain-build first.

## Pick the mode

- **Day one.** "My marketer starts Monday, what do I do?" or "onboard my new hire".
- **Daily review.** "Review the brain changes", "prep my daily", "what did [marketer] propose".
- **Switch.** "Switch the brain to digest mode" or the founder asks whether the two weeks are up.

Read `brain.yml` and `CLAUDE.md` in the repo first, every time.

## Day one

Ask three things, one at a time: the marketer's start date, their GitHub username (if they don't have one, it's free at github.com and takes two minutes) and the time for your daily talk.

Then build the checklist from the founder's own files. Never from a generic onboarding list.

1. **Access.** Go through `tools/stack.md` and `tools/people-and-access.md` line by line. For each tool: what it's for, who grants access, which level you'd suggest (view, edit, admin) and why. Flag any tool where the file says `[not given yet]` for who grants access. Never ask for or write a password.
2. **The repo.** Add the marketer as a collaborator (Settings, Collaborators, Add people). Update `brain.yml`: `mode: handoff`, `handoff_started`, `marketer_role`, both GitHub handles, `daily_talk`.
3. **Founder-only flags.** List every file with `owner: founder`. Ask the founder to confirm the list in one line or change it. Mention once that a hard lock (CODEOWNERS plus branch protection, see `CODEOWNERS.example`) needs GitHub Pro or Team on a private repo and that the soft flag works without it because every AI reading the repo follows `CLAUDE.md`.
4. **Their AI.** Tell the founder to send the marketer three things: the repo link, the project instructions from the top of `CLAUDE.md` and one sentence: "Make one Claude Project for [company], connect GitHub, paste these instructions, then ask it anything before you ask me."
5. **The daily talk.** 15 to 30 minutes, every working day for two weeks, at a fixed time. Suggest putting it in both calendars now. If the founder says daily is impossible, suggest every two or three days and say once that daily is better for two weeks.
6. **The first reading list** for the marketer: `positioning/`, `customers/`, `experiments/channels.md`, then the motion that brings most revenue in `gtm-motions/`.
7. **What's missing.** Any file still full of `[not given yet]` or `[recording needed]` that the marketer will need in week one. Offer to fill the top three now with brain-build add mode.

Hand back:

```
# Day one checklist: [marketer role], starts [date]

## Before they start
- [ ] Access: [tool] · [level] · grant via [who] · [why they need it]
- [ ] Add [@handle] to the repo, set brain.yml to handoff
- [ ] Confirm founder-only: [files] (soft lock: stops the AIs, not people, unless you add the hard lock)
- [ ] Send the repo link + project instructions
- [ ] Daily talk in both calendars: [time], [date] to [date]

## Their first reading
1. [file] · [why first]

## Gaps to fill this week
- [file] · [what's missing] · [who can fill it]
```

End with the one thing to do today.

## Daily review

1. List the open pull requests on the repo (or the "Proposed changes" the marketer sent, if the repo isn't on GitHub yet). For each: the file, what changes, why, based on what and the gate from `CLAUDE.md` (minor or significant). Judge the gate yourself from the change, never from the checkbox the author ticked.
2. For each one, give the founder your read in one line: looks right, needs a source, conflicts with [file], touches a founder-only file. Never more than one line per change.
3. Ask the founder to go through them: yes, no or change. For every no, ask for the reason in a few words. The reason gets written into the PR when it's closed, because a "no" without a why teaches the marketer nothing.
4. Read `open-questions.md`. Group the questions by topic.
5. Hand back the agenda for today's talk:

```
# Daily talk, [date] (day [n] of 10 working days)

## Decided
- [change] · yes / no because [reason]

## Open questions from [marketer]
- [question] · [file the answer goes into]

## For you to ask them
- [one question about what they learned or got stuck on]
```

6. After the talk, if the founder tells you the answers, write them into the right files (founder-only files only by or for the founder), delete the answered lines from `open-questions.md` and merge or close the PRs the founder decided. If you can't push to GitHub, hand back the exact edits.

## Switch

The founder decides when the two weeks are up. Help them decide with two numbers from the last three working days: how many new open questions came in and how many proposals got a "no". Few of both means the brain is doing its job. Lots of either means the brain is missing something, which usually says more about the brain than about the person. Say that plainly, then let the founder call it.

On switch: set `mode: digest` and `digest_started` in `brain.yml`, keep the founder-only flags (or drop the ones the founder lets go) and tell the founder to run **brain-digest** setup next.

## What this skill will not do

- It doesn't approve, merge or close a change the founder didn't decide.
- It doesn't judge the marketer as a person, score them or suggest anything about keeping or letting them go. If the founder asks, it says that's their call and goes back to what the brain is missing.
- It doesn't write passwords, keys or logins anywhere and doesn't grant access itself. It tells the founder what to grant.
- It doesn't invent a tool, an owner or an access level that isn't in the brain. Gaps stay `[not given yet]`.

## Where this comes from

- Put Your Marketing Brain on GitHub Before You Hire, https://owneropsguide.substack.com/p/marketing-brain-github-saas-founders
- What your hire should do in the first 90 days (Capland's plan): How to Market Your B2B SaaS After the $1M Founder Ceiling, https://owneropsguide.substack.com/p/how-to-market-b2b-saas-after-1m-arr
