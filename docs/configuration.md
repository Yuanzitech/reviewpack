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

## Practical examples

Reviewpack includes practical example configuration files:

    examples/.reviewpack.yml
    examples/config/minimal.reviewpack.yml
    examples/config/python-project.reviewpack.yml
    examples/config/javascript-typescript-project.reviewpack.yml
    examples/config/monorepo.reviewpack.yml

Use these files as starting points.

### Minimal example

Use this when you want a small configuration that keeps Reviewpack defaults mostly intact:

    examples/config/minimal.reviewpack.yml

### Python project example

Use this for Python packages or services that use common files such as:

    pyproject.toml
    requirements.txt
    requirements-dev.txt
    poetry.lock
    pytest.ini
    ruff.toml
    mypy.ini

Example:

    examples/config/python-project.reviewpack.yml

### JavaScript / TypeScript project example

Use this for JavaScript or TypeScript projects that use common files such as:

    package.json
    package-lock.json
    pnpm-lock.yaml
    yarn.lock
    tsconfig.json
    eslint.config.js

Example:

    examples/config/javascript-typescript-project.reviewpack.yml

### Monorepo example

Use this for repositories with multiple apps, packages, or services.

Example:

    examples/config/monorepo.reviewpack.yml

The monorepo example uses broader path patterns such as:

    apps/*/tests/
    packages/*/tests/
    services/*/tests/

## outputs

The `outputs` section controls which files Reviewpack writes.

Supported public configuration keys:

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

### json output key

The public configuration key is:

    json

Internally, Reviewpack maps this to `json_output` to avoid a Pydantic BaseModel field-name conflict.

Users should normally keep using:

    outputs:
      json: true

The output file name remains:

    reviewpack.json

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

## Invalid configuration guidance

Reviewpack currently expects the configuration file to be a YAML mapping.

Valid top-level example:

    outputs:
      json: true

Invalid top-level example:

    - outputs
    - json

If a configuration file is not a YAML mapping, Reviewpack raises an error similar to:

    Reviewpack config must be a YAML mapping

Current public top-level sections are:

    outputs
    risk
    paths

Users should prefer documented keys.

Reviewpack is still pre-1.0, so validation behavior may become stricter before v1.0.

## Common configuration mistakes

### Using json_output instead of json

The public key should normally be:

    outputs:
      json: true

The internal field name `json_output` exists to avoid a Pydantic conflict, but user-facing configuration should prefer `json`.

### Forgetting that config is optional

You do not need a config file to use Reviewpack.

A config file is useful when you want to customize:

- output files
- risk thresholds
- high-risk paths
- path classification

### Using path patterns that are too broad

For example:

    paths:
      docs:
        - src/

This would classify everything under `src/` as documentation.

Prefer more specific patterns.

### Expecting raw diff analysis

Configuration does not enable raw diff analysis.

Reviewpack does not collect raw diffs by default.

## Privacy behavior

Configuration does not change Reviewpack's privacy defaults.

Reviewpack still does not call AI providers by default.

Reviewpack still does not upload raw diffs or full source code by default.

Configuration affects local analysis and output generation behavior.

## Future configuration work

Potential future improvements:

- `reviewpack validate` command
- published machine-readable config schema
- better invalid config error messages
- more project-specific examples
- compatibility and deprecation policy before v1.0

## Related docs

See:

    docs/config-schema.md
    docs/artifact-contract.md
    docs/json-output.md
