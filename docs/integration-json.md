# JSON Integration Guide

This document provides guidance for consumers of Reviewpack's machine-readable JSON output.

Reviewpack writes JSON output by default:

    .reviewpack/reviewpack.json

Reviewpack is currently pre-1.0. The JSON output is useful for integrations, but consumers should treat the schema as a draft until Reviewpack publishes a stable 1.0 artifact contract.

## Current JSON artifact

Default path:

    .reviewpack/reviewpack.json

The JSON artifact can be disabled with:

    outputs:
      json: false

The public config key is:

    json

Internally, Reviewpack maps this to:

    json_output

## Draft JSON schema

Reviewpack includes a draft JSON schema:

    schemas/reviewpack-result.schema.json

The schema is currently pre-1.0.

It documents the current shape of:

    pr
    changed_files
    stats
    risk_signals
    review_focus
    metadata

The schema is intended to help integration authors validate assumptions and build safer tooling.

## Recommended integration practices

### Pin Reviewpack versions

For production integrations, pin the Reviewpack version.

Example:

    reviewpack==0.6.1

This helps avoid accidental breakage when Reviewpack evolves before v1.0.

### Treat unknown fields as allowed

Consumers should tolerate additional fields.

Reviewpack may add fields before v1.0.

Avoid rejecting JSON just because a new field appears.

### Treat optional fields as optional

Some fields are only available in certain modes.

For example, GitHub mode may include:

    state
    is_draft
    base_branch
    head_branch
    commit_count
    labels
    changed file status

Local mode and fixture mode may not include all GitHub-specific metadata.

### Avoid depending on exact Markdown wording

The JSON output is a better integration surface than Markdown artifacts.

Markdown wording may change as Reviewpack improves artifact quality.

If you need stable machine-readable information, prefer:

    reviewpack.json

over parsing:

    pr-summary.md
    risk-checklist.md
    reviewer-checklist.md
    release-note-hints.md

### Prefer categories and structured fields

Useful fields for integrations include:

    changed_files[].path
    changed_files[].category
    changed_files[].additions
    changed_files[].deletions
    changed_files[].status
    risk_signals[].level
    risk_signals[].title
    stats.files_changed
    stats.additions
    stats.deletions

### Do not treat risk signals as security guarantees

Reviewpack risk signals are deterministic review signals.

They are intended to guide review, not prove that a pull request is safe or unsafe.

## Common integration ideas

Potential integrations include:

- dashboards
- release preparation tools
- PR triage tools
- repository health checks
- CI artifact processors
- AI context preparation tools
- maintainer workflow automation

## Example: read changed file categories

Example pseudo-workflow:

    1. Generate Reviewpack output.
    2. Read .reviewpack/reviewpack.json.
    3. Count changed files by category.
    4. Decide whether additional reviewers are needed.

Important fields:

    changed_files[].category
    stats.source_files
    stats.test_files
    stats.docs_files
    stats.dependency_files
    stats.ci_files
    stats.config_files
    stats.infra_files

## Example: detect high risk signals

Example pseudo-workflow:

    1. Read risk_signals.
    2. Filter items where level is high.
    3. Notify maintainers or require extra review.

Important fields:

    risk_signals[].level
    risk_signals[].title
    risk_signals[].files

## Example: release note triage

Example pseudo-workflow:

    1. Read changed file categories.
    2. Check for source, dependency, CI, config, or infrastructure changes.
    3. Read release-note-hints.md for human guidance.
    4. Decide whether the PR needs release notes.

Useful JSON fields:

    changed_files[].category
    stats.dependency_files
    stats.ci_files
    stats.config_files
    stats.infra_files

## Pre-1.0 compatibility expectations

Before v1.0, Reviewpack aims to keep these stable where possible:

- `reviewpack.json` file name
- top-level JSON object shape
- common field names
- enum values for file categories and risk levels

Before v1.0, Reviewpack may still refine:

- optional fields
- metadata fields
- exact risk signal wording
- review focus wording
- schema strictness
- future schema versioning

## Future schema work

Potential future improvements:

- schema version field
- published schema compatibility policy
- stronger validation tests
- integration examples
- generated schema from Pydantic models
- migration notes for breaking changes

## Privacy notes

The JSON artifact is generated locally.

Reviewpack does not call AI providers by default.

Reviewpack does not upload raw diffs or full source code by default.

Users remain in control of which artifacts are shared with external tools.
