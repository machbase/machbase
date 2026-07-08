---
type: docs
title: 'TAG data UPDATE WHERE/SET constraints (TODO(verify))'
weight: 20
---

> **확인 중 (TODO(verify))**: 이 문서의 일부 내용은 추가 검증이 필요합니다. 확인 중인 항목은 별도 표시합니다.

TAG 테이블의 UPDATE 문에서 사용할 수 있는 WHERE 절 조건과 SET 절 컬럼에는 제약이 있습니다.

## SET 절 제약

| 컬럼 역할 | SET 가능 여부 |
|-----------|:------------:|
| 데이터 컬럼 (일반 VALUE) | 확인 중 |
| SUMMARIZED 속성 컬럼 | O |
| BASETIME 컬럼 (time 축) | X |
| PRIMARY KEY 컬럼 (name) | X |
| 메타데이터 컬럼 | UPDATE ... METADATA로 별도 처리 |

현재 확인된 동작:
- `SUMMARIZED` 속성이 있는 컬럼: SET 가능
- `BASETIME` 컬럼: SET 불가
- `PRIMARY KEY` 컬럼(`name`): SET 불가

> 일반 VALUE 컬럼(SUMMARIZED 속성 없음)의 SET 가능 여부는 현재 검증 중입니다.

## WHERE 절 제약

### 데이터 UPDATE

```sql
UPDATE TAG TABLE table_name
   SET col = value
 WHERE name = 'tag-name';
```

| WHERE 조건 | 지원 여부 |
|-----------|:---------:|
| `name = '...'` (PK 등치 조건) | O |
| `name IN (...)` | 확인 중 |
| `time BETWEEN t1 AND t2` | X (계획 중: dbms-nfx#3733) |
| 일반 predicate (value 조건 등) | X (계획 중: dbms-nfx#3733) |

### 메타데이터 UPDATE

```sql
UPDATE table_name METADATA
   SET meta_col = value
 WHERE condition;
```

| WHERE 조건 | 지원 여부 |
|-----------|:---------:|
| `name = '...'` | O |
| 메타데이터 컬럼 조건 | O |
| 데이터 컬럼(`time`, `value`) 조건 | X |

## 컬럼 역할 확인 방법

`DESC` 명령으로 컬럼의 FLAG 값을 확인해 역할을 구분할 수 있습니다.

```sql
DESC sensor_tag;
```

출력의 `FLAG` 컬럼 값으로 역할을 구분합니다:

| FLAG 값 | 역할 |
|---------|------|
| 1 | Tag Data 컬럼 |
| 2 | Rollup 컬럼 |
| 4 | Tag Meta 컬럼 |
| 8 | Tag Stat 컬럼 |

또는 시스템 테이블에서 직접 조회합니다.

```sql
SELECT NAME, TYPE, FLAG
  FROM M$SYS_COLUMNS
 WHERE TABLE_ID = (
     SELECT ID FROM M$SYS_TABLES WHERE NAME = 'SENSOR_TAG'
 );
```

## 오류 사례

```sql
-- 오류: BASETIME 컬럼을 SET 대상으로 지정
UPDATE TAG TABLE sensor_tag
   SET time = TO_DATE('2024-01-01', 'YYYY-MM-DD')
 WHERE name = 'TEMP-01';

-- 오류: time BETWEEN 조건 사용 (현재 미지원)
UPDATE TAG TABLE sensor_tag
   SET value = 0.0
 WHERE name = 'TEMP-01'
   AND time BETWEEN TO_DATE('2024-01-01', 'YYYY-MM-DD')
                AND TO_DATE('2024-01-02', 'YYYY-MM-DD');
```

## 관련 문서

- [TAG data UPDATE syntax](../tag-data-update-syntax/) — TAG UPDATE 문법 개요
- [ROLLUP_REBUILD syntax](../../rollup-rebuild-syntax/) — 데이터 수정 후 집계 재계산
