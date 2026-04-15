import requests
import json

def ask_llm(messages):
    try:
        response = requests.post(
            "http://localhost:1234/v1/chat/completions",   # LM Studio 기본 포트
            headers={"Content-Type": "application/json"},
            data=json.dumps({
                "model": "gpt-3.5-turbo",  # 네가 LM Studio에서 쓰는 모델 이름 확인 후 맞춰줘
                "messages": messages
            }),
            timeout=30  # 타임아웃을 넉넉히 (기본 5초면 너무 짧음)
        )
        response.raise_for_status()
        data = response.json()
        # LM Studio 응답 구조: {"choices":[{"message":{"content":"..."}}]}
        return data["choices"][0]["message"]["content"]

    except requests.exceptions.Timeout:
        return "LM Studio 응답이 늦어서 연결이 끊어진 것 같아요."
    except requests.exceptions.ConnectionError:
        return "LM Studio와 연결되지 않았어요. 서버를 확인해 주세요."
    except Exception as e:
        return f"LM Studio 오류: {str(e)}"
