#!/usr/bin/env python3
"""Install the research-obsidian skill suite into an Obsidian vault.

The canonical, cross-platform installer. The shell and PowerShell entry points
(``install.sh`` / ``install.ps1``) are thin wrappers around this module.

Steps:
  1. Copy owned skills: ``ai-wiki`` into ``<vault>/.claude/skills/`` (vault-scoped)
     and ``paper-figures`` / ``paper-search`` / ``claude-defuddle`` into
     ``~/.claude/skills/`` (user-scoped).
  2. Clone ``claude-defuddle`` at a pinned revision and apply the portability patch.
  3. Clone ``paper-search-mcp`` at a pinned revision.
  4. Create (or reuse) a Python environment with PyMuPDF + Pillow for paper-figures.
  5. Render every ``{{...}}`` placeholder in skills, rules, and config templates.
  6. Seed dependency ``.env`` files from a synced secrets directory, if one exists.
  7. Create the AI-managed folder and copy the note templates into it.
  8. Write ``.claude/rules/{my,permissions,active}.md``, ``CLAUDE.md``, and
     ``.claude/settings.json``.

On a machine that already has the vault (synced by OneDrive, Dropbox, or the
like), ``--skip-vault`` installs only the machine-scoped half. That is the
new-machine command: the vault arrives with the sync client, this renders the
paths for the local machine.

Usage:
    python install/installer.py [VAULT_PATH] [AI_WIKI_NAME] [PAPER_SEARCH_DIR]
                                [--skip-vault]

``--skip-vault`` runs only the machine-scoped half (steps 1-user, 2, 3, 4, 5),
which is what you want when the vault already carries a customised ai-wiki,
rules set, or CLAUDE.md that must not be overwritten.
"""

from __future__ import annotations

import argparse
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

# ai-wiki is vault-scoped (CLAUDE.md points at <vault>/.claude/skills/ai-wiki);
# the other three are user-scoped under ~/.claude/skills.
USER_SKILLS = ("paper-figures", "paper-search", "claude-defuddle")
VAULT_SKILLS = ("ai-wiki",)

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
    if not path.is_file():
        sys.exit(
            f"error: {path} is missing. It pins the third-party revisions and must ship "
            "with the repository; check that .gitignore does not exclude it."
        )
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
    """Return a Python 3 interpreter that actually runs.

    Candidates are probed rather than trusted: on Windows ``python3`` normally
    resolves to the Microsoft Store app-execution alias, which is a stub, not
    an interpreter. The interpreter running this installer is tried first.
    """
    for candidate in (sys.executable, which("python3"), which("python")):
        if not candidate:
            continue
        try:
            probe = subprocess.run(
                [candidate, "-c", "import sys; print(sys.version_info[0])"],
                capture_output=True, text=True, timeout=30,
            )
        except (OSError, subprocess.SubprocessError):
            continue
        if probe.returncode == 0 and probe.stdout.strip() == "3":
            return candidate
    return None


def ensure_figures_python(venv_dir: Path) -> str:
    """Return a Python interpreter that has PyMuPDF and Pillow, creating a venv if needed.

    ``venv_dir`` lives outside the skill directory: step 1 removes and re-copies
    the skill on every run, which would otherwise discard the environment and
    re-download PyMuPDF each time.
    """
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
    venv_python = next((c for c in candidates if c.is_file()), None)
    if venv_python is None:
        sys.exit(f"error: created {venv_dir} but found no interpreter inside it")
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


def has_values(path: Path) -> bool:
    """True if an env file holds at least one non-empty, non-comment assignment."""
    if not path.is_file():
        return False
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line and line.split("=", 1)[1].strip():
            return True
    return False


def seed_env(secrets_dir: Path, name: str, dest: Path) -> None:
    """Copy ``<secrets_dir>/<name>.env`` to ``dest`` unless ``dest`` is already filled in.

    The secrets directory is expected to travel with the vault (a synced folder),
    not with this repository -- keys must never be committed. Absent directory or
    file means this step does nothing.
    """
    src = secrets_dir / f"{name}.env"
    if not src.is_file():
        return
    if has_values(dest):
        log(f"{dest.name} already has values; left untouched")
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(src, dest)
    log(f"seeded {dest.name} from {src}")


def render_to(src: Path, dest: Path, values: dict[str, str]) -> None:
    """Render ``src`` into ``dest``, leaving the source template untouched."""
    text = src.read_text(encoding="utf-8")
    for placeholder, value in values.items():
        text = text.replace(placeholder, value)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(text, encoding="utf-8")


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
    parser.add_argument(
        "--secrets-dir",
        type=Path,
        default=None,
        help="directory holding synced <name>.env files to seed dependency checkouts with "
             "(default: <vault>/.claude/secrets). Keys live with the vault, never in this repo",
    )
    parser.add_argument(
        "--skip-vault",
        action="store_true",
        help="install only the machine-scoped pieces (user skills, integrations, dependency "
             "checkouts) and leave the vault's ai-wiki skill, rules, CLAUDE.md, settings.json, "
             "and folder skeleton untouched",
    )
    args = parser.parse_args()

    vault_path = args.vault_path.resolve()
    ai_wiki_name = args.ai_wiki_name
    paper_search_dir = args.paper_search_dir.resolve()
    secrets_dir = (args.secrets_dir or vault_path / ".claude" / "secrets").resolve()
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
    for skill in USER_SKILLS:
        dest = skills_home / skill
        shutil.rmtree(dest, ignore_errors=True)
        shutil.copytree(repo_dir / "skills" / skill, dest)
        log(f"installed skill (user): {skill}")
    vault_skills_dir = vault_path / ".claude" / "skills"
    if args.skip_vault:
        log("--skip-vault: leaving vault-scoped skills, rules, and config untouched")
    else:
        for skill in VAULT_SKILLS:
            dest = vault_skills_dir / skill
            shutil.rmtree(dest, ignore_errors=True)
            shutil.copytree(repo_dir / "skills" / skill, dest)
            log(f"installed skill (vault): {skill}")

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
    seed_env(secrets_dir, "paper-search", paper_search_dir / ".env")

    # 4. Python environment for paper-figures --------------------------------
    figures_dir = skills_home / "paper-figures"
    figures_python = ensure_figures_python(integrations_dir / "paper-figures-venv")
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

    if not args.skip_vault:
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
            render_to(repo_dir / "install" / "CLAUDE.template.md", claude_md, values)
            log("wrote CLAUDE.md")

        render_to(
            repo_dir / "install" / "settings.template.json",
            vault_path / ".claude" / "settings.json",
            values,
        )
        log("wrote .claude/settings.json")

    print()
    print("Done.")
    print(f"  Next: edit {rules_dir / 'my.md'} with your profile and research directions.")
    print(f"  paper-search: uv run --directory {paper_search_dir} paper-search ...")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
