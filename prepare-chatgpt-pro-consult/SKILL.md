---
name: prepare-chatgpt-pro-consult
description: Prepare a controlled engineering consult package for ChatGPT Pro or a similar remote web model when a project needs multi-file architecture analysis, deep research, roadmap planning, and concrete patch delivery with baseline control.
triggers: ["ChatGPT Pro consult", "prepare ChatGPT Pro", "send to ChatGPT Pro", "ChatGPT Pro refactor", "ChatGPT Pro deep research", "ChatGPT Pro patch", "pack for ChatGPT", "/prepare-chatgpt-pro-consult"]
---

# prepare-chatgpt-pro-consult

Hand off a problem to ChatGPT Pro on the web. The output is a controlled consult package — not a chat prompt. The package tells ChatGPT exactly what to read, what to produce, and how to avoid the most common failure modes (baseline drift, hallucinated APIs, untested patches).

Do not skip the verify-then-iterate loop.

## Default Standard After 2026-05-11

When the user wants ChatGPT Pro to "do more", "research deeply", "work automatically", "provide concrete improvements", or review a broad product/architecture problem, default to a **deep research + patch delivery consult**, not a shallow advisory prompt.

The consult should force ChatGPT Pro to:

1. Reconstruct the current system from repository facts before proposing changes.
2. Trace code/data flow through concrete files, functions, tables, and user-facing surfaces.
3. Research external benchmarks when product or architecture quality depends on the broader market.
4. Run independent analysis lanes before synthesis when the problem is complex or high-stakes.
5. Define the missing decision model or rubric explicitly, instead of only improving wording.
6. Provide SQL/probes/commands for validating claims against local data when the remote model cannot access runtime state.
7. Self-critique the chosen plan before finalizing it.
8. Deliver concrete implementation artifacts: either a branch/commit/PR draft when it can write the repo, or `git apply --check`-able unified diffs when it cannot.
9. Deliver a visual HTML companion artifact for complex reviews, so the user can scan architecture, findings, patch plan, and risks faster than in a long Markdown report.

Do not accept a final ChatGPT Pro deliverable that is only a report when the user's real goal requires implementation. Require at least the first low-risk patch to be concrete code with tests and rollback.

For complex consults, borrow the HeavySkill pattern: ask for several independent reasoning trajectories, then a deliberate synthesis. Use different lenses such as product/user workflow, architecture/data flow, implementation/testability, and adversarial risk. The synthesis must critique the lanes; it must not simply vote or concatenate them.

## Lessons from Multi-Round Code Consults

When a ChatGPT Pro consult runs across several rounds, make each round narrower and more evidence-rich than the last. The highest-yield loop is:

1. Send a constraint-rich prompt with baseline SHA, red lines, required files, output format, and patch contract.
2. Locally apply or reconcile the returned patch.
3. Run the exact tests, smoke checks, runtime probes, and `git diff --check`.
4. Send ChatGPT Pro the new SHA, the local verification output, rejected ideas, any failed hunks, and the next specific question.
5. Ask for one more low-risk patch or one ranked review pass, not a broad re-review of everything.

Do not let later rounds become vague. Every follow-up prompt should include:

- current code SHA and whether earlier patches were accepted, modified, or rejected
- changed files since the previous round
- fresh verification evidence, including failed commands and relevant stdout/stderr
- one current product or engineering bottleneck
- explicit red lines that still hold
- required deliverable: branch/commit/PR draft or apply-checkable diff

Prefer "review this exact new surface" over "review the repo again". For example: "review market/topic grouping and feedback calibration for operator misranking risks" is stronger than "find more improvements".

## Quality Bar for Useful ChatGPT Pro Output

Reject or iterate any answer that fails these checks:

- **Specificity**: findings cite files, functions, fields, tables, and user-facing surfaces.
- **Causality**: each issue explains how the current code causes a user-visible failure, not just that it is inelegant.
- **Patchability**: at least one recommendation is delivered as code with tests, not only a plan.
- **Verification**: every "passed" claim includes the command, baseline/current SHA, and enough output to replay locally.
- **Boundary control**: the patch does not cross red lines such as changing readiness gates, live trading semantics, security posture, or source-of-truth contracts.
- **Rollback**: implementation notes say how to undo the change cleanly.
- **User value**: product improvements map to a concrete review surface, workflow, dashboard, message, or operator decision.

When ChatGPT Pro gives many ideas, force a triage ladder:

1. Must-fix correctness bugs
2. Misleading user-facing behavior
3. Missing tests around already-changed behavior
4. Low-risk product/readability improvements
5. Larger architecture work for a later PR

The first accepted patch should usually come from categories 1-4. Do not let category 5 block small shippable improvements.

## ChatGPT Pro Sandbox Capabilities (Verified 2026-04)

- Public GitHub repository discovery works through web search and page open.
- Public repository file reading works through browser pages for README, source files, and test trees.
- Shell git access fails in the sandbox: `Could not resolve host: github.com`. No local checkout is available.
- Local install, CLI execution, pytest, worktree creation, commit, push, and PR creation all fail because clone fails or shell DNS fails.
- Ordinary shell subprocess execution works and captures stdout.
- File artifacts persist across tool calls in `/mnt/data` within one session.
- External documentation fetch and GitHub issue search work through the browser tool; shell `curl` to external hosts fails DNS.

**Default to the zip path. Promote to live-GitHub only after a per-session probe (Phase 3).**

## When to Use

Use this skill for projects where a web model should act as an external engineering reviewer or planner across several modules. Good triggers: architecture redesign, multi-file refactor planning, competing technical options, roadmap design, migration planning, patch design needing a strict baseline, or any task where the current agent is stuck after multiple attempts.

Do not use it as a one-shot chat prompt. The output is a controlled consult package plus a verification loop.

## When NOT to Use

- Single localized bug fixable in one more try
- Small edits under five files
- Tasks without a clear baseline
- Private repos where the user cannot provide either access or a zip
- Work that needs immediate real-time back-and-forth in the current agent

## Deliverable: One Zip

Build one zip named `{project}-consult-YYYYMMDD.zip`:

```
{project}-consult/
├── README.md              # opening orders for ChatGPT
├── INDEX.md               # reading priority and required order
├── BASELINE_COMMIT        # git rev-parse HEAD anchor
├── PROBLEM.md             # what's broken, what's been tried, what failed
├── DELIVERABLES.md        # exact output contract and patch requirements
├── HOW-TO-WORK.md         # working rules + anti-baseline-drift
├── CONSTRAINTS.md         # budget / runtime / dependency rules / red lines (if applicable)
└── code/                  # relevant source files or repomix bundle
    └── code-bundle.xml
```

For complex product, architecture, or code-review consults, require ChatGPT Pro to produce a standalone `review.html` companion artifact in addition to the Markdown/report output. The HTML is for fast reading and sharing; it does not replace patches, tests, Markdown findings, or verification evidence.

Templates: `templates/README-template.md` and `templates/HOW-TO-WORK-template.md`. Keep in English. Never localize.

## Workflow (5 Phases)

### Phase 1 — Discovery

Collect before writing anything:

- **User's original problem statement** — preserve exact quotes, do not paraphrase
- **Specific pain points with raw evidence** — error messages, failing test names, logs, screenshots. Vague complaints are not actionable.
- **What's been tried** — every approach the current agent attempted, with exact reasoning for why each failed. This prevents ChatGPT from repeating dead ends.
- **Hard constraints** — dependency versions, deployment environment, time/budget limits, interfaces that cannot change, red lines
- **Desired output format** — patches? architecture doc? comparison table? roadmap? Be explicit.
- **Acceptance checks** — convert vague goals into concrete pass/fail criteria

If the user can't articulate the problem clearly, extract it from the current session's error logs and failed attempts.

For broad redesign, product-quality, architecture-quality, or "make it actually useful" requests, use the deep research + patch delivery output contract. Do not let the package stop at "recommendations"; make the desired output a report plus concrete code artifacts.

### Phase 2 — Build the Package

1. **Anchor the baseline**:
   ```bash
   git rev-parse HEAD > BASELINE_COMMIT
   git log -1 --format='%H%n%ai%n%s%n%an' >> BASELINE_COMMIT
   git status --short >> BASELINE_COMMIT
   ```

2. **Collect code** — only what's relevant to the problem:
   ```bash
   # Option A: repomix for a focused bundle
   repomix --include "src/relevant_module/**" -o code/code-bundle.xml

   # Option B: copy individual files
   mkdir -p code && cp src/foo.py src/bar.py code/
   ```
   Record absolute paths from the repository root. Do NOT include secrets, local usernames, tokens, `.env`, cache directories, or generated binaries. Do NOT pack the entire repo — every irrelevant file dilutes attention.

3. **Write PROBLEM.md** — the single most important file:
   - What the problem is (specific, with evidence)
   - Current state (what works, what doesn't)
   - Each failed approach with exact error or reasoning
   - What you want ChatGPT to produce (explicit format)
   - File map: which files in `code/` and what each does
   - Acceptance checks from Phase 1

4. **Write INDEX.md**:
   - P0: must-read authority docs
   - P1: source files to trace
   - P2: tests, fixtures, docs, and optional references

5. **Write DELIVERABLES.md**:
   - Required report sections
   - Required implementation artifacts
   - Independent analysis lanes and synthesis requirements for complex consults
   - Patch format, branch/commit expectations, tests, rollback, and acceptance checks
   - If the remote model cannot edit the repo, require unified diffs that pass `git apply --check`
   - For complex consults, require a standalone `review.html` companion artifact with visual summary, code/data-flow diagram, ranked findings, patch plan, risk matrix, and verification checklist

6. **Write CONSTRAINTS.md** (if applicable):
   - Dependency versions, runtime environment, budget, red lines, stable interfaces

7. **Fill templates**: `README-template.md` → `README.md`, `HOW-TO-WORK-template.md` → `HOW-TO-WORK.md`. Fill placeholders.

8. **Zip**:
   ```bash
   cd /tmp
   zip -r {project}-consult-YYYYMMDD.zip {project}-consult/ \
     -x "*.DS_Store" -x "*__pycache__*" -x "*.pyc"
   ```

### Phase 3 — Engage ChatGPT Pro

First test the model session with this probe:

```bash
git clone <repo-url>
cd <repo>
git rev-parse HEAD
python3 -m pip install -e '.[dev]'
pytest -q
```

Side effects: these commands create a local checkout and local install artifacts. They do not modify the remote repository.

**If the probe succeeds**: prefer the live GitHub path. Require ChatGPT Pro to treat the cloned HEAD as source of truth, compare it with `BASELINE_COMMIT`, and write every patch against the live SHA.

**If clone, install, or tests fail**: use the zip path. Upload the consult package and tell ChatGPT Pro to base all patches on `BASELINE_COMMIT`. Any claim such as "tests passed" is forbidden unless the exact command ran in that same session. If only browser reading works, ask for design, risk analysis, and patch drafts with verification recipes, then send the result to an independent local reviewer.

Opening message for zip path:

> Read README.md first. Treat BASELINE_COMMIT as ground truth. Build every patch against that SHA. Do not claim "tests passed" without a reproducible command run in this session. Start working.

Opening message for live-private-GitHub path:

```text
Please access this private repository:

<repo-url>

First read the root handoff prompt or consult package docs. Confirm:
- repository access
- current HEAD
- baseline SHA
- files you will read first

Then execute the full deep research + patch delivery workflow. Do not stop at recommendations. If you can write the repository, create a branch and commit the first low-risk patch. If you cannot write the repository, output unified diffs that can be saved and checked with `git apply --check`.
```

### Phase 4 — Verify v1

Never apply v1 directly. The reviewer (you or another agent) must:

- Run `git apply --check` on every patch against the BASELINE_COMMIT SHA
- Grep every imported symbol, CLI flag, env var against current HEAD
- Run every test ChatGPT claims passed
- Check migration safety (forward, rollback, dry-run)
- Report exact failures with evidence

### Phase 5 — Iterate v2

Return the review report to the **same** ChatGPT Pro conversation — context is expensive, do not start a new one. Require a revised package against the current SHA. Apply only reviewer-approved patches, one commit per patch, with a clear rollback path.

### Phase 6 — Visual Companion

For any consult that produces more than a short localized patch, require a single-file HTML artifact named `review.html` or `{project}-review.html`.

The HTML artifact must be:

- standalone: inline CSS and SVG, no remote assets, no build step
- safe to share: no secrets, tokens, private local paths, or unnecessary user-identifying details
- scan-first: first viewport shows the current decision, top findings, patch status, and next action
- evidence-linked: every visual claim links to or names the source file/function/command
- responsive: readable on desktop and mobile
- printable enough for leadership or PR review
- secondary to code: it may visualize the patch plan, but it must not replace diffs, tests, or verification commands

Strong default sections:

- Executive strip: baseline SHA, current SHA, access status, branch/patch status, verification status
- System map: SVG or HTML flow from input data to user-facing output
- Findings board: ranked cards colored by severity, each with file/function, impact, fix, and test
- Patch plan: PR-sized steps with changed files, feature flags, rollback, and acceptance checks
- Risk matrix: what can break, blast radius, detection probe, fallback
- Verification console: exact commands and summarized outputs
- Copy-next-prompt button: exports a concise follow-up prompt for the same ChatGPT Pro thread

If ChatGPT Pro cannot write files, ask it to output the HTML as a fenced `html` block after the Markdown report. The local agent can save it as an artifact.

## Anti-Baseline-Drift

Every patch must start with:

```text
# Based on commit SHA: <40-char SHA>
```

Every patch must include this verification recipe:

```bash
git checkout <SHA>
git apply --check patches/<name>.diff
```

Before writing a patch, verify every import, function, CLI flag, environment variable, and file path against the baseline. Use `grep`, `rg`, or direct file reads. If a symbol is absent, add it in the same patch before using it.

For semantic changes, list all downstream callers and readers. For migrations, provide forward, rollback, dry-run, integrity checks, and expected data loss status. For tests, include the exact command, commit SHA, and first stdout lines. A statement without reproducible evidence is treated as unverified.

## Sub-Agent Briefs

When building the package, these roles can be dispatched in parallel:

**Bug investigator**: write problem statement, system context, known defects, evidence samples, and a focused code bundle for concrete failures.

**Architecture researcher**: research candidates from primary sources, summarize tradeoffs, map them to project constraints, and write selection questions.

**Style agent**: collect real user output samples, extract hard style rules. Samples override prose rules when they conflict.

**Package agent**: assemble the zip, verify required files, exclude secrets, and record the baseline.

**Reviewer agent**: perform read-only review. Run `git apply --check`, verify references, rerun claimed tests, and report exact failures. Do not edit source.

## No-Filler Rules for ChatGPT

Write these into `HOW-TO-WORK.md`:

Banned: "I would be happy to help" / "I suggest" / "perhaps" / "In summary" / "to conclude"
Required: "Do X because Y, evidence Z" / "Choose A over B; A wins on N dimensions"

Do NOT wait for confirmation. Drive forward.

## Scaling Deliverables by Task Type

Tell ChatGPT what to produce in PROBLEM.md:

- **Bug fix**: patches + tests + verification recipe
- **Architecture decision**: comparison table (≥3 options) + recommendation with evidence + migration sketch
- **Refactor**: patches + tests + migration plan + rollback + decision log
- **Large redesign**: all above + architecture diagram (Mermaid) + risk assessment + roadmap
- **Deep product/system redesign**: seven-round protocol:
  1. repository truth reconstruction
  2. code/data-flow trace
  3. independent analysis lanes plus deliberate synthesis
  4. external benchmark research
  5. explicit decision model/rubric
  6. SQL/probe validation plan
  7. self-critique and tradeoff reconciliation
  8. concrete patch delivery
  9. standalone HTML companion artifact for fast scan and sharing

For deep product/system redesign, require the first implementation patch to be code, not pseudocode. A good first patch is usually a low-risk deterministic layer behind a feature flag or shadow path, plus tests and one user-facing readout.

## Independent Analysis Lanes

For hard consults, require three to five independent lanes before the final recommendation. Lanes should not see or depend on one another's conclusions. Good default lanes:

- **Product/user lane**: what the user actually needs, where current output fails, and what the target experience should make obvious.
- **Architecture/data-flow lane**: current modules, tables, data contracts, side effects, and likely fracture points.
- **Implementation/test lane**: smallest patch sequence, tests, migration/backfill, rollback, and verification commands.
- **Adversarial/risk lane**: how the proposed plan can fail, what it could overfit, what it could silently break, and what evidence would refute it.

The synthesis step must identify agreement, disagreement, missing evidence, and the strongest minority objection. Majority agreement is not proof. A minority lane with better evidence can override the majority.

## Patch Delivery Contract

When implementation is required, ChatGPT Pro must choose one delivery mode:

**Mode A — branch/commit/PR draft**

- Create a branch with a descriptive name.
- Commit the first low-risk patch.
- Report branch name, commit SHA, changed files, tests run, and PR description draft.

**Mode B — unified diffs**

- Output one diff per PR-sized patch.
- Each diff starts with:
  ```text
  # Based on commit SHA: <40-char SHA>
  # Patch: <short-name>
  # Intent: <why this patch exists>
  # Verification: <commands to run after applying>
  ```
- Every diff must be checkable with:
  ```bash
  git checkout <SHA>
  git apply --check patches/<name>.diff
  ```
- Include tests, smoke commands, runtime-vs-shadow behavior, migration/backfill notes, and exact rollback.

Reject deliverables that contain only prose, pseudocode, or "implementation left to the local agent" when the user asked for concrete improvements.

## Upgrade Path

Rerun the sandbox capability probes after any major ChatGPT Pro, browser-tool, or sandbox change. Promote the live GitHub path only after clone, dependency install, CLI help, and pytest are verified in that session. Promote PR-based handoff only after branch creation, push, and PR creation are verified with explicit write authorization.

## Maintenance

- `last_validated_at: 2026-04`
- Revalidate sandbox capabilities every three months or after a major model/tool release
- Templates change only when the deliverable contract changes
