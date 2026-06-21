# Output Interpretation

Treat the trailing `scan_summary` as the trust gate.

```bash
OUT="${OUT:-work/bumblebee-project.ndjson}"

jq -e 'select(.record_type=="scan_summary" and .status=="complete")' "$OUT" >/dev/null
jq -r 'select(.record_type=="scan_summary") | [.status,.profile,.package_records_emitted,.findings_emitted,.package_records_suppressed,.diagnostics_count,.timed_out] | @tsv' "$OUT"
```

Count package records:

```bash
jq -r 'select(.record_type=="package") | [.ecosystem,.confidence] | @tsv' "$OUT" | sort | uniq -c
```

List findings:

```bash
jq -r 'select(.record_type=="finding") | [.severity,.catalog_id,.ecosystem,.package_name,.version,.confidence,.source_type,.source_file] | @tsv' "$OUT" | sort -u
```

Inspect MCP records:

```bash
jq -r 'select(.record_type=="package" and .source_type=="mcp-config") | [.server_name,.package_manager,.package_name,(.version//""),(.requested_spec//""),.confidence,.source_file] | @tsv' "$OUT"
```

Record type overview:

```bash
jq -r '[.record_type, (.ecosystem // "-")] | @tsv' "$OUT" | sort | uniq -c
```

## Rules

- Only promote results as current evidence when `scan_summary.status=="complete"`.
- `partial`, `error`, timeout, or missing summary output is raw evidence only.
- A complete scan with zero package records or zero findings is valid for the scanned scope.
- Absence of a recent complete scan means stale or unknown, not clean.
- `baseline` and `project` can support current-state inventory. Treat `deep` as campaign evidence unless scoped carefully.
- `confidence` describes how directly Bumblebee inferred package identity.
- Preserve exact diagnostics before summarizing.

## Report Shape

```text
Bumblebee: v0.1.1, selftest <passed|failed>
Scope: <profile>, root(s), ecosystem(s), duration cap
Output: <ndjson path>
Summary: status=<complete|partial|error>, packages=<n>, findings=<n>, suppressed=<n>, diagnostics=<n>, timed_out=<true|false>
Findings: <advisory/package/version/source/confidence grouped summary>
Limits: <coverage gaps, low-confidence matches, stale/partial state, handoff tool if needed>
```
