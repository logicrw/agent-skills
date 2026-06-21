# CLI Safety

Use this before any Sumink mutation.

## Entry

Prefer global `sumink`. On this machine `~/.local/bin/sumink` forwards to the app CLI.

```bash
if command -v sumink >/dev/null 2>&1; then
  sumink_cli() { sumink "$@"; }
else
  sumink_cli() { node /Applications/Sumink.app/Contents/Resources/cli/cli.cjs "$@"; }
fi
sumink_cli --version
sumink_cli --help
```

Tested locally:

- app `0.40.0`
- CLI `0.1.0`

If versions differ, run help and a smoke test before trusting old behavior.

## Help

`sumink help` is invalid.

```bash
sumink_cli --help
sumink_cli <command> --help
sumink_cli <command> <subcommand> --help
```

Read built-in resources before writing unfamiliar content:

```bash
sumink_cli resource read introduction --format text
sumink_cli resource read sumink-flavored-markdown --format text
sumink_cli resource read infinity-canvas-markup --format text
```

## Output

Use `--format json`. Errors become JSON on stdout and still return a failing exit code.

Exit codes:

- `0`: success
- `1`: business error
- `64`: usage error

## Boundary

Write only through the CLI or the human UI. Never write:

- `sumink.db`
- Local Storage / LevelDB
- app caches
- sockets
- internal endpoints
- extracted app files

Package inspection is allowed for research, not for production writes.

## Search

```bash
sumink_cli card search "<query>" --format json
```

`card search` has no `--fields`. For content listing:

```bash
sumink_cli card list --fields all,content --format json
```

Use card IDs when names collide.

## Mutation Rules

- Use `--content-file` for multiline content.
- Do not repeat the note title as the first heading.
- Read back every create, append, edit, and canvas write.
- Trash only agent-created temporary cards unless the user asks otherwise.
