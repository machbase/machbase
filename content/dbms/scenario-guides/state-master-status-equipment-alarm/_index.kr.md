---
type: docs
title: '15.1 장비 마스터 데이터와 알람 상태 관리'
weight: 30
---

산업 현장에서는 수백~수천 개의 장비가 각기 다른 임계값과 운영 정책을 갖습니다. LOOKUP 테이블로 장비 마스터를 관리하고, TAG 테이블의 센서 데이터와 결합해 임계값 초과 알람을 실시간 감지하고 이력을 기록하는 패턴입니다.

**난이도**: 중급
**소요 시간**: 45~60분
**주요 기능**: LOOKUP 테이블, TAG 테이블, LOG 테이블, JOIN, 임계값 알람

---

## 시나리오 개요

```
LOOKUP 테이블 (equipment)   ← 장비 마스터 (ID, 이름, 위치, 임계값)
        │
        │ JOIN
        ▼
TAG 테이블 (sensor_tag)     ← 실시간 센서 데이터
        │
        │ 임계값 초과 감지
        ▼
LOG 테이블 (alarm_log)      ← 알람 이력 기록
        │
        ▼
대시보드 쿼리               ← 장비 상태 현황판
```

---

## 1단계: LOOKUP 테이블로 장비 마스터 관리

LOOKUP 테이블은 전체 CRUD를 지원하며, 자주 변경되지 않는 참조 데이터(마스터 데이터)에 적합합니다.

```sql
CREATE LOOKUP TABLE equipment (
    eq_id       VARCHAR(32) PRIMARY KEY,
    eq_name     VARCHAR(64),
    location    VARCHAR(64),
    dept        VARCHAR(32),
    temp_limit  DOUBLE,          -- 온도 상한 임계값
    press_limit DOUBLE,          -- 압력 상한 임계값
    status      VARCHAR(16),     -- 운영 상태: ACTIVE, STANDBY, MAINTENANCE
    install_date VARCHAR(10)
);
```

### 장비 마스터 데이터 등록

```sql
INSERT INTO equipment VALUES
    ('PUMP_01', '1호 펌프',  'A동 1층 기계실', '설비팀', 80.0, 5.0, 'ACTIVE',     '2022-03-15');
INSERT INTO equipment VALUES
    ('PUMP_02', '2호 펌프',  'A동 1층 기계실', '설비팀', 80.0, 5.0, 'STANDBY',    '2022-03-15');
INSERT INTO equipment VALUES
    ('MOTOR_01','1호 모터',  'B동 2층 전기실', '전기팀', 90.0, NULL,'ACTIVE',     '2021-07-20');
INSERT INTO equipment VALUES
    ('MOTOR_02','2호 모터',  'B동 2층 전기실', '전기팀', 90.0, NULL,'MAINTENANCE','2021-07-20');
INSERT INTO equipment VALUES
    ('CHILLER_01','냉동기',  'C동 옥상',       '설비팀', 60.0, 8.0, 'ACTIVE',     '2023-01-10');
```

### 장비 정보 조회 및 수정

```sql
-- 전체 장비 조회
SELECT eq_id, eq_name, location, status, temp_limit
FROM equipment
ORDER BY eq_id;

-- 장비 상태 업데이트 (LOOKUP 테이블은 UPDATE 지원)
UPDATE equipment
SET status = 'ACTIVE'
WHERE eq_id = 'MOTOR_02';

-- 임계값 조정
UPDATE equipment
SET temp_limit = 85.0
WHERE eq_id = 'PUMP_01';
```

---

## 2단계: TAG 테이블에 센서 데이터 수집

장비 ID와 측정 항목을 조합해 태그 이름을 구성합니다.

```sql
CREATE TAG TABLE sensor_tag (
    name  VARCHAR(32) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE SUMMARIZED
);

-- 태그 메타데이터 등록
INSERT INTO sensor_tag METADATA VALUES ('PUMP_01.TEMP');
INSERT INTO sensor_tag METADATA VALUES ('PUMP_01.PRESS');
INSERT INTO sensor_tag METADATA VALUES ('MOTOR_01.TEMP');
INSERT INTO sensor_tag METADATA VALUES ('MOTOR_01.CURR');
INSERT INTO sensor_tag METADATA VALUES ('CHILLER_01.TEMP');
INSERT INTO sensor_tag METADATA VALUES ('CHILLER_01.PRESS');
```

### 센서 데이터 삽입 (테스트용)

```sql
-- 정상 범위 데이터
INSERT INTO sensor_tag VALUES ('PUMP_01.TEMP',   NOW(), 72.5);
INSERT INTO sensor_tag VALUES ('PUMP_01.PRESS',  NOW(), 3.8);
INSERT INTO sensor_tag VALUES ('MOTOR_01.TEMP',  NOW(), 68.0);
INSERT INTO sensor_tag VALUES ('CHILLER_01.TEMP',NOW(), 55.2);

-- 임계값 초과 데이터 (알람 발생용)
INSERT INTO sensor_tag VALUES ('PUMP_01.TEMP',   NOW(), 83.7);   -- 임계값 80 초과
INSERT INTO sensor_tag VALUES ('MOTOR_01.TEMP',  NOW(), 94.1);   -- 임계값 90 초과
INSERT INTO sensor_tag VALUES ('CHILLER_01.PRESS',NOW(), 9.3);   -- 임계값 8 초과
```

---

## 3단계: LOOKUP JOIN으로 장비 정보와 센서값 결합 조회

LOOKUP 테이블과 TAG 테이블을 JOIN해 장비 정보와 센서값을 한 번에 조회합니다.

### 현재 센서값과 장비 정보 조합

```sql
SELECT
    e.eq_id,
    e.eq_name,
    e.location,
    t.time,
    t.value                     AS current_temp,
    e.temp_limit,
    e.status
FROM sensor_tag t
    INNER JOIN equipment e
        ON t.name = CONCAT(e.eq_id, '.TEMP')
WHERE t.time >= NOW() - INTERVAL '1' MINUTE
ORDER BY t.time DESC;
```

### 최신값 기준 장비 현황 조회

각 장비의 가장 최근 센서값을 가져옵니다.

```sql
SELECT
    e.eq_id,
    e.eq_name,
    e.location,
    e.status,
    t.value    AS latest_temp,
    e.temp_limit,
    CASE
        WHEN t.value > e.temp_limit THEN 'ALARM'
        WHEN t.value > e.temp_limit * 0.9 THEN 'WARNING'
        ELSE 'NORMAL'
    END        AS alarm_status
FROM equipment e
    LEFT JOIN sensor_tag t
        ON t.name = CONCAT(e.eq_id, '.TEMP')
        AND t.time >= NOW() - INTERVAL '5' MINUTE
WHERE e.status = 'ACTIVE'
ORDER BY e.eq_id;
```

---

## 4단계: 임계값 초과 알람 감지 쿼리

LOOKUP 테이블의 임계값과 TAG 테이블의 센서값을 비교해 알람 대상 장비를 탐지합니다.

### 온도 임계값 초과 장비 목록

```sql
SELECT
    e.eq_id,
    e.eq_name,
    e.location,
    e.dept,
    t.time                              AS alarm_time,
    ROUND(t.value, 2)                   AS measured_temp,
    e.temp_limit,
    ROUND(t.value - e.temp_limit, 2)    AS excess
FROM sensor_tag t
    INNER JOIN equipment e
        ON t.name = CONCAT(e.eq_id, '.TEMP')
WHERE t.time >= NOW() - INTERVAL '5' MINUTE
  AND e.status = 'ACTIVE'
  AND t.value > e.temp_limit
ORDER BY excess DESC;
```

### 압력 임계값 초과 감지

```sql
SELECT
    e.eq_id,
    e.eq_name,
    t.time                              AS alarm_time,
    ROUND(t.value, 2)                   AS measured_press,
    e.press_limit,
    ROUND(t.value - e.press_limit, 2)   AS excess
FROM sensor_tag t
    INNER JOIN equipment e
        ON t.name = CONCAT(e.eq_id, '.PRESS')
WHERE t.time >= NOW() - INTERVAL '5' MINUTE
  AND e.status = 'ACTIVE'
  AND e.press_limit IS NOT NULL
  AND t.value > e.press_limit
ORDER BY alarm_time DESC;
```

---

## 5단계: 알람 이력 LOG 테이블에 기록

알람 발생 이력을 LOG 테이블에 기록해 추적 및 분석에 활용합니다.

```sql
CREATE TABLE alarm_log (
    eq_id       VARCHAR(32),
    eq_name     VARCHAR(64),
    alarm_type  VARCHAR(32),
    measured    DOUBLE,
    threshold   DOUBLE,
    severity    VARCHAR(16),
    alarm_time  DATETIME
);
```

### 알람 이력 삽입

애플리케이션 또는 STREAM에서 임계값 초과를 감지하면 alarm_log에 기록합니다.

```sql
INSERT INTO alarm_log VALUES (
    'PUMP_01',
    '1호 펌프',
    'TEMP_HIGH',
    83.7,
    80.0,
    'CRITICAL',
    NOW()
);

INSERT INTO alarm_log VALUES (
    'MOTOR_01',
    '1호 모터',
    'TEMP_HIGH',
    94.1,
    90.0,
    'CRITICAL',
    NOW()
);
```

### 최근 알람 이력 조회

```sql
SELECT alarm_time, eq_id, eq_name, alarm_type, measured, threshold, severity
FROM alarm_log
WHERE alarm_time >= NOW() - INTERVAL '24' HOUR
ORDER BY alarm_time DESC;
```

### 장비별 알람 발생 빈도 분석

```sql
SELECT
    eq_id,
    eq_name,
    alarm_type,
    COUNT(*) AS alarm_cnt,
    MAX(measured) AS max_value
FROM alarm_log
WHERE alarm_time >= NOW() - INTERVAL '7' DAY
GROUP BY eq_id, eq_name, alarm_type
ORDER BY alarm_cnt DESC;
```

---

## 6단계: 실시간 대시보드용 쿼리 패턴

### 장비 전체 현황판 (장비 상태 + 최근 센서값 + 알람 여부)

```sql
SELECT
    e.eq_id,
    e.eq_name,
    e.location,
    e.status                                    AS eq_status,
    ROUND(t.value, 2)                           AS latest_temp,
    e.temp_limit,
    CASE
        WHEN e.status != 'ACTIVE' THEN 'INACTIVE'
        WHEN t.value > e.temp_limit THEN 'ALARM'
        WHEN t.value > e.temp_limit * 0.9 THEN 'WARNING'
        ELSE 'NORMAL'
    END                                         AS alarm_status,
    (SELECT COUNT(*)
     FROM alarm_log a
     WHERE a.eq_id = e.eq_id
       AND a.alarm_time >= NOW() - INTERVAL '1' HOUR) AS recent_alarm_cnt
FROM equipment e
    LEFT JOIN sensor_tag t
        ON t.name = CONCAT(e.eq_id, '.TEMP')
        AND t.time = (
            SELECT MAX(time)
            FROM sensor_tag
            WHERE name = CONCAT(e.eq_id, '.TEMP')
        )
ORDER BY e.eq_id;
```

### 부서별 알람 현황 집계

```sql
SELECT
    e.dept,
    COUNT(DISTINCT e.eq_id)                             AS total_equipment,
    SUM(CASE WHEN a.eq_id IS NOT NULL THEN 1 ELSE 0 END) AS alarmed_equipment
FROM equipment e
    LEFT JOIN (
        SELECT DISTINCT eq_id
        FROM alarm_log
        WHERE alarm_time >= NOW() - INTERVAL '1' HOUR
    ) a ON e.eq_id = a.eq_id
WHERE e.status = 'ACTIVE'
GROUP BY e.dept
ORDER BY alarmed_equipment DESC;
```

---

## 핵심 포인트 요약

| 항목 | 내용 |
|------|------|
| LOOKUP 테이블 | `CREATE LOOKUP TABLE` 구문. 전체 CRUD 지원. 마스터 데이터·임계값 관리에 적합 |
| TAG 테이블 태그명 규칙 | `장비ID.측정항목` 형식(예: `PUMP_01.TEMP`)으로 구성하면 JOIN 조건 작성이 용이 |
| LOOKUP + TAG JOIN | `CONCAT(e.eq_id, '.TEMP')` 패턴으로 장비 ID와 태그명을 동적으로 결합 |
| 임계값 비교 | `CASE WHEN t.value > e.temp_limit THEN 'ALARM'` 패턴으로 상태 분류 |
| 알람 이력 | LOG 테이블(`alarm_log`)에 임계값 초과 이벤트를 기록해 이력 추적 |
| 대시보드 쿼리 | LOOKUP JOIN + 서브쿼리 조합으로 전체 장비 현황을 단일 쿼리로 제공 |

---

## 다음 단계

- TAG, LOG, RDB 복합 조인 대시보드: [TAG + RDB + LOG 조인 대시보드](../join-tag-rdb-log/)
- STREAM 알람 자동화: [STREAM으로 LOG를 TAG로 자동 적재](/dbms/log-table-usage/stream-log-processing/#stream-log-tag)
- 실시간 상태판: [실시간 상태판 만들기](../state-status-real-time-dashboard/)
