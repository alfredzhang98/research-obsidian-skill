---
name: vault-permissions
description: Safe, reusable boundaries for reading and writing an Obsidian vault
updated: "{{DATE}}"
---

# Vault Permissions

`{{VAULT_ROOT}}` is the resolved vault root. `{{AI_WIKI_DIR}}` is the resolved AI-managed directory inside that vault. Replace both placeholders during installation and verify that the second path is contained by the first.

## Zone policy

| Zone | Read and search | Create or edit | Move, rename, or delete |
|---|---|---|---|
| `{{AI_WIKI_DIR}}/**` | Allowed | Allowed for the current task | Only when explicitly requested, or when replacing an assistant-created artifact in the current task with a recoverable version |
| Other note folders under `{{VAULT_ROOT}}/**` | Allowed when relevant | Ask before changing existing content | Always ask first |
| `{{VAULT_ROOT}}/.claude/rules/**` | Allowed | Only for an explicit configuration request or the documented active-index update | Always ask first |
| `{{VAULT_ROOT}}/.obsidian/**` | Allowed only when needed for diagnosis | Do not modify | Do not modify |
| `{{VAULT_ROOT}}/.trash/**` | Do not inspect unless recovery is requested | Do not modify | Do not modify |
| `{{VAULT_ROOT}}/.git/**` | Read only for repository diagnostics | Do not modify directly | Do not modify directly |

## Required safeguards

1. Resolve and normalize every destination before writing. Stop if it is outside `{{VAULT_ROOT}}` or if a link redirects outside the vault.
2. Search for an existing note before creating a near-duplicate.
3. Preserve user-authored content. Prefer a new section or a clearly scoped patch over replacing a whole note.
4. Ask before destructive or hard-to-recover operations. Use version history or trash when available.
5. Never store credentials, access tokens, private keys, personal contact details, or unrelated private material in generated notes.
6. Treat external publication, sharing, messaging, and repository pushes as separate actions that require explicit user intent.
7. Leave Obsidian configuration and plugin state untouched unless the user specifically requests a configuration change.
8. Report every path created, edited, moved, or removed when the task finishes.
