from reviewpack.config import load_config


def test_load_default_config_when_path_is_none() -> None:
    config = load_config()

    assert config.privacy.include_branch_name is False
    assert config.privacy.include_commit_messages is False
    assert config.privacy.include_diff_snippets is False
    assert config.privacy.include_file_paths is True
    assert config.ai.enabled is False
    assert config.large_pr.changed_files == 20
    assert config.large_pr.changed_lines == 800


def test_load_default_config_when_file_is_missing(tmp_path) -> None:
    missing_config = tmp_path / ".reviewpack.yml"

    config = load_config(missing_config)

    assert config.ai.enabled is False
    assert config.privacy.redact_secrets is True
    assert "src/auth/**" in config.risk_paths_high


def test_load_custom_config_from_yaml(tmp_path) -> None:
    config_file = tmp_path / ".reviewpack.yml"
    config_file.write_text(
        "\n".join(
            [
                "risk_paths_high:",
                "  - app/security/**",
                "  - app/billing/**",
                "test_paths:",
                "  - spec/**",
                "docs_paths:",
                "  - handbook/**",
                "large_pr:",
                "  changed_files: 5",
                "  changed_lines: 200",
                "privacy:",
                "  include_branch_name: true",
                "  include_commit_messages: false",
                "  include_diff_snippets: false",
                "  include_file_paths: true",
                "  redact_secrets: true",
                "ai:",
                "  enabled: true",
                "  provider: openai",
                "  model: gpt-4.1-mini",
                "  max_input_chars: 6000",
            ]
        ),
        encoding="utf-8",
    )

    config = load_config(config_file)

    assert config.risk_paths_high == ["app/security/**", "app/billing/**"]
    assert config.test_paths == ["spec/**"]
    assert config.docs_paths == ["handbook/**"]
    assert config.large_pr.changed_files == 5
    assert config.large_pr.changed_lines == 200
    assert config.privacy.include_branch_name is True
    assert config.privacy.include_commit_messages is False
    assert config.privacy.include_diff_snippets is False
    assert config.ai.enabled is True
    assert config.ai.provider == "openai"
    assert config.ai.model == "gpt-4.1-mini"
    assert config.ai.max_input_chars == 6000
