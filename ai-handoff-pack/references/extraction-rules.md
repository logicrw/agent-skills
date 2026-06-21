# Extraction Rules

Extract for handoff value, not completeness.

## Entity Threshold

Create an entity file only when the item will likely be referenced again. Otherwise put it in `current-state.md`, `decisions.md`, or `open-questions.md`.

Good entity candidates:

- tools and systems
- project modules
- papers, products, datasets, APIs
- recurring concepts
- durable people or organizations
- reusable workflows

Poor entity candidates:

- one-off comments
- prompt wording
- temporary emotional reactions
- duplicate claims
- unverified speculation

## Batch Ingest

For many source files:

1. Build a source inventory first.
2. Identify newest or authoritative sources.
3. Extract current facts and superseded facts separately.
4. Update existing handoff files before creating new entity files.
5. Preserve source anchors for decisions and contested claims.

## Source Handling

Use the strongest available source:

1. current local files, commands, tests, docs, or official sources
2. explicit latest user instruction
3. recent chat conclusion with source anchor
4. older chat conclusion
5. inference

If sources conflict, write the conflict instead of choosing silently.

## Update Policy

- Keep `current-state.md` short and current.
- Move stale conclusions into "Superseded" sections only when they explain current choices.
- Keep `decisions.md` newest or most important first.
- Keep `tasks.md` executable.
- Keep `sources.md` complete enough for replay, not exhaustive enough to become noise.
