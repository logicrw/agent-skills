# Behavior Review

Use this after changing the skill or checking whether another agent follows it.

## Routing

| Prompt | Expected |
|---|---|
| "Turn this conversation into Obsidian cards and place them on a Canvas" | use skill |
| "Read the groups, lines, and card order in this Canvas" | use skill |
| "I framed several cards together; turn them into paragraph structure" | use skill |
| "Merge these cards into one argument card" | use skill, confirm before merge |
| "Draw a generic system flowchart" | use `json-canvas` |
| "Explain Obsidian wikilink syntax" | use `obsidian-markdown` |

## Behavior

| Scenario | Pass |
|---|---|
| New cards from notes | searches first, writes Markdown cards, then creates file nodes |
| Existing cards | rereads before edit; preserves wording unless asked to rewrite |
| Human group box | validates group containment and states confidence |
| Human labeled edge | maps endpoints and preserves label |
| Unlabeled proximity | marks low confidence; does not treat as durable meaning |
| Merge request | rereads both cards, preserves source trails, asks before merging |
| Delete/archive request | asks first; follows existing vault convention |
| Draft/output | rereads cards and Canvas; reports source cards, skipped cards, uncertainty |

## Risk Checks

- No vault root: stop before creating cards or file nodes.
- Dangling edge endpoint: fix or report before drafting.
- Missing file node target: create the card first or remove the node.
- Canvas text node with durable meaning: promote it to Markdown before final output.
- No generic smoke script: Obsidian validation is vault-specific. For real work, parse the target `.canvas`, resolve file nodes, and check edge endpoints.

## Near Neighbors

- Generic mind maps, flowcharts, or diagrams: use `json-canvas`.
- Obsidian Markdown syntax only: use `obsidian-markdown`.
- Obsidian plugin or app debugging: use `obsidian-cli`.
