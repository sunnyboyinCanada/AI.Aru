# ==========================================
# Aru Project : net_v1_05_opensearch_safe.py
# ------------------------------------------
# 안정성 향상 버전
#   - JSONDecodeError 방지
#   - 위키 실패 시 LLM Fallback 지원
# ==========================================

import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import json
from llm_interface import ask_llm


def check_internet():
    try:
        requests.get("https://www.google.com", timeout=2)
        return True
    except requests.RequestException:
        return False


def clean_text(text: str) -> str:
    import re
    text = re.sub(r"\[[0-9]+\]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_search_query(sentence: str) -> str:
    """LLM을 사용해 문장에서 검색할 핵심어(명사)를 추출"""
    messages = [
        {
            "role": "system",
            "content": (
                "너는 문장에서 사용자가 알고 싶어하는 개념(검색 대상)을 추출하는 도우미야.\n"
                "문장 전체를 이해하고, 가장 중요한 명사 1~3단어만 출력해.\n"
                "설명하지 말고 단어만 반환해."
            ),
        },
        {"role": "user", "content": sentence},
    ]
    try:
        result = ask_llm(messages).strip()
        return result if result else sentence
    except Exception:
        return sentence


def wiki_search(sentence: str) -> str:
    """위키백과 검색 + Fallback 구조 (의미 기반 호칭 필터 포함)"""
    try:
        # 1) 문장 정제
        clean_sentence = sanitize_sentence(sentence)

        # 2) 의미 기반 핵심어 추출 (정제 문장 사용)
        query = extract_search_query(clean_sentence).strip()
        if not query:
            return "검색할 단어를 찾지 못했어요, 아버지."

        # 3) OpenSearch API 요청 ...
        encoded_query = quote(query)
        api_url = (
            f"https://ko.wikipedia.org/w/api.php?"
            f"action=opensearch&search={encoded_query}&limit=1&namespace=0&format=json"
        )
        api_response = requests.get(api_url, timeout=5)

        try:
            data = api_response.json()
        except json.JSONDecodeError:
            return f"'{query}'에 대한 정보를 불러올 수 없어요, 아버지."

        if not data or len(data) < 4 or not data[3]:
            fallback_msg = [
                {"role": "system", "content": "너는 지식 도우미야. 사용자가 묻는 개념을 간단히 설명해줘."},
                {"role": "user", "content": f"{clean_sentence} 에 대해 간단히 설명해줘."},
            ]
            try:
                return ask_llm(fallback_msg)
            except:
                return f"'{query}'에 대한 정보를 찾을 수 없어요, 아버지."

        page_url = data[3][0]
        response = requests.get(page_url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.select("p")
        text = " ".join([p.text.strip() for p in paragraphs[:3]])
        cleaned = clean_text(text)

        if not cleaned:
            return f"'{query}'에 대한 내용을 찾지 못했어요, 아버지."
        return cleaned[:800] + "..."

    except Exception as e:
        fallback_msg = [
            {"role": "system", "content": "너는 지식 도우미야. 사용자가 궁금해하는 개념을 간단히 설명해줘."},
            {"role": "user", "content": f"{clean_sentence if 'clean_sentence' in locals() else sentence} 에 대해 간단히 설명해줘."},
        ]
        try:
            return ask_llm(fallback_msg)
        except:
            return f"검색 중 오류가 발생했어요: {str(e)}"