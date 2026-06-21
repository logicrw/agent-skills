<!--
Template: ACCESS_MODE.md
Placeholders:
  {SELECTED_MODE}       - live-github | zip-only | browser-only | no-write-analysis
  {BASELINE_SHA}        - baseline commit SHA
  {PROBE_SUMMARY}       - commands attempted and results
  {WRITE_CAPABILITY}    - what ChatGPT Pro can write, if anything
-->

# Access Mode

Selected mode: `{SELECTED_MODE}`

Baseline: `{BASELINE_SHA}`

## Probe Summary

{PROBE_SUMMARY}

## Capability Contract

ChatGPT Pro may:

- {WRITE_CAPABILITY}

ChatGPT Pro must not:

- claim tests passed unless the exact command ran in this session
- write patches against any SHA other than `{BASELINE_SHA}` unless this file is updated
- switch modes without explaining the new probe result

## Mode Rules

- `live-github`: create a branch/commit when safe; report branch, commit SHA, and commands run.
- `zip-only`: output unified diffs that pass `git apply --check`; include exact local replay commands.
- `browser-only`: produce patch drafts and verification recipes; mark all runtime claims unverified.
- `no-write-analysis`: provide evidence-backed analysis only; do not imply implementation was completed.
