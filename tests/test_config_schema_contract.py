from reviewpack.config import ReviewpackConfig, load_config


def test_public_outputs_keys_are_supported() -> None:
    config = ReviewpackConfig.model_validate(
        {
            "outputs": {
                "pr_summary": False,
                "risk_checklist": False,
                "reviewer_checklist": False,
                "release_note_hints": False,
                "ai_review_prompt": False,
                "ai_handoff": False,
                "ai_context": False,
                "json": False,
            }
        }
    )

    assert config.outputs.pr_summary is False
    assert config.outputs.risk_checklist is False
    assert config.outputs.reviewer_checklist is False
    assert config.outputs.release_note_hints is False
    assert config.outputs.ai_review_prompt is False
    assert config.outputs.ai_handoff is False
    assert config.outputs.ai_context is False
    assert config.outputs.json_output is False


def test_internal_json_output_name_is_supported_for_backward_safe_model_population() -> None:
    config = ReviewpackConfig.model_validate(
        {
            "outputs": {
                "json_output": False,
            }
        }
    )

    assert config.outputs.json_output is False


def test_risk_config_public_keys_are_supported() -> None:
    config = ReviewpackConfig.model_validate(
        {
            "risk": {
                "large_pr_files": 10,
                "large_pr_lines": 250,
                "high_risk_paths": [
                    ".github/workflows/",
                    "pyproject.toml",
                ],
            }
        }
    )

    assert config.risk.large_pr_files == 10
    assert config.risk.large_pr_lines == 250
    assert config.risk.high_risk_paths == [
        ".github/workflows/",
        "pyproject.toml",
    ]


def test_paths_config_public_keys_are_supported() -> None:
    config = ReviewpackConfig.model_validate(
        {
            "paths": {
                "docs": ["docs/"],
                "tests": ["tests/"],
                "dependencies": ["pyproject.toml"],
                "ci": [".github/workflows/"],
                "config": [".reviewpack.yml"],
                "infrastructure": ["infra/"],
            }
        }
    )

    assert config.paths.docs == ["docs/"]
    assert config.paths.tests == ["tests/"]
    assert config.paths.dependencies == ["pyproject.toml"]
    assert config.paths.ci == [".github/workflows/"]
    assert config.paths.config == [".reviewpack.yml"]
    assert config.paths.infrastructure == ["infra/"]


def test_load_config_preserves_public_outputs_json_key(tmp_path) -> None:
    config_path = tmp_path / ".reviewpack.yml"
    config_path.write_text(
        """
outputs:
  json: false
""",
        encoding="utf-8",
    )

    config = load_config(config_path)

    assert config.outputs.json_output is False


def test_config_schema_document_exists() -> None:
    from pathlib import Path

    assert Path("docs/config-schema.md").exists()
