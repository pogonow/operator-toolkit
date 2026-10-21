# AI Overviews: the Google query list and the weekly check

Last verified: 2026-10-20 against SerpApi's docs (https://serpapi.com/search-api, https://serpapi.com/ai-overview, https://serpapi.com/google-ai-overview-api, https://serpapi.com/pricing).

Read this in onboarding question 6 once the founder said ok to the engines. Read it again before each weekly run that touches AI Overviews.

## Why a separate list

AI Overviews answer Google searches. A buyer who googles types three to six words, so a long chat prompt tests a search nobody runs. ChatGPT and Gemini get the conversational list from `references/prompt-building.md`. AI Overviews get list (b): 15 to 20 short Google-style queries.

AI Overviews are their own surface. Even Google's AI Mode and AI Overviews cite the same URLs only 13.7% of the time (Ahrefs, https://ahrefs.com/blog/ai-overviews-vs-ai-mode). So a win on Gemini tells you nothing about the answer box on top of Google.

## How buyers google

Short, plain and close to buying. The patterns that matter for a SaaS founder:

- Category plus niche: "[category] for [niche]", like "influencer platform for shopify brands"
- Competitor escape: "[competitor] alternatives", "[competitor] alternative for [niche]"
- Head to head: "[competitor] vs [competitor]", "[product] vs [competitor]"
- Pricing: "[category] pricing", "[competitor] pricing", "[product] pricing"
- Job to be done: "how to [job] [niche]", "best way to [job]"

## Building list (b)

1. **Seed it.** Use the category, each niche, each competitor and the founder's own words from questions 1 to 5. Typical seeds: "[category]", "[category] for [niche]", "best [category]", "[Competitor 1] alternatives", "[Competitor 1] vs", "[category] pricing".
2. **Pull autocomplete.** It's free and needs no key:
   ```
   python3 [skill folder]/scripts/run_prompts.py --suggest-queries --seeds "[category] for [niche]" "[Competitor 1] alternatives"
   ```
   With a `config.json` in the working folder, `--suggest-queries --workdir [working folder]` builds the seeds from the config itself. Set `serpapi.gl` and `serpapi.hl` there to the buyers' country and language. Without a shell, fetch `https://suggestqueries.google.com/complete/search?client=firefox&q=[seed]` with your own web tool. It returns JSON: the seed first, then a list of suggestions.
3. **Pick 15 to 20.** Keep what a buyer types before choosing a tool. Drop logins, jobs, salaries, downloads, "free" hunts the founder can't win and anything about a different meaning of the word.
4. **Mix the intents.** About half discovery (category plus niche), a third comparison (alternatives, vs), the rest pricing. Keep [1 to 2] branded queries like "[product] pricing" so the pricing check has something to read. Branded queries stay out of share of voice.
5. **Add the founder's words.** A phrase a customer used on a call goes in as is, shortened to how they'd google it. Mark its source "your words".
6. **If autocomplete can't be reached**, build the list from the founder's words and the patterns above. Say so in the table.

Show the list as a table: number (G1, G2 ...), query, intent (discovery, comparison, pricing), branded or non-branded, source (autocomplete or your words). Get a yes. Save it in `config.json` under `google_queries`, each with `id`, `text`, `intent`, `branded`, `niche` and `source`.

Run no AI Overview check during onboarding. The SerpApi key arrives in question 7.

## The weekly check

Each query runs once a week through SerpApi:

1. `GET https://serpapi.com/search.json?engine=google&q=[query]&gl=[gl]&hl=[hl]&google_domain=[domain]&api_key=[key]`. One search.
2. When the response has `ai_overview` with a `page_token` and no `text_blocks`, Google sent the AI Overview through a separate request. The script fetches it right away with `GET https://serpapi.com/search.json?engine=google_ai_overview&page_token=[token]&api_key=[key]`, because the token expires within 1 minute. It counts as a second search.
3. No `ai_overview` in the response means no AI Overview for that query this week.

Per query the script records:

- AI Overview shown: yes, no or unknown (the block came back with an error or the second request failed)
- Founder mentioned: a name match in the AI Overview text
- Founder cited: the founder's domain among the AI Overview references
- Competitors mentioned, each competitor named in the query left out
- Cited URLs and domains from the AI Overview `references`, typed the same way as chat sources
- For a query with no AI Overview: a suggested swap and how many weeks in a row it had none

## Queries with no AI Overview

Some queries never show one. Each week the report lists them under "No AI Overview for these queries this week", with one suggested swap per query. The swap comes from the same response, so it costs no extra search: first `related_searches`, then `related_questions`. When the response has neither, the script tries free autocomplete for that query. It picks the candidate closest to the original query that isn't already on the list.

The founder approves swaps at the start of the next run. A query with no AI Overview [3] weeks in a row gets flagged for replacement. Change the number under `aio_replace_after_weeks` in `config.json`.

## How lost queries feed the actions

A query is lost when its AI Overview shows and leaves the founder out. Lost queries go through the same source-type map in `references/source-actions.md` and into the same pool as the lost chat prompts, under the same cap of [5] actions a week. YouTube carries AI Overviews far more than ChatGPT, so a YouTube-heavy lost query ranks the video action higher.

## Budget

About 20 queries a week comes to 80 to 90 searches a month. When the second AI Overview request applies to every query, that doubles to about 170 to 180. Both fit inside the free plan's 250 searches a month. The free plan also caps throughput at 50 searches an hour, which one weekly run of 20 queries stays under even with every second request. Only successful searches count. Cached repeats within an hour are free. The script prints the searches each run used.

## What stays unverified

- No live SerpApi call has been made with a real key. The parser was tested on mocked responses shaped like the docs examples.
- SerpApi's docs don't say outright whether the second `google_ai_overview` request counts as a search. The script and the budget assume it does.
- A cached first response may carry an expired `page_token`. The script then records the AI Overview as unknown for that week.
