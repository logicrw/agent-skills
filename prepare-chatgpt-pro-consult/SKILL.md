---
name: prepare-chatgpt-pro-consult
description: Use when preparing a baseline-controlled consult package for ChatGPT Pro or another remote web model, especially multi-file review, patch planning, deep research, roadmap planning, or Pro Saturation.
---

# prepare-chatgpt-pro-consult

Prepare replayable consult packages for remote web models. The goal is not the longest prompt; it is a package whose result can be checked locally.

## Core Contract

Every non-trivial package must state:

1. Access mode: live repo, uploaded zip, browser-only, or no-write analysis.
2. Baseline: commit SHA, dirty-state policy, and patch target.
3. Context provenance: included files, omitted files, and why.
4. Replay path: commands, probes, checklist, or local review steps.

Use judgment on everything else. Add artifacts only when they improve the remote model's answer or the local review loop.

## Tiers

Choose the lightest tier that can produce a trustworthy answer.

| Tier | Use When | Add |
|---|---|---|
| Focused consult | narrow architecture or review question | README, INDEX, BASELINE_COMMIT, ACCESS_MODE, CONTEXT_MANIFEST, PROBLEM, DELIVERABLES, relevant evidence |
| Implementation consult | patches, migrations, tests, or PR planning are in scope | focused consult plus PATCH_QUEUE, VERIFICATION_MATRIX, rollback notes, round-trip prompt |
| Long-running goal | remote model should keep working toward a measurable objective | GOAL, CHECKLIST, PROGRESS, EXPERIMENTS, stop rules |
| Pro Saturation | user explicitly wants maximum ChatGPT Pro effort/output | load `references/pro-saturation-mode.md`; add MAXIMIZE and split context bundles |

Do not turn a small local fix into a large consult. Do not accept a report-only answer when the user's goal requires code, tests, or a concrete patch plan.

## Load References

Load only what the package needs:

- `references/workflow.md`: package creation workflow, zip layout, remote engagement, local review.
- `references/package-execution-contract.md`: large, unfamiliar, implementation-heavy, or long-running packages.
- `references/context-tool-ladder.md`: choosing search, repo maps, symbol lookup, direct copies, or bundle strategy.
- `references/repomix-context-packaging.md`: any source package built with Repomix.
- `references/pro-saturation-mode.md`: explicit maximum-depth / maximum-output requests only.
- `references/pressure-checks.md`: maintainer checks after routing, template, or package-content changes.

Keep `SKILL.md` as the router. Put mechanics in references and templates.

## Workflow

1. Frame the job: original request, desired output, non-goals, red lines, acceptance checks, and stop rule.
2. Anchor the baseline before packaging.
3. Select focused, auditable context; never include secrets, local caches, binaries, or irrelevant private data.
4. Build the package from templates when useful.
5. Validate before zipping.
6. Engage the remote model with access mode and baseline constraints.
7. Review the returned work locally before trusting it.

Use `references/workflow.md` for commands and layout.

## Output Contracts

Pick by task:

- Bug fix: patch, test, verification command, rollback.
- Architecture decision: options, tradeoffs, recommendation, migration sketch.
- Refactor: patch sequence, tests, compatibility notes, rollback.
- Product/system redesign: repo truth reconstruction, data-flow trace, decision model, concrete patch plan.
- Long-running goal: measurable score, checklist, progress ledger, attempts ledger, stop rule.

For complex multi-finding, architecture, product, or Pro Saturation packages, request a `review.html` companion only when it improves scanning or sharing. HTML never replaces diffs, tests, Markdown findings, or verification evidence.

## Quality Gates

The package is not ready if:

- baseline or dirty-state target is ambiguous
- access mode is missing
- context selection is not explained
- replay path is missing
- implementation output lacks patch/test/rollback expectations
- secrets or irrelevant bulk context are included

The remote answer is not ready if:

- APIs, flags, imports, paths, or tests are invented
- implementation was requested but only prose is returned
- patches are not tied to a baseline
- verification claims lack commands or evidence
- risks and rollback are missing for behavior or data changes

## Maintenance

- `last_validated_at: 2026-06-20`
- Recheck current ChatGPT Pro capabilities before relying on specific Pro, Deep Research, Agent, Codex, file-upload, connector, or sandbox behavior.
- After changing routing, templates, or package contents, run the pressure scenarios in `references/pressure-checks.md`.
