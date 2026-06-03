from __future__ import annotations

from pathlib import Path

from reviewpack.models import ReviewpackResult
from reviewpack.redaction import redact_text


def render_ai_input_preview(result: ReviewpackResult) -> str:
    """Render a local preview of AI-bound context.

    This function does not call any AI provider. It only generates a local
    Markdown file that shows the type of context that could be sent if a future
    AI integration is explicitly enabled.
    """

    lines: list[str] = []

    lines.append("# AI Input Preview")
    lines.append("")
    lines.append("This file is generated locally.")
    lines.append("")
    lines.append("It shows the context that may be sent to an AI provider if AI mode is enabled in a future version.")
    lines.append("")
    lines.append("Reviewpack does not send this content anywhere by default.")
    lines.append("")
    lines.append("## Included by default")
    lines.append("")
    lines.append("- Pull request title")
    lines.append("- Pull request description")
    lines.append("- Changed file paths")
    lines.append("- Change statistics")
    lines.append("- Deterministic risk signals")
    lines.append("- Suggested review focus")
    lines.append("")
    lines.append("## Excluded by default")
    lines.append("")
    lines.append("- Raw diffs")
    lines.append("- Full source code")
    lines.append("- Branch names")
    lines.append("- Commit messages")
    lines.append("- Environment variables")
    lines.append("- Terminal history")
    lines.append("- Git remote URLs")
    lines.append("- API tokens")
    lines.append("")
    lines.append("## Pull Request")
    lines.append("")
    lines.append(f"- Title: {redact_text(result.pr.title)}")
    lines.append(f"- Author: {redact_text(result.pr.author)}")

    if result.pr.url:
        lines.append(f"- URL: {redact_text(result.pr.url)}")

    if result.pr.description:
        lines.append("")
        lines.append("## Description")
        lines.append("")
        lines.append(redact_text(result.pr.description.strip()))

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
            f"- {redact_text(changed_file.path)} "
            f"({changed_file.category.value}, +{changed_file.additions}/-{changed_file.deletions})"
        )

    lines.append("")
    lines.append("## Risk Signals")
    lines.append("")

    if result.risk_signals:
        for signal in result.risk_signals:
            lines.append(f"- {signal.level.value}: {redact_text(signal.title)}")
            lines.append(f"  - {redact_text(signal.message)}")
            if signal.files:
                lines.append("  - Affected files:")
                for file_path in signal.files:
                    lines.append(f"    - {redact_text(file_path)}")
    else:
        lines.append("- No deterministic risk signals were detected.")

    lines.append("")
    lines.append("## Suggested Review Focus")
    lines.append("")

    for item in result.review_focus:
        lines.append(f"- {redact_text(item.title)}")
        lines.append(f"  - {redact_text(item.reason)}")

    lines.append("")
    lines.append("## Safety Notes")
    lines.append("")
    lines.append("- This preview was generated without network access.")
    lines.append("- This preview was generated without calling an AI provider.")
    lines.append("- This preview does not include raw diffs or source code.")
    lines.append("- This preview should be reviewed before being copied into any AI tool.")
    lines.append("")

    return "\n".join(lines)


def write_ai_input_preview(result: ReviewpackResult, output_dir: str | Path) -> Path:
    """Write AI input preview Markdown to an output directory."""

    target_dir = Path(output_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    output_path = target_dir / "ai-input-preview.md"
    output_path.write_text(render_ai_input_preview(result), encoding="utf-8")

    return output_path
