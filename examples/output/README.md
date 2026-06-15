# Example Output Artifacts

This directory contains example Reviewpack output artifacts.

These files are examples only. They are intended to help users understand what Reviewpack generates before running the tool.

For real pull requests, generate fresh output with:

    reviewpack demo
    reviewpack github https://github.com/owner/repo/pull/123
    reviewpack local

Reviewpack writes output to:

    .reviewpack/

by default.

## Example files

This directory includes:

    pr-summary.example.md
    risk-checklist.example.md
    reviewer-checklist.example.md
    release-note-hints.example.md
    ai-review-prompt.example.md
    ai-handoff.example.md
    ai-context.example.md
    reviewpack.example.json

## Recommended reading order

For human review:

1. `pr-summary.example.md`
2. `risk-checklist.example.md`
3. `reviewer-checklist.example.md`
4. `release-note-hints.example.md`

For AI handoff:

1. If the AI assistant can read files, start with `ai-handoff.example.md`.
2. If the AI assistant can accept one uploaded file, use `ai-context.example.md`.
3. If only copy and paste is available, use `ai-review-prompt.example.md`.

For integrations:

1. Start with `reviewpack.example.json`.
2. See `docs/json-output.md`.
3. See `docs/integration-json.md`.
4. See `schemas/reviewpack-result.schema.json`.

## Notes

Example outputs are not a stable API by themselves.

For current artifact expectations, see:

    docs/artifact-contract.md
    docs/output-artifacts.md
    docs/json-output.md

Reviewpack is still pre-1.0, so Markdown wording and structure may continue to evolve before the stable artifact contract is finalized.

## Privacy notes

Reviewpack does not call AI providers by default.

Reviewpack does not collect raw diffs or full source code by default.

Users remain in control of which artifacts are shared with AI tools.
