"""Check the runtime environment and print a summary table.

Usage:
    python scripts/check_environment.py
"""

from __future__ import annotations

import platform
import sys


def main() -> int:
    print("== Tieng Lang environment check ==")
    print(f"Python: {sys.version.split()[0]} ({sys.executable})")
    print(f"OS: {platform.platform()}")
    try:
        import psutil  # type: ignore  # noqa: F401

        mem = psutil.virtual_memory()
        print(f"RAM: {mem.total / 1e9:.1f} GB total, {mem.available / 1e9:.1f} GB available")
        cpu = psutil.cpu_count(logical=True)
        print(f"CPU: {cpu} logical cores")
    except ImportError:
        import os

        print("RAM: (psutil not installed; reading via os)")
        mem_kb = 0
        if hasattr(os, "sysconf"):
            try:
                mem_kb = os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES")
            except (ValueError, OSError):
                mem_kb = 0
        print(f"RAM (approx): {mem_kb / 1e6:.1f} GB" if mem_kb else "RAM: unknown")
        print("CPU: unknown (install psutil for details)")

    checks = []
    try:
        import dotenv  # noqa: F401

        checks.append(("python-dotenv", True))
    except ImportError:
        checks.append(("python-dotenv", False))
    for mod in ("faster_whisper", "edge_tts", "streamlit", "google.genai", "groq"):
        try:
            __import__(mod)
            checks.append((mod, True))
        except ImportError:
            checks.append((mod, False))
    print("\nOptional modules:")
    for name, ok in checks:
        print(f"  {name}: {'OK' if ok else 'MISSING'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
