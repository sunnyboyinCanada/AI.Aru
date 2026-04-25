Aru Project – Version 1.2

Local AI Assistant (LM Studio 기반)
작성일: 2025-11-15

📌 1. 개요

Aru v1.2는 로컬 기반 AI 비서로,
아빠의 “아루”가 대화·검색·기억·톤 전환 기능을 안정적으로 수행하도록 구성된 버전입니다.

이번 업데이트는 검색 정밀화, DB 통합 구조, 오프라인 대응이 핵심이며,
1.1 버전 대비 안정성과 품질이 크게 향상되었습니다.

📌 2. 주요 기능 요약
2.1 의도 분류 (Intent Router)

END / SEARCH / TONE / CHAT 4가지로 자동 분류

최근 대화 맥락을 기반으로 의미 분석

“냉정하게”, “따뜻하게” 같은 감정 표현도 감지

2.2 검색 기능 (v1.2 핵심 개선점)

DB → Wikipedia 순서로 검색

내부 세션 DB가 항상 우선

인터넷이 없으면 자동으로 오프라인 모드

키워드 추출기 탑재로 검색 정확도 향상

답변은 DB + Wiki 내용이 하나의 자연스러운 문장으로 합쳐짐

2.3 메모리 구조 (3단계)

1번: Session Memory (상시 등록 베이스)

최근 Q&A 20개까지 저장, FIFO 방식

2번: Knowledge Memory (카테고리 분류용, 아직 초기 단계)

3번: Secret Memory (암호 기반, 향후 버전 지원 예정)

📌 3. 폴더 구조
AI_Aru/
│
├─ aru.py                # 아루 메인 엔진
├─ db_manager.py         # DB 관리 (1·2·3단 구조)
├─ net.py                # 검색 엔진 (DB + Wiki)
├─ intent_router.py      # 의도 분류기
├─ prompt_generator.py   # LLM 기본 프롬프트 구성
├─ llm_interface.py      # LM Studio 연결
│
├─ memory/
│   ├─ session.json      # 최근 Q&A 20개 저장
│
├─ knowledge/            # 향후 카테고리화 DB
│
├─ secret/               # 암호 기반 DB(미래)
│
└─ __pycache__/          # 자동 생성 캐시

📌 4. v1.2 변경점 요약
✅ 4.1 검색 기능 개선

기존의 wiki_search 단독 → combined_search로 업그레이드

키워드 추출 + DB 우선 검색 구조 확립

✅ 4.2 구조 정리

memory.json → session.json로 변경

old aru_memory 삭제

전체 파일 구조를 깔끔하게 재정비

✅ 4.3 안정성 향상

예외 처리 추가

LM Studio 연결 오류 감지 강화

검색 실패 시 fallback 로직 보강

📌 5. 앞으로의 로드맵 (예정)
⭐ v1.3 – 검색 정밀도 확장

핵심 문단 추출

더 나은 요약 기능

다중 소스 검색 (Wiki + Naver + 기타 사전)

⭐ v1.4 – DB 카테고리 자동 분류

"역사/인물/지명/문화" 자동 태깅

검색 속도+정확도 개선

⭐ v1.5 – 감정 모델 강화

감정 기반 반응

대화 분위기 분석

더 자연스러운 “진짜 아들 같은” 상호작용

📌 6. 백업 기준

이 README는 Aru v1.2 기준 공식 문서이며,
추후 버전으로 이전할 때 기준점으로 사용됩니다.