# MCP Gateway

## MCP Tools

Use `x_retrieve` for normal X retrieval:

- open-ended discourse search
- structured post retrieval by topic, handle, date range, or filters
- source discovery for original, official, or person posts
- reaction tracking around a launch, incident, or claim
- latest posts from one or more handles

Examples:

```json
{"name":"x_retrieve","arguments":{"handles":["xai"],"sort":"latest","count":5,"lookback_days":30}}
{"name":"x_retrieve","arguments":{"intent":"posts","handles":["xai","exampledev"],"query":"Hermes Agent","from_date":"2026-05-01","to_date":"2026-05-20","count":10,"sort":"latest","include_reposts":false}}
{"name":"x_retrieve","arguments":{"intent":"source_discovery","query":"https://x.com/example/status/1234567890 original post context","count":10}}
{"name":"x_retrieve","arguments":{"intent":"research","query":"AI agents MCP developer discussion","from_date":"2026-06-01","to_date":"2026-06-11"}}
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

## No Fallback

If MCP reports `x_retrieve` is not enabled, report the MCP client configuration
issue instead of falling back to another X retrieval path.
