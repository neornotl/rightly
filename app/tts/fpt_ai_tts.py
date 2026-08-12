"""FPT.AI TTS Adapter (High-quality Vietnamese TTS with free tier).

FPT.AI provides excellent Vietnamese TTS with natural voices.
Free tier: 500 chars/request, 100 requests/day.
Voices: leminh (male), mai (female), linh (female), etc.
"""

from __future__ import annotations

import hashlib
import shutil
import subprocess
import time
from pathlib import Path
from typing import Optional

import requests

from app.tts.base import BaseTTS


class FPTAI_TTS(BaseTTS):
    """FPT.AI TTS with caching and WAV conversion."""

    name = "fpt_ai"

    # Available voices (FPT.AI)
    VOICES = {
        "leminh": "leminh",      # Male, deep, professional
        "mai": "mai",            # Female, warm, clear
        "linh": "linh",          # Female, young, energetic
        "thuminh": "thuminh",    # Female, gentle
        "quynh": "quynh",        # Female, standard
        "hoa": "hoa",            # Female, soft
    }

    def __init__(
        self,
        api_key: str,
        voice: str = "mai",
        speed: float = 0.9,       # Slightly slower for elderly
        cache_dir: Path = Path("results/tts_cache"),
        output_format: str = "wav",
    ):
        self.api_key = api_key
        self.voice = self.VOICES.get(voice.lower(), voice)
        self.speed = speed
        self.cache_dir = Path(cache_dir)
        self.output_format = output_format.lower()
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.api_url = "https://api.fpt.ai/hmi/tts/v5"

    @staticmethod
    def _cache_key(text: str, voice: str, speed: float) -> str:
        return hashlib.sha256(f"{voice}|{speed}|{text}".encode("utf-8")).hexdigest()[:24]

    def _cached_path(self, text: str) -> Path:
        return self.cache_dir / f"{self._cache_key(text, self.voice, self.speed)}.{self.output_format}"

    def _convert_to_wav(self, input_path: Path, output_path: Path) -> bool:
        """Convert audio to WAV using ffmpeg."""
        try:
            subprocess.run([
                "ffmpeg", "-y", "-i", str(input_path),
                "-ar", "16000", "-ac", "1", "-sample_fmt", "s16",
                str(output_path)
            ], check=True, capture_output=True, timeout=30)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return False

    def synthesize(
        self,
        text: str,
        output_path: str | Path,
        speed: Optional[float] = None,
    ) -> str:
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)

        use_speed = speed if speed is not None else self.speed
        cached = self._cached_path(text)

        if cached.exists():
            if out != cached:
                shutil.copy2(cached, out)
            return str(out)

        # FPT.AI TTS API call
        headers = {
            "api-key": self.api_key,
            "speed": str(use_speed),
            "voice": self.voice,
        }

        try:
            response = requests.post(
                self.api_url,
                headers=headers,
                data=text.encode("utf-8"),
                timeout=30
            )
            response.raise_for_status()
        except Exception as exc:
            raise RuntimeError(f"FPT.AI TTS request failed: {exc}") from exc

        # Response contains async URL, need to poll
        result = response.json()
        if result.get("error") != 0:
            raise RuntimeError(f"FPT.AI TTS error: {result.get('message', 'Unknown error')}")

        audio_url = result.get("async")
        if not audio_url:
            raise RuntimeError("FPT.AI TTS: No audio URL in response")

        # Poll for audio file
        max_attempts = 30
        for attempt in range(max_attempts):
            try:
                audio_resp = requests.get(audio_url, timeout=30)
                if audio_resp.status_code == 200:
                    break
            except Exception:
                pass
            time.sleep(1)
        else:
            raise RuntimeError("FPT.AI TTS: Timeout waiting for audio generation")

        # Save audio (FPT.AI returns MP3)
        mp3_path = out.with_suffix(".mp3")
        mp3_path.write_bytes(audio_resp.content)

        # Convert to requested format
        if self.output_format == "wav":
            if self._convert_to_wav(mp3_path, out):
                mp3_path.unlink(missing_ok=True)
            else:
                mp3_path.rename(out)
        else:
            if mp3_path != out:
                shutil.move(str(mp3_path), str(out))

        # Cache
        if cached != out:
            shutil.copy2(out, cached)

        return str(out)
