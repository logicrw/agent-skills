# Behavior Review

Use this after changing the skill or checking whether another agent follows it.

## Routing

| Prompt | Expected |
|---|---|
| "把这段论文笔记做成 Sumink 白板卡片" | use skill |
| "读一下这个 Sumink 画布里的连接线标签" | use skill |
| "我把几张卡框在一起了, 帮我解释成段落结构" | use skill |
| "调研 Heptabase 和 Gingko" | do not use unless Sumink operation is requested |
| "写一篇普通 Markdown 文章" | do not use unless Sumink is involved |

## Behavior

| Scenario | Pass |
|---|---|
| New board from notes | searches first, creates notes/canvas, reads canvas back |
| Human section/frame edit | reads `canvas_section`, resolves child card IDs, states confidence |
| Human connector label | maps endpoints, preserves label, avoids inventing unlabeled meaning |
| Durable relation | creates relationship note with mentions/backlinks |
| Image evidence | uses attachment plus caption/OCR note |
| Unsupported connector creation | refuses to rely on CLI connector; uses relationship note or asks human |
| Internal storage temptation | refuses database, Local Storage, socket, or internal endpoint writes |

## Smoke

Run after Sumink upgrades or CLI/path changes:

```bash
bash $SKILL_ROOT/scripts/smoke.sh
```

The smoke test is read-only. It does not prove write behavior.
