---
name: geb-context-map
description: Use when maintained codebase work risks context bloat from large diffs, module boundaries, doc drift, GEB maps, L1/L2/L3 docs, or requests to avoid reading everything.
---

# GEB Context Map

IRON LAW: MAP BEFORE LOADING. Keep out any file, doc, log, or repo pack that will not change the current decision.

GEB is a context-saving map, not a documentation project. Load the smallest useful context and sync only changed code facts.

## Use Gate

Use only for maintained codebases when one is true:

- New repo or module onboarding.
- Large diff, multi-file work, architecture change, or public-surface change.
- User asks to save context, avoid reading everything, or apply GEB.
- Agent docs, module maps, file contracts, or doc drift affect the work.

Stop for throwaway scripts, prose/data/media/email tasks, local edits with no boundary impact, or global doc/hook audits unless explicitly requested.

## Core Rule

Locate before loading. Read only the nearest useful layer:

| Layer | Read or maintain | When it matters |
|---|---|---|
| L1 | Root `AGENTS.md`, `CLAUDE.md`, README, or project map | New repo, cross-module work, architecture or command changes |
| L2 | Nearest module `AGENTS.md`, `CLAUDE.md`, `INDEX.md`, or module note | Module work or public-surface changes |
| L3 | Target file header, docstring, exports/imports, or role comment | Core entrypoint, service, schema, adapter, API handler, state, permission, or data-access file |

## Workflow Checklist

1. Gate: if the use gate fails, stop.
2. Locate first with `rg --files`, Serena/LSP, `ast-grep`, `jq`, or `repomix --token-count-tree`.
3. Load only layers that change the edit boundary. If current guidance supplies L1, do not reread it.
4. State the boundary in 5 lines or fewer: read layers, likely touched files, ignored files.
5. Work from the narrowest useful evidence.
6. Finish from the diff. Update L3 for responsibility/import/export changes; L2 for membership/public-surface changes; L1 for top-level structure, commands, stack, or architecture rules.

## Write Rules

- L1/L2 should be maps: paths, commands, module boundaries, public surfaces, invariants.
- L3 should be a compact role contract. Add it only to core boundary files, not helpers.
- If no GEB docs exist, do not seed a full system during routine work.
- Keep generated docs short enough to be useful in context. Delete stale or duplicate text instead of adding explanations.

## Red Flags

- Reading a repo pack, long log, or full file before locating the slice.
- Creating `INDEX.md` trees, commit hooks, or all-file headers without an explicit request.
- Updating docs broadly because "GEB says so".
- Writing philosophy, process history, or personal preference into project maps.
- Using GEB as a reason to load more context than the task needs.

If any red flag appears, return to Step 2 and shrink the context surface before continuing.

## Pre-Delivery Check

- [ ] Use was appropriate, not forced onto a small task.
- [ ] No repo pack, long log, or broad file read was loaded without a reason.
- [ ] L1/L2/L3 edits match changed code facts.
- [ ] Final report states updated or skipped layers when GEB affected the work.

## Final Report

When this skill affected a coding task, include:

```text
GEB:
- L3: updated / no update, reason
- L2: updated / no update, reason
- L1: updated / no update, reason
- Context: largest thing avoided or offloaded, if relevant
```
