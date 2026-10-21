# Operator Toolkit

[![skills.sh](https://skills.sh/b/pogonow/operator-toolkit)](https://skills.sh/pogonow/operator-toolkit)

Hey, I'm [Paul](https://www.linkedin.com/in/pawelogonowski/) 👋 3x founder and in B2B marketing since 2008. These days I do growth and GTM for B2B SaaS. I also write [The Anti-Grind SaaS Manual](https://owneropsguide.substack.com), GTM playbooks for B2B SaaS founders who can't be the whole GTM anymore.

This repo is where I put the stuff I actually use: Claude skills, prompts and small scripts. Everything in here ran on my own work first (my research, my newsletter, my pipeline) before it got a README, so it's probably more opinionated than it should be. Take what helps and bend the rest to your setup.

To be straight about where it is: the repo is brand new and there are three skills and one prompt in here right now. More is coming as I clean things up enough to share them (the slow part is ripping my own name and context out of every file, I apparently hardcode myself everywhere).

## What's in here

| Folder | What goes there | Status |
|---|---|---|
| [`plugins/`](plugins/) | Skills in the open [Agent Skills](https://agentskills.io) format. They work in Claude, Claude Code and Cowork and in most other agents that read `SKILL.md` | 3 skills |
| [`prompts/`](prompts/) | Prompts you paste into any chat | 1 prompt |
| [`scripts/`](scripts/) | Small scripts that glue the rest together | Coming soon |

## Skills

| Skill | What it does |
|---|---|
| [deep-research](plugins/deep-research/skills/deep-research/) | Research done the way a strategy consultant would do it. Context first, a plan you sign off, primary sources first and a report that opens with the answer, with every claim linked to the page it came from |
| [founders-brief](plugins/founders-brief/skills/founders-brief/) | The onboarding your AI never got. It researches your SaaS, interviews you about ARR, ACV, ICP, positioning, competitors, GTM motions and channels and writes one private brief your AI reads before every answer about your company |
| [ai-shortlist-check](plugins/ai-shortlist-check/skills/ai-shortlist-check/) | Does ChatGPT recommend your SaaS or someone else? Runs your buyers' prompts through ChatGPT, Gemini and Google's AI Overviews every week, counts your share of voice next to three competitors and hands you up to five fixes, for about $7 to $19 a month in API costs ([ZIP](downloads/Anti_Grind_SaaS_Manual_AI_Shortlist_Check.zip)) |

## Prompts

| Prompt | What it does |
|---|---|
| [how-did-you-hear-about-us-sorter](prompts/how-did-you-hear-about-us-sorter.md) | Sorts free-text "How did you hear about us?" answers into channels and tells you what share came from ChatGPT and other AI tools |

## Install a skill

**Claude Code**

```
/plugin marketplace add pogonow/operator-toolkit
/plugin install deep-research@operator-toolkit
/plugin install founders-brief@operator-toolkit
/plugin install ai-shortlist-check@operator-toolkit
```

**Claude.ai and Cowork:** grab the skill's ZIP from [`downloads/`](downloads/) and upload it under Skills in Claude's settings.

**Other agents** (Codex, Cursor, Copilot, Gemini CLI and a bunch more):

```
npx skills add pogonow/operator-toolkit
```

## License

MIT. Use it, change it, ship it. A link back is always nice.

## Say hi

If something here saved you an afternoon (or broke on your setup), open an issue or DM me on [LinkedIn](https://www.linkedin.com/in/pawelogonowski/). I read everything.
