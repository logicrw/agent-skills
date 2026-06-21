# Troubleshooting

Use this when commands fail or readback disagrees with intent.

## CLI Not Ready

```bash
sumink_cli launch --format json
sumink_cli space list --format json
```

If still failing, ask the user to open Sumink and enable CLI features. Do not edit `state.json`.

## Help

`sumink help` is invalid. Use `sumink --help`.

## Search vs List

`card search` finds cards. It does not support `--fields`.

`card list` supports fields:

```bash
sumink_cli card list --fields all,content --type note --limit 20 --format json
```

Use `note read` or `canvas read` for exact targets.

## Unknown Embed Names

`canvas read` may show `name="Unknown note"`. Resolve by `cardId`:

```bash
sumink_cli card get <cardId> --format json
```

## Section Missing Or Broken

Check:

- children are XML elements
- no direct Markdown inside `<section>`
- simple nodes and embeds only
- readback confirms the section

Fallback: heading nodes plus relationship note.

## Connector Missing

If a written connector is absent from readback, treat it as failed. Use a relationship note or ask the human to draw and label it.

Empty connector label means only "visually connected".

## Attachment Rejected

Check MIME type. Convert SVG/PDF/other formats to PNG/JPEG/WebP. Reference the attachment immediately from a note or canvas.

## Layout Wrong

`canvas append` is not precise layout repair. Inspect existing markup, create a new canvas, or ask the human to arrange visually.

## Stop

Stop and report unsupported when the request requires:

- full drawing automation through CLI
- reliable automatic connector creation
- direct DB/storage mutation
- claims not supported by readback
