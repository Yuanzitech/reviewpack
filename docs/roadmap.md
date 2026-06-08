# Roadmap

This roadmap outlines the planned direction for Reviewpack after the v0.5.0 release.

Reviewpack is a privacy-first context generator for AI-assisted pull request review. The roadmap focuses on improving maintainer workflows without requiring AI or uploading code by default.

## Current stage

Reviewpack is currently a PyPI-published early product.

It already supports:

- PyPI installation
- Demo mode
- Fixture-based input
- Local git diff input
- GitHub pull request metadata input
- GitHub Action artifact output
- Markdown and JSON outputs
- Reviewer checklist output
- Release note hints output
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

See:

    docs/github-action.md

## Near-term priorities

The next stage should focus on making Reviewpack more useful for real maintainers and teams.

## v0.6.x: GitHub workflow, configuration, and artifact quality

Focus areas:

- GitHub Action UX polish
- Configuration-driven rules and outputs
- Review artifact quality improvements
- Better output examples
- Clearer project status and roadmap documentation

Potential additions:

- Improved GitHub Action examples
- Local mode GitHub Action example
- Clearer artifact download instructions
- More visible AI handoff guidance in GitHub Action workflows
- Configurable output selection
- Configurable risk thresholds
- Configurable high-risk paths
- More structured reviewer checklist output
- More useful release note hints
- More example output files

## v0.7.x: Config-driven workflows

Focus areas:

- Stronger `.reviewpack.yml` support
- Team-specific rules
- Configurable path classification
- Configurable output generation
- Configurable thresholds

Potential configuration areas:

    outputs
    risk
    paths
    github
    ai_handoff

Example future configuration:

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

## v0.8.x: Review artifact quality

Focus areas:

- Better risk signal quality
- Better reviewer checklist quality
- Better release note hints
- Better AI context structure
- More realistic examples

Potential improvements:

- More explicit risk reasons
- Suggested reviewer actions
- Better docs/test/dependency impact detection
- More structured release note categories
- More output examples under `examples/output/`

## v0.9.x: GitHub PR workflow enrichment

Focus areas:

- Better GitHub PR metadata support
- Better GitHub API error handling
- Better rate limit guidance
- Optional safe metadata enrichment

Potential additions:

- PR draft status
- Labels
- Changed file status
- Commit count
- Base branch metadata
- Friendlier rate limit errors
- Clearer token guidance

Reviewpack should continue to avoid raw diff collection by default.

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

Optional PR comment mode may be useful later.

It should be opt-in.

It should not post comments by default.

Potential behavior:

- Post a short summary
- Link to workflow artifact
- Mention generated handoff files
- Avoid noisy line-by-line comments

Before implementation, Reviewpack should define:

- Comment permissions
- Update strategy
- Duplicate comment prevention
- Fork PR behavior
- Markdown length limits
- Privacy guidance

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
