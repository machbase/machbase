---
type: docs
title: '15.1 실시간 장비 상태와 알람'
weight: 10
toc: true
aliases:
  - /dbms/scenario-guides/state-status-real-time-dashboard/
---

LOOKUP 테이블에 장비 기준 정보와 임계값을 두고, TAG 최신값을 비교해 알람 상태를 계산합니다.
발생한 알람은 LOG 테이블에 이력으로 저장합니다.

## 1단계: 테이블 생성

<a id="사전-준비"></a>

```sql
CREATE LOOKUP TABLE sc15_equipment (
    eq_id      VARCHAR(32) PRIMARY KEY,
    eq_name    VARCHAR(64),
    location   VARCHAR(64),
    temp_limit DOUBLE,
    status     VARCHAR(16),
    install_at DATETIME
);

CREATE TAG TABLE sc15_equipment_temp (
    name  VARCHAR(32) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE SUMMARIZED
);

CREATE LOG TABLE sc15_alarm_log (
    eq_id         VARCHAR(32),
    alarm_type    VARCHAR(32),
    measured_value DOUBLE
);
```

## 2단계: 기준 정보와 센서값 입력

```sql
INSERT INTO sc15_equipment VALUES
  ('PUMP_01', '1호 펌프', 'A동', 80.0, 'ACTIVE', TO_DATE('2022-03-15'));
INSERT INTO sc15_equipment VALUES
  ('MOTOR_01', '1호 모터', 'B동', 90.0, 'ACTIVE', TO_DATE('2021-07-20'));

INSERT INTO sc15_equipment_temp METADATA VALUES ('PUMP_01');
INSERT INTO sc15_equipment_temp METADATA VALUES ('MOTOR_01');
INSERT INTO sc15_equipment_temp VALUES ('PUMP_01', SYSDATE, 83.7);
INSERT INTO sc15_equipment_temp VALUES ('MOTOR_01', SYSDATE, 68.0);

EXEC TABLE_FLUSH(sc15_equipment_temp);
```

한 장비만 확인할 때는 역방향 스캔과 `LIMIT 1`을 사용할 수 있습니다.

```sql
SELECT /*+ SCAN_BACKWARD(sc15_equipment_temp) */
       name, time, value
  FROM sc15_equipment_temp
 WHERE name = 'PUMP_01'
 LIMIT 1;
```

## 3단계: 최신 상태와 알람 대상 조회

<a id="1단계-최신-센서값-조회"></a>
<a id="2단계-상태-판정"></a>

```sql
WITH latest AS (
    SELECT t.name, t.time, t.value
      FROM sc15_equipment_temp t
      JOIN v$sc15_equipment_temp_stat s
        ON t.name = s.name
       AND t.time = s.recent_row_time
)
SELECT e.eq_id, e.eq_name, e.location,
       l.time AS measured_at, l.value, e.temp_limit,
       CASE WHEN l.value > e.temp_limit THEN 'ALARM' ELSE 'NORMAL' END AS state
  FROM sc15_equipment e
  JOIN latest l
    ON e.eq_id = l.name
 WHERE e.status = 'ACTIVE'
 ORDER BY e.eq_id;
```

위 예제에서는 `PUMP_01`이 `ALARM`, `MOTOR_01`이 `NORMAL`로 표시됩니다. 알람 판정
결과를 애플리케이션이 확인한 뒤 이력 테이블에 기록합니다. 반복 조회 때 같은 알람을
계속 기록할지, 상태가 바뀔 때만 기록할지도 애플리케이션에서 결정합니다.

API나 대시보드는 조회 결과와 함께 마지막 측정 시각을 반환하고, 허용 지연을 넘긴 장비를
별도 `STALE` 상태로 표현합니다. 위 SQL에는 `STALE` 판정이 포함되어 있지 않습니다.
또한 내부 조인을 사용하므로 측정값이 없는 장비는 결과에 나타나지 않습니다. 운영 화면에서는
미수집 장비와 NULL 측정값을 정상 상태로 오인하지 않도록 별도로 처리합니다.
주기적 조회 간격은 유입 주기와 쿼리 비용을 측정해 정합니다.

```sql
INSERT INTO sc15_alarm_log VALUES ('PUMP_01', 'TEMP_HIGH', 83.7);

SELECT _arrival_time, eq_id, alarm_type, measured_value
  FROM sc15_alarm_log
 ORDER BY _arrival_time DESC;
```

장비 ID와 TAG 이름에 같은 값을 사용하므로 조인할 때 문자열 변환이 필요하지 않습니다.
더 복잡한 이름 규칙이 필요하면 적재 단계에서 정규화한 키를
별도 열로 관리하십시오.

## 4단계: 정리

<a id="3단계-정리"></a>

```sql
DROP TABLE sc15_alarm_log;
DROP TABLE sc15_equipment_temp;
DROP TABLE sc15_equipment;
```
