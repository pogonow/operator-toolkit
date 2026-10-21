# The no-key and paste routes

Last verified: 2026-10-20

Read this when the founder picked the no-key route or the paste-everything route, when you hand out a paste block on the API route or when the founder insists on Copilot.

## No-key route

Answer each chat prompt yourself with web search, the way a neutral assistant would answer a buyer. Write the full answer before you check whether the founder's product is in it. Record the brands you named and the URLs you cited. These rows use engine `proxy` and carry the APPROXIMATION label.

Then give the founder this block for the top 5 non-branded prompts (the ones closest to buying):

```
Open ChatGPT in a fresh chat, with memory off if you can. Paste each
prompt on its own, [3] times, each time in a new chat. Copy the full
answer with its sources and paste it back here with the prompt number
and run on top, like "P2, run 1".

P1: [prompt]
...
P5: [prompt]
```

Add Gemini to the first line only if the founder wants it pasted too. Then this block for the top 5 non-branded Google queries:

```
Google each query in a private window. For each one, tell me: did an
AI Overview show? If yes, paste its text and the links listed in it.

G1: [query]
...
G5: [query]
```

Pasted answers become real rows with mode `manual` (engine `ai_overviews` for the Google ones). Approximation rows and real rows never go into one share of voice number.

## Paste-everything route

The founder pastes every answer by hand, using the blocks above with all their prompts and queries. Be honest that this takes an hour or so. Offer to cut to the [10] prompts and [5] queries closest to buying for this week.

On the no-key and paste routes (and for pasted answers on the API route), write the rows yourself. Read `references/history-format.md` first.

## Why no Copilot (for you, never said unprompted)

Never propose Copilot as an engine. Consumer Copilot has no public API. The Microsoft 365 Copilot Chat API answers from the company's own data and needs an M365 Copilot licence plus a sign-in to the founder's tenant. The closest proxy is an Azure AI Foundry agent with Grounding with Bing Search, at $35 per 1,000 calls plus agent and model costs. It's heavy to set up and still only a proxy. A weekly manual paste is a chore founders drop.

If the founder insists, offer the top 5 non-branded prompts as a paste block for Copilot (rows with engine `copilot` and mode `manual`). If they want it automated, describe the Azure option at that high level and say this skill's script doesn't call it. Describe no menu path or setting you can't see.
