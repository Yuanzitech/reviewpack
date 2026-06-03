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

## Core idea

Direct AI review:

    PR diff -> AI -> review comments

Reviewpack workflow:

    PR data -> local analysis -> structured context pack -> human reviewer or AI assistant

## Privacy-first by default

Reviewpack runs locally by default.

By default, it does not send code, diffs, branch names, commit messages, environment variables, repository metadata, or terminal information to any external service.

AI features, when added, will be optional and explicit. Users will be able to control what context is sent to an AI provider.

Current privacy-oriented features include:

- Local fixture mode
- Local git diff mode
- AI-ready prompt generation without AI calls
- AI input preview without AI calls
- Best-effort secret redaction for preview text
- No raw diff upload by default
- No branch name upload by default
- No commit message upload by default
- Local-first review pack generation

## Current status

Reviewpack is in early development.

The current milestone supports:

- Local fixture-based input
- Local git diff input
- Structured Markdown and JSON output
- Optional AI input preview generation
- Secret-like value redaction in preview text
- No network access by default
- No AI calls by default

## Install for local development

    python -m venv .venv
    source .venv/bin/activate
    pip install -e ".[dev]"

On Windows PowerShell:

    python -m venv .venv
    .venv\Scripts\Activate.ps1
    pip install -e ".[dev]"

## Usage

Generate a review pack from the example fixture:

    reviewpack from-fixture examples/fixtures/simple-pr.json --output .reviewpack

Generate a review pack with AI input preview:

    reviewpack from-fixture examples/fixtures/simple-pr.json --output .reviewpack --preview-ai-input

Generate a review pack from local git diff:

    reviewpack local --base main --head HEAD --output .reviewpack

Generate local git diff output with AI input preview:

    reviewpack local --base main --head HEAD --output .reviewpack --preview-ai-input

Use an optional config file:

    reviewpack from-fixture examples/fixtures/simple-pr.json --config .reviewpack.example.yml --output .reviewpack

Show the installed version:

    reviewpack version

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

## Documentation

- Usage guide: docs/usage.md
- Privacy model: docs/privacy.md
- Design notes: docs/design.md
- Local git diff mode: docs/local-git.md
- AI input preview: docs/ai-preview.md
- Examples guide: examples/README.md

## Roadmap

### v0.1.0

- Local fixture input
- Deterministic rule-based analysis
- Markdown review pack output
- JSON artifact output
- No network access
- No AI calls
- Basic tests and CI

### v0.2.0

- .reviewpack.yml configuration
- Local git diff mode
- AI input preview file
- Best-effort secret redaction
- More risk rules

### v0.3.0

- GitHub PR URL support
- GitHub token support
- Optional AI provider skeleton
- OpenAI provider support as opt-in

### v0.4.0

- GitHub Action integration
- Optional PR comment mode
- Release note hints
- More maintainer workflow automation

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
