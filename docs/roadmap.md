# Roadmap

This roadmap outlines the planned direction for Reviewpack.

Reviewpack is a privacy-first context generator for AI-assisted pull request review. The roadmap focuses on improving maintainer workflows without requiring AI or uploading code by default.

## Current stage

Reviewpack already supports:

- Fixture-based input
- Local git diff input
- GitHub pull request metadata input
- Markdown and JSON output
- AI-ready prompt generation
- AI input preview generation
- Best-effort secret redaction
- Basic test coverage and CI

## Near-term priorities

### 1. Public launch polish

Goals:

- Improve README onboarding
- Add example output
- Improve roadmap and release notes
- Make the project easier to understand for first-time visitors

### 2. Stronger review artifacts

Potential additions:

- Reviewer checklist output
- Release note hints
- More explicit docs and test coverage summaries
- Better large-PR summaries
- More configurable risk rules

### 3. Better GitHub workflow support

Potential additions:

- Stronger GitHub error handling
- Better token guidance
- Optional GitHub Action integration
- Optional PR comment output
- Linked issue hints
- Maintainer-oriented review summaries

### 4. Safer AI integration

Potential additions:

- Provider interface abstraction
- Optional OpenAI provider
- Optional local provider support
- Improved redaction rules
- AI input inspection improvements
- Explicit AI usage reporting

## Planned milestones

### v0.1.x

Focus:

- Core local workflows
- Docs polish
- Examples polish
- Stable public repository presentation

### v0.2.x

Focus:

- Better rule coverage
- Better artifact quality
- Better AI preview quality
- Stronger privacy controls

### v0.3.x

Focus:

- Stronger GitHub metadata workflows
- More maintainer-focused output
- Better integration ergonomics

### v0.4.x

Focus:

- GitHub Actions integration
- Optional PR comments
- Release workflow support
- More automation for maintainers

## Out of scope for now

Not immediate priorities:

- Full source code upload
- Raw diff upload by default
- Automatic PR approval
- Automatic PR merge
- Autonomous review bot behavior
- Mandatory AI provider integration
- SaaS hosting

## Guiding principles

Reviewpack should remain:

- Local-first when possible
- Privacy-first by default
- Useful without AI
- Clear about what is collected
- Inspectable before anything is sent to AI
- Focused on helping maintainers, not replacing them
