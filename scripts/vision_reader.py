"""Round 14 — vision reader: send the submission-screenshot PNG to vision-capable
council members, collect their readings into the pool (debate_output/vision_round14.json).
"""

from __future__ import annotations

import base64
import json
import os
import sys
import urllib.request

IMAGE = r"C:\Users\laptopppp\Downloads\768303436_977051945358641_2784924474550321218_n.png"

PROMPT = """Bạn là thành viên hội đồng của đội thi "Rightly" (AI voice-first cho
người cao tuổi VN; thi Intel Vietnam AI Impact Festival 2026 — KHÔNG phải VAIFF).

Ảnh đính kèm là ảnh chụp màn hình (screenshot) liên quan tới cuộc thi này — có thể là
một phần Google Form nộp bài, bảng tiêu chí chấm điểm, yêu cầu video, hoặc cơ cấu giải.

Nhiệm vụ của bạn (vision member): ĐỌC ẢNH một cách chi tiết và chính xác bằng tiếng
Việt. BẮT BUỘC xuất ra:
1) LOẠI ẢNH: là gì (form? rubric? tiêu chí? thông báo?)
2) TOÀN BỘ VĂN BẢN/chữ trong ảnh, chuyển thành text rõ ràng, giữ nguyên các con số,
   dấu đầu dòng, bảng (ghi đúng tiếng Việt có dấu, không bỏ sót mục nào).
3) Nếu ảnh chứa tiêu chí/trọng số/điểm số → liệt kê CHÍNH XÁC từng dòng với số liệu.
4) Dòng chữ nào mờ/không đọc được → ghi rõ [KHÔNG ĐỌC ĐƯỢC].
5) Kết luận ngắn: thông tin quan trọng nhất mà đội cần dùng ngay (tối đa 5 dòng).

KHÔNG suy đoán, KHÔNG bịa số liệu. Chỉ báo cáo những gì nhìn thấy trong ảnh."""


def read_b64() -> str:
    with open(IMAGE, "rb") as f:
        return base64.b64encode(f.read()).decode()


def post_json(url: str, payload: dict, headers: dict) -> dict | str:
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", **headers},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:  # noqa: BLE001
        return f"ERROR: {e}"


def msg_openai(image_b64: str, model: str) -> dict:
    return {
        "model": model,
        "max_tokens": 4096,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": PROMPT},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{image_b64}"},
                    },
                ],
            }
        ],
    }


def main() -> None:
    image_b64 = read_b64()
    results: dict = {"image": IMAGE, "bytes": len(image_b64) * 3 // 4, "readings": {}}

    gemini_key = os.environ.get("GEMINI_API_KEY", "")
    if gemini_key:
        for model in ["gemini-2.0-flash", "gemini-2.5-flash"]:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": PROMPT},
                            {
                                "inline_data": {
                                    "mime_type": "image/png",
                                    "data": image_b64,
                                }
                            },
                        ]
                    }
                ]
            }
            r = post_json(url, payload, {"x-goog-api-key": gemini_key})
            if isinstance(r, dict) and "candidates" in r:
                text = r["candidates"][0]["content"]["parts"][0]["text"]
                results["readings"][f"gemini-{model}"] = {"status": "OK", "text": text}
                break
            results["readings"][f"gemini-{model}"] = {"status": "FAIL", "raw": str(r)[:500]}

    groq_key = os.environ.get("GROQ_API_KEY", "")
    if groq_key:
        r = post_json(
            "https://api.groq.com/openai/v1/chat/completions",
            msg_openai(image_b64, "llama-3.2-11b-vision-preview"),
            {"Authorization": f"Bearer {groq_key}"},
        )
        if isinstance(r, dict) and "choices" in r:
            results["readings"]["groq-llama3.2-11b-vision"] = {
                "status": "OK",
                "text": r["choices"][0]["message"]["content"],
            }
        else:
            results["readings"]["groq-llama3.2-11b-vision"] = {
                "status": "FAIL",
                "raw": str(r)[:500],
            }

    nvidia_key = os.environ.get("NVIDIA_API_KEY", "")
    if nvidia_key:
        for model in [
            "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning",
            "minimaxai/minimax-m3",
        ]:
            r = post_json(
                "https://integrate.api.nvidia.com/v1/chat/completions",
                msg_openai(image_b64, model),
                {"Authorization": f"Bearer {nvidia_key}"},
            )
            if isinstance(r, dict) and "choices" in r:
                results["readings"][model] = {
                    "status": "OK",
                    "text": r["choices"][0]["message"]["content"],
                }
            else:
                results["readings"][model] = {"status": "FAIL", "raw": str(r)[:500]}

    or_key = os.environ.get("OPENROUTER_API_KEY", "")
    if or_key:
        r = post_json(
            "https://openrouter.ai/api/v1/chat/completions",
            msg_openai(image_b64, "qwen/qwen-2.5-vl-72b-instruct:free"),
            {"Authorization": f"Bearer {or_key}", "X-Title": "TienLang-Council"},
        )
        if isinstance(r, dict) and "choices" in r:
            results["readings"]["openrouter-qwen2.5-vl-72b"] = {
                "status": "OK",
                "text": r["choices"][0]["message"]["content"],
            }
        else:
            results["readings"]["openrouter-qwen2.5-vl-72b"] = {
                "status": "FAIL",
                "raw": str(r)[:500],
            }

    out = r"C:\Users\laptopppp\intel\debate_output\vision_round14.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(json.dumps({k: v.get("status") for k, v in results["readings"].items()}, indent=1))
    print("written:", out)


if __name__ == "__main__":
    sys.exit(main())
