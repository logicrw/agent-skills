<!--
Template: VERIFICATION_MATRIX.md
Placeholders:
  {BASELINE_SHA}       - baseline commit SHA
  {FASTEST_FEEDBACK}   - fastest meaningful local command/probe
-->

# Verification Matrix

Baseline: `{BASELINE_SHA}`

Fastest feedback loop: `{FASTEST_FEEDBACK}`

| Check | Owner | Command/probe | Expected result | When to run | Evidence/status |
| --- | --- | --- | --- | --- | --- |
| Patch applies | ChatGPT Pro + local reviewer | `git apply --check patches/<name>.diff` | no errors | every patch | pending |
| Symbol exists | ChatGPT Pro + local reviewer | `rg "<symbol>" <path>` | expected definition/callers found | before patch claim | pending |

## Evidence Rules

- Every passed command needs command, SHA, and summarized stdout.
- Every failed command needs command, SHA, stderr, and next repair prompt.
- If a check cannot run in ChatGPT Pro, mark owner as `local reviewer`.
