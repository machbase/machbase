---
type: docs
title: '16.8 AI Agent Reference'
weight: 100
toc: true
description: 'Machbase DBMS 문서를 사용하는 AI 에이전트와 RAG 시스템을 위한 탐색 및 근거 가이드'
---

AI Agent Reference는 AI 에이전트와 RAG 시스템이 Machbase DBMS 8.7 문서에서 정확한
정본을 찾도록 돕는 탐색 계층입니다. SQL 문법, SDK 지원 여부와 운영 절차를 이 절에서
다시 정의하지 않고 각 기능의 정본으로 연결합니다.

## 구성

| 페이지 | 목적 |
|--------|------|
| [Agent 사용 가이드](./guide-agent/) | 질문 분류, 검증 순서와 응답 원칙 |
| [canonical-url-map](./canonical-url-map/) | 주제별 정규 문서 URL |
| [task-map](./task-map/) | 사용자 작업별 읽기·검증 순서 |
| [support-matrix](./support-matrix/) | Edition·테이블·SDK 지원표 정본 찾기 |
| [constraints-index](./constraints-index/) | 제약과 오류 조건 정본 찾기 |
| [evidence-map](./evidence-map/) | 주장 유형별 근거 선택 |
| [terminology-disambiguation](./terminology-disambiguation/) | 혼동하기 쉬운 용어 확인 |
| [sql-generation-rules](./sql-generation-rules/) | SQL 생성 전 검증 규칙 |
| [sdk-api-selection-rules](./sdk-api-selection-rules/) | SDK와 API 선택 순서 |
| [operations-checklist](./operations-checklist/) | 안전한 운영 답변 생성 순서 |
| [error-resolution-map](./error-resolution-map/) | 오류 진단 정본 찾기 |
| [llms.txt](./llms-txt/) | 간략한 기계 판독 문서 맵 |
| [전체 본문과 RAG 인덱스](./llms-full-txt-chunk-index/) | 전체 Markdown과 JSON 문서 인덱스 |

## 기계 판독 출력

- [llms.txt](/kr/llms.txt)
- [llms-full.txt](/kr/llms-full.txt)
- [llms-chunks.json](/kr/llms-chunks.json)

위 출력은 현재 한국어 DBMS 문서만 포함합니다. Machbase Neo와 보존용 DBMS 8.5 문서는
포함하지 않습니다.

## 사용 원칙

1. 서버 버전, Edition, 테이블 타입과 SDK를 먼저 확인합니다.
2. 기능 정본과 지원 범위를 함께 읽습니다.
3. 확인되지 않은 문법, 기본값, 제한과 오류 코드를 만들지 않습니다.
4. 운영 변경은 대상, 영향, 복구 방법과 완료 조건을 명시합니다.
5. 답변 링크는 공개 canonical URL을 사용합니다.
