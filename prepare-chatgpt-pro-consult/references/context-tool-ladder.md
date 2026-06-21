# Context Tool Ladder

Use this during Phase 2 code collection when the repo is large, unfamiliar, multi-module, or the package is in Pro Saturation Mode.

The goal is not to use every tool. The goal is to produce a source-backed, portable context package that ChatGPT Pro can read deeply and that the local agent can verify against `BASELINE_COMMIT`.

## Principle

`repomix` is the default packaging tool. Search, git, and symbol tools define and verify the scope before packaging. For detailed recipes, use `references/repomix-context-packaging.md`.

- `repomix` produces reproducible upload artifacts: stable repository snapshots, include/exclude filters, token counts, security checks, split output, and portable XML/Markdown/JSON/plain output.
- `rg`, `git grep`, manifests, changed files, tests, and docs build the first candidate file list.
- Serena/LSP, `ast-grep`/`sg`, `tree-sitter`, `jq`, and repo mapping tools are gap closers: they prove that selected files, functions, routes, flags, env vars, schemas, and tests actually exist.
- Direct source copies are for exact line-level evidence when compressed or bundled context is not precise enough.

## Routing Order

1. Establish baseline:
   - `git rev-parse HEAD`
   - `git status --short`
   - `rg --files`
   - package manifests, test config, routing/config entrypoints
2. Build a first candidate file list with `rg --files`, manifests, docs, changed files, tests, and known symbols.
3. Refine the candidate list with:
   - `rg` / `git grep` for caller strings, routes, commands, errors, and config keys
   - Serena/LSP definitions and references when available
   - `ast-grep` or `sg` structural searches when installed
   - `jq` for structured JSON manifests, package files, config, and lockfiles
   - repo mapping or tree-sitter tools for module orientation when useful
4. Build portable bundles with `repomix`:
   - focused include patterns for source and tests
   - `--stdin` from `context-files.txt` when selection must be precise
   - `--token-count-tree` when deciding what to omit
   - `--compress` only for orientation bundles, not as the only source artifact
   - `--include-diffs` when working tree changes matter
   - `--include-logs --include-logs-count N` when recent history matters
   - `--split-output` when a bundle is too large for upload
   - `--parsable-style` for XML/Markdown robustness when code contains fence-like text
5. Copy critical files directly when exact line-level review matters.
6. Close gaps with search and symbol tools:
   - `rg` for text, errors, routes, CLI flags, config keys, env vars
   - `git grep` for committed-source-only searches
   - `jq` for JSON manifests, lockfiles, and structured config
   - Serena/LSP for definitions, references, and diagnostics when available
   - `ast-grep` or `sg` for structural code patterns when installed
7. Record the result in `CONTEXT_MANIFEST.md`.

## Replacement Matrix

| Need | First choice | Fallback | Not enough by itself |
| --- | --- | --- | --- |
| Discover relevant modules | `rg --files`, manifests, docs, git history | repo mapping tools, LSP references | Full repo dump |
| Build uploadable code package | `repomix` | direct file copies, zip source subset | UI state or prior chat |
| Preserve orientation | `repomix --compress`, repo mapping summary | direct architecture notes with file paths | text search only |
| Verify symbols/imports/routes | Serena/LSP, `rg`, `git grep` | direct reads | LLM memory |
| Find structured patterns | `ast-grep`/`sg` | `rg` plus direct reads | broad natural-language summary |
| Track included/omitted context | `CONTEXT_MANIFEST.md` | `PROBLEM.md` file map | implicit memory |

## Default Recipes

Focused `repomix` package:

```bash
rg --files > context-file-candidates.txt
rg "<symbol|route|error|config-key>" -n
repomix --include "src/**,tests/**,*.md" --ignore "dist/**,build/**,node_modules/**" --style xml --parsable-style -o code/core-bundle.xml
```

Curated file-list package:

```bash
git diff --name-only > context-files.raw
rg -l "<symbol|route|error|config-key>" src tests docs >> context-files.raw
sort -u context-files.raw > context-files.txt
repomix --stdin --token-count-tree 100 --no-files < context-files.txt
repomix --stdin --style xml --parsable-style -o code/core-bundle.xml < context-files.txt
```

`repomix` unavailable:

```bash
mkdir -p code/direct
while IFS= read -r file; do
  mkdir -p "code/direct/$(dirname "$file")"
  cp "$file" "code/direct/$file"
done < context-files.txt
find code/direct -type f | sort > code/direct-file-list.txt
```

Record this fallback in `CONTEXT_MANIFEST.md`; direct copies become the source authority.

Precise file list:

```bash
rg --files | rg '^(src|tests|docs)/' > context-files.txt
repomix --stdin --style xml --parsable-style -o code/core-bundle.xml < context-files.txt
```

Token triage:

```bash
repomix --include "src/**,tests/**" --token-count-tree 500 --no-files
```

Large bundle split:

```bash
repomix --stdin --style xml --parsable-style --split-output 2mb -o code/core-bundle.xml < context-files.txt
```

## Manifest Requirements

Record:

- tools attempted and whether each succeeded
- `repomix` include/exclude patterns, flags, output filenames, and split parts
- `context-files.txt` source and path when `--stdin` was used
- any direct-copy files and why exact source was needed
- symbols/routes/tests/configs verified by `rg`, `git grep`, Serena/LSP, or structural tools
- important files intentionally omitted and why
- secret-scan or manual review result before upload

Never treat `repomix`, LSP, memory, repo maps, or a prior chat as authority. The authority is the checked-out repository at `BASELINE_COMMIT`, plus explicit user constraints and verification output.
