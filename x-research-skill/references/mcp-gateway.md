# MCP Gateway And CLI

## MCP Tools

Use `x_search` for open-ended search:

- "What are people saying about X?"
- "Search X for reactions to this launch."
- "Find discussion around this API change."
- Inputs: `query`, optional handles/date/image/video/raw/model.

Use `x_posts` for structured retrieval:

- latest N posts from one or more handles
- posts by handle plus topic
- posts in a date range
- include/exclude replies or reposts
- best-effort likes/reposts/replies/views filters

Use `x_latest_posts` only as a shortcut for recent posts from one handle.

Examples:

```json
{"name":"x_latest_posts","arguments":{"handle":"xai","count":5,"lookback_days":30}}
{"name":"x_posts","arguments":{"handles":["xai","exampledev"],"query":"Hermes Agent","from_date":"2026-05-01","to_date":"2026-05-20","count":10,"sort":"latest","include_reposts":false}}
{"name":"x_search","arguments":{"query":"AI agents MCP developer discussion","from_date":"2026-06-01","to_date":"2026-06-11"}}
```

## Query Patterns

- Topic: `"Hermes Agent" OR "Grok MCP"`
- Handle scoped: `from:xai "Hermes Agent"`
- Expert/source scoped: `from:<handle> <topic>`
- Pain points: `<topic> (bug OR broken OR issue OR migration)`
- Positive signal: `<topic> (shipped OR benchmark OR faster OR launch)`
- Technical sources: `<topic> has:links`
- Domain links: `<topic> url:github.com OR url:docs.example.com`
- Noise reduction: `-is:retweet -is:reply`
- Spam reduction: `-airdrop -giveaway -whitelist -mint`

If results are weak, refine once before answering: narrow handles, adjust date range, add/remove `OR`, or switch between latest and relevance.

## CLI Lane

Use the CLI only when the user needs API-shaped X data or workflows that xAI `x_search` does not provide.

Good CLI reasons:

- exact profile, tweet, or thread lookup
- raw JSON / markdown output for saving or replay
- watchlist checks
- advanced recent-search operators
- future X Developer API workflows once credentials/scopes are available

Run from the current `x-research-skill` directory:

```bash
cd <this x-research-skill directory>
source .env
```

Common commands:

```bash
bun run x-search.ts search "<query>" --quick
bun run x-search.ts search "<query>" --sort recent --since 1d --limit 20
bun run x-search.ts search "from:<handle> <topic>" --no-replies --quality
bun run x-search.ts search "<topic> has:links" --markdown --save
bun run x-search.ts profile <username> --count 20
bun run x-search.ts thread <tweet_id>
bun run x-search.ts tweet <tweet_id> --json
bun run x-search.ts watchlist check
```

High-value flags: `--quick`, `--from`, `--since`, `--sort`, `--limit`, `--pages`, `--no-replies`, `--quality`, `--min-likes`, `--min-impressions`, `--json`, `--markdown`, `--save`.

CLI auth depends on local env, usually `X_BEARER_TOKEN`. For endpoint/operator details, read `references/x-api.md` only when needed. Do not use this skill for posting tweets or account management.
