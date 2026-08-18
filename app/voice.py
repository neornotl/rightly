"""Hands-free browser audio processing helpers.

The browser still needs one explicit permission gesture. After that gesture,
the processor groups speech into utterances and emits a WAV file after a
short period of silence.
"""

from __future__ import annotations

import io
import queue
import threading
import wave

import numpy as np

try:
    from streamlit_webrtc import AudioProcessorBase
except ImportError:  # pragma: no cover - optional UI dependency
    AudioProcessorBase = object  # type: ignore[misc,assignment]


def encode_wav(samples: np.ndarray, sample_rate: int) -> bytes:
    """Encode mono float/int audio as 16-bit PCM WAV."""
    array = np.asarray(samples)
    if array.ndim > 1:
        array = array.mean(axis=0)
    if np.issubdtype(array.dtype, np.floating):
        array = np.clip(array, -1.0, 1.0) * 32767
    pcm = np.asarray(array, dtype=np.int16).tobytes()
    output = io.BytesIO()
    with wave.open(output, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        wav.writeframes(pcm)
    return output.getvalue()


class HandsFreeAudioProcessor(AudioProcessorBase):
    """Collect speech and emit one WAV payload after silence."""

    sample_rate = 16000
    silence_rms = 450.0
    end_silence_seconds = 0.9
    min_speech_seconds = 0.25

    def __init__(self):
        self._lock = threading.Lock()
        self._frames: list[np.ndarray] = []
        self._speech_samples = 0
        self._silence_samples = 0
        self._last_rms = 0.0
        self._received_frames = 0
        self._ready: queue.Queue[bytes] = queue.Queue()

    def recv(self, frame):  # pragma: no cover - exercised by browser/WebRTC
        samples = frame.to_ndarray()
        if samples.ndim > 1:
            samples = samples.mean(axis=0)
        samples = np.asarray(samples, dtype=np.float32).reshape(-1)
        rate = int(getattr(frame, "sample_rate", 0) or self.sample_rate)
        self.sample_rate = rate
        rms = float(np.sqrt(np.mean(np.square(samples)))) if samples.size else 0.0
        with self._lock:
            self._last_rms = rms
            self._received_frames += 1
            if rms >= self.silence_rms:
                self._frames.append(samples.copy())
                self._speech_samples += samples.size
                self._silence_samples = 0
            elif self._frames:
                self._frames.append(samples.copy())
                self._silence_samples += samples.size
                if self._silence_samples >= self.end_silence_seconds * rate:
                    if self._speech_samples >= self.min_speech_seconds * rate:
                        audio = np.concatenate(self._frames)
                        self._ready.put(encode_wav(audio, rate))
                    self._frames = []
                    self._speech_samples = 0
                    self._silence_samples = 0
        return frame

    def pop_audio(self) -> bytes | None:
        try:
            return self._ready.get_nowait()
        except queue.Empty:
            return None

    @property
    def status(self) -> tuple[float, int, bool]:
        """Return microphone level, received frame count, and speech state."""
        with self._lock:
            return self._last_rms, self._received_frames, bool(self._frames)
