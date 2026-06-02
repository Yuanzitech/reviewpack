from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class RiskLevel(str, Enum):
    """Risk level for a review signal."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class FileCategory(str, Enum):
    """High-level file category used by Reviewpack rules."""

    SOURCE = "source"
    TEST = "test"
    DOCS = "docs"
    DEPENDENCY = "dependency"
    CI = "ci"
    CONFIG = "config"
    INFRA = "infra"
    UNKNOWN = "unknown"


class PullRequestInfo(BaseModel):
    """Basic pull request metadata.

    This model intentionally avoids requiring branch names, commit messages,
    local paths, or environment information. Those fields may be sensitive and
    should only be added through explicit opt-in features in future versions.
    """

    title: str
    author: str
    url: str | None = None
    description: str | None = None


class ChangedFile(BaseModel):
    """A file changed by a pull request."""

    path: str
    additions: int = 0
    deletions: int = 0
    patch: str | None = None
    category: FileCategory = FileCategory.UNKNOWN


class RiskSignal(BaseModel):
    """A deterministic review signal produced by Reviewpack."""

    level: RiskLevel
    title: str
    message: str
    files: list[str] = Field(default_factory=list)


class ReviewFocusItem(BaseModel):
    """A suggested focus area for human or AI-assisted review."""

    title: str
    reason: str


class ReviewpackInput(BaseModel):
    """Input data for generating a review context pack.

    v0.1.0 supports fixture-based input. Later versions may add GitHub API,
    local git diff, or other integrations.
    """

    pr: PullRequestInfo
    changed_files: list[ChangedFile]


class ChangeStats(BaseModel):
    """Aggregated change statistics."""

    files_changed: int = 0
    additions: int = 0
    deletions: int = 0
    source_files: int = 0
    test_files: int = 0
    docs_files: int = 0
    dependency_files: int = 0
    ci_files: int = 0
    config_files: int = 0
    infra_files: int = 0
    unknown_files: int = 0


class ReviewpackResult(BaseModel):
    """Structured output produced by Reviewpack analysis."""

    pr: PullRequestInfo
    changed_files: list[ChangedFile]
    stats: ChangeStats
    risk_signals: list[RiskSignal] = Field(default_factory=list)
    review_focus: list[ReviewFocusItem] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
