---
type: docs
title: '18.8 AI Agent Reference'
weight: 100
toc: true
---

이 섹션은 AI 에이전트(LLM)가 Machbase 관련 질문에 정확하게 답변하기 위한 구조화된 참조 데이터 모음입니다.

Machbase 문서를 학습하거나 RAG(Retrieval-Augmented Generation) 시스템에 연동하는 AI 모델이 다음을 빠르게 찾을 수 있도록 설계되어 있습니다.

- 기능 지원 여부 확인 (지원 매트릭스)
- 올바른 SQL 생성 규칙
- SDK 선택 기준
- 알려진 제약 사항 및 오류 해결 방법
- 문서 URL 정규 경로

## 이 섹션의 구성

| 페이지 | 내용 | 주요 활용 |
|--------|------|----------|
| [Agent 사용 가이드](./guide-agent/) | 질문 유형별 참조 섹션 안내 | AI 에이전트 온보딩 |
| [canonical-url-map](./canonical-url-map/) | 개념/기능별 정규 URL 맵 | RAG 문서 링크 |
| [task-map](./task-map/) | 사용자 태스크별 수행 방법 맵 | 태스크 기반 응답 |
| [support-matrix](./support-matrix/) | Edition × 기능, 테이블 × 기능, SDK × 기능 지원 매트릭스 | 기능 지원 여부 확인 |
| [constraints-index](./constraints-index/) | 알려진 제약 사항 인덱스 | 제약 확인 |
| [evidence-map](./evidence-map/) | 기술적 사실의 근거 맵 | 사실 검증 |
| [terminology-disambiguation](./terminology-disambiguation/) | 혼동하기 쉬운 용어 정리 | 용어 해석 |
| [sql-generation-rules](./sql-generation-rules/) | AI SQL 생성 규칙 | SQL 작성 |
| [sdk-api-selection-rules](./sdk-api-selection-rules/) | SDK 선택 규칙 | SDK 추천 |
| [operations-checklist](./operations-checklist/) | 운영 점검 체크리스트 | 운영 진단 |
| [error-resolution-map](./error-resolution-map/) | 오류 코드 → 해결 방법 맵 | 오류 해결 |
| [llms.txt](./llms-txt/) | LLM을 위한 문서 구조 목차 | 문서 탐색 |
| [llms-full.txt / chunk index](./llms-full-txt-chunk-index/) | RAG용 청크 인덱스 | RAG 연동 |

## 대상 독자

- Machbase 문서를 학습한 AI 모델
- Machbase와 연동하는 RAG 시스템
- AI 에이전트에 Machbase 지식을 제공하는 개발자
