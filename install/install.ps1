# Thin wrapper around install/installer.py (the canonical installer).
#
# Usage:
#   .\install\install.ps1 [-VaultPath <path>] [-AiWikiName <name>] [-PaperSearchDir <path>]
#
# Defaults:
#   VaultPath       : the parent of this repository
#   AiWikiName      : 0ai_wiki
#   PaperSearchDir  : $HOME\paper-search-mcp

param(
    [string]$VaultPath = "",
    [string]$AiWikiName = "0ai_wiki",
    [string]$PaperSearchDir = ""
)

$ErrorActionPreference = "Stop"

$RepoDir = Split-Path -Parent $PSScriptRoot
$Installer = Join-Path $RepoDir "install\installer.py"

$python = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $python) { throw "python not found; install Python 3 then rerun" }

$pyArgs = @($Installer)
if ($VaultPath) { $pyArgs += $VaultPath }
$pyArgs += $AiWikiName
if ($PaperSearchDir) { $pyArgs += $PaperSearchDir }

& $python @pyArgs
exit $LASTEXITCODE
