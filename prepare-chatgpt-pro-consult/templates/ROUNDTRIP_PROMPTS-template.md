<!--
Template: ROUNDTRIP_PROMPTS.md
Placeholders:
  {BASELINE_SHA}       - original baseline commit SHA
  {CURRENT_SHA}        - current local SHA after accepted patches
  {GOAL_SUMMARY}       - one-line current goal
-->

# Roundtrip Prompts

Use these prompts in the same ChatGPT Pro thread. Do not start a new thread unless the original one is unusable.

## V2 After Local Review

```text
Continue in this same thread.

Original baseline: {BASELINE_SHA}
Current local SHA: {CURRENT_SHA}
Goal: {GOAL_SUMMARY}

Local review results:
<paste PATCH_QUEUE status changes>
<paste VERIFICATION_MATRIX failures and pass evidence>

Revise only the blocked or failed patches. Keep accepted patches unchanged. Output apply-checkable diffs and updated ledgers.
```

## Patch Apply Failed

```text
The patch did not pass git apply --check.

Failure:
<paste exact command and stderr>

Repair the diff against the stated SHA. Do not change intent unless the failure proves the intent is wrong.
```

## Tests Failed

```text
The patch applied but verification failed.

Command:
<paste command>

Output:
<paste relevant stdout/stderr>

Explain the cause, then output the smallest corrected patch plus updated verification notes.
```
