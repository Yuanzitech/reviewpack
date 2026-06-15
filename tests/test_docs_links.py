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
    "docs/integration-json.md",
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


KEY_CONFIG_EXAMPLES = {
    "examples/config/minimal.reviewpack.yml",
    "examples/config/python-project.reviewpack.yml",
    "examples/config/javascript-typescript-project.reviewpack.yml",
    "examples/config/monorepo.reviewpack.yml",
}


KEY_OUTPUT_EXAMPLES = {
    "examples/output/README.md",
    "examples/output/pr-summary.example.md",
    "examples/output/risk-checklist.example.md",
    "examples/output/reviewer-checklist.example.md",
    "examples/output/release-note-hints.example.md",
    "examples/output/ai-review-prompt.example.md",
    "examples/output/ai-handoff.example.md",
    "examples/output/ai-context.example.md",
    "examples/output/reviewpack.example.json",
}


SCHEMA_FILES = {
    "schemas/reviewpack-result.schema.json",
}


def test_key_documentation_files_linked_from_readme_exist() -> None:
    for file_path in sorted(DOCUMENTATION_FILES_LINKED_FROM_README):
        assert Path(file_path).exists(), f"Missing documented file: {file_path}"


def test_key_example_files_exist() -> None:
    for file_path in sorted(EXAMPLE_FILES_LINKED_FROM_README):
        assert Path(file_path).exists(), f"Missing example file: {file_path}"


def test_key_config_examples_exist() -> None:
    for file_path in sorted(KEY_CONFIG_EXAMPLES):
        assert Path(file_path).exists(), f"Missing config example: {file_path}"


def test_key_output_examples_exist() -> None:
    for file_path in sorted(KEY_OUTPUT_EXAMPLES):
        assert Path(file_path).exists(), f"Missing output example: {file_path}"


def test_schema_files_exist() -> None:
    for file_path in sorted(SCHEMA_FILES):
        assert Path(file_path).exists(), f"Missing schema file: {file_path}"


def test_readme_mentions_contract_schema_and_integration_docs() -> None:
    readme = Path("README.md").read_text(encoding="utf-8")

    assert "docs/artifact-contract.md" in readme
    assert "docs/config-schema.md" in readme
    assert "docs/json-output.md" in readme
    assert "docs/integration-json.md" in readme
    assert "docs/v1-readiness.md" in readme
    assert "schemas/reviewpack-result.schema.json" in readme


def test_chinese_readme_mentions_contract_schema_and_integration_docs() -> None:
    readme = Path("README.zh-CN.md").read_text(encoding="utf-8")

    assert "docs/artifact-contract.md" in readme
    assert "docs/config-schema.md" in readme
    assert "docs/json-output.md" in readme
    assert "docs/integration-json.md" in readme
    assert "docs/v1-readiness.md" in readme
    assert "schemas/reviewpack-result.schema.json" in readme


def test_configuration_docs_mention_config_examples() -> None:
    docs = Path("docs/configuration.md").read_text(encoding="utf-8")

    for file_path in sorted(KEY_CONFIG_EXAMPLES):
        assert file_path in docs


def test_output_docs_mention_output_examples() -> None:
    docs = Path("docs/output-artifacts.md").read_text(encoding="utf-8")
    contract = Path("docs/artifact-contract.md").read_text(encoding="utf-8")

    assert "examples/output/" in docs
    assert "examples/output/" in contract


def test_json_docs_mention_schema_and_example_json() -> None:
    json_docs = Path("docs/json-output.md").read_text(encoding="utf-8")
    integration_docs = Path("docs/integration-json.md").read_text(encoding="utf-8")

    assert "schemas/reviewpack-result.schema.json" in integration_docs
    assert "examples/output/reviewpack.example.json" in integration_docs
    assert "reviewpack.json" in json_docs
