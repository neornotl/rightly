"""Config tests: defaults, validation, and secret redaction."""

from __future__ import annotations

from pathlib import Path

from app.config import ConfigError, load_settings, safe_repr, safe_settings_summary

# Tests must be hermetic: never read a real .env from the repo root.
_NO_ENV = Path(__file__).resolve().parent / "_no_such_env_file.env"


def test_defaults_are_mock(monkeypatch):
    for key in ("APP_MODE", "ASR_BACKEND", "LLM_BACKEND", "TTS_BACKEND"):
        monkeypatch.delenv(key, raising=False)
    settings = load_settings(env_file=_NO_ENV)
    assert settings.app_mode == "mock"
    assert settings.asr_backend == "mock"
    assert settings.llm_backend == "mock"
    assert settings.tts_backend == "mock"
    assert settings.save_transcripts is False
    assert settings.delete_raw_audio_after_session is True


def test_invalid_mode_raises(monkeypatch):
    monkeypatch.setenv("APP_MODE", "bogus")
    try:
        load_settings(env_file=_NO_ENV)
        assert False, "expected ConfigError"
    except ConfigError as exc:
        assert "APP_MODE" in str(exc)


def test_boolean_env_parsing(monkeypatch):
    monkeypatch.setenv("SAVE_TRANSCRIPTS", "true")
    settings = load_settings(env_file=_NO_ENV)
    assert settings.save_transcripts is True


def test_safe_repr_redacts_secret_keys():
    assert safe_repr("sk-abc123", key="GEMINI_API_KEY") == "<REDACTED>"
    assert safe_repr("sk-abc123", key="API_KEY") == "<REDACTED>"
    assert safe_repr("hello", key="LLM_BACKEND") == "hello"


def test_settings_summary_never_contains_key_values():
    import os

    os.environ["GEMINI_API_KEY"] = "FAKE_GEMINI_KEY_FOR_LOGGING_TEST"
    settings = load_settings(env_file=_NO_ENV)
    summary = str(safe_settings_summary(settings))
    assert "FAKE_GEMINI_KEY_FOR_LOGGING_TEST" not in summary
    assert "set" in summary


def test_utf8_vietnamese_text_roundtrip():
    settings = load_settings(env_file=_NO_ENV)
    assert "Bộ phận một cửa" in settings.official_one_stop_label
    assert "Đường dây nóng" in settings.official_hotline_label


def test_default_min_retrieval_score_matches_rrf_scale(monkeypatch):
    monkeypatch.delenv("MIN_RETRIEVAL_SCORE", raising=False)
    settings = load_settings(env_file=_NO_ENV)
    assert settings.min_retrieval_score == 0.01
