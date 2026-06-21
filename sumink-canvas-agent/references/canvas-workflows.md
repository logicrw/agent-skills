# Canvas Workflows

Use this before creating or reading canvases, sections, embeds, images, or nested boards.

## Model

A Sumink canvas is a writing board plus a drawing surface. The CLI creation format covers the writing-board subset, not every drawing feature.

## Agent-Writable Elements

```xml
<node color="blue" width="600">
## Heading or instruction
</node>

<embed_note cardId="NOTE_ID" color="green" width="420"/>

<embed_note name="New note" color="green">
Note body.
</embed_note>

<embed_canvas cardId="CANVAS_ID" color="violet" width="420" height="315"/>

<embed_canvas name="Sub-board" color="violet">
  <node>Sub-board note</node>
</embed_canvas>

<section name="Argument: evidence for claim A" color="yellow">
  <node>These cards form one paragraph.</node>
  <embed_note cardId="A_ID"/>
  <embed_note cardId="B_ID"/>
</section>

<canvas_image src="attachment:ATTACHMENT_ID" width="640" height="360"/>
```

Read back after writing.

## Sections

Use `section` for:

- same paragraph
- same argument
- same evidence bundle
- same subsection
- review together

Name sections semantically. Avoid `Group 1`.

Local test confirmed `canvas read` preserves section name and child embeds.

Caveats:

- section children must be XML elements
- direct Markdown inside `<section>` is ignored
- child coordinates may read back as absolute
- keep rich children simple
- add a relationship note when section meaning must survive export

## Relationship Notes

For durable semantics:

```markdown
<mention type="note" id="A_ID"/> --supports--> <mention type="note" id="B_ID"/>

Meaning: A supplies evidence for B.
Writing action: put A before B in the same paragraph.
```

Mentions create backlinks.

## Connectors

Human-drawn labeled connectors can be read:

```xml
<canvas_connector label="前因" from="note" to="note_3"/>
```

Treat them as visual intent. Do not rely on CLI-created connectors; local tests showed they may be dropped.

Preserve connector labels exactly.

## Layout

Prefer readable rough layout:

- left to right for flow
- top to bottom for outline
- sections for groups
- nodes for headings
- relationship notes for durable meaning

Omit `x` and `y` when placement is unimportant. Use `canvas append` for additions, not precise repair. For careful layout, create a new canvas or ask the human to arrange it.

## Nested Canvases

Use `embed_canvas` for chapters, subtopics, source maps, or deep argument branches. Do not create hierarchy unless it helps inspection.
