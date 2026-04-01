#!/usr/bin/env python3
"""
Merge a main HTML file and its linked local JS/CSS files into a single text file.

Output format:

#### FILE: relative/path/to/index.html ####
<file content>

#### FILE: relative/path/to/style.css ####
<file content>

#### FILE: relative/path/to/app.js ####
<file content>

The script:
- reads the main HTML file
- finds linked local CSS files from <link rel="stylesheet" href="...">
- finds linked local JS files from <script src="..."></script>
- follows CSS @import rules recursively
- ignores remote URLs such as http://, https://, //, data:, mailto:, javascript:
- avoids duplicate files
- writes everything into one text file

Usage:
    python merge_web_files.py index.html
    python merge_web_files.py index.html -o merged_project.txt
    python merge_web_files.py path/to/index.html --root path/to/project
"""

from __future__ import annotations

import argparse
import html.parser
import os
import re
import sys
from pathlib import Path
from typing import Iterable


REMOTE_PREFIXES = (
    "http://",
    "https://",
    "//",
    "data:",
    "mailto:",
    "javascript:",
    "#",
)


class HtmlDependencyParser(html.parser.HTMLParser):
    """
    Parse an HTML file and collect local CSS and JS dependencies.

    Collected:
    - <link rel="stylesheet" href="...">
    - <script src="..."></script>
    """

    def __init__(self) -> None:
        super().__init__()
        self.css_files: list[str] = []
        self.js_files: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        """
        Process HTML start tags and extract relevant local file references.
        """
        attr_map = {key.lower(): value for key, value in attrs if key}

        if tag.lower() == "link":
            rel_value = (attr_map.get("rel") or "").lower()
            href_value = attr_map.get("href") or ""
            if "stylesheet" in rel_value and href_value:
                self.css_files.append(href_value)

        elif tag.lower() == "script":
            src_value = attr_map.get("src") or ""
            if src_value:
                self.js_files.append(src_value)


def is_remote_reference(reference: str) -> bool:
    """
    Return True if the reference points to a remote or non-file resource.
    """
    stripped = reference.strip().lower()
    return stripped.startswith(REMOTE_PREFIXES)


def strip_url_fragment_and_query(reference: str) -> str:
    """
    Remove query string and fragment from a URL-like path.

    Example:
        app.js?v=1#main -> app.js
    """
    return reference.split("#", 1)[0].split("?", 1)[0].strip()


def read_text_file(file_path: Path) -> str:
    """
    Read a text file using UTF-8 first, then fall back to common Windows encodings.
    """
    for encoding in ("utf-8", "utf-8-sig", "cp1252", "latin-1"):
        try:
            return file_path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue

    return file_path.read_text(encoding="utf-8", errors="replace")


def resolve_local_reference(base_file: Path, reference: str, project_root: Path) -> Path | None:
    """
    Resolve a local file reference relative to the current file.

    Returns None for remote references or empty values.
    """
    if not reference:
        return None

    cleaned_reference = strip_url_fragment_and_query(reference)
    if not cleaned_reference or is_remote_reference(cleaned_reference):
        return None

    candidate = (base_file.parent / cleaned_reference).resolve()

    try:
        candidate.relative_to(project_root.resolve())
    except ValueError:
        # The path points outside the selected project root.
        # Still allow it if the file exists, because some projects use ../ references.
        pass

    return candidate


def extract_css_imports(css_text: str) -> list[str]:
    """
    Extract file paths from CSS @import statements.

    Supported forms:
        @import "file.css";
        @import 'file.css';
        @import url("file.css");
        @import url('file.css');
        @import url(file.css);
    """
    imports: list[str] = []

    patterns = [
        re.compile(r"""@import\s+["']([^"']+)["']""", re.IGNORECASE),
        re.compile(r"""@import\s+url\(\s*["']?([^"')]+)["']?\s*\)""", re.IGNORECASE),
    ]

    for pattern in patterns:
        for match in pattern.finditer(css_text):
            import_path = match.group(1).strip()
            if import_path:
                imports.append(import_path)

    return imports


def parse_html_dependencies(html_file: Path) -> tuple[list[str], list[str]]:
    """
    Parse a local HTML file and return linked CSS and JS references.
    """
    parser = HtmlDependencyParser()
    parser.feed(read_text_file(html_file))
    return parser.css_files, parser.js_files


def normalize_output_name(file_path: Path, project_root: Path) -> str:
    """
    Return a clean display path for the merged output header.
    """
    try:
        return file_path.resolve().relative_to(project_root.resolve()).as_posix()
    except ValueError:
        return file_path.resolve().as_posix()


def collect_files_from_html(entry_html: Path, project_root: Path) -> list[Path]:
    """
    Collect the main HTML file and all linked local CSS/JS files.

    CSS imports are followed recursively.
    Duplicate files are removed while preserving discovery order.
    """
    discovered_files: list[Path] = []
    visited_files: set[Path] = set()
    queued_css: list[Path] = []

    def add_file(file_path: Path) -> None:
        """
        Add a file once, if it exists.
        """
        resolved_path = file_path.resolve()
        if resolved_path in visited_files:
            return
        if not resolved_path.exists():
            print(f"Warning: file not found: {resolved_path}", file=sys.stderr)
            return
        if resolved_path.is_dir():
            print(f"Warning: expected file, got directory: {resolved_path}", file=sys.stderr)
            return

        visited_files.add(resolved_path)
        discovered_files.append(resolved_path)

    add_file(entry_html)

    css_refs, js_refs = parse_html_dependencies(entry_html)

    for css_ref in css_refs:
        resolved_css = resolve_local_reference(entry_html, css_ref, project_root)
        if resolved_css is not None:
            add_file(resolved_css)
            if resolved_css.exists():
                queued_css.append(resolved_css)

    for js_ref in js_refs:
        resolved_js = resolve_local_reference(entry_html, js_ref, project_root)
        if resolved_js is not None:
            add_file(resolved_js)

    processed_css: set[Path] = set()

    while queued_css:
        current_css = queued_css.pop(0).resolve()
        if current_css in processed_css:
            continue
        processed_css.add(current_css)

        css_text = read_text_file(current_css)
        import_refs = extract_css_imports(css_text)

        for import_ref in import_refs:
            resolved_import = resolve_local_reference(current_css, import_ref, project_root)
            if resolved_import is None:
                continue

            already_known = resolved_import.resolve() in visited_files
            add_file(resolved_import)

            if resolved_import.exists() and not already_known:
                queued_css.append(resolved_import)

    return discovered_files


def merge_files_to_text(file_paths: Iterable[Path], project_root: Path) -> str:
    """
    Build the merged text output for all collected files.
    """
    sections: list[str] = []

    for file_path in file_paths:
        display_name = normalize_output_name(file_path, project_root)
        file_content = read_text_file(file_path)

        sections.append(f"#### FILE: {display_name} ####\n{file_content.rstrip()}\n")

    return "\n".join(sections).rstrip() + "\n"


def build_default_output_path(entry_html: Path) -> Path:
    """
    Create a default output file path next to the entry HTML file.
    """
    return entry_html.with_name(f"{entry_html.stem}_merged.txt")


def parse_arguments() -> argparse.Namespace:
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Merge an HTML file and its linked local JS/CSS files into one text file."
    )
    parser.add_argument(
        "html_file",
        help="Path to the main HTML file."
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Path to the output text file. Default: <html_stem>_merged.txt"
    )
    parser.add_argument(
        "--root",
        help="Project root used for nicer relative file names in output. Default: directory of the HTML file."
    )
    return parser.parse_args()


def main() -> int:
    """
    Run the CLI program.
    """
    args = parse_arguments()

    entry_html = Path(args.html_file).resolve()
    if not entry_html.exists():
        print(f"Error: HTML file does not exist: {entry_html}", file=sys.stderr)
        return 1

    if not entry_html.is_file():
        print(f"Error: HTML path is not a file: {entry_html}", file=sys.stderr)
        return 1

    project_root = Path(args.root).resolve() if args.root else entry_html.parent.resolve()
    output_path = Path(args.output).resolve() if args.output else build_default_output_path(entry_html).resolve()

    collected_files = collect_files_from_html(entry_html, project_root)
    merged_text = merge_files_to_text(collected_files, project_root)

    output_path.write_text(merged_text, encoding="utf-8")

    print(f"Merged {len(collected_files)} file(s) into: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())