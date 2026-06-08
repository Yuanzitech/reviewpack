# Configuration

Reviewpack can be configured with a `.reviewpack.yml` file.

Configuration is optional.

If no configuration file is present, Reviewpack uses privacy-first defaults.

## Default config path

By default, Reviewpack looks for:

    .reviewpack.yml

in the current working directory.

You can also pass a custom config path:

    reviewpack demo --config path/to/reviewpack.yml
    reviewpack local --config path/to/reviewpack.yml
    reviewpack github https://github.com/owner/repo/pull/123 --config path/to/reviewpack.yml

## Example configuration

Example:

    outputs:
      pr_summary: true
      risk_checklist: true
      reviewer_checklist: true
      release_note_hints: true
      ai_review_prompt: true
      ai_handoff: true
      ai_context: true
      json: true

    risk:
      large_pr_files: 20
      large_pr_lines: 500
      high_risk_paths:
        - .github/workflows/
        - pyproject.toml
        - reviewpack/github_client.py

    paths:
      docs:
        - docs/
        - README.md
        - README.zh-CN.md
      tests:
        - tests/
      dependencies:
        - pyproject.toml
        - requirements.txt
        - package.json
      ci:
        - .github/workflows/
      config:
        - .reviewpack.yml
        - ruff.toml
      infrastructure:
        - Dockerfile
        - docker-compose.yml
        - infra/

## outputs

The `outputs` section controls which files Reviewpack writes.

Supported values:

    outputs:
      pr_summary: true
      risk_checklist: true
      reviewer_checklist: true
      release_note_hints: true
      ai_review_prompt: true
      ai_handoff: true
      ai_context: true
      json: true

If an output is set to `false`, Reviewpack will skip that file.

Example:

    outputs:
      ai_context: false
      release_note_hints: false

## risk

The `risk` section controls deterministic risk thresholds and high-risk paths.

Example:

    risk:
      large_pr_files: 20
      large_pr_lines: 500
      high_risk_paths:
        - .github/workflows/
        - pyproject.toml
        - reviewpack/github_client.py

### large_pr_files

If the number of changed files is greater than or equal to this value, Reviewpack emits a large pull request risk signal.

### large_pr_lines

If the number of added plus deleted lines is greater than or equal to this value, Reviewpack emits a large line change risk signal.

### high_risk_paths

Paths that should be treated as high risk.

Supported pattern styles:

- Directory prefix: `.github/workflows/`
- Exact file path: `pyproject.toml`
- Glob: `src/*.py`

## paths

The `paths` section controls file classification.

Reviewpack uses file categories to compute statistics, risk signals, reviewer checklist items, and release note hints.

Supported categories:

- docs
- tests
- dependencies
- ci
- config
- infrastructure

Example:

    paths:
      docs:
        - docs/
        - README.md
      tests:
        - tests/
        - spec/
      dependencies:
        - pyproject.toml
        - uv.lock
      ci:
        - .github/workflows/
      config:
        - .reviewpack.yml
      infrastructure:
        - Dockerfile
        - infra/

## Pattern behavior

Reviewpack supports simple path matching:

### Directory prefix

    docs/

Matches:

    docs/usage.md
    docs/reference/configuration.md

### Exact file path

    pyproject.toml

Matches:

    pyproject.toml

### Glob

    src/*.py

Matches:

    src/app.py

## Privacy behavior

Configuration does not change Reviewpack's privacy defaults.

Reviewpack still does not call AI providers by default.

Reviewpack still does not upload raw diffs or full source code by default.

Configuration affects local analysis and output generation behavior.

## Example file

See:

    examples/.reviewpack.yml
