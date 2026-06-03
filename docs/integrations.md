# Integration Principles

Reviewpack is designed to support multiple maintainer workflows without forcing users into a single AI provider or hosting model.

## Current integrations

Reviewpack currently supports:

- Local fixture input
- Local git diff input
- AI-ready prompt generation
- AI input preview generation

These modes are local-first and do not require network access.

## Planned integrations

Future integrations may include:

- GitHub pull request metadata
- GitHub Actions
- Optional PR comments
- Optional AI providers
- Local AI providers
- Release note hints
- Issue triage summaries

## Integration rules

Every integration should follow these principles:

1. Local-first behavior should remain available.
2. AI should be optional.
3. Network access should be explicit.
4. Tokens should be user-provided and never stored by Reviewpack.
5. Generated outputs should be inspectable.
6. Maintainers should stay in control.
7. Reviewpack should avoid noisy automated comments by default.

## GitHub integration

GitHub integration should be added in stages:

1. Parse GitHub PR URLs.
2. Fetch public PR metadata.
3. Support explicit GitHub tokens for private repositories.
4. Generate Reviewpack output from GitHub PR files.
5. Optionally support GitHub Actions.
6. Optionally support PR comments.

The current implementation only covers step 1.

## AI integration

AI integration should also be added in stages:

1. Generate AI-ready prompts locally.
2. Generate AI input preview locally.
3. Add redaction helpers.
4. Add provider configuration.
5. Add optional provider calls.
6. Add local provider support.

The current implementation covers the first three steps.

## Non-goals

Reviewpack integrations should not:

- Automatically approve pull requests
- Automatically merge pull requests
- Upload source code by default
- Send raw diffs by default
- Require AI provider tokens for basic use
- Store API keys or GitHub tokens
- Replace human maintainers
