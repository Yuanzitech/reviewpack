from pathlib import Path

from reviewpack.config import ReviewpackConfig, load_config


EXAMPLE_CONFIG_FILES = {
    "examples/.reviewpack.yml",
    "examples/config/minimal.reviewpack.yml",
    "examples/config/python-project.reviewpack.yml",
    "examples/config/javascript-typescript-project.reviewpack.yml",
    "examples/config/monorepo.reviewpack.yml",
}


def test_example_config_files_exist() -> None:
    for config_path in sorted(EXAMPLE_CONFIG_FILES):
        assert Path(config_path).exists(), f"Missing example config: {config_path}"


def test_example_config_files_load_successfully() -> None:
    for config_path in sorted(EXAMPLE_CONFIG_FILES):
        config = load_config(config_path)

        assert isinstance(config, ReviewpackConfig)


def test_example_config_files_use_public_json_output_key() -> None:
    for config_path in sorted(EXAMPLE_CONFIG_FILES):
        text = Path(config_path).read_text(encoding="utf-8")

        assert "json:" in text
        assert "json_output:" not in text


def test_example_config_files_define_expected_top_level_sections() -> None:
    for config_path in sorted(EXAMPLE_CONFIG_FILES):
        config = load_config(config_path)

        assert config.outputs is not None
        assert config.risk is not None
        assert config.paths is not None


def test_example_config_files_define_path_categories() -> None:
    for config_path in sorted(EXAMPLE_CONFIG_FILES):
        config = load_config(config_path)

        assert config.paths.docs
        assert config.paths.tests
        assert config.paths.dependencies
        assert config.paths.ci
        assert config.paths.config
        assert config.paths.infrastructure


def test_example_config_files_define_risk_thresholds() -> None:
    for config_path in sorted(EXAMPLE_CONFIG_FILES):
        config = load_config(config_path)

        assert config.risk.large_pr_files > 0
        assert config.risk.large_pr_lines > 0
        assert config.risk.high_risk_paths


def test_configuration_docs_mention_example_config_files() -> None:
    docs = Path("docs/configuration.md").read_text(encoding="utf-8")

    assert "examples/config/minimal.reviewpack.yml" in docs
    assert "examples/config/python-project.reviewpack.yml" in docs
    assert "examples/config/javascript-typescript-project.reviewpack.yml" in docs
    assert "examples/config/monorepo.reviewpack.yml" in docs


def test_config_schema_docs_mention_example_config_files() -> None:
    docs = Path("docs/config-schema.md").read_text(encoding="utf-8")

    assert "examples/config/minimal.reviewpack.yml" in docs
    assert "examples/config/python-project.reviewpack.yml" in docs
    assert "examples/config/javascript-typescript-project.reviewpack.yml" in docs
    assert "examples/config/monorepo.reviewpack.yml" in docs


def test_config_schema_docs_mention_invalid_config_guidance() -> None:
    docs = Path("docs/config-schema.md").read_text(encoding="utf-8")

    assert "Invalid configuration guidance" in docs
    assert "YAML mappings" in docs
    assert "Unknown keys" in docs
