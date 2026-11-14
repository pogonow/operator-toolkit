# The note and the report

Last verified: 2026-11-14

Read this at the end of every run, when you write the notes file, build the report and hand back the note.

Write `fix-list/notes-[YYYY-MM-DD].json` with four lists (`own_site`, `earned`, `filtered`, `unread`), then run `fixlist.py --dir [working folder] report`. It writes `fix-list/report-[date].html` next to the Shortlist Check report in the same look and links to it: the week in four numbers, the next 8 things waiting on the founder and one table of every page with coloured stages, sorting by page, citations, stage or due date, filters (open, on you, overdue, paid offers, live, closed, Fix or Earn) and a search box. It shows 20 rows at a time, so it reads the same at 50 pages as at 500.

Then hand back this note, with every overdue item said plainly: what's late, since when and what you'd do now.

```
AI Fix List, [date], [product]. Report: fix-list/report-[date].html

Waiting on you: [n] ([n] overdue)
1. [what], [domain], by [date] [OVERDUE since [date]: what I'd do now]
Fix, wrong lines: [n] open ([n] new)
1. [page title], [domain], cited [n]x: "[wrong line]" -> [right line]. Stage: [stage], next: [step] by [date]
Earn, mentions to get: [n] open ([n] new)
1. [page title], [domain], cited [n]x for "[prompt]". Not on this list / out of date. Proposed: "[mention]" in [placement]. Stage: [...]
Paid offers: [domain] asks $[x], my call: [yes / counter at $[ceiling] / no], because [cited in n prompts, Tranco rank n]
First emails this week: [n] of [limit]. [n] more wait as found.
Your own site first: [the inconsistency]
Earned, not email: [Reddit thread / video], cited [n]x
Filtered: [n] ([reasons])
Couldn't open: [URLs], open them and tell me what they say about you
Live: [n] this week, [n] total
```

When nothing is wrong and nothing is missing, say so in one line. Silence reads as "not checked".

Once a month, when the AI Shortlist Check did its full run, add a digest to the note: what went live on each track, which owners went quiet and the new pages since last month.
