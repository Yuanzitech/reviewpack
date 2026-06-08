from reviewpack.analyzer import analyze_reviewpack_input
from reviewpack.demo import build_demo_reviewpack_input
from reviewpack.models import FileCategory
from reviewpack.renderers import write_reviewpack_outputs


def test_build_demo_reviewpack_input_contains_expected_data() -> None:
    reviewpack_input = build_demo_reviewpack_input()

    assert reviewpack_input.pr.title == "Add token refresh support"
    assert reviewpack_input.pr.author == "demo-user"
    assert len(reviewpack_input.changed_files) == 5


def test_demo_input_can_be_analyzed() -> None:
    reviewpack_input = build_demo_reviewpack_input()

    result = analyze_reviewpack_input(reviewpack_input)

    categories = {changed_file.category for changed_file in result.changed_files}

    assert FileCategory.SOURCE in categories
    assert FileCategory.DEPENDENCY in categories
    assert FileCategory.CI in categories
    assert FileCategory.DOCS in categories
    assert result.stats.files_changed == 5
    assert len(result.risk_signals) >= 1


def test_demo_output_writes_expected_files(tmp_path) -> None:
    reviewpack_input = build_demo_reviewpack_input()
    result = analyze_reviewpack_input(reviewpack_input)

    write_reviewpack_outputs(result, tmp_path)

    assert (tmp_path / "pr-summary.md").exists()
    assert (tmp_path / "risk-checklist.md").exists()
    assert (tmp_path / "reviewer-checklist.md").exists()
    assert (tmp_path / "release-note-hints.md").exists()
    assert (tmp_path / "ai-review-prompt.md").exists()
    assert (tmp_path / "ai-handoff.md").exists()
    assert (tmp_path / "ai-context.md").exists()
    assert (tmp_path / "reviewpack.json").exists()
