"""OpenVINO / CPU ASR benchmark for the Intel loan machine (F4-prep, honest).

Runs PhoWhisper (faster-whisper, ctranslate2) on real Vietnamese audio and
records latency + WER + peak memory. On a laptop WITHOUT NPU (i7-10510U) it
reports CPU-only; on the loaned Intel AI PC (Core Ultra) the same script also
tries the NPU device.

Usage:
    python scripts/benchmark_openvino.py                      # VIVOS if present
    python scripts/benchmark_openvino.py --audio <dir-or-file> [--refs refs.jsonl]

Outputs: results/hardware_benchmark.csv (append) — text+metrics only, raw
audio is never copied into the repo. Ref lines: {"audio": "...", "reference": "..."}.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

OUT_CSV = ROOT / "results" / "hardware_benchmark.csv"


def _detect_devices() -> list[str]:
    devices = ["CPU"]
    try:
        import openvino as ov  # type: ignore

        core = ov.Core()
        available = {d.split(".")[0] for d in core.available_devices}
        if "NPU" in available:
            devices.append("NPU")
    except Exception:  # noqa: BLE001 - openvino may not be installed
        devices.append("(openvino not installed)")
    return devices


def _refs_map(path: Path) -> dict[str, str]:
    refs: dict[str, str] = {}
    if path and path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            rec = json.loads(line)
            refs[Path(rec["audio"]).stem] = rec["reference"]
    return refs


def main() -> int:
    ap = argparse.ArgumentParser(description="OpenVINO/CPU ASR benchmark")
    ap.add_argument("--audio", default="", help="wav file or dir (default: VIVOS test)")
    ap.add_argument("--refs", default="", help="optional JSONL with reference transcripts")
    ap.add_argument("--limit", type=int, default=10, help="max clips")
    args = ap.parse_args()

    print(
        f"Devices: {', '.join(_detect_devices())} (demo machine has NO NPU; "
        "run on the loaned AI PC for NPU numbers)"
    )

    wavs: list[Path] = []
    audio_arg = args.audio or str(ROOT / "data" / "private_cache" / "vivos" / "test" / "waves")
    apath = Path(audio_arg)
    if apath.is_dir():
        wavs = sorted(apath.rglob("*.wav"))[: args.limit]
    elif apath.exists():
        wavs = [apath]
    if not wavs:
        print("NO audio found. Provide --audio or add VIVOS under data/private_cache.")
        return 1

    refs = _refs_map(Path(args.refs)) if args.refs else {}

    from app.asr.phowhisper_asr import PhoWhisperASR
    from eval.wer import evaluate_wer  # noqa: E402

    asr = PhoWhisperASR()
    rows: list[dict] = []
    for wav in wavs:
        try:
            start = time.perf_counter()
            res = asr.transcribe(wav)
            latency = res.latency_ms or round((time.perf_counter() - start) * 1000.0, 1)
            hyp = res.transcript
        except Exception as exc:  # noqa: BLE001
            print(f"ERROR {wav.stem}: {exc}")
            hyp, latency = "", -1.0
        ref = refs.get(wav.stem, "")
        wer = None
        if ref:
            (wer, _s, _i, _d), _ = evaluate_wer([{"reference": ref, "hypothesis": hyp}])
        rows.append(
            {
                "device": "CPU",
                "audio": wav.name,
                "audio_seconds": round(_wav_duration_seconds(wav), 2),
                "asr_ms": round(latency, 1),
                "wer": "n/a" if wer is None else round(wer, 4),
            }
        )
        print(
            f"  {wav.name}: {round(latency, 1)}ms" + (f" wer={wer:.1%}" if wer is not None else "")
        )

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    header = list(rows[0]) if rows else ["device", "audio", "audio_seconds", "asr_ms", "wer"]
    with OUT_CSV.open("a", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=header)
        if fh.tell() == 0:
            writer.writeheader()
        writer.writerows(rows)
    print(f"Saved -> {OUT_CSV}")
    return 0


def _wav_duration_seconds(path: Path) -> float:
    try:
        import wave

        with wave.open(str(path), "rb") as wf:
            return wf.getnframes() / float(wf.getframerate() or 1)
    except Exception:  # noqa: BLE001
        return 0.0


if __name__ == "__main__":
    raise SystemExit(main())
