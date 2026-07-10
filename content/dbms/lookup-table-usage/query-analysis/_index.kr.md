---
title: '9.5 조회와 분석'
weight: 50
toc: true
---
LOOKUP 테이블의 조회와 분석을 다룬다.


<a id="original-85-querying-data"></a>

## Lookup 데이터 조회

SQL 문을 사용하여 데이터를 조회한다. LOOKUP 테이블은 `PRIMARY KEY` 기반 조회, 일반 조건 조회, 다른 테이블과의 JOIN에 주로 사용한다.

<a id="query-lookup-primary-key"></a>

## PRIMARY KEY 조회

단건 조회는 `PRIMARY KEY` 조건을 사용한다.

```sql
SELECT equip_id, equip_name, location, status
FROM equipment_master
WHERE equip_id = 1001;
```

문자열 키를 사용하는 경우에도 같은 방식으로 조회한다.

```sql
SELECT sensor_id, site, unit, status
FROM sensor_master
WHERE sensor_id = 'TEMP-01';
```

<a id="query-lookup-condition"></a>

## 일반 조건 조회

LOOKUP 테이블은 일반 컬럼 조건으로도 조회할 수 있다. 자주 사용하는 조건 컬럼에는 인덱스를 추가한다.

```sql
SELECT equip_id, equip_name, location
FROM equipment_master
WHERE location = 'Line-1'
  AND status = 'ACTIVE';
```

범위 조건과 정렬도 사용할 수 있다.

```sql
SELECT seq, sensor_id, alarm_type, occurred_at
FROM alarm_history
WHERE seq > 1000
ORDER BY seq DESC
LIMIT 20;
```

<a id="query-lookup-join"></a>

## TAG·LOG 테이블과 JOIN

LOOKUP 테이블은 TAG 또는 LOG 테이블의 원본 데이터에 설명 정보를 붙이는 용도로 자주 사용한다.

```sql
SELECT d.name, m.site, m.unit, d.time, d.value
FROM sensor_data d
JOIN sensor_master m ON d.name = m.sensor_id
WHERE m.status = 'ACTIVE'
  AND d.time >= NOW - 3600000000000;
```

로그 이벤트의 코드값을 사람이 읽을 수 있는 라벨로 변환할 때도 사용한다.

```sql
SELECT e.event_time, e.device_id, c.label, e.message
FROM event_log e
JOIN status_code c ON e.status = c.code
WHERE e.event_time >= NOW - 86400000000000;
```

<a id="query-lookup-analysis-pattern"></a>

## 분석 패턴

LOOKUP 테이블은 원본 데이터를 저장하기보다 분석 기준을 제공한다. 다음과 같은 패턴에 적합하다.

| 패턴 | 설명 |
|------|------|
| 코드 변환 | 상태 코드, 알람 코드, 장비 타입을 라벨로 변환 |
| 기준값 비교 | 센서값을 임계값 테이블과 JOIN해 초과 여부 판단 |
| 그룹 기준 제공 | 위치, 부서, 라인 등 집계 기준 제공 |
| 최신 설정 반영 | 운영 중 변경되는 설정값을 조회 시점에 반영 |

임계값 비교 예시는 다음과 같다.

```sql
SELECT s.name, s.time, s.value, t.high_val
FROM sensor_data s
JOIN alarm_threshold t ON s.name = t.sensor_id
WHERE s.time >= NOW - 60000000000
  AND s.value > t.high_val;
```

<a id="query-lookup-performance"></a>

## 조회 성능 기준

- 단건 조회와 JOIN 기준 컬럼은 `PRIMARY KEY` 또는 인덱스 컬럼을 사용한다.
- 조건에 자주 쓰는 일반 컬럼은 별도 인덱스를 검토한다.
- 대량 원본 데이터와 JOIN할 때는 원본 테이블의 시간 범위를 먼저 좁힌다.
- LOOKUP 테이블에는 기준 정보를 저장하고, 장기 원본 데이터는 TAG 또는 LOG 테이블에 저장한다.
