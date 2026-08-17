#!/usr/bin/env python3
"""Validate package structure, skill metadata, links, and publication privacy."""

from __future__ import annotations

import argparse
import json
import py_compile
import re
import sys
from pathlib import Path


REQUIRED_PATHS = (
    ".gitattributes",
    ".gitignore",
    "LICENSE",
    "README.md",
    "THIRD_PARTY_NOTICES.md",
    "docs/USER-MANUAL.md",
    "install/CLAUDE.template.md",
    "install/dependencies.env",
    "install/install.ps1",
    "install/install.sh",
    "install/installer.py",
    "install/settings.template.json",
    "integrations/claude-defuddle/portable.patch",
    "rules/active.md",
    "rules/my.md",
    "rules/permissions.md",
    "skills/ai-wiki/SKILL.md",
    "skills/ai-wiki/references/figures-diagrams.md",
    "skills/ai-wiki/references/note-specs.md",
    "skills/ai-wiki/references/tools.md",
    "skills/ai-wiki/references/vault-guide.md",
    "skills/claude-defuddle/SKILL.md",
    "skills/paper-figures/SKILL.md",
    "skills/paper-figures/scripts/extract-figures.py",
    "skills/paper-search/SKILL.md",
    "templates/learning-note.md",
    "templates/paper-note.md",
    "templates/topic-plan.md",
)

SKILL_NAMES = ("ai-wiki", "claude-defuddle", "paper-figures", "paper-search")
TEXT_SUFFIXES = {".env", ".json", ".md", ".patch", ".ps1", ".py", ".sh", ".txt", ".yaml", ".yml"}

PRIVACY_PATTERNS = {
    "Windows user path": re.compile(r"[A-Za-z]:[\\/]+Users[\\/]", re.IGNORECASE),
    "macOS user path": re.compile(r"/Users/(?!you(?:/|\b)|<)[^\s/]+/"),
    "OneDrive path": re.compile(r"\bOneDrive\b", re.IGNORECASE),
    "email address": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE),
    "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"),
    "OpenAI-style secret": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "Google API key": re.compile(r"\bAIza[A-Za-z0-9_-]{25,}\b"),
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "non-English Han text": re.compile(r"[\u3400-\u9fff]"),
}

MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def iter_text_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.name in {"LICENSE", ".gitignore", ".gitattributes"} or path.suffix.lower() in TEXT_SUFFIXES:
            yield path


def validate_required(root: Path, errors: list[str]) -> None:
    for rel in REQUIRED_PATHS:
        path = root / rel
        if not path.is_file():
            errors.append(f"missing required file: {rel}")
        elif path.stat().st_size == 0:
            errors.append(f"empty required file: {rel}")


def validate_skill_metadata(root: Path, errors: list[str]) -> None:
    for name in SKILL_NAMES:
        path = root / "skills" / name / "SKILL.md"
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, flags=re.DOTALL)
        if not match:
            errors.append(f"missing YAML frontmatter: {path.relative_to(root)}")
            continue
        fields: dict[str, str] = {}
        for line in match.group(1).splitlines():
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip().strip("'\"")
        if fields.get("name") != name:
            errors.append(f"skill name mismatch in {path.relative_to(root)}: {fields.get('name')!r}")
        if not fields.get("description"):
            errors.append(f"missing skill description: {path.relative_to(root)}")
        unexpected = sorted(set(fields) - {"name", "description"})
        if unexpected:
            errors.append(f"unexpected skill frontmatter fields in {path.relative_to(root)}: {', '.join(unexpected)}")


def validate_privacy(root: Path, errors: list[str]) -> None:
    for path in iter_text_files(root):
        rel = path.relative_to(root).as_posix()
        # Pattern source text necessarily contains the signatures it checks.
        if rel == "scripts/validate_repo.py":
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for label, pattern in PRIVACY_PATTERNS.items():
            match = pattern.search(text)
            if match:
                line = text.count("\n", 0, match.start()) + 1
                errors.append(f"{label} in {rel}:{line}")


def validate_json(root: Path, errors: list[str]) -> None:
    for path in root.rglob("*.json"):
        if ".git" in path.parts:
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001 - report all parser failures
            errors.append(f"invalid JSON in {path.relative_to(root)}: {exc}")


def validate_markdown_links(root: Path, errors: list[str]) -> None:
    for path in root.rglob("*.md"):
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        for raw_target in MARKDOWN_LINK.findall(text):
            target = raw_target.strip().split()[0].strip("<>")
            if not target or target.startswith(("#", "http://", "https://", "mailto:")):
                continue
            target = target.split("#", 1)[0]
            if not target or "{{" in target or "_attachments" in target:
                continue
            candidate = (path.parent / target).resolve()
            if not candidate.exists():
                errors.append(f"broken relative link in {path.relative_to(root)}: {raw_target}")


def validate_python(root: Path, errors: list[str]) -> None:
    for path in root.rglob("*.py"):
        if ".git" in path.parts:
            continue
        try:
            py_compile.compile(str(path), doraise=True)
        except py_compile.PyCompileError as exc:
            errors.append(f"Python syntax error in {path.relative_to(root)}: {exc.msg}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root.resolve()

    errors: list[str] = []
    validate_required(root, errors)
    validate_skill_metadata(root, errors)
    validate_privacy(root, errors)
    validate_json(root, errors)
    validate_markdown_links(root, errors)
    validate_python(root, errors)

    if errors:
        print(f"Validation failed with {len(errors)} issue(s):", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Validation passed: {len(REQUIRED_PATHS)} required files, {len(SKILL_NAMES)} skills, privacy scan clean.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
