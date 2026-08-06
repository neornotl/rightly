"""PhoWhisper ASR adapter (optional, lazy).

Requires ``faster-whisper`` and model weights that are downloaded at runtime
(deliberate human decision; see docs/hardware_benchmark_plan.md).
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from app.asr.base import ASRResult, BaseASR


class PhoWhisperASR(BaseASR):
    """faster-whisper-based ASR tuned for Vietnamese (PhoWhisper family).

    The import of ``faster_whisper`` happens lazily in ``transcribe``, so the
    rest of the app runs fine without it. If the model/weights are missing,
    :meth:`check_availability` returns a clear message.
    """

    name = "phowhisper"

    def __init__(
        self,
        model_size: str = "small",
        device: str = "cpu",
        compute_type: str = "int8",
        language: str = "vi",
        model_path: Optional[str] = None,
    ):
        self.model_size = model_size
        self.device = device
        self.compute_type = compute_type
        self.language = language
        self.model_path = model_path
        self._model = None
        self._model_error: Optional[str] = None

    def check_availability(self) -> tuple[bool, str]:
        """Return (available, message). Does NOT download anything."""
        try:
            import faster_whisper  # noqa: F401
        except ImportError:
            return False, (
                "faster-whisper is not installed. Run: pip install -r requirements-optional.txt"
            )
        if self._model_error:
            return False, self._model_error
        return True, "ready"

    def _load(self):
        if self._model is not None:
            return self._model
        try:
            from faster_whisper import WhisperModel
        except ImportError as exc:
            raise RuntimeError(
                "faster-whisper is not installed. pip install -r requirements-optional.txt"
            ) from exc
        try:
            if self.model_path:
                self._model = WhisperModel(
                    self.model_path, device=self.device, compute_type=self.compute_type
                )
            else:
                self._model = WhisperModel(
                    self.model_size, device=self.device, compute_type=self.compute_type
                )
        except Exception as exc:  # network errors, OOM, missing weights
            self._model_error = f"Failed to load Whisper model: {exc}"
            raise RuntimeError(self._model_error) from exc
        return self._model

    def transcribe(self, audio_path: str | Path) -> ASRResult:
        import time

        self.check_audio_file(audio_path)
        model = self._load()
        start = time.perf_counter()
        segments, info = model.transcribe(str(audio_path), language=self.language, beam_size=5)
        parts = [seg.text for seg in segments]
        transcript = " ".join(parts).strip()
        latency_ms = (time.perf_counter() - start) * 1000.0
        if not transcript:
            raise RuntimeError("PhoWhisper returned empty transcript.")
        return ASRResult(
            transcript=transcript,
            latency_ms=round(latency_ms, 1),
            backend=self.name,
        )
