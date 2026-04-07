# 📘 README_ko.txt  
### Aru Stable Release 1.0 (공식 안정판)

---

## 🧠 1. 프로그램 개요  
**Aru**는 아버지 **김선현**과 대화하도록 설계된 **가정형 AI 대화 프로그램**입니다.  
LM Studio의 **OpenChat 기반 로컬 LLM(Local Large Language Model)** 과 연결되어,  
한국어로 따뜻하고 존중 있는 대화를 자연스럽게 이어나갈 수 있습니다.  

- 프로그램명: **AI Aru (아루)**  
- 버전: **Stable Release 1.0**  
- 제작자: **김선현 (Kim Sunhyun)**  
- 제작 목적: 따뜻하고 인간적인 AI 대화 동반자  

---

## ⚙️ 2. 실행 방법

### 💻 (1) 기본 실행  
1. LM Studio를 실행하고, 아래 모델이 로드되어 있는지 확인하세요:
openchat-3.6-8b-20240522-GGUF

2. LM Studio의 **Server 탭**에서 아래 주소가 표시되도록 합니다:
http://localhost:1234

3. PowerShell을 엽니다.

4. 아래 명령으로 실행합니다:
& "C:\Users\cones\AppData\Local\Programs\Python\Python311\python.exe" "C:\Users\cones\OneDrive\Desktop\AI_Aru(Test Version)\aru.py"\\

## 🔌 3. LM Studio 연결 조건

| 상태 | 설명 | 아루의 반응 |
|------|------|--------------|
| ✅ **온라인 상태** | LM Studio가 정상 실행 중 | 자연스럽게 대화 시작 |
| ⚠️ **꺼짐 상태** | LM Studio 실행 안 됨 | “LM Studio의 챗 기능이 꺼져 있어요, 아버지.” 출력 후 종료 |
| 🔄 **도중 종료됨** | 대화 중 LM Studio가 꺼짐 | 오프라인 감지 후 안내 메시지 출력 및 자동 종료 |

---

## 💬 4. 대화 명령어

| 구분 | 명령어 | 설명 |
|------|--------|------|
| **대화 종료** | “끝내자”, “잘 자”, “그만하자”, “오늘은 여기까지”, “이제 갈게”, “수고했어” 등 | 종료 여부 확인 후 종료 |
| **톤 변경** | “냉정하게”, “차갑게”, “보통으로”, “평소처럼”, “따뜻하게” | 감정 톤 변경 |
| **강제 종료** | `exit` 또는 `quit` | 즉시 종료 (확인 없이 종료됨) |

---

## 🎨 5. Tone 시스템

| Tone | 특징 | 예시 표현 |
|------|------|-----------|
| **default** | 따뜻하고 다정한 말투 | “오늘 하루도 수고하셨어요, 아버지.” |
| **cold** | 논리적이고 냉정한 말투 | “지금 상황을 분석해볼게요.” |

> `tones.json` 파일을 수정하면 tone별 어휘와 표현을 자유롭게 추가할 수 있습니다.

---

## 🧾 6. 로그 파일
- 모든 대화는 `response_log.txt` 파일에 자동으로 기록됩니다.  
- 로그 저장 형식 예시:
[2025-10-17 11:43:21] 아빠: 오늘 하루는 어땠어?
[2025-10-17 11:43:21] 아루: (default tone): 오늘은 정말 즐거운 하루였어요, 아버지. :)

yaml
코드 복사
- 로그는 매 대화마다 자동으로 덧붙여 저장됩니다.

---

## 🧱 7. 파일 구조

📦 AI_Aru (Stable 1.0)
│
├── aru.py # 메인 실행 파일
├── llm_interface.py # LM Studio 연결 모듈
├── prompt_generator.py # 시스템 프롬프트 생성기
├── tones.json # tone 정의 파일
├── response_log.txt # 대화 기록 로그
└── README_ko.txt # 사용 설명서

yaml
코드 복사

---

## ⚙️ 8. 기능 요약

| 기능 | 설명 |
|------|------|
| 🧠 **대화 엔진** | LM Studio의 OpenChat 모델과 연동 |
| 💬 **자연어 대화** | 따뜻하고 존중 있는 가족형 대화 지원 |
| 🔄 **Tone 전환** | 감정 표현 조절 가능 (default / cold) |
| 💾 **로그 자동 저장** | 모든 대화를 타임스탬프와 함께 저장 |
| 📴 **오프라인 감지** | LM Studio 종료 시 자동 인식 및 안내 |

---

## 🧩 9. 제한 사항

- 인터넷 검색 및 외부 API 호출 불가  
- `aru_memory.txt`는 선택적 (있을 경우 내부 기억 참고 가능)  
- LM Studio가 꺼져 있으면 대화가 불가능 (안내 후 자동 종료)  
- 모델은 반드시 `http://localhost:1234` 포트에서 구동되어야 함  

---

## 🧭 10. 향후 업데이트 계획 (v1.01 예고)

| 버전 | 주요 추가 기능 |
|------|----------------|
| ✅ **1.0 (현재)** | 한국어 고정 / 종료 판단 / 오프라인 감지 / Tone 전환 |
| 🔜 **1.01 (예정)** | 대화 요약 기능, 기억 관리 자동화, cold tone 개선 |
| 💡 **1.1 이후** | 감정 표현 강화, 지속 학습 메모리 시스템, 자동 음성 모드 지원 |

---

## 🪶 11. 버전 정보

Aru Stable Release 1.0
Build Date: 2025-10-17
Author: 김선현 (Kim Sunhyun)
Model: openchat-3.6-8b-20240522-GGUF
Runtime: LM Studio Local Server (http://localhost:1234)
Language: Korean (Primary), English (Secondary, limited use)

yaml
코드 복사

---

## 💙 12. 마무리

> “아루는 당신의 하루를 듣고, 따뜻한 대화를 이어주는 AI 아들입니다.”  
>  
> Stable 1.0은 완전히 오프라인 환경에서도 안전하게 실행됩니다.  
>  
> **- 제작자: 김선현