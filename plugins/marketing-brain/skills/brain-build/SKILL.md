---
name: brain-build
description: Builds a B2B SaaS founder's marketing brain, a private GitHub repo with ten folders (customers, positioning, proof, voice, GTM motions, experiments, tools, processes, skills, brand) that a first marketing hire and every AI they use read before doing anything (or that only the founder and their own AI read, before any hire), by researching the company first and then interviewing the founder out loud instead of asking them to write docs. Also adds to it and refreshes it. Use when the founder says "build my marketing brain", "I'm hiring my first marketer", "get my marketing out of my head", "set up a second brain for marketing", "onboard my marketer", "my new hire keeps asking me everything", "a marketing brain just for me", "I'm not hiring yet but want Claude to know my marketing" or pastes a Founder's Brief and wants to turn it into a brain.
---

Last verified: 2026-11-03
Companion post: Put Your Marketing Brain on GitHub Before You Hire, https://owneropsguide.substack.com/p/marketing-brain-github-saas-founders
From The Anti-Grind SaaS Manual by Paul Ogonowski.

# Build your marketing brain

Everything your first marketer needs to know is in your head right now. This skill gets it out. It researches your company, interviews you (you talk, it writes) and hands back a repo with ten folders your marketer and their AI read on day one.

It never invents a fact about your company and it never decides anything for you. It writes down what you know and labels what you don't.

The two other skills in this set take over from here: **brain-handoff** runs the first two weeks with your new hire and **brain-digest** keeps both of you up to date after that.

Not hiring yet? Build it anyway, just for yourself. Your own Claude reads the same files, so every marketing chat starts from them instead of from zero. The other two skills can wait until someone joins.

## Pick the mode first

- **Build.** No brain exists yet. Run the full flow below.
- **Add.** The founder says "add this to the brain" or an answer missed something. Write the one to three lines that would have prevented the miss, put them in the right folder, update `last_verified` in that file and propose the change (see "How changes land" below).
- **Refresh.** The founder says "refresh my brain" or a file's `last_verified` date is more than 60 days old. Ask the six refresh questions in `references/interview.md` and update only what changed.

If the founder pastes a Founder's Brief, use it as the answers it already holds and skip those questions. Ask only what's missing.

## Before you start: say how this works

Tell the founder, in your own words, in four short lines:

1. This takes about 1 to 2 hours of talking for the first version, so we'll do it in two sittings by default (one long chat hits usage limits and gets slow). Voice mode, a dictation tool like Wispr Flow or a Granola note you talk into all work.
2. Rambling is fine. "We tried it, I don't remember the numbers, it's probably in HubSpot" is a perfectly good answer.
3. Everything ends up as plain text files in a private repo. Passwords, API keys and customers' personal data never go in.
4. Before we start: make one Claude Project for your company and run this inside it. Your marketer will make their own project for the company later. Past-chat search works per project, so keeping all marketing work in one project per person is what lets the brain learn from your chats later.

## Step 1: Research first

Ask for the founder's name and company website only. Then research the company the way a good new hire would before day one. Follow Step 1 of `references/interview.md` (website, pricing page, reviews, LinkedIn, podcasts, changelog, competitors).

**Then the founder's own writing.** Ask: "Do you post on LinkedIn or write a newsletter? If yes, give me your profile URL or paste a few posts." Read up to two years of posts if you can open them (LinkedIn often needs a login: if you can't open it, ask the founder to paste 10 to 20 posts or export them). Pull out the beliefs they repeat, the stories they tell and the words they use. These feed `positioning/beliefs.md`, `voice/founder.md` and `customers/`.

Hand back a summary of ten lines at most, with the source on every line. Nothing from the research goes into the brain until the founder confirms it.

## Step 2: Give it the stuff you'd never summarize yourself

Ask which of these the founder can connect or paste. Take whatever they have, skip the rest:

- **Email.** If a Gmail or Outlook connector is on, search threads with customers, agencies, consultants and contractors from the last 2 to 3 years for past campaigns, tests and decisions. List what you found and ask the founder to confirm before anything goes in.
- **Projects.** Notion, Basecamp, Jira, ClickUp, Google Drive, wherever old campaigns, plans and reports live. Same rule: list, confirm, then write.
- **Calls.** Sales call recordings or transcripts (Granola, Gong, Fathom, Zoom). Pull the words customers use for the problem into `customers/their-words.md`.
- **An experiment log**, if there is one.

No connectors at all? That's fine. The interview covers it, it just takes longer.

## Step 3: The interview

Follow Steps 2 to 4 of `references/interview.md`: one or two questions at a time, skip what the research and the connected tools already answered, use the founder's words. Three parts of it are where this skill goes deeper than a normal company brief, so never skip them:

1. **Every GTM motion and channel, one by one.** For each motion and each channel in the lists in `references/interview.md`, ask four things: Did you ever try it? When, roughly? What happened? Where would the data be if we needed it? "Never tried" is an answer. Write every channel down, including the ones that did nothing. That file is the one that saves your marketer weeks.
2. **Tools and who owns access.** For every tool marketing and sales touch: what it's for, who can let a new person in, what plan you're on. Never ask for or write down a password, a key or a login.
3. **Processes.** For anything the founder does themselves every week or month (the webinar setup, the newsletter send, the ad report), ask them to record a short screen video of doing it and talking through it. When they share the recording or its transcript, write it down as a step-by-step process in `processes/`. Until then, add the process name with `[recording needed]`.

Ask for proof on anything that "worked" or "didn't work": what happened, when and how do you know? No proof goes in as `(unverified)`. A belief with no reason goes in as `(gut feel)`. Both are allowed, they just get labelled.

Ask the founder which files only they may change. Default founder-only: everything in `positioning/`, `voice/founder.md` and `proof/pricing.md`. Everything else is shared.

**Two sittings.** At the end of the first sitting, write `brain-progress.md` (what's covered, what's left, the answers so far) and hand it to the founder. At the start of the second, ask them to paste or attach it and carry on from there.

**If the founder pastes a password, key or login:** don't write it anywhere, say it's now in the chat history, tell them to change it and note only who grants access to that tool.

## Step 4: Write the repo

First show the founder the file list, how many lines are still `[not given yet]` and the repo name and ask: "OK to write it?" Only then create anything.

Build it from `templates/brain/`. Copy `gtm-motions/_motion-template.md` once per motion that brings revenue and delete the template. Fill `brain.yml` with what you know. Every content file (not the READMEs or `open-questions.md`) starts with this header:

```
---
owner: founder        # founder = only the founder changes it, the marketer proposes. shared = both can change it, subject to the gates in CLAUDE.md.
last_verified: YYYY-MM-DD
sources: [interview, website, G2, email 2025-03, HubSpot report]
---
```

Fill the files the template lists. Keep every file short: a few lines per item, a pointer where the data lives. Cut anything a generic AI would get right without being told. What stays is what only this founder knows.

Before handing it over, check every number and name against what the founder said. If you rounded or narrowed something, put back their wording.

**How to deliver it:**

- If you can push to GitHub (a GitHub connector, Claude Code, Cowork with git): create a **private** repo named `[company]-marketing-brain`, commit everything and send the founder the link.
- If you can't: create the files and hand them over as one ZIP with the folder structure, then walk the founder through it: on github.com, New repository, Private, then "uploading an existing file" and drag the unzipped folder in. Five minutes, no command line.

Heavy files (logo files, banners, screen recordings, decks) go to Google Drive or wherever the founder keeps them. `brand/README.md` and `processes/` link to the folders.

## Step 5: Hook it up

Say this to the founder, in your own words:

1. In your company Claude Project, connect GitHub (or add the repo files to the project knowledge if you're not using GitHub yet). Paste the project instructions from the top of the `CLAUDE.md` in your repo into the project's instructions field. A Project reads the repo but can't write to it, so changes made from a Project come out as "Proposed change" blocks you paste on github.com (CLAUDE.md explains how). Claude Code or Cowork with git can open the pull requests directly.
2. When your marketer starts, run **brain-handoff** and ask: "My marketer starts Monday, what do I do?"
3. Two weeks later, run **brain-digest** setup to get the daily digest into Slack.

## How changes land

Every change to the brain is a proposal with a reason:

- **Founder-only files** (`owner: founder`): if the person asking isn't the founder, never edit. Propose the change as a pull request (or, without GitHub, as a "Proposed changes" list) with what changes, why and based on what.
- **Shared files**: in the first two weeks with a new hire, propose too. After that, follow the gates in `templates/brain/CLAUDE.md`: minor changes go straight in, significant ones wait for the founder.

## What this skill will not do

- It doesn't invent a number, a channel result, a customer or a belief. Anything not said stays `[not given yet]`.
- It doesn't ask for exact revenue (a range is enough) and never writes down passwords, keys, logins or customers' personal data.
- It doesn't decide your positioning, pricing, channels or who you hire. It writes down what you decided.
- It doesn't put anything from email, Notion or calls into the brain before you confirm it.
- It doesn't make the repo public. Ever.

## Where this comes from

- Put Your Marketing Brain on GitHub Before You Hire, https://owneropsguide.substack.com/p/marketing-brain-github-saas-founders
- The interview builds on The Founder's Brief: Why AI Gives You Generic Answers About Your SaaS (and How to Fix It), https://owneropsguide.substack.com/p/why-ai-gives-generic-answers
- Who to hire before you build this: How to Market Your B2B SaaS After the $1M Founder Ceiling, https://owneropsguide.substack.com/p/how-to-market-b2b-saas-after-1m-arr
