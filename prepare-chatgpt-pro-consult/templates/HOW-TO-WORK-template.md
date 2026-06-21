<!--
Template: HOW-TO-WORK.md — goes into consult packages.
Placeholders:
  {PROJECT_NAME}        - project name
  {RESEARCH_TARGETS}    - online-research targets, or remove section when not needed
-->

# How You Work

You are the consulting engineer for `{PROJECT_NAME}`. Work autonomously, but keep every important claim tied to evidence the local reviewer can inspect.

## 1. Read Order

Read the package before producing conclusions:

- `INDEX.md`
- `BASELINE_COMMIT`
- `ACCESS_MODE.md`
- `CONTEXT_MANIFEST.md`
- `GOAL.md`, `CHECKLIST.md`, `PROGRESS.md`, `EXPERIMENTS.md` when present
- source bundles or direct evidence in `code/`
- `PROBLEM.md`, `CONSTRAINTS.md`, `DELIVERABLES.md`

If package docs conflict with exact source, trust exact source. If compressed context conflicts with direct source, trust direct source. Put unavoidable questions in an `OPEN_QUESTIONS` section after the useful work.

## 2. Research

{RESEARCH_TARGETS}

Use online research when current external facts, market comparison, official APIs, product capabilities, or legal/security behavior affect the recommendation. Prefer primary sources and record what you relied on.

_(If no research targets are needed, remove this section.)_

## 3. Decision Style

Make choices, not vague suggestions.

For material decisions, include:

- options considered
- chosen option
- evidence
- tradeoffs
- what would change your mind

Use direct language such as `Choose A because B; evidence C`. Mark uncertainty instead of hiding it.

## 4. Baseline and Patch Discipline

The common failure mode is producing patches against imagined code. Use the baseline and context manifest to prevent that.

Every patch should include:

```text
# Based on commit SHA: <full SHA from BASELINE_COMMIT>
# Intent: <why this patch exists>
# Verification: <commands to run after applying>
```

Before relying on imports, functions, CLI flags, env vars, routes, tables, or file paths, verify them in the provided source or state the evidence gap.

For semantic changes, identify downstream callers/readers and the rollback path. For migrations, include forward path, rollback, dry run, integrity checks, and expected data-loss status.

Verification claims should include the command, snapshot/SHA, and enough output for replay. If real tests cannot run, provide the local replay command and expected result.

## 5. Review Gates

A delivery fails review when any of these are true:

- baseline or target snapshot is ambiguous
- implementation was requested but the answer contains only prose
- a patch references symbols, flags, routes, tables, env vars, or paths that are not verified in the provided source
- test or verification claims lack replayable command evidence
- behavior/data changes lack rollback or risk notes
- source packages include secrets, auth files, caches, generated binaries, or unrelated bulk context

Use these as hard gates, not as style preferences. Everything else is judgment.

## 6. Goal Loop

If `GOAL.md` exists, treat it as the loop objective.

Before implementation or major recommendations, state:

- selected access mode
- target score or checklist threshold
- fastest feedback command/probe/checklist
- stop rule
- red lines

After each patch, probe, or major recommendation, update applicable ledgers:

- `CHECKLIST.md`
- `PROGRESS.md`
- `EXPERIMENTS.md`
- `PATCH_QUEUE.md`
- `VERIFICATION_MATRIX.md`

If you cannot write files, include updated ledger sections in your answer.

Stop when the goal score is met with evidence, a documented blocker prevents progress, or the next step would cross a red line.

## 7. Implementation Output

Choose the delivery mode allowed by `ACCESS_MODE.md`:

- **Writable repo**: create a branch, commit a low-risk patch, report branch, commit SHA, changed files, tests, and PR draft.
- **Zip/browser/no-write**: output unified diffs or a patch plan as requested. Diffs should be checkable with `git apply --check`.
- **Analysis-only**: deliver the decision model, tradeoff table, risks, and verification plan without pretending code was changed.

When code was requested, include concrete implementation artifacts. A roadmap alone is not enough.

## 8. Deep Review Pattern

For broad product, architecture, or system-quality work, use independent lanes before synthesis:

- product/user workflow
- architecture/data flow
- implementation/testability
- adversarial risk

The synthesis should identify agreement, disagreement, missing evidence, and the strongest minority objection. Strong evidence can override majority agreement.

Useful output sequence:

1. repository truth reconstruction
2. code/data-flow trace
3. external research when relevant
4. decision model or rubric
5. patch queue or implementation plan
6. verification matrix
7. rollback/risk notes

## 9. HTML Companion

Create `review.html` for complex, multi-finding, shareable, or Pro Saturation reviews when it improves scanability.

Good HTML is:

- single file with inline CSS/SVG and no remote assets
- in the user's preferred language for user-facing text
- evidence-linked to files, commands, functions, or sources
- responsive and readable on desktop/mobile
- focused on decision, top findings, patch status, risk, and next action

Recommended sections:

- executive strip
- system map
- ranked findings board
- patch plan
- risk matrix
- verification console
- copy-next-prompt block

The HTML is a visual companion. It does not replace the report, diffs, tests, or verification evidence.
