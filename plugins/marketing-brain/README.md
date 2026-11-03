# The Marketing Brain

Get your marketing out of your head before you hire your first marketer.

Everything your new marketer needs to know is in your head right now: who buys and why, what you believe, which channels you tried and what flopped, which tool does what. Usually that turns into two calls, a doc that skims the surface and weeks of archaeology in your inbox. These three skills turn it into a private GitHub repo your marketer and every AI either of you uses read on day one, plus the rules that keep it from drifting once two people change it.

You talk, Claude writes. Usually about 1 to 2 hours of talking for the first version, split over two sittings.

## Not hiring yet?

Build it anyway, just for you. Your own Claude reads the same files, so every marketing chat starts from your customers, your positioning and what you already tried, instead of from zero. Run brain-build on its own. brain-handoff and brain-digest can wait until someone joins.

## The three skills

**brain-build** researches your company (site, pricing, reviews, your LinkedIn posts), reads what you connect (email, Notion, Basecamp, Jira, ClickUp, call transcripts) and interviews you, including every GTM motion and channel you ever tried and the ones that did nothing. It writes a repo with ten folders: customers, positioning, proof, voice (the company's and yours), GTM motions, experiments, tools and who grants access, processes, skills and brand. Never passwords, never made-up facts.

**brain-handoff** runs the first two weeks. Ask "my marketer starts Monday, what do I do?" and you get a checklist from your own files: which access to grant in which tool, which files stay founder-only, when your daily talk is. Then every day it goes through your marketer's proposed changes with you (10 minutes, yes or no and why) and turns their open questions into the agenda for your 15 to 30 minute talk.

**brain-digest** takes over after that. Every day (or week) a scheduled task writes what changed, who changed it, why and based on what, both ways. Minor changes go straight in, anything touching positioning, voice, pricing or a founder-only file waits for you. A GitHub Action posts each digest to Slack as Brain Bot.

**Nobody has to remember to update it.** Claude flags new brain material while you work (a `🧠 Brain update` block at the end of the answer, or a pull request straight away in Claude Code). Every Monday a GitHub Action runs Claude Code on your subscription (no API key), turns everything caught into one "What's missing" pull request and Brain Bot posts it to Slack, with a 30-second prompt that collects the blocks left in your claude.ai chats. Claude Code users can add a small Python script that sweeps their local sessions the same way.

## What it costs

Nothing beyond your Claude plan. Skills and Projects work on every Claude plan, Free included, so brain-build and brain-handoff run there (the Free plan's usage limits mean the interview takes two or three sittings). The daily digest, the weekly sweep and past-chat search need a paid plan. GitHub's free plan covers the repo and the Action (2,000 minutes a month on private repos, a digest takes seconds). The free Slack plan is enough for Brain Bot.

One honest limit: on a free GitHub account the "founder-only" flag is soft. Every AI reading the repo respects it because the rules file says so, but GitHub itself won't block a push. If you want a hard lock, GitHub Pro or Team plus the included `CODEOWNERS.example` does it.

## Install

**Claude Code**

```
/plugin marketplace add pogonow/operator-toolkit
/plugin install marketing-brain@operator-toolkit
```

Then say "build my marketing brain".

**Claude.ai and Cowork:** download the three ZIPs from [`downloads/`](https://github.com/pogonow/operator-toolkit/tree/main/downloads) (`marketing-brain-build.zip`, `marketing-brain-handoff.zip`, `marketing-brain-digest.zip`) and upload each one under Skills in Claude's settings. Do it inside one Claude Project for your company. Your marketer makes their own project later.

Already built a Founder's Brief? Paste it in at the start and brain-build skips every question it already answers.

## Read the why

[Put Your Marketing Brain on GitHub Before You Hire](https://owneropsguide.substack.com/p/marketing-brain-github-saas-founders) has the story behind it: the cold outreach campaign a founder forgot to tell me about and why I'd pick GitHub over Notion for this.

## Something broke?

Open an [issue](https://github.com/pogonow/operator-toolkit/issues) or DM me on [LinkedIn](https://www.linkedin.com/in/pawelogonowski/). Tell me which question felt pointless for a company your size and which file your marketer still had to ask you about.
