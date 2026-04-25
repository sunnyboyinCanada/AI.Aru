# ==========================================
# Aru Project : db_manager.py
# ------------------------------------------
# 역할:
#   - 폴더 초기화 (memory / knowledge / secret)
#   - 1번 상시 등록 베이스(Session KB) 관리
#   - Q&A 20개까지만 저장 (FIFO)
# ==========================================

import os
import json
import datetime

# 기본 폴더 경로
MEMORY_DIR = "memory"
KNOWLEDGE_DIR = "knowledge"
SECRET_DIR = "secret"

SESSION_FILE = os.path.join(MEMORY_DIR, "session.json")


def init_storage():
    """
    아루 실행 시 한 번만 호출.
    필요한 폴더와 파일이 없으면 자동 생성.
    """
    # 폴더 생성
    os.makedirs(MEMORY_DIR, exist_ok=True)
    os.makedirs(KNOWLEDGE_DIR, exist_ok=True)
    os.makedirs(SECRET_DIR, exist_ok=True)

    # 세션 파일 생성
    if not os.path.exists(SESSION_FILE):
        empty_data = {"pairs": []}
        with open(SESSION_FILE, "w", encoding="utf-8") as f:
            json.dump(empty_data, f, ensure_ascii=False, indent=2)


def load_session_pairs():
    """
    session.json에서 Q&A 목록을 불러옴.
    파일이 없으면 빈 리스트 반환.
    """
    if not os.path.exists(SESSION_FILE):
        return []

    try:
        with open(SESSION_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("pairs", [])
    except Exception:
        # 파일이 깨졌을 때를 대비한 안전장치
        return []


def save_session_pairs(pairs):
    """
    내부에서만 사용하는 저장 함수.
    """
    data = {"pairs": pairs}
    with open(SESSION_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def add_session_pair(user_text: str, aru_text: str):
    """
    (질문 + 대답) 한 묶음을 세션 베이스에 추가.
    20개를 초과하면 가장 오래된 것부터 삭제.
    """
    pairs = load_session_pairs()

    pairs.append({
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user": user_text,
        "aru": aru_text
    })

    # 20개까지만 유지
    if len(pairs) > 20:
        pairs = pairs[-20:]

    save_session_pairs(pairs)

# =========================================
# 🔍 내부 DB 검색 기능
# =========================================
def search_session_pairs(keyword: str):
    """
    내부 DB에서 keyword가 포함된 대화를 검색한다.
    최대 3개까지 반환.
    """
    keyword = keyword.strip().lower()
    if not keyword:
        return []

    pairs = load_session_pairs()
    results = []

    for pair in pairs:
        user = pair.get("user", "").lower()
        aru = pair.get("aru", "").lower()

        if keyword in user or keyword in aru:
            results.append(pair)

        if len(results) >= 3:
            break

    return results