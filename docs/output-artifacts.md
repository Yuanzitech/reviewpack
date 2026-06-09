# Output Artifacts

Reviewpack generates structured review artifacts.

By default, output files are written to:

    .reviewpack/

Use `--output PATH` to choose another directory.

## Default output files

A typical Reviewpack output directory includes:

    pr-summary.md
    risk-checklist.md
    reviewer-checklist.md
    release-note-hints.md
    ai-review-prompt.md
    ai-handoff.md
    ai-context.md
    reviewpack.json

If AI input preview is enabled, Reviewpack also writes:

    ai-input-preview.md

## pr-summary.md

The PR summary provides:

- Pull request title
- Author
- URL when available
- Description
- Change statistics
- Changed files
- Suggested review focus
- Privacy notes

Start here when reviewing a generated pack manually.

## risk-checklist.md

The risk checklist summarizes deterministic risk signals.

Each risk signal includes:

- Risk level
- Why the signal matters
- What reviewers should check
- Affected files

This file is designed to be actionable for maintainers.

## reviewer-checklist.md

The reviewer checklist organizes review work into sections:

- Correctness
- Tests
- Documentation
- Dependencies
- CI, configuration, and infrastructure
- Release notes
- Risk review
- AI handoff
- Final maintainer decision

This file is useful for human review and review coordination.

## release-note-hints.md

Release note hints help maintainers decide whether a PR should be mentioned in release notes.

Reviewpack does not generate final release notes automatically.

Instead, it provides:

- Categories
- Reasons
- Suggested maintainer actions
- Decision questions

## ai-review-prompt.md

The AI review prompt is a copy/paste-oriented prompt for AI assistants.

Use this when an AI assistant cannot read local files and cannot accept uploaded files.

## ai-handoff.md

The AI handoff file is a lightweight instruction file.

Use it when an AI assistant can read files in a workspace.

Recommended instruction:

    Please read .reviewpack/ai-handoff.md and follow it.

## ai-context.md

The AI context file is a single-file bundle.

Use it when an AI assistant cannot read multiple local files but can accept one uploaded Markdown file.

It includes:

- Review objective
- Known limitations
- PR metadata
- Changed files
- Risk signals
- Suggested review focus
- Reviewer checklist
- Release note hints
- Requested AI review output
- Privacy notes

## reviewpack.json

The JSON output is machine-readable.

It is intended for integrations, automation, and future tooling.

## Recommended reading order

For human review:

1. `pr-summary.md`
2. `risk-checklist.md`
3. `reviewer-checklist.md`
4. `release-note-hints.md`

For AI handoff:

1. If the AI assistant can read local files, use `ai-handoff.md`.
2. If the AI assistant can accept one uploaded file, upload `ai-context.md`.
3. If only copy and paste is available, use `ai-review-prompt.md`.

## Privacy notes

Reviewpack does not call AI providers by default.

Reviewpack does not upload raw diffs or source code by default.

Users remain in control of which artifacts are shared with AI tools.
