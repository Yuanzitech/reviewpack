# Reviewpack v0.5.0

Reviewpack v0.5.0 improves the first-run CLI experience and AI handoff workflow.

This release makes Reviewpack easier to try after PyPI installation and easier to hand off to AI coding assistants without requiring users to copy large prompt files manually.

## Highlights

### First-run demo command

Reviewpack now includes:

    reviewpack demo

The demo command generates a complete synthetic review pack without requiring users to create fixture files manually.

Recommended first-run workflow:

    pip install reviewpack
    reviewpack demo
    reviewpack handoff

Reviewpack writes output to `.reviewpack/` by default.

### Product-oriented command guide

Reviewpack now includes:

    reviewpack guide

This command gives users a workflow-oriented command map.

It explains when to use:

- `reviewpack demo`
- `reviewpack github`
- `reviewpack local`
- `reviewpack from-fixture`
- `reviewpack handoff`

This complements the existing Typer CLI help:

    reviewpack --help

### AI handoff workflow

Reviewpack now generates:

    .reviewpack/ai-handoff.md

This lightweight file tells AI coding tools how to use Reviewpack artifacts in the `.reviewpack/` directory.

If an AI assistant can read workspace files, users can ask:

    Please read .reviewpack/ai-handoff.md and follow it.

### Single-file AI context bundle

Reviewpack now generates:

    .reviewpack/ai-context.md

This file combines the most useful Reviewpack context into one Markdown file.

It is useful when an AI assistant cannot read a local workspace but can accept one uploaded file.

Recommended fallback order:

1. If the AI assistant can read local files, use `.reviewpack/ai-handoff.md`.
2. If the AI assistant cannot read local files but can accept one uploaded file, upload `.reviewpack/ai-context.md`.
3. If only copy and paste is available, use `.reviewpack/ai-review-prompt.md`.

### Better first-run documentation

The README and installation guide now use the PyPI-first workflow:

    pip install reviewpack
    reviewpack demo

The documentation also clarifies that:

- `.reviewpack/` is the default output directory
- `--output PATH` is optional for custom output directories
- `from-fixture` requires an existing fixture file
- `reviewpack demo` is preferred for first-time usage

### Simplified Chinese README sync

The Simplified Chinese README has been updated with the new first-run workflow, AI handoff workflow, and AI context fallback guidance.

## What's changed since v0.4.0

### Added

- `reviewpack demo`
- `reviewpack handoff`
- `reviewpack guide`
- `.reviewpack/ai-handoff.md`
- `.reviewpack/ai-context.md`
- AI context renderer
- AI handoff documentation
- Commands guide
- Demo command tests
- AI handoff tests
- AI context tests
- CLI guide tests
- Chinese README updates for first-run and AI handoff workflows

### Changed

- Package version bumped to 0.5.0
- CLI version bumped to 0.5.0
- README now uses `pip install reviewpack` and `reviewpack demo` as the first-run workflow
- README now documents `ai-context.md` as the one-file upload fallback
- Installation guide now documents PyPI installation, demo workflow, and AI handoff fallback options
- Commands guide now documents AI handoff fallback options
- `reviewpack handoff` now explains fallback options for AI tools without file access
- `reviewpack guide` now explains AI handoff fallback options
- Reviewpack output now includes `ai-handoff.md` by default
- Reviewpack output now includes `ai-context.md` by default
- Fixture mode error message now suggests `reviewpack demo` for first-run usage
- Package workflow now verifies `ai-handoff.md` and `ai-context.md`
- TestPyPI install workflow now verifies `ai-handoff.md` and `ai-context.md`

## Why this release matters

Reviewpack v0.4.0 made the project publishing-ready and enabled official PyPI publication.

After the first PyPI release, the main user experience issue was clear: new users should not need to create fixture JSON files manually before seeing Reviewpack work.

Reviewpack v0.5.0 addresses that by making the first-run workflow:

    pip install reviewpack
    reviewpack demo

It also improves AI handoff by avoiding a copy-first workflow. Users can now point AI tools to `ai-handoff.md`, upload `ai-context.md`, or fall back to `ai-review-prompt.md` only when needed.

## Privacy notes

Reviewpack v0.5.0 does not add AI provider calls.

The new AI handoff and AI context files are generated locally.

They do not upload source code, raw diffs, branch names, commit messages, environment variables, or repository secrets.

The user remains in control of what is shared with AI tools.

## Known limitations

This release does not yet include:

- Direct AI provider integration
- Automatic PR comments
- Raw diff analysis
- Local AI provider integration
- IDE plugin integration
- MCP server integration

## Next steps

Planned next steps may include:

- GitHub Action UX polish
- Optional PR comment mode
- Stronger configuration support
- Optional AI provider interface
- More output examples
- Better rule customization
