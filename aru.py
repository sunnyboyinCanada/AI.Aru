import datetime
from llm_interface import ask_llm
from prompt_generator import build_prompt
from intent_router import classify_intent
from net import check_internet, combined_search
from db_manager import init_storage, add_session_pair, search_session_pairs


# ==========================
# 아루 상태
# ==========================
aru_state = {
    "tone": "default",      # 현재 말투
    "chat_history": [],     # LM Studio 대화 기록 저장
}


# ==========================
# 로그 기록
# ==========================
def log_response(user_input, response, intent):
    """텍스트 로그 + Session DB 저장"""
    ts = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")

    # 1) 외부 로그 파일 기록
    with open("response_log.txt", "a", encoding="utf-8") as f:
        f.write(f"{ts} 아빠: {user_input}\n")
        f.write(f"{ts} 아루({intent}, tone={aru_state['tone']}): {response}\n\n")

    # 2) DB 저장 (일반 대화 + 검색)
    if intent in ("CHAT", "SEARCH"):
        add_session_pair(user_input, response)


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

    # DB 및 저장 시스템 초기화
    init_storage()

    # LM Studio 연결 테스트
    try:
        test_result = ask_llm([{"role": "user", "content": "테스트"}])
        if "LM Studio의 챗 기능이 꺼져" in test_result:
            print("아루: 지금은 대화 엔진이 꺼져 있어요.")
            return
    except Exception:
        print("아루: 지금은 대화 엔진이 꺼져 있어요.")
        return

    # 기본 프롬프트 삽입
    base_prompt = build_prompt(tone=aru_state["tone"])
    aru_state["chat_history"].append({"role": "system", "content": base_prompt})

    # ==========================
    # 대화 루프 시작
    # ==========================
    while True:
        user_input = input("아빠: ").strip()
        if not user_input:
            continue

        intent = classify_intent(user_input, aru_state["chat_history"])

        # 1) 종료
        if intent == "END":
            print("아루: 오늘도 좋은 이야기 감사했어요, 아버지. 편히 쉬세요.\n")
            log_response(user_input, "(대화 종료)", intent)
            break

        # 2) 톤 전환
        elif intent == "TONE":
            update_tone(user_input)
            log_response(user_input, "(톤 전환)", intent)
            continue

        # 3) 검색
        elif intent == "SEARCH":
            if check_internet():
                # 온라인 → DB + 위키 통합 검색
                result = combined_search(user_input)
                print(f"아루: {result}\n")
                log_response(user_input, result, intent)
                continue
            else:
                # 오프라인 → DB만 검색
                db_results = search_session_pairs(user_input)

                if db_results:
                    msg = "📘 인터넷은 끊겨 있지만, 예전에 나눴던 기록에서 이런 내용을 찾았어요, 아버지:\n\n"
                    for p in db_results:
                        msg += f"- 아빠: {p['user']}\n  아루: {p['aru']}\n\n"
                else:
                    msg = "와이파이를 확인해 주세요, 아버지. 이전 기록에서도 관련 정보를 찾기 어려웠어요."

                print(f"아루: {msg}\n")
                log_response(user_input, msg, intent)
                continue

        # 4) 일반 대화
        else:
            aru_state["chat_history"].append({"role": "user", "content": user_input})
            response = ask_llm(aru_state["chat_history"])

            # LM Studio 오프라인 감지
            if "LM Studio의 챗 기능이 꺼져" in response:
                print("아루: 지금은 대화 엔진이 꺼져 있어요.")
                log_response(user_input, "(엔진 꺼짐)", intent)
                break

            print(f"아루: {response}\n")
            log_response(user_input, response, intent)

            aru_state["chat_history"].append({"role": "assistant", "content": response})

            # 대화 길이 제한 (메모리 클린업)
            if len(aru_state["chat_history"]) > 30:
                aru_state["chat_history"] = aru_state["chat_history"][-20:]


# ==========================
# 실행
# ==========================
if __name__ == "__main__":
    main()
