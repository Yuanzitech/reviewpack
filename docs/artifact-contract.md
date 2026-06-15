# Artifact Contract

This document describes Reviewpack's current output artifact running the tool.This document describes Reviewpack's current output artifact contract.

For real pull requests, generate fresh artifacts with:

    reviewpack demo
    reviewpack github https://github.com/owner/repo/pull/123
    reviewpack local

## Configurable output files

Output generation can be configured with `.reviewpack.yml`.

Example:

    outputs:
      pr_summary: true
      risk_checklist: true
      reviewer_checklist: true
      release_note_hints: true
      ai_review_prompt: true
      ai_handoff: true
      ai_context: true
      json: true

The public configuration key for JSON output is:

    json

Internally, Reviewpack maps this to `json_output`.

Users should normally keep using:

    outputs:
      json: true

## Current artifact stability level

Reviewpack currently treats artifact names as important user-facing behavior.

These output file names should remain stable unless there is a strong reason to change them:

    pr-summary.md
    risk-checklist.md
    reviewer-checklist.md
    release-note-hints.md
    ai-review-prompt.md
    ai-handoff.md
    ai-context.md
    reviewpack.json

Before v1.0, the internal Markdown structure may still evolve.

After v1.0, Reviewpack should document a stronger compatibility policy.

## pr-summary.md

Purpose:

    Human-readable summary of the pull request review context.

Current contents may include:

- Pull request title
- Pull request author
- Pull request URL
- Optional GitHub PR metadata
- Pull request description
- Change statistics
- Changed files
- Suggested review focus
- Privacy notes

Optional GitHub metadata may include:

- PR state
- Draft status
- Base branch
- Head branch
- Commit count
- Labels

## risk-checklist.md

Purpose:

    Deterministic risk review checklist for maintainers.

Current contents may include:

- Risk level
- Risk title
- Why this matters
- What to check
- Affected files

Risk levels currently include:

    high
    medium
    low

Risk signals are deterministic and based on metadata, file categories, configured thresholds, and configured high-risk paths.

Reviewpack risk signals are not security guarantees.

## reviewer-checklist.md

Purpose:

    Structured maintainer review checklist.

Current sections may include:

- Correctness
- Tests
- Documentation
- Dependencies
- CI, configuration, and infrastructure
- Release notes
- Risk review
- AI handoff
- Final maintainer decision

This artifact is intended for human review coordination.

## release-note-hints.md

Purpose:

    Help maintainers decide whether a PR should be mentioned in release notes.

Current contents may include:

- Release note categories
- Reasons
- Suggested maintainer actions
- Decision questions

Reviewpack does not generate final release notes automatically.

## ai-review-prompt.md

Purpose:

    Copy/paste-oriented AI review prompt.

Use this when an AI assistant cannot read local files and cannot accept uploaded files.

This artifact is generated locally and does not call an AI provider.

## ai-handoff.md

Purpose:

    Lightweight file-based handoff instructions for AI coding assistants.

Use this when an AI assistant can read files in a workspace.

Recommended instruction:

    Please read .reviewpack/ai-handoff.md and follow it.

## ai-context.md

Purpose:

    Single-file AI context bundle.

Use this when an AI assistant cannot read multiple local files but can accept one uploaded Markdown file.

Current contents may include:

- Review objective
- Known limitations
- Pull request metadata
- Change statistics
- Changed files
- Risk signals
- Suggested review focus
- Reviewer checklist
- Release note hints
- Requested AI review output
- Privacy notes

## ai-input-preview.md

Purpose:

    Optional preview of AI-oriented input text.

This file is generated only when users pass:

    --preview-ai-input

It is intended to help users inspect AI-oriented context before sharing it.

## reviewpack.json

Purpose:

    Machine-readable Reviewpack result.

This artifact is intended for integrations, automation, and future tooling.

The JSON structure is not yet a stable 1.0 schema.

See:

    docs/json-output.md
    docs/integration-json.md
    schemas/reviewpack-result.schema.json

## Artifact reading order

For human review:

1. `pr-summary.md`
2. `risk-checklist.md`
3. `reviewer-checklist.md`
4. `release-note-hints.md`

For AI handoff:

1. If the AI assistant can read local files, use `ai-handoff.md`.
2. If the AI assistant can accept one uploaded file, upload `ai-context.md`.
3. If only copy and paste is available, use `ai-review-prompt.md`.

For automation:

1. Use `reviewpack.json`.
2. Treat the JSON schema as pre-1.0 until a stable schema is documented.
3. See `docs/integration-json.md`.

## Compatibility expectations before v1.0

Before v1.0, Reviewpack aims to keep these stable when possible:

- CLI command names
- Default output file names
- Default output directory
- Public configuration keys
- Privacy-first defaults

Before v1.0, Reviewpack may still refine:

- Markdown section structure
- Risk signal wording
- Reviewer checklist wording
- Release note hint wording
- JSON field details
- Configuration schema details

## Compatibility expectations for v1.0

Before a v1.0 release, Reviewpack should define:

- Stable artifact names
- Stable JSON schema expectations
- Stable configuration schema expectations
- Stable GitHub Action inputs
- Deprecation policy
- Migration policy
- Breaking change policy

## Privacy notes

Reviewpack does not call AI providers by default.

Reviewpack does not collect raw diffs or full source code by default.

Users remain in control of which artifacts are shared with AI tools.

Reviewpack is not yet a stable 1.0 product, so this contract is considered pre-1.0 and may still evolve.

The purpose of this document is to make current expectations explicit for users, maintainers, and integrations.

## Default output directory

Reviewpack writes output to:

    .reviewpack/

by default.

Users can choose another directory with:

    --output PATH

Example:

    reviewpack demo --output reviewpack-output

## Default output files

By default, Reviewpack may generate:

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

## Example output files

Reviewpack includes example output artifacts under:

    examples/output/

Example files include:

    examples/output/pr-summary.example.md
    examples/output/risk-checklist.example.md
    examples/output/reviewer-checklist.example.md
    examples/output/release-note-hints.example.md
    examples/output/ai-review-prompt.example.md
    examples/output/ai-handoff.example.md
    examples/output/ai-context.example.md
    examples/output/reviewpack.example.json

