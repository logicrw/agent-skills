---
name: conventional-commit
description: Draft, rewrite, and validate commit messages and PR titles as Conventional Commits.
---

Format commit messages and PR titles as Conventional Commits. Repo-local rules always override this skill.

## Input Priority

When drafting a commit message, use sources in this order:
1. Repo-local commit rules from `AGENTS.md`, `CLAUDE.md`, `.github/pull_request_template.md`, or package docs
2. Staged diff from `git diff --cached`
3. Unstaged diff from `git diff`
4. Current session discussion
5. Recent commit style from `git log -5 --oneline`

Never infer behavior changes from conversation alone if the diff contradicts it.

## Git Diff Rules

Default to staged changes only:
- Use `git diff --cached` as the source of truth.
- If there are no staged changes, state that no staged changes were found and ask whether to draft from unstaged changes.
- Do not include unstaged files in the commit message unless the user explicitly asks.

## Atomicity Rules

- If the staged diff contains unrelated changes, say so and provide separate commit message options.
- Do not hide unrelated changes under a vague header like `chore: update project`.
- Prefer one clear behavior change per commit.

## Procedural Workflow

1. **Check Local Rules:** If `AGENTS.md`, `CLAUDE.md`, `.github/pull_request_template.md`, or package docs define commit or PR title conventions, follow those instead.
2. **Inspect Changes:** Review staged diff first. Use unstaged diff only when explicitly requested.
3. **Determine Type:** Use the Type Decision Table below.
4. **Determine Scope:** Add a scope when it narrows down which module changed. Keep it noun-like. Skip it when the change is repo-wide.
5. **Draft Header:** `<type>[optional scope]: <description>` — imperative mood, no trailing period. Mark breaking changes with `!`.
6. **Draft Body:** Use the Default Body template only when the change is complex enough to justify it (see Body Omission Rules).
7. **Validate:** Check against the AI-Context Rules. Drop any field you cannot back with a fact from this session or the diff.

### Type Decision Table

| Change | Type | AI-Context Focus |
|---|---|---|
| New functionality | `feat` | Architectural choices and tradeoffs |
| Bug fix | `fix` | Root cause and why this fix is safe |
| Structural code change | `refactor` | Why the new structure is safer or clearer |
| Documentation | `docs` | Skip AI-Context |
| CI or release workflow | `ci` | Skip AI-Context |
| Build system or dependency change | `build` | Skip AI-Context unless it changes runtime behavior |
| Formatting only | `style` | Skip AI-Context |
| Minor maintenance | `chore` | Skip AI-Context |

## Breaking Changes

For this skill, use the stricter form:
- Add `!` after the type or scope.
- Add a `BREAKING CHANGE:` footer explaining the migration impact.
- Do not mark a change as breaking unless the public API, CLI behavior, config schema, database schema, or user-facing contract changes.

## Body Omission Rules

Use **header-only** output when:
- The change is `docs`, `chore`, `style`, `ci`, `build`, or a trivial fix
- The user asks for a PR title only
- The diff is too small to justify a body

Use the **full body** when:
- The change is `feat`
- The fix has a non-obvious root cause
- The refactor changes architecture
- Testing or rollout risks need to be preserved

## Default Body

```md
## Summary
- Describe the behavior change

## AI-Context
- **Intent**: What problem does this change solve?
- **Decision**: What approach was chosen and why?
- **Rejected**: What alternatives were discarded and why?

## Testing
- List the exact validation commands

## Risks
- Note remaining concerns
```

## AI-Context Rules

Each field is a **concrete, 1-2 sentence fact** from the staged diff, this session, or explicit user instruction.

| Rule | How to Apply |
|---|---|
| Keep it short | 1-2 sentences per field. Summarize the decision, not the conversation. |
| Omit empty fields | No alternative was discussed? Drop `Rejected`. |
| Session-Ref | Include `Session-Ref: <id>` only when the agent runtime supplies a real ID. Otherwise leave it out. |
| Real facts only | Every claim must trace to this session or diff. Never invent alternatives or motivations. |

## Testing Rules

- Only list validation commands that were actually run.
- If no validation was run, write "Not run".
- Do not claim tests passed unless tool output confirmed it.

## Examples

### Full commit (with AI-Context)

```md
feat(auth): add OAuth2 SSO login flow

## Summary
- Implemented Google OAuth2 login using passport.js
- Added `/auth/callback` endpoint for provider redirects

## AI-Context
- **Intent**: Users needed a faster onboarding path than email and password registration.
- **Decision**: Chose passport-google-oauth20 because it fits the Express stack and avoids introducing a separate auth platform.
- **Rejected**: Dropped Firebase Auth to avoid tying user identity to an external provider.

## Testing
- `npm run test:auth`

## Risks
- Requires `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` in production.
```

### Header-only (no body needed)

- `docs: clarify sync workflow`
- `chore(ci): enforce semantic PR titles`
- `style: fix eslint warnings`

## Validation & Rewriting

When reviewing an existing commit message:
1. Check the header against Conventional Commits format.
2. Check whether the type matches the actual diff.
3. For `feat` and complex `fix` commits, check whether AI-Context is present and factual.
4. Explain the mismatch precisely.
5. Provide 1-3 corrected options.

## Pull Request Titles

If the repo squash-merges PRs, the PR title becomes the merge commit header — make it Conventional Commits compliant. Use the repo's PR template for the body when one exists.

## Reference

For canonical wording, see [references/conventional-commits-v1.0.0.md](references/conventional-commits-v1.0.0.md).
