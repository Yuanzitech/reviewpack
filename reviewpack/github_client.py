from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any

from reviewpack.models import ChangedFile, PullRequestInfo, ReviewpackInput


GITHUB_PR_URL_PATTERN = re.compile(
    r"^https://github\.com/(?P<owner>[^/]+)/(?P<repo>[^/]+)/pull/(?P<number>\d+)/?$"
)


class GitHubAPIError(RuntimeError):
    """Raised when GitHub API requests fail."""


@dataclass(frozen=True)
class GitHubPullRequestRef:
    """Parsed GitHub pull request URL reference."""

    owner: str
    repo: str
    number: int


def parse_github_pull_request_url(pr_url: str) -> GitHubPullRequestRef:
    """Parse a GitHub pull request URL."""

    match = GITHUB_PR_URL_PATTERN.match(pr_url.strip())

    if not match:
        raise ValueError(
            "Invalid GitHub pull request URL. Expected format: "
            "https://github.com/owner/repo/pull/123"
        )

    return GitHubPullRequestRef(
        owner=match.group("owner"),
        repo=match.group("repo"),
        number=int(match.group("number")),
    )


def build_github_api_url(ref: GitHubPullRequestRef) -> str:
    """Build GitHub API URL for pull request metadata."""

    return f"https://api.github.com/repos/{ref.owner}/{ref.repo}/pulls/{ref.number}"


def build_github_files_api_url(ref: GitHubPullRequestRef) -> str:
    """Build GitHub API URL for pull request changed files."""

    return f"https://api.github.com/repos/{ref.owner}/{ref.repo}/pulls/{ref.number}/files"


def get_github_token(token: str | None = None) -> str | None:
    """Return GitHub token from explicit input or environment."""

    if token:
        return token

    return os.getenv("REVIEWPACK_GITHUB_TOKEN")


def github_error_message(status_code: int, url: str) -> str:
    """Return a friendly GitHub API error message."""

    if status_code == 401:
        return (
            "GitHub API request failed with 401 Unauthorized. "
            "The token may be missing, invalid, or expired. "
            "For private repositories or rate-limited usage, set REVIEWPACK_GITHUB_TOKEN."
        )

    if status_code == 403:
        return (
            "GitHub API request failed with 403 Forbidden. "
            "This may be caused by rate limits or insufficient token permissions. "
            "For private repositories or rate-limited usage, set REVIEWPACK_GITHUB_TOKEN."
        )

    if status_code == 404:
        return (
            "GitHub API request failed with 404 Not Found. "
            "The pull request may not exist, or the repository may not be accessible with the current token."
        )

    return f"GitHub API request failed with HTTP {status_code}: {url}"


def fetch_github_json(url: str, token: str | None = None) -> Any:
    """Fetch JSON from GitHub API."""

    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "reviewpack",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    github_token = get_github_token(token)
    if github_token:
        headers["Authorization"] = f"Bearer {github_token}"

    request = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            raw_body = response.read().decode("utf-8")
    except urllib.error.HTTPError as error:
        raise GitHubAPIError(github_error_message(error.code, url)) from error
    except urllib.error.URLError as error:
        raise GitHubAPIError(f"GitHub API request failed: {error}") from error

    return json.loads(raw_body)


def collect_reviewpack_input_from_github_url(pr_url: str, token: str | None = None) -> ReviewpackInput:
    """Collect Reviewpack input from a GitHub pull request URL."""

    ref = parse_github_pull_request_url(pr_url)

    pr_data = fetch_github_json(build_github_api_url(ref), token=token)
    files_data = fetch_github_json(build_github_files_api_url(ref), token=token)

    if not isinstance(pr_data, dict):
        raise GitHubAPIError("GitHub pull request response was not a JSON object.")

    if not isinstance(files_data, list):
        raise GitHubAPIError("GitHub pull request files response was not a JSON array.")

    labels = [
        label.get("name")
        for label in pr_data.get("labels", [])
        if isinstance(label, dict) and isinstance(label.get("name"), str)
    ]

    pull_request = PullRequestInfo(
        title=str(pr_data.get("title") or ""),
        author=str((pr_data.get("user") or {}).get("login") or "unknown"),
        url=str(pr_data.get("html_url") or pr_url),
        description=pr_data.get("body"),
        state=pr_data.get("state"),
        is_draft=pr_data.get("draft"),
        base_branch=(pr_data.get("base") or {}).get("ref"),
        head_branch=(pr_data.get("head") or {}).get("ref"),
        commit_count=pr_data.get("commits"),
        labels=labels,
    )

    changed_files: list[ChangedFile] = []

    for file_data in files_data:
        if not isinstance(file_data, dict):
            continue

        changed_files.append(
            ChangedFile(
                path=str(file_data.get("filename") or ""),
                additions=int(file_data.get("additions") or 0),
                deletions=int(file_data.get("deletions") or 0),
                status=file_data.get("status"),
            )
        )

    return ReviewpackInput(
        pr=pull_request,
        changed_files=changed_files,
    )
