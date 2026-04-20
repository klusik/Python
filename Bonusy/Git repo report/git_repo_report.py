#!/usr/bin/env python3
"""Generate a human-readable Markdown report for the current Git repository."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass
class CommitSummary:
    commit_hash: str
    author_date: str
    subject: str


class GitCommandError(RuntimeError):
    """Raised when a git command fails."""


def run_git(args: list[str], cwd: Path, check: bool = True) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if check and result.returncode != 0:
        stderr = result.stderr.strip() or "unknown git error"
        raise GitCommandError(f"git {' '.join(args)} failed: {stderr}")
    return result.stdout.strip()


def run_git_lines(args: list[str], cwd: Path, check: bool = True) -> list[str]:
    output = run_git(args, cwd=cwd, check=check)
    return [line for line in output.splitlines() if line.strip()]


def safe_git(args: list[str], cwd: Path) -> str | None:
    try:
        return run_git(args, cwd=cwd, check=True)
    except GitCommandError:
        return None


def safe_git_lines(args: list[str], cwd: Path) -> list[str]:
    try:
        return run_git_lines(args, cwd=cwd, check=True)
    except GitCommandError:
        return []


def parse_commit_lines(lines: Iterable[str]) -> list[CommitSummary]:
    commits: list[CommitSummary] = []
    for line in lines:
        parts = line.split("\x1f", 2)
        if len(parts) != 3:
            continue
        commits.append(CommitSummary(*parts))
    return commits


def try_int(value: str | None) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except ValueError:
        return None


def pluralize(count: int, singular: str, plural: str | None = None) -> str:
    return singular if count == 1 else (plural or f"{singular}s")


def detect_default_branch(repo_root: Path) -> str | None:
    symbolic = safe_git(["symbolic-ref", "refs/remotes/origin/HEAD"], repo_root)
    if symbolic:
        return symbolic.rsplit("/", 1)[-1]

    for candidate in ("master", "main"):
        ref = safe_git(["rev-parse", "--verify", candidate], repo_root)
        if ref:
            return candidate
    return None


def get_branch_status(repo_root: Path) -> tuple[str | None, int | None, int | None]:
    branch = safe_git(["branch", "--show-current"], repo_root)
    if not branch:
        return None, None, None

    upstream = safe_git(["rev-parse", "--abbrev-ref", f"{branch}@{{upstream}}"], repo_root)
    if not upstream:
        return branch, None, None

    counts = safe_git(["rev-list", "--left-right", "--count", f"{branch}...{upstream}"], repo_root)
    if not counts:
        return branch, None, None

    behind_ahead = counts.split()
    if len(behind_ahead) != 2:
        return branch, None, None

    ahead = try_int(behind_ahead[0])
    behind = try_int(behind_ahead[1])
    return branch, ahead, behind


def format_top_authors(lines: list[str], limit: int = 5) -> list[str]:
    authors: list[str] = []
    for line in lines[:limit]:
        if "\t" not in line:
            continue
        count_text, name = line.split("\t", 1)
        count = try_int(count_text.strip()) or 0
        authors.append(f"- {name.strip()}: {count} {pluralize(count, 'commit')}")
    return authors


def collect_year_counts(repo_root: Path) -> Counter[str]:
    lines = safe_git_lines(["log", "--date=format:%Y", "--pretty=format:%ad", "--all"], repo_root)
    return Counter(lines)


def collect_month_counts(repo_root: Path) -> Counter[str]:
    lines = safe_git_lines(["log", "--date=format:%Y-%m", "--pretty=format:%ad", "--all"], repo_root)
    return Counter(lines)


def collect_commits(repo_root: Path, args: list[str]) -> list[CommitSummary]:
    lines = safe_git_lines(
        ["log", "--date=short", "--pretty=format:%H\x1f%ad\x1f%s", *args],
        repo_root,
    )
    return parse_commit_lines(lines)


def get_pathspec(repo_root: Path, start_path: Path) -> str | None:
    relative = os.path.relpath(start_path, repo_root)
    if relative == ".":
        return None
    return relative


def format_commit(commit: CommitSummary) -> str:
    short_hash = commit.commit_hash[:7]
    return f"`{commit.author_date}` `{short_hash}` {commit.subject}"


def build_report(target_path: Path) -> str:
    repo_root_text = safe_git(["rev-parse", "--show-toplevel"], target_path)
    if not repo_root_text:
        raise GitCommandError("Not inside a Git repository.")

    repo_root = Path(repo_root_text)
    current_path = target_path.resolve()
    pathspec = get_pathspec(repo_root, current_path)
    repo_name = repo_root.name
    branch, ahead, behind = get_branch_status(repo_root)
    default_branch = detect_default_branch(repo_root)
    total_commits = try_int(safe_git(["rev-list", "--count", "--all"], repo_root)) or 0
    status_porcelain = safe_git(["status", "--porcelain"], repo_root) or ""
    worktree_clean = not status_porcelain.strip()

    recent_commits = collect_commits(repo_root, ["--all", "-n", "12"])
    year_counts = collect_year_counts(repo_root)
    month_counts = collect_month_counts(repo_root)
    author_lines = safe_git_lines(["shortlog", "-sne", "--all"], repo_root)
    tag_lines = safe_git_lines(
        ["for-each-ref", "--sort=creatordate", "--format=%(creatordate:short) %(refname:short)", "refs/tags"],
        repo_root,
    )

    local_branches = safe_git_lines(["for-each-ref", "--format=%(refname:short)", "refs/heads"], repo_root)
    remote_branches = safe_git_lines(["for-each-ref", "--format=%(refname:short)", "refs/remotes"], repo_root)

    path_commits: list[CommitSummary] = []
    if pathspec:
        path_commits = collect_commits(repo_root, ["--follow", "--", pathspec])

    lines: list[str] = []
    lines.append(f"# Git Repository Report: {repo_name}")
    lines.append("")
    lines.append("## Overview")
    lines.append(f"- Repository root: `{repo_root}`")
    lines.append(f"- Analyzed path: `{current_path}`")
    if branch:
        lines.append(f"- Current branch: `{branch}`")
    if default_branch:
        lines.append(f"- Default branch guess: `{default_branch}`")
    lines.append(f"- Worktree status: {'clean' if worktree_clean else 'has uncommitted changes'}")
    lines.append(f"- Total commits across all refs: `{total_commits}`")
    lines.append(f"- Local branches: `{len(local_branches)}`")
    lines.append(f"- Remote refs: `{len(remote_branches)}`")
    lines.append(f"- Tags: `{len(tag_lines)}`")

    if branch and ahead is not None and behind is not None:
        lines.append(f"- Upstream divergence: ahead `{ahead}`, behind `{behind}`")

    if default_branch and branch and branch != default_branch:
        counts = safe_git(["rev-list", "--left-right", "--count", f"{branch}...{default_branch}"], repo_root)
        if counts:
            left, right = counts.split()
            lines.append(f"- Divergence vs `{default_branch}`: branch-only `{left}`, default-only `{right}`")

    lines.append("")
    lines.append("## Findings")
    if pathspec:
        lines.append(f"- This is a broader repository; the current working directory is the subpath `{pathspec}`.")
    else:
        lines.append("- The current working directory is the repository root.")

    if worktree_clean:
        lines.append("- The worktree is clean, so the report reflects committed history only.")
    else:
        lines.append("- There are uncommitted changes, so the repo state is ahead of the last commit history.")

    if recent_commits:
        latest = recent_commits[0]
        lines.append(f"- The latest visible commit is {format_commit(latest)}.")

    if path_commits:
        first_path_commit = path_commits[-1]
        latest_path_commit = path_commits[0]
        lines.append(
            f"- The current subpath has `{len(path_commits)}` {pluralize(len(path_commits), 'commit')} in history, "
            f"from {format_commit(first_path_commit)} to {format_commit(latest_path_commit)}."
        )
    elif pathspec:
        lines.append("- No path-specific commit history could be resolved for the current subpath.")

    if year_counts:
        busiest_year, busiest_count = max(year_counts.items(), key=lambda item: item[1])
        lines.append(f"- The busiest year was `{busiest_year}` with `{busiest_count}` commits.")

    lines.append("")
    lines.append("## Activity Over Time")
    if year_counts:
        for year in sorted(year_counts):
            lines.append(f"- {year}: {year_counts[year]} {pluralize(year_counts[year], 'commit')}")
    else:
        lines.append("- No commit history found.")

    if month_counts:
        lines.append("")
        lines.append("### Recent Monthly Activity")
        for month, count in sorted(month_counts.items())[-12:]:
            lines.append(f"- {month}: {count} {pluralize(count, 'commit')}")

    if recent_commits:
        lines.append("")
        lines.append("## Recent Commits")
        for commit in recent_commits:
            lines.append(f"- {format_commit(commit)}")

    if path_commits:
        lines.append("")
        lines.append("## Current Path History")
        for commit in path_commits[:10]:
            lines.append(f"- {format_commit(commit)}")

    top_authors = format_top_authors(author_lines)
    if top_authors:
        lines.append("")
        lines.append("## Top Authors")
        lines.extend(top_authors)

    if tag_lines:
        lines.append("")
        lines.append("## Recent Tags")
        for tag_line in tag_lines[-10:]:
            lines.append(f"- {tag_line}")

    lines.append("")
    lines.append("## Interpretation")
    interpretation: list[str] = []
    if pathspec and path_commits:
        if len(path_commits) <= 3:
            interpretation.append(
                "The current project path looks episodic: it was created, then revisited in a small number of major updates."
            )
        else:
            interpretation.append(
                "The current project path shows an extended series of revisions rather than a single burst of work."
            )
    if default_branch and branch and branch != default_branch:
        interpretation.append(
            f"The active branch is not the default branch, which usually means current work is being staged before merge or publication."
        )
    if tag_lines:
        interpretation.append(
            "The repository uses tags as milestones or release-like snapshots, which helps identify project checkpoints over time."
        )
    if len(local_branches) + len(remote_branches) > 10:
        interpretation.append(
            "The branch layout suggests a multi-project or long-lived personal repository rather than a narrowly scoped single application."
        )
    if not interpretation:
        interpretation.append("The repository history looks straightforward, with no unusual branch or path-level signals.")

    for item in interpretation:
        lines.append(f"- {item}")

    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a Markdown report for the current Git repository."
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Repository path or a subdirectory inside the repository. Defaults to the current directory.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    target_path = Path(args.path).expanduser().resolve()

    try:
        report = build_report(target_path)
    except GitCommandError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print(report, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
