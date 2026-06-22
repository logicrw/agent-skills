---
name: obsidian-canvas-card-writing
description: "Use when a task involves Obsidian Markdown cards and Canvas maps: conversation-to-cards, card creation, card editing, card linking, card sorting, group boxes, labeled edges, human-edited boards, canvas-to-outline, card-to-draft, research synthesis, or long-form writing. Not for generic diagrams or format-only .canvas edits."
---

# Obsidian Canvas Card Work

IRON LAW: Cards are the durable unit. Canvas is the visual work surface. Read before acting; read back after acting.

Use this skill to operate Obsidian cards safely. The human owns the evolving knowledge system. The agent owns clean card creation, careful edits, explicit links, reliable readback, and traceable outputs.

**REQUIRED SUB-SKILLS:** `obsidian-markdown` for cards; `json-canvas` for `.canvas`.

## Work Loop

0. Scope [BLOCKING]
   - Identify vault root, topic folder, card folder, canvas path, and output path.
   - Search existing cards and canvases before creating.
   - Do not create cards or file nodes until the vault root is known.
1. Read
   - Read relevant cards, canvas nodes, edges, groups, and recent human edits.
   - Treat memory of prior layout as stale until the files are read.
2. Distill
   - Turn input into reusable cards, not a transcript dump.
   - One card = one idea, question, source, evidence item, method, counterpoint, synthesis, or draft fragment.
   - Keep cards self-contained enough to survive outside the current board.
3. Operate
   - Create Markdown cards before Canvas file nodes.
   - Edit existing cards in place when meaning is preserved.
   - Split broad cards; merge only after rereading both cards and confirming.
   - Delete or archive only with explicit user approval.
4. Relate
   - Use wikilinks, backlinks, tags, or properties for vault-wide meaning.
   - Use Canvas groups and labeled edges for local thinking and writing structure.
   - Promote important Canvas text nodes into Markdown cards.
5. Read Back [REQUIRED]
   - Parse Canvas JSON.
   - Validate node IDs, edge endpoints, node types, and vault-relative file paths.
   - Report groups, edges, orphan cards, skipped cards, and uncertainty.
6. Output
   - Produce the requested board update, outline, draft, memo, plan, book skeleton, or question list.
   - Name source cards and unresolved structure.

## Operations

| Task | Rule |
|---|---|
| Create | search first; write `.md`; then place file node |
| Edit | reread card; preserve user wording unless asked to rewrite |
| Link | use wikilink for durable relation; edge label for local relation |
| Group | use Canvas group for theme, argument, section, project, evidence bundle, or open problem |
| Merge | confirm; preserve source trails; do not silently discard disagreement |
| Archive | use the vault's existing convention; otherwise ask |
| Delete | confirm; prefer archive when the vault already has an archive convention |
| Draft | reread cards and Canvas; state skipped cards and uncertainty |

## Object Map

| Need | Use |
|---|---|
| durable thought | Markdown card |
| source record | source card or source link |
| visual placement | Canvas `file` node |
| local label | Canvas `text` node |
| theme or argument | Canvas `group` |
| local relation | labeled edge |
| vault-wide relation | wikilink, backlink, tag, property |
| final artifact | Markdown draft |

Optional starter shape: `Topic/Cards/`, `Topic/Topic.canvas`, `Topic/Draft.md`. Follow the existing vault structure when one exists.

Optional useful properties: `type`, `status`, `role`, `source`, `created`, `order`. Add them only when they help search, sorting, or synthesis.

## Readback

Ask:

1. Which file nodes point to real cards?
2. Which group bounds contain which cards?
3. What do group labels say?
4. Which edges connect cards, and what are their labels?
5. Which cards are orphaned, duplicated, stale, or disconnected?
6. Which cards changed since the previous pass?

Containment: a card is inside a group when its node box is fully inside the group box. Allow small drag drift. Treat partial overlap as low confidence. If several groups contain it, use the smallest one.

| Strength | Signals |
|---|---|
| High | card text, explicit properties, wikilinks, labeled group, contained file node, labeled edge |
| Medium | clear group containment, consistent row or column, nearby heading text |
| Low | proximity, partial overlap, unlabeled connector, unlabeled box, color, resize |

When signals conflict, prefer card text, explicit labels, and links over position.

## Synthesis

Order material by: explicit `order`, group order, labeled edge direction, row or column order, then proximity.

Map group labels to headings, claims, themes, or project stages. Use contained cards as material. Use edge labels as transitions or logic. Treat `role: evidence` as support, `role: counter` as contrast, and `role: question` as unresolved unless answered elsewhere.

Ask only about ambiguity that changes the output.

## Do Not

- Do not route generic Canvas diagrams here; use `json-canvas`.
- Do not turn transcripts into exhaustive card dumps.
- Do not make every sentence a permanent card.
- Do not leave durable meaning only in Canvas text nodes.
- Do not infer strong meaning from position, color, resize, unlabeled lines, or unlabeled boxes.
- Do not create file nodes before target Markdown files exist.
- Do not overwrite, merge, delete, or archive human-edited cards without rereading and confirming.
- Do not edit Obsidian plugin state, caches, databases, or internal app files.
- Do not sync or mirror to another app unless the user explicitly asks.

## Checks

- [ ] Vault root, topic folder, card folder, canvas path, and output path are known.
- [ ] Existing cards and canvases were searched.
- [ ] Durable content is in Markdown cards.
- [ ] Canvas JSON parses.
- [ ] Edge endpoints resolve.
- [ ] File nodes use vault-relative paths and point to existing files.
- [ ] Output names source cards, skipped cards, and unresolved cards.

For route checks, use `references/behavior-review.md`.
