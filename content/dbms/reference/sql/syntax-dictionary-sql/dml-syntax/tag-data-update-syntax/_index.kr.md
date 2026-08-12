---
type: docs
title: '18.1.1.12.1 TAG data UPDATE'
weight: 10
toc: true
---

TAG 테이블의 시계열 데이터는 일반 `UPDATE` 문으로 수정합니다. `UPDATE TAG TABLE`이라는
별도 키워드는 사용하지 않습니다.

<span class="badge-since">Machbase 8.7.0부터 지원되는 기능</span>

TAG data UPDATE는 Standard Edition의 논리 TAG 테이블에서만 지원합니다.

## Syntax

```sql
UPDATE table_name
   SET data_column = expression [, data_column = expression ...]
 WHERE tag_selector
   AND time_condition
   [AND data_predicate ...];
```

`tag_selector`에는 `name = ...`, `name IN (...)`, `name LIKE ...` 조건을 사용할 수 있습니다.
`time_condition`은 BASETIME 컬럼의 등치, `BETWEEN`, 양쪽 범위, 한쪽 범위 조건을 사용할 수
있습니다.

## Examples

### 단일 태그와 시간 범위

```sql
UPDATE sensor_tag
   SET value = 110,
       status = 1
 WHERE name = 'TEMP-01'
   AND time >= TO_DATE('2026-07-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
   AND time <  TO_DATE('2026-07-02 00:00:00', 'YYYY-MM-DD HH24:MI:SS');
```

### 여러 태그

```sql
UPDATE sensor_tag
   SET note = 'corrected'
 WHERE name IN ('TEMP-01', 'TEMP-02')
   AND time BETWEEN TO_DATE('2026-07-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
                AND TO_DATE('2026-07-01 23:59:59', 'YYYY-MM-DD HH24:MI:SS');
```

### LIKE와 데이터 컬럼 predicate

```sql
UPDATE sensor_tag
   SET status = 7
 WHERE name LIKE 'TEMP-%'
   AND time >= TO_DATE('2026-07-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
   AND value > 100;
```

### CASE 표현식

```sql
UPDATE sensor_tag
   SET grade = CASE
                 WHEN 1 = 1 THEN 'HIGH'
                 ELSE 'LOW'
               END
 WHERE name = 'TEMP-01'
   AND time >= TO_DATE('2026-07-01', 'YYYY-MM-DD');
```

## Metadata UPDATE

TAG 메타데이터 컬럼은 TAG data UPDATE의 SET 대상이 아닙니다. 메타데이터는
`UPDATE ... METADATA` 구문으로 수정합니다.

```sql
UPDATE sensor_tag METADATA
   SET location = 'zone-2',
       owner = 'ops'
 WHERE name = 'TEMP-01';
```

## Restrictions

- WHERE 절에는 하나의 태그 선택 조건과 하나 이상의 BASETIME 조건이 필요합니다. `name =`,
  `name IN (...)`, `name LIKE ...`와 등치·BETWEEN·양쪽/한쪽 시간 범위를 사용할 수 있으며,
  데이터 컬럼 조건은 `AND`로 추가할 수 있습니다.
- `OR`, 서브쿼리, 집계식, non-bare tag/axis 표현식은 UPDATE 대상 조건으로 사용할 수 없습니다.
- `name`(PRIMARY KEY), `time`(BASETIME), 메타데이터 컬럼, 숨김/시스템 컬럼은 data UPDATE의
  SET 대상이 될 수 없습니다.
- SET 우변은 상수, bind 변수, 기존 행 컬럼을 참조하지 않는 함수·연산식·`CASE`·NULL만
  사용할 수 있습니다. `value = value + 1`처럼 기존 행 컬럼을 참조하는 식은 허용되지 않습니다.
- UPDATE는 이미 구체화된 롤업 row를 자동으로 보정하지 않습니다. 롤업 조회 전에 영향을
  받은 구간을 `ROLLUP_REBUILD`로 재구성합니다.

## Related

- [TAG data UPDATE WHERE/SET constraints](../tag-data-update-where-set-constraints/)
- [ROLLUP_REBUILD syntax](../../rollup-rebuild-syntax/)
