# Project Status

This document summarizes the current status of Reviewpack after the v0.6.1 patch release.

Reviewpack is an early-stage, PyPI-published, privacy-first CLI and GitHub Action for generating structured pull request review context.

## Current stage

Reviewpack is currently a usable early product.

It is no longer only a prototype or repository-local tool.

Reviewpack currently supports:

- PyPI installation
- CLI usage
- GitHub Action usage
- Demo mode for first-run experience
- Local git diff analysis
- Enriched GitHub pull request metadata analysis
- Fixture-based input for tests and integrations
- Structured Markdown output
- Machine-readable JSON output
- Configurable rules and outputs
- Improved review artifacts
- Optional short PR comment mode
- AI handoff files without calling AI providers
- TestPyPI and PyPI installation verification workflows

## Latest stable version

Current latest stable PyPI version:

    0.6.1

v0.6.1 fixed a Pydantic warning caused by the internal `OutputConfig.json` field shadowing `BaseModel.json`.

The public configuration key remains:

    outputs:
      json: true

## Installation status

Reviewpack is available on PyPI:

    pip install reviewpack

Recommended first-run workflow:

    reviewpack demo
    reviewpack handoff
    reviewpack guide

Reviewpack writes output to `.reviewpack/` by default.

## Current CLI commands

Reviewpack currently includes:

    reviewpack demo
    reviewpack github
    reviewpack local
    reviewpack from-fixture
    reviewpack handoff
    reviewpack guide
    reviewpack version

Command-level help is available through:

    reviewpack --help
    reviewpack demo --help
    reviewpack github --help
    reviewpack local --help
    reviewpack from-fixture --help

## Current configuration support

Reviewpack can load:

    .reviewpack.yml

Configuration can currently control:

- output generation
- large PR thresholds
- high-risk paths
- docs path patterns
- tests path patterns
- dependency path patterns
- CI path patterns
- config path patterns
- infrastructure path patterns

CLI commands load `.reviewpack.yml` by default when present.

Users can also pass:

    --config path/to/reviewpack.yml

See:

    docs/config-schema.md
    docs/configuration.md

## Current artifact contract

Reviewpack currently generates a pre-1.0 artifact contract.

Default output files may include:

    .reviewpack/pr-summary.md
    .reviewpack/risk-checklist.md
    .reviewpack/reviewer-checklist.md
    .reviewpack/release-note-hints.md
    .reviewpack/ai-review-prompt.md
    .reviewpack/ai-handoff.md
    .reviewpack/ai-context.md
    .reviewpack/reviewpack.json

If AI input preview is enabled, Reviewpack also writes:

    .reviewpack/ai-input-preview.md

See:

    docs/artifact-contract.md
    docs/output-artifacts.md
    docs/json-output.md

## Recommended workflows

### First-time users

    pip install reviewpack
    reviewpack demo
    reviewpack handoff

### GitHub pull request review

    reviewpack github https://github.com/owner/repo/pull/123
    reviewpack handoff

Public repositories usually do not require a token.

Private repositories or rate-limited usage may require:

    REVIEWPACK_GITHUB_TOKEN=YOUR_TOKEN reviewpack github https://github.com/owner/repo/pull/123

### Local development before opening a PR

    reviewpack local
    reviewpack handoff

### GitHub Actions

Reviewpack can run in pull request workflows and upload generated review packs as artifacts.

Artifact-only mode is the default.

Optional PR comment mode is available with:

    comment: "true"

Comment mode is opt-in and posts a short pointer comment. It does not paste the full review pack into the pull request.

See:

    docs/github-action.md

## AI handoff status

Reviewpack does not call AI providers by default.

Instead, Reviewpack generates local files that users can inspect and choose to share.

Recommended AI handoff order:

1. If the AI assistant can read local workspace files, ask it to read `.reviewpack/ai-handoff.md`.
2. If the AI assistant cannot read local files but can accept one uploaded file, upload `.reviewpack/ai-context.md`.
3. If only copy and paste is available, use `.reviewpack/ai-review-prompt.md`.

## Privacy status

Reviewpack is privacy-first by default.

Current defaults:

- No AI provider calls by default
- No raw diff upload by default
- No full source code upload by default
- No commit message collection for AI context by default
- No token storage
- No token logging
- No PR comments by default
- Local-first workflows where possible

GitHub mode uses network access to fetch explicitly requested pull request metadata and changed file statistics from the GitHub API.

GitHub mode may include metadata such as labels, base/head branch names, commit count, draft status, and changed file status in generated local artifacts.

## Publishing and verification status

Reviewpack has:

- CI workflow
- Package build workflow
- Publish workflow
- TestPyPI install verification workflow
- PyPI install verification workflow

The package workflow verifies:

- Distribution build
- Package metadata checks
- Wheel contents
- Installed wheel CLI smoke test
- Config import without `UserWarning`

The PyPI install workflow verifies:

- Installation from PyPI
- Config import without `UserWarning`
- `reviewpack version`
- `reviewpack guide`
- `reviewpack demo`
- `reviewpack handoff`
- Expected output files
- AI input preview output

## Current limitations

Reviewpack does not currently include:

- Direct AI provider integration
- Raw diff analysis by default
- Inline PR review comments
- IDE plugin integration
- MCP server integration
- Automatic approval or merge
- Stable 1.0 artifact contract

These are intentionally not part of the current default workflow.

## Current product maturity

Reviewpack is best described as:

    Early product / public OSS developer tool

It is suitable for:

- Trying Reviewpack locally
- Generating PR review context
- Preparing AI handoff artifacts
- Using GitHub Action artifact output
- Experimenting with opt-in PR comment mode
- Adapting basic rules and outputs through configuration

It is not yet a stable 1.0 product.

Before 1.0, Reviewpack should further improve:

- Artifact contract stability
- Configuration schema stability
- GitHub Action validation
- Optional GitHub Enterprise host support
- JSON schema documentation
- Release candidate criteria

See:

    docs/v1-readiness.md
