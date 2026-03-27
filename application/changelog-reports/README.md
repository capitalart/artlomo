# Changelog Reports Directory

This directory contains all ArtLomo status reports, deployment checklists, and project completion documentation.

## Files Organization

### Reports

- **DEPLOYMENT_CHECKLIST.md** - Pre and post-deployment verification checklist

- **QUICK_REFERENCE.md** - One-page quick reference guide

- **STAGE_C_COMPLETION_REPORT.md** - Executive summary of Stage C completion

- **STAGE_C_FINAL_SUMMARY.md** - Comprehensive technical summary

- **STAGE_C_INDEX.md** - Complete index of all changes and implementations

- **STAGE_C_PERSISTENCE_COMPLETE.md** - Technical deep-dive into persistence layer

- **COVER_MODE_IMPLEMENTATION.md** - Cover mode implementation details

## Markdown Standards

All files in this directory must follow the Markdown Linting Standards defined in `/srv/artlomo/.copilotrules` (Section 13).

### Key Standards

- ✅ MD022: Blank lines around headings (1 before, 1 after)

- ✅ MD032: Blank lines around lists (1 before, 1 after)

- ✅ MD031: Blank lines around code blocks (1 before, 1 after)

- ✅ MD040: Language specified for all fenced code blocks

- ✅ MD060: Proper spacing in markdown tables (spaces around pipes)

- ✅ MD024: No duplicate headings in same file

- ✅ MD026: No trailing punctuation in headings

- ✅ MD029: Sequential numbering for ordered lists

- ✅ MD009: No trailing spaces at end of lines

## Linting Configuration

A `.markdownlintrc.json` file exists in the root `/srv/artlomo/` directory to configure markdown linting rules.

### Auto-Fixing Errors

To automatically fix markdown linting errors:

```bash
cd /srv/artlomo/changelog-reports
npx markdownlint-cli2 --fix *.md
```

### Checking Without Fixing

To check for linting errors without modifying files:

```bash
cd /srv/artlomo/changelog-reports
npx markdownlint-cli2 *.md
```

## Best Practices

When creating or editing markdown files in this directory:

1. **Always add blank lines after headings** - No content immediately after `##`

1. **Always add blank lines around lists** - Content, list, content pattern

1. **Always add blank lines around code blocks** - Both before and after ```

1. **Always specify code block language** - `\`\`\`python` not just `\`\`\``

| 5. **Keep table formatting clean** - ` | text | text | text | ` with spaces |

1. **Use sequential numbering** - `1.`, `2.`, `3.` for ordered lists

1. **Remove trailing spaces** - Check at end of every line

## Copilot Guidelines

Refer to `/srv/artlomo/.copilotrules` Section 13 for complete Markdown Linting Standards that must be followed when generating or editing ANY markdown file in this project.

---

**Last Updated:** February 23, 2026
