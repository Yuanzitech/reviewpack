from reviewpack.analyzer import analyze_reviewpack_input
from reviewpack.config import ReviewpackConfig
from reviewpack.demo import build_demo_reviewpack_input
from reviewpack.renderers import write_reviewpack_outputs


DEFAULT_ARTIFACTS = {
    "pr-summary.md",
    "risk-checklist.md",
    "reviewer-checklist.md",
    "release-note-hints.md",
    "ai-review-prompt.md",
    "ai-handoff.md",
    "ai-context.md",
    "reviewpack.json",
}


def make_result():
    return analyze_reviewpack_input(build_demo_reviewpack_input())


def test_default_artifact_contract_files_are_generated(tmp_path) -> None:
    result = make_result()

    write_reviewpack_outputs(result, tmp_path)

    generated_files = {path.name for path in tmp_path.iterdir() if path.is_file()}

    assert DEFAULT_ARTIFACTS.issubset(generated_files)


def test_default_artifact_contract_does_not_generate_ai_input_preview_by_default(tmp_path) -> None:
    result = make_result()

    write_reviewpack_outputs(result, tmp_path)

    assert not (tmp_path / "ai-input-preview.md").exists()


def test_config_can_disable_json_artifact_with_public_json_key(tmp_path) -> None:
    result = make_result()
    config = ReviewpackConfig.model_validate(
        {
            "outputs": {
                "json": False,
            }
        }
    )

    write_reviewpack_outputs(result, tmp_path, config)

    assert not (tmp_path / "reviewpack.json").exists()
    assert (tmp_path / "pr-summary.md").exists()


def test_config_can_disable_selected_markdown_artifacts(tmp_path) -> None:
    result = make_result()
    config = ReviewpackConfig.model_validate(
        {
            "outputs": {
                "ai_context": False,
                "release_note_hints": False,
            }
        }
    )

    write_reviewpack_outputs(result, tmp_path, config)

    assert not (tmp_path / "ai-context.md").exists()
    assert not (tmp_path / "release-note-hints.md").exists()
    assert (tmp_path / "pr-summary.md").exists()
    assert (tmp_path / "reviewpack.json").exists()


def test_artifact_contract_document_exists() -> None:
    from pathlib import Path

    assert Path("docs/artifact-contract.md").exists()
