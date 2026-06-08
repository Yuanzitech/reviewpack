# AI Handoff

Reviewpack can generate a lightweight AI handoff file:

    .reviewpack/ai-handoff.md

This file helps users hand Reviewpack output to AI coding assistants without copying a large prompt manually.

## Why AI handoff exists

Some AI coding tools can read files in the current workspace.

Examples include IDE-based or agent-based tools that can inspect local project files.

For those tools, users can simply ask:

    Please read .reviewpack/ai-handoff.md and follow it.

The AI assistant can then inspect the Reviewpack artifacts in `.reviewpack/`.

## Generated files

A Reviewpack output directory may include:

    .reviewpack/pr-summary.md
    .reviewpack/risk-checklist.md
    .reviewpack/reviewer-checklist.md
    .reviewpack/release-note-hints.md
    .reviewpack/ai-review-prompt.md
    .reviewpack/ai-handoff.md
    .reviewpack/reviewpack.json

If AI input preview is enabled, it may also include:

    .reviewpack/ai-input-preview.md

## Recommended workflow

Generate a pack:

    reviewpack github https://github.com/owner/repo/pull/123

Then run:

    reviewpack handoff

Ask your AI assistant:

    Please read .reviewpack/ai-handoff.md and follow it.

## If the AI assistant cannot access files

Some AI assistants cannot read local files directly.

In that case, upload or paste:

    .reviewpack/ai-review-prompt.md

If multiple files can be uploaded, also include:

    .reviewpack/pr-summary.md
    .reviewpack/risk-checklist.md
    .reviewpack/reviewer-checklist.md
    .reviewpack/release-note-hints.md

## Privacy behavior

AI handoff does not call AI providers.

It does not upload code.

It does not upload raw diffs.

It only generates local instructions and local Markdown artifacts.

The user remains in control of what is shared with AI tools.
