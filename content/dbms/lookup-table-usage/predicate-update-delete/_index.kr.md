---
title: '9.13 일반 predicate UPDATE/DELETE'
weight: 130
toc: true
---
LOOKUP 테이블의 일반 조건식 기반 UPDATE/DELETE를 다룬다.


<a id="condition-lookup-delete"></a>

## LOOKUP 일반 조건식 DELETE

LOOKUP 테이블은 primary key 조건뿐 아니라 일반 조건식으로도 `DELETE`할 수 있다.
조건에 맞는 모든 row가 삭제된다.

## 예제

```sql
DELETE FROM alarm_threshold
WHERE active = 0
   OR updated_at < TO_DATE('2026-01-01 00:00:00');
```

JSON 컬럼 조건도 사용할 수 있다.

```sql
DELETE FROM device_config
WHERE config->'$.region' = 'kr'
  AND JSON_EXTRACT_INTEGER(config, '$.level') < 2;
```

## 정책

- `WHERE` 절은 일반 컬럼, 범위, 문자열, 날짜, JSON path 조건을 사용할 수 있다.
- `WHERE` 절 없이 실행하면 LOOKUP 테이블의 모든 row가 삭제된다.
- 운영 데이터에서는 먼저 같은 조건으로 대상 범위를 확인한다.

```sql
SELECT COUNT(*)
FROM alarm_threshold
WHERE active = 0;
```

<a id="condition-lookup-update"></a>

## LOOKUP 일반 조건식 UPDATE

LOOKUP 테이블은 primary key 조건뿐 아니라 일반 조건식으로도 `UPDATE`할 수 있다.
조건에 맞는 모든 row가 갱신된다.

## 예제

```sql
UPDATE alarm_threshold
SET high_limit = high_limit + 5.0,
    updated_at = NOW
WHERE device_type = 'MOTOR'
  AND active = 1;
```

LOOKUP 테이블은 JSON 컬럼을 일반 컬럼으로 지원한다. JSON path 조건을 UPDATE 대상 선정에
사용할 수 있지만, JSON path별 전용 인덱스는 지원하지 않으므로 고빈도 조건은 일반 컬럼으로
분리한다.

## 정책

- `WHERE` 절은 일반 컬럼, 범위, 문자열, 날짜 조건을 사용할 수 있다.
- `SET` 절의 오른쪽 표현식은 현재 row 값을 참조할 수 있다.
- Primary key 컬럼 자체는 갱신할 수 없다.
- 대량 갱신 전에는 같은 조건으로 `SELECT COUNT(*)`를 실행해 영향 범위를 확인한다.

<a id="design-condition-lookup-update-delete"></a>

## UPDATE·DELETE 조건 설계

LOOKUP 테이블은 primary key 조건과 일반 조건식 기반 `UPDATE`/`DELETE`를 지원한다.

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

LOOKUP 테이블은 JSON 컬럼을 일반 컬럼으로 지원한다. JSON path 조건을 자주 사용하면
해당 값을 일반 컬럼으로 분리해 인덱스와 함께 사용하는 설계를 우선 검토한다.

## DELETE

```sql
DELETE FROM equipment_master
WHERE status = 'RETIRED'
   OR updated_at < TO_DATE('2026-01-01 00:00:00');
```

## 조건 설계 지침

1. **단건 변경은 PK 조건 사용**: 가장 명확하고 빠른 경로이다.
2. **일괄 변경은 대상 범위 확인**: 일반 조건식은 조건에 맞는 모든 row에 적용된다.
3. **자주 쓰는 조건은 별도 컬럼화**: JSON path별 전용 인덱스는 지원하지 않으므로 고빈도 조건은 일반 컬럼으로 분리한다.
4. **PK 컬럼은 변경하지 않음**: primary key 컬럼은 `UPDATE SET` 대상이 될 수 없다.

```sql
SELECT COUNT(*)
FROM equipment_master
WHERE status = 'RETIRED';
```
