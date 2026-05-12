<!--
Template: GOAL.md — use for long-running ChatGPT Pro consults.
Placeholders:
  {PROJECT_NAME}      - project name
  {OBJECTIVE}         - one measurable objective
  {BASELINE_SHA}      - baseline commit SHA
  {SCORE_TARGET}      - numeric/checklist target that means done
  {FEEDBACK_COMMAND}  - fastest valid command/probe/checklist
-->

# Goal for {PROJECT_NAME}

## Objective

{OBJECTIVE}

## Baseline

- Baseline SHA: `{BASELINE_SHA}`
- Source of truth: repository code at the baseline SHA

## Completion Score

Done means: `{SCORE_TARGET}`.

Do not stop until the target is met, a stop rule applies, or a red line would be crossed.

## Fast Feedback Loop

Run after every patch or major recommendation:

```bash
{FEEDBACK_COMMAND}
```

If you cannot run this command in your session, provide exact local replay instructions and expected output.

## Red Lines

- Do not weaken production safety, security, or readiness gates.
- Do not claim tests passed unless they ran in this session.
- Do not change unrelated behavior to improve the score.

## Stop Rules

- Stop when the completion score is met and verification evidence is attached.
- Stop when required repo/test/runtime access is unavailable and no local replay path can prove the change.
- Stop when the next improvement would require crossing a red line.
