# JSON Output

Reviewpack writes a machine-readable JSON artifact by default:

    .reviewpack/reviewpack.json

This document describes the current JSON output structure and stability expectations.

Reviewpack is not yet a stable 1.0 product, so the JSON output should be considered pre-1.0.

## Purpose

The JSON output is intended for:

- integrations
- automation
- downstream tooling
- testing
- future dashboards
- future GitHub Action enhancements

For human review, start with Markdown artifacts such as:

    pr-summary.md
    risk-checklist.md
    reviewer-checklist.md
    release-note-hints.md

## Output file

Default path:

    .reviewpack/reviewpack.json

The JSON output can be disabled with:

    outputs:
      json: false

The public config key is `json`.

Internally, Reviewpack maps it to `json_output`.

## Top-level structure

The current JSON output is generated from the `ReviewpackResult` model.

Current top-level fields:

    pr
    changed_files
    stats
    risk_signals
    review_focus
    metadata

## pr

The `pr` object contains pull request metadata.

Current fields may include:

    title
    author
    url
    description
    state
    is_draft
    base_branch
    head_branch
    commit_count
    labels

Some fields may be null or omitted depending on input mode.

### CLI demo mode

Demo mode uses synthetic metadata.

### Local mode

Local mode uses user-provided or default title and author values.

### GitHub mode

GitHub mode may include enriched GitHub metadata such as:

- PR state
- draft status
- base branch
- head branch
- commit count
- labels

## changed_files

The `changed_files` array contains changed file metadata.

Current fields may include:

    path
    additions
    deletions
    category
    status

The `status` field is most relevant for GitHub mode and may include values such as:

    added
    modified
    removed
    renamed

The `category` field is assigned by Reviewpack path classification.

Current categories include:

    source
    test
    docs
    dependency
    ci
    config
    infrastructure
    unknown

## stats

The `stats` object contains aggregate change statistics.

Current fields include:

    files_changed
    additions
    deletions
    source_files
    test_files
    docs_files
    dependency_files
    ci_files
    config_files
    infra_files
    unknown_files

## risk_signals

The `risk_signals` array contains deterministic risk signals.

Current fields include:

    level
    title
    message
    files

Current risk levels include:

    high
    medium
    low

Risk signals are deterministic metadata-based signals.

They are not security guarantees.

## review_focus

The `review_focus` array contains suggested review focus items.

Current fields include:

    title
    reason

These focus items are intended to guide human or AI-assisted review.

## metadata

The `metadata` object contains Reviewpack execution metadata.

Current fields may include:

    ai_used
    network_used
    mode

Values vary by command.

Example modes include:

    demo
    local_git
    github

## Stability expectations before v1.0

Before v1.0, Reviewpack aims to keep these reasonably stable:

- top-level object shape
- common field names
- output file name
- core enum values where possible

Before v1.0, Reviewpack may still refine:

- optional fields
- metadata fields
- risk signal wording
- review focus wording
- validation strictness

## Future schema work

Potential future improvements:

- Published JSON schema
- JSON schema version field
- Stable compatibility policy
- Migration notes
- Schema validation tests
- Integration examples

## Recommended integration guidance

If you build integrations on top of `reviewpack.json` before v1.0:

1. Treat unknown fields as allowed.
2. Treat missing optional fields as expected.
3. Avoid depending on exact Markdown wording.
4. Prefer stable identifiers such as file paths, categories, and risk levels.
5. Pin Reviewpack versions for production integrations.
6. Review changelog entries before upgrading.

## Privacy notes

The JSON output is generated locally.

Reviewpack does not call AI providers by default.

Reviewpack does not collect raw diffs or full source code by default.

Users remain in control of which artifacts are shared.
