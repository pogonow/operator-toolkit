# Setup and keeping the facts current

Last verified: 2026-11-14

Read this on the first run, when `fix-list/facts.md` doesn't exist yet and whenever the facts may be out of date. Ask one question per message and wait for each answer. A scheduled run starts a fresh session, so every answer goes into `fix-list/facts.md` or the ledger settings.

## The six questions

1. "Which pages on your site are the source of truth? Your pricing page for sure, plus any page that says who you're for and what you do better (usually the homepage). I'll read them and write down the facts a third-party page could get wrong." Open them, write `fix-list/facts.md` with prices, plan names, plan limits, the free plan, the main integrations, who the product is for and how you position it, each with the URL that proves it. Then add a **Features** section: every feature the product has, from the features and pricing pages and the help center (`fixlist.py lookup [word]` and the sitemap find the pages), each with the plan it's on and its URL. Mark the core ones, the features a buyer compares tools on, as `core`. Comparison pages and AI answers that say "doesn't have X" are checked against this list. A missing core feature is the claim that knocks a product off a shortlist. Then run `fixlist.py --dir [working folder] facts --add [url] [url]` so the script snapshots those pages. Show the facts and ask: "Anything here that changed in the last year? Old prices and killed features are where most wrong pages come from." Add the old values as "was [old value] until [date]".
2. "In two sentences, what should a list owner say about you? Who it's for, the one thing you do better and one number." Save it under "Mention" in `facts.md`. Every Earn email builds its proposed mention from this, in the owner's format.
3. "Is your Claude connected to the Gmail you'd send these from?" If yes, check that you can search threads and create a draft, then take the founder's name from that account (and their role from the site's about page when it's there) and save both under "Sender". If no, the drafts come to the chat for pasting, ask for the name to sign with and everything else works the same.
4. "When you ask an owner to add you, what can you offer them? A free account to test, a screenshot, a short blurb in their format, nothing." Save under "Offer". Emails offer only that.
5. "If an owner asks for money to add you or keep you on their list, what's the most you'd pay for one placement for a year? A number. 'Never' works too." Run `fixlist.py --dir [working folder] config --ceiling [number]` (0 for never).
6. "How many new first emails a week can you actually read and send? 5, 10, 20 or 30. Follow-ups come on top. You can change it any week by saying 'Fix List limit [n]'." Run `fixlist.py --dir [working folder] config --weekly [n]`.

Then do the first run.

## When your own pages change

Every weekly run starts with `fixlist.py --dir [working folder] facts`. It fetches the source pages fresh and compares them with the last snapshot.

- **Same:** carry on.
- **CHANGED:** read the old and the new snapshot it names. Many changes are noise (a rotating testimonial, a new customer count). When a fact in `facts.md` changed (a price, a plan, a limit, a feature, who you're for), show the founder the old line and the new line and update `facts.md` after their yes, keeping the old value as "was [old value] until [date]".
- **The founder says it first** ("we changed our pricing", "new positioning", "Fix List, update the facts"): run `facts` right away, same steps. A new page to watch: `facts --add [url]`. A page that's gone: `facts --remove [url]`.

After any fact changes, recheck the ledger before new emails go out:

- Every open Fix page: is the "right line" in its draft or its follow-ups still right? Rewrite the drafts that aren't sent yet.
- Every `live` page and every page that named you correctly in the last `candidates-*.json`: it's now quoting the old fact, so it becomes a new Fix page (kind `wrong`, the old value as the wrong line). Tell the founder how many pages that is, since a price change can turn ten good pages into ten wrong ones overnight.
- Every proposed mention in Earn: rewrite the ones that carry the old fact or the old positioning.
