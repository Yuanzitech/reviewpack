from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlparse


@dataclass(frozen=True)
class GitHubPullRequestRef:
    """Parsed GitHub pull request reference."""

    owner: str
    repo: str
    pull_number: int
    url: str


def parse_github_pr_url(url: str) -> GitHubPullRequestRef:
    """Parse a GitHub pull request URL.

    Supported format:

    https://github.com/owner/repo/pull/123

    This function does not use network access. It only parses the URL string
    provided by the user.
    """

    parsed = urlparse(url.strip())

    if parsed.scheme not in {"http", "https"}:
        raise ValueError("GitHub PR URL must use http or https.")

    if parsed.netloc.lower() != "github.com":
        raise ValueError("GitHub PR URL must use github.com.")

    parts = [part for part in parsed.path.split("/") if part]

    if len(parts) != 4:
        raise ValueError("GitHub PR URL must have the format /owner/repo/pull/number.")

    owner, repo, pull_segment, pull_number_raw = parts

    if pull_segment != "pull":
        raise ValueError("GitHub PR URL must contain /pull/ before the pull request number.")

    if not pull_number_raw.isdigit():
        raise ValueError("GitHub PR number must be numeric.")

    pull_number = int(pull_number_raw)

    if pull_number <= 0:
        raise ValueError("GitHub PR number must be greater than zero.")

    return GitHubPullRequestRef(
        owner=owner,
        repo=repo,
        pull_number=pull_number,
        url=url.strip(),
    )


def is_github_pr_url(url: str) -> bool:
    """Return True if a string looks like a supported GitHub PR URL."""

    try:
        parse_github_pr_url(url)
    except ValueError:
        return False

    return True
