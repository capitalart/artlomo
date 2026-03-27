# Markdown Auto-Fix Guide

## TL;DR - Is It Safe?

## Yes, but with caveats

- ✅ **Safe to auto-fix**: MD022, MD032, MD031, MD040, MD038 (what `--auto` does)
- ⚠️ **Semi-safe**: MD036 (emphasis as heading) - needs manual review
- ❌ **Not auto-fixable**: MD024 (duplicate headings), MD026 (trailing punctuation)

## Usage

### Option 1: Safe Automatic Fixes (Recommended)

```bash
./fix-markdown.sh --auto
```

## What it fixes

- MD022: Adds blank lines around headings
- MD032: Adds blank lines around lists
- MD031: Adds blank lines around code blocks
- MD040: Adds language identifiers to code blocks (defaults to `text` if ambiguous)
- MD038: Removes spaces inside inline code

**Risk level:** Very low - these are formatting-only changes

### Option 2: Check Without Fixing

```bash
./fix-markdown.sh --check
```

Lists all errors without modifying files. Useful before running fixes.

### Option 3: All Fixes (With Manual Review)

```bash
./fix-markdown.sh --all
```

Runs auto-fixes + automatically converts emphasis-used-as-headings (`**Title**` → `## Title`).

**Risk level:** Medium - MD036 conversions need review to ensure correct heading level

## Why Some Errors Can't Be Auto-Fixed

### MD024 - Duplicate Headings

## Example

```markdown

## Configuration

...

## Configuration  ← Same heading text (error)

```

**Why manual:** Computer can't decide which one to rename. Could be:

- Rename second to `## Configuration (Part 2)`
- Rename first to `## Setup Configuration`
- Delete duplicate entirely

**Fix:** Manually make headings unique

### MD026 - Trailing Punctuation in Headings

Example

```markdown

## Installation Steps:  ← Colon at end (error)

```

**Why manual:** Sometimes punctuation is intentional in technical headings:

- `## What's Next?` (rhetorical)
- `## Key Points:` (list follows)

**Fix:** Remove punctuation if truly not needed

### MD036 - Emphasis Used as a Heading

Example

```markdown

## Main Section

Content here...
```

**Why risky:** The script converts this to `## Main Section`, but it can't know:

- Should it be `#` (top level) or `##` (sub-level)?
- Is this really meant to be a heading, or just bold text?

**How `--all` handles it:** Converts to `##` (reasonable default)

**Risk:** May create incorrect hierarchy - requires review

## Workflow Recommendations

### For Development Work

```bash

# Before committing

./fix-markdown.sh --auto
git diff                    # Review changes
git add .
git commit -m "fix: apply markdown linting fixes"
```

### For User-Generated Content

If creating a document and want to ensure compliance:

```bash
./fix-markdown.sh --check   # See what needs fixing
./fix-markdown.sh --auto    # Apply safe fixes

# Manually review any remaining errors

```

### For CI/CD Pipeline

```bash

# Pre-commit hook

| ./fix-markdown.sh --check |  | exit 1  # Fail if errors remain |
```

```bash

# Auto-fix in pipeline (safe only)

./fix-markdown.sh --auto
git add .
```

## What Markdownlint Actually Does

The tool uses `npx markdownlint-cli2 --fix`, which:

1. **Reads** the `.markdownlintrc.json` configuration
2. **Identifies** all violations
3. **Applies safe fixes** (can be 100% automatic)
4. **Reports** errors that can't be auto-fixed

In ArtLomo's config:

```json
{
  "default": true,
  "MD013": false,    ← Line-length disabled (technical docs need longer lines)
  "MD033": false     ← Inline HTML disabled (allows flexibility)
}
```

## Error Categories

### Automatic Fixes (100% Safe)

| Error | What It Does | Auto-Fix Result | Risk |
| --- | --- | --- | --- |
| MD022 | Headings need blanks | Adds blank lines | None - formatting only |
| MD032 | Lists need blanks | Adds blank lines | None |
| MD031 | Code blocks need blanks | Adds blank lines | None |
| MD040 | Code blocks need language | Adds language | Low |
| MD038 | Remove spaces in backticks | Removes spaces | None |

### Manual Review Needed

| Error | Why | Fix Strategy |
| --- | --- | --- |
| MD036 | Emphasis as heading | Use heading format |
| MD024 | Duplicate headings | Make heading unique |
| MD026 | Trailing punctuation | Remove punctuation |

## Testing the Script

```bash

# Test on a specific file first

./fix-markdown.sh --check changelog-reports/README.md

# Then auto-fix

./fix-markdown.sh --auto

# Verify no critical errors remain

npx markdownlint-cli2 --version
npx markdownlint-cli2 .copilotrules changelog-reports/*.md
```

## Rollback If Something Goes Wrong

The script creates `.backup` files for semi-automatic fixes:

```bash

# Find and restore backups

find . -name "*.backup" -exec ls -lh {} \;

# Restore a file

mv filename.md.backup filename.md

# Clean up all backups

find . -name "*.backup" -delete
```

## Integration with .copilotrules

The script respects the standards defined in `/srv/artlomo/.copilotrules` (Section 13):

- All fixes align with documented Markdown Linting Standards
- Both AI assistants and the script apply the same rules
- Ensures consistency across the project

## Recommended Process

1. **Initial Setup**: Run `./fix-markdown.sh --auto` once on all files
1. **Ongoing**: Run `./fix-markdown.sh --check` before committing
1. **Pre-Commit Hook**: Add to `.git/hooks/pre-commit`:

   ```bash
   #!/bin/bash
   ./fix-markdown.sh --auto
   git add .
   ```

1. **Review**: Always do `git diff` before committing to catch unexpected changes

## Summary: Risk Assessment

| Scenario | Command | Risk | Recommendation |
| --- | --- | --- | --- |
| Quick fix | `--auto` | Very Low | ✅ Always safe |
| Fix before push | `--auto` + review | Low | ✅ Recommended |
| Auto-convert emphasis | `--all` | Medium | ⚠️ Review after |
| Check before auto-fix | `--check` | None | ✅ Always do this first |
| Production/CI/CD | `--auto` only | Low | ✅ Safe for automation |

**Bottom line:** Use `--auto` freely in development. Use `--all` + manual review for production changes.
