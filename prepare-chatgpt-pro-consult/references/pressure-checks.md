# Pressure Checks

Use these scenarios after changing tool routing, templates, package contents, or ChatGPT Pro engagement rules.

## Scenario 1: Large Repo, Focused Context

Prompt:

> Prepare a ChatGPT Pro consult package for a large multi-module repo. Use the best available context tools and keep the upload focused.

Expected behavior:

- Use `rg --files`, targeted `rg`/`git grep`, manifests, changed files, tests, optional symbol tools, and focused `repomix`.
- Produce `CONTEXT_MANIFEST.md` with tool attempts, bundle map, omissions, and privacy review.
- Do not ask the user to enable optional context tools when `repomix` and direct source copies can build the package.

## Scenario 2: Pro Saturation, Zip-Only

Prompt:

> Squeeze ChatGPT Pro as hard as possible. It cannot clone the private repo, so use a zip.

Expected behavior:

- Activate Pro Saturation Mode.
- Create `MAXIMIZE.md`, `ACCESS_MODE.md`, `PATCH_QUEUE.md`, `VERIFICATION_MATRIX.md`, and `ROUNDTRIP_PROMPTS.md`.
- Require apply-checkable diffs, not just recommendations.
- Run `scripts/check-consult-package.sh` before zipping.

## Scenario 2b: Selective Repomix Context

Prompt:

> Prepare a ChatGPT Pro consult package for a large repo. The bug likely involves three modules and two tests. Do not upload unrelated code.

Expected behavior:

- Build `context-files.txt` from `git diff --name-only`, targeted `rg -l`, manifests, tests, and hand-added authority docs.
- Run a token triage pass with `repomix --stdin --token-count-tree ... --no-files`.
- Produce a focused `code/core-bundle.xml` from `repomix --stdin`, not a whole-repo dump.
- Optionally produce an orientation bundle with `--compress`, clearly marked as non-authoritative for patches.
- Record selection commands, omitted modules, and bundle authority in `CONTEXT_MANIFEST.md`.

## Scenario 3: Dirty Worktree

Prompt:

> Package this repo for ChatGPT Pro. There are uncommitted local changes and I want the current behavior reviewed.

Expected behavior:

- Record dirty files in `BASELINE_COMMIT` and `CONTEXT_MANIFEST.md`.
- Include a diff artifact or `repomix --include-diffs`.
- State whether patches target committed HEAD or the dirty snapshot.
- Ask only if dirty changes look unrelated or ambiguous.

## Scenario 4: Small Local Fix

Prompt:

> Fix this one failing unit test in a small file.

Expected behavior:

- Do not use this skill unless the user explicitly asks for ChatGPT Pro handoff.
- Keep the work local.
- Do not build a consult package.

## Scenario 5: Analysis-Only Consult

Prompt:

> Prepare a ChatGPT Pro consult package for a no-write architecture decision. I do not want patches.

Expected behavior:

- Use `ACCESS_MODE.md` with `no-write-analysis`.
- Produce `CONTEXT_MANIFEST.md` with `No code package: yes - <reason>` only if code is genuinely out of scope.
- Do not create `PATCH_QUEUE.md`, `VERIFICATION_MATRIX.md`, or `ROUNDTRIP_PROMPTS.md`.
- `scripts/check-consult-package.sh` passes the no-code package only when the no-code rationale is explicit.

## Scenario 6: Long-Run Analysis Goal

Prompt:

> Let ChatGPT Pro keep working on a competitive research plan until the checklist is complete, but no code changes are requested.

Expected behavior:

- Create `GOAL.md`, `CHECKLIST.md`, `PROGRESS.md`, and `EXPERIMENTS.md`.
- Do not require the patch trio unless implementation enters scope.
- Keep a replayable evidence/checklist loop instead of forcing fake code patches.

## Scenario 7: Repomix Missing

Prompt:

> Prepare a ChatGPT Pro consult package. `repomix` is not installed.

Expected behavior:

- Do not ask the user to install or open tools unless the package cannot be built any other way.
- Use `rg --files`, targeted `rg`/`git grep`, and direct source copies under `code/direct/`.
- Record the missing `repomix` fallback in `CONTEXT_MANIFEST.md`.
- Treat direct copies as source authority.

## Scenario 8: Medium Consult Without HTML

Prompt:

> Prepare a focused ChatGPT Pro consult for a two-module refactor plan. I only need the report and diffs.

Expected behavior:

- Use the Standard or Implementation tier, not Pro Saturation.
- Do not require `MAXIMIZE.md`.
- Do not require `review.html` unless the findings become complex or the user asks for a visual artifact.
- Keep patch and verification requirements if implementation is in scope.

## Pass Criteria

The skill passes only if future agents choose the right mode, produce the required artifacts, and avoid asking the user to manually enable optional tools.
