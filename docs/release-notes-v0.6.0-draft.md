# Reviewpack v0.6.0

Reviewpack v0.6.0 is a GitHub workflow, configuration, and artifact quality release.

This release builds on v0.5.0 by making Reviewpack more useful for real maintainer workflows and team adoption.

## Highlights

### GitHub Action UX polish

The GitHub Action now provides clearer next-step guidance after generating Reviewpack output.

It highlights important files such as:

    pr-summary.md
    risk-checklist.md
    reviewer-checklist.md
    release-note-hints.md
    ai-handoff.md
    ai-context.md
    ai-review-prompt.md
    reviewpack.json

Artifact upload now explicitly supports hidden Reviewpack output directories.

The GitHub Action documentation now explains:

- how to download workflow artifacts
- how to use generated artifacts
- how to hand artifacts to AI assistants
- public and private repository token behavior
- local mode workflow usage

### Configuration-driven rules and outputs

Reviewpack now supports `.reviewpack.yml`.

Configuration is optional. If no config file is present, Reviewpack uses privacy-first defaults.

Configuration can control:

- output generation
- large PR thresholds
- high-risk paths
- docs path patterns
- tests path patterns
- dependency path patterns
- CI path patterns
- config path patterns
- infrastructure path patterns

Example:

    outputs:
      ai_context: true
      ai_handoff: true
      reviewer_checklist: true
      release_note_hints: true

    risk:
      large_pr_files: 20
      large_pr_lines: 500
      high_risk_paths:
        - .github/workflows/
        - pyproject.toml

    paths:
      docs:
        - docs/
        - README.md
      tests:
        - tests/

CLI commands now load `.reviewpack.yml` by default when present.

Users can also pass a custom config path:

    reviewpack demo --config path/to/reviewpack.yml
    reviewpack local --config path/to/reviewpack.yml
    reviewpack github https://github.com/owner/repo/pull/123 --config path/to/reviewpack.yml

### Review artifact quality improvements

Reviewpack output artifacts are now clearer and more actionable.

The risk checklist now includes:

- why the signal matters
- what reviewers should check
- affected files

The reviewer checklist is now structured around maintainer review areas:

- correctness
- tests
- documentation
- dependencies
- CI, configuration, and infrastructure
- release notes
- risk review
- AI handoff
- final maintainer decision

Release note hints now include:

- categories
- reasons
- suggested maintainer actions
- decision questions

AI context now includes:

- review objective
- known limitations
- pull request metadata
- change statistics
- risk signals
- reviewer checklist
- release note hints
- requested AI review output
- privacy notes

### Output artifact documentation and examples

This release adds documentation for generated artifacts:

    docs/output-artifacts.md

It also adds example output files under:

    examples/output/

These examples help users understand Reviewpack output without running the tool first.

### Enriched GitHub PR metadata

GitHub mode now captures more metadata when available:

- pull request state
- draft status
- base branch name
- head branch name
- commit count
- labels
- changed file status

This metadata may appear in:

    pr-summary.md
    ai-review-prompt.md
    ai-context.md
    reviewpack.json

GitHub mode still does not collect raw diffs or full source code by default.

### Friendlier GitHub API errors

GitHub API errors are now more actionable for common cases:

- 401 Unauthorized
- 403 Forbidden
- 404 Not Found

The error messages now better explain token, permission, rate limit, and repository accessibility issues.

### Optional PR comment mode

The GitHub Action now supports optional PR comment mode:

    comment: "true"

This is disabled by default.

When enabled, Reviewpack posts or updates a short pointer comment on the pull request.

The comment points maintainers to the generated workflow artifact and key files.

It does not paste the full review pack into the pull request.

Reviewpack comments include a stable marker:

    <!-- reviewpack-comment -->

Repeated workflow runs update the existing Reviewpack comment instead of creating duplicates.

Comment mode requires:

    permissions:
      contents: read
      pull-requests: write

Artifact-only mode can continue to use:

    permissions:
      contents: read
      pull-requests: read

## Privacy notes

Reviewpack v0.6.0 keeps the privacy-first defaults.

This release does not add AI provider calls.

This release does not collect raw diffs by default.

This release does not upload source code to AI providers.

This release does not post PR comments by default.

Optional PR comment mode only posts a short pointer comment when explicitly enabled.

## What's changed since v0.5.0

### Added

- Project status document
- GitHub Action local mode example
- Configuration model
- Configurable output generation
- Configurable risk thresholds
- Configurable high-risk paths
- Configurable path classification
- Configuration guide
- Example `.reviewpack.yml`
- Output artifacts documentation
- Example output files
- Enriched GitHub PR metadata
- Friendly GitHub API error messages
- Optional PR comment mode
- GitHub PR comment helper
- Stable Reviewpack PR comment marker
- GitHub Action comment mode example
- Tests for new behavior

### Changed

- GitHub Action UX improved
- GitHub Action documentation improved
- CLI commands now load `.reviewpack.yml` by default when present
- CLI commands now support `--config`
- File classification now uses configurable path patterns
- Risk detection now uses configurable thresholds and high-risk paths
- Risk checklist output is now more actionable
- Reviewer checklist output is now more structured
- Release note hints include suggested maintainer actions and decision questions
- AI context includes review objective and known limitations
- GitHub mode includes enriched metadata when available
- GitHub Action supports opt-in PR comment mode

## Known limitations

This release does not yet include:

- Direct AI provider integration
- Raw diff analysis by default
- Inline review comments
- Automatic approval
- Automatic merge
- GitHub Enterprise host support
- Stable 1.0 artifact contract

## Suggested upgrade path

Install or upgrade from PyPI:

    pip install --upgrade reviewpack

Verify:

    reviewpack version
    reviewpack demo
    reviewpack handoff
    reviewpack guide

For GitHub Action users, update workflow references after the GitHub release is published:

    uses: Yuanzitech/reviewpack@v0.6.0

## Next steps

Potential next steps include:

- stabilization toward a stronger artifact contract
- broader GitHub Action validation
- optional GitHub Enterprise host support
- optional raw diff mode design
- stronger JSON schema documentation
- release candidate criteria for 1.0
