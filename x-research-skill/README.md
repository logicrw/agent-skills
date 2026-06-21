# x-research-skill

Research X/Twitter discourse from an agent.

## Paths

Default path: local Grok MCP Gateway.

- MCP server name: `grok_mcp_gateway`
- Default endpoint: `http://127.0.0.1:9996/mcp`
- Tools: `x_search`, `x_posts`, `x_latest_posts`

CLI path: bundled Bun script for raw X API workflows.

- Requires Bun.
- Requires `X_BEARER_TOKEN` in the environment or local `.env`.
- Read-only. It does not post, like, follow, or manage accounts.

## Setup

For the MCP path, install and run [Grok MCP Gateway](https://github.com/logicrw/grok-mcp-gateway) separately, then expose it to your agent as `grok_mcp_gateway`.

For the CLI path:

```bash
cp .env.example .env
$EDITOR .env
bun run x-search.ts search "AI agents MCP" --quick
```

## Security

Do not put bearer tokens directly in commands. Keep `.env` local and uncommitted. Treat X discourse as signal, not primary evidence; verify linked docs, repos, papers, announcements, filings, or screenshots before presenting factual claims.
