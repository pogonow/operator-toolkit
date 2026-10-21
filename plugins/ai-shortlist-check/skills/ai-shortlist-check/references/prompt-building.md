# Building the prompt lists

Last verified: 2026-10-20

Read this before you build, pull out or propose a single prompt in onboarding question 5. You build two lists. List (a) holds the conversational prompts for ChatGPT and Gemini. List (b) holds the short Google queries for AI Overviews, built in question 6. Most of this file is about list (a). List (b) has its own section at the end.

## Why the prompts have to sound like a person

Buyers talk to ChatGPT in full sentences, in the first person, with their situation inside the prompt: team size, the tool they use today, the thing that annoys them, the budget they have. The engine uses all of that to pick who it names. A prompt like "best CRM software" tests a question almost nobody asks.

The best example comes from Tally. Tally asks people who found it through an AI tool what they actually asked. One answer they shared: "Google forms that doesn't look like poop". A competitor and a pain in seven words. No keyword tool would ever produce it. (Marie Martens, Tally's co-founder, on LinkedIn, 18 September 2026.)

Ethan Smith of Graphite says the same from the tracking side: track the long prompts you hear on sales calls and read in support tickets. Prompts that ChatGPT or a keyword tool invents for you test a buyer who doesn't exist.

## Where the prompts come from, in this order

1. **The founder's signup or demo form.** A "What did you ask it?" field, shown when someone picks ChatGPT or another AI tool under "How did you hear about us?". These are real prompts from real buyers. Use them close to word for word. If the founder doesn't have the field, recommend adding it this week. It takes about [5] minutes in most form tools and it feeds this check forever.
2. **Sales-call notes and support tickets.** Look for the moment the buyer explains their situation: "we're 12 people", "we use HubSpot", "our current tool keeps double-booking". Keep their words. Turn the situation into a question they'd ask an AI.
3. **Your own proposals.** Only to fill the gaps the first two leave. Build them from the founder's niches, competitors and the jobs customers bought the product for.

Mark each prompt's source in the list you show back, so the founder sees how much of it is real buyer language.

## Three intents, 2 to 3 phrasings each

Cover all three. Write 2 to 3 phrasings per intent and per niche that matters, each with the buyer's context inside (team size, use case, constraint, current tool).

**Discovery.** The buyer doesn't know the options yet.
- "We're a [size] [type of company] using [tool]. What's the best [category] for [job]?"
- "I run a [niche] business with [size] people. We keep [pain in the buyer's words]. What should we use?"
- "What's a good [category] for a [niche] team that needs [constraint, like an integration or a budget]?"

**Comparison.** The buyer has names and is choosing.
- "Compare [product] and [competitor]. Which one is better for a team like ours?"
- "We're moving off [competitor] because [reason]. What should we switch to?"
- "Is there something like [competitor] that [does the thing it doesn't]?"

**Validation, pricing included.** The buyer is close to buying and checking.
- "Is [product] worth it for a [niche] company? How much does it cost?"
- "What do people complain about with [product]?"
- "Does [product] work with [tool]? We can't switch away from [tool]."

## Rules for the list

- **Aim for 20 to 30 prompts.** Fewer than 15 makes share of voice jumpy. More than 30 costs time without telling you much more.
- **Keyword-style prompts are a small minority.** At most [3] in the whole list, kept only if the founder's form or calls show buyers really type that way.
- **Keep branded and non-branded apart.** A prompt that names the founder's product is branded. Share of voice is counted on non-branded prompts only, because a buyer who names you already found you. The script marks any prompt that names the product as branded, even when the list says otherwise.
- **Branded prompts are conversational too.** "[product] pricing" becomes "Is [product] worth it for a [niche] company? How much does it cost?" Keep at least one branded pricing prompt, so the pricing check has something to read.
- **Competitors named in the prompt don't count for that prompt.** "We're moving off [competitor]..." names that competitor because the buyer did. The script leaves it out of that competitor's share of voice for that prompt.
- **Keep the founder's real spelling.** Typos and slang from the form stay in. Fix nothing that a buyer would really type.
- **One niche per prompt.** It keeps the won and lost table readable.

## How to show the list back

A table, one row per prompt: number, the prompt, intent, branded or non-branded, niche, source. Under it, one line with the count per intent and the share of prompts from real buyer language. Then ask for a yes. Change what the founder changes and show it once more only if more than a few rows moved.

In `config.json` each prompt carries `id`, `text`, `intent`, `branded`, `niche` and `source` (see `templates/config.example.json`).

## List (b): Google queries for AI Overviews

AI Overviews answer Google searches, so they get short queries the way buyers google. A chat prompt there tests a search nobody types. Build this list in question 6, after the founder said ok to the engines.

- **15 to 20 queries**, three to six words each.
- **How buyers google:** "influencer platform for shopify brands", "[competitor] alternatives", "[competitor] vs [competitor]", "[category] pricing", "[category] for [niche]".
- **Source them from Google autocomplete** (free, no key), seeded with the category, the niches and the competitors. Add the founder's own words from calls and tickets, shortened to how a buyer would google them.
- **Mix the intents:** about half discovery, a third comparison, the rest pricing. Keep [1 to 2] branded queries so the pricing check has something to read.
- **Show it as its own table** (G1, G2 ...) with a source column and get a yes.

The full steps, the `--suggest-queries` command and the weekly SerpApi check are in `references/ai-overviews.md`.
