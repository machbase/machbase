---
title: '9.15 LOOKUP 권한과 DML 성능'
weight: 150
toc: true
---

LOOKUP 테이블의 권한 모델과 일반 조건식 기반 UPDATE/DELETE의 운영 기준을 다룹니다.

<a id="privileges-lookup-update-delete-target-select"></a>

## LOOKUP UPDATE/DELETE 권한

| 작업 | 필요한 권한 |
|------|-------------|
| SELECT | `SELECT` |
| UPDATE | `UPDATE` |
| DELETE | `DELETE` |

UPDATE와 DELETE는 Primary key 조건과 일반 조건식을 모두 사용할 수 있습니다. 실행에는 해당
DML 권한만 필요하며, 내부 대상 행 조회를 위해 별도의 `SELECT` 권한을 요구하지 않습니다.
애플리케이션이 변경 전후 값을 직접 조회해야 할 때만 `SELECT` 권한을 부여합니다.

```sql
GRANT SELECT ON sys.device_config TO ops_user;
GRANT UPDATE ON sys.device_config TO ops_user;
GRANT DELETE ON sys.device_config TO ops_user;

UPDATE device_config
SET status = 'INACTIVE'
WHERE device_id = 'DEV-001';

DELETE FROM device_config
WHERE device_id = 'DEV-001';
```

<a id="performance-considerations-lookup-predicate-dml"></a>

## DML 성능 고려사항

Primary key equality 조건은 fast path로 대상을 식별합니다. 일반 조건식은 조건을 평가해 대상
Primary key 집합을 수집한 뒤 행을 변경하는 경로를 사용합니다. 반복적인 단건 변경은 prepared
statement와 bind 변수를 사용하고, 일괄 변경 전에는 같은 조건으로 대상 범위를 확인합니다.

```sql
UPDATE device_meta
SET status = ?
WHERE device_id = ?;
```

여러 행을 일괄 변경할 때는 일반 조건식을 사용할 수 있습니다. 전체 교체가 적합한 기준 정보라면
조건 없는 DELETE 후 다시 입력합니다. LOOKUP 테이블은 TRUNCATE를 지원하지 않습니다.

```sql
DELETE FROM device_meta;
```

JSON path 조건으로 대상을 선택하고 JSON 컬럼을 변경할 수도 있습니다.

```sql
UPDATE device_meta
SET meta = JSON_SET(meta, '$.state', 'active')
WHERE meta->'$.region' = 'kr';
```
