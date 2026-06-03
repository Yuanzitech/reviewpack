import pytest

from reviewpack.github import is_github_pr_url, parse_github_pr_url


def test_parse_github_pr_url() -> None:
    ref = parse_github_pr_url("https://github.com/octo-org/example-repo/pull/123")

    assert ref.owner == "octo-org"
    assert ref.repo == "example-repo"
    assert ref.pull_number == 123
    assert ref.url == "https://github.com/octo-org/example-repo/pull/123"


def test_parse_github_pr_url_with_trailing_slash() -> None:
    ref = parse_github_pr_url("https://github.com/octo-org/example-repo/pull/123/")

    assert ref.owner == "octo-org"
    assert ref.repo == "example-repo"
    assert ref.pull_number == 123


def test_parse_github_pr_url_with_query_string() -> None:
    ref = parse_github_pr_url("https://github.com/octo-org/example-repo/pull/123?tab=files")

    assert ref.owner == "octo-org"
    assert ref.repo == "example-repo"
    assert ref.pull_number == 123


def test_parse_github_pr_url_allows_http() -> None:
    ref = parse_github_pr_url("http://github.com/octo-org/example-repo/pull/123")

    assert ref.owner == "octo-org"
    assert ref.repo == "example-repo"
    assert ref.pull_number == 123


def test_parse_github_pr_url_rejects_non_github_host() -> None:
    with pytest.raises(ValueError, match="github.com"):
        parse_github_pr_url("https://example.com/octo-org/example-repo/pull/123")


def test_parse_github_pr_url_rejects_missing_pull_segment() -> None:
    with pytest.raises(ValueError, match="/pull/"):
        parse_github_pr_url("https://github.com/octo-org/example-repo/issues/123")


def test_parse_github_pr_url_rejects_non_numeric_pull_number() -> None:
    with pytest.raises(ValueError, match="numeric"):
        parse_github_pr_url("https://github.com/octo-org/example-repo/pull/abc")


def test_parse_github_pr_url_rejects_zero_pull_number() -> None:
    with pytest.raises(ValueError, match="greater than zero"):
        parse_github_pr_url("https://github.com/octo-org/example-repo/pull/0")


def test_is_github_pr_url_returns_true_for_valid_url() -> None:
    assert is_github_pr_url("https://github.com/octo-org/example-repo/pull/123") is True


def test_is_github_pr_url_returns_false_for_invalid_url() -> None:
    assert is_github_pr_url("https://github.com/octo-org/example-repo/issues/123") is False
``
