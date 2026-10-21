# Setting the weekly run

Last verified: 2026-10-21

Read this after the first report, when you offer to schedule the check.

The check only works weekly. After the first report, offer to schedule it.

- In Claude.ai or Cowork: if scheduled tasks are available to you, offer to create a weekly one with this prompt: "Run AI Shortlist Check for [product] with last week's history". Describe no menu path you can't see.
- In Claude Code: offer the built-in scheduling if this setup has it. Otherwise give a cron line for Monday morning:

```
0 7 * * 1 cd [working folder] && python3 [skill folder]/scripts/run_prompts.py --workdir . && python3 [skill folder]/scripts/build_report.py --workdir .
```

  The script decides on its own whether this week is a weekly run or a full run (every `full_every_days`, set at onboarding). Cron collects the answers, runs the Google queries once through SerpApi and builds the numbers. The brands named instead, the source types, the actions and the query swaps still need a session, so the founder opens Claude with the one-line prompt after it ran. Swaps the founder approves take effect on the next run.
- Fallback: a calendar reminder every Monday with that same one-line prompt.
