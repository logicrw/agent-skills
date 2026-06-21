<!--
Template: CONTEXT_MANIFEST.md
Placeholders:
  {BASELINE_SHA}          - baseline commit SHA
  {PACKAGE_DATE}          - YYYY-MM-DD
  {NO_CODE_PACKAGE_REASON_OR_NA} - "yes - <reason>" only when code is out of scope; otherwise "N/A"
  {TOOL_ATTEMPTS}         - tool attempts and outcomes
  {BUNDLE_TABLE}          - included bundles/files table
  {OMISSIONS}             - important omitted files and why
  {PRIVACY_REVIEW}        - secret/path review result
-->

# Context Manifest

Baseline: `{BASELINE_SHA}`

Package date: `{PACKAGE_DATE}`

No code package: {NO_CODE_PACKAGE_REASON_OR_NA}

## Tool Attempts

{TOOL_ATTEMPTS}

Record `repomix` commands, search/symbol commands, structured-data probes, direct-copy fallbacks, and any skipped tools.

## Included Context

{BUNDLE_TABLE}

Recommended columns:

| Artifact | Source command/tool | Why included | Token/size note | Authority level |
| --- | --- | --- | --- | --- |

Authority levels:

- `source`: exact source file or direct copy
- `bundle`: `repomix` portable bundle
- `orientation`: codemap, compressed summary, repo map, or architecture note
- `evidence`: logs, screenshots, diffs, SQL/probe output

## Omitted Context

{OMISSIONS}

For `repomix` bundles, include the exact `--include` / `--ignore` patterns or the `--stdin` file-list source. If a whole-repo bundle was used, state why a focused bundle was not better.

## Dirty State

State whether the working tree was clean. If dirty, list files and whether diffs were included.

## Privacy Review

{PRIVACY_REVIEW}

Confirm no secrets, tokens, `.env`, cache directories, generated binaries, or unnecessary user-identifying absolute paths were included.

## Context Risks

List anything ChatGPT Pro might misunderstand because context is missing, compressed, stale, or generated.
