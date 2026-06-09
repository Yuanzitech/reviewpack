from __future__ import annotations

from dataclasses import dataclass

from reviewpack.models import FileCategory, ReviewpackResult, RiskLevel


@dataclass(frozen=True)
class ReleaseNoteHint:
    """A deterministic release note hint."""

    category: str
    title: str
    reason: str
    suggested_action: str


def generate_release_note_hints(result: ReviewpackResult) -> list[ReleaseNoteHint]:
    """Generate deterministic release note hints from a Reviewpack result."""

    categories = {changed_file.category for changed_file in result.changed_files}
    hints: list[ReleaseNoteHint] = []

    if FileCategory.SOURCE in categories:
        hints.append(
            ReleaseNoteHint(
                category="Changed",
                title="Source behavior may have changed",
                reason="Source files were changed.",
                suggested_action=(
                    "Decide whether this change affects users, maintainers, APIs, CLI behavior, "
                    "or runtime behavior."
                ),
            )
        )

    if FileCategory.DEPENDENCY in categories:
        hints.append(
            ReleaseNoteHint(
                category="Dependencies",
                title="Dependency metadata changed",
                reason="Dependency files were changed.",
                suggested_action=(
                    "Review whether dependency changes should be mentioned in release notes, "
                    "migration notes, or compatibility notes."
                ),
            )
        )

    if FileCategory.CI in categories:
        hints.append(
            ReleaseNoteHint(
                category="CI",
                title="CI workflow changed",
                reason="CI workflow files were changed.",
                suggested_action=(
                    "Mention this only if it affects contributors, maintainers, release behavior, "
                    "or required checks."
                ),
            )
        )

    if FileCategory.DOCS in categories:
        hints.append(
            ReleaseNoteHint(
                category="Documentation",
                title="Documentation changed",
                reason="Documentation files were changed.",
                suggested_action="Mention this if the documentation update is user-facing or release-relevant.",
            )
        )

    if FileCategory.CONFIG in categories:
        hints.append(
            ReleaseNoteHint(
                category="Configuration",
                title="Configuration changed",
                reason="Configuration files were changed.",
                suggested_action=(
                    "Check whether tool behavior, contributor workflow, or project defaults changed."
                ),
            )
        )

    if FileCategory.INFRA in categories:
        hints.append(
            ReleaseNoteHint(
                category="Infrastructure",
                title="Infrastructure changed",
                reason="Infrastructure files were changed.",
                suggested_action="Mention this if deployment, runtime, or environment behavior changed.",
            )
        )

    if any(signal.level == RiskLevel.HIGH for signal in result.risk_signals):
        hints.append(
            ReleaseNoteHint(
                category="Risk",
                title="High-risk changes detected",
                reason="Reviewpack detected one or more high-risk signals.",
                suggested_action=(
                    "Confirm whether release notes, upgrade notes, or maintainer notes should call out "
                    "the risk area."
                ),
            )
        )

    return hints


def render_release_note_hints(result: ReviewpackResult) -> str:
    """Render release note hints as Markdown."""

    hints = generate_release_note_hints(result)
    lines: list[str] = []

    lines.append("# Release Note Hints")
    lines.append("")
    lines.append("These hints help maintainers decide whether a PR should be mentioned in release notes.")
    lines.append("")
    lines.append("Reviewpack does not generate final release notes automatically.")
    lines.append("")

    if not hints:
        lines.append("No release-note-relevant signals were detected.")
        lines.append("")
        lines.append("Maintainers should still decide whether this PR has user-facing impact.")
        lines.append("")
        return "\n".join(lines)

    lines.append("## Summary")
    lines.append("")
    lines.append("Review the categories below and decide whether the PR needs a release note entry.")
    lines.append("")

    for hint in hints:
        lines.append(f"## {hint.category}: {hint.title}")
        lines.append("")
        lines.append(f"Why this might matter: {hint.reason}")
        lines.append("")
        lines.append(f"Suggested maintainer action: {hint.suggested_action}")
        lines.append("")

    lines.append("## Suggested Decision Questions")
    lines.append("")
    lines.append("- Is this change visible to users?")
    lines.append("- Does this change affect installation, configuration, CI, or release behavior?")
    lines.append("- Does this change affect APIs, CLI commands, output files, or compatibility?")
    lines.append("- Should this be documented as Added, Changed, Fixed, Deprecated, or Removed?")
    lines.append("")

    return "\n".join(lines)
