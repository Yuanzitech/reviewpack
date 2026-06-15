# Configuration Schema

This document describes Reviewpack's current `.reviewpack.yml` configuration schema.

Reviewpack is not yet a stable 1.0 product, so the configuration schema is currently pre-1.0.

The goal of this document is to make the current configuration structure explicit.

## Configuration file

By default, Reviewpack looks for:

    .reviewpack.yml

in the current working directory.

Users can also pass a custom config file:

    reviewpack demo --config path/to/reviewpack.yml
    reviewpack local --config path/to/reviewpack.yml
    reviewpack github https://github.com/owner/repo/pull/123 --config path/to/reviewpack.yml

## Top-level sections

Current top-level sections:

    outputs
    risk
    paths

All sections are optional.

If no config file is present, Reviewpack uses defaults.

## outputs

The `outputs` section controls which output files Reviewpack writes.

Supported public keys:

    outputs:
      pr_summary: true
      risk_checklist: true
      reviewer_checklist: true
      release_note_hints: true
      ai_review_prompt: true
      ai_handoff: true
      ai_context: true
      json: true

## outputs.pr_summary

Controls whether Reviewpack writes:

    pr-summary.md

Default:

    true

## outputs.risk_checklist

Controls whether Reviewpack writes:

    risk-checklist.md

Default:

    true

## outputs.reviewer_checklist

Controls whether Reviewpack writes:

    reviewer-checklist.md

Default:

    true

## outputs.release_note_hints

Controls whether Reviewpack writes:

    release-note-hints.md

Default:

    true

## outputs.ai_review_prompt

Controls whether Reviewpack writes:

    ai-review-prompt.md

Default:

    true

## outputs.ai_handoff

Controls whether Reviewpack writes:

    ai-handoff.md

Default:

    true

## outputs.ai_context

Controls whether Reviewpack writes:

    ai-context.md

Default:

    true

## outputs.json

Controls whether Reviewpack writes:

    reviewpack.json

Default:

    true

The public configuration key is:

    json

Internally, Reviewpack maps this to:

    json_output

This avoids a Pydantic BaseModel field-name conflict.

Users should normally keep using:

    outputs:
      json: true

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

## risk.large_pr_files

If the number of changed files is greater than or equal to this value, Reviewpack emits a large pull request risk signal.

Default:

    20

## risk.large_pr_lines

If the number of added plus deleted lines is greater than or equal to this value, Reviewpack emits a large line change risk signal.

Default:

    500

## risk.high_risk_paths

List of paths or patterns that should be treated as high risk.

Default includes common sensitive paths such as:

    src/auth/
    auth/
    security/
    .github/workflows/
    pyproject.toml

Supported pattern styles:

- Directory prefix
- Exact file path
- Glob

Examples:

    risk:
      high_risk_paths:
        - .github/workflows/
        - pyproject.toml
        - src/*.py

## paths

The `paths` section controls file classification.

Current supported categories:

    docs
    tests
    dependencies
    ci
    config
    infrastructure

## paths.docs

Patterns classified as documentation.

Example:

    paths:
      docs:
        - docs/
        - README.md
        - README.zh-CN.md
        - CHANGELOG.md

## paths.tests

Patterns classified as tests.

Example:

    paths:
      tests:
        - tests/
        - test/
        - spec/

## paths.dependencies

Patterns classified as dependency files.

Example:

    paths:
      dependencies:
        - pyproject.toml
        - requirements.txt
        - requirements-dev.txt
        - poetry.lock
        - package.json
        - package-lock.json

## paths.ci

Patterns classified as CI files.

Example:

    paths:
      ci:
        - .github/workflows/
        - .gitlab-ci.yml
        - azure-pipelines.yml

## paths.config

Patterns classified as configuration files.

Example:

    paths:
      config:
        - .reviewpack.yml
        - ruff.toml
        - mypy.ini
        - pytest.ini

## paths.infrastructure

Patterns classified as infrastructure files.

Example:

    paths:
      infrastructure:
        - Dockerfile
        - docker-compose.yml
        - k8s/
        - deploy/
        - infra/
        - terraform/

## Pattern behavior

Reviewpack supports simple path matching.

### Directory prefix

Pattern:

    docs/

Matches:

    docs/usage.md
    docs/reference/configuration.md

### Exact file path

Pattern:

    pyproject.toml

Matches:

    pyproject.toml

### Glob

Pattern:

    src/*.py

Matches:

    src/app.py

## Practical example files

Reviewpack includes these example configuration files:

    examples/.reviewpack.yml
    examples/config/minimal.reviewpack.yml
    examples/config/python-project.reviewpack.yml
    examples/config/javascript-typescript-project.reviewpack.yml
    examples/config/monorepo.reviewpack.yml

These examples are validated by tests.

## Invalid configuration guidance

Reviewpack currently expects configuration files to be YAML mappings.

Valid shape:

    outputs:
      json: true

Invalid shape:

    - outputs
    - json

If the root YAML value is not a mapping, Reviewpack raises an error similar to:

    Reviewpack config must be a YAML mapping

## Unknown keys

Reviewpack currently uses Pydantic validation for configuration.

Users should prefer documented keys.

Unknown or unsupported behavior may become stricter before v1.0.

Future versions may add:

- stronger validation
- better error messages
- a `reviewpack validate` command
- a machine-readable config schema

## Common compatibility expectations

Before v1.0, Reviewpack aims to keep these stable where possible:

- `.reviewpack.yml` default file name
- `--config` CLI option
- public `outputs` keys
- public `risk` keys
- public `paths` keys
- public `outputs.json` key

The internal `json_output` field is implementation detail compatibility support.

Users should normally use:

    outputs:
      json: true

## Pre-1.0 stability

Before v1.0, Reviewpack aims to keep these stable where possible:

- `outputs` public keys
- `risk` public keys
- `paths` public keys
- `.reviewpack.yml` default file name
- `--config` CLI option

Before v1.0, Reviewpack may still refine:

- default thresholds
- default path patterns
- validation strictness
- advanced configuration sections

## Future schema work

Potential future improvements:

- Published JSON schema for `.reviewpack.yml`
- Schema validation command
- Better error messages for invalid config
- More examples for common project types
- Backward compatibility policy
- Deprecation policy
