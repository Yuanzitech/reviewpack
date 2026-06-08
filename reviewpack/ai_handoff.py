from __future__ import annotations

from pathlib import Path

from reviewpack.models import ReviewpackResult


def render_ai_handoff(result: ReviewpackResult) -> str:
    """Render a lightweight AI handoff file.

    The handoff file is intentionally short. It tells AI coding tools how to use
    the Reviewpack artifacts in the output directory without forcing users to
    copy a large prompt manually.
    """

    lines: list[str] = []

    lines.append("# AI Handoff")
    lines.append("")
    lines.append("Please read the Reviewpack files in this directory and use them to review the pull request.")
    lines.append("")
    lines.append("Start with:")
    lines.append("")
    lines.append("- ai-review-prompt.md")
    lines.append("- pr-summary.md")
    lines.append("- risk-checklist.md")
    lines.append("- reviewer-checklist.md")
    lines.append("- release-note-hints.md")
    lines.append("")
    lines.append("## Pull Request")
    lines.append("")
    lines.append(f"- Title: {result.pr.title}")
    lines.append(f"- Author: {result.pr.author}")

    if result.pr.url:
        lines.append(f"- URL: {result.pr.url}")

    lines.append("")
    lines.append("## Instructions for the AI assistant")
    lines.append("")
    lines.append("- Use the Reviewpack artifacts as review context.")
    lines.append("- Do not assume hidden code or files that are not available.")
    lines.append("- Do not claim that raw source code was inspected unless source code was provided separately.")
    lines.append("- Prefer concrete, actionable maintainer feedback.")
    lines.append("- Focus on correctness, tests, compatibility, security-sensitive changes, and maintainability.")
    lines.append("- Treat Reviewpack output as context for human review, not as ground truth.")
    lines.append("")
    lines.append("## If files are not accessible")
    lines.append("")
    lines.append("If local files cannot be accessed, ask the user to upload or paste:")
    lines.append("")
    lines.append("- ai-review-prompt.md")
    lines.append("")
    lines.append("If the user can upload multiple files, also ask for:")
    lines.append("")
    lines.append("- pr-summary.md")
    lines.append("- risk-checklist.md")
    lines.append("- reviewer-checklist.md")
    lines.append("- release-note-hints.md")
    lines.append("")
    lines.append("## Privacy notes")
    lines.append("")
    lines.append("- Reviewpack does not call an AI provider by default.")
    lines.append("- Reviewpack does not upload raw diffs or full source code by default.")
    lines.append("- Reviewpack does not require branch names or commit messages for this handoff.")
    lines.append("- The user remains in control of what is shared with AI tools.")
    lines.append("")

    return "\n".join(lines)


def write_ai_handoff(result: ReviewpackResult, output_dir: str | Path) -> Path:
    """Write the AI handoff file to an output directory."""

    target_dir = Path(output_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    output_path = target_dir / "ai-handoff.md"
    output_path.write_text(render_ai_handoff(result), encoding="utf-8")

    return output_path


def render_handoff_terminal_text(output_dir: str | Path = ".reviewpack") -> str:
    """Render short terminal guidance for handing Reviewpack output to AI tools."""

    target_dir = Path(output_dir)
    handoff_path = target_dir / "ai-handoff.md"
    prompt_path = target_dir / "ai-review-prompt.md"

    lines: list[str] = []

    lines.append("Reviewpack AI handoff")
    lines.append("")
    lines.append("If your AI assistant can read files in this workspace, ask:")
    lines.append("")
    lines.append(f'  "Please read {handoff_path} and follow it."')
    lines.append("")
    lines.append("If your AI assistant cannot access local files, upload or paste:")
    lines.append("")
    lines.append(f"  {prompt_path}")
    lines.append("")
    lines.append("Useful Reviewpack files:")
    lines.append("")
    lines.append(f"- {handoff_path}")
    lines.append(f"- {prompt_path}")
    lines.append(f"- {target_dir / 'pr-summary.md'}")
    lines.append(f"- {target_dir / 'risk-checklist.md'}")
    lines.append(f"- {target_dir / 'reviewer-checklist.md'}")
    lines.append(f"- {target_dir / 'release-note-hints.md'}")
    lines.append("")

    return "\n".join(lines)
