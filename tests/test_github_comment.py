from reviewpack.github_comment import (
    REVIEWPACK_COMMENT_MARKER,
    build_issue_comment_url,
    build_issue_comments_url,
    find_existing_reviewpack_comment,
    render_reviewpack_comment,
)


def test_render_reviewpack_comment_contains_marker_and_artifact_guidance() -> None:
    body = render_reviewpack_comment(
        artifact_name="reviewpack-output",
        output_dir=".reviewpack",
        workflow_run_url="https://github.com/owner/repo/actions/runs/123",
    )

    assert REVIEWPACK_COMMENT_MARKER in body
    assert "## Reviewpack Summary" in body
    assert "`pr-summary.md`" in body
    assert "`risk-checklist.md`" in body
    assert "`reviewer-checklist.md`" in body
    assert "`release-note-hints.md`" in body
    assert "`ai-handoff.md`" in body
    assert "`ai-context.md`" in body
    assert "`ai-review-prompt.md`" in body
    assert "`reviewpack-output`" in body
    assert "https://github.com/owner/repo/actions/runs/123" in body


def test_render_reviewpack_comment_does_not_claim_ai_was_called() -> None:
    body = render_reviewpack_comment()

    assert "Reviewpack did not call an AI provider." in body
    assert "not a full automated review" in body


def test_build_issue_comments_url() -> None:
    url = build_issue_comments_url("owner", "repo", 123)

    assert url == "https://api.github.com/repos/owner/repo/issues/123/comments"


def test_build_issue_comment_url() -> None:
    url = build_issue_comment_url("owner", "repo", 456)

    assert url == "https://api.github.com/repos/owner/repo/issues/comments/456"


def test_find_existing_reviewpack_comment_returns_matching_comment() -> None:
    comments = [
        {"id": 1, "body": "Other comment"},
        {"id": 2, "body": f"{REVIEWPACK_COMMENT_MARKER}\nReviewpack comment"},
    ]

    comment = find_existing_reviewpack_comment(comments)

    assert comment == {"id": 2, "body": f"{REVIEWPACK_COMMENT_MARKER}\nReviewpack comment"}


def test_find_existing_reviewpack_comment_returns_none_when_missing() -> None:
    comments = [
        {"id": 1, "body": "Other comment"},
    ]

    assert find_existing_reviewpack_comment(comments) is None
