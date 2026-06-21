---
name: sumink-canvas-agent
description: "Use when working with Sumink or Summer Ink canvases for human-agent visual writing: text-to-card boards, human-edited layouts, connector labels, sections, backlinks, attachments, or drafting from board structure."
allowed-tools: Bash(sumink *) Bash(node /Applications/Sumink.app/Contents/Resources/cli/cli.cjs *) Bash(jq *) Bash(mktemp *) Bash(qlmanage *)
metadata:
  sumink-app-version-tested: "0.40.0"
  sumink-cli-version-tested: "0.1.0"
  last-tested: "2026-06-21"
---

# Sumink Canvas Agent

IRON LAW: READ BACK EVERY WRITE. A SUMINK COMMAND SUCCEEDING DOES NOT PROVE THE CANVAS KEPT THE STRUCTURE.

Operate Sumink as a shared visual writing desk. The agent writes cards, sections, embeds, links, images, and drafts. The human edits the board visually. The agent reads it back, resolves meaning, and turns it into structure or prose.

## Workflow

```text
Sumink Progress
- [ ] 1. Connect
- [ ] 2. Load only the needed reference
- [ ] 3. Search before creating
- [ ] 4. Write or update
- [ ] 5. Read back
- [ ] 6. Interpret human edits
- [ ] 7. Report IDs, meaning, limits
```

## 1. Connect

Install Sumink from `https://www.sumink.com/download`. Use global `sumink` when present. Fall back to the app bundle.

```bash
if command -v sumink >/dev/null 2>&1; then
  sumink_cli() { sumink "$@"; }
else
  sumink_cli() { node /Applications/Sumink.app/Contents/Resources/cli/cli.cjs "$@"; }
fi
sumink_cli --version
sumink_cli space list --format json
```

Before any mutation, read `references/cli-safety.md`.

If the CLI is not ready, run `sumink_cli launch --format json`. If it still fails, ask the user to open Sumink and enable CLI features. Do not edit app state files.

## 2. Load References

Load only what the task needs.

| Task | Reference |
|---|---|
| Notes, Markdown, formulas, tables, mentions, images | `references/content-formats.md` |
| Canvas, sections, embeds, nested boards, layout | `references/canvas-workflows.md` |
| Human drag/drop edits, frames, connector labels, grouping | `references/human-collaboration.md` |
| Capability decision: agent-direct vs human-assisted vs UI-only | `references/capability-matrix.md` |
| Evidence for local behavior | `references/verified-behavior.md` |
| Failed writes or odd CLI behavior | `references/troubleshooting.md` |

## 3. Search Before Creating

```bash
sumink_cli card search "<query>" --format json
```

Use IDs, not names, when names may collide.

## 4. Choose The Object

| Intent | Use |
|---|---|
| Durable idea, claim, source, evidence, paragraph unit | note |
| Local label, heading, instruction, caption | canvas node |
| Place an existing card | `embed_note` |
| Chapter or subtopic drill-down | `embed_canvas` |
| Same paragraph, same argument, same evidence bundle | `section name="..."` |
| Relationship that must survive export | relationship note with `<mention .../>` |
| Human-readable relation direction | human-drawn connector label |
| Figure, screenshot, generated diagram | attachment plus `canvas_image` plus caption |

Do not rely on CLI-created connectors. If meaning matters, add a section label or relationship note.

## 5. Read Back

After every canvas create/append:

```bash
sumink_cli canvas read <canvasId> --format json
```

For important cards:

```bash
sumink_cli backlink list <cardId> --format json
```

Interpret by evidence strength:

1. relationship notes, mentions, backlinks
2. `canvas_section name="..."` with child embeds
3. labeled `canvas_connector`
4. nearby explanatory nodes
5. spatial order or proximity

If sources conflict, report the conflict and ask which one controls the draft.

## 6. Human Collaboration

Human owns fast visual intent: drag, frame, group, label, connect, reorder, edit by sight. Agent owns durable structure: cards, sections, mentions, backlinks, relationship notes, readback, and prose.

For human-edited boards, load `references/human-collaboration.md`. State only draft-changing uncertainty; do not ask about every small placement choice.

Core readings: frame/section means "these belong together"; section label means paragraph or argument role; connector label means relation or transition; card edit supersedes earlier agent text; proximity is weak unless backed by label, section, or relationship note.

## 7. Deliver

Return:

- canvas name and ID
- important note/card IDs
- created or updated objects
- readback evidence
- interpretation of sections, connectors, mentions, backlinks, and order
- UI-only or human-assisted steps still needed
- temporary test cards kept or trashed

If the user wants a non-visual handoff, export the board interpretation with `ai-handoff-pack`: current state, decisions, open questions, tasks, source anchors, and entity notes. Do not export raw canvas JSON as the handoff.

If the user wants an article, draft from strongest structure first: relationship notes and backlinks, then sections, then labeled connectors, then nearby explanatory nodes, then visual order. Preserve unresolved ambiguity as comments or questions rather than silently choosing.

## Maintenance

After Sumink upgrades or skill edits:

```bash
cd <skill-root>
bash scripts/smoke.sh
```

For behavior review, use `references/behavior-review.md`.

## Do Not

- Do not write Sumink database, Local Storage, cache, sockets, or internal endpoints.
- Do not claim a connector, section, image, or embed exists unless readback shows it.
- Do not treat x/y position alone as final meaning.
- Do not infer unlabeled connectors or boxes.
- Do not use `canvas append` for precise layout repair.
- Do not leave important relations only in visuals; add a relationship note.
- Do not make every sentence a permanent card.

## Checklist

- [ ] CLI and active space checked.
- [ ] Required reference loaded.
- [ ] Existing cards searched.
- [ ] Canvas writes read back.
- [ ] IDs captured.
- [ ] Groups backed by `canvas_section` or marked as inference.
- [ ] Connectors backed by `canvas_connector label=...`.
- [ ] Durable relations backed by notes, mentions, backlinks, or section labels.
- [ ] Unsupported actions named plainly.
