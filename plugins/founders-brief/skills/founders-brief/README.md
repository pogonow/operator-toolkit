# The Founder's Brief

The onboarding your AI never got, built for B2B SaaS founders.

Ask a fresh chat a hard question about your company and you get a five-point plan that could fit any SaaS on earth. The model isn't the problem. It knows nothing about your ICP, your ACV, your motion or what you already tried, same as a smart new hire on day one. This skill fixes that by interviewing you instead of asking you to write a 20-page doc.

## How it works

1. **Homework first.** It asks for your name and your website, then reads your site, your pricing page, your G2 and Capterra reviews, your LinkedIn and any podcasts you've been on. You get a ten-line summary with a source on every line and nothing goes in the brief until you confirm it.
2. **The SaaS basics.** ARR range (a band, never the exact number), ACV, ICP and who signs the deal, your positioning and value prop (executive value and end-user value for high-ACV deals), the positioning you already tested, your competitors, your GTM motions and the channels that feed them, churn and NRR. If you keep an experiment log, it reads that too.
3. **The interview.** One question at a time, up to about 30. Anything you say failed needs proof and anything you believe will work needs a reason. Unproven stuff still goes in, just labelled, so your AI knows a fact from a hunch.
4. **The founder-only layer.** Runway, margins by plan, the customer you'd happily lose. It reminds you to check your data and memory settings first and marks every private line so a team copy can strip it.
5. **One file back.** A few pages of Markdown, dated, plus a short instruction to paste into a Claude or ChatGPT project so every answer starts from the brief and the brief gets updated when you correct something.

It also has an add mode (one to three lines after a miss) and a ten-minute monthly refresh.

## Install

**Claude Code**

```
/plugin marketplace add pogonow/operator-toolkit
/plugin install founders-brief@operator-toolkit
```

Then say "build my brief".

**Claude.ai and Cowork:** download the ZIP from [the post that comes with it](https://owneropsguide.substack.com/p/owners-brief-skill) and upload it under Skills in Claude's settings. Works on every plan, Free included.

**ChatGPT, Gemini and other agents:** paste the whole `SKILL.md` into the chat or the project instructions and say "build my brief". Or:

```
npx skills add pogonow/operator-toolkit
```

## Read the why

[Why AI Gives You Generic Answers About Your SaaS (and How to Fix It)](https://owneropsguide.substack.com/p/why-ai-gives-generic-answers) has the story behind it, plus two ways to keep the brief alive: one project with one file or a private GitHub repo like mine.

## Something broke?

Open an [issue](https://github.com/pogonow/operator-toolkit/issues) or DM me on [LinkedIn](https://www.linkedin.com/in/pawelogonowski/). Tell me which question felt pointless for a company your size and which one was missing.
