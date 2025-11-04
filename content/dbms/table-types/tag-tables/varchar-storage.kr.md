---
title: 'VARCHAR 저장소 최적화'
type: docs
weight: 100
---

## 개요

고정 영역과 가변 영역에 데이터가 저장되는 시점을 제어하여 VARCHAR 컬럼 저장소를 최적화하고, 성능과 저장 효율성을 모두 향상시킵니다.

## VARCHAR 저장소 옵션
varchar 데이터를 고정 영역에 저장할 수 있는 최대 크기입니다.
이 값보다 긴 varchar 값은 가변 영역에 저장됩니다.
이 값은 15에서 127까지 지정할 수 있으며, 기본값은 15입니다.

```sql
-- 입력 VARCHAR 데이터의 크기가 15 이하이면 확장 파일 대신 고정 데이터 파일에 저장됩니다.

CREATE TAG TABLE tag (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED, strval VARCHAR(100)) VARCHAR_FIXED_LENGTH_MAX = 15;
```

VARCHAR 저장소 옵션 값의 속성은 테이블 m$sys_table_property에 표시됩니다.
```sql
SELECT * FROM m$sys_table_property WHERE id={table_id} AND name = 'VARCHAR_FIXED_LENGTH_MAX';
```
