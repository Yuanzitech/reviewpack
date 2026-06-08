from __future__ import annotations

import json
from pathlib import Path

from reviewpack.ai_context import render_ai_context
from reviewpack.ai_handoff import render_ai_handoff
from reviewpack.models import ReviewpackResult, RiskLevel
from reviewpack.release_notes import render_release_note_hints
from reviewpack.reviewer_checklist import render_reviewer_checklist


def risk_icon(level: RiskLevel) -> str:
    """Return a simple text icon for a risk level."""

    if level == RiskLevel.HIGH:
        return "[HIGH]"
    if level == RiskLevel.MEDIUM:
        return "[MEDIUM]"
    return "[LOW]"


def render_pr_summary(result: ReviewpackResult) -> str:
    """Render the main PR summary Markdown."""

    lines: list[str] = []

    lines.append("# PR Review Context Pack")
    lines.append("")
    lines.append("## Pull Request")
    lines.append("")
    lines.append(f"- Title: {result.pr.title}")
    lines.append(f"- Author: {result.pr.author}")

    if result.pr.url:
        lines.append(f"- URL: {result.pr.url}")

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
        lines.append(
            f"- {changed_file.path} "
            f"({changed_file.category.value}, +{changed_file.additions}/-{changed_file.deletions})"
        )

    lines.append("")
    lines.append("## Suggested Review Focus")
    lines.append("")

    for index, item in enumerate(result.review_focus, start=1):
        lines.append(f"{index}. {item.title}")
        lines.append(f"   - {item.reason}")

    lines.append("")
    lines.append("## Privacy Notes")
    lines.append("")
    lines.append("- This pack was generated locally from provided input data.")
    lines.append("- AI was not used.")
    lines.append("- Branch names, commit messages, and terminal environment variables were not collected.")
    lines.append("")

    return "\n".join(lines)


def render_risk_checklist(result: ReviewpackResult) -> str:
    """Render risk checklist Markdown."""

    lines: list[str] = []

    lines.append("# Risk Checklist")
    lines.append("")

    if not result.risk_signals:
        lines.append("No deterministic risk signals were detected.")
        lines.append("")
        return "\n".join(lines)

    for signal in result.risk_signals:
        lines.append(f"## {risk_icon(signal.level)} {signal.title}")
        lines.append("")
        lines.append(signal.message)
        lines.append("")

        if signal.files:
            lines.append("Affected files:")
            lines.append("")
            for file_path in signal.files:
                lines.append(f"- {file_path}")
            lines.append("")

    return "\n".join(lines)


def render_ai_review_prompt(result: ReviewpackResult) -> str:
    """Render an AI-ready review prompt.

    The prompt is generated locally. It does not call any AI provider.
    """

    lines: list[str] = []

    lines.append("# AI Review Prompt")
    lines.append("")
    lines.append("Use the context below to review this pull request.")
    lines.append("Focus on correctness, missing tests, compatibility, security-sensitive changes, and maintainability.")
    lines.append("")
    lines.append("Important constraints:")
    lines.append("- Do not assume hidden code outside the provided context.")
    lines.append("- Prefer concrete, actionable feedback.")
    lines.append("- Avoid noisy style-only comments unless they affect correctness or maintainability.")
    lines.append("- Treat the output as suggestions for a human maintainer to verify.")
    lines.append("")
    lines.append("## Pull Request")
    lines.append("")
    lines.append(f"Title: {result.pr.title}")
    lines.append(f"Author: {result.pr.author}")

    if result.pr.description:
        lines.append("")
        lines.append("Description:")
        lines.append(result.pr.description.strip())

    lines.append("")
    lines.append("## Changed Files")
    lines.append("")

    for changed_file in result.changed_files:
        lines.append(
            f"- {changed_file.path}: {changed_file.category.value}, "
            f"+{changed_file.additions}/-{changed_file.deletions}"
        )

    lines.append("")
    lines.append("## Risk Signals")
    lines.append("")

    if result.risk_signals:
        for signal in result.risk_signals:
            lines.append(f"- {signal.level.value}: {signal.title} - {signal.message}")
    else:
        lines.append("- No deterministic risk signals were detected.")

    lines.append("")
    lines.append("## Suggested Review Focus")
    lines.append("")

    for item in result.review_focus:
        lines.append(f"- {item.title}: {item.reason}")

    lines.append("")
    lines.append("## Requested Review Output")
    lines.append("")
    lines.append("Please provide:")
    lines.append("1. A short summary of the change.")
    lines.append("2. The top risks to review.")
    lines.append("3. Missing or weak test coverage, if any.")
    lines.append("4. Documentation or release-note concerns, if any.")
    lines.append("5. Specific questions the maintainer should ask before merging.")
    lines.append("")

    return "\n".join(lines)


def write_reviewpack_outputs(result: ReviewpackResult, output_dir: str | Path) -> None:
    """Write Reviewpack outputs to an output directory."""

    target_dir = Path(output_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    (target_dir / "pr-summary.md").write_text(render_pr_summary(result), encoding="utf-8")
    (target_dir / "risk-checklist.md").write_text(render_risk_checklist(result), encoding="utf-8")
    (target_dir / "reviewer-checklist.md").write_text(render_reviewer_checklist(result), encoding="utf-8")
    (target_dir / "release-note-hints.md").write_text(render_release_note_hints(result), encoding="utf-8")
    (target_dir / "ai-review-prompt.md").write_text(render_ai_review_prompt(result), encoding="utf-8")
    (target_dir / "ai-handoff.md").write_text(render_ai_handoff(result), encoding="utf-8")
    (target_dir / "ai-context.md").write_text(render_ai_context(result), encoding="utf-8")

    json_text = json.dumps(
        result.model_dump(mode="json"),
        indent=2,
        ensure_ascii=False,
    )
    (target_dir / "reviewpack.json").write_text(json_text + "\n", encoding="utf-8")
