---
name: ai-shortlist-check
description: Weekly check of whether ChatGPT, Gemini and Google's AI Overviews recommend the founder's SaaS. Onboards the founder once with one question at a time, including what the check will cost, then runs 10 to 25 conversational buyer prompts on ChatGPT and Gemini (through one OpenRouter key) plus 15 to 30 short Google searches for AI Overviews (through SerpApi), counts share of voice next to three competitors, lists the brands and pages that get named instead and turns them into at most five fixes for the week, with an HTML report that grows week by week. Use when the founder asks "does ChatGPT recommend us", "are we in Google's AI Overviews", "are we showing up in AI search", "who does ChatGPT recommend instead of us", "track our AI visibility", "AI search share of voice", "what's my rank in ChatGPT", "how much does AI visibility tracking cost" or wants to see competitors in AI answers. Also fires on "Run AI Shortlist Check for [product]" and /ai-shortlist-check.
---

Last verified: 2026-10-21
From The Anti-Grind SaaS Manual by Paul Ogonowski, https://owneropsguide.substack.com. Source and updates: https://github.com/pogonow/operator-toolkit

# AI Shortlist Check

Every week you run your buyers' questions through ChatGPT, Gemini and Google's AI Overviews, count how often you show up next to three competitors and see who gets named and cited when you don't. Then you get at most five fixes for the week, the ones you control first. This skill gives you no rank from one run, never dresses up a guess as a ChatGPT answer and never builds or publishes anything for you.

## First run

After you install the skill, open a new chat and type "Run AI Shortlist Check for [your product]". Plain text always works. Where your app lists skills in the slash menu, you can also call it as /ai-shortlist-check.

## Onboarding (first session only)

Look for `config.json` in the founder's working folder first. If it's there, read it and skip straight to the run. If it isn't, this session is the onboarding. Open with this line:

> This is a one-time onboarding: [10] short questions, about [20] minutes. Three of them set what the check costs you each month, with the numbers next to every option. I save your answers to config.json so next week we skip straight to the run.

Rules for every question:

- Exactly one question per message, with a progress marker on top ("Question 2 of [10]"). Then stop and wait for the answer.
- A vague answer ("SMBs", "everyone", "the usual tools") gets one follow-up asking for the concrete version. Then move on with what you have.
- Never ask for an API key in the chat.
- Run no AI Overview check during onboarding. The SerpApi key comes at the end.
- Every cost you quote comes from `references/costs.md`. Never round it into a promise.

The questions, in this order:

1. "What's the product and its category, in one line? Add the URL of your pricing page. If pricing is hidden, just say so." You need the pricing to catch answers that quote a wrong or invented price.
2. "Which 3 to 6 niches or use cases could you honestly win?" Follow-up when vague: "Which type of customer signed last month? What job did they buy you for?"
3. "Which 3 competitors do you lose deals to? Names plus their domains."
4. "Does your signup or demo form ask people who found you through ChatGPT what they asked it? Something like a 'What did you ask it?' field." If no, recommend adding it this week, shown when someone picks an AI tool under "How did you hear about us?". Tally does this. Those answers are the best prompts you'll ever track.
5. How many prompts to track. Script below.
6. The prompts themselves. "Paste what you have: answers from that form field, lines from sales-call notes, support tickets. Or tell me to propose them." Read `references/prompt-building.md` first. Build exactly the number from question 5, across discovery, comparison and validation with pricing, about 70% non-branded and 30% branded, kept apart. Show the list as a table and get a yes.
7. What gets tracked, then the Google query list. Script below.
8. The run route. Script below.
9. API route only: weekly runs per prompt. Script below.
10. API route only: the full run. Script below.

After question 10 (or 8 on the other routes) comes the setup: keys, top-up and a small test. Save the answers as `config.json` in the founder's working folder, in the shape of `templates/config.example.json`. If you can't write files, hand it back as a code block to keep.

## Question 5: how many prompts

Read `references/costs.md`. Say this:

> Question 5 of [10]. How many buyer questions should I track? More prompts catch more niches and cost more on the API route, the one I'll recommend in question 8. With 2 weekly runs and a full run every 4 weeks, roughly:
>
> - 10 prompts: about $7 a month
> - 15 prompts: about $11 a month
> - 20 prompts: about $15 a month
> - 25 prompts: about $19 a month
>
> Google's AI Overviews come on top at $0: 20 to 30 Google searches a week fit SerpApi's free plan, a separate pool from these costs. I'd start with 20, or 25 if you sell into more than three niches. If you skip the API later, this number sets your weekly time instead, not money.

Save it as `prompt_count`.

## Question 7: what gets tracked

Say this:

> Question 7 of [10]. Here's what I'll track for you each week.
>
> ChatGPT, because that's where most B2B buyers ask. Gemini, because it's Google's own chat. Both run through one OpenRouter key.
>
> Google's AI Overviews, the answer box anyone sees when they just google. That's a separate surface from Gemini. Even Google's AI Mode and AI Overviews cite the same URLs only 13.7% of the time (Ahrefs). AI Overviews answer short Google searches, so they get their own list of queries. I'll pull it from Google autocomplete next.
>
> Ok?

Propose no other engine. Mention Perplexity only if the founder asks: "Perplexity stays off unless your buyers use it. A 2026 G2 survey puts it at 1 to 3% of B2B buyers. Say the word and I'll add it."

When the founder says ok, read `references/ai-overviews.md` and build the Google query list from autocomplete (`run_prompts.py --suggest-queries`, no key needed) plus the founder's own words. Show 15 to 25 queries as a table, still under "Question 7 of [10]". Ask: "These are the Google searches I'll check once a week for an AI Overview. Good to go? Change any you like." Save them under `google_queries` in `config.json`.

## Question 8: the run route

Say this:

> Question 8 of [10]. How we get the answers each week.
>
> I recommend the API route. A small script asks the real engines, so you see their real answers with the sources they cite. The weekly run is fully automatic. It needs two keys:
>
> 1. OpenRouter for ChatGPT and Gemini. Paid, prepaid credits. The next two questions set how much.
> 2. SerpApi for AI Overviews. Its free plan covers this check.
>
> Do you already have both keys? Missing one or both? I'll walk you through it after the next two questions, about [20] minutes. Rather skip keys altogether? I'll show you what your week looks like then.

- **API route.** Go on to questions 9 and 10.
- **They don't want to deal with keys.** Describe the week concretely: "Each week I answer your prompts with my own web search. The report marks those answers as an approximation, because they show which pages search surfaces and can't tell you what ChatGPT says. Then you paste real ChatGPT answers for your top 5 prompts. You also google your top 5 queries and tell me whether an AI Overview shows and who it names. That's about [15] minutes a week and I hand you the blocks to copy." Let them choose. If this session has no web search either, offer the paste-everything route. Skip questions 9 and 10.

Write the chosen route into `config.json` as `run_route` (`api`, `no-key` or `paste-all`).

## Question 9: weekly runs per prompt

Say this, with the founder's prompt count from question 5 filled in from the table in `references/costs.md`:

> Question 9 of [10]. Each week I run your [N] non-branded prompts. Branded ones ("Is [Product] worth it?") skip the weekly run, since you usually win them and they don't count toward share of voice. They come back in the full run (next question).
>
> How many times should each prompt run per week?
>
> - **2 runs (my recommendation): about $[x] a week.** AI answers repeat the same list of brands less than once in 100 runs (SparkToro). Two answers per prompt give you a weekly number you can read.
> - **1 run (saves about $[y] a month): about $[z] a week.** One answer per prompt is mostly dice. A single week's move means nothing, so you read the 4-week trend only.
>
> The weekly run uses a cheaper OpenAI model for ChatGPT ($0.03 an answer instead of $0.09-0.15). In a test on three prompts it named the same core brands as ChatGPT's own model. The full run keeps checking that.

Save it as `runs_weekly`.

## Question 10: the full run

Say this, with the numbers for the founder's choices from `references/costs.md`:

> Question 10 of [10]. Once in a while I run everything: every prompt, branded ones included, and ChatGPT through its own chat model, the one ChatGPT users get. That's where most of the money goes: ChatGPT's own model pastes the search results into its prompt and costs $0.09-0.15 per answer.
>
> Three choices:
>
> 1. **How often.** Every 4 weeks (my recommendation, $[x] a month all in) or every 8 weeks ($[y] a month). Every 8 weeks checks the cheaper weekly model less often.
> 2. **Branded prompts in the full run.** 2 runs each (recommended) or 1 (saves about $[z] a run).
> 3. **The first full run, today.** Real (3 runs per non-branded prompt, about $[a]) or a test at 1 run each (about $[b]), just to see what comes back. Either one starts the cycle.

Save `full_every_days` (28 or 56), `runs_branded_full` (2 or 1) and `first_run` (`full` or `test`).

## Setup: keys, top-up, a small test

On the API route:

1. **Keys.** Ask where they live (shell, `~/.zshrc`, a `.env` file in the working folder, project settings). Remind them never to paste a key into the chat. If one is missing, walk them through `references/api-keys-setup.md`, OpenRouter first, SerpApi second, one step per message. Wait for "done" each time.
2. **Top-up.** Tell them how much to put on OpenRouter: at least $15, or $20 when they track 25 prompts and chose a real first full run. "$10 is too tight: a full run at 25 prompts costs about $9.30 by itself and OpenRouter takes about 5.5% when you buy credits."
3. **Check.** `run_prompts.py --workdir [working folder] --check-keys` says "set" or "missing" and never prints a key.
4. **Small test.** `run_prompts.py --workdir [working folder] --mode full --runs 1 --limit 3 --tag test --no-history`. Three prompts once on each engine, three Google queries, about $0.30. It prints the real cost per answer. Show that line to the founder.

## Run the prompts

Say this plainly before the first run: Claude can't open ChatGPT and no Claude tool can.

### Before the run

From week two on:

- **Query swaps.** List last run's Google queries that showed no AI Overview with their suggested swaps. Flag any with no AI Overview [3] weeks in a row. Ask which swaps to approve and update `google_queries`.
- **Competitor swap.** If a brand in `other_brands` beat a tracked competitor on share of voice two runs in a row, suggest the swap. The report recounts every older run with the new list, so the history comes back with it.

### API route

```
python3 [skill folder]/scripts/run_prompts.py --workdir [working folder]
```

With no `--mode`, the script picks the run itself: a full run when the last one is `full_every_days` old or there's none yet, a weekly run otherwise. Force one with `--mode full` or `--mode weekly`. For the first run, add `--mode full`, plus `--runs 1` when the founder chose the test.

ChatGPT and Gemini go through OpenRouter (`OPENROUTER_API_KEY`) with web search on. Each Google query runs once through SerpApi (`SERPAPI_API_KEY`). The script reads a `.env` file in the working folder too and skips any engine without a key. It resolves Gemini's Google redirect links to the real pages, strips tracking parameters, saves every answer with its cited links and its cost to `runs/[YYYY-MM-DD].json` and appends rows to `data/history.json`. It prints the run's cost at the end. A crashed run picks up where it stopped when you run the same command the same day. AI Overview details are in `references/ai-overviews.md`.

Read the raw answers for every lost prompt anyway. Name matching misses odd spellings. A logged-in buyer can still see something else.

To test the setup with no API calls, add `--dry-run` in a scratch folder. It writes a fake run marked SYNTHETIC. It refuses to touch a history that holds real runs.

### No-key route

Answer each chat prompt yourself with web search, the way a neutral assistant would answer a buyer. Those answers use engine `proxy` and carry the APPROXIMATION label. Then hand the founder two paste blocks: real ChatGPT answers for the top 5 non-branded prompts and an AI Overview check by hand for the top 5 Google queries. Read `references/manual-routes.md` for the blocks and the rules.

### Paste-everything route

The founder pastes every answer by hand with the same blocks. Be honest that this takes an hour or so. Offer to cut to the [10] prompts and [5] queries closest to buying for this week. On both routes you write the run file and the rows yourself. Read `references/history-format.md` first.

### Copilot (for you, never said unprompted)

Never propose Copilot as an engine. It has no usable public API for this. If the founder insists, read the Copilot part of `references/manual-routes.md`.

## After the run: brands and sources

1. **Brands named instead.** Read the answers for vendor names that aren't the founder or a tracked competitor. Add each one named in 2 or more answers to `other_brands` in `config.json` (name, aliases, domain). Names match case-sensitively, so a brand that's also a plain word (Aspire, Later, Archive) only counts with its capital.
2. **Source types.** The script sorts cited pages into: your site, tracked competitor, other vendor, review site or app store, Reddit or forum, YouTube, docs or help, listicle or comparison, other. Take the most cited pages left as "other" (up to [5]) and ask the founder once what they are. Save the answers in `source_types` (`{"domain": "type"}`) so they stay sorted.

## How to decide

Apply these in order.

1. **Count share of voice across repeated runs.** Runs that name the founder divided by all runs, per engine, non-branded only. On AI Overviews the runs are the queries that showed one. Report no position, because AI tools repeat the same list of brands less than once in 100 runs.
2. **Keep every engine apart.** Only 2.37% of cited URLs show up in three big AI engines at once. A win in one says nothing about another.
3. **Know which run you're reading.** Weekly runs use the cheaper OpenAI model for ChatGPT, full runs ChatGPT's own model. Compare weekly with weekly. A jump on a full-run week can be the model, so check it against the next weekly run before calling it. With 1 weekly run per prompt, mark the week LOW CONFIDENCE and talk about the 4-week trend only.
4. **Won, mixed or lost.** A chat prompt is won when the founder is named in at least half its runs, lost when named in none, mixed in between. A Google query is lost when its AI Overview leaves the founder out. A query with no AI Overview is neither.
5. **For every lost prompt or query, list who got cited instead**, by source type.
6. **Map each lost prompt or query to one action**, from its most cited source type. The map is in `references/source-actions.md`. Reddit, forums, other people's lists and creators are earned work. Mark them SECOND PILE.
7. **Flag pricing.** Flag a quoted price that doesn't match the pricing page from question 1. When pricing is hidden, flag any quoted price, since the AI made it up. The action is always the bot-readable pricing page. Branded prompts carry most of these, so they show up in full runs.
8. **At most [5] actions a week, control pile first.** One action per lost prompt or query, all engines in one pool. Take the ones closest to buying first (discovery for a niche, "moving off [competitor]", "[competitor] alternatives"). When two share a fix, merge them into one action and say so. Earned actions come after every open control action.
9. **Compare with the last run of the same kind and report only what's worth acting on.** That means a non-branded prompt or query moving into or out of lost. A new domain cited in the founder's place on [2] or more prompts. A share of voice move of [10] points or more on one engine (on AI Overviews only with [5] or more queries showing one both weeks). An untracked brand passing a tracked competitor. More pricing flags than last time. Everything else stays in the report. List at most [8] moves.
10. **Skip the myths.** Never suggest llms.txt, schema or FAQ markup, a wire press release or hidden prompts as a fix. None of them moves AI answers and hidden prompts can cost the domain.

## What to hand back

Write `analysis/[YYYY-MM-DD].json` in the working folder:

```json
{
  "changes": ["[a change worth acting on, one sentence]"],
  "pricing_flags": ["\"[prompt]\" on [engine] quoted [what it said]. Your pricing page says [what it says]."],
  "actions": [{"action": "[the one action]", "prompt": "[prompt or query]", "engines": "chatgpt, gemini",
               "cited_instead": "[domain (type), domain (type)]", "pile": "control"}],
  "do_today": "[the first action, as one thing to start today]"
}
```

Then build the report:

```
python3 [skill folder]/scripts/build_report.py --workdir [working folder]
```

It writes `report-[YYYY-MM-DD].html`, which opens offline by double click: share of voice with trend charts (weekly or monthly), the brands named instead, the pages cited when the founder is missing, the actions, every prompt with every run's full answer and clickable links, and every AI Overview. It copies the analysis into `data/history.json`. Without a shell or code tool, hand back the run file and the analysis and tell the founder to bring them next week.

Then reply in chat with this and nothing more:

```
AI Shortlist Check, [date], [weekly | full] run. Answers: [API via OpenRouter and SerpApi | Claude's web search (approximation) plus your pastes | pasted by you]. [N] prompts, [runs] runs each. [N] Google queries, [N] with an AI Overview. Cost: $[x] on OpenRouter.
[APPROXIMATION, SYNTHETIC or LOW CONFIDENCE labels, if any]

Share of voice (non-branded):
- [Engine]: [x]% ([+/- y] points vs [last run of the same kind])

You next to your competitors this run:
- [Product] [x]% | [Competitor 1] [x]% | [Competitor 2] [x]% | [Competitor 3] [x]%
- Not tracked, named most: [Brand] [x]%, [Brand] [x]%

Changes worth acting on:
- [change] (or: Nothing moved enough to act on.)

Lost prompts and queries, who got cited instead:
- "[prompt]" on [engine]: [domain] ([type]), [domain] ([type])

No AI Overview this run (swap to approve next run):
- "[query]" -> "[suggested swap]"

Pricing flags:
- "[prompt]" on [engine] quoted [what it said]. Your pricing page says [what it says].

This week's actions (at most [5]):
1. [Action] for "[prompt]". Cited instead: [domain] ([type]). Pile: [control or earned].

Do today: [the first action, as one thing to start today].
```

When the run's cost is more than 25% over the table in `references/costs.md` for the founder's choices, say so in one line and name the reason (retries, comparison-heavy prompts, a price change).

## Set it to run every week

The check only works weekly. After the first report, offer to schedule it with the one-line prompt "Run AI Shortlist Check for [product] with last week's history". Read `references/weekly-schedule.md` for the options. Describe no menu path you can't see.

## What this skill will not do

- It never invents an answer, a number, a citation or a price. When the data is thin, say "I don't have enough to call this" and name what's missing.
- It gives no rank. When asked "what's my rank in ChatGPT", explain that one run is mostly dice and offer share of voice from repeated runs instead.
- It never presents an approximation as ChatGPT's answer. Those answers keep the APPROXIMATION label in chat and in the report.
- It never buys a tool, signs up for anything, tops up credits, publishes anything or edits the founder's website.
- It never decides what to build. It recommends, the founder decides.
- It never asks for an API key in the chat.

## Where this comes from

- Main post: 5 Things That Get Your SaaS Cited by AI Search, 5 That Don't, on https://owneropsguide.substack.com
- Costs: measured on OpenRouter on 2026-10-21, `references/costs.md`
- Repeat rates: SparkToro and Gumshoe, https://sparktoro.com/blog/new-research-ais-are-highly-inconsistent-when-recommending-brands-or-products-marketers-should-take-care-when-tracking-ai-visibility/
- Engines disagree: Kevin Indig, https://www.growth-memo.com/p/the-consensus-gap
- AI Mode and AI Overviews cite different URLs: Ahrefs, https://ahrefs.com/blog/ai-overviews-vs-ai-mode
- Which AI tools B2B buyers use: G2 buyer survey, 2026
- "Best" lists: Ahrefs, https://ahrefs.com/blog/best-lists-research/
- Vs pages: Siege Media, https://www.siegemedia.com/research/versus-pages
- Review count: G2 and Kevin Indig, https://learn.g2.com/do-more-g2-reviews-mean-more-ai-visibility
- YouTube by engine: Ahrefs, https://ahrefs.com/blog/most-cited-domains-ai-overviews/
- Crawlers and JavaScript: Vercel, https://vercel.com/blog/the-rise-of-the-ai-crawler
- Invented pricing: Growth Unhinged, https://www.growthunhinged.com/p/ai-pricing-visibility-data
- Asking AI-referred users for their prompts: Marie Martens (Tally) on LinkedIn, 18 September 2026
- Tracking prompts from sales calls and tickets: Ethan Smith (Graphite)
- OpenRouter web search: https://openrouter.ai/docs/features/web-search
- SerpApi Google search and AI Overview: https://serpapi.com/search-api, https://serpapi.com/ai-overview
