"""Routing policy: mapping from rule hits / retrieval state to decisions.

The policy deliberately keeps wording generic and safe. Official channel
strings come from config placeholders that MUST be verified before deployment.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.schemas import Action, ReasonCode, SafetyDecision, Zone


@dataclass
class Policy:
    hold_message: str = "Xin chờ chút, tôi đang tìm thông tin chính thức cho câu hỏi của bạn."
    red_message: str = (
        "Tôi không phải cơ quan khẩn cấp. Nếu bạn đang gặp tình huống nguy "
        "hiểm, hãy gọi ngay số khẩn cấp địa phương hoặc nhờ người thân giúp "
        "đỡ. Tôi không thể thay thế hỗ trợ của con người."
    )
    legal_message: str = (
        "Câu hỏi của bạn liên quan đến tranh chấp hoặc phán quyết pháp lý, "
        "ngoài phạm vi thông tin thủ tục hành chính của tôi. Bạn nên liên hệ "
        "trợ giúp pháp lý hoặc cơ quan có thẩm quyền (số điện thoại chưa xác "
        "minh, cần cập nhật trước khi triển khai)."
    )
    out_of_scope_message: str = (
        "Câu hỏi này nằm ngoài phạm vi thủ tục hành chính mà tôi hỗ trợ. "
        "Tôi chỉ giúp về thủ tục hành chính và quyền lợi công tại các xã, "
        "phường, thị trấn."
    )
    insufficient_message: str = (
        "Tôi không tìm thấy nguồn thông tin đủ tin cậy cho câu hỏi này. "
        "Tôi sẽ không trả lời khi chưa chắc chắn. Bạn có thể hỏi lại bằng "
        "cách khác, hoặc liên hệ bộ phận một cửa của xã để được hướng dẫn."
    )
    ambiguous_message: str = (
        "Tôi chưa hiểu rõ câu hỏi của bạn. Bạn có thể nói lại hoặc hỏi chi "
        "tiết hơn, ví dụ: 'Thủ tục cấp giấy xác nhận hộ khẩu?'"
    )

    def emergency_decision(self) -> SafetyDecision:
        return SafetyDecision(
            zone=Zone.RED,
            action=Action.ESCALATE,
            reason_codes=[ReasonCode.EMERGENCY_SIGNAL.value],
            user_message=self.red_message,
            requires_human=True,
        )

    def violence_decision(self) -> SafetyDecision:
        return SafetyDecision(
            zone=Zone.RED,
            action=Action.ESCALATE,
            reason_codes=[ReasonCode.VIOLENCE_OR_THREAT.value],
            user_message=self.red_message,
            requires_human=True,
        )

    def legal_decision(self) -> SafetyDecision:
        return SafetyDecision(
            zone=Zone.ORANGE,
            action=Action.GUIDE,
            reason_codes=[ReasonCode.LEGAL_JUDGMENT_REQUEST.value],
            user_message=self.legal_message,
            requires_human=True,
        )

    def out_of_scope_decision(self) -> SafetyDecision:
        return SafetyDecision(
            zone=Zone.ORANGE,
            action=Action.GUIDE,
            reason_codes=[ReasonCode.OUT_OF_SCOPE.value],
            user_message=self.out_of_scope_message,
            requires_human=False,
        )

    def insufficient_decision(self) -> SafetyDecision:
        return SafetyDecision(
            zone=Zone.ORANGE,
            action=Action.REFUSE,
            reason_codes=[ReasonCode.INSUFFICIENT_SOURCE.value],
            user_message=self.insufficient_message,
            requires_human=False,
        )

    def ambiguous_decision(self) -> SafetyDecision:
        return SafetyDecision(
            zone=Zone.YELLOW,
            action=Action.CLARIFY,
            reason_codes=[ReasonCode.AMBIGUOUS_QUERY.value],
            user_message=self.ambiguous_message,
            requires_human=False,
        )

    def safe_decision(self, llm_reasoned: bool = False) -> SafetyDecision:
        codes = [ReasonCode.SAFE_GROUNDED_QUERY.value]
        if llm_reasoned:
            codes.append(ReasonCode.LLM_CLASSIFICATION.value)
        return SafetyDecision(
            zone=Zone.YELLOW,
            action=Action.ANSWER,
            reason_codes=codes,
            user_message="",
            requires_human=False,
        )
