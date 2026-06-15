# Roadmap

This roadmap outlines the planned direction for Reviewpack after the v0.6.0 release.

Reviewpack is a privacy-first context generator for AI-assisted pull request review. The roadmap focuses on improving maintainer workflows without requiring AI or uploading code by default.

## Current stage

Reviewpack is currently a PyPI-published early product.

It already supports:

- PyPI installation
- Demo mode
- Fixture-based input
- Local git diff input
- Enriched GitHub pull request metadata input
- GitHub Action artifact output
- Optional short PR comment mode
- Markdown and JSON outputs
- Configurable output generation
- Configurable risk thresholds
- Configurable high-risk paths
- Configurable path classification
- Improved risk checklist output
- Improved reviewer checklist output
- Improved release note hints output
- AI-ready prompt generation
- AI handoff file generation
- Single-file AI context bundle generation
- AI input preview generation
- Best-effort secret redaction
- CI, package, publishing, TestPyPI, and PyPI verification workflows

## Current recommended workflows

### First-run workflow

    pip install reviewpack
    reviewpack demo
    reviewpack handoff

### GitHub PR workflow

    reviewpack github https://github.com/owner/repo/pull/123
    reviewpack handoff

### Local development workflow

    reviewpack local
    reviewpack handoff

### GitHub Action workflow

Use Reviewpack in pull request workflows and download the generated artifact.

Optional short PR comment mode is available through:

    comment: "true"

See:

    docs/github-action.md

## Near-term priorities

After v0.6.0, the next stage should focus on stabilization, validation, and preparing a stronger artifact contract.

## v0.7.x: Configuration and artifact contract refinement

Focus areas:

- Stronger `.reviewpack.yml` documentation
- Configuration schema stability
- Output selection stability
- JSON output structure documentation
- Backward compatibility expectations
- More realistic configuration examples

Potential additions:

- JSON schema documentation
- Configuration examples for Python projects
- Configuration examples for JavaScript projects
- More explicit artifact stability notes
- Migration notes for future breaking changes

## v0.8.x: GitHub workflow validation

Focus areas:

- Broader GitHub Action validation
- Fork pull request behavior documentation
- Comment mode failure handling
- GitHub Enterprise host design
- More robust token and permission guidance

Potential additions:

- Optional GitHub Enterprise host support
- Better fork PR guidance
- Safer comment mode fallback behavior
- More examples for private repositories
- More examples for monorepos

Reviewpack should continue to avoid raw diff collection by default.

## v0.9.x: Stabilization before 1.0

Focus areas:

- Stable command surface
- Stable output file names
- Stable JSON artifact expectations
- Stable GitHub Action inputs
- Stable privacy model
- Documentation completeness

Potential additions:

- 1.0 readiness checklist
- Artifact contract documentation
- Configuration compatibility policy
- Deprecation policy
- More complete example gallery

## v1.0.0: Stable CLI and artifact contract

Reviewpack should consider v1.0.0 when these are stable:

- CLI command names
- CLI core options
- Output file names
- JSON output structure
- GitHub Action inputs
- Privacy model
- Configuration schema
- Documentation structure
- Release and publishing process

A v1.0.0 release should clearly document stability guarantees and migration expectations.

## Out of scope for now

Not immediate priorities:

- Automatic PR approval
- Automatic PR merge
- Noisy default PR comments
- AI provider calls by default
- Raw diff upload by default
- Full source code upload by default
- SaaS hosting
- IDE plugin
- MCP server

These may be revisited later, but they should not distract from Reviewpack's current privacy-first maintainer workflow focus.

## AI provider integration

Direct AI provider integration is intentionally deferred.

Reasons:

- API key handling
- Cost control
- Data upload boundaries
- Redaction requirements
- Provider abstraction
- Prompt safety
- User trust

Current direction:

- Generate local AI handoff artifacts
- Let users decide what to share
- Keep Reviewpack useful without AI provider tokens

Future AI provider support should be:

- Optional
- Explicit
- Previewable
- Privacy-aware
- Provider-neutral where possible

## Optional PR comment mode

Optional PR comment mode is available and intentionally opt-in.

It should remain:

- disabled by default
- short and non-noisy
- artifact-oriented
- free of full review pack content
- free of AI-generated claims

Future work may improve:

- fork PR behavior
- comment failure handling
- artifact link guidance
- GitHub Enterprise compatibility

## Raw diff analysis

Raw diff analysis is intentionally not enabled by default.

If added later, it should be:

- explicit
- opt-in
- clearly documented
- previewable
- privacy-aware

## Guiding principles

Reviewpack should remain:

- Local-first where possible
- Privacy-first by default
- Useful without AI
- Clear about what is collected
- Inspectable before anything is shared with AI
- Focused on helping maintainers, not replacing them
- Conservative about network access
- Explicit about tokens and permissions
