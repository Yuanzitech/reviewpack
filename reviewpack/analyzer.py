from __future__ import annotations

from collections import Counter

from reviewpack.config import ReviewpackConfig
from reviewpack.models import (
    ChangeStats,
    ChangedFile,
    FileCategory,
    ReviewFocusItem,
    ReviewpackInput,
    ReviewpackResult,
)
from reviewpack.rules import categorize_file, generate_risk_signals


def categorize_changed_files(
    files: list[ChangedFile],
    config: ReviewpackConfig | None = None,
) -> list[ChangedFile]:
    """Return changed files with file categories populated."""

    active_config = config or ReviewpackConfig()
    categorized: list[ChangedFile] = []

    for changed_file in files:
        categorized.append(
            changed_file.model_copy(
                update={
                    "category": categorize_file(changed_file.path, active_config),
                }
            )
        )

    return categorized


def calculate_stats(files: list[ChangedFile]) -> ChangeStats:
    """Calculate aggregate change statistics."""

    category_counts = Counter(item.category for item in files)

    return ChangeStats(
        files_changed=len(files),
        additions=sum(item.additions for item in files),
        deletions=sum(item.deletions for item in files),
        source_files=category_counts[FileCategory.SOURCE],
        test_files=category_counts[FileCategory.TEST],
        docs_files=category_counts[FileCategory.DOCS],
        dependency_files=category_counts[FileCategory.DEPENDENCY],
        ci_files=category_counts[FileCategory.CI],
        config_files=category_counts[FileCategory.CONFIG],
        infra_files=category_counts[FileCategory.INFRA],
        unknown_files=category_counts[FileCategory.UNKNOWN],
    )


def generate_review_focus(result_files: list[ChangedFile]) -> list[ReviewFocusItem]:
    """Generate suggested review focus areas from file categories."""

    categories = {item.category for item in result_files}
    focus: list[ReviewFocusItem] = []

    if FileCategory.SOURCE in categories:
        focus.append(
            ReviewFocusItem(
                title="Validate behavior changes",
                reason="Source files changed. Review correctness, edge cases, and backward compatibility.",
            )
        )

    if FileCategory.TEST not in categories and FileCategory.SOURCE in categories:
        focus.append(
            ReviewFocusItem(
                title="Check test coverage",
                reason="Source files changed without test updates. Confirm whether existing tests are sufficient.",
            )
        )

    if FileCategory.DEPENDENCY in categories:
        focus.append(
            ReviewFocusItem(
                title="Review dependency impact",
                reason="Dependency files changed. Check version compatibility, security, and lockfile consistency.",
            )
        )

    if FileCategory.CI in categories:
        focus.append(
            ReviewFocusItem(
                title="Review CI behavior",
                reason="CI configuration changed. Check triggers, permissions, secrets, and required checks.",
            )
        )

    if FileCategory.INFRA in categories:
        focus.append(
            ReviewFocusItem(
                title="Review deployment impact",
                reason="Infrastructure files changed. Check deployment, runtime, and environment behavior.",
            )
        )

    if FileCategory.DOCS in categories:
        focus.append(
            ReviewFocusItem(
                title="Verify documentation accuracy",
                reason="Documentation changed. Confirm examples and usage notes match the implementation.",
            )
        )

    if not focus:
        focus.append(
            ReviewFocusItem(
                title="Review changed files",
                reason="No specific category-based focus was detected. Review the changed files manually.",
            )
        )

    return focus


def analyze_reviewpack_input(
    reviewpack_input: ReviewpackInput,
    config: ReviewpackConfig | None = None,
) -> ReviewpackResult:
    """Analyze Reviewpack input and return a structured result."""

    active_config = config or ReviewpackConfig()
    categorized_files = categorize_changed_files(reviewpack_input.changed_files, active_config)
    stats = calculate_stats(categorized_files)
    risk_signals = generate_risk_signals(categorized_files, active_config)
    review_focus = generate_review_focus(categorized_files)

    return ReviewpackResult(
        pr=reviewpack_input.pr,
        changed_files=categorized_files,
        stats=stats,
        risk_signals=risk_signals,
        review_focus=review_focus,
        metadata={
            "reviewpack_version": "0.1.0",
            "mode": "fixture",
            "network_used": False,
            "ai_used": False,
        },
    )
