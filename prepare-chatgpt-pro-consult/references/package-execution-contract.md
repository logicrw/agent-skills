# Package Execution Contract

Use this after Phase 1 for any large, unfamiliar, multi-module, Pro saturation, or long-running ChatGPT Pro consult package.

## Job

Turn the tool ladder into concrete artifacts. The package must show what the local agent knew, which tools it tried, what context it uploaded, what it omitted, and how ChatGPT Pro should return patches.

## Required Artifacts

Create these for every non-trivial package:

- `ACCESS_MODE.md`: selected route, probes, limits, and what ChatGPT Pro may do.
- `CONTEXT_MANIFEST.md`: tool attempts, included bundles, direct-copy files, omissions, context risks, and privacy review.

The minimum package must still include a replay path: baseline SHA, relevant artifacts, instructions for how to verify or locally replay claims, and an explicit reason for any omitted code. If source code is not in scope, write `No code package: yes - <reason>` in `CONTEXT_MANIFEST.md`. Do not create dummy `code/` files to satisfy the checker.

Create these for Pro saturation, patch-producing long-running goals, or implementation-heavy consults:

- `PATCH_QUEUE.md`: ordered patch stack from must-fix to stretch.
- `VERIFICATION_MATRIX.md`: commands, probes, expected output, owner, and evidence status.
- `ROUNDTRIP_PROMPTS.md`: v2/v3 prompts for the same ChatGPT Pro thread after local review.

For a long-running analysis-only goal, `GOAL.md`, `CHECKLIST.md`, `PROGRESS.md`, and `EXPERIMENTS.md` are enough. Add the patch trio only when patches or code changes are in scope.

## Access Mode

Choose exactly one initial mode:

- `live-github`: ChatGPT Pro can clone, install, test, and write a branch.
- `zip-only`: ChatGPT Pro can read uploaded files but cannot write the repository.
- `browser-only`: ChatGPT Pro can browse docs/repo pages but cannot reliably run shell commands.
- `no-write-analysis`: the task is analysis-only; patches are out of scope.

Record the probe output that selected the mode. If the probe changes later, update `ACCESS_MODE.md` and `PROGRESS.md` before asking for v2.

## Context Assembly

Use `references/context-tool-ladder.md` for tool routing and `references/repomix-context-packaging.md` for bundle construction.

Rules:

- `repomix` is the default portable bundle generator.
- Build `repomix` inputs from explicit include patterns, `rg --files`, manifests, changed files, tests, or hand-curated `--stdin` file lists.
- Use `repomix --stdin` when the review needs a precise, auditable file set; save the file list beside the bundle or reproduce it in `CONTEXT_MANIFEST.md`.
- Use `repomix --include` and `--ignore` when module boundaries are clean; record both patterns exactly.
- Run a token/size triage pass before broad packaging, such as `repomix --stdin --token-count-tree 100 --no-files < context-files.txt`.
- Use `rg`, `git grep`, `jq`, Serena/LSP, `ast-grep`/`sg`, tree-sitter, or repo mapping tools to verify symbols, routes, schemas, config keys, and boundaries before packaging.
- Direct source copies override compressed summaries when exact line-level patching matters.
- `repomix --compress` is an orientation artifact, not the only source of truth.
- `repomix --split-output` is required when one bundle is too large to upload or scan comfortably.
- `repomix --include-diffs` is required when dirty working-tree changes are intentionally part of the consult.
- `repomix --include-logs --include-logs-count N` is useful for history-sensitive review; keep N small and record why history is included.
- Avoid `--output-show-line-numbers` as the only patch source. It is fine for review-only evidence, but line prefixes can confuse generated diffs.
- Never use `--no-security-check` for uploadable packages.

Dirty worktree policy:

- Clean committed state is preferred.
- Dirty state is allowed only when the user wants current uncommitted work included.
- If dirty state is included, record every dirty file, include a diff artifact, and say whether patches target committed HEAD or the dirty snapshot.
- If dirty state is unrelated or ambiguous, stop and ask one narrow question before packaging.

## Pre-Zip Gate

Before zipping, run:

```bash
scripts/check-consult-package.sh <consult-dir>
```

Resolve `scripts/` relative to the directory that contains this skill's `SKILL.md`.

Failure means the package is not ready. Fix missing files, unreplaced placeholders, missing code artifacts without an explicit no-code rationale, or unsafe contents before upload.

## Local Review Gate

After ChatGPT Pro returns v1:

1. Save every patch separately.
2. Run `git apply --check` for each patch.
3. Run commands from `VERIFICATION_MATRIX.md` when possible.
4. Mark each patch accepted, modified, rejected, or blocked in `PATCH_QUEUE.md`.
5. Send one prompt from `ROUNDTRIP_PROMPTS.md` back to the same ChatGPT Pro thread.

Do not start a fresh thread for v2 unless the original thread is unusable.
