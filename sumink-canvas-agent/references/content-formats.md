# Content Formats

Use this before writing notes, rich text nodes, mentions, formulas, tables, code blocks, or images.

## Notes

Use notes for durable, searchable units:

- claim
- evidence
- source summary
- paragraph candidate
- relation explanation
- task list

Use canvas nodes for local labels and temporary instructions.

## Markdown

Sumink-flavored Markdown supports:

````markdown
## Heading
- Bullet
1. Numbered
- [ ] Todo
- [x] Done

**bold** *italic* `code`
[link](https://example.com)
<span color="red">colored text</span>

Inline math: $E=mc^2$

$$
F = ma
$$

| Claim | Evidence |
|---|---|
| A | B |

```mermaid
flowchart LR
  A --> B
```
````

Notes:

- headings 4-6 become heading 3
- use `<empty_block/>` for intentional blank lines
- ordinary blank lines may be normalized

## Mentions

Use mentions for stable relations:

```markdown
<mention type="note" id="CARD_ID">Optional name</mention>
<mention type="note" id="CARD_ID"/>
```

Resolve real IDs first. Preserve mention attributes when rewriting.

## Images

Create the attachment:

```bash
sumink_cli attachment add figure.png --format json
```

Use it in a note:

```markdown
![640x360](attachment:ATTACHMENT_ID)
```

Or on a canvas:

```xml
<canvas_image src="attachment:ATTACHMENT_ID" width="640" height="360"/>
```

Limits:

- accepted: PNG, JPEG/JPG, WebP
- SVG rejected; convert to PNG
- unreferenced attachments may be cleared
- add caption/OCR if the image carries meaning

## Tables

Use GFM tables for simple cells. Use XML table syntax only for merged cells or multi-block content.
