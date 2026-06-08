from __future__ import annotations

from fnmatch import fnmatch

from reviewpack.config import ReviewpackConfig
from reviewpack.models import (
    ChangeStats,
    ChangedFile,
    FileCategory,
    ReviewFocusItem,
    RiskLevel,
    RiskSignal,
)


def matches_path_pattern(file_path: str, pattern: str) -> bool:
    """Return whether a file path matches a configured pattern.

    Supported pattern styles:
    - Directory prefix: docs/
    - Exact file name: pyproject.toml
    - Glob: **/*.md or src/**/*.py
    """

    normalized_path = file_path.replace("\\", "/")
    normalized_pattern = pattern.replace("\\", "/")

    if not normalized_pattern:
        return False

    if "*" in normalized_pattern:
        return fnmatch(normalized_path, normalized_pattern)

    if normalized_pattern.endswith("/"):
        return normalized_path.startswith(normalized_pattern)

    return normalized_path == normalized_pattern or normalized_path.startswith(f"{normalized_pattern}/")


def matches_any_pattern(file_path: str, patterns: list[str]) -> bool:
    """Return whether a file path matches any configured pattern."""

    return any(matches_path_pattern(file_path, pattern) for pattern in patterns)


def categorize_file(path: str, config: ReviewpackConfig | None = None) -> FileCategory:
    """Categorize a changed file path."""

    reviewpack_config = config or ReviewpackConfig()
    normalized_path = path.replace("\\", "/")
    lower_path = normalized_path.lower()

    if matches_any_pattern(normalized_path, reviewpack_config.paths.tests):
        return FileCategory.TEST

    if matches_any_pattern(normalized_path, reviewpack_config.paths.docs):
        return FileCategory.DOCS

    if matches_any_pattern(normalized_path, reviewpack_config.paths.dependencies):
        return FileCategory.DEPENDENCY

    if matches_any_pattern(normalized_path, reviewpack_config.paths.ci):
        return FileCategory.CI

    if matches_any_pattern(normalized_path, reviewpack_config.paths.infrastructure):
        return FileCategory.INFRA

    if matches_any_pattern(normalized_path, reviewpack_config.paths.config):
        return FileCategory.CONFIG

    if lower_path.endswith((".py", ".js", ".ts", ".tsx", ".jsx", ".go", ".rs", ".java", ".kt", ".rb", ".php")):
        return FileCategory.SOURCE

    return FileCategory.UNKNOWN


def classify_changed_files(
    changed_files: list[ChangedFile],
    config: ReviewpackConfig | None = None,
) -> list[ChangedFile]:
    """Return changed files with categories assigned from configured rules."""

    reviewpack_config = config or ReviewpackConfig()
    classified_files: list[ChangedFile] = []

    for changed_file in changed_files:
        category = changed_file.category

        if category == FileCategory.UNKNOWN:
            category = categorize_file(changed_file.path, reviewpack_config)

        classified_files.append(
            ChangedFile(
                path=changed_file.path,
                additions=changed_file.additions,
                deletions=changed_file.deletions,
                category=category,
            )
        )

    return classified_files


def compute_change_stats(changed_files: list[ChangedFile]) -> ChangeStats:
    """Compute aggregate change statistics."""

    stats = ChangeStats(
        files_changed=len(changed_files),
        additions=sum(file.additions for file in changed_files),
        deletions=sum(file.deletions for file in changed_files),
    )

    for changed_file in changed_files:
        if changed_file.category == FileCategory.SOURCE:
            stats.source_files += 1
        elif changed_file.category == FileCategory.TEST:
            stats.test_files += 1
        elif changed_file.category == FileCategory.DOCS:
            stats.docs_files += 1
        elif changed_file.category == FileCategory.DEPENDENCY:
            stats.dependency_files += 1
        elif changed_file.category == FileCategory.CI:
            stats.ci_files += 1
        elif changed_file.category == FileCategory.CONFIG:
            stats.config_files += 1
        elif changed_file.category == FileCategory.INFRA:
            stats.infra_files += 1
        else:
            stats.unknown_files += 1

    return stats


def detect_risk_signals(
    changed_files: list[ChangedFile],
    stats: ChangeStats,
    config: ReviewpackConfig | None = None,
) -> list[RiskSignal]:
    """Detect deterministic risk signals from changed files and stats."""

    reviewpack_config = config or ReviewpackConfig()
    signals: list[RiskSignal] = []

    total_lines_changed = stats.additions + stats.deletions

    if stats.files_changed >= reviewpack_config.risk.large_pr_files:
        signals.append(
            RiskSignal(
                level=RiskLevel.HIGH,
                title="Large pull request",
                message=(
                    f"This PR changes {stats.files_changed} files. "
                    "Consider whether it should be split into smaller reviewable changes."
                ),
                files=[changed_file.path for changed_file in changed_files],
            )
        )

    if total_lines_changed >= reviewpack_config.risk.large_pr_lines:
        signals.append(
            RiskSignal(
                level=RiskLevel.HIGH,
                title="Large line change",
                message=(
                    f"This PR changes {total_lines_changed} lines. "
                    "Reviewers should focus on behavior, compatibility, and test coverage."
                ),
                files=[changed_file.path for changed_file in changed_files],
            )
        )

    dependency_files = [file.path for file in changed_files if file.category == FileCategory.DEPENDENCY]
    if dependency_files:
        signals.append(
            RiskSignal(
                level=RiskLevel.MEDIUM,
                title="Dependency files changed",
                message="Dependency changes can affect installation, compatibility, and security.",
                files=dependency_files,
            )
        )

    ci_files = [file.path for file in changed_files if file.category == FileCategory.CI]
    if ci_files:
        signals.append(
            RiskSignal(
                level=RiskLevel.MEDIUM,
                title="CI workflow changed",
                message="CI changes can affect required checks, automation, or release behavior.",
                files=ci_files,
            )
        )

    infra_files = [file.path for file in changed_files if file.category == FileCategory.INFRA]
    if infra_files:
        signals.append(
            RiskSignal(
                level=RiskLevel.MEDIUM,
                title="Infrastructure files changed",
                message="Infrastructure changes can affect deployment, runtime, or environment behavior.",
                files=infra_files,
            )
        )

    source_files = [file.path for file in changed_files if file.category == FileCategory.SOURCE]
    test_files = [file.path for file in changed_files if file.category == FileCategory.TEST]

    if source_files and not test_files:
        signals.append(
            RiskSignal(
                level=RiskLevel.MEDIUM,
                title="Source changed without tests",
                message="Source files changed, but no test files were detected.",
                files=source_files,
            )
        )

    high_risk_files = [
        changed_file.path
        for changed_file in changed_files
        if matches_any_pattern(changed_file.path, reviewpack_config.risk.high_risk_paths)
    ]
    if high_risk_files:
        signals.append(
            RiskSignal(
                level=RiskLevel.HIGH,
                title="High-risk area changed",
                message="This PR changes paths configured as high risk in Reviewpack configuration.",
                files=high_risk_files,
            )
        )

    return signals


def suggest_review_focus(
    changed_files: list[ChangedFile],
    risk_signals: list[RiskSignal],
) -> list[ReviewFocusItem]:
    """Suggest high-level review focus items."""

    categories = {changed_file.category for changed_file in changed_files}
    focus_items: list[ReviewFocusItem] = []

    if FileCategory.SOURCE in categories:
        focus_items.append(
            ReviewFocusItem(
                title="Review behavior changes",
                reason="Source files changed.",
            )
        )

    if FileCategory.TEST not in categories and FileCategory.SOURCE in categories:
        focus_items.append(
            ReviewFocusItem(
                title="Check test coverage",
                reason="Source files changed without detected test updates.",
            )
        )

    if FileCategory.DOCS in categories:
        focus_items.append(
            ReviewFocusItem(
                title="Check documentation accuracy",
                reason="Documentation files changed.",
            )
        )

    if FileCategory.DEPENDENCY in categories:
        focus_items.append(
            ReviewFocusItem(
                title="Review dependency impact",
                reason="Dependency files changed.",
            )
        )

    if FileCategory.CI in categories:
        focus_items.append(
            ReviewFocusItem(
                title="Review CI behavior",
                reason="CI workflow files changed.",
            )
        )

    if FileCategory.INFRA in categories:
        focus_items.append(
            ReviewFocusItem(
                title="Review infrastructure impact",
                reason="Infrastructure files changed.",
            )
        )

    if risk_signals:
        focus_items.append(
            ReviewFocusItem(
                title="Review detected risk signals",
                reason="Reviewpack detected deterministic risk signals.",
            )
        )

    if not focus_items:
        focus_items.append(
            ReviewFocusItem(
                title="Review changed files",
                reason="No specific category-based focus area was detected.",
            )
        )

    return focus_items
