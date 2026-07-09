---
type: docs
title: 'LOOKUP UPDATE/DELETE 권한'
weight: 50
---

LOOKUP 테이블의 `UPDATE`와 `DELETE`는 primary key 조건과 일반 predicate 조건을 모두
지원합니다. 권한 검사는 사용자가 실행한 DML 권한을 기준으로 수행합니다.

## 권한 기준

| 작업 | 필요한 권한 |
|------|-------------|
| SELECT | `SELECT` |
| UPDATE | `UPDATE` |
| DELETE | `DELETE` |

일반 predicate `UPDATE`/`DELETE` 실행 중 내부적으로 대상 row를 찾더라도, 사용자에게 별도
`SELECT` 권한을 추가로 요구하지 않습니다.

```sql
-- UPDATE 권한이 있으면 일반 predicate UPDATE 가능
UPDATE device_config
SET status = 'inactive'
WHERE region = 'ASIA';

-- DELETE 권한이 있으면 일반 predicate DELETE 가능
DELETE FROM device_config
WHERE last_seen < TO_DATE('2026-01-01 00:00:00');
```

## 권한 설정 예

```sql
GRANT UPDATE ON sys.device_config TO ops_user;
GRANT DELETE ON sys.device_config TO ops_user;
```

대상 범위를 사용자가 직접 확인하도록 하려면 `SELECT` 권한을 별도로 부여합니다.

```sql
GRANT SELECT ON sys.device_config TO ops_user;
```
