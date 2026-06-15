# Reviewpack

Privacy-first context packs for AI-assisted pull request review.

## Language

- English: README.md
- 简体中文: README.zh-CN.md

Reviewpack helps open-source maintainers and engineering teams prepare structured, reusable context before reviewing a pull request with a human reviewer or an AI coding assistant.

It is not another noisy AI reviewer. Reviewpack is a context layer: it collects pull request metadata, changed files, test signals, documentation signals, dependency signals, risk indicators, release note hints, reviewer checklist items, AI handoff instructions, and review focus areas into a clear review pack.

## Quick Start

Install Reviewpack:

    pip install reviewpack

Generate a demo review pack:

    reviewpack demo

Reviewpack writes output to `.reviewpack/` by default.

Show AI handoff instructions:

    reviewpack handoff

If your AI assistant can read files in your workspace, ask:

    Please read .reviewpack/ai-handoff.md and follow it.

If your AI assistant cannot read local files but can accept one uploaded file, upload:

    .reviewpack/ai-context.md

If only copy and paste is available, use:

    .reviewpack/ai-review-prompt.md

## Why Reviewpack?

AI coding tools are powerful, but review quality depends heavily on context.

Direct AI review often starts from raw diffs. That can miss important project-level signals:

- Which files are high risk?
- Were tests updated?
- Were docs updated?
- Did dependencies change?
- Is the pull request too large?
- Does the change affect CI, configuration, or release behavior?
- Should this PR be mentioned in release notes?
- What should a maintainer focus on first?

Reviewpack prepares that context before review starts.

## Common workflows

### First-time demo

    reviewpack demo

### GitHub pull request

    reviewpack github https://github.com/owner/repo/pull/123

GitHub mode may collect PR metadata such as state, draft status, base/head branch names, commit count, labels, changed file status, and changed file statistics.

GitHub mode does not collect raw diffs or full source code by default.

Public repositories usually do not require a token.

Private repositories or rate-limited usage may require:

    REVIEWPACK_GITHUB_TOKEN=YOUR_TOKEN reviewpack github https://github.com/owner/repo/pull/123

### Local development

    reviewpack local

By default, local mode compares:

    main...HEAD

### Fixture input

    reviewpack from-fixture simple-pr.json

The fixture file must already exist.

For first-time usage, prefer:

    reviewpack demo

### Command guide

    reviewpack guide

For CLI options:

    reviewpack --help
    reviewpack github --help
    reviewpack local --help

## Configuration

Reviewpack can be configured with:

    .reviewpack.yml

Configuration is optional.

If no configuration file is present, Reviewpack uses privacy-first defaults.

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

Use a custom config file:

    reviewpack demo --config path/to/reviewpack.yml

See:

    docs/configuration.md
    docs/config-schema.md
    examples/.reviewpack.yml

## GitHub Action

Reviewpack can run in GitHub Actions and upload the generated review pack as a workflow artifact.

Example workflow:

    name: Reviewpack

    on:
      pull_request:

    jobs:
      reviewpack:
        runs-on: ubuntu-latest

        permissions:
          contents: read
          pull-requests: read

        steps:
          - name: Check out repository
            uses: actions/checkout@v4

          - name: Run Reviewpack
            uses: Yuanzitech/reviewpack@v0.6.1
            with:
              mode: github
              pr-url: ${{ github.event.pull_request.html_url }}
              github-token: ${{ github.token }}

By default, the action uploads a workflow artifact named:

    reviewpack-output

After the workflow finishes, download the artifact from the GitHub Actions run.

Recommended files:

    pr-summary.md
    reviewer-checklist.md
    risk-checklist.md
    release-note-hints.md
    ai-handoff.md
    ai-context.md

The GitHub Action does not post PR comments or call AI providers by default.

Optional PR comment mode is available through:

    comment: "true"

Comment mode posts or updates a short pointer comment. It does not paste the full review pack into the pull request.

Comment mode requires:

    permissions:
      contents: read
      pull-requests: write

See:

    docs/github-action.md

Examples:

    examples/github-action.yml
    examples/github-action-local.yml
    examples/github-action-comment.yml

## What Reviewpack generates

A review pack may include:

- PR summary
- Changed file overview
- Risk checklist
- Reviewer checklist
- Release note hints
- Suggested review focus
- AI-ready review prompt
- AI handoff instructions
- AI context bundle
- AI input preview
- Machine-readable JSON output

Example output directory:

    .reviewpack/pr-summary.md
    .reviewpack/risk-checklist.md
    .reviewpack/reviewer-checklist.md
    .reviewpack/release-note-hints.md
    .reviewpack/ai-review-prompt.md
    .reviewpack/ai-handoff.md
    .reviewpack/ai-context.md
    .reviewpack/ai-input-preview.md
    .reviewpack/reviewpack.json

Output artifact details:

    docs/output-artifacts.md
    docs/artifact-contract.md

JSON output details:

    docs/json-output.md
    docs/integration-json.md

Draft JSON schema:

    schemas/reviewpack-result.schema.json

Example output files:

    examples/output/

## AI handoff

Reviewpack does not call AI providers by default.

Instead, it generates local artifacts that can be inspected and shared intentionally.

If your AI assistant can read files in your workspace, ask:

    Please read .reviewpack/ai-handoff.md and follow it.

If your AI assistant cannot read local files but can accept one uploaded file, upload:

    .reviewpack/ai-context.md

If only copy and paste is available, use:

    .reviewpack/ai-review-prompt.md

See:

    docs/ai-handoff.md

## Privacy-first by default

Reviewpack runs locally by default for demo, fixture, and local git workflows.

By default, it does not send code, diffs, commit messages, environment variables, repository secrets, or terminal information to any external AI service.

GitHub mode uses network access only to fetch explicitly requested pull request metadata and changed file statistics from the GitHub API.

GitHub mode may include PR metadata such as labels, base/head branch names, commit count, draft status, and changed file status in generated local artifacts.

The GitHub Action integration generates workflow-local artifacts and does not call AI providers.

Current privacy-oriented features include:

- Local demo mode
- Local fixture mode
- Local git diff mode
- GitHub PR metadata mode
- GitHub Action artifact mode
- Optional short PR comment mode
- Configurable output generation
- Configurable risk thresholds
- Configurable high-risk paths
- Configurable path classification
- AI-ready prompt generation without AI calls
- AI handoff without AI calls
- AI context bundle without AI calls
- AI input preview without AI calls
- Release note hints without AI calls
- Reviewer checklist without AI calls
- Best-effort secret redaction for preview text
- No raw diff upload by default
- No full source code upload by default
- No commit message upload by default
- No PR comments by default

## Documentation

- Project status: docs/status.md
- Installation guide: docs/installation.md
- Commands guide: docs/commands.md
- Configuration guide: docs/configuration.md
- Configuration schema: docs/config-schema.md
- Output artifacts: docs/output-artifacts.md
- Artifact contract: docs/artifact-contract.md
- JSON output: docs/json-output.md
- JSON integration guide: docs/integration-json.md
- v1.0 readiness: docs/v1-readiness.md
- Usage guide: docs/usage.md
- Privacy model: docs/privacy.md
- Design notes: docs/design.md
- Local git diff mode: docs/local-git.md
- GitHub support: docs/github.md
- GitHub Action: docs/github-action.md
- AI handoff: docs/ai-handoff.md
- AI input preview: docs/ai-preview.md
- Release note hints: docs/release-note-hints.md
- Reviewer checklist: docs/reviewer-checklist.md
- Integration principles: docs/integrations.md
- Roadmap: docs/roadmap.md
- Release checklist: docs/release-checklist.md
- Examples guide: examples/README.md

## Core idea

Direct AI review:

    PR diff -> AI -> review comments

Reviewpack workflow:

    PR data -> local analysis -> structured context pack -> human reviewer or AI assistant

## Current status

Reviewpack is a PyPI-published early product.

It currently supports:

- PyPI installation
- Demo mode
- Local fixture input
- Local git diff input
- Enriched GitHub PR metadata input
- GitHub Action artifact output
- Optional short PR comment mode
- Structured Markdown and JSON output
- Draft JSON schema for `reviewpack.json`
- JSON integration guidance
- Configurable rules and outputs
- Improved review artifacts
- Reviewer checklist
- Release note hints
- AI handoff
- AI context bundle
- Optional AI input preview generation
- Secret-like value redaction in preview text
- No AI calls by default

Recommended first-run workflow:

    pip install reviewpack
    reviewpack demo
    reviewpack handoff

For a detailed status overview, see:

    docs/status.md

## Roadmap

Near-term roadmap:

- v0.7.x: Configuration and artifact contract refinement
- v0.8.x: GitHub workflow validation
- v0.9.x: Stabilization before 1.0
- v1.0.0: Stable CLI and artifact contract

Detailed roadmap:

    docs/roadmap.md

v1.0 readiness checklist:

    docs/v1-readiness.md

## Non-goals

Reviewpack does not aim to:

- Automatically approve pull requests
- Automatically merge pull requests
- Replace human maintainers
- Spam line-by-line comments
- Upload code by default
- Require AI to be useful

## Design principles

1. Local-first
2. Privacy-first
3. AI-optional
4. Human-readable
5. Machine-readable
6. Maintainer-controlled
7. Tool-agnostic

Reviewpack should work with human reviewers, Codex, Cursor, Cline, OpenCode, Claude Code, GitHub Copilot, and other coding assistants.

## License

MIT
