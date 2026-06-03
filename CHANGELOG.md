# Changelog

All notable changes to this project will be documented in this file.

This project follows a simple changelog format during early development.

## Unreleased

### Added

- Trusted publishing guide
- TestPyPI runbook

### Changed

- Expanded PyPI publishing notes with trusted publishing and TestPyPI runbook links
- Expanded PyPI release checklist with trusted publishing and TestPyPI setup checks

### Fixed

- Nothing yet.

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
