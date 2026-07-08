---
type: docs
title: 'TAG data UPDATE 지원표'
weight: 40
---

이 페이지는 TAG 테이블의 UPDATE 기능 현재 지원 현황과 계획 중인 기능을 정리합니다.

## WHERE 조건별 지원 현황

| WHERE 조건 | 현재 지원 | 계획 중 | 비고 |
|-----------|:---------:|:-------:|------|
| `WHERE name = '...'` (PK 단일 조건) | O | — | 현재 유일하게 완전 지원 |
| `WHERE name IN ('a', 'b', ...)` | X | O | planned: dbms-nfx#3733 |
| `WHERE name LIKE '...'` | X | O | planned: dbms-nfx#3733 |
| `WHERE time BETWEEN ... AND ...` | X | O | planned: dbms-nfx#3733 |
| `WHERE time >= ... AND time <= ...` | X | O | planned: dbms-nfx#3733 |
| 조건 없이 전체 UPDATE | X | X | 미지원, 계획 없음 |

## SET 대상 컬럼별 지원 현황

| SET 대상 | 현재 지원 | 비고 |
|---------|:---------:|------|
| SUMMARIZED 속성 컬럼 | O | 사용자 정의 집계 컬럼 |
| 일반 메타 컬럼 | O | TAG 스키마 정의에 따라 다름 |
| `name` (TAGNAME, PK) | X | PK 컬럼 변경 불가 |
| `time` (BASETIME) | X | 시간 컬럼 변경 불가 |
| `value` (기본 측정값 컬럼) | X | 불가 |

## 현재 지원되는 UPDATE 예시

```sql
-- 가능: name 조건으로 SUMMARIZED 컬럼 업데이트
UPDATE sensor_data
SET min_value = 0.0, max_value = 100.0
WHERE name = 'sensor01';

```

## 현재 불가능한 UPDATE 예시

```sql
-- 불가: time 컬럼 조건
UPDATE sensor_data SET min_value = 0.0
WHERE name = 'sensor01' AND time >= TO_DATE('2024-01-01');  -- 오류

-- 불가: BASETIME 컬럼 업데이트
UPDATE sensor_data SET time = NOW() WHERE name = 'sensor01';  -- 오류

-- 불가: TAGNAME 컬럼 업데이트
UPDATE sensor_data SET name = 'new_sensor' WHERE name = 'sensor01';  -- 오류
```

## 계획 중인 기능 (planned: dbms-nfx#3733)

다음 기능은 현재 미지원이며, 향후 업데이트에서 제공될 예정입니다.

- **시간 범위 조건**: `WHERE name = '...' AND time BETWEEN ... AND ...`
- **LIKE 조건**: `WHERE name LIKE 'sensor%'`
- **복합 조건 UPDATE**: 여러 조건을 결합한 UPDATE

## 현재 제약 우회 방법

| 필요 기능 | 현재 우회 방법 |
|----------|--------------|
| 시간 범위 내 데이터 수정 | 해당 범위 데이터를 DELETE 후 재삽입 |
| 여러 태그 일괄 업데이트 | 태그별로 `WHERE name = '...'` 조건으로 반복 UPDATE |

> **주의**: TAG 테이블에서 DELETE 후 재삽입은 ROLLUP 데이터에 영향을 줄 수 있습니다. 중요 데이터는 변경 전 백업을 권장합니다.
