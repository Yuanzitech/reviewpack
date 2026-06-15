import pytest

from reviewpack.github_client import (
    GitHubPullRequestRef,
    build_github_api_url,
    build_github_files_api_url,
    collect_reviewpack_input_from_github_url,
    github_error_message,
    parse_github_pull_request_url,
)


def test_parse_github_pull_request_url() -> None:
    ref = parse_github_pull_request_url("https://github.com/owner/repo/pull/123")

    assert ref == GitHubPullRequestRef(
        owner="owner",
        repo="repo",
        number=123,
    )


def test_parse_github_pull_request_url_rejects_invalid_url() -> None:
    with pytest.raises(ValueError):
        parse_github_pull_request_url("https://github.com/owner/repo/issues/123")


def test_build_github_api_url() -> None:
    ref = GitHubPullRequestRef(owner="owner", repo="repo", number=123)

    assert build_github_api_url(ref) == "https://api.github.com/repos/owner/repo/pulls/123"


def test_build_github_files_api_url() -> None:
    ref = GitHubPullRequestRef(owner="owner", repo="repo", number=123)

    assert build_github_files_api_url(ref) == "https://api.github.com/repos/owner/repo/pulls/123/files"


def test_github_error_message_for_common_status_codes() -> None:
    assert "401 Unauthorized" in github_error_message(401, "https://api.github.com/example")
    assert "403 Forbidden" in github_error_message(403, "https://api.github.com/example")
    assert "404 Not Found" in github_error_message(404, "https://api.github.com/example")
    assert "HTTP 500" in github_error_message(500, "https://api.github.com/example")


def test_collect_reviewpack_input_from_github_url_reads_enriched_metadata(monkeypatch) -> None:
    pr_response = {
        "title": "Improve docs",
        "user": {"login": "octocat"},
        "html_url": "https://github.com/owner/repo/pull/123",
        "body": "This updates documentation.",
        "state": "open",
        "draft": False,
        "base": {"ref": "main"},
        "head": {"ref": "docs-update"},
        "commits": 3,
        "labels": [
            {"name": "documentation"},
            {"name": "good first issue"},
        ],
    }
    files_response = [
        {
            "filename": "README.md",
            "additions": 10,
            "deletions": 2,
            "status": "modified",
        },
        {
            "filename": "docs/usage.md",
            "additions": 20,
            "deletions": 1,
            "status": "added",
        },
    ]

    def fake_fetch(url: str, token: str | None = None):
        if url.endswith("/files"):
            return files_response
        return pr_response

    monkeypatch.setattr("reviewpack.github_client.fetch_github_json", fake_fetch)

    reviewpack_input = collect_reviewpack_input_from_github_url(
        "https://github.com/owner/repo/pull/123",
        token="token",
    )

    assert reviewpack_input.pr.title == "Improve docs"
    assert reviewpack_input.pr.author == "octocat"
    assert reviewpack_input.pr.state == "open"
    assert reviewpack_input.pr.is_draft is False
    assert reviewpack_input.pr.base_branch == "main"
    assert reviewpack_input.pr.head_branch == "docs-update"
    assert reviewpack_input.pr.commit_count == 3
    assert reviewpack_input.pr.labels == ["documentation", "good first issue"]

    assert len(reviewpack_input.changed_files) == 2
    assert reviewpack_input.changed_files[0].path == "README.md"
    assert reviewpack_input.changed_files[0].status == "modified"
    assert reviewpack_input.changed_files[1].path == "docs/usage.md"
    assert reviewpack_input.changed_files[1].status == "added"
