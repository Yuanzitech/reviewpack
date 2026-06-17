# Changelog

All notable changes to this project will be documented in this file.

 to 0.5.0This project follows a simple changelog format during early development.
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

### Fixed

- Nothing.

## v0.4.0 - 2026-06-03

### Added

- Manual PyPI publishing workflow
- PyPI release checklist
- TestPyPI verification guide
- Publish workflow metadata tests

### Changed

- Package version bumped to 0.4.0
- CLI version bumped to 0.4.0
- Expanded PyPI publishing notes with manual workflow and TestPyPI guidance

### Fixed

- Nothing.

## v0.3.0 - 2026-06-03

### Added

- Installation guide
- PyPI publishing notes
- Package build workflow
- Package metadata tests
- Installed wheel smoke test in package workflow
- Wheel installation smoke test documentation

### Changed

- Package version bumped to 0.3.0
- CLI version bumped to 0.3.0
- README now links to installation documentation
- Package workflow now verifies that the installed wheel exposes a working `reviewpack` CLI

### Fixed

- Nothing.

## v0.2.0 - 2026-06-03

### Added

- Reviewer checklist output
- Reviewer checklist renderer
- Reviewer checklist tests
- Reviewer checklist documentation
- GitHub Action metadata
- GitHub Action usage guide
- GitHub Action workflow example
- GitHub Action metadata tests
- Release note hints output
- Release note hints renderer
- Release note hints tests
- Release note hints documentation

### Changed

- Package version bumped to 0.2.0
- CLI version bumped to 0.2.0
- README now documents reviewer checklist output
- README now documents GitHub Action usage
- README now documents release note hints output
- CLI output now lists `reviewer-checklist.md`
- CLI output now lists `release-note-hints.md`
- Reviewpack output now includes `reviewer-checklist.md` by default
- Reviewpack output now includes `release-note-hints.md` by default

### Fixed

- Nothing.

## v0.1.0 - 2026-06-03

### Added

- Simplified Chinese README
- Language links in README
- Public roadmap
- Draft release notes for v0.1.0
- Example PR summary output
- Contributing guide
- Security policy
- Bug report issue template
- Feature request issue template
- Pull request template
- Release checklist
- GitHub API metadata collector
- `reviewpack github` command
- Optional GitHub token support
- GitHub metadata collector tests
- GitHub pull request URL parser
- GitHub URL parser tests
- GitHub integration guide
- Integration principles documentation
- AI input preview generation through `--preview-ai-input`
- Local AI input preview renderer
- Best-effort secret redaction helper
- Tests for AI input preview rendering
- Tests for secret redaction behavior
- AI input preview documentation
- Local git diff mode through `reviewpack local`
- Local git numstat parser
- Tests for local git diff parsing
- Local git diff mode documentation
- Configuration loading tests
- Usage guide
- Privacy model documentation
- Design notes
- Example Reviewpack configuration
- Examples guide
- Initial project metadata
- Privacy-first project positioning
- Local-first roadmap
- Planned CLI workflow
- MIT license

### Changed

- Improved README quick start and public launch messaging
- Updated project URLs to https://github.com/Yuanzitech/reviewpack
- Expanded README with GitHub metadata workflow
- Expanded GitHub documentation with metadata mode
- Expanded README with AI input preview usage
- Expanded CLI output to include optional AI input preview file
- Expanded README with installation, usage, and documentation links
- CI now opts into Node.js 24 for GitHub Actions
- Ruff configuration relaxed for early Typer-based CLI development

### Fixed

- Declared Hatchling wheel package configuration
- Moved source files into the `reviewpack` package directory

## Unreleased

### Added

- Nothing yet.

### Changed

- Nothing yet.

### Fixed

- Nothing yet.

## v0.7.0 - 2026-06-15

### Added

- Artifact contract documentation
- Configuration schema documentation
- JSON output documentation
- v1.0 readiness checklist
- Contract tests for default output artifact generation
- Contract tests for configurable output artifact generation
- Contract tests for `reviewpack.json` top-level structure
- Contract tests for pull request JSON fields
- Contract tests for changed file JSON fields
- Contract tests for stats JSON fields
- Contract tests for risk signal JSON fields
- Contract tests for review focus JSON fields
- Contract tests for public `.reviewpack.yml` configuration keys
- Contract tests for `outputs.json` compatibility
- Documentation link contract tests for README-linked files
- GitHub Action contract tests for stable inputs and defaults
- GitHub Action contract tests for opt-in comment mode
- GitHub Action contract tests for artifact upload behavior
- GitHub Action contract tests for next-step guidance
- GitHub Action example workflow tests
- GitHub Action documentation permission and fork limitation tests
- Draft JSON schema for `reviewpack.json`
- JSON integration guidance for consumers of Reviewpack output
- Tests validating demo `reviewpack.json` output against the draft schema
- Tests for file category and risk level schema enums
- Minimal `.reviewpack.yml` example
- Python project `.reviewpack.yml` example
- JavaScript / TypeScript project `.reviewpack.yml` example
- Monorepo `.reviewpack.yml` example
- Tests for loading example configuration files
- Tests ensuring example configuration files use the public `outputs.json` key
- Output examples README
- Example `pr-summary.md` output
- Example `ai-review-prompt.md` output
- Example `reviewpack.json` output
- Tests for example output artifact files
- Tests for example output Markdown sections
- Tests for example `reviewpack.json` top-level and nested fields
- Final v0.7 stabilization docs and link coverage

### Changed

- Package version bumped to 0.7.0
- CLI version bumped to 0.7.0
- Project status updated for v0.7.0 stabilization foundation
- Roadmap updated after v0.7.0 stabilization foundation
- README now links to artifact contract, config schema, JSON output, JSON integration, and v1.0 readiness docs
- Simplified Chinese README now links to artifact contract, config schema, JSON output, JSON integration, and v1.0 readiness docs
- Output artifacts documentation now links to `examples/output/`
- Artifact contract documentation now links to `examples/output/`
- Configuration guide now links to practical example config files
- Configuration schema docs now include practical examples and invalid config guidance
- GitHub Action documentation now clarifies artifact-only and comment mode permissions
- GitHub Action documentation now includes troubleshooting for token, permission, fork PR, and artifact issues
- JSON integration guide now more clearly explains pre-1.0 schema expectations
- Documentation link tests now cover `schemas/reviewpack-result.schema.json`
- Documentation link tests now cover `examples/config/`
- Documentation link tests now cover `examples/output/`
- TestPyPI install verification workflow default package version updated to 0.7.0
- PyPI install verification workflow default package version updated to 0.7.0

### Fixed

- Nothing.

## v0.6.1 - 2026-06-15

### Added

- Package smoke test now fails on Reviewpack config import `UserWarning`
- Test coverage for importing Reviewpack config with `UserWarning` treated as errors

### Changed

- Package version bumped to 0.6.1
- CLI version bumped to 0.6.1
- Internal output config field renamed from `json` to `json_output`
- Public `.reviewpack.yml` key `outputs.json` remains supported through a Pydantic alias
- Configuration documentation now clarifies the public `json` output key
- TestPyPI install verification workflow default package version updated to 0.6.1
- PyPI install verification workflow default package version updated to 0.6.1

### Fixed

- Fixed Pydantic warning caused by `OutputConfig.json` shadowing `BaseModel.json`

## v0.6.0 - 2026-06-15

### Added

- Project status document
- GitHub Action local mode example
- Configuration model for Reviewpack outputs, risk thresholds, and path classification
- Configurable output generation
- Configurable large PR thresholds
- Configurable high-risk paths
- Configurable docs, tests, dependencies, CI, config, and infrastructure path patterns
- Configuration guide
- Example `.reviewpack.yml`
- Configuration tests
- Configurable rules tests
- Output artifacts documentation
- Example risk checklist output
- Example reviewer checklist output
- Example release note hints output
- Example AI handoff output
- Example AI context output
- GitHub PR state metadata
- GitHub PR draft status metadata
- GitHub PR base and head branch metadata
- GitHub PR commit count metadata
- GitHub PR labels metadata
- GitHub changed file status metadata
- Tests for enriched GitHub metadata collection
- Tests for enriched GitHub metadata rendering
- Optional PR comment mode for the GitHub Action
- GitHub PR comment helper
- Stable Reviewpack PR comment marker
- GitHub Action comment mode example
- Tests for Reviewpack PR comment rendering and marker detection
- Action metadata tests for optional PR comment mode

### Changed

- Package version bumped to 0.6.0
- CLI version bumped to 0.6.0
- Roadmap updated after v0.5.0
- README now links to project status and updated roadmap
- Simplified Chinese README now links to project status and updated roadmap
- GitHub Action now prints clearer next-step guidance after generation
- GitHub Action artifact upload now includes hidden Reviewpack output directories
- GitHub Action documentation now explains artifact download and AI handoff usage
- GitHub Action examples updated to v0.5.0
- README now explains GitHub Action artifact usage
- Simplified Chinese README now explains GitHub Action artifact usage
- GitHub Action metadata tests now cover next-step guidance and hidden artifact uploads
- CLI commands now load `.reviewpack.yml` by default when present
- CLI commands now support `--config` for custom configuration files
- File classification now uses configurable path patterns
- Risk detection now uses configurable thresholds and high-risk paths
- README now documents configuration support
- Simplified Chinese README now documents configuration support
- Risk checklist output is now more actionable with why-it-matters and what-to-check sections
- Reviewer checklist output is now more structured around maintainer review areas
- Release note hints now include suggested maintainer actions and decision questions
- AI context output now includes review objective and known limitations sections
- README now links to output artifact documentation and example outputs
- Simplified Chinese README now links to output artifact documentation and example outputs
- GitHub mode now includes enriched PR metadata in generated artifacts when available
- PR summary now displays GitHub PR state, draft status, branches, commit count, and labels when available
- AI review prompt now includes enriched GitHub PR metadata when available
- AI context now includes enriched GitHub PR metadata when available
- GitHub API error messages are now more actionable for common authentication, rate limit, and not found cases
- GitHub documentation now describes enriched metadata collection boundaries
- Commands guide now documents enriched GitHub metadata behavior
- README now documents enriched GitHub metadata behavior
- Simplified Chinese README now documents enriched GitHub metadata behavior
- GitHub Action now supports `comment: "true"` as an explicit opt-in
- GitHub Action documentation now explains PR comment permissions and fork limitations
- README now documents optional PR comment mode
- Simplified Chinese README now documents optional PR comment mode
- TestPyPI install verification workflow default package version updated to 0.6.0
- PyPI install verification workflow default package version updated to 0.6.0

### Fixed

- Nothing.

## v0.5.0 - 2026-06-08

### Added

- `reviewpack demo` command
- `reviewpack handoff` command
- `reviewpack guide` command
- AI handoff output file
- AI context bundle output file
- AI context renderer
- AI handoff documentation
- AI context fallback guidance in AI handoff documentation
- Commands guide
- Demo command tests
- AI handoff tests
- AI context tests
- CLI guide tests
- Chinese README updates for first-run and AI handoff workflows

### Changed

- Package version bumped to 0.5.0
