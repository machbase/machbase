---
type: docs
title: '공통 쿼리와 자동 처리 참고'
weight: 970
---

Machbase는 시계열 데이터에 최적화된 다양한 조회·분석 구문을 제공합니다. 일반 SQL에 더해 DURATION, PIVOT, ROLLUP, SERIES BY, 보간, 윈도우 함수 등 시계열 분석에 특화된 확장 문법을 갖추고 있습니다.

## 이 장에서 다루는 내용

- **[조회 방식 선택](./selection-query-method/)**: 상황에 맞는 쿼리 방식 선택 기준
- **[SELECT 조회](./query-select/)**: 기본 SELECT, DURATION, 시간 조건, 힌트, EXPLAIN
- **[조건 검색](./condition-conditional-search/)**: 텍스트·정규식·JSON·네트워크 타입 조건
- **[분석 쿼리](./item/)**: 집계, JOIN, PIVOT, 윈도우 함수, 보간, ROLLUP
- **[자동 처리](./automation/)**: STREAM 기반 실시간 데이터 처리 자동화
