# Agent Skills

A collection of reusable skills for AI coding assistants (Claude Code, Gemini CLI, Codex, etc.).

Each skill is a self-contained folder with:
- **`SKILL.md`** — Instructions and usage documentation
- **`scripts/`** — Helper scripts and utilities
- **`.env.example`** — Required environment variables (copy to `.env` and fill in)

## Available Skills

| Skill | Description |
|---|---|
| [gemini-transcribe](./gemini-transcribe/) | Transcribe or analyze audio/video files via Google Gemini API |
| [video-transcript-downloader](./video-transcript-downloader/) | Download videos, audio, subtitles, and transcripts from YouTube and other sites (pairs well with gemini-transcribe) |
| [trace-review](./trace-review/) | Execution-path tracing code review that demands concrete evidence for every judgment |
| [conventional-commit](./conventional-commit/) | Draft, rewrite, and validate commit messages as Conventional Commits |
| [prepare-chatgpt-pro-consult](./prepare-chatgpt-pro-consult/) | Pack a controlled engineering consult for ChatGPT Pro with baseline control |

## Installation

Copy the desired skill folder into your agent's skills directory:

```bash
# For Claude Code
cp -r gemini-transcribe ~/.claude/skills/

# For Gemini CLI / Antigravity
cp -r gemini-transcribe ~/.gemini/skills/

# For Codex
cp -r gemini-transcribe ~/.codex/skills/
```

Then create a `.env` file in the skill folder with the required API keys (see `.env.example`).

## Contributing

1. Each skill lives in its own top-level directory
2. Include a `SKILL.md` with YAML frontmatter (`name`, `description`)
3. Include `.env.example` for any required secrets
4. Never commit `.env` files with real credentials

## License

MIT
