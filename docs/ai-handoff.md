# AI Handoff

Reviewpack can generate lightweight AI handoff files.

The main handoff file is:

    .reviewpack/ai-handoff.md

Reviewpack also generates a single-file AI context bundle:

    .reviewpack/ai-context.md

These files help users hand Reviewpack output to AI coding assistants without copying a large prompt manually.

## Why AI handoff exists

Some AI coding tools can read files in the current workspace.

Examples include IDE-based or agent-based tools that can inspect local project files.

For those tools, users can ask:

    Please read .reviewpack/ai-handoff.md and follow it.

The AI assistant can then inspect the Reviewpack artifacts in `.reviewpack/`.

## Recommended workflow

Generate a pack:

    reviewpack github https://github.com/owner/repo/pull/123

Then run:

    reviewpack handoff

If the AI assistant can read local files, ask:

    Please read .reviewpack/ai-handoff.md and follow it.

## If the AI assistant cannot access files

Some AI assistants cannot read local files directly.

If the AI assistant can accept one uploaded file, upload:

    .reviewpack/ai-context.md

This file combines the most useful Reviewpack context into one Markdown file.

If only copy and paste is available, use:

    .reviewpack/ai-review-prompt.md

## Generated files

A Reviewpack output directory may include:

    .reviewpack/pr-summary.md
    .reviewpack/risk-checklist.md
    .reviewpack/reviewer-checklist.md
    .reviewpack/release-note-hints.md
    .reviewpack/ai-review-prompt.md
    .reviewpack/ai-handoff.md
    .reviewpack/ai-context.md
    .reviewpack/reviewpack.json

If AI input preview is enabled, it may also include:

    .reviewpack/ai-input-preview.md

## Choosing the right file

Use this order:

1. If the AI assistant can read local files, point it to `.reviewpack/ai-handoff.md`.
2. If the AI assistant cannot read local files but can accept one file, upload `.reviewpack/ai-context.md`.
3. If only copy and paste is available, copy `.reviewpack/ai-review-prompt.md`.

## Privacy behavior

AI handoff does not call AI providers.

It does not upload code.

It does not upload raw diffs.

It only generates local instructions and local Markdown artifacts.

The user remains in control of what is shared with AI tools.
