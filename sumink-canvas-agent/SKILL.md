---
name: sumink-canvas-agent
description: "Use when working with Sumink or Summer Ink cards and canvases: conversation-to-cards, card creation, card editing, sections, frames, connector labels, mentions, backlinks, relationship notes, attachments, human-edited boards, outlines, drafts, or synthesis from board structure."
allowed-tools: Bash(sumink *) Bash(node /Applications/Sumink.app/Contents/Resources/cli/cli.cjs *) Bash(jq *) Bash(mktemp *) Bash(qlmanage *)
metadata:
  sumink-app-version-tested: "0.40.0"
  sumink-cli-version-tested: "0.1.0"
  last-tested: "2026-06-21"
---

# Sumink Canvas Card Work

IRON LAW: Read back every write. A Sumink command succeeding does not prove the board kept the intended structure.

Use this skill to operate Sumink cards safely. The human owns the evolving knowledge system. The agent owns clean card creation, careful edits, explicit relations, reliable readback, and traceable outputs.

This skill is independent. Do not assume any other app exists unless the user asks for migration or sync.

## Work Loop

0. Connect [BLOCKING]
   - Use global `sumink` when present; fall back to the app bundle.
   - Check CLI version and active space.
   - Before mutation, read `references/cli-safety.md`.
1. Scope
   - Identify space, target canvas, search terms, output need, and whether the user wants new cards or updates.
   - Search existing cards before creating. Use IDs when names may collide.
2. Read
   - Read target canvas, relevant notes, sections, embeds, connector labels, mentions, and backlinks.
   - Treat memory of prior layout as stale until readback confirms it.
3. Distill
   - Turn input into reusable notes, not a transcript dump.
   - One card = one idea, question, source, evidence item, method, counterpoint, synthesis, or draft fragment.
   - Use notes for durable meaning; use canvas nodes for local labels, headings, captions, or instructions.
4. Operate
   - Create notes for durable cards.
   - Embed notes on canvas for visual work.
   - Use sections for themes, arguments, paragraphs, projects, evidence bundles, or open problems.
   - Split broad cards. Link only when the relation is explicit or useful.
   - Delete, merge, archive, or overwrite only after rereading and explicit confirmation.
5. Relate
   - Use mentions, backlinks, or relationship notes for durable relations.
   - Use section labels for groups that should survive readback.
   - Use human connector labels as readable local relations.
   - Do not rely on CLI-created connectors for important meaning.
6. Read Back [REQUIRED]
   - Read the canvas after every create or append.
   - Read important notes and backlink lists.
   - Report unsupported or UI-only actions plainly.
7. Output
   - Produce the requested board update, interpretation, outline, draft, memo, plan, book skeleton, or question list.
   - Return IDs, evidence, cards used, cards skipped, and unresolved ambiguity.

## Connect

```bash
if command -v sumink >/dev/null 2>&1; then
  sumink_cli() { sumink "$@"; }
else
  SUMINK_APP_CLI="${SUMINK_APP_CLI:-/Applications/Sumink.app/Contents/Resources/cli/cli.cjs}"
  sumink_cli() { node "$SUMINK_APP_CLI" "$@"; }
fi
sumink_cli --version
sumink_cli space list --format json
```

If the CLI is not ready, run `sumink_cli launch --format json`. If it still fails, ask the user to open Sumink and enable CLI features. Do not edit app state files.

## References

Load only what the task needs.

| Task | Reference |
|---|---|
| Notes, Markdown, formulas, tables, mentions, images | `references/content-formats.md` |
| Canvas, sections, embeds, nested boards, layout | `references/canvas-workflows.md` |
| Human drag/drop edits, frames, connector labels, grouping | `references/human-collaboration.md` |
| Capability decision: agent-direct vs human-assisted vs UI-only | `references/capability-matrix.md` |
| Evidence for local behavior | `references/verified-behavior.md` |
| Failed writes or odd CLI behavior | `references/troubleshooting.md` |

## Commands

```bash
sumink_cli card search "<query>" --format json
sumink_cli canvas read <canvasId> --format json
sumink_cli backlink list <cardId> --format json
```

Use `sumink --help`; `sumink help` is invalid.

## Operations

| Task | Rule |
|---|---|
| Create | search first; create note; embed on canvas when visual work is needed |
| Edit | reread note; preserve user wording unless asked to rewrite |
| Link | use mention/backlink or relationship note for durable meaning |
| Group | use named section for theme, argument, paragraph, project, evidence bundle, or open problem |
| Connect | rely on readback connector labels; otherwise use relationship notes |
| Merge | confirm; preserve source trails; do not silently discard disagreement |
| Archive | use the user's existing convention; otherwise ask |
| Delete/trash | confirm; trash only agent-created temporary cards unless asked otherwise |
| Draft | reread notes, canvas, sections, and backlinks; state skipped cards and uncertainty |

## Object Map

| Need | Use |
|---|---|
| durable thought | note |
| source record | note or link |
| visual placement | embedded note |
| theme or argument | section |
| durable relation | relationship note, mention, backlink |
| local visual relation | labeled connector |
| chapter or subtopic | nested canvas |
| figure or screenshot | attachment image plus caption |

## Readback

Interpret by evidence strength:

1. note text, relationship notes, mentions, backlinks
2. named sections with child embeds
3. labeled connectors
4. nearby explanatory nodes
5. spatial order or proximity

When sources conflict, prefer note text, mentions, backlinks, and section labels over position. Ask only if the conflict changes the requested output.

Core readings: section means "these belong together"; connector label means relation or transition; card edit supersedes earlier agent text; proximity is weak unless backed by label, section, mention, backlink, or relationship note.

## Synthesis

Order material by: explicit section or user order, relationship notes and backlinks, section membership, labeled connector direction, visual row or column order, then proximity.

Map sections to headings, claims, themes, or project stages. Use notes as material. Use relationship notes as logic. Use connector labels as transitions. Preserve low-confidence visual readings as questions or comments.

## Do Not

- Do not write Sumink database, Local Storage, cache, sockets, or internal endpoints.
- Do not claim a section, connector, image, embed, mention, or backlink exists unless readback shows it.
- Do not treat x/y position alone as final meaning.
- Do not infer strong meaning from unlabeled connectors, unlabeled boxes, color, or resize.
- Do not use `canvas append` for precise layout repair.
- Do not leave important relations only in visuals.
- Do not turn transcripts into exhaustive card dumps.
- Do not make every sentence a permanent card.
- Do not sync or mirror to another app unless the user explicitly asks.

## Checks

- [ ] CLI and active space checked.
- [ ] Required reference loaded.
- [ ] Existing cards searched.
- [ ] Canvas writes read back.
- [ ] IDs captured.
- [ ] Durable relations backed by notes, mentions, backlinks, sections, or connector labels.
- [ ] Unsupported actions named plainly.
- [ ] Output names source cards, skipped cards, and unresolved ambiguity.

After Sumink upgrades or skill edits:

```bash
cd <path-to-skill>/sumink-canvas-agent
bash scripts/smoke.sh
```

For behavior review, use `references/behavior-review.md`.
