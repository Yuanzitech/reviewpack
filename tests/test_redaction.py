from reviewpack.redaction import REDACTION_TEXT, redact_text


def test_redact_api_key_assignment() -> None:
    text = "api_key=sk-test1234567890abcdef"
    redacted = redact_text(text)

    assert REDACTION_TEXT in redacted
    assert "sk-test1234567890abcdef" not in redacted


def test_redact_token_assignment() -> None:
    text = "token: ghp_abcdefghijklmnopqrstuvwxyz123456"
    redacted = redact_text(text)

    assert REDACTION_TEXT in redacted
    assert "ghp_abcdefghijklmnopqrstuvwxyz123456" not in redacted


def test_redact_bearer_token() -> None:
    text = "Authorization: Bearer secret-token-value"
    redacted = redact_text(text)

    assert REDACTION_TEXT in redacted
    assert "secret-token-value" not in redacted


def test_non_secret_text_is_preserved() -> None:
    text = "src/auth/session.py changed without tests"

    assert redact_text(text) == text
