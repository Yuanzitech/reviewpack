from reviewpack.github import GitHubPullRequestRef
from reviewpack.github_client import (
    build_github_api_url,
    build_github_request,
    get_github_token,
    github_pr_to_reviewpack_input,
)


def make_ref() -> GitHubPullRequestRef:
    return GitHubPullRequestRef(
        owner="octo-org",
        repo="example-repo",
        pull_number=123,
        url="https://github.com/octo-org/example-repo/pull/123",
    )


def test_build_github_api_url() -> None:
    ref = make_ref()

    url = build_github_api_url(ref, "pulls/123")

    assert url == "https://api.github.com/repos/octo-org/example-repo/pulls/123"


def test_build_github_request_without_token() -> None:
    request = build_github_request("https://api.github.com/repos/octo-org/example-repo/pulls/123")

    assert request.get_header("Accept") == "application/vnd.github+json"
    assert request.get_header("User-agent") == "reviewpack"
    assert request.get_header("Authorization") is None


def test_build_github_request_with_token() -> None:
    request = build_github_request(
        "https://api.github.com/repos/octo-org/example-repo/pulls/123",
        token="test-token",
    )

    assert request.get_header("Authorization") == "Bearer test-token"


def test_get_github_token_prefers_explicit_token(monkeypatch) -> None:
    monkeypatch.setenv("REVIEWPACK_GITHUB_TOKEN", "env-token")

    assert get_github_token("explicit-token") == "explicit-token"


def test_get_github_token_reads_reviewpack_env(monkeypatch) -> None:
    monkeypatch.setenv("REVIEWPACK_GITHUB_TOKEN", "reviewpack-token")
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)

    assert get_github_token() == "reviewpack-token"


def test_get_github_token_falls_back_to_github_token(monkeypatch) -> None:
    monkeypatch.delenv("REVIEWPACK_GITHUB_TOKEN", raising=False)
    monkeypatch.setenv("GITHUB_TOKEN", "github-token")

    assert get_github_token() == "github-token"


def test_github_pr_to_reviewpack_input_maps_metadata_and_files() -> None:
    ref = make_ref()
    pr_data = {
        "title": "Add token refresh support",
        "body": "Update authentication token refresh behavior.",
        "html_url": "https://github.com/octo-org/example-repo/pull/123",
        "user": {
            "login": "alice",
        },
    }
    file_data = [
        {
            "filename": "src/auth/token.py",
            "additions": 120,
            "deletions": 32,
        },
        {
            "filename": "README.md",
            "additions": 12,
            "deletions": 3,
        },
    ]

    reviewpack_input = github_pr_to_reviewpack_input(ref, pr_data, file_data)

    assert reviewpack_input.pr.title == "Add token refresh support"
    assert reviewpack_input.pr.author == "alice"
    assert reviewpack_input.pr.url == "https://github.com/octo-org/example-repo/pull/123"
    assert reviewpack_input.pr.description == "Update authentication token refresh behavior."
    assert len(reviewpack_input.changed_files) == 2
    assert reviewpack_input.changed_files[0].path == "src/auth/token.py"
    assert reviewpack_input.changed_files[0].additions == 120
    assert reviewpack_input.changed_files[0].deletions == 32
