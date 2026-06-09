from __future__ import annotations

from reviewpack.models import FileCategory, ReviewpackResult, RiskLevel


def render_reviewer_checklist(result: ReviewpackResult) -> str:
    """Render a structured reviewer checklist."""

    categories = {changed_file.category for changed_file in result.changed_files}
    high_risk_signals = [signal for signal in result.risk_signals if signal.level == RiskLevel.HIGH]
    medium_risk_signals = [signal for signal in result.risk_signals if signal.level == RiskLevel.MEDIUM]

    lines: list[str] = []

    lines.append("# Reviewer Checklist")
    lines.append("")
    lines.append("Use this checklist to guide human review.")
    lines.append("")
    lines.append("Reviewpack output is deterministic context, not a replacement for maintainer judgment.")
    lines.append("")

    lines.append("## Correctness")
    lines.append("")
    lines.append("- [ ] Confirm the intended behavior is clear from the PR description and changed files.")
    lines.append("- [ ] Review edge cases and failure modes around the changed areas.")
    lines.append("- [ ] Check whether the implementation matches the stated PR goal.")

    if FileCategory.SOURCE in categories:
        lines.append("- [ ] Review source changes for behavior, compatibility, and maintainability.")

    lines.append("")

    lines.append("## Tests")
    lines.append("")

    if FileCategory.TEST in categories:
        lines.append("- [ ] Review updated or added tests for meaningful coverage.")
        lines.append("- [ ] Confirm tests cover the changed behavior, not only happy paths.")
    elif FileCategory.SOURCE in categories:
        lines.append("- [ ] Source files changed but no test files were detected.")
        lines.append("- [ ] Ask whether tests should be added or updated before merging.")
    else:
        lines.append("- [ ] Confirm whether test updates are needed for this change.")

    lines.append("")

    lines.append("## Documentation")
    lines.append("")

    if FileCategory.DOCS in categories:
        lines.append("- [ ] Review documentation changes for accuracy and completeness.")
        lines.append("- [ ] Confirm examples, commands, and paths match current behavior.")
    else:
        lines.append("- [ ] Confirm whether user-facing behavior changed and needs documentation.")

    lines.append("")

    lines.append("## Dependencies")
    lines.append("")

    if FileCategory.DEPENDENCY in categories:
        lines.append("- [ ] Review dependency changes for compatibility and security impact.")
        lines.append("- [ ] Confirm lock files and package metadata are consistent.")
    else:
        lines.append("- [ ] No dependency files were detected, but confirm no implicit dependency behavior changed.")

    lines.append("")

    lines.append("## CI, Configuration, and Infrastructure")
    lines.append("")

    if FileCategory.CI in categories:
        lines.append("- [ ] Review CI workflow changes for required checks and release behavior.")
    if FileCategory.CONFIG in categories:
        lines.append("- [ ] Review configuration changes for tool behavior and developer workflow impact.")
    if FileCategory.INFRA in categories:
        lines.append("- [ ] Review infrastructure changes for deployment, runtime, and environment impact.")

    if not {FileCategory.CI, FileCategory.CONFIG, FileCategory.INFRA}.intersection(categories):
        lines.append("- [ ] Confirm no CI, configuration, or infrastructure behavior is affected.")

    lines.append("")

    lines.append("## Release Notes")
    lines.append("")
    lines.append("- [ ] Check `release-note-hints.md` to decide whether this PR should be mentioned in release notes.")
    lines.append("- [ ] Confirm whether the change is user-facing, maintainer-facing, or internal only.")
    lines.append("")

    lines.append("## Risk Review")
    lines.append("")

    if high_risk_signals:
        lines.append("- [ ] High risk signals were detected. Review these before merging.")
        for signal in high_risk_signals:
            lines.append(f"  - [ ] {signal.title}")
    elif medium_risk_signals:
        lines.append("- [ ] Medium risk signals were detected. Confirm mitigations before merging.")
        for signal in medium_risk_signals:
            lines.append(f"  - [ ] {signal.title}")
    else:
        lines.append("- [ ] No deterministic risk signals were detected.")
        lines.append("- [ ] Still review the change manually for project-specific risk.")

    lines.append("")
    lines.append("## AI Handoff")
    lines.append("")
    lines.append("- [ ] If using an AI assistant, start with `ai-handoff.md` when file access is available.")
    lines.append("- [ ] If uploading one file, use `ai-context.md`.")
    lines.append("- [ ] If only copy and paste is available, use `ai-review-prompt.md`.")
    lines.append("")
    lines.append("## Final Maintainer Decision")
    lines.append("")
    lines.append("- [ ] Confirm open questions are resolved.")
    lines.append("- [ ] Confirm required checks pass.")
    lines.append("- [ ] Confirm the PR is appropriately scoped for merge.")
    lines.append("")

    return "\n".join(lines)
