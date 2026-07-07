---
type: docs
title: 'LOOKUP non-PK UPDATE 미지원'
weight: 50
---

LOOKUP 테이블의 일반 조건식(non-PK 컬럼 기준) UPDATE는 현재 빌드에서 지원되지 않습니다.
PRIMARY KEY equality 조건만 사용할 수 있습니다.

## 현재 지원 범위

현재 LOOKUP 테이블의 UPDATE는 PRIMARY KEY equality 조건만 허용합니다. Primary key가 아닌 컬럼 조건을 사용하면 `Invalid UPDATE/DELETE condition` 오류가 발생합니다.

```sql
-- 현재 권장: PK 기준 UPDATE
UPDATE alarm_threshold SET high_limit = 90.0
WHERE sensor_id = 'TEMP-01';  -- sensor_id = PK
```

## 지원하지 않는 조건식

다음 구문은 현재 실행할 수 없습니다.

```sql
UPDATE alarm_threshold SET high_limit = 85.0
WHERE device_type = 'MOTOR';  -- device_type = non-PK 컬럼
-- [ERR-02190: Invalid UPDATE/DELETE condition. Specify it as (primary key column) = (value)]

UPDATE device_config SET active = 0
WHERE last_seen < NOW - 2592000000000000;
-- [ERR-02190: Invalid UPDATE/DELETE condition. Specify it as (primary key column) = (value)]
```

## 현재 대안

현재 PK가 아닌 조건으로 여러 행을 UPDATE해야 하는 경우:

1. **애플리케이션 레이어에서 PK 목록 조회 후 개별 UPDATE**:
```sql
-- 1단계: 해당 PK 목록 조회
SELECT sensor_id FROM alarm_threshold WHERE device_type = 'MOTOR';

-- 2단계: 각 PK에 대해 UPDATE 실행 (애플리케이션 루프)
UPDATE alarm_threshold SET high_limit = 85.0 WHERE sensor_id = 'TEMP-01';
UPDATE alarm_threshold SET high_limit = 85.0 WHERE sensor_id = 'TEMP-02';
...
```

2. **RDB 테이블 활용**: non-PK 조건 UPDATE/DELETE가 핵심이면 LOOKUP 대신 RDB 테이블 고려

> LOOKUP 테이블의 JSON 타입 컬럼도 현재 빌드에서 지원되지 않습니다.
