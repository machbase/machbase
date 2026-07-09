---
title: '9.13 일반 predicate UPDATE/DELETE'
weight: 130
toc: true
---
일반 predicate UPDATE/DELETE에 해당하는 세부 문서를 모았습니다.


<a id="condition-lookup-delete"></a>

## LOOKUP 일반 조건식 DELETE

LOOKUP 테이블은 primary key 조건뿐 아니라 일반 조건식으로 `DELETE`할 수 있습니다.
조건에 맞는 모든 row가 삭제됩니다.

### 예제

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

### 정책

- `WHERE` 절은 일반 컬럼, 범위, 문자열, 날짜, JSON path 조건을 사용할 수 있습니다.
- `WHERE` 절 없이 실행하면 LOOKUP 테이블의 모든 row가 삭제됩니다.
- 운영 데이터에서는 먼저 같은 조건으로 대상 범위를 확인합니다.

```sql
SELECT COUNT(*)
FROM alarm_threshold
WHERE active = 0;
```

<a id="condition-lookup-update"></a>

## LOOKUP 일반 조건식 UPDATE

LOOKUP 테이블은 primary key 조건뿐 아니라 일반 조건식으로 `UPDATE`할 수 있습니다.
조건에 맞는 모든 row가 갱신됩니다.

### 예제

```sql
UPDATE alarm_threshold
SET high_limit = high_limit + 5.0,
    updated_at = NOW
WHERE device_type = 'MOTOR'
  AND active = 1;
```

LOOKUP 테이블은 JSON 컬럼을 지원하지 않습니다. 유동 속성을 조건으로 자주 사용한다면 해당 값을
일반 컬럼으로 분리한 뒤 UPDATE 조건에 사용합니다.

### 정책

- `WHERE` 절은 일반 컬럼, 범위, 문자열, 날짜 조건을 사용할 수 있습니다.
- `SET` 절의 오른쪽 표현식은 현재 row 값을 참조할 수 있습니다.
- Primary key 컬럼 자체는 갱신할 수 없습니다.
- 대량 갱신 전에는 같은 조건으로 `SELECT COUNT(*)`를 실행해 영향 범위를 확인합니다.

<a id="design-condition-lookup-update-delete"></a>

## UPDATE·DELETE 조건 설계

LOOKUP 테이블은 primary key 조건과 일반 조건식 기반 `UPDATE`/`DELETE`를 지원합니다.

### UPDATE

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

### DELETE

```sql
DELETE FROM equipment_master
WHERE status = 'RETIRED'
   OR updated_at < TO_DATE('2026-01-01 00:00:00');
```

### 조건 설계 지침

1. **단건 변경은 PK 조건 사용**: 가장 명확하고 빠른 경로입니다.
2. **일괄 변경은 대상 범위 확인**: 일반 조건식은 조건에 맞는 모든 row에 적용됩니다.
3. **자주 쓰는 조건은 별도 컬럼화**: LOOKUP 테이블은 JSON 컬럼을 지원하지 않으므로 고빈도 조건은 일반 컬럼으로 분리합니다.
4. **PK 컬럼은 변경하지 않음**: primary key 컬럼은 `UPDATE SET` 대상이 될 수 없습니다.

```sql
SELECT COUNT(*)
FROM equipment_master
WHERE status = 'RETIRED';
```
