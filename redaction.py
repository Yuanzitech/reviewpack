from __future__ import annotations

import re


REDACTION_TEXT = "[REDACTED]"


SECRET_PATTERNS = [
    re.compile(
        r"(?i)(api[_-]?key|token|password|passwd|secret|client[_-]?secret)\s*[:=]\s*['\"]?[^'\"\s]+['\"]?"
    ),
    re.compile(r"(?i)(authorization:\s*bearer\s+)[a-z0-9._\-]+"),
    re.compile(r"ghp_[A-Za-z0-9_]{20,}"),
    re.compile(r"gho_[A-Za-z0-9_]{20,}"),
    re.compile(r"ghu_[A-Za-z0-9_]{20,}"),
    re.compile(r"ghs_[A-Za-z0-9_]{20,}"),
    re.compile(r"sk-[A-Za-z0-9_\-]{20,}"),
]


def redact_text(text: str) -> str:
    """Redact common secret-like values from text.

    This is a best-effort helper. It is not a complete secret scanner.
    Reviewpack should still avoid collecting sensitive content by default.
    """

    redacted = text

    for pattern in SECRET_PATTERNS:
        redacted = pattern.sub(_replace_match, redacted)

    return redacted


def _replace_match(match: re.Match[str]) -> str:
    """Replace a regex match with a redacted marker.

    For key-value patterns, keep the key name and redact the value.
    For bearer tokens, keep the authorization prefix and redact the token.
    For standalone token patterns, replace the whole value.
    """

    text = match.group(0)

    if ":" in text or "=" in text:
        separator = ":" if ":" in text else "="
        key = text.split(separator, maxsplit=1)[0].strip()
        return f"{key}{separator} {REDACTION_TEXT}"

    if text.lower().startswith("authorization: bearer"):
        return f"Authorization: Bearer {REDACTION_TEXT}"

    return REDACTION_TEXT
