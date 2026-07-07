---
type: docs
title: '테이블 변경'
weight: 20
---

`ALTER TABLE` 문으로 컬럼을 추가하거나 속성을 변경합니다. 지원 범위는 테이블 타입에 따라 다릅니다.

## 테이블 타입별 지원 범위

| 작업 | LOG | TAG | RDB | VOLATILE | LOOKUP |
|------|-----|-----|-----|----------|--------|
| ADD COLUMN | O | O (METADATA만) | O | O | O |
| DROP COLUMN | O | O (METADATA만) | O | O | O |
| RENAME COLUMN | X | O (일반 컬럼) | O | X | X |
| MODIFY COLUMN | O | O (일반 컬럼) | X | X | X |
| RENAME TABLE | X | X | O | X | X |
| ADD RETENTION | O | O | X | X | X |
| DROP RETENTION | O | O | X | X | X |

## ADD COLUMN

```sql
ALTER TABLE table_name ADD COLUMN (column_name type [DEFAULT value]);
```

```sql
-- LOG 테이블에 컬럼 추가
ALTER TABLE web_access ADD COLUMN (region VARCHAR(32));
ALTER TABLE web_access ADD COLUMN (resp_time DOUBLE);

-- LOOKUP 테이블에 컬럼 추가
ALTER TABLE country_code ADD COLUMN (capital VARCHAR(64));

-- RDB 테이블에 컬럼 추가
ALTER TABLE orders ADD COLUMN (note VARCHAR(256));

-- TAG 테이블 METADATA에 컬럼 추가
ALTER TABLE sensor_data METADATA ADD COLUMN (unit VARCHAR(16));
```

## DROP COLUMN

```sql
ALTER TABLE table_name DROP COLUMN (column_name);
```

```sql
ALTER TABLE web_access DROP COLUMN (region);

-- TAG 테이블 METADATA 컬럼 삭제
ALTER TABLE sensor_data METADATA DROP COLUMN (unit);
```

## RENAME COLUMN

TAG 일반 컬럼과 RDB 테이블에서만 지원됩니다. LOG, VOLATILE, LOOKUP 테이블은 지원하지 않습니다.

```sql
ALTER TABLE table_name RENAME COLUMN old_name TO new_name;
```

```sql
-- TAG 테이블 일반 컬럼 이름 변경
ALTER TABLE sensor_data RENAME COLUMN value TO temperature;

-- RDB 테이블 컬럼 이름 변경
ALTER TABLE orders RENAME COLUMN note TO memo;
```

## MODIFY COLUMN

LOG 테이블과 TAG 테이블의 일반 컬럼에서 지원됩니다. RDB, VOLATILE, LOOKUP 테이블은 지원하지 않습니다.

```sql
-- VARCHAR 크기 확장 (줄이기는 불가)
ALTER TABLE web_access MODIFY COLUMN (uri VARCHAR(2048));

-- NOT NULL 제약 추가 (LOG 테이블)
ALTER TABLE web_access MODIFY COLUMN status NOT NULL;

-- MINMAX_CACHE_SIZE 변경 (LOG 테이블 컬럼)
ALTER TABLE web_access MODIFY COLUMN status SET MINMAX_CACHE_SIZE = 20480;
```

## RENAME TABLE

RDB 테이블에서만 지원됩니다.

```sql
ALTER TABLE old_name RENAME TO new_name;
```

```sql
-- RDB 테이블 이름 변경
ALTER TABLE orders RENAME TO order_history;
```

## 주의사항

- LOG 테이블에 추가된 컬럼은 기존 레코드에서 NULL로 읽힙니다.
- TAG 테이블의 일반 데이터 컬럼(PRIMARY KEY, BASETIME)은 변경할 수 없습니다.
- VOLATILE 테이블 변경 사항은 서버 재시작 후 초기화 스크립트로 재적용해야 합니다.
