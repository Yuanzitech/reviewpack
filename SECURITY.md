# Security Policy

Reviewpack is a privacy-first developer tool for generating structured pull request review context.

## Supported versions

Reviewpack is currently in early development.

Security fixes are handled on the main branch until the project starts publishing stable releases.

## Reporting a vulnerability

If you believe you found a security issue, please do not open a public issue with sensitive details.

Instead, please report it privately through GitHub security advisories if available, or contact the maintainers through a private channel.

When reporting a vulnerability, include:

- Affected version or commit
- Description of the issue
- Steps to reproduce
- Potential impact
- Suggested fix, if known

## Security design principles

Reviewpack should follow these principles:

- Local-first by default
- AI optional
- No source code upload by default
- No raw diff upload by default
- No branch name collection by default
- No commit message collection by default
- No token storage
- No token logging
- Generated outputs should be inspectable

## Token handling

Reviewpack may support user-provided tokens for integrations such as GitHub.

Tokens should:

- Be provided explicitly by the user
- Be read from supported environment variables when needed
- Never be stored by Reviewpack
- Never be written to generated output files
- Never be printed in normal CLI output

## AI-related security

AI-related features should remain explicit and opt-in.

Before any context is sent to an AI provider, users should be able to understand what will be included.

Reviewpack should avoid sending by default:

- Raw diffs
- Full source code
- Branch names
- Commit messages
- Environment variables
- Git remote URLs
- API tokens
- Repository secrets

## Secret redaction

Reviewpack includes best-effort redaction helpers for common secret-like values.

This is not a complete secret scanner.

Users should still avoid placing sensitive data in input files, pull request descriptions, or generated outputs.
