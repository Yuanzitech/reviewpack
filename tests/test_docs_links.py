from pathlib import Path


DOCUMENTATION_FILES_LINKED_FROM_README = {
    "docs/status.md",
    "docs/installation.md",
    "docs/commands.md",
    "docs/configuration.md",
    "docs/config-schema.md",
    "docs/output-artifacts.md",
    "docs/artifact-contract.md",
    "docs/json-output.md",
    "docs/v1-readiness.md",
    "docs/usage.md",
    "docs/privacy.md",
    "docs/design.md",
    "docs/local-git.md",
    "docs/github.md",
    "docs/github-action.md",
    "docs/ai-handoff.md",
    "docs/ai-preview.md",
    "docs/release-note-hints.md",
    "docs/reviewer-checklist.md",
    "docs/integrations.md",
    "docs/roadmap.md",
    "docs/release-checklist.md",
    "examples/README.md",
}


EXAMPLE_FILES_LINKED_FROM_README = {
    "examples/.reviewpack.yml",
    "examples/github-action.yml",
    "examples/github-action-local.yml",
    "examples/github-action-comment.yml",
    "examples/output/risk-checklist.example.md",
    "examples/output/reviewer-checklist.example.md",
    "examples/output/release-note-hints.example.md",
    "examples/output/ai-handoff.example.md",
    "examples/output/ai-context.example.md",
}


def test_key_documentation_files_linked_from_readme_exist() -> None:
    for file_path in sorted(DOCUMENTATION_FILES_LINKED_FROM_README):
        assert Path(file_path).exists(), f"Missing documented file: {file_path}"


def test_key_example_files_exist() -> None:
    for file_path in sorted(EXAMPLE_FILES_LINKED_FROM_README):
        assert Path(file_path).exists(), f"Missing example file: {file_path}"


def test_readme_mentions_contract_and_schema_docs() -> None:
    readme = Path("README.md").read_text(encoding="utf-8")

    assert "docs/artifact-contract.md" in readme
    assert "docs/config-schema.md" in readme
    assert "docs/json-output.md" in readme
    assert "docs/v1-readiness.md" in readme


def test_chinese_readme_mentions_contract_and_schema_docs() -> None:
    readme = Path("README.zh-CN.md").read_text(encoding="utf-8")

    assert "docs/artifact-contract.md" in readme
    assert "docs/config-schema.md" in readme
    assert "docs/json-output.md" in readme
    assert "docs/v1-readiness.md" in readme
