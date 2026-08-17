"""Shared council model registry (Pateway, OpenRouter, NVIDIA NIM, local m365)."""

from __future__ import annotations

MEMBERS = [
    {
        "display": "gpt-4o-mini (OpenRouter)",
        "url": "https://openrouter.ai/api/v1/chat/completions",
        "key_env": "OPENROUTER_API_KEY",
        "model": "openai/gpt-4o-mini",
        "headers_extra": {"X-Title": "TienLang-Council"},
        "vision": True,
        "max_tokens": 1000,
    },
    {
        "display": "gpt-5.6-luna (Pateway)",
        "url": "https://api.pateway.ai/v1/chat/completions",
        "key_env": "PATEWAY_API_KEY",
        "model": "gpt-5.6-luna",
        "vision": True,
    },
    {
        "display": "nemotron-3-ultra (NIM)",
        "url": "https://integrate.api.nvidia.com/v1/chat/completions",
        "key_env": "NVIDIA_API_KEY",
        "model": "nvidia/nemotron-3-ultra-550b-a55b",
        "vision": False,
    },
    {
        "display": "gemini-2.5-flash (OpenRouter)",
        "url": "https://openrouter.ai/api/v1/chat/completions",
        "key_env": "OPENROUTER_API_KEY",
        "model": "google/gemini-2.5-flash",
        "headers_extra": {"X-Title": "TienLang-Council"},
        "vision": True,
        "max_tokens": 800,
    },
    {
        "display": "claude-sonnet-4.6 (OpenRouter)",
        "url": "https://openrouter.ai/api/v1/chat/completions",
        "key_env": "OPENROUTER_API_KEY",
        "model": "anthropic/claude-sonnet-4.6",
        "headers_extra": {"X-Title": "TienLang-Council"},
        "vision": True,
        "max_tokens": 150,
    },
{
        "display": "m365-copilot (local proxy)",
        "url": "http://localhost:8000/v1/chat/completions",
        "key_env": None,
        "model": "m365-copilot",
        "vision": False,
    },
]

PROXY_URLS = ["http://localhost:8000", "http://localhost:3000"]
