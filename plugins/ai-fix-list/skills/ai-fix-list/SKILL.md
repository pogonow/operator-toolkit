---
name: ai-fix-list
description: Works the pages AI quotes about the founder's SaaS that the founder doesn't own, on two tracks at once. Fix covers pages that get a fact wrong (a price, a plan limit, a feature). Earn covers best X lists, alternatives pages and comparisons AI cites for the founder's buyer questions where the product is missing or out of date. Reads the AI Shortlist Check's runs, filters out poor fits, finds each page's owner, drafts the first email and its follow-ups into Gmail, tracks every page to live or closed and builds a weekly HTML report. Never sends or pays on its own. Needs a setup that can run Python and reach the web (Claude Code or Cowork on your computer). Use when the founder asks "what does AI get wrong about us", "which pages does ChatGPT quote about us", "who do I email to fix this", "get us onto best X lists", "get more mentions in AI answers", "fix list", "AI search outreach", "a blog has our pricing wrong", "should I pay for this listicle spot", "what follow-ups are due", "we changed our pricing" or after any AI Shortlist Check run. Also fires on "Run AI Fix List for [product]" and /ai-fix-list.
---

Last verified: 2026-11-14
Companion post: Get Your SaaS Mentioned by ChatGPT on Pages You Don't Own, [COMPANION POST URL]
From The Anti-Grind SaaS Manual by Paul Ogonowski, https://owneropsguide.substack.com. Source and updates: https://github.com/pogonow/operator-toolkit

# AI Fix List

Most of what AI says about your product comes from pages you don't own: other people's best X lists, competitors' comparison and pricing pages, review sites, Reddit. This skill works those pages on two tracks at the same time. **Fix:** the pages that get a fact about you wrong. **Earn:** the lists and comparisons AI cites for your buyers' questions where you're missing or out of date. Same pages, same owners, same inbox, so it's one weekly loop.

It drafts. You send. It never emails anyone on its own and never agrees to pay for anything.

It runs on top of the AI Shortlist Check, which asks the AI your buyers' questions and saves every page the answers cited. Everything runs through `python3 [skill folder]/scripts/fixlist.py --dir [working folder]`, where the working folder is the AI Shortlist Check folder (the one with `config.json` and `runs/`).

## Before anything

This skill runs a Python script that opens web pages and keeps a ledger on disk. Check that you can run `python3` and reach the web. If you can't (the claude.ai chat, a phone), stop and say: "The Fix List needs Claude Code or Cowork on your computer, because it runs a script and keeps a file of every page between weeks. Install it there and say 'Run AI Fix List for [product]'." Don't walk through the steps as if you ran them.

## Which file to read when

| When | Read |
|---|---|
| First run (no `fix-list/facts.md` yet) or your own pricing or positioning changed | `references/setup.md` |
| Judging new pages, checking a claim about a feature, before any first email, when an owner asks for money | `references/rules.md` |
| Writing any email or follow-up | `references/emails.md` |
| Moving a page between stages, recording a draft or a send, closing a page | `references/stages.md` |
| End of every run | `references/note-and-report.md` |

No `runs/` folder: stop and say "The Fix List works the pages from your AI Shortlist Check runs. Run that first ('Run AI Shortlist Check for [product]'), then come back." Don't guess which pages AI cites.

## Every week

Run `fixlist.py facts` first: it fetches your own pricing and positioning pages fresh and flags any change since last week (what to do then is in `references/setup.md`). Then `fixlist.py due`: every open next step with its date, who it's on and OVERDUE where the date has passed.

1. **Inbox.** Open the Gmail thread of every `sent` page. A reply: read it whole, move the page to its stage, tell the founder what changed. `live` only after you see the fix or the mention on the page.
2. **Follow-ups due.** Draft each one as a reply in the same thread (or into the chat). Record it once the founder sends it.
3. **Quiet period over.** The second and last round: check the page again, then a fresh first email, `live` or `closed`.
4. **New pages.** If a run file is newer than the last `fix-list/candidates-*.json`, run `fixlist.py collect` and judge only the pages not yet in the ledger. No new run: steps 1 to 3 only.
5. **First emails, up to the weekly limit.** Most cited first, Fix and Earn in one queue. The rest waits as `found`.
6. **Report and note.** Build the report, hand back the note.

## The rules in one line each

Full versions in `references/rules.md`.

1. Filter first: vendors' own pages, content farms, link sellers and off-category lists get no email.
2. Wrong means provable from `facts.md`. Opinions stay. A line you can't check gets `fixlist.py lookup` on your own site first, then becomes a fact or a question for the founder. A missing feature you do have goes first in the queue.
3. Your own site first when your own pages disagree with each other.
4. Earn means missing from a cited list in your category or on it but out of date.
5. Every Earn email proposes the exact entry, where it goes and why it helps their readers.
6. A competitor's wrong page gets an email to their founder and the founder's own vs page that week.
7. Find the owner, never guess an email address.
8. Check the contact history before every first email.
9. Price a placement on citations first, authority second, against the founder's ceiling.
10. One email, one ask.

Nothing stays open forever: two silent rounds close a page by themselves, a stale draft or a page stuck behind the limit comes back as "send it or close it" and every close needs a reason (`references/stages.md`).

## Set it to run every week

After the first run, offer the weekly run: in Claude Code or Cowork a scheduled task on the morning after the AI Shortlist Check's weekly run, with the prompt "Run AI Fix List for [product]". Offer it unasked, in the same message as the first report. Elsewhere, a calendar reminder with the same line. The scheduled run prepares the drafts, the report and the note. The founder clicks send.

## What this skill will not do

- Send an email, a form or a LinkedIn message. The founder sends from their own inbox, because an owner fixes a line or adds a tool for a real person much faster than for something that smells like automation.
- Agree to pay or reply to a paid offer without the founder's yes.
- Write to a page that is only unflattering or argue an opinion.
- Offer money, a link swap or a review in exchange for a mention.
- Guess an email address or contact someone who didn't answer less than 3 months ago.
- Post on Reddit, comment on YouTube or write review-site reviews.
- Mark a page live before it opened the page and saw it.
- Invent a citation count, a price or a number in a proposed mention. Every number comes from the run files, the page, `facts.md` or the founder.

## Where this comes from

- The companion post: Get Your SaaS Mentioned by ChatGPT on Pages You Don't Own, [COMPANION POST URL]
- The AI Shortlist Check, the skill this one reads from: https://owneropsguide.substack.com/p/ai-shortlist-check-skill
- Follow-up timing: Backlinko and Pitchbox, 12 million outreach emails (2019), one follow-up lifted replies by 65.8%: https://backlinko.com/email-outreach-study
- Authority lookups: the Tranco list, https://tranco-list.eu
