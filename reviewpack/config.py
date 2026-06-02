from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import BaseModel, Field


class PrivacyConfig(BaseModel):
    """Privacy controls for Reviewpack.

    Reviewpack is local-first and privacy-first by default.

    These defaults intentionally avoid sending branch names, commit messages,
    raw diffs, or local environment information to any external service.
    """

    include_branch_name: bool = False
    include_commit_messages: bool = False
    include_diff_snippets: bool = False
    include_file_paths: bool = True
    redact_secrets: bool = True


class AIConfig(BaseModel):
    """Optional AI configuration.

    AI is disabled by default. v0.1.0 does not call AI providers.
    These fields reserve a stable configuration shape for future versions.
    """

    enabled: bool = False
    provider: str | None = None
    model: str | None = None
    max_input_chars: int = 12000


class LargePRConfig(BaseModel):
    """Thresholds for large pull request detection."""

    changed_files: int = 20
    changed_lines: int = 800


class ReviewpackConfig(BaseModel):
    """Project-level Reviewpack configuration."""

    risk_paths_high: list[str] = Field(
        default_factory=lambda: [
            "src/auth/**",
            "src/security/**",
            "src/payment/**",
        ]
    )
    test_paths: list[str] = Field(
        default_factory=lambda: [
            "tests/**",
            "__tests__/**",
            "test/**",
        ]
    )
    docs_paths: list[str] = Field(
        default_factory=lambda: [
            "README.md",
            "docs/**",
        ]
    )
    large_pr: LargePRConfig = Field(default_factory=LargePRConfig)
    privacy: PrivacyConfig = Field(default_factory=PrivacyConfig)
    ai: AIConfig = Field(default_factory=AIConfig)


def load_config(path: str | Path | None = None) -> ReviewpackConfig:
    """Load Reviewpack configuration.

    If no path is provided, the default configuration is returned.
    If the file does not exist, the default configuration is returned.

    The first public version keeps configuration loading intentionally simple.
    """

    if path is None:
        return ReviewpackConfig()

    config_path = Path(path)

    if not config_path.exists():
        return ReviewpackConfig()

    data = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    return ReviewpackConfig.model_validate(data)
