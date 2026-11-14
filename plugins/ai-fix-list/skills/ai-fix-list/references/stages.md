# Stages, next steps and closing

Last verified: 2026-11-14

Read this when you move a page between stages, record a draft or a send and when you close a page.

Every page sits in one stage: `found`, `drafted`, `sent`, `replied`, `negotiating`, `payment-requested`, `approved`, `live`, `quiet`, `closed`. The script works out the next step for each one, who it's on and by when (a draft waits 2 days for the click, a follow-up has its date, a reply or a price decision 2 to 3 days, an approved placement gets checked 7 days later). In the note, say it plainly for each overdue one: what's late, since when and what you'd do now.

Nothing stays open forever:

- **No reply, two rounds, closed.** A round is the first email plus its three follow-ups. After the first silent round the page goes quiet for 90 days, then gets one fresh email. After the second silent round the script closes it with the reason `no-reply`.
- **Stale on your side.** A draft nobody sent for 14 days and a page waiting 30 days behind the weekly limit both come up as "send it or close it" and "still worth it or close it?". Ask the founder once, then do what they say.
- **Closing by hand.** `fixlist.py --dir [working folder] set [url] --status closed --close-reason [declined|no-reply|not-worth-it|page-gone|filtered|fixed-elsewhere|too-expensive]`. A reason is required, so the report says why it closed.
- Closed and live pages leave the open list. The report keeps them behind their own buttons, so they're still searchable when an owner writes back a year later.

## Recording drafts and sends

Record every draft: `fixlist.py --dir [working folder] set [url] --status drafted --kind [wrong|missing|refresh] --title "[page title]" --cites [n] --contact-name "[name]" --contact-email [address] --contact-source "[where]"` plus `--wrong-line`, `--right-line` and `--proof-url` for Fix or `--proposed-mention`, `--placement` and `--why-readers` for Earn. When the founder says it's sent: `set [url] --status sent --gmail-thread [thread id]`.

Follow-ups go out about 7, 14 and 28 days after the first email, each as a reply in the same thread. After the last one the page goes quiet for 90 days.

When the founder says a follow-up went out: `fixlist.py --dir [working folder] set [url] --followup-sent [n]`. The script moves the next date (a late follow-up pushes the later ones too) and, after the third one, starts the quiet period or closes the page.

A reply moves the page with `set [url] --status [replied|negotiating|payment-requested|approved|live]` or `--status closed --close-reason declined`. A paid offer also takes `--price-asked` and your call in `--recommendation`.
