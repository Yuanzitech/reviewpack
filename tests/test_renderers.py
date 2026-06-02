import json

from reviewpack.analyzer import analyze_reviewpack_input
from reviewpack.models import ChangedFile, PullRequestInfo, ReviewpackInput
from reviewpack.renderers import (
    render_ai_review_prompt,
    render_pr_summary,
    render_risk_checklist,
    write_reviewpack_outputs,
)


def make_result():
    reviewpack_input = ReviewpackInput(
        pr=PullRequestInfo(
            title="Add token refresh support",
            author="alice",
            url="https://github.com/octo-org/example-repo/pull/123",
            description="Update token refresh behavior.",
        ),
        changed_files=[
            ChangedFile(path="src/auth/token.py", additions=120, deletions=32),
            ChangedFile(path="README.md", additions=12, deletions=3),
        ],
    )
    return analyze_reviewpack_input(reviewpack_input)


def test_render_pr_summary_contains_expected_sections() -> None:
    result = make_result()
    markdown = render_pr_summary(result)

    assert "# PR Review Context Pack" in markdown
    assert "## Pull Request" in markdown
    assert "## Change Statistics" in markdown
    assert "## Suggested Review Focus" in markdown
    assert "Privacy Notes" in markdown


def test_render_risk_checklist_contains_risk_content() -> None:
    result = make_result()
    markdown = render_risk_checklist(result)

    assert "# Risk Checklist" in markdown
    assert "High-risk area changed" in markdown


def test_render_ai_review_prompt_contains_requested_output() -> None:
    result = make_result()
    markdown = render_ai_review_prompt(result)

    assert "# AI Review Prompt" in markdown
    assert "Requested Review Output" in markdown
    assert "human maintainer" in markdown


def test_write_reviewpack_outputs_creates_expected_files(tmp_path) -> None:
    result = make_result()

    write_reviewpack_outputs(result, tmp_path)

    assert (tmp_path / "pr-summary.md").exists()
    assert (tmp_path / "risk-checklist.md").exists()
    assert (tmp_path / "ai-review-prompt.md").exists()
    assert (tmp_path / "reviewpack.json").exists()

    data = json.loads((tmp_path / "reviewpack.json").read_text(encoding="utf-8"))
    assert data["pr"]["title"] == "Add token refresh support"
