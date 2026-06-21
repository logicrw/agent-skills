# Human Collaboration

Use this after the human edits, groups, frames, connects, labels, or rearranges a board.

## Loop

1. Agent creates cards, sections, relationship notes, and a rough canvas.
2. Human edits visually.
3. Agent reads back and states its interpretation.
4. Human corrects only ambiguous points.
5. Agent drafts, reorganizes, or exports.

## Read Human Intent

| Human action | Agent reading |
|---|---|
| Cards close together | weak group; verify if draft-changing |
| Cards inside section/frame | strong group if readback shows `canvas_section` |
| Box around cards | group only if readback or label supports it |
| Text on box/section | group label |
| Connector line | relation exists, type unknown |
| Connector label | relation verb or discourse role |
| Card text edit | re-read card before drafting |
| Row/column order | draft order if no stronger signal conflicts |
| Human says "these form one paragraph" | create or use a section; draft one paragraph |
| Human says "these support one claim" | group as evidence under that claim |
| Human leaves unlabeled drawing | treat as visual hint, not durable semantics |

## Confidence

- High: section name, relationship note, mention/backlink, labeled connector, explicit node
- Medium: clear section membership or clear visual order
- Low: unlabeled proximity, unlabeled box, unlabeled connector, ambiguous x/y

Mark low-confidence readings plainly.

## Section Protocol

When cards are framed as one paragraph or argument:

1. Find `canvas_section name=...`.
2. Resolve child `canvas_embed cardId=...`.
3. Read card content.
4. Check nearby notes or labels.
5. Draft one paragraph or cluster summary.

If no section is readable, propose a relationship note instead of assuming.

## Connector Protocol

1. Map endpoints from `canvas_connector` to `canvas_embed`.
2. Preserve the label.
3. Empty label means only "visually connected".
4. If the connector touches a relationship note, read that note as semantics.

## Response Shape

```text
我读到的结构：
- Section「论点 A」包含：卡 1、卡 2、卡 3。可合成一个段落。
- 连接线「前因」：卡 1 -> 卡 2。
- 不确定：左下两张卡靠近，但没有 section 或标签。
```

Ask only about uncertainty that changes the draft.

## Drafting

- section name -> paragraph role or subsection
- cards in section -> paragraph material
- relationship note -> discourse logic
- connector label -> transition or relation phrase
- explicit order -> section order -> labeled arrows -> spatial order
- image -> use caption/OCR, not the image reference alone

## Export

For article output:

1. Build an outline from sections and relationship notes.
2. Collapse each section into one paragraph unless the section is clearly a chapter.
3. Use connector labels as transition phrases.
4. Put low-confidence visual readings in questions or comments.

For agent handoff:

1. Convert canvas interpretation into `ai-handoff-pack` files.
2. Store current state, decisions, open questions, tasks, entities, and source anchors.
3. Do not export raw canvas JSON as the handoff unless explicitly requested.
