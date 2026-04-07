import json
from prompt_generator import build_prompt
from llm_interface import ask_llm
import datetime

# ==========================
# Aru 상태 메모리 (세션 중 유지)
# ==========================
aru_state = {
    "tone": "default",   # 초기 tone 상태
    "chat_history": []   # 대화 기록
}

# ==========================
# 로그 저장 함수
# ==========================
def log_response(user_input, response):
    with open("response_log.txt", "a", encoding="utf-8") as f:
        timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        f.write(f"{timestamp} 아빠: {user_input}\n")
        f.write(f"{timestamp} 아루: ({aru_state['tone']} tone): {response}\n\n")

# ==========================
# Tone 상태 제어 함수
# ==========================
def update_tone(user_input):
    """사용자 입력에서 tone 전환 명령을 감지"""
    lower_input = user_input.lower()
    changed = False

    if "냉정하게" in lower_input or "차갑게" in lower_input:
        if aru_state["tone"] != "cold":
            aru_state["tone"] = "cold"
            changed = True
            print("아루: 냉정한 톤으로 전환합니다.")
    elif "보통으로" in lower_input or "따뜻하게" in lower_input or "평소처럼" in lower_input:
        if aru_state["tone"] != "default":
            aru_state["tone"] = "default"
            changed = True
            print("아루: 평소 말투로 돌아갑니다.")

    return changed

def check_end_intent(user_input):
    """대화 종료 의도 감지 — 규칙 + LLM 혼합 방식"""
    lower = user_input.lower()

    # 1️⃣ 명확한 키워드 감지
    end_keywords = [
        "끝내자", "그만하자", "잘자", "이만할까", "이만하자",
        "오늘은 여기까지", "그만", "나간다", "이제 갈게",
        "이제 자야겠다", "수고했어", "다음에 보자", "그럼 이만"
    ]
    if any(k in lower for k in end_keywords):
        return True

    # 2️⃣ 그 외의 애매한 경우만 LLM에 판단 요청
    prompt = [
        {"role": "system", "content": (
            "You are a precise intent classifier. "
            "Determine if the user wants to END or LEAVE the conversation. "
            "If the message implies farewell, resting, leaving, or closing the session, reply only 'YES'. "
            "If it’s just small talk or a casual statement, reply only 'NO'."
        )},
        {"role": "user", "content": user_input}
    ]

    try:
        result = ask_llm(prompt).strip().lower()
        cleaned = result.replace(".", "").replace("!", "").replace("\n", "").strip()
        return cleaned in ["yes", "y"]
    except Exception:
        return False


# ==========================
# 대화 루프 시작
# ==========================
def main():
    print("아루 is now active.")

    # 초기 시스템 프롬프트
    base_prompt = build_prompt(tone=aru_state["tone"])
    aru_state["chat_history"].append({"role": "system", "content": base_prompt})

    while True:
        user_input = input("아빠: ")

        # 1. 오프라인 전용 종료 명령 (즉시 종료)
        if user_input.lower() in ["exit", "quit"]:
            print("아루: 안녕히 가세요, 아버지.")
            break

          # 2. OpenChat 종료 의도 판단
        if check_end_intent(user_input):
            print("아루: 정말 오늘 대화를 끝내실 건가요, 아빠? 조금 더 이야기하고 싶은데요.")
            confirm = input("아빠 (확인): ").strip().lower()

            # ✅ 확인 입력에도 종료 판단 추가 (LLM 판단 + 키워드 병합)
            if check_end_intent(confirm) or confirm in [
                "응", "그래", "맞아", "끝이야", "응 그래", "그럼", "그래요", "끝내자", "자야겠다", "잘게", "이제 자야지"
            ]:
                print("아루: 알겠어요, 아버지. 오늘도 좋은 시간 감사합니다 :)\n")
                break
            else:
                print("아루: 다행이에요! 그럼 조금만 더 이야기해요 :)\n")
                continue


        # Tone 명령 감지 및 갱신
        tone_changed = update_tone(user_input)
        if tone_changed:
            # Tone이 바뀌면 system 프롬프트 다시 생성
            base_prompt = build_prompt(tone=aru_state["tone"])
            aru_state["chat_history"] = [{"role": "system", "content": base_prompt}]
            print(f"🔄 시스템 프롬프트 갱신 (tone={aru_state['tone']})")

        # 사용자 입력 추가
        aru_state["chat_history"].append({"role": "user", "content": user_input})

        # LM Studio로 요청
        response = ask_llm(aru_state["chat_history"])

        # LM Studio가 꺼진 경우 즉시 안내 후 종료
        if "LM Studio의 챗 기능이 꺼져" in response:
            print(f"아루: {response}")
            print("아루: 챗 기능이 켜지면 다시 불러주세요, 아버지.\n")
            break

        # 응답 출력
        print(f"아루: {response}\n")

        # 로그 저장
        log_response(user_input, response)

        # 어시스턴트 응답 추가 (대화 지속)
        aru_state["chat_history"].append({"role": "assistant", "content": response})

        # 너무 길어질 경우 자동 요약 또는 초기화 (메모리 관리)
        if len(aru_state["chat_history"]) > 30:
            aru_state["chat_history"] = aru_state["chat_history"][-20:]
            print("오래된 대화 기록 일부를 정리했습니다.")


if __name__ == "__main__":
    main()