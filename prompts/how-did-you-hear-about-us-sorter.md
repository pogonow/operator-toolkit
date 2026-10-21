# Sort the "How did you hear about us?" answers

What it's for: you ask every new signup or demo booking where they first heard about you, in a free-text field. After a week or a month you have a pile of messy answers ("chatgpt", "my friend at a podcast", "googled it then saw you in an AI thing"). This prompt sorts them into buckets and tells you what share came from AI tools.

Where it comes from: [5 Things That Get Your SaaS Cited by AI Search, 5 That Don't](https://owneropsguide.substack.com) in The Anti-Grind SaaS Manual.

## What you fill in

- `[signup / demo booking]`: which form the answers come from
- Paste the answers under the prompt, one per line

Change the buckets if your channels are different (add Reddit, a partner, an event), but keep the three AI buckets apart.

## The prompt

Paste this into ChatGPT or Claude, then your answers below it:

```
Below are free-text answers to "How did you first hear about us?" from our [signup / demo booking] form, one per line. Put each answer into exactly one bucket: ChatGPT, Google AI answers (AI Overviews, AI Mode, Gemini), Perplexity or another AI tool, Google search, LinkedIn, Friend or colleague, Podcast or YouTube, Other. If an answer names an AI tool and something else, pick the AI tool and add a note. Return a table with the answer, the bucket and a one-line reason, then a count per bucket and the share of the three AI buckets combined. Flag answers you can't classify instead of guessing.
```

## What to do with the result

Sum it up every week and again every month. If you can, join it to pipeline and conversion by source, so you know whether the AI crowd actually buys or just books calls.
