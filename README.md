# Operator Toolkit

Hey, I'm [Paul](https://www.linkedin.com/in/pawelogonowski/) 👋 3x founder, 2 exits and in B2B marketing since 2008. These days I do growth and GTM for B2B SaaS. I also write [The Anti-Grind Business Manual](https://owneropsguide.substack.com), a weekly newsletter about running ops in a B2B business without grinding yourself into the ground.

This repo is where I put the stuff I actually use: Claude skills, prompts, n8n workflows and small scripts. Everything in here ran on my own work first (my research, my newsletter, my pipeline) before it got a README, so it's probably more opinionated than it should be. Take what helps and bend the rest to your setup.

To be straight about where it is: the repo is brand new and there's one skill in here right now. More is coming as I clean things up enough to share them (the slow part is ripping my own name and context out of every file, I apparently hardcode myself everywhere).

## What's in here

| Folder | What goes there | Status |
|---|---|---|
| [`plugins/`](plugins/) | Skills in the open [Agent Skills](https://agentskills.io) format. They work in Claude, Claude Code and Cowork and in most other agents that read `SKILL.md` | 1 skill |
| [`prompts/`](prompts/) | Prompts you paste into any chat | Coming soon |
| [`n8n/`](n8n/) | Importable n8n workflows | Coming soon |
| [`scripts/`](scripts/) | Small scripts that glue the rest together | Coming soon |

## Skills

| Skill | What it does |
|---|---|
| [deep-research](plugins/deep-research/skills/deep-research/) | Research done the way a strategy consultant would do it. Context first, a plan you sign off, primary sources first and a report that opens with the answer, with every claim linked to the page it came from |

## Install a skill

**Claude Code**

```
/plugin marketplace add pogonow/operator-toolkit
/plugin install deep-research@operator-toolkit
```

**Claude.ai and Cowork:** grab the skill's ZIP from [Releases](../../releases) and upload it under Skills in Claude's settings.

**Other agents** (Codex, Cursor, Copilot, Gemini CLI and a bunch more):

```
npx skills add pogonow/operator-toolkit
```

## License

MIT. Use it, change it, ship it. A link back is always nice.

## Say hi

If something here saved you an afternoon (or broke on your setup), open an issue. I read everything.
