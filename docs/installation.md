# Installation

Reviewpack is available on PyPI.

## Install from PyPI

Install Reviewpack:

    pip install reviewpack

Verify installation:

    reviewpack version

Generate a demo review pack:

    reviewpack demo

Reviewpack writes output to `.reviewpack/` by default.

## First-run workflow

Recommended first-run workflow:

    pip install reviewpack
    reviewpack demo
    reviewpack handoff

The `demo` command does not require users to create fixture files manually.

It generates a synthetic review pack for first-run exploration.

## GitHub pull request workflow

If you already have a GitHub pull request URL:

    reviewpack github https://github.com/owner/repo/pull/123

Public repositories usually do not require a token.

Private repositories or rate-limited usage may require:

    REVIEWPACK_GITHUB_TOKEN=YOUR_TOKEN reviewpack github https://github.com/owner/repo/pull/123

## Local development workflow

If you are working in a local git repository:

    reviewpack local

By default, Reviewpack writes files to:

    .reviewpack/

## Fixture workflow

Fixture mode is still available:

    reviewpack from-fixture simple-pr.json

The fixture file must already exist.

For first-time usage, prefer:

    reviewpack demo

## AI handoff

After generating a review pack, run:

    reviewpack handoff

Then ask your AI assistant:

    Please read .reviewpack/ai-handoff.md and follow it.

If the AI assistant cannot access local files, upload or paste:

    .reviewpack/ai-review-prompt.md

## Install from source for development

Clone the repository:

    git clone https://github.com/Yuanzitech/reviewpack.git
    cd reviewpack

Create a virtual environment:

    python -m venv .venv
    source .venv/bin/activate

Install Reviewpack in editable mode:

    pip install -e ".[dev]"

Run tests:

    pytest

Run lint checks:

    ruff check .

## Windows PowerShell

Create and activate a virtual environment:

    python -m venv .venv
    .venv\Scripts\Activate.ps1

Install from PyPI:

    pip install reviewpack

Or install from source:

    pip install -e ".[dev]"

## Install from a built wheel

Reviewpack can be built into Python distribution files.

Install build tooling:

    python -m pip install --upgrade pip
    python -m pip install build

Build the package:

    python -m build

Install the generated wheel in a clean environment:

    python -m venv .smoke
    source .smoke/bin/activate
    python -m pip install --upgrade pip
    python -m pip install dist/*.whl

Verify the CLI:

    reviewpack version
    reviewpack demo
