from __future__ import annotations

from dataclasses import dataclass

from reviewpack.models import FileCategory, ReviewpackResult, RiskLevel


@dataclass(frozen=True)
class ReleaseNoteHint:
    """A deterministic hint for maintainers preparing release notes."""

    category: str
    title: str
    message: str


def generate_release_note_hints(result: ReviewpackResult) -> list[ReleaseNoteHint]:
    """Generate deterministic release note hints from a Reviewpack result.

    These hints are not final release notes. They are maintainer-facing prompts
    to help decide whether a pull request should be mentioned in release notes.
    """

    categories = {changed_file.category for changed_file in result.changed_files}
    hints: list[ReleaseNoteHint] = []

    if FileCategory.SOURCE in categories:
        hints.append(
            ReleaseNoteHint(
                category="Changed",
                title="Source files changed",
                message="Consider whether this PR changes user-visible behavior or public APIs.",
            )
        )

    if FileCategory.DEPENDENCY in categories:
        hints.append(
            ReleaseNoteHint(
                category="Dependencies",
                title="Dependency files changed",
                message="Check whether dependency updates affect compatibility, security, or installation.",
            )
        )

    if FileCategory.CI in categories:
        hints.append(
            ReleaseNoteHint(
                category="CI",
                title="CI workflow changed",
                message="Review whether CI behavior, required checks, or release automation changed.",
            )
        )

    if FileCategory.INFRA in categories:
        hints.append(
            ReleaseNoteHint(
                category="Infrastructure",
                title="Infrastructure files changed",
                message="Check whether deployment, runtime, or environment behavior should be mentioned.",
            )
        )

    if FileCategory.DOCS in categories:
        hints.append(
            ReleaseNoteHint(
                category="Documentation",
                title="Documentation changed",
                message="Confirm whether documentation updates should be referenced in release notes.",
            )
        )

    if FileCategory.TEST in categories and FileCategory.SOURCE not in categories:
        hints.append(
            ReleaseNoteHint(
                category="Tests",
                title="Test-only change",
                message="This may not need user-facing release notes unless it affects quality or reliability.",
            )
        )

    high_risk_signals = [signal for signal in result.risk_signals if signal.level == RiskLevel.HIGH]
    if high_risk_signals:
        hints.append(
            ReleaseNoteHint(
                category="Risk",
                title="High-risk area changed",
                message="Consider whether users need migration notes, compatibility notes, or upgrade guidance.",
            )
        )

    if not hints:
        hints.append(
            ReleaseNoteHint(
                category="Review",
                title="No obvious release note category detected",
                message="Review the PR manually to decide whether a changelog entry is needed.",
            )
        )

    return hints


def render_release_note_hints(result: ReviewpackResult) -> str:
    """Render release note hints as Markdown."""

    hints = generate_release_note_hints(result)
    lines: list[str] = []

    lines.append("# Release Note Hints")
    lines.append("")
    lines.append("This file contains deterministic hints for maintainers preparing release notes.")
    lines.append("")
    lines.append("These hints are not final release notes.")
    lines.append("They are intended to help maintainers decide whether a PR should be mentioned in a release.")
    lines.append("")
    lines.append("## Pull Request")
    lines.append("")
    lines.append(f"- Title: {result.pr.title}")
    lines.append(f"- Author: {result.pr.author}")

    if result.pr.url:
        lines.append(f"- URL: {result.pr.url}")

    lines.append("")
    lines.append("## Possible Release Categories")
    lines.append("")

    for hint in hints:
        lines.append(f"### {hint.category}: {hint.title}")
        lines.append("")
        lines.append(hint.message)
        lines.append("")

    lines.append("## Maintainer Checklist")
    lines.append("")
    lines.append("- Confirm whether this PR needs a changelog entry.")
    lines.append("- Check whether behavior changes are user-visible.")
    lines.append("- Check whether dependency changes affect compatibility or security.")
    lines.append("- Confirm whether docs and examples match the implementation.")
    lines.append("- Decide whether migration notes or upgrade notes are needed.")
    lines.append("")
    lines.append("## Privacy Notes")
    lines.append("")
    lines.append("- This file was generated from local Reviewpack analysis results.")
    lines.append("- AI was not used to generate these hints.")
    lines.append("- Raw diffs and full source code are not required for this output.")
    lines.append("")

    return "\n".join(lines)
