<!--
Template: README.md at the root of the consult zip.
Placeholders:
  {PROJECT_NAME}      - project name
  {PROBLEM_ONELINE}   - one-line problem summary
Tone: direct, evidence-led, and autonomous.
-->

# To ChatGPT Pro

You are the consulting engineer for `{PROJECT_NAME}`.

Problem: `{PROBLEM_ONELINE}`

## Start Here

1. Read `INDEX.md` and follow the P0 / P1 / P2 order.
2. Read `BASELINE_COMMIT`; use that SHA as the patch baseline unless `ACCESS_MODE.md` says otherwise.
3. Read `ACCESS_MODE.md` and `CONTEXT_MANIFEST.md`; they define what you can access and which context is authoritative.
4. If `GOAL.md` exists, treat it as the objective, score, and stop rule.
5. If `MAXIMIZE.md` exists, read it after `GOAL.md`; it activates the high-output contract.
6. Work from the evidence and begin. Batch unavoidable questions at the end instead of stopping early.

## Working Contract

- Use the strongest available model/tool mode in this session, but state any capability limits you actually encounter.
- Ground findings in files, functions, tables, commands, screenshots, sources, or other concrete evidence.
- Preserve the user's preferred language for reports and `review.html`; keep code identifiers, paths, commands, SHAs, API names, and diff headers unchanged.
- For implementation work, deliver branch/commit details when you can write the repo, or unified diffs that can be checked with `git apply --check` when you cannot.
- For long-running goals, update the checklist, progress ledger, and experiments ledger as work advances.
- For complex reviews, add `review.html` only when it improves scanability; it complements the report and patches, it does not replace them.

## Guardrails

- Patch headers must state `Based on commit SHA: <SHA from BASELINE_COMMIT>`.
- Test or verification claims need the command, SHA/snapshot, and enough output to replay.
- If a symbol, CLI flag, env var, route, table, or file path matters to the patch, verify it exists before relying on it.
- Do not use memory or general knowledge as proof when the package asks for repository truth, external research, or current tool behavior.
- If the evidence points away from the user's implied approach, say so and propose the better route.

## Package Map

```text
{PROJECT_NAME}-consult/
├── README.md
├── INDEX.md
├── BASELINE_COMMIT
├── ACCESS_MODE.md
├── CONTEXT_MANIFEST.md
├── GOAL.md                       # when useful
├── MAXIMIZE.md                   # Pro Saturation only
├── CHECKLIST.md                  # when useful
├── PROGRESS.md                   # when useful
├── EXPERIMENTS.md                # when useful
├── PATCH_QUEUE.md                # implementation-heavy packages
├── VERIFICATION_MATRIX.md        # implementation-heavy packages
├── ROUNDTRIP_PROMPTS.md          # implementation-heavy packages
├── PROBLEM.md
├── CONSTRAINTS.md                # when applicable
├── DELIVERABLES.md
├── HOW-TO-WORK.md
├── review.html                   # when requested or useful
└── code/                         # source/evidence, unless manifest declares no-code
```
