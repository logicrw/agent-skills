# Repomix Context Packaging

Use this during Phase 2 when collecting source for a ChatGPT Pro consult package.

Repomix is not only a whole-repo packer. Treat it as a reproducible context packager: choose files first, then pack the chosen set with recorded commands.

## Default Stance

- Do not dump the whole repo unless the repo is small and the token/size budget proves it is safe.
- Prefer exact source bundles over compressed summaries for patch-producing work.
- Use compressed/orientation bundles only as maps, not as the patch authority.
- Keep security checks enabled for every uploadable bundle.
- Record every command, include/exclude pattern, stdin file list, split part, warning, and omission in `CONTEXT_MANIFEST.md`.

## Selection Ladder

1. Start from repository evidence:
   ```bash
   git rev-parse HEAD
   git status --short
   rg --files > context-file-candidates.txt
   ```
2. Add files by intent:
   ```bash
   git diff --name-only >> context-files.raw
   git diff --cached --name-only >> context-files.raw
   rg -l "<route|symbol|error|config-key>" app scripts tests docs >> context-files.raw
   git ls-files "app/**" "scripts/**" "tests/**" "docs/**" >> context-files.raw
   ```
3. Add authority files manually: package manifests, DB schemas, migrations, config, tests, fixtures, README/AGENTS, and docs that define the contract.
4. Normalize:
   ```bash
   sort -u context-files.raw | sed '/^$/d' > context-files.txt
   ```
5. Token-check before packing:
   ```bash
   repomix --stdin --token-count-tree 100 --no-files < context-files.txt
   ```
6. If the set is too large, cut by authority:
   - Keep source, tests, schemas, migrations, config, and contract docs.
   - Move broad docs and adjacent modules into an orientation bundle.
   - Omit generated files, caches, vendored dependencies, large fixtures, screenshots, and logs unless they are evidence.

## Bundle Types

Exact source bundle for patches:

```bash
repomix --stdin --style xml --parsable-style -o code/core-bundle.xml < context-files.txt
```

Orientation bundle for broad architecture:

```bash
repomix --include "app/**,scripts/**,tests/**,docs/**,*.md" \
  --ignore "node_modules/**,dist/**,build/**,.venv/**,output/**" \
  --compress --style xml --parsable-style -o code/orientation-bundle.xml
```

Dirty-state bundle when current uncommitted behavior matters:

```bash
repomix --stdin --style xml --parsable-style \
  --include-diffs --include-logs --include-logs-count 10 \
  -o code/dirty-context-bundle.xml < context-files.txt
```

Large package split:

```bash
repomix --stdin --style xml --parsable-style \
  --split-output 2mb -o code/core-bundle.xml < context-files.txt
```

Repeatable config for complex packages:

```bash
repomix -c consult-repomix.config.json
```

Use a temporary or consult-package-local config when include/ignore/output/security settings are complex. Do not add or change a project-root `repomix.config.json` unless the user wants that repo behavior changed. If a config file is used, include it in the consult package or copy its relevant settings into `CONTEXT_MANIFEST.md`.

Metadata-only sizing pass:

```bash
repomix --include "app/**,tests/**" --token-count-tree 500 --no-files
```

## Choosing Flags

Use by default:

- `--style xml`: stable for mixed code and markdown.
- `--parsable-style`: prevents code fences or XML-like code from breaking the bundle.
- `--stdin`: best for hand-curated or search-derived file sets.
- `--include` / `--ignore`: best for clear module or directory boundaries.
- `--token-count-tree`: decide what to cut before upload.
- `--split-output`: keep each upload part readable and within UI limits.

Use only when appropriate:

- `--compress`: orientation only. Do not make it the only source artifact for patches.
- `--include-diffs`: required when dirty worktree changes are part of the consult.
- `--include-logs --include-logs-count N`: useful for history-sensitive reviews; keep N small.
- `--output-show-line-numbers`: useful for review-only packages; avoid as the only patch source because line prefixes can confuse generated diffs.
- `--remove-comments` / `--remove-empty-lines`: use for orientation or very large packages, not when comments document behavior or tests.
- `--instruction-file-path`: optional convenience; package docs still remain the authority.

Avoid:

- `--no-security-check` for anything uploaded to ChatGPT Pro.
- `--no-gitignore`, `--no-default-patterns`, or broad `**/*` unless you have a specific reason and record it.
- A single huge full-repo bundle with no file map, token triage, or omissions.

## Manifest Entries

For each bundle, record:

| Field | Required content |
| --- | --- |
| Selection source | include patterns, `context-files.txt`, direct files, or command that produced the list |
| Command | exact `repomix` command and working directory |
| Output | file path and split parts |
| Purpose | patch source, orientation, evidence, dirty diff, or logs |
| Authority | exact source, bundle, orientation, or evidence |
| Size/token note | token tree summary or reason it fits |
| Omissions | what was intentionally left out and why |
| Security | security check result or manual review note |

ChatGPT Pro should be told which bundle is authoritative for patches. Usually `code/core-bundle.xml` is authoritative; orientation bundles are supporting context only.
