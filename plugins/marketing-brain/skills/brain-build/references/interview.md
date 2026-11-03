# The interview

Read this when brain-build tells you to. It's the research and question list, with the folder each answer goes into. Adapted from The Founder's Brief.

## Step 1: Research

If you can search the web and open pages:

1. Read the website: the product, who it's for, the pricing page (plans, price points, free trial or freemium, "contact sales"), case studies, integrations, the team page.
2. Look for reviews (G2, Capterra, TrustRadius, Product Hunt, marketplace listings, Reddit threads).
3. Find the founder's LinkedIn profile and the About section.
4. Look for podcasts, interviews, conference talks, Indie Hackers or MicroConf posts with the founder.
5. Check the changelog or blog for what shipped recently and which competitors the site compares itself to.
6. Build a short competitor list from the G2 or Capterra category page and "alternatives to [product]" searches.

If a page won't open, say so and ask the founder to paste it. If you can't browse at all, ask for the homepage, pricing page and LinkedIn About.

Summary back to the founder: ten lines at most, source on every line, ask them to correct it.

## Step 2: The basics

One or two at a time, only what the research didn't answer. Folder in brackets.

1. ARR range as a band: under $1M, $1-3M, $3-10M, over $10M. Growth, roughly. [proof/numbers.md]
2. ACV: what a typical customer pays per year, the range if it varies, which segment brings most revenue. Plans and price points. [proof/pricing.md, segment in proof/numbers.md]
3. ICP and buyers: which companies (size, industry, stack), who uses it, who signs, who can block. [customers/icp.md]
4. Why customers buy, in their words. Which words they use for the problem. [customers/their-words.md]
5. Positioning: how you describe what you do in one or two sentences, the main reason customers pick you. For deals of roughly $20K a year and up, executive value and end-user value separately. [positioning/positioning.md]
6. Positioning you already tested (homepage, ads, outbound hooks, decks): what worked, what didn't, the proof. [experiments/positioning-tests.md]
7. Your beliefs: the opinions you repeat on every sales call, the things you'll never say, who you're against. [positioning/beliefs.md]
8. Competitors and alternatives (count "do nothing", spreadsheets and agencies): where you win, where you lose. [positioning/competitors.md]
9. Retention: churn and NRR if tracked. "Don't track it" is fine. [proof/numbers.md]
10. Team: how many people, how many in GTM, who owns growth today. [tools/people-and-access.md]
11. This quarter's one or two goals, with numbers if they have them. [positioning/goals.md]

Never push for exact revenue. If an answer is vague ("we do some content"), ask for the concrete version: which channel brought the last five customers, what did the last deal close at.

## Step 3: The deep parts

### Every motion and channel

Motions: founder-led, inbound, outbound, partners, PLG (self-serve, trial, freemium), paid. Channels: network and intros, referrals, LinkedIn posting, cold outreach (email and LinkedIn), intimate events, large conferences, webinars, content and blog, SEO, AI search, paid ads, signal-based outbound, ecosystem partnerships, app marketplaces, newsletters, B2B creators, PR, cold calling.

For each one, four questions:

1. Did you ever try it?
2. When, roughly?
3. What happened? (spend, time it ran, what it produced or "don't remember")
4. Where would the data be? (HubSpot campaign, a Notion page, the agency's report, an inbox thread)

Write one file per motion in `gtm-motions/` (copy `_motion-template.md`) (what brings revenue today, which channels feed it). Write every channel that was ever tried into `experiments/channels.md`, one block each, including the ones that did nothing. Never tried: one line, "never tried".

### Proof and beliefs

For anything that "worked" or "didn't work": what happened, when and how do you know? Proof is a number, a dashboard, a record or a customer's words. No proof: `(unverified)`. For a belief about what will work: who told you, what did you see? No reason: `(gut feel)`.

### Voice, twice

1. The company's voice: how the site, emails and ads should sound, words to use, words never to use, product and plan names. [voice/company.md]
2. The founder's own voice, for anything the marketer writes or amplifies in the founder's name: how they write and talk, what sounds like them, what makes them cringe. Use the LinkedIn posts from the research as the samples. [voice/founder.md]

### Tools and access

For every tool marketing and sales touch (CRM, email, ads accounts, analytics, website CMS, design, scheduling, data): what it's for, who can grant access, which plan. [tools/stack.md, tools/people-and-access.md]. Never passwords, keys or logins: the file says who to ask and where the credentials live (a password manager).

### Processes

For every recurring thing the founder does: name, how often, a link to the screen recording when it exists, steps written from the recording or transcript. No recording yet: `[recording needed]`. [processes/]

### Skills

Prompts and Claude skills the founder already uses for marketing or sales: what each does, where it lives. [skills/README.md]

### Brand

Colours (hex), fonts, logo rules (clear space, what not to do), templates, links to the Drive folders with the files. [brand/README.md]

## Step 4: Who owns what

Ask: "Which of these should only you change? Your marketer can always propose, but only you approve." Default founder-only: `positioning/`, `voice/founder.md`, `proof/pricing.md`. Their headers say `owner: founder`.

Stop when every file has one concrete line or `[not given yet]` or when the founder says "enough". If they ask a business question mid-interview, write it to `open-questions.md` and carry on.

## Refresh: six questions

One at a time, about ten minutes:

1. Did your goals for the quarter change?
2. Did the numbers move (ARR range, ACV, churn, NRR)?
3. Which customers did you win or lose and why did you lose them?
4. Which motion, channel or positioning test did you start, stop or change and how did it go?
5. What changed on the team (roles, not names)?
6. Is there anything you now believe or stopped believing, about what works?

Update only what changed, set `last_verified` on each file you touched, propose the change with a "why" and a "based on".
