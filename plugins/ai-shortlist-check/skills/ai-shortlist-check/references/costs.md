# What the API route costs, and the three choices that set it

Last verified: 2026-10-21, on real OpenRouter calls (usage.cost on every answer). Prices move. The script prints the real cost at the end of every run, so trust that line over this table after week one.

Read this before onboarding questions 5, 9 and 10, and whenever the founder asks what the check costs.

## Where the money goes

Every chat answer with web search is billed twice: the tokens and a search fee. What differs between engines is which of the two is big.

| Engine (model on OpenRouter) | Cost per answer | What you pay for |
|---|---|---|
| ChatGPT, own chat model (`openai/gpt-chat-latest`) | $0.09-0.15 | The search results get pasted into the model's prompt. A 60-token buyer question becomes 13,000-21,000 input tokens at $5 per million, plus ~1,200 output tokens at $30 per million, plus the search fee. Comparison prompts cost the most, since more pages get pasted in. |
| ChatGPT, cheaper OpenAI model (`openai/gpt-6-luna`) | $0.03-0.04 | The same pasted pages, at $0.10 per million input tokens. Almost all of it is the search fee. |
| Gemini (`google/gemini-3.8-flash`) | ~$0.03 | Google searches on its side and doesn't bill the pages as tokens. You pay a flat grounding fee per answer, so the tokens look tiny and the bill doesn't. |
| AI Overviews (SerpApi) | $0 | One Google search per query. 20-30 queries a week fit SerpApi's free 250 searches a month. That is a separate pool from OpenRouter. |

On top: OpenRouter adds a fee of about 5.5% when you buy credits.

Two things that did not cut the bill in testing: `search_context_size` (low and medium gave the same tokens) and a lower `max_results`. The script doesn't send either.

Two things that inflated the first real run by about a quarter: retries on a new account's rate limits and a restart that asked again. The script now retries only calls that were never billed (rate limits and provider errors), never a timeout, and picks up from the run file after a crash.

## The two kinds of run

- **Weekly run.** Non-branded prompts only. ChatGPT answers through the cheaper OpenAI model, Gemini as always. This is the trend line.
- **Full run.** Every prompt, branded ones included. ChatGPT answers through its own chat model, the one ChatGPT users get. It checks the weekly model against the real one and catches the branded answers (wrong prices, old facts) that move slowly.

Branded prompts ("Is [Product] worth it?", "[Product] vs [Competitor]") never run weekly. The founder usually wins them and they don't count toward share of voice.

## The choices the founder makes

1. **How many prompts.** 10, 15, 20 or 25. About 70% non-branded, 30% branded.
2. **Runs per non-branded prompt each week.** 2 (recommended) or 1 (cheaper). AI answers repeat the same list of brands less than once in 100 runs (SparkToro), so one run a week is noise and only a 4-week trend means anything. Two runs give a weekly number worth reading.
3. **How often the full run comes back.** Every 4 weeks (recommended) or every 8. Non-branded prompts get 3 runs there. Branded prompts get 2 (recommended) or 1 (cheaper, saves $0.40-1 a run).
4. **The first full run.** Real (3 runs, branded 2) or a test at 1 run each, to see what comes back before spending more. The test starts the cycle like a real one.

## The table

Monthly figures include the 5.5% OpenRouter fee. Branded prompts at 2 runs in the full run.

| Prompts | Weekly run, 1 run each | Weekly run, 2 runs each | Full run | Month, full every 4 weeks (1 / 2 weekly runs) | Month, full every 8 weeks (1 / 2) | First full run as a 1-run test |
|---|---|---|---|---|---|---|
| 10 | $0.44 | $0.88 | $3.70 | $6 / $7 | $4 / $6 | $1.40 |
| 15 | $0.69 | $1.39 | $5.60 | $9 / $11 | $6 / $9 | $2.10 |
| 20 | $0.95 | $1.89 | $7.50 | $12 / $15 | $8 / $12 | $2.70 |
| 25 | $1.13 | $2.27 | $9.30 | $15 / $19 | $10 / $14 | $3.40 |

How it's computed: weekly = non-branded prompts x runs x ($0.0315 ChatGPT on the cheaper model + $0.0315 Gemini). Full = (non-branded x 3 + branded x 2) x ($0.105 ChatGPT on its own model + $0.032 Gemini). A 4-week cycle is 3 weekly runs and 1 full run.

## How much to top up

- At least **$15** on OpenRouter. A full run at 25 prompts costs about $9.30 on its own, so $10 minus the fee leaves nothing spare for a comparison-heavy week.
- **$20** for 25 prompts with a real full run at the start, so the first month runs without a second top-up.
- The balance is a hard cap. When credits run out mid-run, the calls fail and get recorded as errors. Top up and run the same command again the same day: it keeps the answers already saved and asks only the missing ones.
