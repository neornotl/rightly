"""Naturalness tests (Round 11 council): tone, templates, spoken citation.

Council consensus: answers must stay grounded/safe but sound like a real
hotline agent — short sentences, polite fillers, spoken citation <=15 words.
"""

from __future__ import annotations

from app.llm.prompts import SYSTEM_PROMPT, TEMPLATES, shorten_spoken_citation


class TestSystemPromptTone:
    def test_has_polite_pronouns(self):
        assert "anh/chị" in SYSTEM_PROMPT
        assert "ạ" in SYSTEM_PROMPT and "dạ" in SYSTEM_PROMPT

    def test_forbids_repeating_document_title(self):
        assert "KHÔNG lặp lại nguyên văn tiêu đề văn bản" in SYSTEM_PROMPT

    def test_short_sentence_rule(self):
        assert "18 từ" in SYSTEM_PROMPT
        assert "Một ý một câu" in SYSTEM_PROMPT

    def test_grounding_still_enforced(self):
        assert "CHÍNH XÁC" in SYSTEM_PROMPT
        assert "source_id" in SYSTEM_PROMPT
        assert "không bịa thông tin" in SYSTEM_PROMPT

    def test_safety_rules_present(self):
        assert "113" in SYSTEM_PROMPT and "115" in SYSTEM_PROMPT
        assert "hết hiệu lực" in SYSTEM_PROMPT
        assert "Ngoài phạm vi" in SYSTEM_PROMPT

    def test_default_length_rule(self):
        assert "NGẮN" in SYSTEM_PROMPT
        assert "80 từ" in SYSTEM_PROMPT


class TestTemplates:
    def test_all_six_situations_covered(self):
        assert set(TEMPLATES) == {
            "answer_full",
            "insufficient",
            "off_scope",
            "criminal",
            "expired",
            "clarify",
        }

    def test_insufficient_offers_guidance_not_bare_rejection(self):
        text = TEMPLATES["insufficient"]
        assert "chưa có dữ liệu" in text
        assert "1022" in text
        assert "được hướng dẫn" in text

    def test_criminal_routes_to_emergency(self):
        text = TEMPLATES["criminal"]
        assert "113" in text and "115" in text

    def test_clarify_asks_for_limited_info(self):
        assert "{needed}" in TEMPLATES["clarify"]

    def test_expired_points_to_replacement(self):
        assert "{replacement}" in TEMPLATES["expired"]


class TestSpokenCitation:
    def test_empty_input(self):
        assert shorten_spoken_citation("") == ""

    def test_strips_leading_opener(self):
        out = shorten_spoken_citation("Căn cứ Điều 14 Luật Hôn nhân và Gia đình 2014")
        assert out.startswith("Điều 14")
        assert "Căn cứ" not in out

    def test_drops_article_clause_details(self):
        out = shorten_spoken_citation("Luật Hôn nhân và Gia đình 2014, Điều 14, Khoản 1, Điểm a")
        assert out == "Luật Hôn nhân và Gia đình 2014, Điều 14"
        assert "Khoản" not in out and "Điểm" not in out

    def test_trims_after_sentence_boundary(self):
        out = shorten_spoken_citation(
            "Theo quy định của Nghị định 134/2015/NĐ-CP. Người lao động được..."
        )
        assert "Người lao động" not in out

    def test_caps_word_count(self):
        long = "Luật Hôn nhân và Gia đình năm 2014 " + " ".join(f"từ{a}" for a in range(25))
        out = shorten_spoken_citation(long)
        assert len(out.split()) <= 16

    def test_short_citation_untouched(self):
        out = shorten_spoken_citation("Điều 4, Nghị định 134/2015")
        assert out == "Điều 4, Nghị định 134/2015"
