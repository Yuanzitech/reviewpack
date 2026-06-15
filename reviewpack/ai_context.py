from __future__ import annotations

from pathlib import Path

from reviewpack.models import PullRequestInfo, ReviewpackResult
from reviewpack.release_notes import render_release_note_hints
from reviewpack.reviewer_checklist import render_reviewer_checklist


def render_optional_pr_metadata(pr: PullRequestInfo) -> list[str]:
    """Render optional pull request metadata lines for AI context."""

    lines: list[str] = []

    if pr.state:
        lines.append(f"- State: {pr.state}")

    if pr.is_draft is not None:
        lines.append(f"- Draft: {str(pr.is_draft).lower()}")

    if pr.base_branch:
        lines.append(f"- Base branch: {pr.base_branch}")

    if pr.head_branch:
        lines.append(f"- Head branch: {pr.head_branch}")

    if pr.commit_count is not None:
        lines.append(f"- Commits: {pr.commit_count}")

    if pr.labels:
        lines.append(f"- Labels: {', '.join(pr.labels)}")

    return lines


def render_ai_context(result: ReviewpackResult) -> str:
    """Render a single-file AI context bundle.

    This file is useful when an AI assistant cannot read multiple workspace
    files but can accept one uploaded or pasted Markdown file.
    """

    lines: list[str] = []

    lines.append("# Reviewpack AI Context")
    lines.append("")
    lines.append("This file combines the most useful Reviewpack context into a single Markdown file.")
    lines.append("")
    lines.append("Use this file when an AI assistant cannot read the full `.reviewpack/` directory.")
    lines.append("")
    lines.append("## Review Objective")
    lines.append("")
    lines.append("Help a human maintainer review this pull request.")
    lines.append("")
    lines.append("Focus on:")
    lines.append("")
    lines.append("- Correctness")
    lines.append("- Missing or weak tests")
    lines.append("- Compatibility")
    lines.append("- Security-sensitive changes")
    lines.append("- Documentation and release-note impact")
    lines.append("- Maintainer questions before merge")
    lines.append("")
    lines.append("## Known Limitations")
    lines.append("")
    lines.append("- Reviewpack output is context, not ground truth.")
    lines.append("- Do not assume hidden code or files that are not included.")
    lines.append("- Do not claim that raw source code was inspected unless source code was provided separately.")
    lines.append("- Treat this file as review context for a human maintainer to verify.")
    lines.append("- Prefer concrete, actionable feedback.")
    lines.append("")
    lines.append("## Pull Request")
    lines.append("")
    lines.append(f"- Title: {result.pr.title}")
    lines.append(f"- Author: {result.pr.author}")

    if result.pr.url:
        lines.append(f"- URL: {result.pr.url}")

    optional_metadata = render_optional_pr_metadata(result.pr)
    if optional_metadata:
        lines.extend(optional_metadata)

    if result.pr.description:
        lines.append("")
        lines.append("## Description")
        lines.append("")
        lines.append(result.pr.description.strip())

    lines.append("")
    lines.append("## Change Statistics")
    lines.append("")
    lines.append(f"- Files changed: {result.stats.files_changed}")
    lines.append(f"- Lines added: {result.stats.additions}")
    lines.append(f"- Lines deleted: {result.stats.deletions}")
    lines.append(f"- Source files: {result.stats.source_files}")
    lines.append(f"- Test files: {result.stats.test_files}")
    lines.append(f"- Documentation files: {result.stats.docs_files}")
    lines.append(f"- Dependency files: {result.stats.dependency_files}")
    lines.append(f"- CI files: {result.stats.ci_files}")
    lines.append(f"- Config files: {result.stats.config_files}")
    lines.append(f"- Infrastructure files: {result.stats.infra_files}")
    lines.append(f"- Unknown files: {result.stats.unknown_files}")

    lines.append("")
    lines.append("## Changed Files")
    lines.append("")

    for changed_file in result.changed_files:
        status = f"{changed_file.status}, " if changed_file.status else ""
        lines.append(
            f"- {changed_file.path} "
            f"({status}{changed_file.category.value}, +{changed_file.additions}/-{changed_file.deletions})"
        )

    lines.append("")
    lines.append("## Risk Signals")
    lines.append("")

    if result.risk_signals:
        for signal in result.risk_signals:
            lines.append(f"### {signal.level.value}: {signal.title}")
            lines.append("")
            lines.append(signal.message)
            lines.append("")

            if signal.files:
                lines.append("Affected files:")
                lines.append("")
                for file_path in signal.files:
                    lines.append(f"- {file_path}")
                lines.append("")
    else:
        lines.append("No deterministic risk signals were detected.")
        lines.append("")

    lines.append("## Suggested Review Focus")
    lines.append("")

    for item in result.review_focus:
        lines.append(f"- {item.title}")
        lines.append(f"  - {item.reason}")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(render_reviewer_checklist(result).strip())

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(render_release_note_hints(result).strip())

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Requested AI Review Output")
    lines.append("")
    lines.append("Please provide:")
    lines.append("")
    lines.append("1. A short summary of the change.")
    lines.append("2. The top risks to review.")
    lines.append("3. Missing or weak test coverage, if any.")
    lines.append("4. Documentation or release-note concerns, if any.")
    lines.append("5. Specific questions the maintainer should ask before merging.")
    lines.append("")
    lines.append("## Privacy Notes")
    lines.append("")
    lines.append("- Reviewpack does not call an AI provider by default.")
    lines.append("- Reviewpack does not upload raw diffs or full source code by default.")
    lines.append("- GitHub mode may include PR metadata such as labels, branch names, commit count, and file status.")
    lines.append("- The user remains in control of what is shared with AI tools.")
    lines.append("")

    return "\n".join(lines)


def write_ai_context(result: ReviewpackResult, output_dir: str | Path) -> Path:
    """Write the single-file AI context bundle to an output directory."""

    target_dir = Path(output_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    output_path = target_dir / "ai-context.md"
    output_path.write_text(render_ai_context(result), encoding="utf-8")

    return output_path
