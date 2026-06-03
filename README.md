# Reviewpack

Privacy-first context packs for AI-assisted pull request review.

Reviewpack helps open-source maintainers and engineering teams prepare structured, reusable context before reviewing a pull request with a human reviewer or an AI coding assistant.

It is not another noisy AI reviewer. Reviewpack is a context layer: it collects pull request metadata, changed files, test signals, documentation signals, dependency signals, risk indicators, and review focus areas into a clear review pack.

## Why Reviewpack?

AI coding tools are powerful, but review quality depends heavily on context.

Direct AI review often starts from raw diffs. That can miss important project-level signals:

- Which files are high risk?
- Were tests updated?
- Were docs updated?
- Did dependencies change?
- Is the pull request too large?
- Does the change affect CI, configuration, or release behavior?
- What should a maintainer focus on first?

Reviewpack prepares that context before review starts.

## Quick Start

Install for local development:

    python -m venv .venv
    source .venv/bin/activate
    pip install -e ".[dev]"

Generate a review pack from the example fixture:

    reviewpack from-fixture examples/fixtures/simple-pr.json --output .reviewpack

Generate a review pack with AI input preview:

    reviewpack from-fixture examples/fixtures/simple-pr.json --output .reviewpack --preview-ai-input

Open the generated files:

    .reviewpack/pr-summary.md
    .reviewpack/risk-checklist.md
    .reviewpack/ai-review-prompt.md
    .reviewpack/reviewpack.json

## Example Output

Example PR summary:

    examples/output/pr-summary.example.md

This gives a quick view of the type of structured review context Reviewpack produces.

## Core idea

Direct AI review:

    PR diff -> AI -> review comments

Reviewpack workflow:

    PR data -> local analysis -> structured context pack -> human reviewer or AI assistant

## Supported input modes

Reviewpack currently supports:

- Fixture input
- Local git diff input
- GitHub pull request metadata input

Examples:

    reviewpack from-fixture examples/fixtures/simple-pr.json --output .reviewpack

    reviewpack local --base main --head HEAD --output .reviewpack

    reviewpack github https://github.com/owner/repo/pull/123 --output .reviewpack

## Privacy-first by default

Reviewpack runs locally by default for fixture and local git workflows.

By default, it does not send code, diffs, branch names, commit messages, environment variables, repository metadata, or terminal information to any external AI service.

GitHub mode uses network access only to fetch explicitly requested pull request metadata and changed file statistics from the GitHub API.

AI features, when added, will be optional and explicit. Users will be able to control what context is sent to an AI provider.

Current privacy-oriented features include:

- Local fixture mode
- Local git diff mode
- GitHub PR metadata mode
- AI-ready prompt generation without AI calls
- AI input preview without AI calls
- Best-effort secret redaction for preview text
- No raw diff upload by default
- No branch name upload by default
- No commit message upload by default
- Local-first review pack generation where possible

## What Reviewpack generates

A review pack may include:

- PR summary
- Changed file overview
- Risk checklist
- Test impact
- Documentation impact
- Dependency impact
- CI and configuration impact
- Suggested review focus
- AI-ready review prompt
- AI input preview
- Machine-readable JSON output

Example output directory:

    .reviewpack/pr-summary.md
    .reviewpack/risk-checklist.md
    .reviewpack/ai-review-prompt.md
    .reviewpack/ai-input-preview.md
    .reviewpack/reviewpack.json

## Current status

Reviewpack is in early development.

The current milestone supports:

- Local fixture-based input
- Local git diff input
- GitHub PR metadata input
- Structured Markdown and JSON output
- Optional AI input preview generation
- Secret-like value redaction in preview text
- No AI calls by default

## Documentation

- Usage guide: docs/usage.md
- Privacy model: docs/privacy.md
- Design notes: docs/design.md
- Local git diff mode: docs/local-git.md
- GitHub support: docs/github.md
- AI input preview: docs/ai-preview.md
- Integration principles: docs/integrations.md
- Roadmap: docs/roadmap.md
- Release checklist: docs/release-checklist.md
- Examples guide: examples/README.md

## Roadmap

High-level roadmap:

- v0.1.x: polish core local workflows
- v0.2.x: improve privacy-aware AI preview and configuration
- v0.3.x: strengthen GitHub pull request workflows
- v0.4.x: add GitHub Actions integration and maintainer automation

Detailed roadmap:

    docs/roadmap.md

## Why this project exists

Reviewpack exists because AI-assisted review is only as good as the context it receives.

Instead of replacing maintainers, Reviewpack helps maintainers prepare better review context:

- locally when possible
- explicitly when network access is needed
- inspectably before any AI provider is involved
- with privacy-aware defaults

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
