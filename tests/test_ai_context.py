from reviewpack.ai_context import render_ai_context, write_ai_context
from reviewpack.analyzer import analyze_reviewpack_input
from reviewpack.demo import build_demo_reviewpack_input
from reviewpack.models import PullRequestInfo, ReviewpackInput


def make_result():
    return analyze_reviewpack_input(build_demo_reviewpack_input())


def test_render_ai_context_contains_expected_sections() -> None:
    result = make_result()
    markdown = render_ai_context(result)

    assert "# Reviewpack AI Context" in markdown
    assert "Review Objective" in markdown
    assert "Known Limitations" in markdown
    assert "Pull Request" in markdown
    assert "Change Statistics" in markdown
    assert "Risk Signals" in markdown
    assert "Reviewer Checklist" in markdown
    assert "Release Note Hints" in markdown
    assert "Requested AI Review Output" in markdown
    assert "Privacy Notes" in markdown


def test_render_ai_context_includes_demo_pr_metadata() -> None:
    result = make_result()
    markdown = render_ai_context(result)

    assert "Add token refresh support" in markdown
    assert "demo-user" in markdown


def test_render_ai_context_includes_optional_github_metadata() -> None:
    reviewpack_input = ReviewpackInput(
        pr=PullRequestInfo(
            title="Improve docs",
            author="octocat",
            url="https://github.com/owner/repo/pull/123",
            state="open",
            is_draft=False,
            base_branch="main",
            head_branch="docs-update",
            commit_count=3,
            labels=["documentation"],
        ),
        changed_files=[],
    )
    result = analyze_reviewpack_input(reviewpack_input)

    markdown = render_ai_context(result)

    assert "- State: open" in markdown
    assert "- Draft: false" in markdown
    assert "- Base branch: main" in markdown
    assert "- Head branch: docs-update" in markdown
    assert "- Commits: 3" in markdown
    assert "- Labels: documentation" in markdown


def test_render_ai_context_does_not_claim_raw_source_was_inspected() -> None:
    result = make_result()
    markdown = render_ai_context(result)

    assert "Do not claim that raw source code was inspected" in markdown


def test_write_ai_context_creates_file(tmp_path) -> None:
    result = make_result()

    output_path = write_ai_context(result, tmp_path)

    assert output_path.exists()
    assert output_path.name == "ai-context.md"

    markdown = output_path.read_text(encoding="utf-8")
    assert "# Reviewpack AI Context" in markdown
