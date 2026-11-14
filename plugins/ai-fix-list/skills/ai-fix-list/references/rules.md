# How to decide

Last verified: 2026-11-14

Read this before you judge new pages, before any first email and whenever an owner asks for money. The short version is in SKILL.md, this is the full rule set.

1. **Filter first.** Skip it and list under `filtered` with the reason: a vendor's own alternatives or comparison page that leaves you out (their marketing), thin auto-generated directories and content farms (no author, a page per tool, text that reads machine-made), link sellers and private blog networks, pages about another category or a buyer you don't serve. Reddit, forums and YouTube aren't for email either: list them under `earned`.
2. **Fix: wrong means provable.** A line is wrong only when a page in `facts.md` proves it: a price, a limit, a plan, a feature you have or killed, an integration. "Their widgets look generic" or "it's pricey" is an opinion and it stays. A line you can't check against `facts.md` (a plan you don't recognise, a feature that isn't on the list) gets looked up first: `fixlist.py --dir [working folder] lookup [two or three words from the claim]` searches your own site, help center and docs. Found: add the fact to `facts.md` with its URL and say "added to facts" in the note, then judge the line. Not found: it goes to the founder as a question, not into an email.
   A page that says you don't have a feature you do have (or don't have a `core` one) is the most expensive kind of wrong. It knocks you off shortlists before a buyer ever reaches your site, so it goes first in the queue, before a wrong price.
3. **Your own site first.** When a wrong line on someone else's page matches something on your own site (one page says 18 integrations, another says 35), the first fix is yours. Say so before any email goes out.
4. **Earn: missing or out of date.** Kind `missing`: the page is cited for a buyer prompt that doesn't name you, it's a best X list, an alternatives page or a comparison and you aren't on it. Say it flat: "Not on this list." Kind `refresh`: you're on it, but as a one-liner, under an old name or with last year's plans, so ask for a better mention.
5. **Every Earn email proposes a specific mention.** The exact text in their format (two sentences built from "Mention" in `facts.md`, the length and tone of their other entries), where it goes on their page (which section, next to which tool) and why it helps their readers (the buyer their list is for who's missing an option). Save all three with `--proposed-mention`, `--placement` and `--why-readers`.
6. **A competitor's page gets two moves.** Email their founder with the correction (a wrong price on their own comparison makes them look sloppy too). And tell the founder to publish or update their own honest vs page that week. This skill drafts the email, not the vs page.
7. **Find the owner, never guess the email.** The author's byline, the About or contact page, the site's founder on LinkedIn. Save where it came from with `--contact-source`. No email found: the contact form or a LinkedIn message and say which. Never build an address from a pattern.
8. **History before every first email.** Search Gmail for the domain and the person. They replied before: write in that thread. You wrote and they never answered less than 3 months ago: `set [url] --status quiet --quiet-until [3 months after that email]`.
9. **Price a placement on citations first, authority second.** When an owner asks for money, move the page to `payment-requested` with `--price-asked` and your call in `--recommendation`:
   - Not cited in any of your buyer prompts in the last [2] runs (compare the last two `candidates-*.json`, run `collect --run runs/[older date].json` if one is missing): no, whatever the price.
   - Cited and at or under the ceiling: yes.
   - Cited and up to twice the ceiling: counter at the ceiling.
   - Over twice the ceiling: a polite no.
   - Authority adjusts, it doesn't decide. `fixlist.py authority [domain]` gives the free Tranco rank or use the founder's own Domain Rating. A domain outside the top million asking for more than half the ceiling gets a counter, not a yes.
   - Nobody has published whether AI treats a placement marked "sponsored" differently. Say so if asked.
   Then `negotiating` while you go back and forth, `approved` once the founder says yes, `live` once you see it on the page.
10. **One email, one ask.** One wrong line with the right line and the proof or one proposed mention. No link request, no "while I have you".
