# Installation

Reviewpack is currently an early-stage CLI tool.

This document explains current and planned installation options.

## Current recommended installation

Until Reviewpack is published to PyPI, install it from source.

Clone the repository:

    git clone https://github.com/Yuanzitech/reviewpack.git
    cd reviewpack

Create a virtual environment:

    python -m venv .venv
    source .venv/bin/activate

Install Reviewpack in editable mode:

    pip install -e ".[dev]"

Show the installed version:

    reviewpack version

Run the example fixture:

    reviewpack from-fixture examples/fixtures/simple-pr.json --output .reviewpack

## Windows PowerShell

Create and activate a virtual environment:

    python -m venv .venv
    .venv\Scripts\Activate.ps1

Install Reviewpack:

    pip install -e ".[dev]"

Run the example fixture:

    reviewpack from-fixture examples/fixtures/simple-pr.json --output .reviewpack

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
    reviewpack from-fixture examples/fixtures/simple-pr.json --output .reviewpack-smoke

Expected smoke test output files:

    .reviewpack-smoke/pr-summary.md
    .reviewpack-smoke/risk-checklist.md
    .reviewpack-smoke/reviewer-checklist.md
    .reviewpack-smoke/release-note-hints.md
    .reviewpack-smoke/ai-review-prompt.md
    .reviewpack-smoke/reviewpack.json

## GitHub Action usage

Reviewpack can also run in GitHub Actions.

See:

    docs/github-action.md

Example workflow:

    examples/github-action.yml

## Future PyPI installation

Reviewpack is not yet published to PyPI.

After PyPI publishing is ready, the intended installation command will be:

    pip install reviewpack

For isolated CLI installation, pipx may be recommended:

    pipx install reviewpack

## Verify installation

After installation, run:

    reviewpack version

You can also run:

    reviewpack from-fixture examples/fixtures/simple-pr.json --output .reviewpack

Expected output files include:

    .reviewpack/pr-summary.md
    .reviewpack/risk-checklist.md
    .reviewpack/reviewer-checklist.md
    .reviewpack/release-note-hints.md
    .reviewpack/ai-review-prompt.md
    .reviewpack/reviewpack.json

If `--preview-ai-input` is enabled, Reviewpack also writes:

    .reviewpack/ai-input-preview.md

## Current limitations

Current source installation requires:

- Python 3.10 or newer
- pip
- git, for cloning the repository
- network access during dependency installation

PyPI publishing is planned for a future release.
