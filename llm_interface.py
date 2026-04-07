import requests

API_URL = "http://localhost:1234/v1/chat/completions"
MODEL = "openchat-3.6-8b-20240522"

def ask_llm(messages):
    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.7,
    }

    try:
        r = requests.post(API_URL, json=payload, timeout=5)
        r.raise_for_status()
        data = r.json()
        if "choices" in data and len(data["choices"]) > 0:
            response = data["choices"][0]["message"]["content"].strip()
            return response + "\n"
    except Exception:
        # 🔻 LM Studio가 꺼져 있을 때
        return "LM Studio의 챗 기능이 꺼져 있어요, 아버지. LM Studio를 실행해 주세요."