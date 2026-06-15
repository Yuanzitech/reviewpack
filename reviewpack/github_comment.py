from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any

from reviewpack.github_client import GitHubAPIError, parse_github_pull_request_url


REVIEWPACK_COMMENT_MARKER = "<!-- reviewpack-comment -->"


def render_reviewpack_comment(
    artifact_name: str = "reviewpack-output",
    output_dir: str = ".reviewpack",
    workflow_run_url: str | None = None,
) -> str:
    """Render a short Reviewpack pull request comment body."""

    lines: list[str] = []

    lines.append(REVIEWPACK_COMMENT_MARKER)
    lines.append("")
    lines.append("## Reviewpack Summary")
    lines.append("")
    lines.append("Reviewpack generated a pull request review context pack for this PR.")
    lines.append("")
    lines.append("Recommended files in the workflow artifact:")
    lines.append("")
    lines.append("- `pr-summary.md`")
    lines.append("- `risk-checklist.md`")
    lines.append("- `reviewer-checklist.md`")
    lines.append("- `release-note-hints.md`")
    lines.append("- `ai-handoff.md`")
    lines.append("- `ai-context.md`")
    lines.append("- `ai-review-prompt.md`")
    lines.append("")
    lines.append("AI handoff:")
    lines.append("")
    lines.append("- If an AI assistant can read files, start with `ai-handoff.md`.")
    lines.append("- If an AI assistant cannot read multiple files, upload `ai-context.md`.")
    lines.append("- If only copy and paste is available, use `ai-review-prompt.md`.")
    lines.append("")
    lines.append("Artifact:")
    lines.append("")
    lines.append(f"- Name: `{artifact_name}`")
    lines.append(f"- Output directory: `{output_dir}`")

    if workflow_run_url:
        lines.append(f"- Workflow run: {workflow_run_url}")

    lines.append("")
    lines.append("Privacy notes:")
    lines.append("")
    lines.append("- Reviewpack did not call an AI provider.")
    lines.append("- Reviewpack did not upload source code to an AI provider.")
    lines.append("- This comment is a short pointer to the generated artifact, not a full automated review.")
    lines.append("")

    return "\n".join(lines)


def build_issue_comments_url(owner: str, repo: str, number: int) -> str:
    """Build the GitHub issue comments URL for a pull request."""

    return f"https://api.github.com/repos/{owner}/{repo}/issues/{number}/comments"


def build_issue_comment_url(owner: str, repo: str, comment_id: int) -> str:
    """Build the GitHub issue comment URL for a specific comment."""

    return f"https://api.github.com/repos/{owner}/{repo}/issues/comments/{comment_id}"


def github_json_request(
    url: str,
    token: str,
    method: str = "GET",
    payload: dict[str, Any] | None = None,
) -> Any:
    """Send a JSON request to the GitHub API."""

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "User-Agent": "reviewpack",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(
        url,
        data=data,
        headers=headers,
        method=method,
    )

    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            raw_body = response.read().decode("utf-8")
    except urllib.error.HTTPError as error:
        raise GitHubAPIError(f"GitHub comment API request failed with HTTP {error.code}: {url}") from error
    except urllib.error.URLError as error:
        raise GitHubAPIError(f"GitHub comment API request failed: {error}") from error

    if not raw_body:
        return None

    return json.loads(raw_body)


def find_existing_reviewpack_comment(comments: list[Any]) -> dict[str, Any] | None:
    """Find an existing Reviewpack comment by marker."""

    for comment in comments:
        if not isinstance(comment, dict):
            continue

        body = comment.get("body")
        if isinstance(body, str) and REVIEWPACK_COMMENT_MARKER in body:
            return comment

    return None


def post_or_update_reviewpack_comment(
    pr_url: str,
    token: str,
    artifact_name: str = "reviewpack-output",
    output_dir: str = ".reviewpack",
    workflow_run_url: str | None = None,
) -> str:
    """Post or update the Reviewpack PR comment."""

    ref = parse_github_pull_request_url(pr_url)
    comment_body = render_reviewpack_comment(
        artifact_name=artifact_name,
        output_dir=output_dir,
        workflow_run_url=workflow_run_url,
    )

    comments_url = build_issue_comments_url(ref.owner, ref.repo, ref.number)
    comments = github_json_request(comments_url, token=token, method="GET")

    if not isinstance(comments, list):
        raise GitHubAPIError("GitHub comments response was not a JSON array.")

    existing_comment = find_existing_reviewpack_comment(comments)

    if existing_comment is not None:
        comment_id = existing_comment.get("id")
        if not isinstance(comment_id, int):
            raise GitHubAPIError("Existing Reviewpack comment did not include a numeric id.")

        comment_url = build_issue_comment_url(ref.owner, ref.repo, comment_id)
        github_json_request(
            comment_url,
            token=token,
            method="PATCH",
            payload={"body": comment_body},
        )
        return "updated"

    github_json_request(
        comments_url,
        token=token,
        method="POST",
        payload={"body": comment_body},
    )
    return "created"


def main() -> None:
    """Entry point used by the GitHub Action."""

    token = os.getenv("REVIEWPACK_GITHUB_TOKEN")
    pr_url = os.getenv("REVIEWPACK_PR_URL")
    artifact_name = os.getenv("REVIEWPACK_ARTIFACT_NAME", "reviewpack-output")
    output_dir = os.getenv("REVIEWPACK_OUTPUT_DIR", ".reviewpack")
    workflow_run_url = os.getenv("REVIEWPACK_WORKFLOW_RUN_URL")

    if not token:
        raise SystemExit("REVIEWPACK_GITHUB_TOKEN is required to post a Reviewpack PR comment.")

    if not pr_url:
        raise SystemExit("REVIEWPACK_PR_URL is required to post a Reviewpack PR comment.")

    result = post_or_update_reviewpack_comment(
        pr_url=pr_url,
        token=token,
        artifact_name=artifact_name,
        output_dir=output_dir,
        workflow_run_url=workflow_run_url,
    )

    print(f"Reviewpack PR comment {result}.")


if __name__ == "__main__":
    main()
