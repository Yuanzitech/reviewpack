# Contributing to Reviewpack

Thanks for your interest in contributing to Reviewpack.

Reviewpack is a privacy-first context generator for AI-assisted pull request review. The project focuses on helping maintainers prepare structured, reusable review context without uploading code or requiring AI by default.

## Project goals

Reviewpack aims to:

- Help maintainers understand pull requests faster
- Generate structured review context packs
- Support human and AI-assisted review workflows
- Stay local-first where possible
- Keep AI optional
- Keep maintainers in control

## Good first contributions

Good starting points include:

- Improving documentation
- Adding tests
- Improving file categorization rules
- Adding risk signal rules
- Improving examples
- Improving error messages
- Adding privacy-focused safeguards

## Development setup

From the repository root:

    python -m venv .venv
    source .venv/bin/activate
    pip install -e ".[dev]"

On Windows PowerShell:

    python -m venv .venv
    .venv\Scripts\Activate.ps1
    pip install -e ".[dev]"

## Run checks

Run tests:

    pytest

Run lint checks:

    ruff check .

Generate a review pack from fixture data:

    reviewpack from-fixture examples/fixtures/simple-pr.json --output .reviewpack

Generate with AI input preview:

    reviewpack from-fixture examples/fixtures/simple-pr.json --output .reviewpack --preview-ai-input

## Contribution workflow

1. Open an issue or pick an existing issue.
2. Create a focused branch.
3. Make a small, reviewable change.
4. Add or update tests when behavior changes.
5. Update documentation when user-facing behavior changes.
6. Run tests and lint checks.
7. Open a pull request with a clear description.

## Pull request expectations

A good pull request should include:

- Clear motivation
- Summary of changes
- Tests for behavior changes
- Documentation updates when needed
- Notes about privacy impact, if any

## Privacy expectations

Reviewpack should avoid collecting or sending sensitive information by default.

Contributions should preserve these principles:

- Do not upload source code by default
- Do not send raw diffs by default
- Do not collect branch names by default
- Do not collect commit messages by default
- Do not store user tokens
- Do not print tokens in logs
- Keep AI features optional and explicit

## AI-related contributions

AI-related features should be designed carefully.

Before adding AI provider calls, consider:

- What exact context is sent?
- Can the user preview it?
- Is the feature opt-in?
- Are secrets redacted where possible?
- Is the output clearly marked as a suggestion?
- Can the tool remain useful without AI?

## Code style

The project currently uses:

- Python 3.10+
- Typer for CLI
- Pydantic for models
- Pytest for tests
- Ruff for linting

Keep changes simple, typed, and well tested.

## Non-goals

Reviewpack does not aim to:

- Automatically approve pull requests
- Automatically merge pull requests
- Replace human maintainers
- Spam pull requests with noisy comments
- Require AI provider tokens for basic use
- Upload code by default
