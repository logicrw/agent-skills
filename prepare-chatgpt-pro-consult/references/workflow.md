# Consult Package Workflow

Use this when creating the actual package. Keep generated reports and HTML in the user's preferred language; keep commands, paths, SHAs, identifiers, and diff headers unchanged.

## Frame

Capture the user's original request, desired output, and acceptance checks. Preserve exact quotes for ambiguous pain points.

For broad goals, write:

- objective
- non-goals
- red lines
- fastest feedback loop
- stop rule

If analysis-only, say so in `ACCESS_MODE.md` and `CONTEXT_MANIFEST.md`; do not invent fake code artifacts.

## Baseline

```bash
git rev-parse HEAD > BASELINE_COMMIT
git log -1 --format='%H%n%ai%n%s%n%an' >> BASELINE_COMMIT
git status --short >> BASELINE_COMMIT
```

If dirty changes are intentionally part of the consult, record every dirty file and whether patches target committed HEAD or the dirty snapshot.

## Context

Prefer focused, auditable context over full repository dumps.

Useful inputs:

- `rg --files`
- `git diff --name-only`
- `git grep` / `rg` for symbols, routes, errors, config keys, tables, tests
- manifests, schemas, migrations, fixtures, docs, current rules
- Serena/LSP, `ast-grep`, tree-sitter, repo maps when installed and helpful

Use Repomix selectively. Prefer `repomix --stdin` for curated file lists and record exact commands in `CONTEXT_MANIFEST.md`.

Never package secrets, auth files, local caches, generated binaries, or unrelated private data.

## Layout

```text
{project}-consult/
├── README.md
├── INDEX.md
├── BASELINE_COMMIT
├── ACCESS_MODE.md
├── CONTEXT_MANIFEST.md
├── PROBLEM.md
├── DELIVERABLES.md
├── HOW-TO-WORK.md
├── GOAL.md                # when useful
├── CHECKLIST.md           # when useful
├── PROGRESS.md            # when useful
├── EXPERIMENTS.md         # when useful
├── MAXIMIZE.md            # Pro Saturation only
├── PATCH_QUEUE.md         # implementation-heavy
├── VERIFICATION_MATRIX.md # implementation-heavy
├── ROUNDTRIP_PROMPTS.md   # implementation-heavy
└── code/
    └── code-bundle.xml    # or direct source/evidence files
```

Use templates from `templates/` when they match the job.

Validate before zipping:

```bash
scripts/check-consult-package.sh {project}-consult/
zip -r {project}-consult-YYYYMMDD.zip {project}-consult/ \
  -x "*.DS_Store" -x "*__pycache__*" -x "*.pyc"
```

Resolve `scripts/` relative to the skill directory.

## Remote Engagement

Ask the session to use the strongest available model/tool mode, but do not hardcode stale model names.

Start with an access probe when live repo work is plausible. If clone/install/tests fail, use the uploaded zip path and require patches against `BASELINE_COMMIT`.

Opening instruction for zip path:

```text
Read README.md first. Treat BASELINE_COMMIT as ground truth. Build every patch against that SHA. Do not claim tests passed unless you ran the command in this session. Start working.
```

For long-running goals:

```text
Treat GOAL.md as the loop objective. Keep working until CHECKLIST.md is complete, the score in GOAL.md is met, or a documented blocker requires stopping. Update PROGRESS.md and EXPERIMENTS.md after each patch or probe.
```

For Pro Saturation, follow `references/pro-saturation-mode.md`.

## Local Review

Do not trust v1 blindly. Check:

- patch baseline SHA
- `git apply --check`
- imported symbols, CLI flags, env vars, routes, tables, and file paths
- claimed test commands
- migration, rollback, and blast radius

Send failures back to the same thread with current SHA, accepted/rejected changes, exact command output, and one concrete next request.
