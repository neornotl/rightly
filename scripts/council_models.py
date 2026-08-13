"""Shared council model registry (OpenRouter, NVIDIA NIM, local m365 proxy)."""

from __future__ import annotations

MEMBERS = [
    {
        "display": "gpt-4o-mini (OpenRouter)",
        "url": "https://openrouter.ai/api/v1/chat/completions",
        "key_env": "OPENROUTER_API_KEY",
        "model": "openai/gpt-4o-mini",
        "headers_extra": {"X-Title": "TienLang-Council"},
    },
    {
        "display": "nemotron-3-ultra (NIM)",
        "url": "https://integrate.api.nvidia.com/v1/chat/completions",
        "key_env": "NVIDIA_API_KEY",
        "model": "nvidia/nemotron-3-ultra-550b-a55b",
    },
    {
        "display": "gemini-flash-1.5 (OpenRouter)",
        "url": "https://openrouter.ai/api/v1/chat/completions",
        "key_env": "OPENROUTER_API_KEY",
        "model": "google/gemini-flash-1.5",
        "headers_extra": {"X-Title": "TienLang-Council"},
    },
    {
        "display": "claude-3.5-sonnet (OpenRouter)",
        "url": "https://openrouter.ai/api/v1/chat/completions",
        "key_env": "OPENROUTER_API_KEY",
        "model": "anthropic/claude-3.5-sonnet",
        "headers_extra": {"X-Title": "TienLang-Council"},
    },
    {
        "display": "m365-copilot (local proxy)",
        "url": "http://localhost:8000/v1/chat/completions",
        "key_env": None,
        "model": "m365-copilot",
    },
]

PROXY_URLS = ["http://localhost:8000", "http://localhost:3000"]