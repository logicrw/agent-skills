<!--
Template: MAXIMIZE.md — use only for Pro Saturation Mode.
Placeholders:
  {PROJECT_NAME}      - project name
  {PROBLEM_ONELINE}   - one-line problem summary
  {TARGET_SCORE}      - measurable completion target
  {RED_LINES}         - non-negotiable constraints
-->

# Maximize ChatGPT Pro

You are working in Pro Saturation Mode for {PROJECT_NAME}.

Problem: {PROBLEM_ONELINE}

Target: {TARGET_SCORE}

Red lines:

{RED_LINES}

## Operating Rule

Use the strongest available ChatGPT Pro model and any available Deep Research, Agent, Codex, file, browser, connector, or code-execution capability that helps. If a capability is unavailable in this session, state that once and continue with the uploaded package.

Do not optimize for brevity. Optimize for maximum useful engineering output under the package constraints.

## Required Work Loop

1. Read `ACCESS_MODE.md` and `CONTEXT_MANIFEST.md`. State the selected mode and which artifacts are source authority.
2. Reconstruct the repository truth from the package before proposing changes.
3. Trace the affected code/data flow through concrete files, functions, schemas, tests, and user-facing surfaces.
4. Run independent analysis lanes:
   - product/user impact
   - architecture/data flow
   - implementation/test strategy
   - adversarial/risk
   - external benchmark or official-doc research when relevant
5. Synthesize the lanes. Identify agreement, disagreement, missing evidence, and the strongest minority objection.
6. Build `PATCH_QUEUE.md`: must-fix, high-value, enabling, stretch.
7. Implement the largest safe stack of PR-sized patches you can produce.
8. For each patch, include tests, verification commands, rollback, and affected callers/readers.
9. Update `CHECKLIST.md`, `PROGRESS.md`, `EXPERIMENTS.md`, `PATCH_QUEUE.md`, and `VERIFICATION_MATRIX.md`.
10. Produce `review.html` after the report and patches.

## Patch Stack Rules

Prefer many reviewable patches over one huge patch.

Every patch must start with:

```text
# Based on commit SHA: <full SHA from BASELINE_COMMIT>
# Patch: <short-name>
# Intent: <why this patch exists>
# Verification: <commands to run after applying>
```

Every patch must be checkable with:

```bash
git checkout <SHA>
git apply --check patches/<name>.diff
```

If you can write the repository, create a branch and commit the first low-risk patch. If you cannot write the repository, output unified diffs. Do not output pseudocode as a substitute for implementation.

## Minimum Acceptable Delivery

Your final answer must include or update:

- repository truth reconstruction
- access mode and context-authority summary
- ranked findings with file/function references
- `PATCH_QUEUE.md`
- concrete diffs or branch/commit details
- `VERIFICATION_MATRIX.md`
- updated `CHECKLIST.md`, `PROGRESS.md`, and `EXPERIMENTS.md`
- rollback notes per patch
- exact next prompt for the same ChatGPT Pro thread
- updated `ROUNDTRIP_PROMPTS.md` if local review found failures or blockers
- `review.html`

If you cannot complete a patch because of missing runtime, missing credentials, or insufficient repository context, output the blocker, the smallest probe needed to unblock it, and the next best patch that does not require the missing item.

## Stop Rules

Stop only when:

- the target score is met and evidence is attached
- the next patch would cross a red line
- a missing credential/runtime/user decision blocks all meaningful progress
- the session refuses additional tool use or output

Do not stop because the project is large. Convert breadth into patch queues and continue.
