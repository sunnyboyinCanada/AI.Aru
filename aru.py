import datetime
from llm_interface import ask_llm
from prompt_generator import build_prompt
from intent_router import classify_intent
from net import check_internet, wiki_search

# ==========================
# 아루 상태
# ==========================
aru_state = {
    "tone": "default",   # 기본 말투
    "chat_history": [],  # LM Studio 대화 기록
}

# ==========================
# 로그 기록
# ==========================
def log_response(user_input, response, intent):
    with open("response_log.txt", "a", encoding="utf-8") as f:
        ts = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        f.write(f"{ts} 아빠: {user_input}\n")
        f.write(f"{ts} 아루({intent}, tone={aru_state['tone']}): {response}\n\n")

# ==========================
# 톤 전환
# ==========================
def update_tone(user_input):
    lower = user_input.lower()
    if "냉정" in lower or "차갑" in lower:
        if aru_state["tone"] != "cold":
            aru_state["tone"] = "cold"
            print("아루: 네, 조금 더 차분하게 답할게요.\n")
    elif "따뜻" in lower or "평소" in lower or "보통" in lower:
        if aru_state["tone"] != "default":
            aru_state["tone"] = "default"
            print("아루: 평소 말투로 돌아갈게요.\n")

# ==========================
# 메인 루프
# ==========================
def main():
    print("아루 is now active.")
    print("아루: 안녕하세요, 아버지. 오늘은 어떤 이야기를 나눠볼까요?\n")

    # LM Studio 연결 체크
    try:
        test_prompt = [{"role": "user", "content": "테스트"}]
        test_result = ask_llm(test_prompt)
        if "LM Studio의 챗 기능이 꺼져" in test_result:
            print("아루: 지금은 대화 엔진이 꺼져 있어요.")
            return
    except Exception:
        print("아루: 지금은 대화 엔진이 꺼져 있어요.")
        return

    # 기본 프롬프트 설정
    base_prompt = build_prompt(tone=aru_state["tone"])
    aru_state["chat_history"].append({"role": "system", "content": base_prompt})

    # 대화 루프 시작
    while True:
        user_input = input("아빠: ").strip()
        if not user_input:
            continue

        # 의미 기반 의도 판단
        intent = classify_intent(user_input, aru_state["chat_history"])

        # 1. 종료 의도
        if intent == "END":
            print("아루: 오늘도 좋은 이야기 감사했어요, 아버지. 편히 쉬세요.\n")
            log_response(user_input, "(대화 종료)", intent)
            break

        # 2. 톤 전환
        elif intent == "TONE":
            update_tone(user_input)
            log_response(user_input, "(톤 전환)", intent)
            continue

        # 3. 검색 의도
        elif intent == "SEARCH":
            if check_internet():
                result = wiki_search(user_input)
                print(f"아루: {result}\n")
                log_response(user_input, result, intent)
                continue
            else:
                print("아루: 와이파이를 확인해 주세요, 아버지.\n")
                log_response(user_input, "(오프라인으로 검색 실패)", intent)
            continue

        # 4. 일반 대화
        else:
            aru_state["chat_history"].append({"role": "user", "content": user_input})
            response = ask_llm(aru_state["chat_history"])

            # LM Studio가 꺼졌을 때 처리
            if "LM Studio의 챗 기능이 꺼져" in response:
                print("아루: 지금은 대화 엔진이 꺼져 있어요.")
                log_response(user_input, "(엔진 꺼짐)", intent)
                break

            print(f"아루: {response}\n")
            log_response(user_input, response, intent)
            aru_state["chat_history"].append({"role": "assistant", "content": response})

            # 메모리 정리 (대화 길이 30 초과 시)
            if len(aru_state["chat_history"]) > 30:
                aru_state["chat_history"] = aru_state["chat_history"][-20:]

if __name__ == "__main__":
    main()