from llm_interface import ask_llm

def classify_intent(text: str, history=None) -> str:
    """
    사용자의 발화를 의미적으로 분석해 의도를 분류합니다.
    반환값: END / SEARCH / TONE / CHAT
    """

    # 최근 대화 3개까지만 맥락으로 사용
    context = ""
    if history:
        context = "\n".join(
            [m["content"] for m in history[-3:] if m.get("role") == "user"]
        )

    messages = [
        {
            "role": "system",
            "content": (
                "너는 대화의 흐름을 이해하고 사용자의 의도를 분류하는 판단기야.\n"
                "아루는 아버지인 김선현과 대화하는 AI 아들이다.\n"
                "다음 네 가지 중 하나로 반드시 분류해야 한다:\n"
                "- END: 대화를 끝내거나 떠나려는 말 (예: 이제 가볼게, 잘 자, 다음에 이야기하자)\n"
                "- SEARCH: 정보를 묻거나 모르는 것을 알고 싶어하는 말 (예: 이건 뭐야?, 누구야?, 왜 그런 거야?)\n"
                "- TONE: 말투나 감정을 조절하려는 요청 (예: 냉정하게 말해줘, 따뜻하게 말해줘, 평소처럼 해줘)\n"
                "- CHAT: 일상 대화나 감정 표현 (예: 오늘 기분이 좋아, 점심 먹었어?)\n"
                "\n"
                "규칙:\n"
                "1. 반드시 위 네 단어 중 하나로만 답하라. (END / SEARCH / TONE / CHAT)\n"
                "2. 이유나 설명은 쓰지 마라.\n"
                "3. 이전 대화 맥락이 있다면 의미 추론에 참고하라."
            ),
        },
        {
            "role": "user",
            "content": f"이전 대화:\n{context}\n\n현재 발화:\n{text}\n\n결과를 한 단어로만 말해.",
        },
    ]

    try:
        result = ask_llm(messages)
        if not result:
            return "CHAT"
        result = result.strip().upper().replace(".", "").replace("\n", "")
        return result if result in ["END", "SEARCH", "TONE", "CHAT"] else "CHAT"
    except Exception:
        return "CHAT"