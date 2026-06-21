---
name: obsidian-canvas-card-writing
description: "Use when a task involves Obsidian Canvas as a writing board: Markdown cards, .canvas layouts, card sorting, group boxes, labeled connectors, research synthesis, paper notes, canvas-to-outline, card-to-draft, card-to-article, reading human-edited boards, or drafting prose from Obsidian cards. Not for generic diagrams."
---

# Obsidian Canvas Card Writing

IRON LAW: Read the cards and the canvas before claiming structure or drafting. Markdown owns text; Canvas owns layout.

Use Obsidian as a file-native writing board. The agent writes cards and structure. The human edits the board by sight. The agent reads it back and drafts.

**REQUIRED SUB-SKILLS:** `obsidian-markdown` for card files; `json-canvas` for `.canvas`.

Red flags: no vault root, missing file paths, dangling edges, unlabeled visual inference, stale memory of human edits. Stop and read back.

## Workflow

1. Scope [BLOCKING]
   - Identify vault root, topic folder, card folder, canvas path, draft path.
   - Search existing topic cards and canvases before creating.
2. Cards first
   - Put durable ideas in `.md`: one claim, evidence item, example, counterpoint, source, or transition per card.
   - Use Canvas text nodes only for headings, labels, scratch notes, or instructions.
   - Promote draft-changing text nodes into cards before final drafting.
3. Canvas second
   - Use vault-relative `file` nodes for cards.
   - Use `group` nodes for paragraphs, sections, arguments, sources, or evidence bundles.
   - Use labeled edges for local rhetorical relations.
   - Preserve human layout unless asked to rebuild it.
4. Read back [REQUIRED]
   - Parse Canvas JSON.
   - Validate IDs, node types, edge endpoints, and file paths.
   - Re-read changed cards before drafting.
5. Draft [REQUIRED]
   - State groups, order, edges, orphans, and low-confidence readings.
   - Ask only about ambiguity that changes the draft.
   - Confirm before deleting cards, overwriting human edits, or replacing human layout.
   - Write the outline or prose to the requested Markdown draft.

## Object Map

| Need | Use |
|---|---|
| Durable text | Markdown card |
| Visual placement | Canvas `file` node |
| Paragraph or argument | Canvas `group` node |
| Local heading or note | Canvas `text` node |
| Source URL | Canvas `link` node or Markdown link |
| Local relation | Labeled edge |
| Vault-wide relation | Wikilink, backlink, tag, or property |
| Final article | Markdown draft |

Default shape: `Topic/Cards/`, `Topic/Topic.canvas`, `Topic/Draft.md`.

Minimal card properties: `type: card`, `status`, `role`, `order`, `source`. Use them only when they help sorting or drafting.

## Readback

Ask:

1. Which file nodes point to real cards?
2. Which group bounds contain which card nodes?
3. What do group labels say?
4. Which edges connect cards, and what are their labels?
5. Which cards are orphaned, duplicated, or disconnected?
6. Which cards changed since the previous pass?

Containment: a card is inside a group when its node box is fully inside the group box. Allow small drag drift. Treat partial overlap as low confidence. If several groups contain it, use the smallest one.

Evidence:

| Strength | Signals |
|---|---|
| High | card text, explicit properties, labeled group, contained file node, labeled edge, wikilink/backlink |
| Medium | clear group containment, consistent row or column, nearby heading text |
| Low | proximity, partial overlap, unlabeled connector, unlabeled box, color, resize |

When signals conflict, prefer card text and explicit labels over position.

## Drafting

Order:

1. explicit `order`
2. group order
3. labeled edge direction
4. row or column order
5. proximity

Map group labels to headings or paragraph roles. Use contained cards as paragraph material. Use edge labels as transitions. Use `role: evidence` to support the nearest claim, `role: counter` as contrast, and orphan cards as a review list unless asked to include all cards.

Before drafting, report draft-changing uncertainty. After drafting, report draft path, cards used, cards skipped, and unresolved structure.

## Do Not

- Do not route generic Canvas diagrams here; use `json-canvas`.
- Do not infer strong meaning from position, color, resize, unlabeled lines, or unlabeled boxes.
- Do not make every sentence a permanent card.
- Do not leave final prose dependent on Canvas-only text nodes.
- Do not overwrite human-edited cards without rereading them.
- Do not create file nodes before target Markdown files exist.
- Do not edit Obsidian plugin state, caches, databases, or internal app files.

## Checks

- [ ] Existing topic files searched.
- [ ] Durable content is in `.md` cards.
- [ ] Canvas JSON parses.
- [ ] Edge endpoints resolve.
- [ ] File nodes use vault-relative paths and point to existing files.
- [ ] Group and edge readings include confidence.
- [ ] Draft output names source cards and unresolved cards.

For behavior review, use `references/behavior-review.md`.
