from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import Base generated."""from pydantic import BaseModel, Field

    pr_summary: bool = True
    risk_checklist: bool = True
    reviewer_checklist: bool = True
    release_note_hints: bool = True
    ai_review_prompt: bool = True
    ai_handoff: bool = True
    ai_context: bool = True
    json: bool = True


class RiskConfig(BaseModel):
    """Configure deterministic risk thresholds and high-risk paths."""

    large_pr_files: int = 20
    large_pr_lines: int = 500
    high_risk_paths: list[str] = Field(
        default_factory=lambda: [
            "src/auth/",
            "auth/",
            "security/",
            ".github/workflows/",
            "pyproject.toml",
        ]
    )


class PathConfig(BaseModel):
    """Configure path classification patterns."""

    docs: list[str] = Field(
        default_factory=lambda: [
            "docs/",
            "README.md",
            "README.zh-CN.md",
            "CHANGELOG.md",
        ]
    )
    tests: list[str] = Field(
        default_factory=lambda: [
            "tests/",
            "test/",
        ]
    )
    dependencies: list[str] = Field(
        default_factory=lambda: [
            "pyproject.toml",
            "requirements.txt",
            "requirements-dev.txt",
            "poetry.lock",
            "Pipfile",
            "Pipfile.lock",
            "package.json",
            "package-lock.json",
            "yarn.lock",
            "pnpm-lock.yaml",
        ]
    )
    ci: list[str] = Field(
        default_factory=lambda: [
            ".github/workflows/",
            ".gitlab-ci.yml",
            "azure-pipelines.yml",
            "circle.yml",
        ]
    )
    config: list[str] = Field(
        default_factory=lambda: [
            ".reviewpack.yml",
            "ruff.toml",
            ".ruff.toml",
            "mypy.ini",
            "pytest.ini",
            "tox.ini",
            ".pre-commit-config.yaml",
        ]
    )
    infrastructure: list[str] = Field(
        default_factory=lambda: [
            "Dockerfile",
            "docker-compose.yml",
            "docker-compose.yaml",
            "k8s/",
            "deploy/",
            "infra/",
            "terraform/",
        ]
    )


class ReviewpackConfig(BaseModel):
    """Top-level Reviewpack configuration."""

    outputs: OutputConfig = Field(default_factory=OutputConfig)
    risk: RiskConfig = Field(default_factory=RiskConfig)
    paths: PathConfig = Field(default_factory=PathConfig)


def load_config(config_path: str | Path | None = None) -> ReviewpackConfig:
    """Load Reviewpack configuration from YAML.

    If config_path is None, Reviewpack looks for .reviewpack.yml in the current
    working directory. If no configuration file exists, defaults are used.
    """

    if config_path is None:
        default_path = Path(".reviewpack.yml")
        if not default_path.exists():
            return ReviewpackConfig()
        config_path = default_path

    path = Path(config_path)

    if not path.exists():
        return ReviewpackConfig()

    raw_data = yaml.safe_load(path.read_text(encoding="utf-8"))

    if raw_data is None:
        return ReviewpackConfig()

    if not isinstance(raw_data, dict):
        raise ValueError(f"Reviewpack config must be a YAML mapping: {path}")

    return ReviewpackConfig.model_validate(raw_data)


class OutputConfig(BaseModel):
