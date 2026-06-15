from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class FileCategory(str, Enum):
    """High-level category for a changed file."""

    SOURCE = "source"
    TEST = "test"
    DOCS = "docs"
    DEPENDENCY = "dependency"
    CI = "ci"
    CONFIG = "config"
    INFRA = "infrastructure"
    UNKNOWN = "unknown"


class RiskLevel(str, Enum):
    """Risk signal level."""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class PullRequestInfo(BaseModel):
    """Pull request metadata used by Reviewpack."""

    title: str
    author: str
    url: str | None = None
    description: str | None = None

    state: str | None = None
    is_draft: bool | None = None
    base_branch: str | None = None
    head_branch: str | None = None
    commit_count: int | None = None
    labels: list[str] = Field(default_factory=list)


class ChangedFile(BaseModel):
    """Changed file metadata used by Reviewpack."""

    path: str
    additions: int = 0
    deletions: int = 0
    category: FileCategory = FileCategory.UNKNOWN
    status: str | None = None


class ReviewpackInput(BaseModel):
    """Input data for Reviewpack analysis."""

    pr: PullRequestInfo
    changed_files: list[ChangedFile]


class ChangeStats(BaseModel):
    """Aggregate change statistics."""

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


class RiskSignal(BaseModel):
    """A deterministic review risk signal."""

    level: RiskLevel
    title: str
    message: str
    files: list[str] = Field(default_factory=list)


class ReviewFocusItem(BaseModel):
    """A suggested focus area for human or AI-assisted review."""

    title: str
    reason: str


class ReviewpackResult(BaseModel):
    """Structured Reviewpack analysis result."""

    pr: PullRequestInfo
    changed_files: list[ChangedFile]
    stats: ChangeStats
    risk_signals: list[RiskSignal] = Field(default_factory=list)
    review_focus: list[ReviewFocusItem] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
