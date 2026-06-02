# Usage

Reviewpack is currently in early development.

The first milestone supports local fixture-based input. This means you can generate a review context pack without GitHub API access, network access, AI calls, or external tokens.

## Install for local development

From the repository root:

    python -m venv .venv
    source .venv/bin/activate
    pip install -e ".[dev]"

On Windows PowerShell:

    python -m venv .venv
    .venv\Scripts\Activate.ps1
    pip install -e ".[dev]"

## Show version

    reviewpack version

## Generate a review pack from a fixture

    reviewpack from-fixture examples/fixtures/simple-pr.json --output .reviewpack

This writes:

    .reviewpack/pr-summary.md
    .reviewpack/risk-checklist.md
    .reviewpack/ai-review-prompt.md
    .reviewpack/reviewpack.json

## Use a config file

Copy the example configuration:

    cp .reviewpack.example.yml .reviewpack.yml

Then run:

    reviewpack from-fixture examples/fixtures/simple-pr.json --config .reviewpack.yml --output .reviewpack

## What the output means

### pr-summary.md

A human-readable summary of the pull request context.

It includes:

- Pull request title
- Author
- Description
- Change statistics
- Changed file list
- Suggested review focus
- Privacy notes

### risk-checklist.md

A deterministic checklist generated from local rules.

Examples:

- Source changed without tests
- Source changed without docs
- Dependency files changed
- CI workflow changed
- Infrastructure files changed
- High-risk paths changed
- Large pull request
- Large line change

### ai-review-prompt.md

A local AI-ready prompt.

This file is generated without calling any AI provider. You can copy it into your preferred coding assistant if you want AI-assisted review.

### reviewpack.json

A machine-readable JSON artifact.

Future integrations can use this file for GitHub Actions, review dashboards, release notes, or other maintainer workflows.

## Privacy behavior

The current fixture mode:

- Does not use network access
- Does not call GitHub APIs
- Does not call AI providers
- Does not upload source code
- Does not upload raw diffs
- Does not collect branch names
- Does not collect commit messages
- Does not collect environment variables
- Does not inspect terminal history

## Configuration fields

### risk_paths_high

Paths that should be treated as high risk.

Example:

    risk_paths_high:
      - "src/auth/**"
      - "src/security/**"
      - "src/payment/**"

### test_paths

Paths that should be treated as tests.

Example:

    test_paths:
      - "tests/**"
      - "__tests__/**"
      - "test/**"

### docs_paths

Paths that should be treated as documentation.

Example:

    docs_paths:
      - "README.md"
      - "docs/**"

### large_pr

Thresholds for large pull request detection.

Example:

    large_pr:
      changed_files: 20
      changed_lines: 800

### privacy

Privacy controls for future integrations.

Example:

    privacy:
      include_branch_name: false
      include_commit_messages: false
      include_diff_snippets: false
      include_file_paths: true
      redact_secrets: true

### ai

Reserved AI configuration.

AI is disabled by default.

Example:

    ai:
      enabled: false
      provider: null
      model: null
      max_input_chars: 12000

## Current limitations

Reviewpack does not yet support:

- Direct GitHub PR URL input
- Local git diff input
- GitHub Action PR comments
- AI provider calls
- Secret redaction implementation
- Release note generation

These are planned for future milestones.
