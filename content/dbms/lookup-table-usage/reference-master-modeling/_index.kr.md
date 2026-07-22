---
title: '9.14 참조·마스터 데이터 모델링'
weight: 140
toc: true
---
LOOKUP 테이블을 활용한 참조·마스터 데이터 모델링 패턴을 다룹니다.


<a id="patterns-reference-design"></a>

## 참조 설계 패턴

LOOKUP 테이블을 다른 테이블과 연계해 참조 데이터를 제공하는 패턴입니다.

### 기준 코드 참조 패턴

```sql
-- 기준 코드 테이블 (LOOKUP)
CREATE LOOKUP TABLE status_code (
    code    VARCHAR(8)  PRIMARY KEY,
    label   VARCHAR(64),
    color   VARCHAR(16)
);

-- 이벤트 테이블 (LOG)
CREATE LOG TABLE event_log (
    event_time DATETIME,
    device_id  VARCHAR(32),
    status     VARCHAR(8)  -- status_code.code 참조
);

-- JOIN 조회
SELECT e.event_time, e.device_id, s.label AS status_label, s.color
FROM event_log e
JOIN status_code s ON e.status = s.code
WHERE e.event_time >= NOW - 3600000000000;
```

### 센서 메타데이터 참조 패턴

```sql
-- 센서 마스터 (LOOKUP)
CREATE LOOKUP TABLE sensor_master (
    sensor_id  VARCHAR(64) PRIMARY KEY,
    location   VARCHAR(128),
    unit       VARCHAR(16),
    dept       VARCHAR(64)
);

-- 센서 계측 (TAG)
CREATE TAG TABLE sensor_data (
    name   VARCHAR(64) PRIMARY KEY,
    time   DATETIME    BASETIME,
    value  DOUBLE
);

-- 위치별 센서 현황 조회
SELECT sd.name, sm.location, sd.time, sd.value, sm.unit
FROM sensor_data sd
JOIN sensor_master sm ON sd.name = sm.sensor_id
WHERE sm.dept = 'Production'
  AND sd.time >= NOW - 3600000000000;
```

### 임계값 참조 패턴

```sql
-- 임계값 설정 (LOOKUP, 실시간 변경 가능)
CREATE LOOKUP TABLE alarm_threshold (
    sensor_id VARCHAR(64) PRIMARY KEY,
    low_val   DOUBLE,
    high_val  DOUBLE
);

-- 초과 센서 조회 (TAG + LOOKUP JOIN)
SELECT s.name, s.time, s.value, t.high_val
FROM sensor_data s
JOIN alarm_threshold t ON s.name = t.sensor_id
WHERE s.time >= NOW - 60000000000
  AND s.value > t.high_val;
```
