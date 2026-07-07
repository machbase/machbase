---
type: docs
title: '테이블 타입별 조회 제약'
weight: 20
---

테이블 타입에 따라 사용 가능한 조회 구문과 제약이 다릅니다.

## 테이블 타입별 조회 지원 범위

| 기능 | TAG | LOG | RDB | VOLATILE | LOOKUP |
|------|-----|-----|-----|---------|--------|
| SELECT * | O | O | O | O | O |
| WHERE 시간 조건 | O | O | O | O | O |
| DURATION | O | O | X | X | X |
| GROUP BY | O | O | O | O | O |
| ORDER BY | O | O | O | O | O |
| LIMIT | O | O | O | O | O |
| SERIES BY | O (시간) | O | O | O | O |
| JOIN | O | O | O | O | O |
| PIVOT | O | O | O | O | O |
| ROLLUP 조회 | O (WITH ROLLUP 테이블) | X | X | X | X |
| INTERPOLATION 힌트 | O | X | X | X | X |
| SAMPLING 힌트 | O | X | X | X | X |
| UNION ALL | O | O | O | O | O |

## 주요 제약

### TAG 테이블
- `DURATION` 키워드를 사용하면 BASETIME 컬럼 기준으로 검색 범위를 좁혀 성능을 크게 향상시킵니다.
- ROLLUP, INTERPOLATION, SAMPLING 힌트는 TAG 테이블 전용 기능입니다.
- `FROM TAG METADATA`로 메타데이터만 조회할 수 있습니다.

### LOG 테이블
- `DURATION`은 `_ARRIVAL_TIME` 기준으로 동작합니다.
- KEYWORD 인덱스가 있으면 `SEARCH`, `ESEARCH` 조건을 사용할 수 있습니다.

### VOLATILE 테이블
- DURATION은 지원하지 않습니다.
- `_ARRIVAL_TIME` 컬럼이 있으나 DURATION의 의미상 시계열 조회에는 적합하지 않습니다.

### LOOKUP 테이블
- 주로 JOIN 참조 테이블로 활용됩니다.
- DURATION 미지원.
