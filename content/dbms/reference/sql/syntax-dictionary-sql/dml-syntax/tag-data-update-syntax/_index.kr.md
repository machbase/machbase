---
type: docs
title: 'TAG data UPDATE syntax (planned: dbms-nfx#3733)'
weight: 10
---

> **계획 중 (planned: dbms-nfx#3733)**: 이 문서에 설명된 일부 기능은 아직 구현 중입니다. 현재 지원 범위와 향후 계획을 함께 기술합니다.

## 현재 지원 상태

현재 TAG 테이블에서 지원되는 UPDATE는 다음 두 가지입니다.

### 1. SUMMARIZED 컬럼 UPDATE (현재 지원)

TAG 테이블의 `SUMMARIZED` 속성 컬럼에 대해 `name` 조건으로 단순 값 갱신이 가능합니다.

```sql
UPDATE TAG TABLE table_name
   SET summarized_col = value
 WHERE name = 'tag-name';
```

```sql
-- SUMMARIZED 컬럼 갱신 예시
UPDATE TAG TABLE sensor_tag
   SET value = 0.0
 WHERE name = 'TEMP-01';
```

### 2. 메타데이터 UPDATE (현재 지원)

TAG 테이블의 메타데이터 컬럼(METADATA)은 `UPDATE ... METADATA` 구문으로 갱신합니다.

```sql
UPDATE table_name METADATA
   SET meta_col = value
 WHERE name = 'tag-name';

-- 메타데이터 컬럼 조건도 사용 가능
UPDATE sensors METADATA
   SET status = 'DONE'
 WHERE status = 'READY';
```

메타데이터 UPDATE의 제약은 [TAG data UPDATE WHERE/SET constraints](../tag-data-update-where-set-constraints/)를 참고하세요.

## 향후 계획 (planned: dbms-nfx#3733)

향후 릴리스에서는 TAG 테이블 데이터에 대한 일반 predicate 기반 UPDATE를 지원할 예정입니다.

```sql
-- 계획 중인 문법 (현재 미지원)
UPDATE TAG TABLE table_name
   SET value_col = expr
 WHERE name = 'tag-name'
   [AND time BETWEEN t1 AND t2];
```

현재 이 문법은 지원되지 않으며, 실행하면 오류가 반환됩니다.

## 현재 제약사항

| 항목 | 현재 상태 |
|------|-----------|
| 데이터 컬럼 갱신 | SUMMARIZED 컬럼만, name 조건 필수 |
| 시간 범위 조건 WHERE time BETWEEN | 미지원 (계획 중) |
| 일반 predicate UPDATE | 미지원 (계획 중) |
| 메타데이터 UPDATE | 지원 (메타데이터 컬럼 조건 포함) |

## 임시 방법

TAG 데이터 수정이 필요한 경우 현재는 다음 절차를 권장합니다.

1. 수정 대상 데이터를 삭제합니다.
2. 수정된 값으로 재입력합니다.
3. 필요 시 `ROLLUP_REBUILD`로 집계를 재계산합니다.

```sql
-- 1. 이상 데이터 삭제
DELETE FROM sensor_tag
 WHERE name = 'TEMP-01'
   AND time BETWEEN TO_DATE('2024-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
                AND TO_DATE('2024-01-01 01:00:00', 'YYYY-MM-DD HH24:MI:SS');

-- 2. 정상 데이터 재입력
INSERT INTO sensor_tag (name, time, value) VALUES ('TEMP-01', TO_DATE('2024-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 25.0);
-- ... (추가 행)

-- 3. ROLLUP 재계산 (Standard Edition만)
EXEC ROLLUP_REBUILD(sensor_tag, _rollup_sensor_tag_value_min,
    TO_DATE('2024-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'),
    TO_DATE('2024-01-01 01:00:00', 'YYYY-MM-DD HH24:MI:SS'));
```

## 관련 문서

- [TAG data UPDATE WHERE/SET constraints](../tag-data-update-where-set-constraints/) — WHERE/SET 제약 상세
- [ROLLUP_REBUILD syntax](../../rollup-rebuild-syntax/) — 집계 재계산
