---
type: docs
title: '9.15.2 LOOKUP 일반 predicate DML 성능 고려사항'
weight: 50
---

LOOKUP 테이블의 primary key 조건 `UPDATE`/`DELETE`는 PK 해시 경로를 사용합니다. 일반
predicate `UPDATE`/`DELETE`는 조건에 맞는 대상 row를 찾은 뒤 변경을 적용하므로, 범위가
넓으면 PK 단건 처리보다 비용이 커질 수 있습니다.

## 권장 패턴

### 1. 단건 변경은 PK 조건 사용

```sql
UPDATE device_meta
SET status = 'ACTIVE'
WHERE device_id = 'DEV-001';

DELETE FROM device_meta
WHERE device_id = 'DEV-001';
```

### 2. 일괄 변경 전 대상 범위 확인

```sql
SELECT COUNT(*)
FROM device_meta
WHERE location = 'Building-A'
  AND status = 'INACTIVE';

UPDATE device_meta
SET status = 'RETIRED'
WHERE location = 'Building-A'
  AND status = 'INACTIVE';
```

### 3. JSON 조건은 타입별 함수 사용

```sql
UPDATE device_meta
SET meta = JSON_SET(meta, '$.state', 'active')
WHERE meta->'$.region' = 'kr'
  AND JSON_EXTRACT_INTEGER(meta, '$.level') >= 3;
```

숫자 비교에는 `->`보다 `JSON_EXTRACT_INTEGER`, `JSON_EXTRACT_DOUBLE` 같은 타입별 함수를
사용합니다.

## 성능 요약

| DML 유형 | 특성 | 권장 사용 |
|----------|------|-----------|
| PK 조건 UPDATE/DELETE | PK 해시 경로 | 단건 또는 명확한 PK 대상 |
| non-PK predicate UPDATE/DELETE | 조건에 맞는 row를 찾아 적용 | 소규모/중간 규모 일괄 변경, 사전 count 권장 |
| JSON path 조건 DML | JSON path 평가 비용 포함 | 자주 쓰는 조건은 별도 컬럼화 |

LOOKUP 테이블은 참조 데이터 용도에 맞게 작고 명확한 범위로 유지하는 것이 좋습니다.
