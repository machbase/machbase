---
title: '9.14 LOOKUP 권한과 DML 성능'
weight: 140
toc: true
---

LOOKUP 테이블의 권한 모델과 Primary key 기반 UPDATE/DELETE의 운영 기준을 다룹니다.

<a id="privileges-lookup-update-delete-target-select"></a>

## LOOKUP UPDATE/DELETE 권한

| 작업 | 필요한 권한 |
|------|-------------|
| SELECT | `SELECT` |
| UPDATE | `UPDATE` |
| DELETE | `DELETE` |

UPDATE와 조건이 있는 DELETE는 Primary key equality 조건을 사용합니다. DML 실행 자체에는 해당
DML 권한이 필요하고, 애플리케이션이 변경 전후 값을 조회하려면 `SELECT` 권한도 부여합니다.

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

Primary key equality 조건은 Primary key 인덱스로 대상을 식별합니다. 반복적인 단건 변경은
prepared statement와 bind 변수를 사용하고, 변경 빈도와 인덱스 메모리 사용량을 함께
모니터링합니다.

```sql
UPDATE device_meta
SET status = ?
WHERE device_id = ?;
```

여러 행을 일괄 변경해야 하면 대상 Primary key를 조회한 뒤 키별 DML을 실행하거나, 전체 교체가
적합한 기준 정보라면 조건 없는 DELETE 후 다시 입력합니다. LOOKUP 테이블은 TRUNCATE를 지원하지
않습니다.

```sql
DELETE FROM device_meta;
```

JSON 컬럼을 변경할 때도 WHERE 절에는 Primary key equality 조건을 사용합니다.

```sql
UPDATE device_meta
SET meta = JSON_SET(meta, '$.state', 'active')
WHERE device_id = 'DEV-001';
```
