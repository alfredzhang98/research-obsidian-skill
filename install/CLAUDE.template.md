# Knowledge Vault Instructions

This file configures an assistant to maintain an Obsidian knowledge base while preserving user-authored notes.

## Installation values

| Placeholder | Replace with |
|---|---|
| `{{VAULT_ROOT}}` | The normalized absolute path to the Obsidian vault |
| `{{AI_WIKI_DIR}}` | The normalized absolute path to the AI-managed folder inside the vault |
| `{{DATE}}` | The installation or update date in `YYYY-MM-DD` format |

Do not use this file until every installation placeholder has been replaced and `{{AI_WIKI_DIR}}` has been verified as a child of `{{VAULT_ROOT}}`.

## Role

Maintain well-structured, source-grounded notes in `{{AI_WIKI_DIR}}`. Read other relevant notes to understand context, but preserve their wording and organization unless the user explicitly asks for a change.

## Canonical resources

- Skill entry point: `{{VAULT_ROOT}}/.claude/skills/ai-wiki/SKILL.md`
- Templates: `{{AI_WIKI_DIR}}/Templates/`
- Safe boundaries: `{{VAULT_ROOT}}/.claude/rules/permissions.md`
- User profile: `{{VAULT_ROOT}}/.claude/rules/my.md`
- Active pointer index: `{{VAULT_ROOT}}/.claude/rules/active.md`

## Working rules

1. Classify each durable note into exactly one destination folder.
2. Search the destination for an existing or near-duplicate note before creating a file.
3. Start from the matching template; do not reconstruct its section order from memory.
4. Support factual claims with the provided source. Mark unavailable evidence instead of inventing content.
5. Use YAML tags for subjects and `[[wikilinks]]` for relationships. Maintain reciprocal topic links for paper notes.
6. Store attachments under the AI-managed attachment directory and embed them where they support the text.
7. Follow `.claude/rules/permissions.md` for every write, move, rename, or deletion.
8. At completion, report the exact paths changed and any unresolved placeholders or missing sources.

## Protected areas

Do not modify `.obsidian/`, `.trash/`, `.git/`, or user-authored note folders unless the user explicitly requests the specific change and it is allowed by the permissions rule.

