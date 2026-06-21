---
name: ai-handoff-pack
description: Use when AI chat logs, project notes, research docs, or loose Markdown need to become a local handoff pack for another agent or session, including project handoff, compile chat, knowledge-base handoff, or optional OKF-strict output.
---

# AI Handoff Pack

Turn messy source material into a compact Markdown handoff that another agent can read before taking over.

Default output is a simple handoff pack, not a full wiki and not strict OKF. Use strict OKF only when the user asks for OKF, Open Knowledge Format, LLM-Wiki compliance, validation, or cross-tool exchange.

## Use Gate

Use this skill when the source is larger or messier than the next agent should read raw:

- AI chat exports, project conversations, research notes, meeting notes, loose Markdown, TXT, or PDFs.
- Multi-session work where current decisions, open questions, and next actions may be buried.
- A handoff to another AI client, another agent, or a future session.

Do not use this for remote model consult packages with baseline, patch queue, and replay contracts; use `prepare-chatgpt-pro-consult`.

## Workflow

1. Locate sources and output root. Default output: `handoff/`.
2. Read existing `handoff/index.md` first when updating a pack.
3. Extract only durable handoff knowledge.
4. Separate current facts, decisions, discarded options, open questions, and tasks.
5. Create or update Markdown files. Prefer standard Markdown links.
6. Add source anchors for important claims.
7. Update `index.md`, `sources.md`, and `log.md`.
8. Report changed files, unresolved uncertainty, and what the next agent should read first.

## Default Layout

```text
handoff/
├── index.md
├── current-state.md
├── decisions.md
├── open-questions.md
├── tasks.md
├── sources.md
├── log.md
└── entities/
    └── <entity>.md
```

Load `references/pack-layout.md` before creating a new pack or changing layout.

## Extraction Rules

One file or section should represent one durable handoff unit:

- current project state
- accepted decision and rationale
- rejected or superseded option
- unresolved question
- next task
- reusable entity, tool, system, person, source, API, paper, product, or concept

Skip trivia, temporary conversation flow, repeated prompts, raw brainstorming, and claims that cannot be sourced or marked as inference.

Load `references/extraction-rules.md` for batch ingest, entity thresholds, source handling, and update policy.

## Links And Provenance

Use standard Markdown links by default. Avoid Obsidian `[[wikilinks]]` unless the user explicitly asks for an Obsidian wiki.

For important claims, include one of:

- source file path and heading
- chat filename plus timestamp or turn marker
- URL
- command, commit, issue, or local artifact path

Mark inferred relationships as inference. Do not rewrite stale chat claims as current truth.

## Optional OKF Strict Mode

Use only on request. OKF strict mode adds:

- YAML frontmatter on every concept file
- non-empty `type`
- reserved `index.md` and `log.md` rules
- bundle-relative Markdown links
- validator run before completion

Before making OKF conformance claims, load `references/okf-strict.md` and run:

```bash
cd <skill-root>
python3 scripts/okf_validate.py /path/to/bundle
```

## Completion Report

Report:

- handoff root
- files created or updated
- source set covered
- current-state summary
- decisions added or changed
- open questions and next tasks
- whether OKF strict validation was requested and passed
- what the next agent should read first

## Do Not

- Do not dump raw chat logs into the handoff pack.
- Do not make every message or sentence a page.
- Do not hide uncertainty.
- Do not let old chat conclusions override newer evidence.
- Do not create manifest files, broad evals, or governance metadata unless the user asks.
- Do not use OKF strict mode as the default.
