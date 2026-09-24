# Operator Toolkit

The skills, prompts, n8n workflows and scripts I use to run growth and ops with AI. Built for my own work first, published here once they have held up on real work.

By Paul Ogonowski, co-founder of Conversion, a data analytics agency (12 years).

## Skills

| Skill | What it does |
|---|---|
| [research](plugins/research/skills/research/) | Consultant-style research: context first, a plan you approve, primary sources, an answer-first report where every claim links to its source |

## What is in here

| Folder | What goes there |
|---|---|
| [`plugins/`](plugins/) | Skills in the open [Agent Skills](https://agentskills.io) format. They work in Claude, Claude Code and Cowork and in most other agents that read `SKILL.md` |
| [`prompts/`](prompts/) | Standalone prompts you paste into any chat |
| [`n8n/`](n8n/) | n8n workflows as importable JSON |
| [`scripts/`](scripts/) | Small scripts that glue the rest together |

## Install a skill

**Claude Code**

```
/plugin marketplace add pogonow/operator-toolkit
/plugin install <skill-name>@operator-toolkit
```

**Claude.ai and Cowork:** download the skill's ZIP from [Releases](../../releases) and upload it under Skills in Claude's settings.

**Other agents** (Codex, Cursor, Copilot, Gemini CLI and the rest):

```
npx skills add pogonow/operator-toolkit
```

## License

MIT. Use it, change it, ship it. A link back is nice, not required.
