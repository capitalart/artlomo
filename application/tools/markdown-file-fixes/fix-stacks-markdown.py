#!/usr/bin/env python3
"""
Fix auto-fixable markdownlint issues across the project.

Supported rules:
- MD003, MD007, MD009, MD010, MD012, MD022, MD024, MD025, MD026, MD028
- MD029, MD031, MD032, MD033, MD034, MD036, MD040, MD046, MD050, MD051
- MD056, MD060

QUICK USAGE:

1) Fix all markdown files recursively from workspace root:
     python3 application/tools/markdown-file-fixes/fix-stacks-markdown.py \
         /srv/artlomo --recursive

2) Fix with all options enabled:
     python3 application/tools/markdown-file-fixes/fix-stacks-markdown.py \
         /srv/artlomo --recursive --include-archived --include-lab --include-stacks

3) Fix one file:
     python3 application/tools/markdown-file-fixes/fix-stacks-markdown.py \
         path/to/file.md

4) Fix a directory:
     python3 application/tools/markdown-file-fixes/fix-stacks-markdown.py \
         application/changelog-reports
"""

import argparse
import hashlib
import re
import sys
from collections import defaultdict
from pathlib import Path


FENCE_RE = re.compile(r"^\s*```")
ATX_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
UL_RE = re.compile(r"^(\s*)([-+*])\s+(.+)$")
OL_RE = re.compile(r"^(\s*)(\d+)\.\s+(.+)$")
LINK_FRAGMENT_RE = re.compile(r"\[([^\]]+)\]\(#([^)]+)\)")


def split_lines(content: str) -> list[str]:
    return content.split("\n")


def join_lines(lines: list[str]) -> str:
    return "\n".join(lines)


def slugify_heading(text: str) -> str:
    # Mirrors markdownlint/GFM fragment behavior closely enough for auto-fix.
    text = text.strip().lower()
    text = re.sub(r"[`*_~]", "", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"[^\w\-\s]", "", text)
    text = re.sub(r"\s+", "-", text).strip("-")
    return text


def heading_anchors(lines: list[str]) -> set[str]:
    anchors: set[str] = set()
    in_code = False
    for line in lines:
        if FENCE_RE.match(line):
            in_code = not in_code
            continue
        if in_code:
            continue
        m = ATX_RE.match(line.strip())
        if not m:
            continue
        slug = slugify_heading(m.group(2))
        if slug:
            anchors.add(slug)
    return anchors


def fix_md012_multiple_blanks(content: str) -> str:
    """Fix MD012: Collapse 3+ blank lines to a single blank line."""
    return re.sub(r'\n\n\n+', '\n\n', content)


def fix_md022_heading_blanks(content: str) -> str:
    """Fix MD022: Ensure headings have blank lines before and after."""
    lines = content.split('\n')
    fixed = []
    i = 0
    
    heading_pattern = re.compile(r'^(#{1,6})\s+')
    
    while i < len(lines):
        line = lines[i]
        is_heading = bool(heading_pattern.match(line))
        
        if is_heading:
            # Check if we need blank line BEFORE
            if fixed and fixed[-1].strip() != '':
                fixed.append('')
            
            fixed.append(line)
            
            # Check if we need blank line AFTER (look ahead)
            if i + 1 < len(lines):
                next_line = lines[i + 1]
                if next_line.strip() != '' and next_line.strip() != '---':
                    fixed.append('')
            
            i += 1
        else:
            fixed.append(line)
            i += 1
    
    return '\n'.join(fixed)


def fix_md009_trailing_spaces(content: str) -> str:
    """Fix MD009: Remove trailing spaces from lines."""
    lines = content.split('\n')
    return '\n'.join(line.rstrip() for line in lines)


def fix_md050_strong_style(content: str) -> str:
    """Fix MD050: Use asterisks for strong, not underscores."""
    lines = content.split('\n')
    fixed = []
    in_code_block = False
    
    for line in lines:
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            fixed.append(line)
            continue
        
        if in_code_block:
            fixed.append(line)
            continue
        
        if '__' in line and not line.strip().startswith('```'):
            line = re.sub(r'(?<!\w)__(\S.*?\S)__(?!\w)', r'**\1**', line)
        
        fixed.append(line)
    
    return '\n'.join(fixed)


def fix_md010_no_tabs(content: str) -> str:
    """Fix MD010: Replace hard tabs with spaces."""
    lines = content.split('\n')
    fixed = []
    for line in lines:
        fixed.append(line.replace('\t', '  '))
    return '\n'.join(fixed)


def fix_md007_ul_indent(content: str) -> str:
    """Fix MD007: Normalize unordered list indentation (top-level=0, nested=+2)."""
    lines = content.split('\n')
    fixed = []
    in_code_block = False
    ul_pattern = re.compile(r'^(\s*)([-+*])\s+(.*)$')
    list_pattern = re.compile(r'^(\s*)(?:[-+*]|\d+\.)\s+')
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('```'):
            in_code_block = not in_code_block
            fixed.append(line)
            continue
        
        if in_code_block:
            fixed.append(line)
            continue
        
        match = ul_pattern.match(line)
        if not match:
            fixed.append(line)
            continue

        marker = match.group(2)
        rest = match.group(3)

        prev_indent = None
        for prev_line in reversed(fixed):
            if prev_line.strip() == '':
                continue
            prev_match = list_pattern.match(prev_line)
            if prev_match:
                prev_indent = len(prev_match.group(1))
            break

        if prev_indent is None:
            indent = ''
        else:
            curr_indent = len(match.group(1))
            if curr_indent > prev_indent:
                indent = ' ' * (prev_indent + 2)
            else:
                indent = ' ' * prev_indent

        fixed.append(f"{indent}{marker} {rest}")
    
    return '\n'.join(fixed)


def fix_md028_no_blanks_in_blockquote(content: str) -> str:
    """Fix MD028: Replace blank lines inside blockquotes with '>' marker lines."""
    lines = content.split('\n')
    fixed = []
    in_code_block = False
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        if stripped.startswith('```'):
            in_code_block = not in_code_block
            fixed.append(line)
            continue
        
        if in_code_block:
            fixed.append(line)
            continue
        
        if stripped != '':
            fixed.append(line)
            continue
        
        prev_is_quote = bool(fixed and fixed[-1].lstrip().startswith('>'))
        next_is_quote = False
        if i + 1 < len(lines):
            next_is_quote = lines[i + 1].lstrip().startswith('>')
        
        if prev_is_quote and next_is_quote:
            fixed.append('>')
        else:
            fixed.append(line)
    
    return '\n'.join(fixed)


def fix_md040_fenced_code_language(content: str) -> str:
    """Fix MD040: Add default language to unlabeled fenced code blocks."""
    lines = content.split('\n')
    fixed = []
    in_code_block = False
    
    for line in lines:
        stripped = line.strip()
        if not stripped.startswith('```'):
            fixed.append(line)
            continue
        
        if not in_code_block:
            if stripped == '```':
                indent = line[:len(line) - len(line.lstrip())]
                fixed.append(f"{indent}```text")
            else:
                fixed.append(line)
            in_code_block = True
        else:
            fixed.append(line)
            in_code_block = False
    
    return '\n'.join(fixed)


def fix_md060_table_column_style(content: str) -> str:
    """Fix MD060: Normalize markdown table rows to consistent spacing."""
    lines = content.split('\n')
    fixed = []
    
    for line in lines:
        stripped = line.strip()
        
        if stripped.count('|') < 2:
            fixed.append(line)
            continue
        
        leading_ws = line[:len(line) - len(line.lstrip())]
        has_outer_pipes = stripped.startswith('|') and stripped.endswith('|')
        if has_outer_pipes:
            raw_cells = stripped.split('|')[1:-1]
        else:
            raw_cells = stripped.split('|')
        
        cells = [cell.strip() for cell in raw_cells]
        fixed.append(f"{leading_ws}| {' | '.join(cells)} |")
    
    return '\n'.join(fixed)


def fix_md025_single_h1(content: str) -> str:
    """Fix MD025: Demote additional H1 headings to H2 headings."""
    lines = content.split('\n')
    fixed = []
    in_code_block = False
    seen_h1 = False
    
    has_frontmatter_title = False
    if len(lines) >= 3 and lines[0].strip() == '---':
        i = 1
        while i < len(lines) and lines[i].strip() != '---':
            if lines[i].lower().startswith('title:'):
                has_frontmatter_title = True
            i += 1
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('```'):
            in_code_block = not in_code_block
            fixed.append(line)
            continue
        
        if in_code_block:
            fixed.append(line)
            continue
        
        if re.match(r'^#\s+\S+', stripped):
            if has_frontmatter_title and not seen_h1:
                fixed.append(line.replace('# ', '## ', 1))
                seen_h1 = True
                continue
            if seen_h1:
                fixed.append(line.replace('# ', '## ', 1))
            else:
                fixed.append(line)
                seen_h1 = True
            continue
        
        fixed.append(line)
    
    return '\n'.join(fixed)


def fix_md029_ordered_list_prefix(content: str) -> str:
    """Fix MD029: Normalize ordered list prefixes to 1/2/3 style by block."""
    lines = content.split('\n')
    fixed = []
    in_code_block = False
    ol_pattern = re.compile(r'^(\s*)(\d+)\.\s+(.*)$')
    
    current_indent = None
    expected = 1
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('```'):
            in_code_block = not in_code_block
            fixed.append(line)
            current_indent = None
            expected = 1
            continue
        
        if in_code_block:
            fixed.append(line)
            continue
        
        match = ol_pattern.match(line)
        if not match:
            fixed.append(line)
            if stripped == '':
                current_indent = None
                expected = 1
            continue
        
        indent, _, rest = match.groups()
        indent_len = len(indent)
        if current_indent is None or indent_len != current_indent:
            current_indent = indent_len
            expected = 1
        
        fixed.append(f"{indent}{expected}. {rest}")
        expected += 1
    
    return '\n'.join(fixed)


def fix_md032_blanks_around_lists(content: str) -> str:
    """Fix MD032: Ensure blank lines around list blocks."""
    lines = content.split('\n')
    fixed = []
    in_code_block = False
    list_pattern = re.compile(r'^\s*(?:[-+*]|\d+\.)\s+')
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        if stripped.startswith('```'):
            in_code_block = not in_code_block
            fixed.append(line)
            continue
        
        if in_code_block:
            fixed.append(line)
            continue
        
        is_list = bool(list_pattern.match(line))
        if is_list:
            if fixed and fixed[-1].strip() != '':
                fixed.append('')
            fixed.append(line)
            
            next_is_list = False
            if i + 1 < len(lines):
                next_is_list = bool(list_pattern.match(lines[i + 1]))
            if not next_is_list and i + 1 < len(lines) and lines[i + 1].strip() != '':
                fixed.append('')
            continue
        
        fixed.append(line)
    
    return '\n'.join(fixed)


def fix_md056_table_column_count(content: str) -> str:
    """Fix MD056: Normalize table row column count to header width."""
    lines = content.split('\n')
    fixed = []
    in_code_block = False
    
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        if stripped.startswith('```'):
            in_code_block = not in_code_block
            fixed.append(line)
            i += 1
            continue
        
        if in_code_block:
            fixed.append(line)
            i += 1
            continue
        
        if i + 1 < len(lines):
            header = lines[i].strip()
            delim = lines[i + 1].strip()
            if header.count('|') >= 2 and re.match(r'^\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?$', delim):
                header_cells = [c.strip() for c in header.strip('|').split('|')]
                expected = len(header_cells)
                
                fixed.append('| ' + ' | '.join(header_cells) + ' |')
                fixed.append('| ' + ' | '.join([c.strip() for c in delim.strip('|').split('|')]) + ' |')
                i += 2
                
                while i < len(lines):
                    row = lines[i]
                    row_strip = row.strip()
                    if row_strip == '' or row_strip.count('|') < 2:
                        break
                    
                    cells = [c.strip() for c in row_strip.strip('|').split('|')]
                    if len(cells) > expected:
                        head = cells[: expected - 1]
                        tail = ' | '.join(cells[expected - 1 :])
                        cells = head + [tail]
                    elif len(cells) < expected:
                        cells.extend([''] * (expected - len(cells)))
                    
                    fixed.append('| ' + ' | '.join(cells) + ' |')
                    i += 1
                continue
        
        fixed.append(line)
        i += 1
    
    return '\n'.join(fixed)


def fix_md031_blanks_around_fences(content: str) -> str:
    """Fix MD031: Ensure fenced code blocks have blank lines above and below."""
    lines = content.split('\n')
    fixed: list[str] = []
    in_code = False

    for idx, line in enumerate(lines):
        stripped = line.strip()
        is_fence = stripped.startswith('```')

        if is_fence and not in_code:
            if fixed and fixed[-1].strip() != '':
                fixed.append('')
            fixed.append(line)
            in_code = True
            continue

        if is_fence and in_code:
            fixed.append(line)
            in_code = False
            if idx + 1 < len(lines) and lines[idx + 1].strip() != '':
                fixed.append('')
            continue

        fixed.append(line)

    return '\n'.join(fixed)


def fix_md036_no_emphasis_as_heading(content: str) -> str:
    """Fix MD036: Convert emphasis-only lines to proper headings."""
    lines = content.split('\n')
    fixed = []
    
    in_code_block = False

    for line in lines:
        stripped = line.strip()

        if stripped.startswith('```'):
            in_code_block = not in_code_block
            fixed.append(line)
            continue

        if in_code_block:
            fixed.append(line)
            continue
        
        # Check for **text** or *text* at start of line (potential heading)
        strong_match = re.match(r'^\*\*([^*]+)\*\*$', stripped)
        if strong_match:
            # This is emphasis used as heading - convert to H2
            text = strong_match.group(1)
            fixed.append(f'## {text}')
            continue
        
        em_match = re.match(r'^\*([^*]+)\*$', stripped)
        if em_match and not line.startswith(' '):  # Not indented code
            text = em_match.group(1)
            # Only convert if it looks like a heading (short, no sentences)
            if len(text) < 80 and not text.endswith('.'):
                fixed.append(f'## {text}')
                continue
        
        fixed.append(line)
    
    return '\n'.join(fixed)


def fix_md034_no_bare_urls(content: str) -> str:
    """Fix MD034: Wrap bare URLs in angle brackets or markdown links."""
    lines = content.split('\n')
    fixed = []
    in_code_block = False
    
    # URL pattern - matches http/https URLs not already in markdown or angle brackets
    url_pattern = re.compile(
        r'(?<![(<\[\]])'  # Not preceded by (<[
        r'(https?://[^\s<>\]]+)'  # Capture the URL
        r'(?![)\]>])'  # Not followed by )}>
    )
    
    for line in lines:
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            fixed.append(line)
            continue
        
        if in_code_block:
            fixed.append(line)
            continue
        
        # Replace bare URLs with angle-bracket wrapped URLs
        line = url_pattern.sub(r'<\1>', line)
        fixed.append(line)
    
    return '\n'.join(fixed)


def fix_md024_no_duplicate_heading(content: str) -> str:
    """Fix MD024: Handle duplicate headings by adding context or renaming."""
    lines = content.split('\n')
    fixed = []
    heading_counts = defaultdict(int)
    in_code_block = False
    
    heading_pattern = re.compile(r'^(#{1,6})\s+(.+)$')
    
    for line in lines:
        stripped = line.strip()
        
        if stripped.startswith('```'):
            in_code_block = not in_code_block
            fixed.append(line)
            continue
        
        if in_code_block:
            fixed.append(line)
            continue
        
        match = heading_pattern.match(stripped)
        if not match:
            fixed.append(line)
            continue
        
        level = match.group(1)
        text = match.group(2)
        
        # Track heading occurrences
        heading_counts[text] += 1
        count = heading_counts[text]
        
        # If duplicate, add counter
        if count > 1:
            # Find trailing parentheses or append
            if text.endswith(')'):
                # Replace existing number if it's just (N)
                text_base = re.sub(r'\s*\(\d+\)$', '', text)
                new_text = f'{text_base} ({count})'
            else:
                new_text = f'{text} ({count})'
            
            fixed.append(f'{level} {new_text}')
        else:
            fixed.append(line)
    
    return '\n'.join(fixed)


def fix_md003_setext_to_atx(content: str) -> str:
    """Fix MD003: Convert setext headings to ATX headings."""
    lines = split_lines(content)
    fixed: list[str] = []
    in_code = False
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if FENCE_RE.match(line):
            in_code = not in_code
            fixed.append(line)
            i += 1
            continue

        if in_code or i + 1 >= len(lines):
            fixed.append(line)
            i += 1
            continue

        underline = lines[i + 1].strip()
        if stripped and re.match(r'^=+$', underline):
            fixed.append(f"# {stripped}")
            i += 2
            continue
        if stripped and re.match(r'^-+$', underline):
            fixed.append(f"## {stripped}")
            i += 2
            continue

        fixed.append(line)
        i += 1

    return join_lines(fixed)


def fix_md026_trailing_punctuation_in_heading(content: str) -> str:
    """Fix MD026: Remove trailing punctuation from heading text."""
    lines = split_lines(content)
    fixed: list[str] = []
    in_code = False

    for line in lines:
        stripped = line.strip()
        if FENCE_RE.match(line):
            in_code = not in_code
            fixed.append(line)
            continue
        if in_code:
            fixed.append(line)
            continue

        m = ATX_RE.match(stripped)
        if not m:
            fixed.append(line)
            continue

        level, text = m.groups()
        text = re.sub(r'[\.:;!?]+$', '', text.strip())
        fixed.append(f"{level} {text}")

    return join_lines(fixed)


def fix_md033_inline_html(content: str) -> str:
    """Fix MD033: Wrap inline HTML tags in backticks when used as literal text."""
    lines = split_lines(content)
    fixed: list[str] = []
    in_code = False

    tag_re = re.compile(r'(<\/?[A-Za-z][^>]*>)')

    for line in lines:
        stripped = line.strip()
        if FENCE_RE.match(line):
            in_code = not in_code
            fixed.append(line)
            continue
        if in_code:
            fixed.append(line)
            continue

        if '<http' in line or '<https' in line:
            fixed.append(line)
            continue

        fixed.append(tag_re.sub(r'`\1`', line))

    return join_lines(fixed)


def fix_md046_indented_code_blocks(content: str) -> str:
    """Fix MD046: Convert indented code blocks into fenced blocks."""
    lines = split_lines(content)
    fixed: list[str] = []
    in_code = False
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if FENCE_RE.match(line):
            in_code = not in_code
            fixed.append(line)
            i += 1
            continue

        if in_code:
            fixed.append(line)
            i += 1
            continue

        if re.match(r'^( {4}|\t)\S', line):
            block: list[str] = []
            j = i
            while j < len(lines):
                curr = lines[j]
                if curr.strip() == '':
                    block.append('')
                    j += 1
                    continue
                if re.match(r'^( {4}|\t)', curr):
                    block.append(re.sub(r'^( {4}|\t)', '', curr, count=1))
                    j += 1
                    continue
                break

            fixed.append('```text')
            fixed.extend(block)
            fixed.append('```')
            i = j
            continue

        fixed.append(line)
        i += 1

    return join_lines(fixed)


def fix_md051_link_fragments(content: str) -> str:
    """Fix MD051: Remove broken local fragment links by keeping link text."""
    lines = split_lines(content)
    anchors = heading_anchors(lines)
    fixed: list[str] = []
    in_code = False

    for line in lines:
        stripped = line.strip()
        if FENCE_RE.match(line):
            in_code = not in_code
            fixed.append(line)
            continue
        if in_code:
            fixed.append(line)
            continue

        def repl(match: re.Match[str]) -> str:
            text = match.group(1)
            frag = match.group(2)
            if frag in anchors:
                return match.group(0)
            return text

        fixed.append(LINK_FRAGMENT_RE.sub(repl, line))

    return join_lines(fixed)


def compress_duplicate_tail(content: str) -> str:
    """Collapse pathological repeated tail blocks caused by previous bad runs."""
    lines = split_lines(content)
    if len(lines) < 2000:
        return content

    # Detect if the final 40-line chunk repeats many times.
    chunk_size = 40
    tail = lines[-chunk_size:]
    if not tail:
        return content

    repeats = 0
    idx = len(lines) - chunk_size
    while idx - chunk_size >= 0 and lines[idx - chunk_size:idx] == tail:
        repeats += 1
        idx -= chunk_size

    if repeats < 5:
        return content

    # Keep a single copy of the repeated tail sequence.
    return join_lines(lines[:idx] + tail)


def apply_all_fixes_once(content: str) -> str:
    """Apply all transforms once in stable order."""
    content = compress_duplicate_tail(content)
    content = fix_md010_no_tabs(content)
    content = fix_md009_trailing_spaces(content)
    content = fix_md003_setext_to_atx(content)
    content = fix_md026_trailing_punctuation_in_heading(content)
    content = fix_md034_no_bare_urls(content)
    content = fix_md036_no_emphasis_as_heading(content)
    content = fix_md024_no_duplicate_heading(content)
    content = fix_md031_blanks_around_fences(content)
    content = fix_md046_indented_code_blocks(content)
    content = fix_md007_ul_indent(content)
    content = fix_md029_ordered_list_prefix(content)
    content = fix_md032_blanks_around_lists(content)
    content = fix_md012_multiple_blanks(content)
    content = fix_md022_heading_blanks(content)
    content = fix_md028_no_blanks_in_blockquote(content)
    content = fix_md040_fenced_code_language(content)
    content = fix_md056_table_column_count(content)
    content = fix_md060_table_column_style(content)
    content = fix_md025_single_h1(content)
    content = fix_md050_strong_style(content)
    content = fix_md033_inline_html(content)
    content = fix_md051_link_fragments(content)
    return content


def fix_file(filepath: Path) -> bool:
    """Fix a markdown file. Return True if modifications were made."""
    try:
        content = filepath.read_text(encoding='utf-8')
        original = content

        # Converge in bounded passes to avoid transform ordering oscillation.
        seen_hashes: set[str] = set()
        for _ in range(5):
            digest = hashlib.sha1(content.encode('utf-8')).hexdigest()
            if digest in seen_hashes:
                break
            seen_hashes.add(digest)

            updated = apply_all_fixes_once(content)
            if updated == content:
                break
            content = updated
        
        # Only write if changed
        if content != original:
            filepath.write_text(content, encoding='utf-8')
            return True
        return False
    
    except Exception as e:
        print(f"Error processing {filepath}: {e}", file=sys.stderr)
        return False


def collect_markdown_files(
    path: Path,
    recursive: bool,
    include_archived: bool,
    include_lab: bool,
    include_stacks: bool,
) -> list[Path]:
    """Collect markdown files from file or directory path."""
    if path.is_file():
        if path.suffix.lower() != '.md':
            print(f"Error: {path} is not a markdown file", file=sys.stderr)
            sys.exit(1)
        return [path]
    
    if not path.is_dir():
        print(f"Error: {path} not found", file=sys.stderr)
        sys.exit(1)
    
    if not recursive:
        return sorted(path.glob('*.md'))
    
    excluded_dirs = {
        '.git',
        '.venv',
        '.pytest_cache',
        '__pycache__',
        'node_modules',
        'outputs',
        'logs',
        '.windsurf',
    }
    
    excluded_fragments = {
        '/var/security-runs/',
    }
    if not include_lab:
        excluded_fragments.update({
            '/application/lab/',
            '/lab/',
        })
    if not include_archived:
        excluded_fragments.add('/application/archived/')
    if not include_stacks:
        excluded_fragments.update({
            '/application/tools/app-stacks/stacks/',
            '/application/tools/app-stacks/backups/',
        })
    
    files = []
    for md_file in path.rglob('*.md'):
        if any(part in excluded_dirs for part in md_file.parts):
            continue
        md_file_posix = md_file.as_posix()
        if any(fragment in md_file_posix for fragment in excluded_fragments):
            continue
        files.append(md_file)
    return sorted(files)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Fix auto-fixable markdownlint issues.'
    )
    parser.add_argument(
        'path',
        nargs='?',
        default='.',
        help='Markdown file or directory to process (default: current directory).',
    )
    parser.add_argument(
        '--recursive',
        action='store_true',
        help='Scan directories recursively for all .md files.',
    )
    parser.add_argument(
        '--include-archived',
        action='store_true',
        help='Include application/archived markdown files in recursive mode.',
    )
    parser.add_argument(
        '--include-lab',
        action='store_true',
        help='Include lab markdown files in recursive mode.',
    )
    parser.add_argument(
        '--include-stacks',
        action='store_true',
        help='Include app-stacks generated markdown files in recursive mode.',
    )
    return parser.parse_args()


def main():
    args = parse_args()
    path = Path(args.path)
    files = collect_markdown_files(
        path,
        recursive=args.recursive,
        include_archived=args.include_archived,
        include_lab=args.include_lab,
        include_stacks=args.include_stacks,
    )
    
    if not files:
        print(f"No markdown files found in: {path}")
        return
    
    fixed_count = 0
    for filepath in files:
        if fix_file(filepath):
            print(f"✓ Fixed: {filepath}")
            fixed_count += 1
        else:
            print(f"  Checked: {filepath}")
    
    print(f"\nFixed {fixed_count}/{len(files)} file(s)")


if __name__ == '__main__':
    main()
