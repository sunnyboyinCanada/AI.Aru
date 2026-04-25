# ==========================================
# Aru Project : net_v1_06_opensearch_combo.py
# ------------------------------------------
# - 위키 + LLM Fallback 통합
# - 세션 DB + 위키 통합 검색(combined_search)
# ==========================================

import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import json

from llm_interface import ask_llm
from db_manager import search_session_pairs

# 호칭 목록 (필터 대상)
VOCATIVE_EXCLUDE = ["아들"]


def sanitize_sentence(text: str) -> str:
    """
    문장에서 불필요한 호칭(예: '아들')을 제거하고 공백을 정리합니다.
    '아들이란 단어의 뜻이 뭐야?'처럼 단어 자체를 묻는 문장은 제외됩니다.
    """
    import re

    # "뜻, 의미, 단어, 정의"가 들어가면 단어 자체 설명일 가능성이 높으니 그대로 둔다.
    if any(x in text for x in ["뜻", "의미", "단어", "정의"]):
        return text

    # 단순 호칭 제거
    text = re.sub(r"\b아들\b", "", text)
    text = re.sub(r"\s{2,}", " ", text)
    return text.strip()


def check_internet() -> bool:
    try:
        requests.get("https://www.google.com", timeout=2)
        return True
    except requests.RequestException:
        return False


def clean_text(text: str) -> str:
    import re
    text = re.sub(r"\[[0-9]+\]", "", text)   # [1], [2] 같은 각주 제거
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_search_query(sentence: str) -> str:
    """
    LLM을 사용해 문장에서 검색할 핵심어(명사)를 추출.
    - 1~3개 키워드를 제안하게 하지만,
    - 실제 위키 검색에는 첫 번째 키워드만 사용.
    """
    messages = [
        {
            "role": "system",
            "content": (
                "너는 사용자의 문장에서 '검색 키워드'를 뽑아주는 도우미야.\n"
                "- 사용자가 알고 싶어하는 핵심 개념 1~3개를 명사 위주로 골라.\n"
                "- 서로 다른 개념이면 쉼표(,)로 구분해서 적어.\n"
                "- 다른 설명은 하지 말고 키워드만 출력해."
            ),
        },
        {"role": "user", "content": sentence},
    ]
    try:
        result = ask_llm(messages).strip()
        if not result:
            return sentence

        # "청와대, 한국 대통령 관저" 처럼 왔다면 첫 번째만 사용
        first = result.split(",")[0].strip()
        return first or sentence
    except Exception:
        return sentence


def wiki_search(sentence: str) -> str:
    """
    위키백과 검색 + LLM Fallback.
    - 가능하면 ko.wikipedia에서 1개 문서를 찾아 2~3단락 요약.
    - 실패하거나 내용이 비어 있으면 LLM이 대신 간단히 설명.
    """
    try:
        # 1) 문장 정제 + 키워드 추출
        clean_sentence = sanitize_sentence(sentence)
        query = extract_search_query(clean_sentence).strip()

        if not query:
            return "검색할 단어를 찾지 못했어요, 아버지."

        encoded_query = quote(query)
        api_url = (
            "https://ko.wikipedia.org/w/api.php?"
            f"action=opensearch&search={encoded_query}&limit=1&namespace=0&format=json"
        )
        api_response = requests.get(api_url, timeout=5)
        data = api_response.json()

        # 결과가 없으면 → 바로 LLM 설명
        if not data or len(data) < 4 or not data[3]:
            fallback_msg = [
                {
                    "role": "system",
                    "content": "너는 지식 도우미야. 사용자가 묻는 개념을 간단히 설명해줘.",
                },
                {
                    "role": "user",
                    "content": f"'{clean_sentence}' 에 대해 간단히 설명해줘.",
                },
            ]
            return ask_llm(fallback_msg)

        page_url = data[3][0]
        response = requests.get(page_url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.select("p")
        text = " ".join([p.text.strip() for p in paragraphs[:3]])
        cleaned = clean_text(text)

        # 위키 본문이 거의 비어 있을 때도 LLM으로 대체
        if not cleaned:
            fallback_msg = [
                {
                    "role": "system",
                    "content": "너는 지식 도우미야. 사용자가 묻는 개념을 간단히 설명해줘.",
                },
                {
                    "role": "user",
                    "content": f"'{clean_sentence}' 에 대해 간단히 설명해줘.",
                },
            ]
            return ask_llm(fallback_msg)

        return cleaned[:800] + "..."

    except Exception:
        # 네트워크/JSON 에러 등 → LLM Fallback
        try:
            fallback_msg = [
                {
                    "role": "system",
                    "content": "너는 지식 도우미야. 사용자가 묻는 개념을 간단히 설명해줘.",
                },
                {
                    "role": "user",
                    "content": f"'{sentence}' 에 대해 간단히 설명해줘.",
                },
            ]
            return ask_llm(fallback_msg)
        except:
            return "검색 도중 연결이 불안정했어요, 아버지. 잠시 후 다시 시도해볼게요."


def combined_search(user_input: str) -> str:
    """
    내부 세션 DB + 위키/LLM 정보를 한 번에 묶어서 반환.
    - DB에 과거 대화가 있으면 먼저 보여주고,
    - 항상 위키/LLM 결과를 함께 붙여준다.
    """
    # 1) 세션 DB 검색
    db_results = search_session_pairs(user_input)

    # 2) 위키 / LLM 검색
    wiki_result = wiki_search(user_input)

    parts = []

    if db_results:
        msg = "📘 예전에 나눴던 기록 중에서 이런 내용이 있었어요, 아버지:\n\n"
        for p in db_results:
            msg += f"- 아빠: {p['user']}\n  아루: {p['aru']}\n\n"
        parts.append(msg.strip())

    if wiki_result:
        parts.append("🌐 위키/외부 정보 요약:\n" + wiki_result)

    if not parts:
        return "이전 기록과 위키에서 모두 정보를 찾기 어려웠어요, 아버지."
    return "\n\n".join(parts)