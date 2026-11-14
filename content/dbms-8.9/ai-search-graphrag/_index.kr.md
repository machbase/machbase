---
type: docs
title: '11. AI 벡터 검색과 GraphRAG'
weight: 110
toc: true
---

Machbase DBMS 8.9의 벡터·키워드·Hybrid 검색으로 문서를 찾고, 재귀 SQL로 개념 간 관계를 탐색해 근거 있는 답변을 구성합니다. Standard Edition의 TRANSACTION 테이블을 사용합니다.

## 읽는 순서

- 문서 검색: 11.1 → 11.2 → 11.3
- 재귀 SQL: 11.4 → 11.8
- GraphRAG: 검색 기초 → 11.4 → 11.5 → 11.6 → 11.7

```text
질문 → 개념·별칭 검색 → 관계 탐색 → 원문 후보 → Hybrid 검색 → 근거와 경로 → LLM 답변
```

DBMS는 데이터 저장·검색·관계 탐색을 수행합니다. 문서 분할, 임베딩 모델 실행과 최종 LLM 호출은 애플리케이션이 담당합니다.

## 구성

| 절 | 학습 내용 |
|---|---|
| [11.1 시작하기](./getting-started/) | 검색 개요·지원 환경과 모델 없는 SQL 실습 |
| [11.2 검색 방식과 인덱스 선택](./search-indexes/) | 검색 방식·거리·인덱스와 권한 필터 |
| [11.3 내 문서로 검색과 RAG 만들기](./document-rag/) | 실제 임베딩·문서 적재·검색·RAG |
| [11.4 재귀 SQL로 관계 탐색하기](./recursive-sql/) | 반복·중복 제거·순환·깊이·경로 |
| [11.5 개념·관계·근거 모델 만들기](./knowledge-model/) | 5개 테이블과 별칭·관계·원문 근거 |
| [11.6 관계를 활용한 GraphRAG 검색](./graph-search/) | 개념 검색·관계 후보·Hybrid 검색과 결과 해석 |
| [11.7 Ollama로 근거 있는 답변 만들기](./ollama/) | 예제 설치·답변 생성·인용과 경로 확인 |
| [11.8 애플리케이션 연동](./application-integration/) | 언어별 VECTOR 바인딩과 재귀 Python 예제 |
| [11.9 운영과 성능 관리](./operations/) | 트랜잭션·실행 계획·메모리·백업과 복원 |
| [11.10 문제 해결과 실습 정리](./troubleshooting/) | 오류 진단·품질 평가·실습 객체 정리 |
