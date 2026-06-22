# Behavior Review

Use this after changing the skill or checking whether another agent follows it.

## Routing

| Prompt | Expected |
|---|---|
| "Turn these paper notes into Sumink canvas cards" | use skill |
| "Read the connector labels on this Sumink canvas" | use skill |
| "I framed several cards together; explain the paragraph structure" | use skill |
| "Research Heptabase and Gingko" | do not use unless Sumink operation is requested |
| "Write a plain Markdown article" | do not use unless Sumink is involved |

## Behavior

| Scenario | Pass |
|---|---|
| New board from notes | searches first, creates notes/canvas, reads canvas back |
| Human section/frame edit | reads `canvas_section`, resolves child card IDs, states confidence |
| Human connector label | maps endpoints, preserves label, avoids inventing unlabeled meaning |
| Durable relation | creates relationship note with mentions/backlinks |
| Image evidence | uses attachment plus caption/OCR note |
| Unsupported connector creation | refuses to rely on CLI connector; uses relationship note or asks human |
| Merge request | rereads both notes, preserves source trails, asks before merging |
| Delete/archive request | asks first; trashes only agent-created temporary cards unless asked otherwise |
| Draft/output | rereads notes, canvas, sections, backlinks; reports skipped cards and uncertainty |
| Internal storage temptation | refuses database, Local Storage, socket, or internal endpoint writes |

## Smoke

Run after Sumink upgrades or CLI/path changes:

```bash
bash $SKILL_ROOT/scripts/smoke.sh
```

The smoke test is read-only. It does not prove write behavior.
