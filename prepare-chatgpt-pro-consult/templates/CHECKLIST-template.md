<!--
Template: CHECKLIST.md — measurable acceptance checklist.
Keep items concrete enough that ChatGPT Pro can mark them done.
-->

# Acceptance Checklist

## Correctness

- [ ] Every changed symbol exists at the baseline SHA.
- [ ] Every patch applies with `git apply --check`.
- [ ] Every behavior change has a regression test or replay probe.

## User Value

- [ ] The first user-facing screen/message/report makes the next action obvious.
- [ ] The output removes or downranks low-value noise rather than only adding fields.
- [ ] The top recommendation explains why it beats the alternatives.

## Safety

- [ ] Red lines in `GOAL.md` remain unchanged.
- [ ] No live/trading/security/readiness boundary is crossed without explicit authorization.
- [ ] Rollback path is documented.

## Verification

- [ ] Fast feedback command/probe ran, or local replay instructions are exact.
- [ ] Claimed test output includes command, SHA, and relevant stdout.
- [ ] Remaining risks are listed with detection probes.
