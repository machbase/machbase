---
type: docs
title: 'VIEW 생성과 관리'
weight: 80
---

VIEW는 하나 이상의 테이블에 대한 SELECT 쿼리를 저장해 두고, 이를 마치 테이블처럼 조회할 수 있게 하는 논리적 객체입니다.

## VIEW 생성

```sql
CREATE VIEW view_name AS
    SELECT ...;
```

### 예시

```sql
-- 최근 1시간 이상 알람 상태인 센서 뷰
CREATE VIEW active_alarms AS
    SELECT sensor_id, value, status
    FROM device_status
    WHERE status = 'ALARM';

-- TAG 테이블과 LOOKUP 테이블 조인 뷰
CREATE VIEW enriched_sensor_data AS
    SELECT t.name, t.time, t.value, m.location, m.dept
    FROM tag t
    LEFT JOIN device_meta m ON t.name = m.sensor_id;

-- 집계 뷰
CREATE VIEW hourly_avg AS
    SELECT name,
           DATE_TRUNC('hour', time) AS hour,
           AVG(value) AS avg_value
    FROM tag
    GROUP BY name, DATE_TRUNC('hour', time);
```

## VIEW 조회

VIEW는 일반 테이블처럼 SELECT 문에서 사용합니다.

```sql
SELECT * FROM active_alarms WHERE sensor_id = 'TEMP-01';

SELECT location, AVG(avg_value)
FROM hourly_avg
WHERE hour > DATEADD('h', -24, NOW)
GROUP BY location;
```

## VIEW 삭제

```sql
DROP VIEW active_alarms;
DROP VIEW enriched_sensor_data;
```

## VIEW 목록 조회

```sql
SELECT * FROM M$SYS_VIEWS;
```

## VIEW 정의 확인

```sql
SELECT VIEW_NAME, VIEW_TEXT
FROM M$SYS_VIEWS
WHERE VIEW_NAME = 'ACTIVE_ALARMS';
```

## VIEW 특성과 제한

- VIEW는 데이터를 물리적으로 저장하지 않습니다. 조회 시마다 정의된 쿼리를 실행합니다.
- VIEW에 대해 INSERT/UPDATE/DELETE는 지원하지 않습니다. 읽기 전용입니다.
- VIEW는 다른 VIEW를 참조할 수 있습니다 (중첩 VIEW).
- TAG, LOG, RDB, VOLATILE, LOOKUP 테이블 모두 VIEW 정의에 포함할 수 있습니다.

## 활용 패턴

```sql
-- 보안: 일부 컬럼만 노출하는 뷰
CREATE VIEW sensor_public AS
    SELECT sensor_id, time, value FROM sensor_log;
    -- value_raw, internal_code 등은 노출 안 함

-- 복잡한 JOIN을 단순화하는 뷰
CREATE VIEW asset_status AS
    SELECT a.asset_id, a.name, s.status, s.last_seen
    FROM assets a
    LEFT JOIN device_status s ON a.device_id = s.device_id;

-- 쿼리 재사용: 자주 쓰는 필터를 뷰로 저장
CREATE VIEW critical_sensors AS
    SELECT * FROM alarm_threshold WHERE high_limit < 50.0;
```
