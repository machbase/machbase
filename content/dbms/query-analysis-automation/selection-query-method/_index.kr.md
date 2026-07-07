---
type: docs
title: '조회 방식 선택'
weight: 10
---

Machbase에서 데이터를 조회하는 방법은 목적과 테이블 타입에 따라 다릅니다.

## 조회 방식 요약

| 조회 목적 | 권장 방식 |
|----------|---------|
| 특정 시간 범위 시계열 조회 | WHERE + 시간 조건 또는 DURATION |
| 최근 N분/시간/일 데이터 | DURATION |
| 태그별 집계 (평균, 최대, 최소) | GROUP BY + 집계 함수 |
| 분 단위 자동 집계 결과 조회 | ROLLUP |
| 여러 TAG를 컬럼으로 배열 | PIVOT |
| 누락 구간 보간 | INTERPOLATION 힌트 |
| 텍스트 패턴 검색 | SEARCH / ESEARCH / LIKE |
| 설정값·상태 JOIN | LOG/TAG ↔ LOOKUP/VOLATILE JOIN |
| 실시간 변환·적재 | STREAM |

하위 페이지에서 테이블 타입별 조회 제약과 선택 가이드를 확인하세요.
