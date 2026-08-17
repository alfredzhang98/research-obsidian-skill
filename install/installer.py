#!/usr/bin/env python3
"""Install the research-obsidian skill suite into an Obsidian vault.

The canonical, cross-platform installer. The shell and PowerShell entry points
(``install.sh`` / ``install.ps1``) are thin wrappers around this module.

Steps:
  1. Copy owned skills (ai-wiki, paper-figures, paper-search, claude-defuddle)
     into ``~/.claude/skills/``.
  2. Clone ``claude-defuddle`` at a pinned revision and apply the portability patch.
  3. Clone ``paper-search-mcp`` at a pinned revision.
  4. Create (or reuse) a Python environment with PyMuPDF + Pillow for paper-figures.
  5. Render every ``{{...}}`` placeholder in skills, rules, and config templates.
  6. Create the AI-managed folder and copy the note templates into it.
  7. Write ``.claude/rules/{my,permissions,active}.md``, ``CLAUDE.md``, and
     ``.claude/settings.json``.

Usage:
    python install/installer.py [VAULT_PATH] [AI_WIKI_NAME] [PAPER_SEARCH_DIR]
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import venv
from datetime import date
from pathlib import Path

PLACEHOLDERS = (
    "{{VAULT_ROOT}}",
    "{{AI_WIKI_DIR}}",
    "{{DATE}}",
    "{{PAPER_SEARCH_DIR}}",
    "{{PAPER_FIGURES_PYTHON}}",
    "{{PAPER_FIGURES_SCRIPT}}",
    "{{DEFUDDLE_PYTHON}}",
    "{{DEFUDDLE_SCRIPT}}",
)

OWNED_SKILLS = ("ai-wiki", "paper-figures", "paper-search", "claude-defuddle")

AI_WIKI_SUBDIRS = (
    "Templates",
    "Research/papers",
    "Research/learning",
    "Research/topics",
    "Research/designs",
    "Research/ideas",
    "Research/figures",
    "Projects",
    "Resources/references",
    "Daily Notes",
    "Inbox",
    "Archive",
    "_attachments/paper-figures",
    "_attachments/screenshots",
)


def log(msg: str) -> None:
    print(f"  {msg}")


def run(cmd: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=str(cwd) if cwd else None, check=True)


def read_deps(repo_dir: Path) -> dict[str, str]:
    deps: dict[str, str] = {}
    path = repo_dir / "install" / "dependencies.env"
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        deps[key.strip()] = value.strip()
    return deps


def which(cmd: str) -> str | None:
    return shutil.which(cmd)


def find_python() -> str | None:
    for candidate in ("python3", "python"):
        found = which(candidate)
        if found:
            return found
    return None


def ensure_figures_python(skills_home: Path, figures_dir: Path) -> str:
    """Return a Python interpreter that has PyMuPDF and Pillow, creating a venv if needed."""
    venv_dir = figures_dir / ".venv"
    candidates = [venv_dir / "Scripts" / "python.exe", venv_dir / "bin" / "python"]
    for cand in candidates:
        if cand.is_file():
            if subprocess.run([str(cand), "-c", "import fitz, PIL"], capture_output=True).returncode == 0:
                log(f"reusing paper-figures venv: {cand}")
                return str(cand)

    base = find_python()
    if base:
        probe = subprocess.run([base, "-c", "import fitz, PIL"], capture_output=True)
        if probe.returncode == 0:
            log(f"using system python (fitz + PIL present): {base}")
            return base

    if not base:
        sys.exit("error: no Python 3 interpreter found; install Python 3 and rerun")
    log("creating paper-figures venv with pymupdf + Pillow")
    venv.create(venv_dir, with_pip=True)
    venv_python = venv_dir / ("Scripts" / "python.exe" if os.name == "nt" else "bin" / "python")
    run([str(venv_python), "-m", "pip", "install", "--quiet", "pymupdf", "Pillow"])
    return str(venv_python)


def clone_pinned(url: str, rev: str, dest: Path, label: str) -> None:
    if (dest / ".git").is_dir():
        log(f"{label} present; checking out pinned revision")
        subprocess.run(["git", "-C", str(dest), "checkout", "--quiet", rev], capture_output=True)
        return
    shutil.rmtree(dest, ignore_errors=True)
    log(f"cloning {label} @ {rev}")
    run(["git", "clone", "--quiet", url, str(dest)])
    run(["git", "-C", str(dest), "checkout", "--quiet", rev])


def render(path: Path, values: dict[str, str]) -> None:
    text = path.read_text(encoding="utf-8")
    for placeholder, value in values.items():
        text = text.replace(placeholder, value)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    repo_dir = Path(__file__).resolve().parents[1]

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("vault_path", nargs="?", type=Path, default=repo_dir.parent)
    parser.add_argument("ai_wiki_name", nargs="?", default="0ai_wiki")
    parser.add_argument("paper_search_dir", nargs="?", type=Path, default=Path.home() / "paper-search-mcp")
    args = parser.parse_args()

    vault_path = args.vault_path.resolve()
    ai_wiki_name = args.ai_wiki_name
    paper_search_dir = args.paper_search_dir.resolve()
    skills_home = Path.home() / ".claude" / "skills"
    integrations_dir = Path.home() / ".claude" / "integrations"
    rules_dir = vault_path / ".claude" / "rules"
    ai_wiki_dir = vault_path / ai_wiki_name
    today = date.today().isoformat()

    deps = read_deps(repo_dir)

    print(f"==> Vault:          {vault_path}")
    print(f"==> AI folder:      {ai_wiki_dir}")
    print(f"==> Skills home:    {skills_home}")
    print(f"==> paper-search:   {paper_search_dir}")

    # 1. Copy owned skills --------------------------------------------------
    skills_home.mkdir(parents=True, exist_ok=True)
    for skill in OWNED_SKILLS:
        dest = skills_home / skill
        shutil.rmtree(dest, ignore_errors=True)
        shutil.copytree(repo_dir / "skills" / skill, dest)
        log(f"installed skill: {skill}")

    # 2. claude-defuddle (pinned + patched) ---------------------------------
    # The wrapper skill lives at skills/claude-defuddle/SKILL.md; the actual
    # upstream checkout goes into a separate machine-local dependency dir so
    # the two never collide.
    integrations_dir.mkdir(parents=True, exist_ok=True)
    defuddle_dir = integrations_dir / "claude-defuddle"
    clone_pinned(deps["DEFUDDLE_URL"], deps["DEFUDDLE_REV"], defuddle_dir, "claude-defuddle")
    patch_path = repo_dir / "integrations" / "claude-defuddle" / "portable.patch"
    check = subprocess.run(["git", "-C", str(defuddle_dir), "apply", "--check", str(patch_path)], capture_output=True)
    if check.returncode == 0:
        run(["git", "-C", str(defuddle_dir), "apply", str(patch_path)])
        log("applied portability patch to claude-defuddle")
    else:
        log("portability patch already applied or not needed")

    # 3. paper-search-mcp (pinned) ------------------------------------------
    clone_pinned(deps["PAPER_SEARCH_URL"], deps["PAPER_SEARCH_REV"], paper_search_dir, "paper-search-mcp")

    # 4. Python environment for paper-figures --------------------------------
    figures_dir = skills_home / "paper-figures"
    figures_python = ensure_figures_python(skills_home, figures_dir)
    defuddle_python = find_python() or figures_python

    # 5. Render placeholders -------------------------------------------------
    figures_script = figures_dir / "scripts" / "extract-figures.py"
    defuddle_script = defuddle_dir / "defuddle.py"
    values = {
        "{{VAULT_ROOT}}": str(vault_path),
        "{{AI_WIKI_DIR}}": str(ai_wiki_dir),
        "{{DATE}}": today,
        "{{PAPER_SEARCH_DIR}}": str(paper_search_dir),
        "{{PAPER_FIGURES_PYTHON}}": figures_python,
        "{{PAPER_FIGURES_SCRIPT}}": str(figures_script),
        "{{DEFUDDLE_PYTHON}}": defuddle_python,
        "{{DEFUDDLE_SCRIPT}}": str(defuddle_script),
    }
    render(skills_home / "paper-search" / "SKILL.md", values)
    render(skills_home / "paper-figures" / "SKILL.md", values)
    render(skills_home / "claude-defuddle" / "SKILL.md", values)
    log("rendered skill placeholders")

    # 6. AI-managed folder + templates ---------------------------------------
    for sub in AI_WIKI_SUBDIRS:
        (ai_wiki_dir / sub).mkdir(parents=True, exist_ok=True)
    shutil.copytree(repo_dir / "templates", ai_wiki_dir / "Templates", dirs_exist_ok=True)
    log(f"wrote AI folder skeleton + templates under {ai_wiki_name}/")

    # 7. Rules ---------------------------------------------------------------
    rules_dir.mkdir(parents=True, exist_ok=True)
    if not (rules_dir / "my.md").exists():
        shutil.copy(repo_dir / "rules" / "my.md", rules_dir / "my.md")
    shutil.copy(repo_dir / "rules" / "permissions.md", rules_dir / "permissions.md")
    if not (rules_dir / "active.md").exists():
        shutil.copy(repo_dir / "rules" / "active.md", rules_dir / "active.md")
    for name in ("my.md", "permissions.md", "active.md"):
        target = rules_dir / name
        if target.exists():
            render(target, values)
    log("wrote .claude/rules/{my,permissions,active}.md (my.md / active.md kept if present)")

    # 8. CLAUDE.md + settings.json -------------------------------------------
    (vault_path / ".claude").mkdir(parents=True, exist_ok=True)
    claude_md = vault_path / "CLAUDE.md"
    if claude_md.exists():
        log("CLAUDE.md already present; leaving it untouched")
    else:
        template = repo_dir / "install" / "CLAUDE.template.md"
        render(template, values)
        shutil.copy(template, claude_md)
        log("wrote CLAUDE.md")

    settings_template = repo_dir / "install" / "settings.template.json"
    render(settings_template, values)
    shutil.copy(settings_template, vault_path / ".claude" / "settings.json")
    log("wrote .claude/settings.json")

    print()
    print("Done.")
    print(f"  Next: edit {rules_dir / 'my.md'} with your profile and research directions.")
    print(f"  paper-search: uv run --directory {paper_search_dir} paper-search ...")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
