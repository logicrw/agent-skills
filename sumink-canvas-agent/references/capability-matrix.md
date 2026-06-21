# Capability Matrix

Use this to decide whether a requested Sumink action is agent-direct, human-assisted, or UI-only.

## Agent-Direct

| Action | Notes |
|---|---|
| create/read/edit notes | Sumink-flavored Markdown |
| create/read canvases | lossy readback |
| append canvas content | placement may drift |
| embed notes | `embed_note` |
| create notes from canvas | `embed_note name=...` |
| embed/create nested canvases | `embed_canvas` |
| create sections | read back to verify |
| add canvas images | PNG/JPEG/WebP attachments |
| create mentions/backlinks | best durable relation layer |
| list backlinks | embeds and mentions count |
| search cards | `card search`; no `--fields` |
| list content | `card list --fields all,content` |
| trash temporary cards | reversible; use sparingly |

## Human-Assisted, Readable

| Action | Agent handling |
|---|---|
| drag/reorder cards | weaker than labels/sections |
| draw connector | read only if returned |
| label connector | strong visual relation |
| draw frame/section | strong if `canvas_section`; cautious if unlabeled shape |
| edit embedded note | re-read note |
| export/copy Markdown | UI or CLI readback |
| export canvas image | UI snapshot |
| presentation mode | human review |

## UI-Only Or Unreliable

| Action | Handling |
|---|---|
| reliable CLI connector creation | use human connector or relationship note |
| full drawing/shape/polyline automation | UI action |
| crop image | UI action |
| Plex graph manipulation | verify before relying |
| built-in AI client | do not assume it replaces external agents |
| direct DB edits | forbidden |

## Best Division Of Labor

Agent:

- split notes into cards
- create sections and relationship notes
- attach figures with captions
- read human-edited boards
- draft from sections and links

Human:

- drag cards
- label frames
- label connector lines
- edit wording
- judge the board visually
