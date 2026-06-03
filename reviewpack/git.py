from __future__ import annotations

import subprocess
from pathlib import Path

from reviewpack.models import ChangedFile


def parse_numstat_value(value: str) -> int:
    """Parse a git numstat value.

    Git reports binary files as "-". Reviewpack treats those as zero-line changes
    for deterministic summary purposes.
    """

    if value == "-":
        return 0

    return int(value)


def parse_numstat_line(line: str) -> ChangedFile | None:
    """Parse one line of git diff numstat output.

    Expected format:
    additions, deletions, path separated by tab characters.
    """

    parts = line.rstrip("\n").split("\t")

    if len(parts) < 3:
        return None

    additions_raw = parts[0]
    deletions_raw = parts[1]
    path = parts[-1]

    return ChangedFile(
        path=path,
        additions=parse_numstat_value(additions_raw),
        deletions=parse_numstat_value(deletions_raw),
    )


def parse_numstat(text: str) -> list[ChangedFile]:
    """Parse git diff numstat output into changed files."""

    files: list[ChangedFile] = []

    for line in text.splitlines():
        if not line.strip():
            continue

        changed_file = parse_numstat_line(line)

        if changed_file is not None:
            files.append(changed_file)

    return files


def collect_changed_files_from_git(
    base: str = "main",
    head: str = "HEAD",
    repo_path: str | Path = ".",
) -> list[ChangedFile]:
    """Collect changed files from a local git repository.

    This function only uses local git metadata. It does not use network access,
    GitHub APIs, AI providers, environment variables, or external services.
    """

    repository = Path(repo_path)

    command = [
        "git",
        "diff",
        "--numstat",
        f"{base}...{head}",
    ]

    completed = subprocess.run(
        command,
        cwd=repository,
        capture_output=True,
        text=True,
        check=False,
    )

    if completed.returncode != 0:
        message = completed.stderr.strip() or "git diff failed"
        raise RuntimeError(message)

    return parse_numstat(completed.stdout)
