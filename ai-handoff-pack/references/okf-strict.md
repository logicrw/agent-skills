# OKF Strict Mode

Use this only when the user asks for OKF, Open Knowledge Format, LLM-Wiki compliance, or a portable bundle that other OKF consumers should validate.

OKF is a portable Markdown bundle convention. It is not the default handoff format.

## Hard Rules

- Every non-reserved `.md` file is a concept document.
- Every concept document starts with parseable YAML frontmatter.
- Every concept frontmatter block has a non-empty `type`.
- `index.md` and `log.md` follow reserved file rules when present.

Reserved filenames:

- `index.md`: optional directory listing for progressive disclosure.
- `log.md`: optional update history.

## Recommended Frontmatter

```yaml
type: Decision
title: Use Sumink For Visual Handoff
description: Sumink is the preferred visual canvas for AI-assisted card writing.
resource: /sources.md
tags: [handoff, sumink]
timestamp: 2026-06-21T00:00:00Z
```

Only `type` is required. Preserve unknown keys.

## Links

Use standard Markdown links. Prefer bundle-relative links:

```markdown
[Sumink](./entities/sumink.md)
```

Do not use `[[wikilinks]]` in OKF strict mode.

## Validation

```bash
cd <skill-root>
python3 scripts/okf_validate.py /path/to/bundle
```

Treat missing optional fields, missing indexes, unknown types, and broken links as warnings unless the user asked for cleanup.

## Report

When claiming OKF conformance, report:

- bundle path
- validation command
- error count
- warning count
- files repaired
- remaining assumptions
