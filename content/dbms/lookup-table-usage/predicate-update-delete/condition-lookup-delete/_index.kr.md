---
type: docs
title: '9.13.1 LOOKUP 일반 조건식 DELETE'
weight: 10
---

LOOKUP 테이블은 primary key 조건뿐 아니라 일반 조건식으로 `DELETE`할 수 있습니다.
조건에 맞는 모든 row가 삭제됩니다.

## 예제

```sql
DELETE FROM alarm_threshold
WHERE active = 0
   OR updated_at < TO_DATE('2026-01-01 00:00:00');
```

JSON 컬럼 조건도 사용할 수 있습니다.

```sql
DELETE FROM device_config
WHERE config->'$.region' = 'kr'
  AND JSON_EXTRACT_INTEGER(config, '$.level') < 2;
```

## 정책

- `WHERE` 절은 일반 컬럼, 범위, 문자열, 날짜, JSON path 조건을 사용할 수 있습니다.
- `WHERE` 절 없이 실행하면 LOOKUP 테이블의 모든 row가 삭제됩니다.
- 운영 데이터에서는 먼저 같은 조건으로 대상 범위를 확인합니다.

```sql
SELECT COUNT(*)
FROM alarm_threshold
WHERE active = 0;
```
