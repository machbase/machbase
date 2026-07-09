---
type: docs
title: '4.3.8 JOIN·메타데이터 설계'
weight: 80
---

여러 테이블 타입을 조합하는 JOIN 설계와 TAG 테이블 METADATA 활용 패턴입니다.

## 크로스 타입 JOIN 패턴

Machbase는 서로 다른 타입의 테이블을 JOIN할 수 있습니다.

```sql
-- TAG(계측) + LOOKUP(기준) + RDB(이력) 3-way JOIN
SELECT
    t.name AS sensor_id,
    m.location,
    m.unit,
    t.time,
    t.value,
    a.alarm_time,
    a.message
FROM sensor_data t
JOIN sensor_master m ON t.name = m.sensor_id
LEFT JOIN alarm_history a ON t.name = a.sensor
    AND a.alarm_time BETWEEN t.time - 60000000000 AND t.time
WHERE t.time >= NOW - 3600000000000
  AND m.dept = 'Production';
```

## METADATA JOIN 패턴

TAG 테이블의 METADATA를 이용하면 별도 JOIN 없이 태그 속성을 함께 조회할 수 있습니다.

```sql
-- METADATA와 계측값 동시 조회
SELECT name, location, unit, time, value
FROM sensor_data
WHERE time >= NOW - 3600000000000
  AND location = 'Building-A';  -- METADATA 컬럼 조건
```

## 서브쿼리 패턴

```sql
-- 임계값을 초과한 센서의 최근 이력 조회
SELECT s.name, s.time, s.value
FROM sensor_data s
WHERE s.name IN (
    SELECT sensor_name FROM alarm_threshold WHERE high_limit < 80.0
)
AND s.time >= NOW - 3600000000000
ORDER BY s.value DESC;
```

## JOIN 성능 최적화

1. 작은 테이블(LOOKUP)을 드라이빙 테이블 쪽으로 배치합니다.
2. JOIN 조건 컬럼에 인덱스를 생성합니다.
3. WHERE 절로 레코드를 최대한 줄인 후 JOIN합니다.

```sql
-- 성능 좋은 패턴: 범위 필터 후 JOIN
SELECT s.name, e.equip_name, s.time, s.value
FROM (
    SELECT name, time, value
    FROM sensor_data
    WHERE time >= NOW - 3600000000000  -- 먼저 범위 필터
      AND value > 80.0
) s
JOIN equipment_master e ON s.name = e.sensor_id;
```
