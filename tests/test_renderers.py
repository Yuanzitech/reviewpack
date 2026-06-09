from reviewpack.analyzer import analyze_reviewpack_input
from reviewpack.demo import build_demo_reviewpack_input
from reviewpack.renderers import render_pr_summary, render_risk_checklist, write_reviewpack_outputs


def make_result():
    return analyze_reviewpack_input(build_demo_reviewpack_input())


def test_render_pr_summary_contains_expected_content() -> None:
    result = make_result()
    markdown = render_pr_summary(result)

    assert "# PR Review Context Pack" in markdown
    assert "## Pull Request" in markdown
    assert "Add token refresh support" in markdown
    assert "## Change Statistics" in markdown
    assert "## Changed Files" in markdown
    assert "## Suggested Review Focus" in markdown
    assert "## Privacy Notes" in markdown


def test_render_risk_checklist_contains_risk_content() -> None:
    result = make_result()
    markdown = render_risk_checklist(result)

    assert "# Risk Checklist" in markdown
    assert "High-risk area changed" in markdown
    assert "### Why this matters" in markdown
    assert "### What to check" in markdown
    assert "### Affected files" in markdown


def test_write_reviewpack_outputs_creates_expected_files(tmp_path) -> None:
    result = make_result()

    write_reviewpack_outputs(result, tmp_path)

    assert (tmp_path / "pr-summary.md").exists()
    assert (tmp_path / "risk-checklist.md").exists()
    assert (tmp_path / "reviewer-checklist.md").exists()
    assert (tmp_path / "release-note-hints.md").exists()
    assert (tmp_path / "ai-review-prompt.md").exists()
    assert (tmp_path / "ai-handoff.md").exists()
    assert (tmp_path / "ai-context.md").exists()
    assert (tmp_path / "reviewpack.json").exists()
