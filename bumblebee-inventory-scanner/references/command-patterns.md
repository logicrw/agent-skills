# Command Patterns

Always write scan output to a file. Use `work/` when no output path is requested.

## Project Package Inventory

```bash
mkdir -p work
PROJECT_ROOT="${PROJECT_ROOT:-$PWD}"

bumblebee roots --profile project --root "$PROJECT_ROOT"
bumblebee scan --profile project \
  --root "$PROJECT_ROOT" \
  --ecosystem npm,pypi,go,rubygems,packagist \
  --max-duration 5m \
  --output file \
  --output-file work/bumblebee-project.ndjson
```

## Baseline Developer Surface

```bash
mkdir -p work

bumblebee roots --profile baseline
bumblebee scan --profile baseline \
  --ecosystem npm,pypi,go,mcp,editor-extension,browser-extension \
  --max-duration 5m \
  --output file \
  --output-file work/bumblebee-baseline.ndjson
```

## Advisory Exposure

```bash
mkdir -p work
SCAN_ROOT="${SCAN_ROOT:-$PWD}"
CATALOG="${CATALOG:-work/exposure-catalog.json}"

jq -e '.schema_version=="0.1.0" and (.entries|type=="array")' "$CATALOG" >/dev/null
bumblebee roots --profile deep --root "$SCAN_ROOT"
bumblebee scan --profile deep \
  --root "$SCAN_ROOT" \
  --ecosystem npm,pypi,go,rubygems,packagist \
  --exposure-catalog "$CATALOG" \
  --findings-only \
  --max-duration 10m \
  --output file \
  --output-file work/bumblebee-findings.ndjson
```

## MCP JSON Inventory

```bash
mkdir -p work

bumblebee scan --profile baseline \
  --ecosystem mcp \
  --max-duration 3m \
  --output file \
  --output-file work/bumblebee-mcp.ndjson
```

Project-local MCP JSON:

```bash
mkdir -p work
PROJECT_ROOT="${PROJECT_ROOT:-$PWD}"

bumblebee scan --profile project \
  --root "$PROJECT_ROOT" \
  --ecosystem mcp \
  --max-duration 3m \
  --output file \
  --output-file work/bumblebee-project-mcp.ndjson
```

## Extensions

```bash
mkdir -p work

bumblebee scan --profile baseline \
  --ecosystem editor-extension,browser-extension \
  --max-duration 3m \
  --output file \
  --output-file work/bumblebee-extensions.ndjson
```
