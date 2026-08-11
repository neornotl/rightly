"""WER/MOS Logging Middleware (P0 - BẮT BUỘC cho pilot 13/08).

Log mỗi session: ASR_conf, TTS_dur, user_rating, intent, latency, route, source_ids.
Export CSV cho báo cáo rubric M1 (Impact & Inclusion).
"""

from __future__ import annotations

import csv
import json
import os
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Optional

from app.schemas import PipelineResult

LOG_DIR = Path(os.environ.get("LOG_DIR", "data/logs"))
LOG_DIR.mkdir(parents=True, exist_ok=True)

CSV_PATH = LOG_DIR / "wer_mos_log.csv"
JSONL_PATH = LOG_DIR / "wer_mos_log.jsonl"


@dataclass
class SessionMetrics:
    session_id: str
    timestamp: str
    user_id_hash: str
    query_text: str
    normalized_query: str
    intent: str
    decision_zone: str
    decision_action: str
    reason_codes: str
    retrieval_ms: float
    safety_ms: float
    llm_ms: float
    tts_ms: float
    total_ms: float
    source_ids: str
    num_chunks: int
    asr_confidence: Optional[float] = None
    asr_transcript: Optional[str] = None
    wer: Optional[float] = None
    mos: Optional[float] = None
    user_rating: Optional[int] = None  # 1-5
    feedback_text: Optional[str] = None


class MetricsLogger:
    def __init__(self, csv_path: Path = CSV_PATH, jsonl_path: Path = JSONL_PATH):
        self.csv_path = csv_path
        self.jsonl_path = jsonl_path
        self._init_csv()

    def _init_csv(self):
        if not self.csv_path.exists():
            with open(self.csv_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "session_id", "timestamp", "user_id_hash", "query_text",
                    "normalized_query", "intent", "decision_zone", "decision_action",
                    "reason_codes", "retrieval_ms", "safety_ms", "llm_ms",
                    "tts_ms", "total_ms", "source_ids", "num_chunks",
                    "asr_confidence", "asr_transcript", "wer", "mos",
                    "user_rating", "feedback_text"
                ])

    def log(self, metrics: SessionMetrics):
        # CSV
        with open(self.csv_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                metrics.session_id, metrics.timestamp, metrics.user_id_hash,
                metrics.query_text, metrics.normalized_query, metrics.intent,
                metrics.decision_zone, metrics.decision_action, metrics.reason_codes,
                metrics.retrieval_ms, metrics.safety_ms, metrics.llm_ms,
                metrics.tts_ms, metrics.total_ms, metrics.source_ids,
                metrics.num_chunks, metrics.asr_confidence, metrics.asr_transcript,
                metrics.wer, metrics.mos, metrics.user_rating, metrics.feedback_text
            ])
        # JSONL (cho Elasticsearch/Logstash)
        with open(self.jsonl_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(metrics), ensure_ascii=False) + "\n")

    def export_summary(self) -> dict:
        """Tổng hợp nhanh cho dashboard."""
        if not self.csv_path.exists():
            return {"sessions": 0}
        import pandas as pd
        df = pd.read_csv(self.csv_path)
        return {
            "sessions": len(df),
            "avg_total_ms": df["total_ms"].mean(),
            "avg_llm_ms": df["llm_ms"].mean(),
            "zone_dist": df["decision_zone"].value_counts().to_dict(),
            "action_dist": df["decision_action"].value_counts().to_dict(),
            "avg_wer": df["wer"].mean() if "wer" in df.columns else None,
            "avg_mos": df["mos"].mean() if "mos" in df.columns else None,
            "avg_rating": df["user_rating"].mean() if "user_rating" in df.columns else None,
        }


# Singleton
_metrics_logger: Optional[MetricsLogger] = None


def get_metrics_logger() -> MetricsLogger:
    global _metrics_logger
    if _metrics_logger is None:
        _metrics_logger = MetricsLogger()
    return _metrics_logger


def log_pipeline_result(
    session_id: str,
    user_id: str,
    query_text: str,
    normalized_query: str,
    result: PipelineResult,
    asr_confidence: Optional[float] = None,
    asr_transcript: Optional[str] = None,
    wer: Optional[float] = None,
    mos: Optional[float] = None,
    user_rating: Optional[int] = None,
    feedback_text: Optional[str] = None,
):
    """Helper để log từ pipeline result."""
    lat = result.latencies_ms
    total = sum(v for v in lat.values() if isinstance(v, (int, float)))
    source_ids = ",".join(c.source_id for c in result.chunks)
    reason_codes = ",".join(result.decision.reason_codes)

    # Intent từ router (đơn giản hóa)
    zone = result.decision.zone.value
    if zone == "RED":
        intent = "emergency"
    elif zone == "ORANGE":
        if "FAKE_LAW_REFERENCE" in result.decision.reason_codes:
            intent = "fake_law"
        elif "CRIMINAL_MATTER" in result.decision.reason_codes:
            intent = "criminal"
        elif "LEGAL_JUDGMENT_REQUEST" in result.decision.reason_codes:
            intent = "legal_judgment"
        elif "OUT_OF_SCOPE" in result.decision.reason_codes:
            intent = "out_of_scope"
        else:
            intent = "orange_other"
    else:
        intent = "legal_info"

    metrics = SessionMetrics(
        session_id=session_id,
        timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        user_id_hash=str(hash(user_id))[:8],
        query_text=query_text[:500],
        normalized_query=normalized_query[:500],
        intent=intent,
        decision_zone=zone,
        decision_action=result.decision.action.value,
        reason_codes=reason_codes,
        retrieval_ms=lat.get("retrieval_ms", 0),
        safety_ms=lat.get("safety_ms", 0),
        llm_ms=lat.get("llm_ms", 0),
        tts_ms=lat.get("tts_ms", 0),
        total_ms=total,
        source_ids=source_ids,
        num_chunks=len(result.chunks),
        asr_confidence=asr_confidence,
        asr_transcript=asr_transcript,
        wer=wer,
        mos=mos,
        user_rating=user_rating,
        feedback_text=feedback_text,
    )
    get_metrics_logger().log(metrics)
