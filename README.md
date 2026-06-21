# Agent Skills

Reusable skills for AI coding assistants such as Codex, Claude Code, Gemini CLI, and Antigravity.

Each top-level directory is a standalone skill package. Copy only the folders you need.

## Install

```bash
git clone https://github.com/logicrw/agent-skills.git
cd agent-skills

# Codex
cp -R sumink-canvas-agent ~/.codex/skills/

# Shared local skill root used by several agents
cp -R sumink-canvas-agent ~/.agents/skills/

# Claude Code
cp -R sumink-canvas-agent ~/.claude/skills/

# Gemini / Antigravity
cp -R sumink-canvas-agent ~/.gemini/skills/
```

If a skill includes `.env.example`, copy it to `.env` locally and fill in your own values. Never commit real credentials.

## Skills

| Skill | One-line use | Extra setup |
|---|---|---|
| [ai-handoff-pack](./ai-handoff-pack/) | Turn messy AI chats, notes, and research docs into a compact handoff pack for another agent. | Standalone. Optional: Python 3 for strict OKF validation. |
| [sumink-canvas-agent](./sumink-canvas-agent/) | Use Sumink as a human-agent visual writing board with cards, sections, connectors, backlinks, and drafts. | Requires Sumink/Summer Ink and its CLI. Optional: `jq`, `qlmanage`. |
| [shared-memory-skill](./shared-memory-skill/) | Read/write source-backed durable memory through a local Shared Memory MCP server. | Requires Shared Memory at `http://127.0.0.1:local-mcp-endpoint`; diagnostics use `MEMORY_HOME`. |
| [prepare-chatgpt-pro-consult](./prepare-chatgpt-pro-consult/) | Package a baseline-controlled consult for ChatGPT Pro or another remote web model. | Standalone. Optional: `repomix`, `zip`, Git. |
| [bumblebee-inventory-scanner](./bumblebee-inventory-scanner/) | Audit local developer supply-chain inventory with Perplexity Bumblebee. | Requires `bumblebee v0.1.1`; the skill can install it with Go. |
| [geb-context-map](./geb-context-map/) | Keep large codebase work context-light with L1/L2/L3 maps and focused reads. | Standalone. Optional: Serena/LSP, `ast-grep`, `repomix`. |
| [x-research-skill](./x-research-skill/) | Research X/Twitter discourse through a local Grok MCP Gateway or optional X API CLI. | Default path requires Grok MCP Gateway at `http://127.0.0.1:9996/mcp`. CLI lane requires Bun and `X_BEARER_TOKEN`. |
| [obsidian-canvas-card-writing](./obsidian-canvas-card-writing/) | Use Obsidian Canvas as a file-native card writing board and draft from `.canvas` structure. | Requires Obsidian Canvas files plus `obsidian-markdown` and `json-canvas` skills. |
| [gemini-transcribe](./gemini-transcribe/) | Transcribe or analyze audio/video files with Gemini. | Requires Gemini API credentials. |
| [video-transcript-downloader](./video-transcript-downloader/) | Download video/audio/subtitles/transcripts from supported sites. | Requires Node dependencies in that folder. |
| [trace-review](./trace-review/) | Review code by tracing execution paths and requiring concrete evidence. | Standalone. |
| [conventional-commit](./conventional-commit/) | Draft and validate Conventional Commit messages. | Standalone. |

## Dependency Notes

- Skills are instruction packages. They do not install external apps, MCP servers, or credentials by themselves.
- MCP-backed skills need the matching local MCP server configured in the agent that runs them.
- CLI-backed skills assume the named CLI is on `PATH`, or document their fallback path.
- Files under `references/` are loaded only when the skill says they are relevant.
- Files under `scripts/` are helper commands; inspect before running in a new environment.

## Privacy Rules

This repository should not contain personal paths, local caches, auth files, real tokens, chat transcripts, databases, or app state. Keep only reusable instructions, references, scripts, templates, and placeholder `.env.example` files.

Before publishing changes:

```bash
git diff --check
rg -n "/Users/|user-home|public-handle|global[.]env|BEGIN .*PRIVATE KEY|sk-[A-Za-z0-9]" -g '!node_modules' -g '!.git' .
ggshield secret scan path -r -y . --json
```

## Contributing

1. Keep each skill in one top-level directory.
2. Include `SKILL.md` with `name` and a trigger-focused `description`.
3. Keep `SKILL.md` short; move heavy guidance to `references/`.
4. Add scripts only for deterministic work.
5. Never commit `.env` or real credentials.

## License

MIT
