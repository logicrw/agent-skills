# Coverage Boundaries

| Area | v0.1.1 behavior |
|---|---|
| npm | Parses npm, pnpm, Yarn, and Bun text lockfile/install metadata. |
| Yarn PnP | `.pnp.cjs` is not parsed. |
| Bun binary lockfile | `bun.lockb` is not parsed; expect diagnostics only. |
| Python | Parses installed dist/egg metadata and supported PyPI project evidence. |
| Go | Parses Go module evidence; global module cache can be very large. |
| Ruby | Parses supported Rubygems evidence such as lockfiles/gemspecs. |
| Composer | Parses supported Packagist/Composer evidence such as `composer.lock` and installed metadata. |
| MCP | Parses supported JSON host configs and project `.mcp.json` shapes. |
| MCP secrets | Env values and env key names are not emitted. |
| Remote MCP | URL entries are sanitized to scheme and host; path, query, fragment, and userinfo are dropped. |
| Codex config | `~/.codex/config.toml` is not parsed by Bumblebee v0.1.1. |
| Continue config | Continue YAML is not parsed. |
| Source code | Arbitrary source files are not read as package evidence. |
| Package managers | Package-manager commands are not executed. |
| Other ecosystems | Cargo, Maven, NuGet, Safari extensions, Homebrew-only inventory, and loose agent-skill directories are out of scope. |

Notes:

- Go baseline scans under `~/go/pkg/mod` can emit many records. Scope ecosystems and roots.
- Editor extension scans can surface vendored npm dependencies. Group by `source_file` or extension before drawing conclusions.
