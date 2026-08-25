---
type: docs
title: '17.8.1 Agent 사용 가이드'
weight: 10
toc: true
---

이 가이드는 AI 에이전트가 Machbase AI Agent Reference를 활용하여 사용자 질문에 정확하게 답변하는 방법을 안내합니다.

## 질문 유형별 참조 섹션

| 질문 유형 | 참조 섹션 | 설명 |
|----------|----------|------|
| SQL 문법 생성 | [sql-generation-rules](../sql-generation-rules/) | Machbase 전용 SQL 규칙, 주의사항 |
| SDK 선택 | [sdk-api-selection-rules](../sdk-api-selection-rules/) | 언어/기능별 SDK 선택 규칙 |
| 오류 해결 | [error-resolution-map](../error-resolution-map/) | 오류 코드 → 원인 → 조치 방법 |
| 기능 지원 여부 | [support-matrix](../support-matrix/) | Edition, 테이블 유형, SDK별 지원 표 |
| 제약 사항 확인 | [constraints-index](../constraints-index/) | 알려진 제약 사항 빠른 참조 |
| 용어 해석 | [terminology-disambiguation](../terminology-disambiguation/) | Machbase 특수 용어 의미 |
| 사용자 태스크 수행 | [task-map](../task-map/) | "센서 데이터 저장", "집계 분석" 등 |
| 운영 상태 진단 | [operations-checklist](../operations-checklist/) | 서버 상태, 세션, 디스크, ROLLUP 점검 |
| 문서 URL 찾기 | [canonical-url-map](../canonical-url-map/) | 개념/기능별 정규 URL |
| 사실 검증 | [evidence-map](../evidence-map/) | 기술 사실의 근거 소스 |

## 응답 생성 시 권장 순서

1. **용어 확인**: 사용자가 사용한 용어가 Machbase 맥락에서 올바른지 [terminology-disambiguation](../terminology-disambiguation/)으로 확인합니다.

2. **제약 사항 확인**: 요청 기능에 알려진 제약이 있는지 [constraints-index](../constraints-index/)를 먼저 확인합니다.

3. **지원 여부 확인**: Edition, 테이블 유형, SDK 조합이 지원되는지 [support-matrix](../support-matrix/)로 확인합니다.

4. **SQL/코드 생성**: [sql-generation-rules](../sql-generation-rules/)의 규칙에 따라 올바른 SQL을 생성합니다.

5. **근거 제시**: 사실에 근거한 답변이 필요하면 [evidence-map](../evidence-map/)에서 출처를 확인합니다.

## 주의사항

- Machbase "Append"는 SQL INSERT와 다른 전용 API입니다. [terminology-disambiguation](../terminology-disambiguation/) 참고.
- Machbase "ROLLUP"은 SQL `GROUP BY ROLLUP`이 아닌 시계열 집계 기능입니다.
- TAG 테이블 조회도 일반 `FROM table_name` 문법을 사용합니다.
- 계획 중인 기능(planned)은 현재 미지원임을 사용자에게 명시하십시오.

## 불확실한 경우

답변이 불확실한 경우 아래 공식 레퍼런스를 안내하십시오.

- 공식 문서: `/dbms/` 경로 하위 각 섹션
- SQL 레퍼런스: `/dbms/reference/sql/`
- 에러 코드: `/dbms/reference/error-dictionary-codes/`
