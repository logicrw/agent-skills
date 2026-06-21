#!/bin/sh
set -eu

if command -v sumink >/dev/null 2>&1; then
  SUMINK="sumink"
else
  SUMINK="node /Applications/Sumink.app/Contents/Resources/cli/cli.cjs"
fi

need_json_array() {
  jq -e 'type == "array"' >/dev/null
}

need_nonempty() {
  test -n "$(cat)"
}

version="$($SUMINK --version)"
test -n "$version"
printf 'version=%s\n' "$version"

$SUMINK space list --format json | need_json_array
printf 'space_list=ok\n'

$SUMINK resource read introduction --format text | need_nonempty
$SUMINK resource read sumink-flavored-markdown --format text | need_nonempty
$SUMINK resource read infinity-canvas-markup --format text | need_nonempty
printf 'resources=ok\n'

$SUMINK card search "Skill测试" --format json | need_json_array
printf 'card_search=ok\n'

printf 'sumink_smoke=ok\n'
