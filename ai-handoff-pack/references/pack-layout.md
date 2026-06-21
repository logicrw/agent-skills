# Handoff Pack Layout

The default handoff pack is optimized for fast agent takeover, not archival completeness.

## Files

`index.md`
: Entry point. Explain the pack purpose, reading order, and top-level map.

`current-state.md`
: Current verified state. Include what is true now, what changed, and what is no longer true.

`decisions.md`
: Accepted decisions with rationale, alternatives considered, and source anchors.

`open-questions.md`
: Unresolved questions, missing evidence, and decisions that need the user.

`tasks.md`
: Next actions. Make each task independently actionable.

`sources.md`
: Source inventory. List chat files, documents, URLs, screenshots, commands, and generated artifacts.

`log.md`
: Newest-first updates. Keep it brief.

`entities/`
: Reusable concepts, tools, systems, papers, products, files, modules, or people that future agents may need.

## Index Template

```markdown
# Handoff Index

## Read First

1. [Current State](current-state.md)
2. [Decisions](decisions.md)
3. [Open Questions](open-questions.md)
4. [Tasks](tasks.md)

## Entity Map

- [Sumink](entities/sumink.md) - visual card canvas used for agent-assisted writing.

## Source Coverage

See [Sources](sources.md).
```

## Log Template

```markdown
# Handoff Log

## YYYY-MM-DD

- Created or updated <files> from <sources>.
```

## Entity Template

```markdown
# Entity Name

## Current Understanding

Short factual summary.

## Why It Matters

How this affects the project or next agent.

## Relationships

- Related to [Other Entity](other-entity.md).

## Sources

- Source anchor.
```
