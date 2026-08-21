# Thin wrapper around install/installer.py (the canonical installer).
#
# Usage:
#   .\install\install.ps1 [-VaultPath <path>] [-AiWikiName <name>] [-PaperSearchDir <path>]
#     [-SkipVault]
#
# Defaults:
#   VaultPath       : the parent of this repository
#   AiWikiName      : 0ai_wiki
#   PaperSearchDir  : $HOME\paper-search-mcp

param(
    [string]$VaultPath = "",
    [string]$AiWikiName = "0ai_wiki",
    [string]$PaperSearchDir = "",
    [switch]$SkipVault
)

$ErrorActionPreference = "Stop"

$RepoDir = Split-Path -Parent $PSScriptRoot
$Installer = Join-Path $RepoDir "install\installer.py"

$python = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $python) { throw "python not found; install Python 3 then rerun" }

# Positional order is VAULT_PATH AI_WIKI_NAME PAPER_SEARCH_DIR, so VaultPath
# must be filled in rather than skipped -- otherwise AiWikiName slides into its slot.
if (-not $VaultPath) { $VaultPath = Split-Path -Parent $RepoDir }

$pyArgs = @($Installer, $VaultPath, $AiWikiName)
if ($PaperSearchDir) { $pyArgs += $PaperSearchDir }
if ($SkipVault) { $pyArgs += "--skip-vault" }

& $python @pyArgs
exit $LASTEXITCODE
