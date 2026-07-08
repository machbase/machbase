---
type: docs
title: 'LOOKUP 일반 조건식 UPDATE'
weight: 50
---

LOOKUP 테이블은 primary key 조건뿐 아니라 일반 조건식으로 `UPDATE`할 수 있습니다.
조건에 맞는 모든 row가 갱신됩니다.

## 예제

```sql
UPDATE alarm_threshold
SET high_limit = high_limit + 5.0,
    updated_at = NOW
WHERE device_type = 'MOTOR'
  AND active = 1;
```

JSON 컬럼도 조건과 갱신 대상에 사용할 수 있습니다.

```sql
UPDATE device_config
SET config = JSON_SET(config, '$.status', 'active')
WHERE site = 'SEOUL'
  AND JSON_EXTRACT_INTEGER(config, '$.level') >= 3;
```

## 정책

- `WHERE` 절은 일반 컬럼, 범위, 문자열, 날짜, JSON path 조건을 사용할 수 있습니다.
- `SET` 절의 오른쪽 표현식은 현재 row 값을 참조할 수 있습니다.
- Primary key 컬럼 자체는 갱신할 수 없습니다.
- 대량 갱신 전에는 같은 조건으로 `SELECT COUNT(*)`를 실행해 영향 범위를 확인합니다.
