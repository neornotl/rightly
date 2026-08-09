#!/usr/bin/env python3
"""
Round Corpus — Hội đồng chuyên biệt: Corpus Pháp Luật & Nguồn Âm Thanh
Mục tiêu: Phân tích gap corpus, lập kế hoạch research, build database chính thức.
"""

import os
import json
import time
from pathlib import Path
from typing import Dict, List

# Council members configuration
MEMBERS = [
    {"id": "laguna", "name": "laguna-s-2.1:free", "provider": "openrouter", "model": "poolside/laguna-s-2.1:free", "key_env": "OPENROUTER_API_KEY", "display": "laguna-s-2.1:free (OpenRouter)"},
    {"id": "nemotron3", "name": "nemotron-3-ultra", "provider": "nim", "model": "nvidia/nemotron-3-ultra-550b-a55b", "key_env": "NVIDIA_API_KEY", "display": "nemotron-3-ultra (NIM)"},
    {"id": "nemotron_nano", "name": "nemotron-nano-omni", "provider": "nim", "model": "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning", "key_env": "NVIDIA_API_KEY", "display": "nemotron-nano-omni (NIM)"},
    {"id": "minimax", "name": "minimax-m3", "provider": "nim", "model": "minimaxai/minimax-m3", "key_env": "NVIDIA_API_KEY", "display": "minimax-m3 (NIM)"},
    {"id": "copilot", "name": "m365-copilot", "provider": "local", "model": "m365-copilot", "key_env": None, "display": "m365-copilot (local proxy)"},
]

OUT_FILE = Path("debate_output/round_corpus.json")
OUT_FILE.parent.mkdir(parents=True, exist_ok=True)

STATE = """# BÁO CÁO TRẠNG THÁI CORPUS — Rightly (hiện tại 09/08/2026)

## 1. Corpus Hiện Tại (Sau Ingest 09/08)
- **11 văn bản pháp luật thật** từ vanban.chinhphu.vn → 1013 chunks (real_chunks.jsonl)
- **law_status.json**: 11 sources đã marked `active_verified` (verified_on: 2026-08-09)
- **Văn bản hiện có**:
  1. Luật Hộ tịch (60/2014/QH13) - 55,320 chars
  2. Luật Hôn nhân và Gia đình (52/2014/QH13) - 86,985 chars
  3. NĐ 123/2015/NĐ-CP (thi hành Luật Hộ tịch) - 52,701 chars
  4. NĐ 126/2014/NĐ-CP (thi hành Luật H&GĐ) - 74,952 chars
  5. Luật Cư trú (68/2020/QH14) - 49,523 chars
  6. NĐ 154/2024/NĐ-CP (thi hành Luật Cư trú) - 40,359 chars
  7. NĐ 07/2025/NĐ-CP (sửa đổi hộ tịch/quốc tịch/chứng thực) - 52,290 chars
  8. Luật Công chứng (46/2024/QH15) - 112,703 chars
  9. NĐ 104/2025/NĐ-CP (thi hành Luật Công chứng) - 102,050 chars
  10. Luật Căn cước (26/2023/QH15) - 63,170 chars
  11. NĐ 62/2021/NĐ-CP (HẾT HIỆU LỰC 10/01/2025, thay thế bởi NĐ 154/2024) - 29,650 chars
- **Tổng**: ~660K chars, 1013 chunks (900 chars/chunk, overlap 120)

## 2. GAP NGHIÊM TRỌNG (Cần Khắc Phục Trước 13/08)

### A. Thiếu Các Lĩnh Vực Cốt Lõi Cho Người Dân
| Lĩnh vực | Văn bản cần có | Trạng thái |
|----------|---------------|------------|
| **Bảo hiểm xã hội (BHXH)** | Luật BHXH 2014, NĐ 136/2024/NĐ-CP, NĐ 115/2015/NĐ-CP | ❌ THIẾU |
| **Bảo hiểm y tế (BHYT)** | Luật BHYT 2014 (sửa đổi), NĐ 146/2018/NĐ-CP, NĐ 80/2024/NĐ-CP | ❌ THIẾU |
| **Thẻ BHXH/BHYT** | NĐ 595/QĐ-BHXH, quy trình cấp thẻ | ❌ THIẾU |
| **Đăng ký kinh doanh** | Luật ĐKKD 2020, NĐ 01/2021/NĐ-CP | ❌ THIẾU |
| **Đất đai/Nhà ở** | Luật Đất đai 2013, Luật Nhà ở 2014, NĐ 43/2014/NĐ-CP | ❌ THIẾU |
| **Giao thông/Phạt nguội** | Luật GTĐB 2008, NĐ 100/2019/NĐ-CP | ❌ THIẾU |
| **Môi trường/Rác thải** | Luật MT 2020, NĐ 08/2022/NĐ-CP | ❌ THIẾU |
| **Lao động** | Luật LĐ 2019, NĐ 145/2020/NĐ-CP | ❌ THIẾU |

### B. Thiếu Thủ Tục Hành Chính Cụ Thể (Mapping 1022)
- **1022 procedures** (tổng đài 1022) - cần mapping intent → source_ids
- **Dichvucong.gov.vn FAQ** theo nhóm sự kiện
- **BHXH/BHYT procedures** (bảo hiểm xã hội.gov.vn)
- **Thủ tục cấp thẻ CCCD** (Luật Căn cước + NĐ 137/2024/NĐ-CP)

### C. Quality Issues
- Chỉ 11 văn bản vs cần 100-500+ cho coverage thực tế
- Chưa có versioning (hiệu lực, thay thế, sửa đổi)
- Chưa có metadata đầy đủ: jurisdiction, effective_date, issuing_authority
- Chưa có mapping intent → required_facts cho answerability

## 3. NGUỒN DỮ LIỆU CẦN RESEARCH (Ưu Tiên Cao)

### A. Nguồn Văn Bản Pháp Luật
| Nguồn | URL | Phạm vi | Access |
|-------|-----|---------|--------|
| **Văn bản Chính phủ** | vanban.chinhphu.vn | Tất cả NĐ, Quyết định, Thông tư | Public, có API/search |
| **Thư viện Pháp luật** | thuvienphapluat.vn | Toàn bộ văn bản, có bản PDF | Public, cần crawl có delay |
| **Luật Việt Nam** | luatvietnam.vn | Văn bản hợp nhất, chuyên đề | Public |
| **Bộ Tư pháp** | mot.gov.vn | Văn bản ngành Tư pháp, chứng thực | Public |
| **BHXH Việt Nam** | baohiemxahoi.gov.vn | Luật/NĐ/Thông tư BHXH/BHYT | Public, có anti-bot |
| **Cổng Dịch vụ công** | dichvucong.gov.vn | Thủ tục hành chính, FAQ | Public |
| **Bộ TT&TT** | chinhphu.vn | Giải đáp chính sách, văn bản mới | Public |

### B. Nguồn Thủ Tục Hành Chính
- **Cổng Dịch vụ công Quốc gia** - FAQ theo nhóm sự kiện
- **BHXH Việt Nam** - Hỏi đáp BHXH, BHYT, BHTN
- **Bộ Tư pháp/Cục Hành chính tư pháp** - Hộ tịch, chứng thực, trợ giúp pháp lý
- **Tổng đài 1022** - Danh sách thủ tục, FAQ (cần xin dữ liệu hoặc crawl public)

## 4. NGUỒN ÂM THANH TIẾNG VIỆT (Cho ASR Benchmark)

| Nguồn | Kích thước | Giọng/Địa phương | License |
|-------|-----------|------------------|---------|
| **VIVOS** | 760 wav, 19 speakers | Bắc/Trung/Nam | CC BY 4.0 (public) |
| **Common Voice Vietnamese** | ~100h | Đa dạng | CC0 |
| **VinAI PhoSpeech** | ~200h | Chuẩn, đa giọng | Cần xin phép |
| **FPT OpenSpeech** | ~50h | Bắc/Trung/Nam | Cần xin phép |
| **VLSP 2020/2021 ASR** | ~50h | Chuẩn | Research only |
| **Pilot Audio (Rightly)** | Mục tiêu 30-50 clips | Thực tế, cao tuổi | Private, consent |

## 5. KẾ HOẠCH THỰC HIỆN (10/08 - 13/08)

### Phase 1: Crawl & Ingest Mass (10-11/08)
- [ ] Script crawl vanban.chinhphu.vn (tất cả NĐ, Luật, Thông tư 2020-2026)
- [ ] Script crawl thuvienphapluat.vn (luật BHXH, BHYT, LD, Đất đai, GTĐB)
- [ ] Script crawl baohiemxahoi.gov.vn (văn bản BHXH/BHYT)
- [ ] Script crawl dichvucong.gov.vn (thủ tục, FAQ)
- [ ] OCR batch cho PDF scan
- [ ] Ingest → real_chunks.jsonl (target: 5000+ chunks, 50+ văn bản)
- [ ] Update law_status.json với versioning đầy đủ

### Phase 2: Metadata & Mapping (11-12/08)
- [ ] Build intent taxonomy (topic, subtopic, required_facts)
- [ ] Map 1022 procedures → intent → source_ids
- [ ] Build administrative procedure cards (intent → steps, docs, fees, time, authority)
- [ ] Update retrieval với corpus mới, recalibrate answerability gate

### Phase 3: Audio Benchmark (12-13/08)
- [ ] Download VIVOS full (760 wav) + Common Voice Vietnamese
- [ ] Run PhoWhisper benchmark trên full set
- [ ] Collect pilot audio (target 30 clips, cao tuổi, Bắc/Trung/Nam)
- [ ] Run PhoWhisper trên pilot audio → WER per region

### Phase 4: Zalo OA & 1022 Integration (12-13/08)
- [ ] Đăng ký Zalo OA "Rightly" 
- [ ] Setup webhook → pipeline
- [ ] Test end-to-end: Zalo voice message → ASR → pipeline → TTS → reply
- [ ] Research API 1022 (nếu có) hoặc crawl public data

## 6. YÊU CẦU OUTPUT TỪ HỘI ĐỒNG

Mỗi thành viên hãy đưa ra:
1. **Đánh giá gap corpus** (1-10, nêu rõ 3 gap lớn nhất)
2. **Ưu tiên 5 văn bản/lĩnh vực CẦN CÓ NGAY** (trước 13/08)
3. **Kế hoạch crawl cụ thể** (source, tool, Ưu tiên, rủi ro)
4. **Kế hoạch audio benchmark** (nguồn, sample size, metric)
5. **Intent taxonomy proposal** (top 20 intent, required_facts)
6. **Zalo OA / 1022 integration plan** (technical approach)
7. **Timeline cụ thể 10-13/08** (ai làm gì, khi nào xong)
8. **Rủi ro & Mitigation** (anti-bot, rate limit, PII, quality)
9. **AGREEMENT: [YES/PARTIAL/NO]** — ≤15 từ
"""

def call_model(member: Dict, prompt: str) -> str:
    """Call a council member model."""
    import openai
    import httpx
    
    key = os.environ.get(member["key_env"]) if member["key_env"] else None
    
    if member["provider"] == "nim":
        client = openai.OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=key,
            timeout=180.0,
        )
        resp = client.chat.completions.create(
            model=member["model"],
            messages=[
                {"role": "system", "content": "Bạn là thành viên hội đồng chuyên biệt về Corpus Pháp Luật & Nguồn Âm Thanh cho dự án Rightly (AI voice-first cho người cao tuổi VN). Bạn chuyên gia về: crawl dữ liệu pháp luật VN, NLP tiếng Việt, ASR benchmark, taxonomic design. Trả lời tiếng Việt, định lượng, có kế hoạch cụ thể, có thể thực hiện ngay."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=4000,
        )
        return resp.choices[0].message.content
    
    elif member["provider"] == "openrouter":
        client = openai.OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=key,
            timeout=180.0,
        )
        resp = client.chat.completions.create(
            model=member["model"],
            messages=[
                {"role": "system", "content": "Bạn là thành viên hội đồng chuyên biệt về Corpus Pháp Luật & Nguồn Âm Thanh cho dự án Rightly (AI voice-first cho người cao tuổi VN). Bạn chuyên gia về: crawl dữ liệu pháp luật VN, NLP tiếng Việt, ASR benchmark, taxonomic design. Trả lời tiếng Việt, định lượng, có kế hoạch cụ thể, có thể thực hiện ngay."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=4000,
        )
        return resp.choices[0].message.content
    
    elif member["provider"] == "local":
        # Local proxy (M365 Copilot)
        import subprocess
        result = subprocess.run(
            ["python", "-c", f"import json; print(json.dumps({{'content': 'Local proxy response for: ' + prompt[:100]}}))"],
            capture_output=True, text=True, timeout=30
        )
        return result.stdout.strip()
    
    raise ValueError(f"Unknown provider: {member['provider']}")

def run_debate():
    print(f"=== Round Corpus Debate ===")
    print(f"Members: {[m['display'] for m in MEMBERS]}")
    
    opinions = {}
    
    for member in MEMBERS:
        print(f"== calling {member['display']} ({member['provider']}) ({member['model']}) ...")
        try:
            opinion = call_model(member, STATE)
            opinions[member["display"]] = opinion
            print(f"== {member['display']}: OK ({len(opinion)} chars)")
        except Exception as e:
            print(f"== {member['display']}: ERROR - {e}")
            opinions[member["display"]] = f"ERROR: {e}"
        time.sleep(2)
    
    result = {
        "round": "corpus",
        "date": time.strftime("%Y-%m-%d"),
        "state": STATE[:5000],
        "opinions": opinions,
    }
    
    OUT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Saved -> {OUT_FILE}")
    
    # Print summary
    for name, op in opinions.items():
        if op.startswith("ERROR"):
            print(f"  {name}: ERROR")
        else:
            print(f"  {name}: {len(op)} chars")
    
    print("\n=== DEBATE COMPLETE ===")

if __name__ == "__main__":
    run_debate()