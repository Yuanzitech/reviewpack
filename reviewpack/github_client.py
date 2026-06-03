from __future__ import annotations

import json
import os
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from reviewpack.github import GitHubPullRequestRef, parse_github_pr_url
from reviewpack.models import ChangedFile, PullRequestInfo, ReviewpackInput


GITHUB_API_BASE_URL = "https://api.github.com"


class GitHubAPIError(RuntimeError):
    """Raised when GitHub API collection fails."""


def get_github_token(explicit_token: str | None = None) -> str | None:
    """Return a GitHub token from explicit input or supported environment variables.

    Reviewpack never stores tokens and never includes them in generated output.
    """

    if explicit_token:
        return explicit_token

    return os.getenv("REVIEWPACK_GITHUB_TOKEN") or os.getenv("GITHUB_TOKEN")


def build_github_api_url(ref: GitHubPullRequestRef, path: str) -> str:
    """Build a GitHub API URL for a pull request resource."""

    owner = quote(ref.owner, safe="")
    repo = quote(ref.repo, safe="")
    clean_path = path.lstrip("/")

    return f"{GITHUB_API_BASE_URL}/repos/{owner}/{repo}/{clean_path}"


def build_github_request(url: str, token: str | None = None) -> Request:
    """Build a GitHub API request.

    The token, when provided, is only sent as an Authorization header. It is not
    written to Reviewpack output files.
    """

    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "reviewpack",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    if token:
        headers["Authorization"] = f"Bearer {token}"

    return Request(url, headers=headers)


def read_github_json(url: str, token: str | None = None) -> object:
    """Read JSON from the GitHub API."""

    request = build_github_request(url, token)

    try:
        with urlopen(request, timeout=20) as response:
            payload = response.read().decode("utf-8")
    except HTTPError as error:
        message = error.read().decode("utf-8", errors="replace")
        raise GitHubAPIError(f"GitHub API request failed with HTTP {error.code}: {message}") from error
    except URLError as error:
        raise GitHubAPIError(f"GitHub API request failed: {error.reason}") from error

    return json.loads(payload)


def fetch_github_pull_request(ref: GitHubPullRequestRef, token: str | None = None) -> dict:
    """Fetch pull request metadata from the GitHub API."""

    url = build_github_api_url(ref, f"pulls/{ref.pull_number}")
    data = read_github_json(url, token)

    if not isinstance(data, dict):
        raise GitHubAPIError("GitHub pull request response was not an object.")

    return data


def fetch_github_pull_request_files(ref: GitHubPullRequestRef, token: str | None = None) -> list[dict]:
    """Fetch changed files for a pull request from the GitHub API."""

    files: list[dict] = []
    page = 1

    while True:
        url = build_github_api_url(ref, f"pulls/{ref.pull_number}/files?per_page=100&page={page}")
        data = read_github_json(url, token)

        if not isinstance(data, list):
            raise GitHubAPIError("GitHub pull request files response was not a list.")

        files.extend(item for item in data if isinstance(item, dict))

        if len(data) < 100:
            break

        page += 1

    return files


def github_pr_to_reviewpack_input(
    ref: GitHubPullRequestRef,
    pr_data: dict,
    file_data: list[dict],
) -> ReviewpackInput:
    """Convert GitHub API data into Reviewpack input."""

    user = pr_data.get("user") or {}
    author = user.get("login") or "unknown"
    title = pr_data.get("title") or f"GitHub PR #{ref.pull_number}"
    description = pr_data.get("body") or None
    html_url = pr_data.get("html_url") or ref.url

    changed_files: list[ChangedFile] = []

    for item in file_data:
        path = item.get("filename")
        if not path:
            continue

        changed_files.append(
            ChangedFile(
                path=str(path),
                additions=int(item.get("additions") or 0),
                deletions=int(item.get("deletions") or 0),
            )
        )

    return ReviewpackInput(
        pr=PullRequestInfo(
            title=str(title),
            author=str(author),
            url=str(html_url),
            description=description,
        ),
        changed_files=changed_files,
    )


def collect_reviewpack_input_from_github_url(
    pr_url: str,
    token: str | None = None,
) -> ReviewpackInput:
    """Collect Reviewpack input from a GitHub pull request URL.

    This function fetches GitHub PR metadata and changed file statistics. It does
    not fetch raw diffs, full source code, branch names, or commit messages.
    """

    ref = parse_github_pr_url(pr_url)
    resolved_token = get_github_token(token)

    pr_data = fetch_github_pull_request(ref, resolved_token)
    file_data = fetch_github_pull_request_files(ref, resolved_token)

    return github_pr_to_reviewpack_input(ref, pr_data, file_data)
