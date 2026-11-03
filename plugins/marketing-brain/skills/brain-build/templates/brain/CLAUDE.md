# Marketing brain: rules for every AI that reads this repo

## Paste this into your Claude Project instructions (founder and marketer, each in their own company project)

```
Before you answer anything about our marketing, sales, customers or brand, read CLAUDE.md in the [company]-marketing-brain repo and the files it points to. Use them as the context for every answer.
When something I tell you or something you figured out isn't in the brain yet, end your answer with a block that starts with the exact line "🧠 Brain update" and lists the file, the lines to add, why and based on what. Use that exact heading every time so the weekly sweep can find it.
If the brain can't answer my question, don't guess. Say it isn't in the brain and add the question to open-questions.md for the founder.
```

## Read order

1. `brain.yml`: which mode we're in (handoff or digest) and who's who.
2. `positioning/` and `customers/`: who we sell to and what we believe.
3. `voice/`: how we sound. `voice/founder.md` only when writing in the founder's name.
4. Then whatever folder the question is about: `proof/`, `gtm-motions/`, `experiments/`, `tools/`, `processes/`, `skills/`, `brand/`.

Every content file (not the READMEs or open-questions.md) has a header with `owner`, `last_verified` and `sources`. A file older than 60 days: mention it once and suggest a refresh.

## Who may change what

- `owner: founder`: only the founder changes it. Anyone else proposes, never edits.
- `owner: shared`: depends on the mode.

**Mode `handoff`** (the first two weeks with a new hire): every change from the marketer is a proposal, one topic per proposal: what changes, why, based on what.

- If you can push to GitHub (Claude Code, Cowork with git): open a pull request on a branch named `proposal/[short-topic]` using the PR template.
- If you can only read the repo (a claude.ai Project with GitHub connected is read-only): write a "Proposed change" block (file, the exact new lines, why, based on what) and tell the person to open the file on github.com, click the pencil, paste it and pick "Create a new branch and start a pull request".

The founder reviews them before the daily talk. Use the gates below to label each one, even in handoff mode and judge the gate yourself instead of trusting the checkbox in the PR.

**Mode `digest`** (after that), the gates:

- **Minor, goes straight in:** a typo or formatting, a source added to an existing line, a new quote in `customers/their-words.md`, a new entry in `experiments/`, a new process written from a recording.
- **Significant, always waits for the founder:** anything in a founder-only file, anything in `positioning/` or `voice/`, anything about pricing, anything that deletes or rewrites an existing line, a new belief.

When in doubt, treat it as significant.

## Never in this repo

Passwords, API keys, logins, tokens, webhook URLs, customers' personal data (emails, phone numbers), exact bank or revenue figures beyond the ranges in `proof/numbers.md`.

If someone pastes one: don't write it anywhere, say it's now sitting in the chat history, tell them to change that password or regenerate that key or webhook and use the tool's own invite-user flow for access instead.

## Brain updates: catch it while you work

Nobody remembers to update a knowledge base later, so catch it in the chat where it comes up. When a chat surfaces something the brain doesn't hold yet (a new competitor, a customer's words, a test result, why something flopped, a decision, a new belief), end your answer with:

```
🧠 Brain update
File: [path]
Add: [the exact lines]
Why: [one line]
Based on: [call, report, test, chat, with date]
```

Always that exact first line, `🧠 Brain update`, so the weekly sweep and past-chat search can find every one of them.

- **If you can write to the repo** (Claude Code, Cowork with git): don't just show the block. Save it as `inbox/YYYY-MM-DD-[short-topic].md`, commit it on a branch `inbox/[short-topic]` and open a pull request. The gates below still decide what goes in.
- **If you can only read it** (a claude.ai Project): show the block. The person can paste it on github.com right away (see "Proposed change" above) or leave it: the Monday Brain Bot message asks Claude to collect every block from the week's chats in one go.

Before you finish a conversation about marketing, sales, customers or the brand, check once whether anything new came up that you didn't flag yet. Skip it if the chat had nothing new.

## Open questions

When the brain can't answer something, add one line to `open-questions.md`: date, the question, who asked. The founder answers them in the daily talk. The answer goes into the right file and the line gets deleted.
