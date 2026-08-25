---
type: docs
title: '15.2 장비 마스터와 알람'
weight: 20
toc: true
---

LOOKUP 테이블에 장비 기준 정보와 임계값을 두고, TAG 최신값을 비교해 알람 상태를 계산합니다.
발생한 알람은 LOG 테이블에 이력으로 저장합니다.

## 1단계: 테이블 생성

```sql
CREATE LOOKUP TABLE sc16_equipment (
    eq_id      VARCHAR(32) PRIMARY KEY,
    eq_name    VARCHAR(64),
    location   VARCHAR(64),
    temp_limit DOUBLE,
    status     VARCHAR(16),
    install_at DATETIME
);

CREATE TAG TABLE sc16_equipment_temp (
    name  VARCHAR(32) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE SUMMARIZED
);

CREATE LOG TABLE sc16_alarm_log (
    eq_id         VARCHAR(32),
    alarm_type    VARCHAR(32),
    measured_value DOUBLE
);
```

## 2단계: 기준 정보와 센서값 입력

```sql
INSERT INTO sc16_equipment VALUES
  ('PUMP_01', '1호 펌프', 'A동', 80.0, 'ACTIVE', TO_DATE('2022-03-15'));
INSERT INTO sc16_equipment VALUES
  ('MOTOR_01', '1호 모터', 'B동', 90.0, 'ACTIVE', TO_DATE('2021-07-20'));

INSERT INTO sc16_equipment_temp METADATA VALUES ('PUMP_01');
INSERT INTO sc16_equipment_temp METADATA VALUES ('MOTOR_01');
INSERT INTO sc16_equipment_temp VALUES ('PUMP_01', SYSDATE, 83.7);
INSERT INTO sc16_equipment_temp VALUES ('MOTOR_01', SYSDATE, 68.0);

EXEC TABLE_FLUSH(sc16_equipment_temp);
```

## 3단계: 최신 상태와 알람 대상 조회

```sql
WITH latest AS (
    SELECT t.name, t.time, t.value
      FROM sc16_equipment_temp t
      JOIN v$sc16_equipment_temp_stat s
        ON t.name = s.name
       AND t.time = s.recent_row_time
)
SELECT e.eq_id, e.eq_name, e.location,
       l.time AS measured_at, l.value, e.temp_limit,
       CASE WHEN l.value > e.temp_limit THEN 'ALARM' ELSE 'NORMAL' END AS state
  FROM sc16_equipment e
  JOIN latest l
    ON e.eq_id = l.name
 WHERE e.status = 'ACTIVE'
 ORDER BY e.eq_id;
```

알람 판정 결과를 애플리케이션이 확인한 뒤 이력 테이블에 기록합니다.

```sql
INSERT INTO sc16_alarm_log VALUES ('PUMP_01', 'TEMP_HIGH', 83.7);

SELECT _arrival_time, eq_id, alarm_type, measured_value
  FROM sc16_alarm_log
 ORDER BY _arrival_time DESC;
```

문자열 결합 함수나 현재 시각에서 interval을 빼는 비표준 표현에 의존하지 않고, 장비 ID를
TAG 이름과 직접 맞췄습니다. 더 복잡한 이름 규칙이 필요하면 적재 단계에서 정규화한 키를
별도 열로 관리하십시오.

## 4단계: 정리

```sql
DROP TABLE sc16_alarm_log;
DROP TABLE sc16_equipment_temp;
DROP TABLE sc16_equipment;
```
