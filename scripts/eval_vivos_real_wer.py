"""R1 with real audio: 30 VIVOS test clips (real human Vietnamese speech).

Pipeline: deterministic sample from VIVOS test set -> PhoWhisper-base
transcription (CPU) -> WER vs official prompts. Outputs JSONL of cases and
WER summary, plus a manifest CSV. Audio files live in data/private_cache
(never committed); only texts and metrics are written to the repo.
"""

from __future__ import annotations

import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from eval.wer import evaluate_wer  # noqa: E402

TEST_DIR = ROOT / "data" / "private_cache" / "vivos" / "test"
PROMPTS = TEST_DIR / "prompts.txt"
WAV_ROOT = TEST_DIR / "waves"
N_SAMPLES = 30
SEED = 42
CACHE_SAMPLE_SR = 16000


def _load_prompts() -> dict[str, str]:
    records: dict[str, str] = {}
    for line in PROMPTS.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        key, _, text = line.partition(" ")
        records[key] = text.strip()
    return records


def main() -> int:
    prompts = _load_prompts()
    all_wavs = sorted(WAV_ROOT.rglob("*.wav"))
    usable = [w for w in all_wavs if w.stem in prompts]
    print(f"prompts: {len(prompts)} | wavs: {len(all_wavs)} | usable: {len(usable)}")
    if len(usable) < N_SAMPLES:
        print("FAIL: not enough usable clips")
        return 1

    random.Random(SEED).shuffle(usable)
    sample = usable[:N_SAMPLES]

    from app.asr.phowhisper_asr import PhoWhisperASR

    asr = PhoWhisperASR()
    cases = []
    for wav in sample:
        reference = prompts[wav.stem]
        try:
            result = asr.transcribe(wav)
            hyp = result.transcript
            latency = result.latency_ms
        except Exception as exc:  # noqa: BLE001
            print(f"ERROR transcribing {wav.stem}: {exc}")
            hyp, latency = "", -1.0
        cases.append(
            {
                "case_id": wav.stem,
                "accent_group": "vivos_test",
                "reference": reference,
                "hypothesis": hyp,
                "latency_ms": round(latency, 1),
                "audio": str(wav.relative_to(ROOT)),
            }
        )

    cases_path = ROOT / "data" / "eval" / "vivos_wer_cases.jsonl"
    cases_path.parent.mkdir(parents=True, exist_ok=True)
    with cases_path.open("w", encoding="utf-8") as fh:
        for c in cases:
            fh.write(json.dumps(c, ensure_ascii=False) + "\n")

    rows, summary = evaluate_wer([{k: v for k, v in c.items() if k != "audio"} for c in cases])
    out_json = ROOT / "results" / "wer_summary_real_vivos.json"
    out_json.parent.mkdir(exist_ok=True)
    out_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"WER (real VIVOS, {len(cases)} clips): {summary['wer']:.4f}")
    print(f"median_wer: {summary['median_wer']:.4f} | p90_wer: {summary['p90_wer']:.4f}")
    print(f"cases -> {cases_path.relative_to(ROOT)}")
    print(f"summary -> {out_json.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
