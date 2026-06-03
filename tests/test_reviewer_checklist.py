from reviewpack.analyzer import analyze_reviewpack_input
from reviewpack.models import ChangedFile, FileCategory, PullRequestInfo, ReviewpackInput
from reviewpack.renderers import write_reviewpack_outputs
from reviewpack.reviewer_checklist import generate_reviewer_checklist_items, render_reviewer_checklist


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


def test_generate_reviewer_checklist_items_detects_expected_sections() -> None:
    result = make_result()
    items = generate_reviewer_checklist_items(result)

    sections = {item.section for item in items}

    assert "Core Review" in sections
    assert "Tests" in sections
    assert "Dependencies" in sections
    assert "CI" in sections
    assert "Documentation" in sections
    assert "Release" in sections
    assert "Privacy" in sections


def test_generate_reviewer_checklist_items_for_test_only_change() -> None:
    reviewpack_input = ReviewpackInput(
        pr=PullRequestInfo(
            title="Add test coverage",
            author="alice",
        ),
        changed_files=[
            ChangedFile(
                path="tests/test_app.py",
                additions=20,
                deletions=0,
                category=FileCategory.TEST,
            ),
        ],
    )
    result = analyze_reviewpack_input(reviewpack_input)
    items = generate_reviewer_checklist_items(result)

    assert any(item.section == "Tests" for item in items)


def test_render_reviewer_checklist_contains_expected_sections() -> None:
    result = make_result()
    markdown = render_reviewer_checklist(result)

    assert "# Reviewer Checklist" in markdown
    assert "## Checklist" in markdown
    assert "Core Review" in markdown
    assert "Maintainers should adapt the checklist" in markdown
    assert "AI was not used" in markdown


def test_write_reviewpack_outputs_creates_reviewer_checklist_file(tmp_path) -> None:
    result = make_result()

    write_reviewpack_outputs(result, tmp_path)

    output_path = tmp_path / "reviewer-checklist.md"

    assert output_path.exists()

    markdown = output_path.read_text(encoding="utf-8")
    assert "# Reviewer Checklist" in markdown
