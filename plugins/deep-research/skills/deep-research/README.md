# Deep Research

Research done the way a strategy consultant or a BizOps lead would do it.

Ask a plain AI to research something and you usually get the intern version. One blog post treated as gospel, a Reddit thread treated as data and the actual answer buried somewhere in paragraph six. (Kyle Poyar [calls these](https://www.growthunhinged.com/p/claude-skills-gtm-and-pricing) "intern-level mistakes", which is exactly it.) This skill runs a fixed workflow so that doesn't happen.

I built it for myself. The first real run was a pricing question for a SaaS I advise. My one complaint was that I couldn't click through to the sources. So now every claim links to the exact page it came from and verbatim quotes jump straight to the highlighted sentence.

## How it works

1. **Context first.** It reads what it already knows about you and your company before it asks you anything.
2. **One round of questions, mostly clicks.** Where to start (the data or the experts), what decision this feeds, what you think the answer is right now and the scope.
3. **A plan you sign off.** The key question, a hypothesis to prove or kill, 3 to 5 sub-questions that don't overlap and the sources it'll use. Nothing gets collected until you say go.
4. **Primary sources first.** Company pages, filings, docs, changelogs, job posts and original data beat articles written about them. Every number gets chased back to where it came from. Forums count as anecdote, never as data.
5. **Answer first.** The title is the answer and every heading is a finding, so you can stop reading after five lines and still know what it found. A source table closes the report.
6. **A red-team pass before you see it.** It re-checks the numbers, names its three weakest claims and looks one more time for evidence against its own answer (confirmation is the default failure, so it goes looking on purpose).

## Two routes

- **Evidence-first** for fact questions: prices, market size, who does what, what changed.
- **Experts-first** for judgment calls: how to price, how to structure a team. It first finds people actually worth listening to (they've done the thing, they publish their own data and they're not selling the answer). You get to add names you trust or drop ones you don't. Then it maps where they agree, where they split and which view fits your situation.

It asks you which route at the start, you don't have to remember it.

## Modes

- `quick` for one fact. No questions, the answer lands in chat.
- `standard` for a real question with a few parts.
- `deep` for a decision with money on it. Each branch gets its own subagent running in parallel.

## Install

**Claude Code**

```
/plugin marketplace add pogonow/operator-toolkit
/plugin install deep-research@operator-toolkit
```

Then just ask for it ("do a deep dive on...", "what do the experts think about...") or call `/deep-research:deep-research`.

**Claude.ai and Cowork:** download `deep-research.zip` from [Releases](https://github.com/pogonow/operator-toolkit/releases) and upload it under Skills in Claude's settings.

**Other agents** (Codex, Cursor, Copilot, Gemini CLI and more):

```
npx skills add pogonow/operator-toolkit
```

## Something broke?

Open an [issue](https://github.com/pogonow/operator-toolkit/issues) or DM me on [LinkedIn](https://www.linkedin.com/in/pawelogonowski/). Tell me what you asked and what came back, that's usually enough for me to fix it.

## Credits

The workflow follows Kyle Poyar's description of his own research skill in [Growth Unhinged](https://www.growthunhinged.com/p/claude-skills-gtm-and-pricing) and Torsten Walbaum's [Deep Research for GTM](https://www.growthunhinged.com/p/deep-research-for-gtm). The effort scaling and source-quality rules come from Anthropic's write-up on their [multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system). The report shape is Barbara Minto's pyramid.
