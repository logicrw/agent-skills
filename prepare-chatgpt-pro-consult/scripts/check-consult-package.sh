#!/usr/bin/env bash
set -u

root="${1:-}"
fail=0

err() {
  printf 'ERROR: %s\n' "$*" >&2
  fail=1
}

warn() {
  printf 'WARN: %s\n' "$*" >&2
}

need_file() {
  if [ ! -f "$root/$1" ]; then
    err "missing required file: $1"
  fi
}

if [ -z "$root" ]; then
  printf 'Usage: %s <consult-dir>\n' "$0" >&2
  exit 2
fi

if [ ! -d "$root" ]; then
  err "consult directory does not exist: $root"
  exit 1
fi

for file in \
  README.md \
  INDEX.md \
  BASELINE_COMMIT \
  ACCESS_MODE.md \
  CONTEXT_MANIFEST.md \
  PROBLEM.md \
  DELIVERABLES.md \
  HOW-TO-WORK.md
do
  need_file "$file"
done

if [ -f "$root/GOAL.md" ]; then
  for file in CHECKLIST.md PROGRESS.md EXPERIMENTS.md; do
    need_file "$file"
  done
fi

needs_patch_trio=0
if [ -f "$root/MAXIMIZE.md" ] || [ -f "$root/PATCH_QUEUE.md" ] || [ -f "$root/VERIFICATION_MATRIX.md" ] || [ -f "$root/ROUNDTRIP_PROMPTS.md" ]; then
  needs_patch_trio=1
fi

if [ "$needs_patch_trio" -eq 1 ]; then
  for file in PATCH_QUEUE.md VERIFICATION_MATRIX.md ROUNDTRIP_PROMPTS.md; do
    need_file "$file"
  done
fi

if [ -f "$root/MAXIMIZE.md" ]; then
  for file in CHECKLIST.md PROGRESS.md EXPERIMENTS.md; do
    need_file "$file"
  done
fi

no_code_declared=0
if [ -f "$root/CONTEXT_MANIFEST.md" ] && grep -Eq '^No code package: yes - .+' "$root/CONTEXT_MANIFEST.md"; then
  no_code_declared=1
fi

if [ ! -d "$root/code" ]; then
  if [ "$no_code_declared" -eq 1 ]; then
    warn "missing code/ directory accepted because CONTEXT_MANIFEST.md declares no-code"
  else
    err "missing code/ directory; add code artifacts or declare 'No code package: yes - <reason>' in CONTEXT_MANIFEST.md"
  fi
elif ! find "$root/code" -type f -print -quit | grep -q .; then
  if [ "$no_code_declared" -eq 1 ]; then
    warn "empty code/ directory accepted because CONTEXT_MANIFEST.md declares no-code"
  else
    err "code/ directory contains no files; add code artifacts or declare 'No code package: yes - <reason>' in CONTEXT_MANIFEST.md"
  fi
fi

if [ -f "$root/BASELINE_COMMIT" ]; then
  sha="$(head -n 1 "$root/BASELINE_COMMIT" | tr -d '[:space:]')"
  if ! printf '%s\n' "$sha" | grep -Eq '^[0-9a-f]{40}$'; then
    err "BASELINE_COMMIT first line is not a 40-char lowercase git SHA"
  fi
fi

placeholder_hits="$(find "$root" -type f \( -name '*.md' -o -name '*.txt' -o -name '*.html' \) -print0 | xargs -0 grep -nE '\{[A-Z][A-Z0-9_]*\}' 2>/dev/null || true)"
if [ -n "$placeholder_hits" ]; then
  err "unreplaced template placeholders found"
  printf '%s\n' "$placeholder_hits" >&2
fi

bad_paths="$(find "$root" \( -name '.git' -o -name '.env' -o -name 'node_modules' -o -name '.DS_Store' -o -name '__pycache__' \) -print)"
if [ -n "$bad_paths" ]; then
  err "unsafe or noisy paths found"
  printf '%s\n' "$bad_paths" >&2
fi

absolute_user_paths="$(find "$root" -type f -print0 | xargs -0 grep -n '/Users/' 2>/dev/null || true)"
if [ -n "$absolute_user_paths" ]; then
  warn "absolute /Users/ paths found; verify they are necessary and safe"
  printf '%s\n' "$absolute_user_paths" >&2
fi

if [ "$fail" -ne 0 ]; then
  exit 1
fi

printf 'OK: consult package passed structural checks: %s\n' "$root"
