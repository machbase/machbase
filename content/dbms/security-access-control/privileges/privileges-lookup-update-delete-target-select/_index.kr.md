---
type: docs
title: 'LOOKUP UPDATE/DELETE 내부 target select 권한 모델 (planned: dbms-nfx#3696)'
weight: 50
---

> **참고**: 이 섹션은 계획 중인 기능(planned: dbms-nfx#3696)에 대한 설명입니다. 현재 버전의 동작과 향후 변경 예정 사항을 구분하여 기술합니다.

## 현재 동작: 기본키 기반 DELETE / UPDATE

현재 Machbase에서 LOOKUP 테이블의 `DELETE`와 `UPDATE`는 기본키(Primary Key) 기반 `WHERE` 조건만 지원합니다.

기본키 기반 조건에서는 내부적으로 SELECT가 발생하지 않으므로, `DELETE` / `UPDATE` 권한만 있으면 충분합니다.

```sql
-- PK 기반 DELETE: SELECT 권한 불필요
DELETE FROM device_config WHERE device_id = 'DEVICE-001';

-- PK 기반 UPDATE: SELECT 권한 불필요
UPDATE device_config SET config_value = 'new_value' WHERE device_id = 'DEVICE-001';
```

위 구문을 실행하려면 해당 테이블에 대한 `DELETE` 또는 `UPDATE` 권한이 있으면 됩니다.

```sql
GRANT DELETE ON sys.device_config TO ops_user;
GRANT UPDATE ON sys.device_config TO ops_user;
```

## 계획 중: non-PK 조건 UPDATE / DELETE

향후 기능 계획(dbms-nfx#3696)으로 LOOKUP 테이블에서 non-PK 조건 기반의 `UPDATE`와 `DELETE` 지원이 검토되고 있습니다.

non-PK 조건을 사용하는 경우, 내부적으로 조건에 맞는 행을 먼저 SELECT하는 과정이 필요합니다.

```sql
-- 계획 중인 기능: non-PK 조건 DELETE (현재 미지원)
DELETE FROM device_config WHERE region = 'ASIA';

-- 계획 중인 기능: non-PK 조건 UPDATE (현재 미지원)
UPDATE device_config SET status = 'inactive' WHERE last_seen < '2025-01-01';
```

## 계획 중인 권한 모델

non-PK 조건 구현 시 내부 SELECT 처리에 대한 권한 모델을 함께 정의할 예정입니다.

현재 검토 중인 방안:

| 방안 | 설명 |
|---|---|
| A | non-PK DELETE/UPDATE 실행 시 `SELECT` 권한도 함께 필요 |
| B | 내부 SELECT는 권한 체크 없이 처리 (DELETE/UPDATE 권한만 필요) |

최종 구현 방식은 dbms-nfx#3696 이슈에서 결정됩니다.

## 현재 버전에서의 권한 설정

현재 버전(Machbase 8.6)에서는 LOOKUP 테이블 `DELETE`/`UPDATE` 시 기본키 조건만 지원합니다.  
따라서 현재는 `DELETE` 또는 `UPDATE` 권한만 부여하면 됩니다.

```sql
-- 현재 필요한 권한 설정
GRANT DELETE ON sys.device_config TO ops_user;
GRANT UPDATE ON sys.device_config TO ops_user;

-- non-PK 조건 구현 후 SELECT도 추가 필요할 수 있음 (추후 결정)
-- GRANT SELECT ON sys.device_config TO ops_user;
```

향후 non-PK 조건 기능이 추가될 때 이 섹션의 내용과 권한 부여 지침이 업데이트됩니다.
