from reviewpack.analyzer import analyze_reviewpack_input
from reviewpack.demo import build_demo_reviewpack_input
from reviewpack.release_notes import generate_release_note_hints, render_release_note_hints


def make_result():
    return analyze_reviewpack_input(build_demo_reviewpack_input())


def test_generate_release_note_hints_detects_expected_categories() -> None:
    result = make_result()
    hints = generate_release_note_hints(result)

    categories = {hint.category for hint in hints}

    assert "Changed" in categories
    assert "Dependencies" in categories
    assert "CI" in categories
    assert "Documentation" in categories
    assert "Risk" in categories


def test_generate_release_note_hints_include_suggested_actions() -> None:
    result = make_result()
    hints = generate_release_note_hints(result)

    assert hints
    assert all(hint.suggested_action for hint in hints)


def test_render_release_note_hints_contains_decision_questions() -> None:
    markdown = render_release_note_hints(make_result())

    assert "# Release Note Hints" in markdown
    assert "## Summary" in markdown
    assert "Why this might matter" in markdown
    assert "Suggested maintainer action" in markdown
    assert "## Suggested Decision Questions" in markdown
