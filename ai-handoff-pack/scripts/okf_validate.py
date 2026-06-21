#!/usr/bin/env python3
import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

try:
    import yaml
except Exception:
    yaml = None


RESERVED = {"index.md", "log.md"}
RECOMMENDED_FIELDS = ("title", "description", "resource", "tags", "timestamp")
LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
DATE_HEADING_RE = re.compile(r"^##\s+(\d{4}-\d{2}-\d{2})\s*$", re.MULTILINE)
ANY_H2_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)


def issue(severity, code, path, message):
    return {"severity": severity, "code": code, "path": path, "message": message}


def read_text(path):
    return path.read_text(encoding="utf-8")


def split_frontmatter(text):
    if not text.startswith("---\n"):
        return None, text, "missing frontmatter"
    end = text.find("\n---\n", 4)
    if end == -1:
        return None, text, "unterminated frontmatter"
    frontmatter = text[4:end]
    body = text[end + 5 :]
    return frontmatter, body, None


def fallback_yaml_parse(frontmatter):
    data = {}
    for raw_line in frontmatter.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"cannot parse YAML line: {raw_line!r}")
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            raise ValueError(f"empty YAML key: {raw_line!r}")
        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            data[key] = [] if not inner else [part.strip().strip("\"'") for part in inner.split(",")]
        else:
            data[key] = value.strip("\"'")
    return data


def parse_frontmatter(frontmatter):
    if yaml is not None:
        parsed = yaml.safe_load(frontmatter) if frontmatter.strip() else {}
    else:
        parsed = fallback_yaml_parse(frontmatter)
    if parsed is None:
        parsed = {}
    if not isinstance(parsed, dict):
        raise ValueError("frontmatter must parse to a mapping")
    return parsed


def normalize_link_target(bundle_root, source_path, href):
    href = href.strip()
    lower = href.lower()
    if (
        not href
        or href.startswith("#")
        or re.match(r"^[a-z][a-z0-9+.-]*:", lower)
        or lower.startswith("mailto:")
    ):
        return None
    href = href.split("#", 1)[0].split("?", 1)[0]
    if not href:
        return None
    href = unquote(href)
    if href.startswith("/"):
        return (bundle_root / href.lstrip("/")).resolve()
    return (source_path.parent / href).resolve()


def target_exists(target):
    if target.exists():
        return True
    if target.suffix == "":
        md_target = target.with_suffix(".md")
        if md_target.exists():
            return True
    if str(target).endswith("/"):
        return target.is_dir()
    return False


def validate_links(bundle_root, file_path, text, rel):
    findings = []
    for match in LINK_RE.finditer(text):
        href = match.group(1)
        target = normalize_link_target(bundle_root, file_path, href)
        if target is None:
            continue
        try:
            target.relative_to(bundle_root.resolve())
        except ValueError:
            continue
        if not target_exists(target):
            findings.append(issue("warning", "broken-link", rel, f"internal link target not found: {href}"))
    return findings


def validate_concept(bundle_root, path):
    rel = path.relative_to(bundle_root).as_posix()
    findings = []
    try:
        text = read_text(path)
    except UnicodeDecodeError:
        return [issue("error", "encoding", rel, "file is not valid UTF-8")]

    frontmatter, body, error = split_frontmatter(text)
    if error:
        findings.append(issue("error", "frontmatter", rel, error))
        findings.extend(validate_links(bundle_root, path, text, rel))
        return findings

    try:
        data = parse_frontmatter(frontmatter)
    except Exception as exc:
        findings.append(issue("error", "frontmatter-yaml", rel, f"frontmatter is not parseable YAML: {exc}"))
        findings.extend(validate_links(bundle_root, path, body, rel))
        return findings

    concept_type = data.get("type")
    if not isinstance(concept_type, str) or not concept_type.strip():
        findings.append(issue("error", "type", rel, "frontmatter must contain a non-empty string type"))

    for field in RECOMMENDED_FIELDS:
        if field not in data or data.get(field) in (None, ""):
            findings.append(issue("warning", "recommended-field", rel, f"recommended field missing: {field}"))

    findings.extend(validate_links(bundle_root, path, body, rel))
    return findings


def validate_index(bundle_root, path):
    rel = path.relative_to(bundle_root).as_posix()
    findings = []
    text = read_text(path)
    frontmatter, body, error = split_frontmatter(text)
    is_root_index = rel == "index.md"
    if frontmatter is not None:
        if not is_root_index:
            findings.append(issue("error", "index-frontmatter", rel, "only the bundle-root index.md may contain frontmatter"))
        try:
            data = parse_frontmatter(frontmatter)
        except Exception as exc:
            findings.append(issue("error", "index-yaml", rel, f"index frontmatter is not parseable YAML: {exc}"))
            data = {}
        if is_root_index and data and set(data) - {"okf_version"}:
            findings.append(issue("warning", "index-frontmatter-extra", rel, "root index.md frontmatter should only declare okf_version"))
        text_for_links = body
    else:
        text_for_links = text
    findings.extend(validate_links(bundle_root, path, text_for_links, rel))
    return findings


def validate_log(bundle_root, path):
    rel = path.relative_to(bundle_root).as_posix()
    findings = []
    text = read_text(path)
    frontmatter, body, _ = split_frontmatter(text)
    if frontmatter is not None:
        findings.append(issue("error", "log-frontmatter", rel, "log.md should not contain frontmatter"))
        text = body

    h2_values = [match.group(1).strip() for match in ANY_H2_RE.finditer(text)]
    date_values = [match.group(1) for match in DATE_HEADING_RE.finditer(text)]
    if h2_values and len(h2_values) != len(date_values):
        findings.append(issue("error", "log-date-heading", rel, "all level-2 log headings must be YYYY-MM-DD dates"))
    if not date_values:
        findings.append(issue("warning", "log-empty", rel, "log.md has no YYYY-MM-DD date headings"))
    else:
        dates = []
        for value in date_values:
            try:
                dates.append(dt.date.fromisoformat(value))
            except ValueError:
                findings.append(issue("error", "log-date", rel, f"invalid date heading: {value}"))
        if dates and dates != sorted(dates, reverse=True):
            findings.append(issue("warning", "log-order", rel, "log.md date headings should be newest first"))

    findings.extend(validate_links(bundle_root, path, text, rel))
    return findings


def validate_bundle(bundle_root):
    bundle_root = bundle_root.resolve()
    findings = []
    if not bundle_root.exists():
        return [issue("error", "bundle-root", str(bundle_root), "bundle path does not exist")]
    if not bundle_root.is_dir():
        return [issue("error", "bundle-root", str(bundle_root), "bundle path is not a directory")]
    if yaml is None:
        findings.append(issue("warning", "yaml-parser", ".", "PyYAML is not installed; using a limited YAML parser"))

    markdown_files = sorted(bundle_root.rglob("*.md"))
    if not markdown_files:
        findings.append(issue("warning", "empty-bundle", ".", "no Markdown files found"))

    has_root_index = (bundle_root / "index.md").exists()
    if not has_root_index:
        findings.append(issue("warning", "missing-root-index", ".", "root index.md is missing; consumers may synthesize one"))

    for path in markdown_files:
        if path.name == "index.md":
            findings.extend(validate_index(bundle_root, path))
        elif path.name == "log.md":
            findings.extend(validate_log(bundle_root, path))
        else:
            findings.extend(validate_concept(bundle_root, path))
    return findings


def main():
    parser = argparse.ArgumentParser(description="Validate an OKF v0.1 bundle.")
    parser.add_argument("bundle", type=Path, help="Path to the OKF bundle root")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    args = parser.parse_args()

    findings = validate_bundle(args.bundle)
    errors = [item for item in findings if item["severity"] == "error"]
    warnings = [item for item in findings if item["severity"] == "warning"]
    result = {
        "bundle": str(args.bundle.resolve()),
        "okf_version": "0.1",
        "errors": len(errors),
        "warnings": len(warnings),
        "findings": findings,
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"OKF bundle: {result['bundle']}")
        print(f"errors={result['errors']} warnings={result['warnings']}")
        for item in findings:
            print(f"{item['severity'].upper()} {item['path']} [{item['code']}]: {item['message']}")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
