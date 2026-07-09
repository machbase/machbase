---
type: docs
title: '9.13.3 UPDATE·DELETE 조건 설계'
weight: 80
---

LOOKUP 테이블은 primary key 조건과 일반 조건식 기반 `UPDATE`/`DELETE`를 지원합니다.

## UPDATE

```sql
UPDATE equipment_master
SET location = 'Line-3',
    status = 'ACTIVE',
    score = score + 10,
    updated_at = NOW
WHERE site = 'SEOUL'
  AND status = 'READY';
```

LOOKUP 테이블은 JSON 컬럼을 지원하지 않습니다. 유동 속성을 조건으로 자주 사용한다면 해당 값을
일반 컬럼으로 분리한 뒤 UPDATE 조건에 사용합니다.

## DELETE

```sql
DELETE FROM equipment_master
WHERE status = 'RETIRED'
   OR updated_at < TO_DATE('2026-01-01 00:00:00');
```

## 조건 설계 지침

1. **단건 변경은 PK 조건 사용**: 가장 명확하고 빠른 경로입니다.
2. **일괄 변경은 대상 범위 확인**: 일반 조건식은 조건에 맞는 모든 row에 적용됩니다.
3. **자주 쓰는 조건은 별도 컬럼화**: LOOKUP 테이블은 JSON 컬럼을 지원하지 않으므로 고빈도 조건은 일반 컬럼으로 분리합니다.
4. **PK 컬럼은 변경하지 않음**: primary key 컬럼은 `UPDATE SET` 대상이 될 수 없습니다.

```sql
SELECT COUNT(*)
FROM equipment_master
WHERE status = 'RETIRED';
```
