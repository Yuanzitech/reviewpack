from reviewpack.analyzer import analyze_reviewpack_input
from reviewpack.models import ChangedFile, PullRequestInfo, ReviewpackInput


def test_analyze_reviewpack_input_generates_stats_and_risks() -> None:
    reviewpack_input = ReviewpackInput(
        pr=PullRequestInfo(
            title="Add token refresh support",
            author="alice",
            url="https://github.com/octo-org/example-repo/pull/123",
        ),
        changed_files=[
            ChangedFile(path="src/auth/token.py", additions=120, deletions=32),
            ChangedFile(path="package.json", additions=4, deletions=2),
            ChangedFile(path=".github/workflows/ci.yml", additions=10, deletions=4),
        ],
    )

    result = analyze_reviewpack_input(reviewpack_input)

    assert result.stats.files_changed == 3
    assert result.stats.source_files == 1
    assert result.stats.dependency_files == 1
    assert result.stats.ci_files == 1
    assert result.metadata["network_used"] is False
    assert result.metadata["ai_used"] is False
    assert len(result.risk_signals) >= 1
    assert len(result.review_focus) >= 1
