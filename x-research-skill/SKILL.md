---
name: x-research-skill
description: >
  Use when researching X/Twitter discourse, community reactions, launch
  chatter, dev opinions, or source discovery via local Grok MCP Gateway.
---

# X Research

IRON LAW: X is signal, not source of truth. Verify primary sources before stating facts.

Use X for real-time perspectives, claims, reactions, and source discovery. Do not treat X discourse as primary truth. Verify linked docs, repos, papers, announcements, filings, or screenshots before presenting factual claims.

## Default Path

Use the local MCP gateway for ordinary X retrieval:

- Server: `grok_mcp_gateway`
- Endpoint: `http://127.0.0.1:9996/mcp`
- Tool: `x_retrieve`

Always pass explicit `from_date` and `to_date` for "today", "latest", "this week", "last month", or any time-sensitive request.

Load `references/mcp-gateway.md` for `x_retrieve` query patterns and examples.

## Tool Choice

- Use `x_retrieve` for open-ended discourse search, structured posts, source discovery, reaction tracking, and latest posts from handles.
- For direct tweet URLs or IDs, pass the full links or IDs in `query`; add `handles`, `from_date`, `to_date`, or `sort` only when they narrow the request.

There is no alternate retrieval fallback in this skill. If `x_retrieve` is reported as not enabled, treat it as an MCP client configuration problem and report it directly instead of changing arguments or switching tools.

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

- Too noisy: add `-is:reply`, narrow terms, use handles, use `sort: relevance` or `best_effort_filters`.
- Too few results: broaden with `OR`, remove filters, expand date range.
- Stale results: pass exact `from_date` / `to_date`.
- Tool rejects arguments: fix the `x_retrieve` arguments against the schema.
- Tool is not enabled: report MCP client config/policy mismatch; do not retry with argument tweaks.
- X-only evidence: say it is discourse/signal, not confirmed fact.
