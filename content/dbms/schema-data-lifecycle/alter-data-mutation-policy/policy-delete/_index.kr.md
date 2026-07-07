---
type: docs
title: 'DELETE 정책'
weight: 20
---

테이블 타입별 DELETE 지원 범위와 조건을 정리합니다.

## 테이블 타입별 DELETE 지원

| 테이블 타입 | DELETE 지원 | 조건 |
|------------|------------|------|
| TAG | O | BEFORE 조건 필수 |
| LOG | O | BEFORE 조건 필수 |
| RDB | O | 일반 WHERE 조건 자유 |
| VOLATILE | O | WHERE 조건 자유 |
| LOOKUP | O | PK 기준 권장. 일반 조건식은 계획 중 (#3696) |

## RDB 테이블 DELETE

일반 관계형 DB와 동일하게 동작합니다.

```sql
-- WHERE 조건으로 삭제
DELETE FROM orders WHERE order_id = 1001;

-- 상태 기반 삭제
DELETE FROM orders WHERE status = 'CANCELLED';

-- 전체 삭제 (주의: RDB는 TRUNCATE로 대체 권장)
DELETE FROM temp_data;
```

## VOLATILE 테이블 DELETE

DELETE WHERE는 기본 키(PK)가 지정된 VOLATILE 테이블에서만 허용됩니다.

- WHERE 절에는 (기본 키 컬럼) = (값) 조건만 허용됩니다.
- 기본 키가 아닌 컬럼을 WHERE 조건으로 사용할 수 없습니다.

```sql
-- 조건 삭제
DELETE FROM device_status WHERE device_id = 'DEV-01';

-- 오래된 데이터 삭제
DELETE FROM device_status WHERE updated_at < DATEADD('h', -24, NOW);
```

## LOOKUP 테이블 DELETE

DELETE WHERE는 기본 키(PK)가 지정된 LOOKUP 테이블에서만 허용됩니다.

- WHERE 절에는 (기본 키 컬럼) = (값) 조건만 허용됩니다.
- 기본 키가 아닌 컬럼을 WHERE 조건으로 사용할 수 없습니다.

```sql
-- PK 기준 삭제 (권장)
DELETE FROM alarm_threshold WHERE sensor_id = 'TEMP-01';
```

> 일반 조건식(non-PK) DELETE는 dbms-nfx#3696에서 계획 중입니다.

## LOG 테이블 DELETE

LOG 테이블은 다양한 DELETE 구문을 지원합니다.

```sql
DELETE FROM table OLDEST N ROWS;          -- 가장 오래된 N건 삭제
DELETE FROM table EXCEPT N ROWS;          -- 최근 N건을 제외하고 전체 삭제
DELETE FROM table EXCEPT N DAY;           -- 최근 N일 데이터를 제외하고 전체 삭제
DELETE FROM table;                        -- 전체 삭제
DELETE FROM table BEFORE datetime_expr;   -- 특정 시점 이전 삭제
```

> DURATION, OLDEST, EXCEPT 구문은 TAG 및 Rollup 테이블에서는 사용할 수 없습니다.

## TAG 테이블 DELETE

TAG와 LOG 테이블의 DELETE는 **BEFORE 조건이 필수**입니다. 특정 시점 이전의 데이터를 일괄 삭제하는 방식으로만 동작합니다.

```sql
-- TAG: 30일 이전 데이터 삭제
DELETE FROM tag BEFORE TO_DATE('2024-01-01', 'YYYY-MM-DD');

-- LOG: 특정 시각 이전 데이터 삭제
DELETE FROM sensor_log BEFORE '2024-01-01 00:00:00 000:000:000';
```

> BEFORE 조건 없이 DELETE를 실행하면 오류가 발생합니다. 상세 내용은 [TAG/KV DELETE 허용 조건](../condition-tag-kv-delete-before/) 페이지를 참고하세요.

### TAG 테이블 DELETE WHERE (조건부 삭제)

Tag 테이블은 tag name, tag name과 시간 조건, 또는 시간 조건만으로 DELETE WHERE를 지원합니다.
시간 조건에는 `=`, `<`, `<=`, `BETWEEN`을 사용할 수 있습니다.

```sql
-- tag name 기준 삭제
DELETE FROM tag WHERE tag_name = 'my_tag_2021';

-- tag name + 시간 기준 삭제
DELETE FROM tag WHERE tag_name = 'my_tag_2021' AND tag_time < TO_DATE('2021-07-01', 'YYYY-MM-DD');
DELETE FROM tag WHERE tag_name = 'my_tag_2021' AND tag_time BETWEEN TO_DATE('2021-07-01', 'YYYY-MM-DD') AND TO_DATE('2021-07-02', 'YYYY-MM-DD');

-- 시간 조건만으로 삭제
DELETE FROM tag WHERE tag_time <= TO_DATE('2021-07-01', 'YYYY-MM-DD');
```

> 삭제 후 물리적 공간 해제까지 시간이 걸릴 수 있습니다.

### TAG ROLLUP DELETE WHERE

```sql
-- rollup을 tag name 기준으로 삭제
DELETE FROM tag ROLLUP WHERE tag_name = 'my_tag_2021';

-- rollup을 tag name + 시간 기준으로 삭제
DELETE FROM tag ROLLUP WHERE tag_name = 'my_tag_2021' AND tag_time < TO_DATE('2021-07-01', 'YYYY-MM-DD');

-- 시간 조건만으로 rollup 삭제
DELETE FROM tag ROLLUP WHERE tag_time BETWEEN TO_DATE('2021-07-01', 'YYYY-MM-DD') AND TO_DATE('2021-07-02', 'YYYY-MM-DD');
```

## 하위 페이지

- [LOOKUP 일반 조건식 DELETE](./condition-lookup-delete/): 계획된 기능 상세
- [TAG 메타데이터 삭제](./delete-tag-metadata/): TAG 테이블 메타데이터 삭제 구문
