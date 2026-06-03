from reviewpack.analyzer import analyze_reviewpack_input
from reviewpack.models import ChangedFile, FileCategory, PullRequestInfo, ReviewpackInput
from reviewpack.release_notes import generate_release_note_hints, render_release_note_hints
from reviewpack.renderers import write_reviewpack_outputs


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
            ChangedFile(path="package.json", additions=4, deletions=2),
            ChangedFile(path=".github/workflows/ci.yml", additions=10, deletions=4),
            ChangedFile(path="README.md", additions=12, deletions=3),
        ],
    )
    return analyze_reviewpack_input(reviewpack_input)


def test_generate_release_note_hints_detects_expected_categories() -> None:
    result = make_result()
    hints = generate_release_note_hints(result)

    categories = {hint.category for hint in hints}

    assert "Changed" in categories
    assert "Dependencies" in categories
    assert "CI" in categories
    assert "Documentation" in categories
    assert "Risk" in categories


def test_generate_release_note_hints_for_test_only_change() -> None:
    reviewpack_input = ReviewpackInput(
        pr=PullRequestInfo(
            title="Add test coverage",
            author="alice",
        ),
        changed_files=[
            ChangedFile(path="tests/test_app.py", additions=20, deletions=0, category=FileCategory.TEST),
        ],
    )
    result = analyze_reviewpack_input(reviewpack_input)
    hints = generate_release_note_hints(result)

    assert any(hint.category == "Tests" for hint in hints)


def test_render_release_note_hints_contains_expected_sections() -> None:
    result = make_result()
    markdown = render_release_note_hints(result)

    assert "# Release Note Hints" in markdown
    assert "Possible Release Categories" in markdown
    assert "Maintainer Checklist" in markdown
    assert "Privacy Notes" in markdown
    assert "AI was not used" in markdown


def test_write_reviewpack_outputs_creates_release_note_hints_file(tmp_path) -> None:
    result = make_result()

    write_reviewpack_outputs(result, tmp_path)

    output_path = tmp_path / "release-note-hints.md"

    assert output_path.exists()

    markdown = output_path.read_text(encoding="utf-8")
    assert "# Release Note Hints" in markdown
