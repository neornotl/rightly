"""Edge-TTS adapter (optional, lazy import; requires network at runtime).

Uses the public Microsoft Edge TTS endpoint. Audio is generated from text
only; no microphone data ever leaves the machine via this adapter.
"""

from __future__ import annotations

import asyncio
import hashlib
from pathlib import Path

from app.tts.base import BaseTTS


class EdgeTTS(BaseTTS):
    name = "edge"

    def __init__(
        self,
        voice: str = "vi-VN-HoaiMyNeural",
        rate: str = "+0%",
        cache_dir: Path = Path("results/tts_cache"),
    ):
        self.voice = voice
        self.rate = rate
        self.cache_dir = Path(cache_dir)

    @staticmethod
    def _cache_key(text: str, voice: str, rate: str) -> str:
        return hashlib.sha256(f"{voice}|{rate}|{text}".encode("utf-8")).hexdigest()[:24]

    def _cached_path(self, text: str, voice: str, rate: str) -> Path:
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        return self.cache_dir / f"{self._cache_key(text, voice, rate)}.mp3"

    def synthesize(
        self,
        text: str,
        output_path: str | Path,
        rate: str = "+0%",
    ) -> str:
        try:
            import edge_tts  # type: ignore
        except ImportError as exc:
            raise RuntimeError(
                "edge-tts not installed. pip install -r requirements-optional.txt"
            ) from exc

        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        cached = self._cached_path(text, self.voice, rate)
        if cached.exists():
            # Reuse cached audio to avoid repeat network calls.
            if out != cached:
                import shutil

                shutil.copy2(cached, out)
            return str(out)
        try:
            asyncio.run(edge_tts.Communicate(text=text, voice=self.voice, rate=rate).save(str(out)))
        except Exception as exc:
            raise RuntimeError(f"Edge-TTS synthesis failed: {exc}") from exc
        if cached != out:
            import shutil

            shutil.copy2(out, cached)
        return str(out)
