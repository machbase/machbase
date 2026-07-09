---
type: docs
title: 'LOOKUP 일반 predicate UPDATE/DELETE 범위가 클 때'
weight: 30
---

LOOKUP 테이블의 일반 predicate `UPDATE`/`DELETE`는 지원됩니다. 다만 조건에 맞는 모든
row에 적용되므로, 의도보다 많은 row가 변경되거나 삭제되지 않도록 대상 범위를 확인해야 합니다.

## 증상

- UPDATE/DELETE가 성공했지만 예상보다 많은 row가 변경됨
- JSON path 또는 범위 조건이 넓어 다수 row가 대상이 됨

## 진단

실행 전 같은 조건으로 대상 row 수를 확인합니다.

```sql
SELECT COUNT(*)
FROM equipment
WHERE location = 'A동'
  AND status = 'inactive';
```

필요하면 대상 key를 함께 확인합니다.

```sql
SELECT eq_id, location, status
FROM equipment
WHERE location = 'A동'
  AND status = 'inactive';
```

## 해결 방법

- 단건 변경은 primary key 조건을 사용합니다.
- 일괄 변경은 조건을 더 좁히고, 변경 전후 count를 확인합니다.
- JSON 숫자 조건은 타입별 함수를 사용합니다.

```sql
UPDATE equipment
SET status = 'retired'
WHERE location = 'A동'
  AND status = 'inactive'
  AND JSON_EXTRACT_INTEGER(meta, '$.level') < 2;
```
