import json
from pathlib import Path


EXAMPLE_OUTPUT_FILES = [
    "examples/output/README.md",
    "examples/output/pr-summary.example.md",
    "examples/output/risk-checklist.example.md",
    "examples/output/reviewer-checklist.example.md",
    "examples/output/release-note-hints.example.md",
    "examples/output/ai-review-prompt.example.md",
    "examples/output/ai-handoff.example.md",
    "examples/output/ai-context.example.md",
    "examples/output/reviewpack.example.json",
]


MARKDOWN_SECTION_CHECKS = {
    "examples/output/pr-summary.example.md": [
        "# PR Review Context Pack",
        "## Pull Request",
        "## Change Statistics",
        "## Changed Files",
        "## Suggested Review Focus",
        "## Privacy Notes",
    ],
    "examples/output/risk-checklist.example.md": [
        "# Risk Checklist",
        "### Why this matters",
        "### What to check",
        "### Affected files",
    ],
    "examples/output/reviewer-checklist.example.md": [
        "# Reviewer Checklist",
        "## Correctness",
        "## Tests",
        "## Documentation",
        "## Dependencies",
        "## Release Notes",
        "## Risk Review",
        "## Final Maintainer Decision",
    ],
    "examples/output/release-note-hints.example.md": [
        "# Release Note Hints",
        "## Summary",
        "Why this might matter",
        "Suggested maintainer action",
        "## Suggested Decision Questions",
    ],
    "examples/output/ai-review-prompt.example.md": [
        "# AI Review Prompt",
        "## Pull Request",
        "## Changed Files",
        "## Risk Signals",
        "## Suggested Review Focus",
        "## Requested Review Output",
    ],
    "examples/output/ai-handoff.example.md": [
        "# AI Handoff",
        "## Pull Request",
        "## Instructions for the AI assistant",
        "## Privacy notes",
    ],
    "examples/output/ai-context.example.md": [
        "# Reviewpack AI Context",
        "## Review Objective",
        "## Known Limitations",
        "## Pull Request",
        "## Change Statistics",
        "## Requested AI Review Output",
        "## Privacy Notes",
    ],
}


def test_example_output_files_exist() -> None:
    for file_path in EXAMPLE_OUTPUT_FILES:
        assert Path(file_path).exists(), f"Missing example output file: {file_path}"


def test_output_examples_readme_lists_expected_artifact_files() -> None:
    readme = Path("examples/output/README.md").read_text(encoding="utf-8")

    for file_path in EXAMPLE_OUTPUT_FILES:
        file_name = Path(file_path).name
        if file_name != "README.md":
            assert file_name in readme


def test_markdown_example_outputs_contain_expected_sections() -> None:
    for file_path, expected_sections in MARKDOWN_SECTION_CHECKS.items():
        text = Path(file_path).read_text(encoding="utf-8")

        for section in expected_sections:
            assert section in text, f"Missing section {section!r} in {file_path}"


def test_reviewpack_json_example_has_expected_top_level_fields() -> None:
    data = json.loads(Path("examples/output/reviewpack.example.json").read_text(encoding="utf-8"))

    assert set(data) == {
        "pr",
        "changed_files",
        "stats",
        "risk_signals",
        "review_focus",
        "metadata",
    }


def test_reviewpack_json_example_has_expected_nested_fields() -> None:
    data = json.loads(Path("examples/output/reviewpack.example.json").read_text(encoding="utf-8"))

    assert {"title", "author", "labels"}.issubset(data["pr"])

    assert data["changed_files"]
    assert {"path", "category", "status"}.issubset(data["changed_files"][0])

    assert {"files_changed", "additions", "deletions"}.issubset(data["stats"])

    assert data["risk_signals"]
    assert {"level", "title", "files"}.issubset(data["risk_signals"][0])

    assert data["review_focus"]
    assert {"title", "reason"}.issubset(data["review_focus"][0])


def test_output_artifacts_docs_mention_examples_directory() -> None:
    docs = Path("docs/output-artifacts.md").read_text(encoding="utf-8")

    assert "examples/output/" in docs


def test_artifact_contract_docs_mention_examples_directory() -> None:
    docs = Path("docs/artifact-contract.md").read_text(encoding="utf-8")

    assert "examples/output/" in docs
