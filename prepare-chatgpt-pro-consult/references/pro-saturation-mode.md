# Pro Saturation Mode

Use this reference only when the user explicitly wants to maximize ChatGPT Pro, squeeze ChatGPT Pro, spend more compute, get the deepest possible analysis, or obtain the largest safe engineering patch stack.

This mode optimizes for maximum useful engineering throughput, not minimum package size.

## Activation

Trigger this mode for wording such as:

- "maximize ChatGPT Pro"
- "squeeze ChatGPT Pro"
- "榨干 ChatGPT Pro"
- "深入到无法更深入"
- "maximum engineering code"
- "largest patch stack"
- "let it work as long as possible"

Do not activate this mode for ordinary focused bug fixes, small refactors, or quick architecture questions.

## Current Capability Assumption

Before relying on exact ChatGPT Pro behavior, re-check current official OpenAI docs. As of 2026-06-20, official OpenAI help describes Pro as including Pro models, Codex, deep research, memory, and file uploads. Limits, model names, model picker behavior, connectors, and sandbox behavior can still change, so the package must include probes and fallbacks.

## Package Additions

Add these files in addition to the normal consult package:

```
ACCESS_MODE.md           # selected live/zip/browser/no-write route and probes
MAXIMIZE.md              # filled from templates/MAXIMIZE-template.md
CONTEXT_MANIFEST.md      # what context was included, omitted, and why
PATCH_QUEUE.md           # ordered patch stack, from must-fix to stretch
VERIFICATION_MATRIX.md   # commands, probes, expected output, ownership
ROUNDTRIP_PROMPTS.md     # next prompts for the same ChatGPT Pro thread
RESEARCH_SOURCES.md      # only when external benchmarks/docs matter
```

Use `MAXIMIZE.md` as the remote model's high-output contract. Use the other files to prevent "deep analysis" from becoming an unbounded essay.

## Context Strategy

Give ChatGPT Pro layered context:

- P0: `BASELINE_COMMIT`, `ACCESS_MODE.md`, `CONTEXT_MANIFEST.md`, `GOAL.md`, `MAXIMIZE.md`, `PROBLEM.md`, `DELIVERABLES.md`, `HOW-TO-WORK.md`
- P1: source files and tests required for the first patch stack
- P2: adjacent callers, data contracts, schemas, fixtures, config, docs
- P3: optional references, benchmark notes, prior failed attempts, screenshots

Prefer several focused bundles over one indiscriminate repository dump. Name bundles by purpose:

```
code/core-bundle.xml
code/tests-bundle.xml
code/contracts-bundle.xml
code/docs-bundle.xml
```

Every bundle must explain why it exists in `CONTEXT_MANIFEST.md`.

Load `references/package-execution-contract.md`, `references/context-tool-ladder.md`, and `references/repomix-context-packaging.md` before collecting code. In this mode, `repomix` is the default reproducible bundle generator and must be used as a focused context packager, not a reflexive whole-repo dump. Use `--stdin` for curated file sets, `--include`/`--ignore` for clean module boundaries, `--token-count-tree` for triage, and `--split-output` for large bundles. Record every part in `CONTEXT_MANIFEST.md`. Include source-backed portable artifacts that can be rechecked against `BASELINE_COMMIT`.

Run discovery in passes:

1. Broad orientation: file tree, manifests, package boundaries, likely owners, and repo maps when useful.
2. Task trace: files and symbols for the concrete user problem.
3. Patch trace: tests, fixtures, migration paths, rollback surfaces, downstream callers.

Use the local tool stack without asking the user to enable optional context tools:

- `rg --files`
- `rg` for symbols, routes, tables, CLI flags, config keys, and error strings
- `git grep` when tracking only committed source is useful
- focused `repomix` bundles, preferably generated from explicit include patterns or `--stdin`
- direct file copies
- `jq` for structured config and manifests
- optional symbol/structure tools such as Serena/LSP, `ast-grep`/`sg`, tree-sitter, or repo mapping tools when installed and useful

## Remote Work Contract

Tell ChatGPT Pro to use the strongest available Pro model and any available Deep Research, Agent, Codex, file, or connector capability that helps. If those features are unavailable in the session, it must state that and continue with the zip path.

The desired output is not "recommendations". It is a large, verified engineering work product:

1. repository truth reconstruction
2. external research where relevant
3. independent analysis lanes
4. explicit decision model
5. ordered patch queue
6. as many safe PR-sized diffs or commits as it can produce
7. tests and verification matrix
8. rollback and migration notes
9. updated ledgers
10. `review.html`

Require a patch stack, not one heroic mega-patch. Each patch should be independently reviewable, checkable, and reversible.

## Minimum Output Bar

For implementation-heavy asks, reject output that lacks any of:

- concrete code diffs or branch/commit details
- tests or test-update diffs where behavior changes
- `git apply --check` recipe for every diff
- symbol/CLI/env-var verification notes
- a ranked `PATCH_QUEUE.md`
- a `VERIFICATION_MATRIX.md`
- rollback notes for each patch
- updated `CHECKLIST.md`, `PROGRESS.md`, and `EXPERIMENTS.md`

If ChatGPT Pro cannot run tests or write files, it must still output apply-checkable diffs plus exact local replay commands.

## Stop Rules

The model should keep going until one of these is true:

- the goal score is met and verification evidence is attached
- no additional patch can be produced without crossing a red line
- required runtime, credentials, private data, or user decision is missing
- the session/tooling refuses further work

"The topic is broad", "this is a lot", or "I recommend future work" is not a stop rule.

## Anti-Patterns

Do not accept:

- only a report
- only a roadmap
- pseudocode instead of patches
- one tiny patch when several safe patches are obvious
- invented APIs, flags, or imports
- patches without baseline SHA
- unbounded rewrite with no rollback path
- dumping the entire repo without a context manifest
- starting a new ChatGPT thread for v2 when the same thread can continue

## Local Review Loop

After ChatGPT Pro returns v1:

1. Save every diff separately.
2. Run `git apply --check` against the baseline or current SHA specified by the patch.
3. Grep-verify referenced symbols, flags, env vars, routes, tables, and files.
4. Run the narrowest meaningful tests.
5. Mark each patch accepted, modified, rejected, or blocked.
6. Send one compact v2 prompt from `ROUNDTRIP_PROMPTS.md` back to the same ChatGPT Pro thread.

The best loop is not one huge final answer. It is a high-output v1 followed by evidence-rich v2 and v3 passes against the same thread.
