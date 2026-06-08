from pathlib import Path

from reviewpack.config import ReviewpackConfig, load_config


def test_default_config_has_expected_outputs_enabled() -> None:
    config = ReviewpackConfig()

    assert config.outputs.pr_summary is True
    assert config.outputs.risk_checklist is True
    assert config.outputs.reviewer_checklist is True
    assert config.outputs.release_note_hints is True
    assert config.outputs.ai_review_prompt is True
    assert config.outputs.ai_handoff is True
    assert config.outputs.ai_context is True
    assert config.outputs.json is True


def test_load_config_returns_defaults_when_file_missing(tmp_path) -> None:
    config_path = tmp_path / "missing.yml"

    config = load_config(config_path)

    assert isinstance(config, ReviewpackConfig)
    assert config.outputs.ai_context is True


def test_load_config_reads_output_settings(tmp_path) -> None:
    config_path = tmp_path / ".reviewpack.yml"
    config_path.write_text(
        """
outputs:
  ai_context: false
  release_note_hints: false
""",
        encoding="utf-8",
    )

    config = load_config(config_path)

    assert config.outputs.ai_context is False
    assert config.outputs.release_note_hints is False
    assert config.outputs.pr_summary is True


def test_load_config_reads_risk_settings(tmp_path) -> None:
    config_path = tmp_path / ".reviewpack.yml"
    config_path.write_text(
        """
risk:
  large_pr_files: 5
  large_pr_lines: 100
  high_risk_paths:
    - .github/workflows/
    - pyproject.toml
""",
        encoding="utf-8",
    )

    config = load_config(config_path)

    assert config.risk.large_pr_files == 5
    assert config.risk.large_pr_lines == 100
    assert ".github/workflows/" in config.risk.high_risk_paths
    assert "pyproject.toml" in config.risk.high_risk_paths


def test_load_config_reads_path_settings(tmp_path) -> None:
    config_path = tmp_path / ".reviewpack.yml"
    config_path.write_text(
        """
paths:
  docs:
    - documentation/
  tests:
    - spec/
  dependencies:
    - uv.lock
""",
        encoding="utf-8",
    )

    config = load_config(config_path)

    assert config.paths.docs == ["documentation/"]
    assert config.paths.tests == ["spec/"]
    assert config.paths.dependencies == ["uv.lock"]


def test_load_config_uses_default_dotfile_when_present(tmp_path, monkeypatch) -> None:
    config_path = tmp_path / ".reviewpack.yml"
    config_path.write_text(
        """
outputs:
  json: false
""",
        encoding="utf-8",
    )

    monkeypatch.chdir(tmp_path)

    config = load_config()

    assert config.outputs.json is False


def test_load_config_rejects_non_mapping_yaml(tmp_path) -> None:
    config_path = tmp_path / ".reviewpack.yml"
    config_path.write_text(
        """
- invalid
- config
""",
        encoding="utf-8",
    )

    try:
        load_config(config_path)
    except ValueError as error:
        assert "Reviewpack config must be a YAML mapping" in str(error)
    else:
        raise AssertionError("Expected ValueError for non-mapping config YAML")


def test_example_config_exists() -> None:
    example_config = Path("examples/.reviewpack.yml")

    assert example_config.exists()
