# Exposure Catalog

Use exposure catalogs for advisory-style matching. Matches are exact by `(ecosystem, package, version)` unless explicitly reported as lower-confidence name-only evidence.

Minimal catalog:

```json
{
  "schema_version": "0.1.0",
  "entries": [
    {
      "id": "advisory-or-case-id",
      "ecosystem": "npm",
      "package": "example-package",
      "versions": ["1.2.3"],
      "severity": "high",
      "reference": "https://example.invalid/advisory"
    }
  ]
}
```

Guidance:

- Use precise package names and versions when available.
- For MCP npm/PyPI/uv launchers, versions are often empty; name-only matching is less certain.
- Docker image tags may appear as versions with medium confidence.
- `--findings-only` requires `--exposure-catalog` and suppresses package records.
