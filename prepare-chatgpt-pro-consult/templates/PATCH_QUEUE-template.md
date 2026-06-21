<!--
Template: PATCH_QUEUE.md
Placeholders:
  {BASELINE_SHA}       - baseline commit SHA
  {TARGET_SCORE}       - completion target or checklist threshold
-->

# Patch Queue

Baseline: `{BASELINE_SHA}`

Target: {TARGET_SCORE}

| Priority | Patch | Intent | Files | Verification | Rollback | Status |
| --- | --- | --- | --- | --- | --- | --- |
| P0 |  |  |  |  |  | planned |

## Priority Rules

- P0: correctness, data loss, security, baseline drift, broken user flow.
- P1: high-value implementation with clear tests and low rollback risk.
- P2: enabling refactor or coverage needed for later patches.
- P3: stretch improvement; do only after P0/P1 are handled.

## Status Values

Use: `planned`, `drafted`, `apply-check-pass`, `apply-check-fail`, `tests-pass`, `tests-fail`, `accepted`, `modified`, `rejected`, `blocked`.
