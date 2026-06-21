---
name: bumblebee-inventory-scanner
description: "Use when auditing local developer supply-chain inventory with Perplexity Bumblebee v0.1.1: packages, lockfiles, editor/browser extensions, MCP JSON configs, or advisory exposure. Not for secrets, EDR, full SBOM, or loose agent-skill directories."
---

# Bumblebee Inventory Scanner

IRON LAW: Bumblebee is a read-only shell inventory scanner. It collects documented local inventory and advisory exposure evidence; it is not MCP, memory, secret scanning, EDR, runtime monitoring, or proof that code executed.

## Use Gate

Use this skill when the user asks whether a local package, lockfile, extension, MCP JSON server entry, or advisory exposure is present on this machine.

Return a bounded command, saved NDJSON evidence path, `scan_summary` status, findings, limits, and the right handoff tool when Bumblebee is out of scope.

## Route

| User intent | Use Bumblebee? | Scope |
|---|---:|---|
| Package or advisory exposure in a repo/project tree | Yes | `deep` with explicit `--root`, exposure catalog, usually `--findings-only` |
| Package inventory in a repo or project directory | Yes | `project --root <path>` with selected ecosystems |
| Global developer inventory | Yes | `baseline` with selected ecosystems |
| VS Code, Cursor, Windsurf, VSCodium, or browser extensions | Yes | `baseline --ecosystem editor-extension,browser-extension` |
| MCP servers from JSON host configs | Yes | `baseline --ecosystem mcp` or project-local MCP scan |
| Codex `~/.codex/config.toml`, Continue YAML, secrets, runtime behavior, complete SBOM, Homebrew-only inventory | No | Use the appropriate parser, `scan-secrets`, incident-response tooling, or SBOM tooling |

Load `references/command-patterns.md` for exact commands.

## Readiness Gate

Before trusting output:

```bash
if ! command -v bumblebee >/dev/null 2>&1 || ! bumblebee version | grep -q 'bumblebee v0.1.1'; then
  GOBIN="$HOME/.local/bin" go install github.com/perplexityai/bumblebee/cmd/bumblebee@v0.1.1
fi

bumblebee version
bumblebee selftest
```

Preview roots before broad work:

```bash
bumblebee roots --profile baseline
bumblebee roots --profile project --root "$PROJECT_ROOT"
bumblebee roots --profile deep --root "$SCAN_ROOT"
```

Root rules:

- `baseline` scans global/user inventory surfaces and refuses bare-home project walking.
- `project` scans configured developer/project roots plus explicit `--root`.
- `deep` requires explicit roots and is the only profile intended for `$HOME`-sized scans.

## Workflow

1. Classify the request.
2. Pick the smallest profile, root, ecosystem, and duration cap.
3. Verify version and selftest.
4. Preview roots.
5. Run scan to an NDJSON file.
6. Check trailing `scan_summary`.
7. Report evidence, limits, and handoffs.

Always save scan output to a file. Use `work/` when no output path is requested.

## Interpret Results

Load `references/output-interpretation.md` before summarizing scan output.

Trust gate:

- `scan_summary.status=="complete"`: current evidence for the chosen scope.
- `partial`, `error`, timeout, or missing summary: raw evidence only.
- Zero package records or findings can be valid for the scanned scope.
- Absence of a recent complete scan means unknown, not clean.

For exposure catalogs, load `references/exposure-catalog.md`. Catalog matches are exact by `(ecosystem, package, version)` unless reported as lower-confidence name-only evidence.

For supported sources and known gaps, load `references/coverage-boundaries.md`.

## Privacy

- Do not paste raw full NDJSON into chat.
- Avoid unnecessary home paths, usernames, hostnames, device IDs, and full endpoint inventories.
- Do not use HTTP transport unless the user explicitly supplied endpoint/token environment variables.
- Never put bearer tokens or API keys in command-line arguments.

## Do Not

- Do not install or describe Bumblebee as a Codex MCP/plugin capability.
- Do not claim it parses Codex TOML, Continue YAML, arbitrary source files, package-manager command output, or secrets.
- Do not claim "no finding" means "no risk" outside the chosen profile/root/ecosystem/catalog.
- Do not treat advisory name-only MCP matches as exact package-version matches.
- Do not run broad `$HOME` scans without `deep`, explicit roots, a duration cap, and a reason.

## Completion Checklist

- [ ] `bumblebee version` shows v0.1.1 or drift is reported.
- [ ] `bumblebee selftest` passed or failure is reported.
- [ ] Roots were previewed for broad `baseline`, `project`, or `deep` work.
- [ ] Output was saved to NDJSON.
- [ ] `scan_summary.status` was checked.
- [ ] Final response states profile, root, ecosystems, output file, findings, and limits.
- [ ] Out-of-scope requests were routed to the right tool.

## References

- `references/command-patterns.md`
- `references/exposure-catalog.md`
- `references/output-interpretation.md`
- `references/coverage-boundaries.md`
- Local module docs: `$HOME/go/pkg/mod/github.com/perplexityai/bumblebee@v0.1.1/README.md`
