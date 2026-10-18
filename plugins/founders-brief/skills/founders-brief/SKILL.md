---
name: founders-brief
description: Builds and maintains The Founder's Brief, one private file that tells a B2B SaaS founder's AI how their company actually works (product, ICP and buyers, ARR range and ACV, GTM motions and channels, this quarter's goals, what was tried and failed, what they believe will work and why, vocabulary, who decides what, plus a founder-only layer) by researching the company and the founder online first (website, pricing page, G2 and Capterra reviews, LinkedIn, podcasts), then interviewing the founder instead of asking them to write it. Use when the founder says "build my brief", "add to my brief", "refresh my brief", "my AI doesn't know my company", "AI keeps giving me generic answers", "set up my company context", "onboard my AI" or pastes an existing Founder's Brief or Owner's Brief. Also use when the founder complains that an AI answer missed because it didn't know something about their company.
---

Skill updated: 2026-10-18
Companion post: Why AI Gives You Generic Answers About Your SaaS (and How to Fix It), https://owneropsguide.substack.com/p/why-ai-gives-generic-answers
From The Anti-Grind SaaS Manual by Paul Ogonowski.

# The Founder's Brief

Your AI is a new hire with amnesia. Every new chat starts on day one, with no idea what you sell, who buys it, how you go to market or what you already tried. This skill runs the onboarding it never got: it works out which context matters for the decisions you want help with, interviews you and hands back one private file you load into your AI projects.

It's built for you, the founder, as your sparring partner, so it gets the full picture. It never invents a fact about your company and it never decides anything for you.

## Pick the mode first

Work out which of three modes the founder needs before asking anything else.

- **Build.** The founder says "build my brief" and there's no brief pasted in the chat or in the project files. Run the full interview below.
- **Add.** The founder says something missed or says "add to my brief" and the brief is pasted in the chat or sits in the project files. Run the add mode.
- **Refresh.** The founder says "refresh my brief". Also, whenever you can see a brief (pasted or in the project files), check its `Last verified` date. If it's more than 30 days old, offer the refresh once, in one sentence, after you've handled what they came for. If they say no, drop it.

If the founder wants add or refresh but you can't see a brief, ask them to paste it. Never rebuild it from scratch without asking. An older Owner's Brief counts as a brief: keep its content, offer to fill the SaaS sections it's missing (numbers, GTM motions and channels) and rename `[OWNER-ONLY]` to `[FOUNDER-ONLY]`. If you can't tell which mode they want, ask one question: "Are we building your brief from scratch, adding something to it or doing the monthly refresh?"

## Build mode

### Step 1: Do your homework first

Before the interview, ask for two things only: the founder's name and the company website.

Then research them, the way a good new hire would before day one. If you can search the web and open pages:

1. Read the website: the product, who it's for, the pricing page (plans, price points, free trial or freemium, "contact sales"), case studies, integrations, the team page.
2. Look for reviews and opinions (G2, Capterra, TrustRadius, Product Hunt, the Shopify or other marketplace listing, Reddit threads, whatever fits the product).
3. Find the founder's LinkedIn profile.
4. Read what the founder writes there: the About section and their recent posts.
5. Look for podcasts, interviews, conference talks, Indie Hackers or MicroConf posts with the founder.
6. Check the changelog or blog for what shipped recently and which competitors the site compares itself to.
7. Build a short competitor list: search the main keywords the product targets and check the G2 or Capterra category page and the "alternatives" lists for this product. You'll use it in Step 2 if the founder can't name their competitors.

LinkedIn often needs a login. If a page won't open, say so and ask the founder to paste their LinkedIn About and two or three recent posts or skip it. If you can't browse at all, ask them to paste their homepage, pricing page and LinkedIn About instead.

Then hand back a short summary, ten lines at most: who they are, what the product does, who it's for, how it's priced, what customers say about it, who it competes with and anything that looked unclear or contradictory. Name the source for each line ("from your pricing page", "from a G2 review"). Ask the founder to correct it. Nothing from the research goes into the brief until the founder confirms it.

### Step 2: The SaaS basics

Ask, one or two at a time, only what the research didn't answer:

1. **ARR range.** Ask for a band, never an exact figure: under $1M, $1-3M, $3-10M or over $10M. Add the growth rate if they know it (roughly, year over year).
2. **ACV.** What does a typical customer pay per year? Ask for the range if it varies a lot by plan or segment. Also ask which segment brings most of the revenue.
3. **ICP and buyers.** Which companies buy (size, industry, tech stack) and which people: who uses it, who signs, who can block the deal.
4. **Positioning and value prop.** How do you describe what you do in one or two sentences and what's the main reason customers pick you over the alternative? For high-ACV deals (roughly $20K a year and up) ask for two kinds of value separately: executive value (what the person who signs gets: revenue, risk, cost, a result they can take to the board) and end-user value (what the people using it every day get: time saved, less manual work, fewer mistakes). Then ask which positioning they already tested (homepage messages, ad angles, outbound hooks, pitch decks), what worked and what didn't, with the proof for each.
5. **Competitors.** Who do you lose deals to and who do customers compare you with? Count "do nothing", spreadsheets and agencies too. If the founder can't name them, show the list from your research and ask them to confirm or correct it.
6. **GTM motions.** Which motions bring revenue today: founder-led sales, sales-led with AEs, product-led (self-serve, free trial, freemium), partner or channel-led, marketplace, community-led. Which one brings most of the new ARR?
7. **GTM channels.** Which channels feed those motions: content, SEO, AEO, PPC, paid social, outbound email, LinkedIn, events, partnerships and integrations, app marketplaces, referrals, word of mouth. Ask which one works best and which one they're spending on without knowing if it works.
8. **Retention.** Monthly or annual churn and net revenue retention, if they track them. "Don't track it" is a fine answer.
9. **Team.** How many people, how many in GTM and who owns growth today (often the founder).
10. **Experiment log.** Do you keep a record of what you tested and what came out of it (a Notion database, a spreadsheet, a doc)? It counts for product, marketing, ICP, positioning, channels and motions. If yes, ask for the link or an export and read it. Pull the tests, the results and the conclusions into the brief (sections 8 and 9), citing the log as the source. If there's no log, offer to add an empty experiment log section at the end of the brief so they can start one.
11. **What you want help with.** Two to four kinds of work or decisions, like pricing, positioning, a launch, outbound sequences, hiring a first marketer, board or investor updates.

Never push for exact revenue numbers. A range is enough for the AI to give stage-appropriate advice and it's safer in a file. If an answer is vague ("we do some content", "help me with growth"), ask for the concrete version before moving on: which channel brought the last five customers, what did the last deal close at, which decision did you make last week that AI could have helped with.

### Step 3: Work out what context matters

For each kind of work the founder named, think like a smart new Head of Growth who has to make that call next week. What would they need to know about this company to get it right? If you can search the web, check what context SaaS companies at this ARR range and ACV need for that kind of decision. A $3K ACV self-serve product and a $60K ACV sales-led product need very different advice, so let the numbers from Step 2 shape the list.

Show the founder a short list of the topics you plan to cover (eight to twelve lines) and ask: "Anything missing that a new hire always gets wrong at your company?" Add what they say.

The list always includes these core sections, in this order:

1. The product, who it's for, pricing and who you turn away
2. The numbers: ARR range, ACV, growth, churn and NRR (ranges are fine)
3. ICP and buying committee
4. Positioning and value prop (executive value and end-user value for high-ACV deals), plus the positioning already tested
5. Competitors and the alternatives customers compare you with
6. GTM motions and channels: what brings revenue today
7. Your goals for this quarter (one or two, with numbers if they have them)
8. What you tried that didn't work and the proof
9. What you haven't tried but believe will work and why
10. Names and vocabulary: product and plan names, feature names, customer nicknames, internal shorthand, words you use and words you never want used
11. Who decides what (roles, not names)
12. Anything specific to the kinds of work from Step 2 (one section each)
13. The founder-only layer

### Step 4: Interview

Go section by section, one question at a time and skip or just confirm what the research and Step 2 already covered. It's up to about 30 questions: roughly half an hour if the founder talks (voice mode works well), closer to an hour typing. Say that upfront and offer to split it across two sittings.

- For section 8, ask for the proof every time: "what happened, when was it and how do you know?" Proof is a number, a dashboard, a record or a customer's words. A channel that "didn't work" needs the spend, the time it ran and what it produced. "From memory" or "I don't know" goes in as `(unverified)`.
- For section 9, ask for the reason every time: "who told you, what did you see?" A belief with no reason goes in as `(gut feel)`. That's allowed, it just has to be labelled.
- Use the founder's own words. Don't polish their vocabulary into consultant language.
- If they say "I don't know" or "skip", write `[not given yet]` and move on. Never fill the gap yourself.

Before section 13, say this once, in your own words: this part stays private, check your AI tool's data settings first (including memory, which some tools use to remember what you say across chats, so consider turning it off for this one) and if something's very sensitive you can describe it with ranges or roles instead of names and exact figures.

Section 13 asks about the things the founder would never say at an all-hands: runway and burn, margins by plan or segment, the customer they'd happily lose, what they really think of the team, co-founder or investor tension plus the constraints the AI should respect (money, time, energy, a co-founder or board they have to keep on side). The section heading carries `[FOUNDER-ONLY]`. Any private line that belongs in another section starts with `[FOUNDER-ONLY]` too, so it gets stripped from a team copy.

If the person being interviewed isn't the founder (a team member running this about their own work), skip section 13 and make section 7 their own goals for the quarter.

A section counts as covered once it has one concrete line or shows `[not given yet]`. Stop when every section is covered or the founder says "enough". Don't start giving advice halfway through. If the founder asks a business question mid-interview, note it at the bottom under `Questions to ask next` and carry on. Once the brief is handed over, offer to answer those questions in the same chat, with the brief as context.

### Step 5: Write the brief

Use the template under "What to hand back". If you can create files, deliver the brief as a downloadable Markdown file named `founders-brief-[company-name].md`. If you can't, put the whole brief in one code block and tell the founder to save it as a `.md` file. Keep it short, a few pages at most. Cut anything a generic AI would get right without being told (SaaS best practices, metric definitions, motivational lines). What stays is what only this founder knows.

Before you hand it over, check every number and name in the brief against what the founder actually said. If you rounded, merged or narrowed something ("outbound" became "LinkedIn outbound"), put back their wording.

## Add mode

Ask, one at a time, skipping anything the founder already told you:

1. What did the AI (or a person) bring back and what was wrong with it?
2. What did it need to know to get it right?

If the answer is vague, ask for the concrete version. Then write the one to three lines that would have prevented the miss, put them in the section or two where they belong, update `Last verified` to today and hand back the full brief with a `Changes` list at the bottom. Don't touch anything else. If the miss came from something in the founder-only layer, mark the new line `[FOUNDER-ONLY]`.

## Refresh mode

Ask these six, one at a time and keep it to about ten minutes:

1. Did your goals for the quarter change?
2. Did the numbers move: ARR range, ACV, churn or NRR?
3. Which customers did you win or lose and why did you lose them?
4. Which motion, channel or positioning test did you start, stop or change and how did it go? (If they keep an experiment log, ask for the new entries instead.)
5. What changed on the team (roles, not names)?
6. Is there anything you now believe (or stopped believing) about what works?

Update the brief, set `Last verified` to today (if you don't know today's date, ask) and hand it back with a `Changes` list. Lines that no longer hold get deleted, not commented out.

## What to hand back

```
# The Founder's Brief: [Company name]
Last verified: [YYYY-MM-DD]
How to use this: load it into a private project in your AI before you ask anything about the company (a Claude Project or a ChatGPT project). Never put this full version in a project your team can see. Never share it without cutting every [FOUNDER-ONLY] section first.

## What we sell
[Product, who it's for, plans and pricing. Who you turn away and why.]

## The numbers
- ARR range: [band] · growth: [rough % or not given yet]
- ACV: [typical range] · main revenue segment: [segment]
- Churn: [rate or not tracked] · NRR: [rate or not tracked]
- Team: [size, how many in GTM, who owns growth]

## ICP and buyers
- Companies: [size, industry, stack]
- Users: [roles] · Signs the deal: [role] · Can block it: [role]

## Positioning and value prop
- How we describe it: [one or two sentences, their words]
- Why customers pick us: [the main reason]
- Executive value: [what the person who signs gets] · End-user value: [what daily users get]
- Positioning we tested: [message] · [result and proof or (unverified)]

## Competitors
- [Name or alternative]: [where we win] · [where we lose]

## How we go to market
- Motions: [founder-led / sales-led / product-led / partner-led / ...] · main source of new ARR: [motion]
- Channels that work: [channel] · [the proof]
- Channels we fund without proof: [channel]

## This quarter
[Goal 1, with the number if there is one]
[Goal 2]

## What we tried that didn't work
- [What] · [what happened: the proof or (unverified)] · [when] · [source: experiment log, if it came from there]

## What we believe will work
- [What] · [why: who said it, what you saw] · [(gut feel) if there's no reason]

## Our words
- [Name or term]: [what it means here and what it is not]
- Never call [our customers / our product / our team]: [word]

## Who decides what
- [Role]: [decisions they own]

## Experiment log
[Link to the founder's log or "none yet" plus the empty table: test · date · result · conclusion]

## [Kind of work 1 from Step 2]
[Only what a new hire needs to make this call well here]

## [Kind of work 2, 3, 4: one section each]

## [FOUNDER-ONLY] What stays between us
[Runway, margins, customers you'd lose, how you see the team, co-founder or board dynamics, constraints the AI must respect]

## Questions to ask next
[Anything the founder asked mid-interview. Leave the section out if there's nothing.]

## Changes
[Add and refresh modes only, one line per change. Leave the section out in build mode.]
```

After the brief, set the founder up so the brief stays the one file every company question starts from. In build mode, say:

"Next: in Claude, create a Project named after your company, open its project knowledge and upload this file (in ChatGPT: Projects, New project, add the file). Keep the project private. Then paste this into the project instructions:"

```
Before you answer anything in this project, read founders-brief-[company-name].md from the project knowledge and use it as the context for every answer.
When I tell you something new about the company or correct one of your answers because you were missing context, propose the one to three lines to add or change in the brief and tell me which section they go in. If you can edit project files, update the brief and its Last verified date yourself. If you can't, give me the full updated file so I can replace the old one.
If the brief's Last verified date is more than 30 days old, remind me once to run "refresh my brief".
```

"Then ask every question about your company inside this project. Start with the one you asked last week and compare the answer." Custom instructions fields are too small for the brief itself, so the brief goes in project knowledge and only the short instruction above goes in the instructions field. In add and refresh mode, deliver the updated file the same way and say: "Next: replace the old file in your project with this one."

## Sharing it with your team

If the founder asks for a version for the team or a new hire, hand back a copy with every `[FOUNDER-ONLY]` section and line removed. Also drop `Questions to ask next` and `Changes`. Replace the "How to use this" line with: "Team version. Founder-only sections and open questions removed." That team version works well as day-one context for a new growth hire. Then suggest the better option for the long run: give each person this skill and let it interview them about their own work, so they build their own brief.

## What this skill will not do

- It doesn't invent a number, a goal, a customer or a past result. Anything the founder didn't say stays `[not given yet]`.
- It doesn't ask for exact revenue. Ranges are enough.
- It doesn't decide your goals, your pricing, your motion, who you hire or who you let go. It writes down what you decided.
- It doesn't hand anyone a version with `[FOUNDER-ONLY]` sections in it and it reminds you to check your data settings before the private part.
- It doesn't keep a copy of your brief. You keep the file and you load it. Your AI tool's memory might remember parts of the interview, which is why you check memory settings before the private part.
- It doesn't turn the interview into a consulting session. Questions go to the bottom and get answered once the brief is loaded.

## Where this comes from

- Why AI Gives You Generic Answers About Your SaaS (and How to Fix It), https://owneropsguide.substack.com/p/why-ai-gives-generic-answers
- For the goals section, if the founder has five goals for one quarter: Quarterly Planning for SaaS Founders, https://owneropsguide.substack.com/p/one-priority-per-quarter
- If the founder is about to hire their first growth person: Don't Hire Yet, https://owneropsguide.substack.com/p/dont-hire-yet-rent-expertise-first
