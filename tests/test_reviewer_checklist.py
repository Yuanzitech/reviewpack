from reviewpack.analyzer import analyze_reviewpack_input
from reviewpack.demo import build_demo_reviewpack_input
from reviewpack.reviewer_checklist import render_reviewer_checklist


def make_result():
    return analyze_reviewpack_input(build_demo_reviewpack_input())


def test_render_reviewer_checklist_contains_expected_sections() -> None:
    markdown = render_reviewer_checklist(make_result())

    assert "# Reviewer Checklist" in markdown
    assert "## Correctness" in markdown
    assert "## Tests" in markdown
    assert "## Documentation" in markdown
    assert "## Dependencies" in markdown
    assert "## CI, Configuration, and Infrastructure" in markdown
    assert "## Release Notes" in markdown
    assert "## Risk Review" in markdown
    assert "## AI Handoff" in markdown
    assert "## Final Maintainer Decision" in markdown


def test_render_reviewer_checklist_contains_actionable_items() -> None:
    markdown = render_reviewer_checklist(make_result())

    assert "- [ ]" in markdown
    assert "Confirm the intended behavior" in markdown
    assert "Check `release-note-hints.md`" in markdown
    assert "ai-handoff.md" in markdown
    assert "ai-context.md" in markdown
