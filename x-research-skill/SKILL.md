---
name: x-research-skill
description: >
  Use when researching X/Twitter discourse, community reactions, launch
  chatter, dev opinions, source discovery, or raw X API workflows via local
  Grok MCP Gateway or bundled CLI.
---

# X Research

Use X for real-time perspectives, claims, reactions, and source discovery. Do not treat X discourse as primary truth. Verify linked docs, repos, papers, announcements, filings, or screenshots before presenting factual claims.

## Default Path

Use the local MCP gateway for ordinary X search:

- Server: `grok_mcp_gateway`
- Endpoint: `http://127.0.0.1:9996/mcp`
- Tools: `x_search`, `x_posts`, `x_latest_posts`

Always pass explicit `from_date` and `to_date` for "today", "latest", "this week", "last month", or any time-sensitive request.

Load `references/mcp-gateway.md` for tool selection, query patterns, CLI lane, and examples.

## Tool Choice

- Use `x_search` for open-ended discourse search.
- Use `x_posts` for handles, counts, date ranges, sort, replies/reposts, or engagement filters.
- Use `x_latest_posts` only for recent posts from one handle.
- Use the bundled CLI only when the user needs raw API-shaped workflows: profile, tweet, thread, saved output, watchlist, advanced operators, or explicit "x-research CLI".

The CLI is not a fallback for failed MCP calls.

## Research Loop

For quick asks, one good MCP query may be enough. For deeper research:

1. Decompose into 3-5 targeted queries: core topic, expert voices, objections, positive signal, linked resources.
2. Search and judge signal quality before summarizing.
3. Follow high-signal threads or profiles only when they change the answer.
4. Fetch linked primary sources before treating a claim as fact.
5. Synthesize by theme, not by query.
6. State what is confirmed, weak, anecdotal, or missing.

## Output

For research briefs:

```markdown
### Finding

1-2 sentence synthesis.

- @user: concise evidence or claim summary [link]
- @user2: supporting or conflicting evidence [link]

Source boundary: confirmed facts, X-only claims, missing evidence, and caveats.
```

For latest-post tasks, give a compact list with author, date, text summary, metrics if available, and link/citation status. Do not invent missing metrics or claim timeline completeness unless the tool verifies it.

## Failure Handling

- Too noisy: add `-is:reply`, narrow terms, use handles, sort by likes.
- Too few results: broaden with `OR`, remove filters, expand date range.
- Stale results: pass exact `from_date` / `to_date`.
- Tool rejects arguments: switch to the tool that owns that parameter.
- X-only evidence: say it is discourse/signal, not confirmed fact.
