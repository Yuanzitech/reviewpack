# Commands

This page summarizes the main Reviewpack commands.

Reviewpack writes output to `.reviewpack/` by default.

Use `--output PATH` if you want a different output directory.

## Quick start

Install Reviewpack:

    pip install reviewpack

Generate a demo review pack:

    reviewpack demo

Show a product-oriented guide:

    reviewpack guide

Show AI handoff instructions:

    reviewpack handoff

## reviewpack demo

Generate a demo review context pack without creating input files manually.

    reviewpack demo

Output directory:

    .reviewpack/

Custom output directory:

    reviewpack demo --output demo-pack

With AI input preview:

    reviewpack demo --preview-ai-input

Use this command for first-run testing.

## reviewpack github

Generate a review context pack from a GitHub pull request URL.

    reviewpack github https://github.com/owner/repo/pull/123

Custom output directory:

    reviewpack github https://github.com/owner/repo/pull/123 --output review-output

Public repositories usually do not require a token.

Private repositories and rate-limited situations may require a GitHub token.

Recommended local token usage:

    REVIEWPACK_GITHUB_TOKEN=YOUR_TOKEN reviewpack github https://github.com/owner/repo/pull/123

GitHub mode collects pull request metadata and changed file statistics.

It does not collect raw diffs or full source code by default.

## reviewpack local

Generate a review context pack from local git diff statistics.

    reviewpack local

By default, this compares:

    main...HEAD

Custom refs:

    reviewpack local --base main --head feature-branch

Local mode does not require GitHub API access.

It only uses local git metadata.

## reviewpack from-fixture

Generate a review context pack from a fixture JSON file.

    reviewpack from-fixture simple-pr.json

The fixture file must already exist.

For first-time usage, prefer:

    reviewpack demo

Fixture mode is useful for:

- Tests
- Examples
- Offline verification
- Integrations that generate Reviewpack-compatible JSON

## reviewpack handoff

Show short instructions for handing generated Reviewpack files to an AI assistant.

    reviewpack handoff

Default output directory:

    .reviewpack/

Custom output directory:

    reviewpack handoff --output review-output

Recommended AI instruction when the AI assistant can read local files:

    Please read .reviewpack/ai-handoff.md and follow it.

If the AI assistant cannot read local files but can accept an uploaded file, upload:

    .reviewpack/ai-context.md

If only copy and paste is available, use:

    .reviewpack/ai-review-prompt.md

## reviewpack guide

Show a short product-oriented guide.

    reviewpack guide

This is different from `reviewpack --help`.

Use `reviewpack guide` when you want to know which workflow to use.

Use `reviewpack --help` when you want CLI options.

## reviewpack version

Show the installed Reviewpack version.

    reviewpack version

## CLI help

Reviewpack also supports command-level help:

    reviewpack --help
    reviewpack demo --help
    reviewpack github --help
    reviewpack local --help
    reviewpack from-fixture --help
