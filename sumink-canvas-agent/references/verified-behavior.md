# Verified Behavior

Use this when a claim depends on observed Sumink behavior.

Tested 2026-06-21:

- app `0.40.0`
- CLI `0.1.0`
- a local test space

## Official Signals

- homepage: write, draw, organize on infinite canvas
- homepage: backlinks, Markdown syntax, block editor, hand-drawn shapes, connectors, polyline
- v0.39: Plex graph
- v0.38: image insertion/cropping, grouping/hierarchy, search index rebuild
- v0.37: connector labels, arrow endpoints, stroke styles, quick connect, improved sections
- v0.36: canvas image export and copy

## Local Tests

### Rich note

`Skill测试：富文本卡片能力` read back headings, todos, table, inline math, display math, and Mermaid code text.

### Section as paragraph container

Canvas `Skill测试：section 作为论点容器`, ID `9c683d3f-cea9-4335-bb27-863d1f75e40a`, read back:

```xml
<canvas_section name="论点容器：共同论据组">
  <canvas_embed cardId="cf00bf1a-bfa4-4515-8e0f-283c98915283"/>
  <canvas_embed cardId="0c561944-3579-4809-b2bb-7538e695201e"/>
</canvas_section>
```

Use sections for same paragraph, same argument, same evidence bundle.

### Mentions and backlinks

Relationship note `Skill测试：共同论据关系索引`, ID `e6c6ed7a-e05b-441b-aa00-4812c515e7a0`, produced inline backlinks. The section canvas produced embed backlinks.

Use relationship notes plus mentions for stable semantics.

### Nested canvas

`embed_canvas name="Skill测试：子画布-章节草稿"` created child canvas ID `5acf651f-342a-428e-8407-1331e83eb788`.

Use nested canvases for chapters or subtopics.

### Attachment image

Canvas `Sumink 隐藏功能实测：附件图片进画布`, ID `cafd077f-5b9d-40b3-9c45-6899a55a6005`, read back `canvas_image src="attachment:0e125a7d-0ba1-40fe-9dfa-d63b0207e01b"`.

SVG attachment was rejected. PNG/JPEG/WebP work.

### Human connector labels

Canvas `关系索引演示：不用连接线也能表达关系`, ID `b1b6dea9-5ae3-4d43-9378-c80928d2574a`, read back:

```xml
<canvas_connector label="前因" from="note" to="note_3"/>
<canvas_connector label="后果" from="note_3" to="note_2"/>
```

Human-drawn connector labels are readable.

### Caveats

- CLI-created connectors may be dropped.
- `sumink help` is invalid; use `sumink --help`.
- `card search` has no `--fields`.
