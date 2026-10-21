# history.json format

Last verified: 2026-10-21

Read this when you write rows by hand (the no-key route, the paste-everything route and any pasted answers on the API route) or when you add the week entry with the actions. On the API route, `scripts/run_prompts.py` writes the rows for you.

The file lives at `[working folder]/data/history.json`. Never delete old rows. A rerun on the same date replaces the rows with the same date, engine, prompt and mode.

```json
{
  "schema": 1,
  "meta": {
    "product": "[Product]",
    "product_domain": "[product.com]",
    "category": "[category]",
    "pricing": "[pricing page URL, or: hidden]",
    "competitors": ["[Competitor 1]", "[Competitor 2]", "[Competitor 3]"]
  },
  "rows": [
    {
      "date": "[YYYY-MM-DD]",
      "mode": "[api | manual | proxy | synthetic]",
      "engine": "[chatgpt | gemini | ai_overviews | proxy | an engine added on request]",
      "engine_label": "[how the answer was produced, e.g. ChatGPT via OpenRouter (openai/gpt-chat-latest, web search)]",
      "via": "[openrouter | direct | serpapi | (empty for pasted and proxy rows)]",
      "prompt_id": "[P1]",
      "prompt": "[prompt text]",
      "branded": false,
      "intent": "[discovery | comparison | validation | pricing]",
      "niche": "[niche]",
      "runs": 3,
      "mentioned": [true, false, true],
      "position": ["[named 2nd of 3 tracked brands in this run]", "not named", "[...]"],
      "competitors_mentioned": {"[Competitor 1]": 2, "[Competitor 2]": 0, "[Competitor 3]": 1},
      "cited_domains": ["[g2.com]", "[bestlists.example]"],
      "cited_sources": [{"domain": "[g2.com]", "type": "[review site]", "count": 2, "example": "[URL]"}],
      "price_mentions": ["[sentence that quotes a price for the product]"],
      "price_flag": "[null or what was quoted and what the pricing page says]",
      "proxy": false,
      "synthetic": false
    },
    {
      "date": "[YYYY-MM-DD]",
      "mode": "[api | manual | synthetic]",
      "engine": "ai_overviews",
      "engine_label": "[Google AI Overviews via SerpApi (google.com, gl=us, hl=en)]",
      "via": "[serpapi | (empty for pasted rows)]",
      "prompt_id": "[G1]",
      "prompt": "[short Google query]",
      "branded": false,
      "intent": "[discovery | comparison | pricing]",
      "niche": "[niche]",
      "aio_shown": true,
      "runs": 1,
      "mentioned": [false],
      "position": ["not named"],
      "cited_founder": false,
      "competitors_mentioned": {"[Competitor 1]": 1, "[Competitor 2]": 0, "[Competitor 3]": null},
      "cited_domains": ["[g2.com]"],
      "cited_sources": [{"domain": "[g2.com]", "type": "[review site]", "count": 1, "example": "[URL]"}],
      "price_mentions": [],
      "price_flag": null,
      "no_aio_streak": 0,
      "alternatives": [],
      "suggested_swap": null,
      "serpapi_searches": 2,
      "aio_error": null,
      "proxy": false,
      "synthetic": false
    }
  ],
  "weeks": [
    {
      "date": "[YYYY-MM-DD]",
      "mode": "[api | no-key | paste-all]",
      "engines": ["[chatgpt]", "[gemini]", "[ai_overviews]"],
      "runs_per_prompt": 3,
      "synthetic": false,
      "changes": ["[a change worth acting on that the report cannot compute, in one sentence]"],
      "actions": [
        {
          "prompt": "[prompt or Google query]",
          "engine": "[chatgpt]",
          "cited_instead": "[domain, domain]",
          "source_type": "[listicle]",
          "action": "[the one action, in one line]",
          "pile": "[control | earned]"
        }
      ],
      "do_today": "[the first action, as one thing to do today]"
    }
  ]
}
```

Rules for the fields:

- `mentioned` holds one entry per run. `runs` equals its length. One run is low confidence.
- `position` is raw data per run. Never add it up into a rank.
- `competitors_mentioned` holds null for a competitor named in the prompt itself ("We're moving off [Competitor 1] because..."), so the prompt does not count toward that competitor.
- `branded` is true for any prompt that names the product, whatever the config says.
- `cited_sources[].type` is one of: your site, tracked competitor, other vendor, review site or app store, Reddit or forum, YouTube, docs or help, listicle or comparison, other, or a type the founder set in `source_types`.
- Proxy rows use engine `proxy` and mode `proxy`, so they never mix with a real engine's numbers.
- Pasted answers use the real engine id and mode `manual`. An engine the founder insisted on that has no id above gets its own lowercase id (the report capitalises it).
- A `price_flag` stays null unless an answer quoted a wrong price or any price while the founder's pricing is hidden.

Rules for AI Overview rows (engine `ai_overviews`):

- One row per Google query per week. `runs` is 1 when an AI Overview showed and 0 when none showed, so a query with no AI Overview never counts toward share of voice.
- `aio_shown` is true, false or null. Null means the block came back with an error or the second request failed. `aio_error` says why. A null week doesn't count toward `no_aio_streak`.
- `mentioned` holds one entry, a name match in the AI Overview text. `cited_founder` is true when the founder's domain is among the AI Overview references.
- `cited_sources` come from the AI Overview references.
- `no_aio_streak` counts the weeks in a row, this one included, with no AI Overview. At `aio_replace_after_weeks` (default [3]) the query is flagged for replacement.
- `alternatives` lists candidate swaps from the same response (`related_searches`, then `related_questions`, then free autocomplete). `suggested_swap` holds the pick as `{"query": "[query]", "from": "[related_searches | related_questions | autocomplete]"}`.
- `serpapi_searches` is 1. It is 2 when the AI Overview needed the second request.
- Pasted AI Overview checks (no-key route) use mode `manual`. Set `aio_shown` from what the founder saw and leave `serpapi_searches` at 0.

## The run file the report reads

`build_report.py` builds the report from `runs/[YYYY-MM-DD].json`, not from history, so every answer and every link stays clickable and old runs can be recounted. On the API route the script writes it. On the no-key and paste-everything routes, write it yourself in this shape (proxy answers use engine `proxy`):

```json
{
  "date": "[YYYY-MM-DD]", "run_mode": "[weekly | full]", "runs_per_prompt": 2, "runs_branded": 2,
  "synthetic": false, "serpapi_searches": 0, "cost_usd": {},
  "results": [
    {"engine": "[chatgpt | gemini | proxy]", "prompt_id": "[P1]", "prompt": "[prompt text]",
     "runs": [{"answer": "[full answer text]", "cited_urls": ["[full URL]"], "model": "[pasted from ChatGPT | claude web search]", "error": null}]},
    {"engine": "ai_overviews", "prompt_id": "[G1]", "prompt": "[query]", "aio_shown": true,
     "answer": "[AI Overview text]", "cited_urls": ["[full URL]"], "alternatives": []}
  ]
}
```

The `weeks` entry for each date holds `run_mode`, `runs_per_prompt` and `cost_usd` (written by the script) and the analysis (`changes`, `pricing_flags`, `actions`, `do_today`), which `build_report.py` copies in from `analysis/[YYYY-MM-DD].json`. The script uses the last `run_mode: "full"` entry to decide when the next full run is due.
