# Eval: Obsidian Canvas Card Writing

Use this after edits or when route quality is uncertain.

## RED Baseline

Observed with AGPair task `TASK-CA76DA32CFC6` before this skill existed:

- The agent produced a useful generic model but inspected unrelated repository files instead of staying anchored to the target vault/canvas.
- It treated some visual details, such as resize and proximity, as stronger intent than the Canvas format can prove.
- It did not provide a compact, reusable operating checklist for card-first, canvas-second writing.

## GREEN Scenario

Positive prompt:

```text
Create an Obsidian Canvas workflow for turning a research conversation into Markdown cards, letting the human rearrange them, then drafting an article from the board.
```

Expected behavior:

- Finds or creates a topic folder with `Cards/`, `.canvas`, and draft `.md`.
- Writes durable ideas as Markdown cards before creating Canvas file nodes.
- Uses group nodes for paragraph/argument clusters and labeled edges for relations.
- Parses the Canvas after writing and validates node IDs, edge endpoints, and file paths.
- Interprets human edits with confidence levels.
- Treats proximity, unlabeled lines, unlabeled boxes, color, and resize as low-confidence signals.
- Drafts only after rereading changed cards and reporting draft-changing ambiguity.

## Boundary Scenarios

Use the skill:

```text
Read this Obsidian .canvas and its Cards folder, infer paragraph groups from labeled boxes and connector labels, then write Draft.md.
```

Do not use the skill:

```text
Make a generic flowchart in JSON Canvas for a system architecture.
```

Expected route: `json-canvas`.

Do not use the skill:

```text
Explain Obsidian wikilink syntax and callouts.
```

Expected route: `obsidian-markdown`.

Risk scenario:

```text
These two cards are close together but not inside a group and their connector has no label. Turn them into a paragraph.
```

Expected behavior: mark the relation as low confidence and ask if the grouping changes the draft.

## Near Neighbors

- Generic mind maps, flowcharts, or diagrams: use `json-canvas`.
- Obsidian Markdown syntax only: use `obsidian-markdown`.
- Obsidian plugin or app debugging: use `obsidian-cli`.
