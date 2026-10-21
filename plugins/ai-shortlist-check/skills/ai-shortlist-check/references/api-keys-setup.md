# Getting the keys for the API route

Last verified: 2026-10-21 against each provider's own docs and real calls. Screens change, so if a label below looks different, follow the URL and look for the closest match.

For Claude: walk the founder through this one step per message. Give the step, wait for "done", then give the next one. Never ask for a key itself and never print one.

You need keys only for the API route, where the weekly run is fully automatic. The no-key route works without them. The API route takes two keys:

1. OpenRouter for ChatGPT and Gemini. Paid, prepaid credits. Top up at least $15, $20 at 25 prompts with a real first full run.
2. SerpApi for Google's AI Overviews. The free plan covers this check.

What it costs depends on three onboarding choices: $7 to $19 a month at 10 to 25 prompts with 2 weekly runs and a full run every 4 weeks. The table and where the money goes are in `costs.md`. The script prints the real cost at the end of every run.

## Key 1: OpenRouter, one key for ChatGPT and Gemini

One account, one top-up, one spending limit, one key. OpenRouter passes your prompt to the OpenAI and Google models with each provider's own web search turned on. The script then reads the sources each answer cites.

1. Go to https://openrouter.ai and sign up.
2. Add credits on the Credits page (https://openrouter.ai/settings/credits). Put on at least $15, or $20 at 25 prompts with a real first full run. $10 is too tight: a full run at 25 prompts costs about $9.30 by itself. OpenRouter charges a 5.5% fee on credit purchases, with a $0.80 minimum (October 2026).
3. Create a key on the Keys page (https://openrouter.ai/settings/keys). Name it `ai-shortlist-check`. Copy it right away.
4. Set a credit limit on that key if the form offers one. OpenRouter is prepaid, so your credit balance is a hard cap on spending either way.
5. Put the key where your setup reads it, under the name `OPENROUTER_API_KEY` (see "Where to put the keys" below).

What the script asks for by default (change it in `config.json` under `openrouter_models`):

| Engine | Model slug | Why this one |
|---|---|---|
| ChatGPT, full run | `openai/gpt-chat-latest` (then `openai/gpt-5.5` if refused) | OpenAI's alias for the chat model ChatGPT uses. $0.09-0.15 an answer |
| ChatGPT, weekly run | `openai/gpt-6-luna` (`openrouter_models_weekly`) | Same OpenAI search, cheaper model. $0.03-0.04 an answer, named the same core brands in a test |
| Gemini | `google/gemini-3.8-flash`, reasoning effort low | Google's current Flash model, with Google Search. ~$0.03 an answer, mostly the grounding fee |

Web search is billed per request on top of tokens, at each provider's own rate. On ChatGPT the search results also land in the prompt as input tokens, which is most of its cost (see `costs.md`).

Only when the founder asks for another engine: Perplexity runs as `perplexity/sonar` and Claude as `anthropic/claude-sonnet-5.5`, both on the same key. Add the engine id to `engines` in `config.json`.

## Key 2: SerpApi, for AI Overviews

SerpApi runs a real Google search for each query and hands back the AI Overview with the links it cites. About 20 queries a week comes to 80 to 90 searches a month. When Google sends the AI Overview through a second request, that one counts too, so the worst case is about 170 to 180. Both fit inside the free plan's 250 searches a month (50 an hour). Paid plans start at $25 a month for 1,000 searches (https://serpapi.com/pricing, October 2026). Only successful searches count.

1. Go to https://serpapi.com and sign up for the free plan.
2. Open your dashboard and copy your private API key (https://serpapi.com/manage-api-key).
3. Put it where your setup reads it, under the name `SERPAPI_API_KEY`.

## Check both, then a small test

The check says "set" or "missing" for each key and never prints one. With a SerpApi key it also shows the searches left this month through SerpApi's account endpoint, which costs no search.

```
python3 [skill folder]/scripts/run_prompts.py --workdir [working folder] --check-keys
python3 [skill folder]/scripts/run_prompts.py --workdir [working folder] --mode full --runs 1 --limit 3 --tag test --no-history
```

The small test asks 3 prompts once on each chat engine and runs 3 Google queries, about $0.30 on OpenRouter and 3 to 6 SerpApi searches. It keeps out of your history and prints the cost per answer.

## Where to put the keys (never in a chat, never in a file you share)

Ask the founder where their keys live today and use that place.

- **Shell profile on a Mac.** Open Terminal and run:
  ```
  echo 'export OPENROUTER_API_KEY="paste-your-key-here"' >> ~/.zshrc
  echo 'export SERPAPI_API_KEY="paste-your-key-here"' >> ~/.zshrc
  source ~/.zshrc
  ```
- **A `.env` file in the working folder.** One line per key: `OPENROUTER_API_KEY=paste-your-key-here`, then `SERPAPI_API_KEY=paste-your-key-here` on the next line. The script reads it on its own. Keep that file out of anything you share or commit.
- **Windows.** Search for "Environment Variables", click New under User variables, enter the name and the key, then open a new terminal.
- **Claude Code or Cowork project settings.** If your setup has a place for environment variables, use the same names there. Describe no menu you can't see.

If a key ever ends up in a chat, a screenshot or a shared doc, delete it and create a new one (OpenRouter Keys page, SerpApi dashboard).

## Already have direct keys?

The script still takes them for the chat engines. It uses them only when `OPENROUTER_API_KEY` isn't set. Any engine without a key gets skipped.

- **OpenAI:** `OPENAI_API_KEY`, from https://platform.openai.com/api-keys. The API is billed separately from a ChatGPT subscription. Web search costs about $10 per 1,000 calls on top of tokens (October 2026).
- **Gemini:** `GEMINI_API_KEY`, from https://aistudio.google.com/apikey. Search grounding needs billing turned on for the project. The paid tier includes 5,000 free search requests a month, then $14 per 1,000 (October 2026). If `GOOGLE_API_KEY` is also set, Google uses that one instead, so keep only one.

The same `--check-keys` command shows which ones are set.
