from reviewpack.ai_preview import render_ai_input_preview, write_ai_input_preview
from reviewpack.analyzer import analyze_reviewpack_input
from reviewpack.models import ChangedFile, PullRequestInfo, ReviewpackInput


def make_result():
    reviewpack_input = ReviewpackInput(
        pr=PullRequestInfo(
            title="Add token refresh support",
            author="alice",
            url="https://github.com/octo-org/example-repo/pull/123",
            description="Update token refresh behavior. api_key=sk-test1234567890abcdef",
        ),
        changed_files=[
            ChangedFile(path="src/auth/token.py", additions=120, deletions=32),
            ChangedFile(path="README.md", additions=12, deletions=3),
        ],
    )

    return analyze_reviewpack_input(reviewpack_input)


def test_render_ai_input_preview_contains_expected_sections() -> None:
    result = make_result()
    markdown = render_ai_input_preview(result)

    assert "# AI Input Preview" in markdown
    assert "Included by default" in markdown
    assert "Excluded by default" in markdown
    assert "Risk Signals" in markdown
    assert "Suggested Review Focus" in markdown
    assert "Safety Notes" in markdown


def test_render_ai_input_preview_redacts_secret_like_values() -> None:
    result = make_result()
    markdown = render_ai_input_preview(result)

    assert "[REDACTED]" in markdown
    assert "sk-test1234567890abcdef" not in markdown


def test_render_ai_input_preview_does_not_claim_network_or_ai_usage() -> None:
    result = make_result()
    markdown = render_ai_input_preview(result)

    assert "without network access" in markdown
    assert "without calling an AI provider" in markdown


def test_write_ai_input_preview_creates_file(tmp_path) -> None:
    result = make_result()

    output_path = write_ai_input_preview(result, tmp_path)

    assert output_path.exists()
    assert output_path.name == "ai-input-preview.md"

    markdown = output_path.read_text(encoding="utf-8")
    assert "# AI Input Preview" in markdown
``
