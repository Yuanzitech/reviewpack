# Privacy Model

Reviewpack is designed to be local-first and privacy-first.

The default workflow does not require network access, API tokens, AI providers, GitHub credentials, or external services.

## Default behavior

By default, Reviewpack does not send any information to external services.

It does not upload:

- Source code
- Raw diffs
- Branch names
- Commit messages
- Environment variables
- Terminal information
- Local file system paths
- Git remote URLs
- Repository secrets
- API keys
- Tokens
- Private configuration files

The first milestone of Reviewpack works from local fixture data and generates local Markdown and JSON files.

## Local-first output

Reviewpack writes output files to a local directory such as:

    .reviewpack/pr-summary.md
    .reviewpack/risk-checklist.md
    .reviewpack/ai-review-prompt.md
    .reviewpack/reviewpack.json

These files are generated on the user's machine or inside the user's CI environment.

## AI is optional

Reviewpack does not require AI to be useful.

The core project is based on deterministic analysis:

- File category detection
- Test impact signals
- Documentation impact signals
- Dependency change signals
- CI and infrastructure change signals
- High-risk path detection
- Large PR detection

Future AI features should be explicit opt-in features.

## Planned AI privacy controls

When AI features are added, Reviewpack should follow these rules:

- AI is disabled by default
- Raw diffs are not sent by default
- Branch names are not sent by default
- Commit messages are not sent by default
- Users can preview AI input before sending
- Users can configure which fields are included
- Secret-like values should be redacted where possible
- AI output should be treated as suggestions for human maintainers

## Branch names

Branch names can contain sensitive information, such as customer names, incident names, private roadmap items, or security-related context.

For that reason, Reviewpack should not include branch names in AI-bound context unless the user explicitly opts in.

## Raw diffs

Raw diffs may contain source code, secrets, credentials, internal URLs, or business logic.

For that reason, Reviewpack should not send raw diffs to AI providers by default.

Future versions may support an explicit option to include diff snippets, but this must be opt-in and clearly documented.

## Maintainer control

Reviewpack should help maintainers prepare better context for review.

It should not:

- Automatically approve pull requests
- Automatically merge pull requests
- Automatically block pull requests
- Replace human maintainers
- Spam line-by-line AI comments by default

The maintainer should stay in control of how Reviewpack output is used.
