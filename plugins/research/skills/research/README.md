# research

Research the way a strategy consultant or a BizOps lead does it, not the way a chatbot does.

Ask a plain AI to research something and you get the intern version: one blog post treated as gospel, a Reddit thread treated as data, a wall of text with the answer somewhere in paragraph six. This skill fixes that with a fixed workflow.

## How it works

1. **Context first.** It reads what it already knows about you and your company before it asks anything.
2. **One round of questions, with clicks.** Where to start (the data or the experts), what decision this feeds, your current bet, the scope.
3. **A plan you sign off.** The key question, a hypothesis to prove or kill, 3-5 sub-questions that do not overlap and the sources it will use. Nothing gets collected before you say go.
4. **Primary sources first.** Company pages, filings, docs, changelogs, job posts and original data beat articles about them. Every number gets chased to where it came from. Forums count as anecdote, never as data.
5. **Answer first.** The title is the answer. Every heading is a finding. Every claim links to the exact page. Verbatim quotes jump straight to the highlighted passage. A source table closes the report.
6. **A red-team pass before you see it.** It re-checks the numbers, names the three weakest claims and looks one more time for evidence against its own answer.

## Two routes

- **Evidence-first** for fact questions: prices, market size, who does what.
- **Experts-first** for judgment calls: how to price, how to structure a team. It first finds people worth listening to (they have done the thing, they publish their own data, they are not selling the answer), lets you add or drop names, then maps where they agree, where they split and which view fits you.

## Modes

`quick` for one fact (no questions, answer in chat), `standard` for a real question and `deep` for a decision with money on it (parallel subagents per branch).

## Install

See the [main README](../../../../README.md#install-a-skill).

## Credits

The workflow follows Kyle Poyar's description of his own research skill in [Growth Unhinged](https://www.growthunhinged.com/p/claude-skills-gtm-and-pricing) and Torsten Walbaum's [Deep Research for GTM](https://www.growthunhinged.com/p/deep-research-for-gtm). Effort scaling and source-quality rules come from Anthropic's [multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system). The report is Barbara Minto's pyramid.
