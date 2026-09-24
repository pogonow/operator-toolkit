---
name: deep-research
description: Run a structured research project the way a strategy consultant or BizOps lead would. Gathers context first, proposes a research plan and waits for sign-off, works primary sources before secondary ones, then delivers a pyramid-structured report (answer first) with in-text citations, a confidence call and a source table. Use when someone asks for a deep dive, research, a competitive analysis, a market or pricing scan, a landing page or funnel teardown, a playbook for how others do X, market sizing, "what do we know about company X", "what do the experts think", "find the best authors first" or any question that needs more than a few searches and a sourced answer.
license: MIT
argument-hint: the question to research (one sentence is enough), optionally quick / standard / deep
---

# Deep Research

Talk to the user in their language. The report ships in English unless the user asks for another language. Write plainly: answer first, no filler, no hedging a claim the evidence supports.

Purpose: answer one business question with evidence a skeptical reader can check. The workflow copies a strategy consultant: define the question, agree the plan, collect evidence from the best sources, lead with the answer.

The failure this skill exists to prevent, in [Kyle Poyar's words](https://www.growthunhinged.com/p/claude-skills-gtm-and-pricing): AI research "makes frustrating intern-level mistakes. It'll sometimes over-index on one blog post, treat a Reddit thread as data, or waste all your tokens on research." Every step below is a guard against one of those three.

## Input

The argument is the question. Parse it for:

- **The question itself.** If it is a topic ("DinoCo") and not a question, propose the question in the Scope slot of the question round, as a clickable option the user accepts or rewrites.
- **Route**, if the user named one ("experts first", "find the authors first", "start with the data"). If not, the question round asks.
- **Mode**, if given: `quick`, `standard` or `deep`. If not given, pick it at the end of Step 1 context gathering (it decides whether the question round happens) and say why in one line.
- **Files or links** the user attached. Read them before anything else, they are context and often the best source.

## Modes (scale effort to the question)

| Mode | When | Plan gate | Budget | Parallelism |
|---|---|---|---|---|
| quick | One fact or a small comparison ("what does X charge", "who founded Y") | No questions, no wait. Assumptions and the plan in 3 lines at the top of the answer | 5-15 tool calls | none |
| standard | A real question with 3-5 parts (competitive scan, pricing teardown, playbook) | Full plan, wait for sign-off | 20-50 tool calls | parallel searches |
| deep | 4+ branches that each need 10+ calls (many entities, a whole market). An important decision alone does not make it deep | Full plan, wait for sign-off | 3-5 subagents, 15-25 calls each | subagents per branch |

Budget counts web searches and page fetches during collection. It is a ceiling, not a target. Setup (reading context), the author scan (15-25 calls of its own) and the Step 5 check are outside it. Stop a branch when the last 3-4 searches added nothing new and say so in Method and limits.

## Step 1: Gather context before asking anything

Pull what is already known, so the user only answers what you cannot find:

1. Read what this session already holds about the user: the conversation, any memory or profile the agent keeps, project instructions and connected files. Look for the user's company, market and role, since they shape the question.
2. Look for earlier reports on the same topic in the research folder (`research/` in the working directory or wherever the user keeps them). If one exists, read it, the new run refreshes and extends it instead of starting from zero. Say which one you found.
3. Read every attached file and link.

If memory, project files or the research folder cannot be reached, say so in one line and continue. Do not invent what those files would have said, work from what is actually in the session (the chat, the prompt, attached files).

No web research before the question round. The one exception: up to 3 searches to understand a topic or company you do not recognize, so the proposed question makes sense.

Then pick the mode (see the table) and say it in one line.

### Pick the route, then let the user choose it

- **Evidence-first** (fits fact questions): prices, market size, who does what, what changed, how a funnel is built. The answer lives in primary data, so go straight to it.
- **Experts-first** (fits judgment questions): "how should I think about X", "what is the right way to do Y", strategy, pricing philosophy, org design, anything where the answer is a call made by people who have done it. It runs in two stages: first find who is worth listening to, then research what they think.
- **Mixing is normal.** An experts-first run still checks the experts' principle against primary evidence in the user's market (competitor pricing pages, for example). An evidence-first run can quote an expert to interpret the data. The route decides where you START and what the report is built around.

The route is always the user's call. It is asked in the question round and the user never has to remember to type it. Recommend the one that fits the question and put it first. Only two cases skip the ask: the user already named a route in the argument ("experts first", "find the authors first", "start with the data") or quick mode.

For a bare topic, propose the question first. A bare topic is never quick mode, it always gets the question round. Pick the angle that serves what the session says the user is working on (a competitor of their product, a client's market). When the session gives an angle, that angle is option 1 (recommended) and option 2 is the same question with a wider or narrower scope. With nothing to go on, option 1 is a plain profile and option 2 one alternative angle. The proposed question stays one question: the scope rides in it as a clause, not as a second question.

### Ask with the question tool

Quick mode skips all asking: state the assumptions at the top of the answer instead.

Everything else asks through the question tool (AskUserQuestion in Claude Code and Cowork or whatever question tool your agent has), so the user answers with clicks and types only where they want to. Its limits shape the round: max 4 questions per call, 2-4 options per question, a free-text "Other" is added to every question automatically, multiSelect for questions where several answers can hold. Only two questions get a recommended option (first, marked "(Recommended)" in the user's language): the route and the proposed question for a bare topic. Decision and current bet options stay unranked. Ask in the user's language.

"The session" means everything visible in this conversation: the chat, the prompt, loaded context, the memory snapshot, installed skills. Where something in it supports a guess, the guess becomes an option to click. When nothing supports a guess, offer 2-3 plausible readings and let "Other" catch the rest. Never invent the user's current bet as the recommended option, offer it as readings to pick from.

**Round 1, one call, up to 4 questions, drop any already answered:**

```
keep these questions and their order, wording may be translated
1. Route: where do I start? Options: the recommended route first, the other route, "mixed". Skip if the user already named a route.
2. Decision: what will you decide or do with this answer? Options: 2-3 guessed decisions. The reader (you only, a client, co-founders) rides in the option text when it matters.
3. Current bet: what do you think the answer is right now? Options: 2-3 plausible answers, including the contrarian one.
4. Scope: geography, segment, time window. For a bare topic this slot carries the proposed question with its scope written in, plus one alternative angle.
```

Access (paid databases, logged-in browser sessions, internal data, people to ask) is not asked: it goes into the plan's Assumptions as "public web only, no internal data", where the user can shift it in one word.

**Round 2, experts-first and mixed only, one call right after round 1:**

```
keep these questions, wording may be translated
1. Authors you know: anyone I must include or leave out? Options: "No, find them yourself" (first), "Yes, I will name them" (the names come through Other). Any author the session links to the user (a newsletter they read, an author a skill of theirs cites) may be offered as an option.
2. What to pull from the authors? multiSelect. Options: "their own numbers and cases", "the conditions when their advice holds", "where they changed their mind", "concrete how-to steps".
```

Authors the user names go through the same trust scoring as the rest and always appear on the roster, labeled "your pick" with their score, so the user sees how they rate. Authors the user excludes are not scored, not on the roster and not used for positions. The plan names them once under "Left out at your request". If one of them was the only voice for the dissent, the plan says so and names counter-evidence instead.

If a clicked option needs text that did not come ("Yes, I will name them" or "Go with changes" without names or changes), ask for it in one plain line. That is a follow-up, not a re-ask.

**Mixed route:** run round 2 and the author scan as for experts-first. The issue tree then carries expert branches and evidence branches side by side. The report keeps both the "Who thinks what" section and the evidence findings.

What to pull from the authors becomes the capture list in Stage 2 and a line in the plan.

If the question tool is not available (claude.ai chat, a headless run), ask the same items as plain numbered text in one message, the options written as short suggestions.

If the user answers nothing or says they will not answer questions, state each assumption in one line and move on. Never re-ask.

### Experts-first: author scan after the answers

Run the author scan (Stage 1 under "Experts-first route" in Step 3) after both rounds and before the plan. The roster then fits the scope, includes the user's picks and the dissenter is chosen against the user's current bet. The roster goes to the user inside the plan, one sign-off for both.

## Step 2: Research plan, then STOP for sign-off

Write the plan in this shape, in the user's language (the field labels may be translated). Keep it under one screen, the roster table excepted.

```
keep these fields in this order, fill the brackets
**Key question:** [one question, specific and time-bound, whose answer is the thing the user needs]
**Decision it feeds:** [one line]
**Day-one hypothesis:** [the answer we expect, to be proven or killed]
**Mode:** [quick / standard / deep], because [one line]

**Issue tree (3-5 branches, no overlaps, together they answer the key question):**
1. [Sub-question] → proves/kills the hypothesis if [what we would need to see] → sources: [named sources, tier 1 first]
2. ...

**Route:** [evidence-first / experts-first / mixed], as the user chose
**What to pull from the authors (experts-first only):** [the user's picks from round 2]
**Expert roster (experts-first only, 5-8 people, the user's picks labeled "your pick"):**
| Author | Criteria met (of the 6) and the concrete proof | Where they publish | Likely stance / school |

**Out of scope:** [what we will not look at]
**Assumptions:** [one line each, so the user can shift any in one word]
**Deliverable:** [report shape, rough length, anything extra such as a comparison table]
```

Test the tree before sending: the branches must not overlap and answering all of them must answer the key question. If a branch cannot change the answer, cut it.

**Gate.** In standard and deep mode, show the plan, then ask for sign-off with the question tool: "Go" (first), "Go with changes" (the changes come through Other: drop or add an author, a branch, what to look for), "Stop". Without the tool, ask in one line. Do not start collecting before the answer. The user reviews between stages on purpose. Apply changes and go without re-sending the plan unless the change is large.

Exception: when another skill or an unattended run calls this skill, there is no one to approve. Put the plan at the top of the report under "Plan (not reviewed)" and proceed.

A branch that needs data the user cannot give (internal numbers with Access "none") moves out of the tree into Assumptions and into "What would change the answer".

**When reality breaks the plan mid-collection** (the sample the plan assumed does not exist, a key source is gone, an approved author never wrote on the topic): make the smallest change that keeps the key question answerable, log it in Method and limits and name it in the chat reply. If the change alters the key question itself, stop and ask.

## Step 3: Collect evidence, primary sources first

### Source tiers

```
paste exactly, do not reword
TIER 1, PRIMARY: the entity itself or the original data.
  Company: its website, pricing page (and its Wayback Machine history), docs and help center, changelog, job postings, investor letters, S-1 / 10-K / 10-Q, earnings call transcripts, founder interviews and podcasts, its own case studies (as claims, not proof).
  Registries and official data: company registries (Companies House, SEC EDGAR and national equivalents), patent offices, national statistics offices, Eurostat, central banks, court records.
  Original datasets and surveys with a published method.
  Raw customer voice: G2, Capterra, Trustpilot, app store reviews, read as individual data points, never as a statistic.
TIER 2, SECONDARY WITH A METHOD: analyst reports that show their method, established business press reporting (not rewriting), practitioner newsletters that publish their own data, academic papers.
  A company's own blog or announcement counts here only for what it says about itself (what it launched, what it charges, why it changed), labeled self-claim.
TIER 3, CONTEXT ONLY: vendor content marketing about the market or about other companies, listicles, "top 10" posts, SEO pages, AI-generated summaries, Reddit, forums, X, LinkedIn posts. Usable for leads and for anecdote, labeled as such. Never the only support for a number or a key finding.
```

### Rules while collecting

- **Chase every number to its origin.** A blog saying "Gartner says 70%" is not a source for 70%. Find the Gartner piece. If you cannot, cite it as "[n], via [blog], original not found" and drop the confidence.
- **No key finding rests on one source.** Two independent sources minimum or it is marked single-source.
- **Date every data point.** The date of the data, not of the article. Flag anything older than 24 months in a fast-moving market.
- **Label vendor bias.** Mark a company's claims about itself as such. Same for a vendor's survey that makes its own category look urgent. Same for a competitor writing about a rival ("X pricing explained" on a rival's blog): label "competitor, interested". Same for the user's own published work (their agency's case study, their post): usable, labeled "user's own work".
- **History questions** ("how did X change since 2024"): the record is the company's own past pages. Try the Wayback Machine first. If it is blocked from this session, open it through the user's logged-in browser if your agent can drive one. If not, try archive.today, then the company's own changelog, docs and announcements. A dated third-party snapshot (a competitor's "X pricing 2023" post) may carry a historical number only when nothing primary exists, labeled "third-party snapshot, [date]" with Low confidence. If the number carries no date of its own, use the post's date and say "date of post, not of price". This is the one case where tier 3 can carry a number and the report says so.
- **Region and currency.** Pricing pages change by region. Aim for the user's market first and say which version you actually saw. If you could only see another region, give that, say so and report any evidence of the user's regional price separately. Never mix currencies in one comparison without saying so.
- **Read key pages raw.** For pricing pages, filings and any source behind a headline number, read the page's own text (full-text fetch or HTML), not a tool's summary. Summaries drop the one line that matters.
- **Blocked sources.** Failed and blocked calls count toward the budget. If blocks eat a third of it, stop that branch and report the block instead of burning the rest.
- **Nearest date, real date.** If the asked baseline ("since 2024") has no record, use the nearest dated one and state its real date ("July 2023 snapshot"). Never relabel it as the asked date.
- **Forums are anecdote.** "One Reddit user reports X" is fine. "Users report X" from three threads is not.
- **No circular verification.** Do not present what the user already knows about their own company as a research finding. Using the user's internal data (their customer list, their numbers) to test how an outside finding fits them is fine and often the best step, labeled "internal data".
- **Search wide, then narrow.** Short broad queries first, see what exists, then specific ones. Search in the market's language too (German for a German market). Use `site:` on docs and help centers. Run independent searches in parallel.
- **Logged-in and paywalled sources:** use the user's logged-in browser when the plan names one and your agent can drive it. A paywall you cannot pass is a limit to report, not a gap to fill with a guess.

### Experts-first route

Stage 1, find the authors (after the question round, before the plan, 15-25 web calls). Your own general knowledge of an author is a lead, not verification. A third-party summary of their talk is a "via" source, not verification either. Score only the criteria you actually checked, unchecked ones count as not met. Search for who the field itself cites: who other practitioners quote, whose frameworks get named, who publishes original data. Start from recommendations inside good sources, not from "top 10 experts in X" lists. Score every candidate against this:

```
paste exactly, do not reword
TRUSTED IF MOST OF THESE HOLD:
  Skin in the game: has done the thing at real scale (operator, founder, buyer), not only written about it.
  Original data or cases: publishes their own numbers, benchmarks or named examples, not rewrites.
  Specific and falsifiable: makes concrete calls that can be checked and past calls held up.
  Independent: does not sell the product their advice points to. If they do, they disclose it.
  Cited by peers: other trusted people reference or argue with their work.
  Current: active in the last 24 months on this topic.
RED FLAGS: engagement-bait posting, only generic frameworks, sells a course on every answer, no track record outside content.
```

Build a roster of 5-8. It must include at least one credible dissenter or a different school, chosen against the user's current bet, so the report maps a debate and not one camp. Credentials are not correctness: a trusted author's claim still needs its evidence.

Operators who explain their own company's choice (a founder on why they changed their pricing) score high on skin in the game and fail independence by definition. Keep them, they are often the best evidence. Label them "interested party".

Before listing an author, open at least one piece where they speak on THIS question or its direct parent (for "per source or per seat": how to pick a pricing metric). The field alone does not count. A famous name with nothing on the topic is a wasted slot.

Scan rules, in priority order:
1. Verified beats many. 5-8 is the target, 4 verified is an acceptable roster (say why it is short). Four verified authors beat seven half-checked ones. An author you could not verify in the scan may be listed only marked "unverified, check in stage 2". Co-authors of one piece take one slot. If the budget ends with fewer than 4 verified, send the short roster anyway, say the scan hit its budget and let stage 2 verify or drop the rest. Do not extend the scan silently.
2. "Most of these hold" means at least 4 of the 6. Any red flag keeps them off the roster, unless they are the only voice of a needed dissent, then they stay labeled with the flag.
3. A company is not an author. Its founder or an executive speaking on record is.
4. The dissenter is someone whose position cuts against the user's bet in their own words. When the bet picks one option among several, the strongest verified voice for any other option qualifies, a voice for the named alternative first. A partial dissent counts when it argues the opposite for conditions that match the user, labeled "partial". If none exists, say so in the plan and name the strongest counter-evidence instead (a documented case, a data point), marked "not opened yet" if you only saw it in search results. Do not promote a weak voice to fill the slot.
5. An operator from an adjacent segment (a data-team tool when the user sells to marketers) stays when the mechanism transfers, labeled with their segment.

Stage 2, after sign-off, research what each one thinks. Go to their own words (their posts, books, talks, podcasts, interviews), not summaries of them. For each author capture: position, the evidence or cases they give, the date and the conditions under which they say it holds (company stage, market, model). Add whatever the user asked to pull from the authors in round 2. Where authors disagree, look for why: different context, different data or a real disagreement.

If an approved author's own words cannot be reached (no transcript, paywall) or turn out to say nothing on the question, pick one: drop the author or use a summary by someone else once and label it "via [source]". Method and limits says which. Never fill their row with what they "would probably say".

In the report, experts-first adds the "Who thinks what" section shown in the Step 4 template. The findings are built on where the experts agree, where they split and which view fits the user's situation. Dates and trust reasons live in the source table, not in this table, so it stays readable.

### Deep mode: subagents

One subagent per issue-tree branch (experts-first: one per 2-3 authors), all launched in one message so they run in parallel. If your agent cannot spawn subagents, run the branches one after another with the same brief. Each gets this brief:

```
paste exactly, fill the brackets
Objective: answer [sub-question] for the research question "[key question]".
Hypothesis to test: [what would prove or kill it].
Sources: start with [named tier 1 sources]. Tier 3 only for leads. Chase every number to its original source.
Boundaries: stay inside this branch. Do not cover [the other branches]. Stop after ~[N] tool calls or when searches stop adding anything new.
Output: an evidence log in the exact table format below, then 3 lines: what you found, how confident, what you could not find.
```

### Evidence log (working file, every mode)

Keep it as you go. It is what the report is written from and nothing enters the report that is not in it. A source gets its [n] the first time it enters the log and keeps that number in the report. Claims get letters (A, B, C), sources get numbers, so the two never mix. Source details (title, publisher, URL, type, trust note) go straight into the Sources table at the same moment.

```
| ID | Claim (one fact) | Source [n] | Tier | Data date | Exact quote or number, as on the page | Confidence |
```

Record the quote or number exactly as the page shows it. That is what makes the Step 5 check cheap. If the fetch tool returned a paraphrase instead of the page text, mark the row "paraphrased by tool".

## Step 4: Synthesize into a pyramid

Write the report from the evidence log, top down. The reader should be able to stop after the first 5 lines and still have the answer.

Rules that hold at the point of writing:

- **The title is the answer**, a full sentence, not a topic. "DinoCo raised entry prices 40% since 2024 and is walking away from freelancers" not "DinoCo pricing analysis".
- **Every finding heading is a full sentence** (the numbered sections and the title). The fixed frame sections of the template (Bottom line, Why this question, What to do and the rest) keep their names. Reading only the finding headings tells the whole story.
- **The title's numbers carry [n] too.**
- **3-5 key findings**, no overlap, each one directly supporting the answer. More than 5 means you have not synthesized yet.
- **Every number and every non-obvious claim carries [n]** right after it. No citation, no claim. Your own estimate is labeled "estimate" with the math shown.
- **Every [n] is a clickable link to the exact page**, written `[[n]](URL)`, so the reader verifies in one click without scrolling to the source table. When the sentence quotes the source word for word, add a text fragment so the browser jumps to the passage: `[[n]](URL#:~:text=first%20five%20words%20of%20quote)`. Use a fragment only for text you saw on the page, never for a tool paraphrase.
- **Each finding ends with a "So what" line** for the decision named in the plan.
- **Evidence that contradicts the answer goes in the report**, not in the bin.
- Tables for comparisons of 3+ entities. Prose for reasoning.

Template:

```
paste exactly, fill the brackets, keep the section order
# [The answer as one sentence]

As of [date] · Mode: [mode] · For: [decision it feeds]

## Bottom line
[2-4 sentences: the answer, why, what to do about it.]
**Confidence:** [High / Medium / Low], because [one line: source quality, agreement, gaps]. Split it when parts differ ("High for today's prices, Low for the history").

## Why this question
[Situation, complication, question. 3-5 sentences max. What the reader already knows, what changed, what we needed to find out.]

## Key findings
1. [Finding as a full sentence] [n]
2. ...
(3-5)

## Who thinks what   <- experts-first only, delete for evidence-first
| Author | Position in one line | Their evidence | When it holds | [n] |
|---|---|---|---|---|
**Consensus:** [what most of them agree on]
**The real split:** [where they disagree and why]
**Fit for you:** [which view matches the user's context and why]

## 1. [Finding 1 as a full sentence]
[Evidence with [n] citations. A table where it helps.]
**So what:** [one line for the decision]

## 2. ...

## What to do
[Recommendations with the first concrete step for each. If the question was not a "what to do" question, say what the findings change for the reader.]

## What would change the answer
[The weakest links: single-source findings, old data, the counter-evidence found, the question we could not answer and how to answer it (a call, a paid source, a test).]

## Method and limits
[Plan approved on [date] (or "not reviewed"), what was searched, number of sources by tier, what was behind paywalls or unreachable, where the search was stopped and why.]

## Sources
| # | Source | Publisher / author | URL | Type | Tier | Data date | Used for | Note |
|---|---|---|---|---|---|---|---|---|
```

## Step 5: Verify before the user sees it

Run this red-team pass on the finished draft. Fix, then deliver.

1. **Citation check.** Every number and quote in the report is checked against the exact text in the evidence log: does the sentence say what the log row says? Does the row point to the right [n]? Then re-open the live source for the numbers in the title, the Bottom line and the key findings, for every row marked "paraphrased by tool" and for at least 5 other claims. Fix or cut every mismatch. Quick mode: re-open the source for every number in the answer. A new fact found while re-checking may enter the answer once it is in the evidence log with its [n].
2. **Weakest three.** Name the three claims most likely to be wrong. Each one is either strengthened with a second source, softened to what the evidence supports or moved to "What would change the answer".
3. **Concentration.** No single source carries more than a quarter of the citations and no key finding rests on tier 3 alone. Exception: when the question is about one entity, that entity's own page (its pricing page, its filing) may carry more. That is the primary source doing its job.
4. **Hypothesis honesty.** If the day-one hypothesis survived, look once more for the strongest evidence against it. Confirmation is the default failure.
5. **The 5-line test.** Title plus Bottom line alone must answer the key question.

## Output

- Files go to `research/[YYYY-MM-DD]-[topic-slug]/` in the working directory or where the user keeps research. With no file system (a plain chat), put the report in the reply and say so in one line. Standard and deep write `report.md` and `evidence-log.md`. Quick writes `evidence-log.md` only, plus `report.md` if asked.
- Standard and deep mode, in chat, in the user's language: the answer sentence, the confidence, the 3-5 findings as one line each, the first recommended step, any change made to the approved plan and where the files are. Nothing else. Then offer in one line a shareable copy (a doc or a PDF) if the agent can make one.
- Quick mode, in chat, in the user's language, in this order: one line on anything that could not be reached (context, archives), the plan and assumptions in up to 3 lines (including the expected answer, which is the hypothesis Step 5 tests), the answer as one sentence with [n], the confidence (split if parts differ), 2-3 supporting points with [n], a "Limits" part of up to 3 short lines (plan changes, blocked sources, contradicting evidence, the weakest claim), the source list with tier, date and the full URL written out. Every [n] in the answer is a link, as in Step 4. Keep the evidence log in the working folder, it is what Step 5 checks against. A report file only if asked.
- If the research could not answer the question (sources do not exist, all paywalled), say so in the first line, report what was found and name the fastest way to a real answer. Do not pad a thin result into a long report.

## Pre-send checklist

- Context was gathered before questions. The questions went through the question tool (or plain text when it is absent), round 1 max 4 questions with clickable options, the route was offered unless the user named it, round 2 only for experts-first. Quick mode asked nothing.
- Standard and deep mode: the plan was approved before collecting or it is shown as "Plan (not reviewed)" for a called or unattended run.
- Experts-first: the user was asked for known authors and what to pull from them, their picks are on the roster labeled "your pick", the author scan ran after the questions, the roster was signed off, it includes a dissenter chosen against the user's bet, every position is cited to the author's own words (or labeled "via"), dropped authors are named and the "Who thinks what" table is in the report.
- Any change to the approved plan is in Method and limits and in the chat reply.
- The title and every finding heading are full sentences, not topics.
- 3-5 key findings, no overlap (quick mode: 2-3 supporting points).
- Every number has [n], every [n] is a working link to its page, every [n] is in the source table with its full URL written out, every source table row is cited somewhere.
- Every number was traced to its origin or marked "original not found".
- No key finding rests on one source or on tier 3 alone, except a history number labeled "third-party snapshot" where nothing primary exists.
- Contradicting evidence and the weakest claims are in "What would change the answer".
- Data dates are in the source table, old data is flagged.
- The citation check (Step 5.1) was actually run, not assumed.
- Quotes stay exactly as the source wrote them.
- Quick mode: the checklist items about report sections apply to their quick-mode lines (the Limits part stands for Method and limits and for What would change the answer).
