from __future__ import annotations

from dataclasses import dataclass

from reviewpack.models import FileCategory, ReviewpackResult, RiskLevel


@dataclass(frozen=True)
class ReviewerChecklistItem:
    """A deterministic checklist item for pull request reviewers."""

    section: str
    text: str
    reason: str


def generate_reviewer_checklist_items(result: ReviewpackResult) -> list[ReviewerChecklistItem]:
    """Generate maintainer-facing checklist items from a Reviewpack result."""

    categories = {changed_file.category for changed_file in result.changed_files}
    items: list[ReviewerChecklistItem] = []

    if FileCategory.SOURCE in categories:
        items.append(
            ReviewerChecklistItem(
                section="Core Review",
                text="Review behavior changes and edge cases.",
                reason="Source files changed.",
            )
        )
        items.append(
            ReviewerChecklistItem(
                section="Compatibility",
                text="Check backward compatibility and public API impact.",
                reason="Source changes may affect existing users or integrations.",
            )
        )

    if FileCategory.SOURCE in categories and FileCategory.TEST not in categories:
        items.append(
            ReviewerChecklistItem(
                section="Tests",
                text="Confirm whether test coverage is sufficient.",
                reason="Source files changed without test file updates.",
            )
        )

    if FileCategory.TEST in categories:
        items.append(
            ReviewerChecklistItem(
                section="Tests",
                text="Review whether test changes match the intended behavior.",
                reason="Test files changed.",
            )
        )

    if FileCategory.DOCS in categories:
        items.append(
            ReviewerChecklistItem(
                section="Documentation",
                text="Confirm documentation and examples match the implementation.",
                reason="Documentation files changed.",
            )
        )

    if FileCategory.SOURCE in categories and FileCategory.DOCS not in categories:
        items.append(
            ReviewerChecklistItem(
                section="Documentation",
                text="Decide whether documentation updates are needed.",
                reason="Source files changed without documentation updates.",
            )
        )

    if FileCategory.DEPENDENCY in categories:
        items.append(
            ReviewerChecklistItem(
                section="Dependencies",
                text="Review dependency compatibility, security, and lockfile consistency.",
                reason="Dependency files changed.",
            )
        )

    if FileCategory.CI in categories:
        items.append(
            ReviewerChecklistItem(
                section="CI",
                text="Review workflow triggers, permissions, secrets usage, and required checks.",
                reason="CI configuration changed.",
            )
        )

    if FileCategory.INFRA in categories:
        items.append(
            ReviewerChecklistItem(
                section="Infrastructure",
                text="Check deployment, runtime, and environment impact.",
                reason="Infrastructure files changed.",
            )
        )

    if result.risk_signals:
        items.append(
            ReviewerChecklistItem(
                section="Risk",
                text="Review all risk signals before merging.",
                reason="Reviewpack detected deterministic risk signals.",
            )
        )

    if any(signal.level == RiskLevel.HIGH for signal in result.risk_signals):
        items.append(
            ReviewerChecklistItem(
                section="Risk",
                text="Pay extra attention to high-risk areas and upgrade impact.",
                reason="At least one high-risk signal was detected.",
            )
        )

    items.append(
        ReviewerChecklistItem(
            section="Release",
            text="Decide whether this PR needs a changelog or release note entry.",
            reason="Maintainers should explicitly decide release note impact.",
        )
    )

    items.append(
        ReviewerChecklistItem(
            section="Privacy",
            text="Confirm generated outputs do not include secrets or sensitive project data.",
            reason="Review artifacts may be shared with maintainers or AI tools.",
        )
    )

    if not items:
        items.append(
            ReviewerChecklistItem(
                section="Review",
                text="Review the changed files manually.",
                reason="No category-specific checklist items were detected.",
            )
        )

    return items


def render_reviewer_checklist(result: ReviewpackResult) -> str:
    """Render reviewer checklist as Markdown."""

    items = generate_reviewer_checklist_items(result)
    lines: list[str] = []

    lines.append("# Reviewer Checklist")
    lines.append("")
    lines.append("This checklist is generated from deterministic Reviewpack analysis.")
    lines.append("")
    lines.append("It is intended to help maintainers review pull requests more consistently.")
    lines.append("")
    lines.append("## Pull Request")
    lines.append("")
    lines.append(f"- Title: {result.pr.title}")
    lines.append(f"- Author: {result.pr.author}")

    if result.pr.url:
        lines.append(f"- URL: {result.pr.url}")

    lines.append("")
    lines.append("## Checklist")
    lines.append("")

    grouped: dict[str, list[ReviewerChecklistItem]] = {}

    for item in items:
        grouped.setdefault(item.section, []).append(item)

    for section, section_items in grouped.items():
        lines.append(f"### {section}")
        lines.append("")

        for item in section_items:
            lines.append(f"- [ ] {item.text}")
            lines.append(f"  - Reason: {item.reason}")

        lines.append("")

    lines.append("## Notes")
    lines.append("")
    lines.append("- This checklist does not replace human judgment.")
    lines.append("- AI was not used to generate this checklist.")
    lines.append("- Raw diffs and full source code are not required for this output.")
    lines.append("- Maintainers should adapt the checklist to the project context.")
    lines.append("")

    return "\n".join(lines)
