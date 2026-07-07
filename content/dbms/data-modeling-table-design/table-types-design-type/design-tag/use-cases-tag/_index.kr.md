---
type: docs
title: '활용 사례'
weight: 30
---

TAG 테이블이 적합한 대표적인 활용 사례를 소개합니다.

## IoT 센서 데이터

공장, 빌딩, 인프라에 설치된 다양한 센서 데이터를 단일 TAG 테이블에서 관리합니다.

```sql
CREATE TAG TABLE factory_sensor (
    name        VARCHAR(128) PRIMARY KEY,
    time        DATETIME     BASETIME,
    temperature DOUBLE,
    vibration   DOUBLE,
    current     DOUBLE
);

-- 센서 이름 규칙: {공장ID}/{라인}/{장비ID}/{측정항목}
-- 예: 'F01/LINE-A/MOTOR-01/TEMP'
INSERT INTO factory_sensor VALUES (
    'F01/LINE-A/MOTOR-01/TEMP',
    NOW,
    75.3, NULL, NULL
);
```

## 에너지 모니터링

전력, 가스, 수도 계량기 데이터를 시간별로 수집합니다.

```sql
CREATE TAG TABLE energy_meter (
    meter_id  VARCHAR(64) PRIMARY KEY,
    time      DATETIME    BASETIME,
    kwh       DOUBLE,
    voltage   DOUBLE,
    current   DOUBLE
);
```

## 차량·이동체 추적

GPS 좌표와 속도를 시계열로 기록합니다.

```sql
CREATE TAG TABLE vehicle_track (
    vehicle_id VARCHAR(32) PRIMARY KEY,
    time       DATETIME    BASETIME,
    lat        DOUBLE,
    lon        DOUBLE,
    speed      DOUBLE,
    heading    DOUBLE
);
```

## 부적합한 경우

- 태그 이름이 매 레코드마다 달라지는 경우 (태그 수 폭발)
- 기존 시계열 값을 직접 UPDATE해야 하는 경우 (TAG 테이블은 실제 데이터 UPDATE 불가)
- 단순 이벤트 로그 (LOG 테이블 권장)
