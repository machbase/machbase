---
type: docs
title: 'LOOKUP UPDATE/DELETE 권한'
weight: 50
---

## 기본키 기반 DELETE / UPDATE

현재 Machbase에서 LOOKUP 테이블의 `DELETE`와 `UPDATE`는 기본키(Primary Key) 기반 `WHERE` 조건만 지원합니다.

기본키 기반 조건에서는 해당 테이블에 대한 `DELETE` 또는 `UPDATE` 권한이 필요합니다.

```sql
-- PK 기반 DELETE: SELECT 권한 불필요
DELETE FROM device_config WHERE device_id = 'DEVICE-001';

-- PK 기반 UPDATE: SELECT 권한 불필요
UPDATE device_config SET config_value = 'new_value' WHERE device_id = 'DEVICE-001';
```

```sql
GRANT DELETE ON sys.device_config TO ops_user;
GRANT UPDATE ON sys.device_config TO ops_user;
```

## non-PK 조건은 지원되지 않음

```sql
-- 오류: non-PK 조건 DELETE
DELETE FROM device_config WHERE region = 'ASIA';

-- 오류: non-PK 조건 UPDATE
UPDATE device_config SET status = 'inactive' WHERE last_seen < '2025-01-01';
```

비-PK 조건을 사용하면 권한 검사 단계 이전 또는 실행 단계에서 다음 오류가 발생합니다.

```
[ERR-02190: Invalid UPDATE/DELETE condition. Specify it as (primary key column) = (value)]
```

## 권한 설정 예

```sql
-- DELETE만 허용
GRANT DELETE ON sys.device_config TO ops_user;

-- UPDATE만 허용
GRANT UPDATE ON sys.device_config TO ops_user;

-- UPDATE/DELETE 대상 확인용 조회도 허용해야 한다면 별도로 SELECT 부여
GRANT SELECT ON sys.device_config TO ops_user;
```
