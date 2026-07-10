---
title: '6.19 ROLLUP 활용 시나리오'
weight: 180
toc: true
---

<a id="storage-sensor-data-rollup"></a>

## 센서 데이터 저장과 ROLLUP 분석

산업 IoT 환경에서 여러 센서가 지속적으로 생성하는 데이터를 Machbase TAG 테이블에 저장하고,
ROLLUP 집계로 분·시간·일 단위 통계를 조회하는 흐름을 단계별로 다룹니다.

**난이도**: 초급
**소요 시간**: 30~45분
**주요 기능**: TAG 테이블, 태그 메타데이터, ROLLUP, Append API

---

### 시나리오 개요

```
센서 장비
   │
   │ (Append API / Python)
   ▼
TAG 테이블 (sensor_tag)     ← 원시 데이터 고속 저장
   │
   ▼
ROLLUP 테이블              ← 1분 / 1시간 / 1일 자동 집계
   │
   ▼
대시보드 쿼리              ← AVG / MIN / MAX / COUNT
```

---

### 1단계: TAG 테이블 생성

TAG 테이블은 `(태그명, 시간, 값)` 패턴의 시계열 데이터에 최적화된 테이블 유형입니다. `BASETIME` 컬럼이 시간축을 정의하고, `SUMMARIZED` 키워드가 붙은 컬럼이 ROLLUP 집계 대상입니다.

```sql
CREATE TAG TABLE sensor_tag (
    name  VARCHAR(32) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE SUMMARIZED
);
```

| 컬럼 | 역할 |
|------|------|
| `name` | 태그 식별자 (PRIMARY KEY). 센서 ID 또는 채널 이름 |
| `time` | 시간축 (`BASETIME`). ROLLUP 집계의 기준 컬럼 |
| `value` | 측정값 (`SUMMARIZED`). 자동 집계 대상 |

> **참고**: 온도, 압력, 진동 등 다양한 물리량을 하나의 테이블로 관리할 때 `name` 컬럼에 태그 이름을 구분자로 넣는 방식(예: `PUMP_01.TEMP`, `PUMP_01.PRESS`)을 주로 사용합니다.

---

### 2단계: 태그 메타데이터 등록

TAG 테이블에 데이터를 입력하기 전에 태그 이름을 메타데이터로 등록합니다.

```sql
-- 태그 이름 등록
INSERT INTO sensor_tag METADATA VALUES ('PUMP_01.TEMP');
INSERT INTO sensor_tag METADATA VALUES ('PUMP_01.PRESS');
INSERT INTO sensor_tag METADATA VALUES ('PUMP_01.VIB');
INSERT INTO sensor_tag METADATA VALUES ('MOTOR_02.TEMP');
INSERT INTO sensor_tag METADATA VALUES ('MOTOR_02.CURR');
```

등록된 태그 목록을 확인합니다.

```sql
SELECT * FROM sensor_tag METADATA;
```

```
NAME
--------------------------------
PUMP_01.TEMP
PUMP_01.PRESS
PUMP_01.VIB
MOTOR_02.TEMP
MOTOR_02.CURR
[5] row(s) selected.
```

---

### 3단계: 데이터 수집 — Append API (Python)

Machbase Python 드라이버의 `machbase()` 클래스로 고속 Append API를 사용할 수 있습니다. INSERT 문보다 대용량 입력에 훨씬 빠릅니다.

#### 설치

```bash
pip install machbasedb
```

#### Python 코드 예시

```python
import machbasedb
import time
import random
from datetime import datetime

# 접속
conn = machbasedb.connect(
    host='127.0.0.1',
    port=5656,
    user='SYS',
    password='MANAGER'
)

# Append 시작
appender = conn.appender('sensor_tag')

# 센서 태그 목록
tags = ['PUMP_01.TEMP', 'PUMP_01.PRESS', 'PUMP_01.VIB',
        'MOTOR_02.TEMP', 'MOTOR_02.CURR']

# 1초 간격으로 데이터 수집 (예시: 60회)
for _ in range(60):
    ts = datetime.now()
    for tag in tags:
        value = round(random.uniform(20.0, 80.0), 2)
        appender.append((tag, ts, value))
    time.sleep(1)

# Append 완료 및 접속 종료
appender.close()
conn.close()
print("데이터 수집 완료")
```

#### SQL INSERT 방식 (소량 테스트용)

소량 데이터를 직접 입력해 테스트할 때는 INSERT 문을 사용할 수 있습니다.

```sql
INSERT INTO sensor_tag VALUES ('PUMP_01.TEMP', NOW(), 45.3);
INSERT INTO sensor_tag VALUES ('PUMP_01.PRESS', NOW(), 2.8);
INSERT INTO sensor_tag VALUES ('PUMP_01.VIB',  NOW(), 0.12);

-- 과거 시점 데이터 삽입 (테스트용)
INSERT INTO sensor_tag VALUES ('PUMP_01.TEMP',
    TO_DATE('2024-01-15 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 44.1);
INSERT INTO sensor_tag VALUES ('PUMP_01.TEMP',
    TO_DATE('2024-01-15 10:01:00', 'YYYY-MM-DD HH24:MI:SS'), 45.7);
INSERT INTO sensor_tag VALUES ('PUMP_01.TEMP',
    TO_DATE('2024-01-15 10:02:00', 'YYYY-MM-DD HH24:MI:SS'), 46.2);
```

---

### 4단계: ROLLUP 테이블 생성

ROLLUP 테이블은 원시 데이터를 시간 단위로 자동 집계합니다. 미리 집계한 결과를 읽으므로
대시보드 요청마다 전체 원시 범위를 다시 집계하지 않아도 됩니다.

```sql
-- 1분 ROLLUP (원본 TAG 테이블로부터)
CREATE ROLLUP _sensor_rollup_min
    ON sensor_tag(value)
    INTERVAL 1 MIN;

-- 1시간 ROLLUP (1분 ROLLUP으로부터 파생)
CREATE ROLLUP _sensor_rollup_hour
    FROM _sensor_rollup_min
    INTERVAL 1 HOUR;
```

`CREATE ROLLUP`의 interval 단위는 `SEC`, `MIN`, `HOUR`를 사용합니다. 1일 단위 값은
시간 단위 ROLLUP 결과 또는 원본 TAG 테이블을 쿼리에서 집계해 계산합니다.

생성된 ROLLUP 테이블을 확인합니다.

```sql
SELECT rollup_name, source_table, rollup_table, interval_time, wakeup_interval
  FROM v$rollup;
```

```
ROLLUP_NAME              SOURCE_TABLE            ROLLUP_TABLE            INTERVAL_TIME
-------------------------------------------------------------------------------------
_sensor_rollup_min       SENSOR_TAG              _SENSOR_ROLLUP_MIN      60
_sensor_rollup_hour      _SENSOR_ROLLUP_MIN      _SENSOR_ROLLUP_HOUR     3600
[2] row(s) selected.
```

---

### 5단계: ROLLUP 집계 쿼리

ROLLUP 결과는 원본 TAG 테이블에 ROLLUP 힌트를 지정해 조회합니다.

#### 1분 ROLLUP 조회 — 기본 집계

```sql
-- PUMP_01.TEMP 태그의 1분 평균 조회
SELECT /*+ ROLLUP(sensor_tag, min, AVG) */ time, value
  FROM sensor_tag
 WHERE name = 'PUMP_01.TEMP'
   AND time BETWEEN TO_DATE('2024-01-15 10:00:00', 'YYYY-MM-DD HH24:MI:SS')
                AND TO_DATE('2024-01-15 11:00:00', 'YYYY-MM-DD HH24:MI:SS')
 ORDER BY time;
```

#### 1시간 ROLLUP 조회 — 여러 태그 비교

```sql
SELECT
    name,
    time,
    ROUND(avg_value, 2) AS avg_val,
    ROUND(min_value, 2) AS min_val,
    ROUND(max_value, 2) AS max_val
FROM _sensor_rollup_hour
WHERE name IN ('PUMP_01.TEMP', 'MOTOR_02.TEMP')
  AND time >= TO_DATE('2024-01-15 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
ORDER BY name, time;
```

#### 1일 ROLLUP 조회 — 월간 트렌드

```sql
-- 최근 30일 일별 평균 온도
SELECT
    TO_CHAR(time, 'YYYY-MM-DD') AS day,
    ROUND(avg_value, 2)         AS daily_avg,
    ROUND(max_value, 2)         AS daily_max
FROM _sensor_rollup_day
WHERE name = 'PUMP_01.TEMP'
  AND time >= NOW() - INTERVAL '30' DAY
ORDER BY time;
```

---

### 6단계: 실시간 조회 + 과거 집계 비교 패턴

대시보드에서는 최근 데이터를 원시 테이블에서, 과거 데이터를 ROLLUP 테이블에서 가져와 조합합니다.

#### 최근 5분 원시 데이터 조회

```sql
-- 실시간 조회: 원시 데이터
SELECT name, time, value
FROM sensor_tag
WHERE name = 'PUMP_01.TEMP'
  AND time >= NOW() - INTERVAL '5' MINUTE
ORDER BY time DESC;
```

#### 오늘 하루 1시간 집계 조회

```sql
-- 일별 트렌드: 1시간 ROLLUP
SELECT
    TO_CHAR(time, 'HH24') AS hour,
    ROUND(avg_value, 2)   AS avg_temp,
    ROUND(max_value, 2)   AS max_temp
FROM _sensor_rollup_hour
WHERE name = 'PUMP_01.TEMP'
  AND time >= TRUNC(NOW(), 'DD')
ORDER BY time;
```

#### 원시 데이터와 ROLLUP 집계를 UNION으로 결합

최근 구간은 원시 데이터를, 과거 구간은 ROLLUP을 사용해 조회 성능을 유지하면서 연속적인 시계열 뷰를 구성합니다.

```sql
-- 최근 1시간: 원시 데이터 (1분 그룹핑)
SELECT
    TRUNC(time, 'MI')    AS bucket_time,
    ROUND(AVG(value), 2) AS avg_val,
    '원시'               AS source
FROM sensor_tag
WHERE name = 'PUMP_01.TEMP'
  AND time >= NOW() - INTERVAL '1' HOUR
GROUP BY TRUNC(time, 'MI')

UNION ALL

-- 1일 전~1시간 전: 1분 ROLLUP
SELECT
    time                 AS bucket_time,
    ROUND(avg_value, 2)  AS avg_val,
    'ROLLUP'             AS source
FROM _sensor_rollup_min
WHERE name = 'PUMP_01.TEMP'
  AND time BETWEEN NOW() - INTERVAL '1' DAY
               AND NOW() - INTERVAL '1' HOUR
ORDER BY bucket_time;
```

---

### 요약

| 항목 | 내용 |
|------|------|
| TAG 테이블 설계 | `name VARCHAR PRIMARY KEY`, `time DATETIME BASETIME`, `value DOUBLE SUMMARIZED` 기본 구조 |
| 메타데이터 등록 | 데이터 입력 전 `INSERT INTO ... METADATA VALUES` 로 태그 이름 등록 필요 |
| Append API | 대용량 수집에는 INSERT보다 Append API 사용. Python `machbasedb` 드라이버 지원 |
| ROLLUP 체인 | `ON tag(value) INTERVAL 1 MIN` → `FROM rollup_min INTERVAL 1 HOUR` 방식으로 단계적 집계 |
| ROLLUP 컬럼 | 각 ROLLUP 테이블에 `avg_value`, `min_value`, `max_value`, `cnt` 컬럼 자동 생성 |
| 실시간 + 집계 조합 | 최근 데이터는 원시 TAG 테이블, 과거 데이터는 ROLLUP 테이블에서 UNION ALL로 결합 |

---

### 다음 단계

- 텍스트 로그와 이벤트 데이터를 다루려면 [로그 데이터 저장과 텍스트 검색](/dbms/log-table-usage/patterns-scenarios/#storage-log-text-search-logs)을 참고합니다.
- 장비 마스터 정보를 함께 관리하려면 [장비 마스터 데이터와 알람 상태 관리](/dbms/scenario-guides/state-master-status-equipment-alarm/)를 참고합니다.
- 이상 데이터 정정 후 ROLLUP을 재계산하려면 [이상 데이터 정정 후 ROLLUP Rebuild](/dbms/tag-rollup-usage/rollup-rebuild/#correction-abnormal-data-rollup-rebuild)를 참고합니다.

<a id="use-cases-rollup"></a>

## ROLLUP 활용 사례

### 사례 1: IoT 센서 실시간 대시보드

수천 개 센서의 1분 평균을 대시보드에 표시합니다.

```sql
-- 설계: 1초 → 1분 → 1시간 계층
CREATE ROLLUP _iot_ru_1s ON iot_sensor(value) INTERVAL 1 SEC;
CREATE ROLLUP _iot_ru_1m FROM _iot_ru_1s INTERVAL 1 MIN;
CREATE ROLLUP _iot_ru_1h FROM _iot_ru_1m INTERVAL 1 HOUR;

-- 대시보드 쿼리 (최근 1시간 1분 단위)
SELECT rollup('min', 1, time) AS rt,
       AVG(value) AS avg_val,
       MAX(value) AS max_val
FROM   iot_sensor
WHERE  name = 'PUMP-01'
  AND  time BETWEEN NOW - INTERVAL '1' HOUR AND NOW
GROUP BY rt
ORDER BY rt;
```

### 사례 2: 품질 정상 데이터만 집계

품질 플래그(quality=1)인 데이터만 집계해 오류 데이터 영향을 차단합니다.

```sql
CREATE ROLLUP _iot_ok_1m ON iot_sensor(value) INTERVAL 1 MIN
  WHERE quality = 1;

-- 조건 ROLLUP 명시 조회
SELECT /*+ ROLLUP_TABLE(_iot_ok_1m) */
       rollup('min', 5, time) AS rt, AVG(value)
FROM   iot_sensor
WHERE  name = 'PUMP-01'
  AND  time BETWEEN '2024-01-01' AND '2024-01-07'
GROUP BY rt
ORDER BY rt;
```

### 사례 3: OHLC 캔들스틱 차트 (확장 ROLLUP)

주식/에너지 거래 데이터의 OHLC 집계입니다.

```sql
CREATE ROLLUP _tick_ru_5m_ext ON tick_data(price) INTERVAL 5 SEC EXTENSION;

-- 5초 단위 OHLC
SELECT /*+ ROLLUP_TABLE(_tick_ru_5m_ext) */
       rollup('sec', 5, time) AS rt,
       FIRST(time, price) AS open,
       MAX(price)         AS high,
       MIN(price)         AS low,
       LAST(time, price)  AS close,
       SUM(volume)        AS volume
FROM   tick_data
WHERE  symbol = 'KRW-BTC'
  AND  time BETWEEN '2024-01-15 09:00:00' AND '2024-01-15 18:00:00'
GROUP BY rt
ORDER BY rt;
```

### 사례 4: 멀티 센서 비교 (PIVOT + ROLLUP)

여러 센서의 시간 단위 평균을 열로 나란히 표시합니다.

```sql
SELECT * FROM (
    SELECT rollup('hour', 1, time) AS rt, name, AVG(value) AS avg_val
    FROM   iot_sensor
    WHERE  name IN ('PUMP-01', 'PUMP-02', 'PUMP-03')
      AND  time BETWEEN '2024-01-01' AND '2024-01-07'
    GROUP BY rt, name
) PIVOT (
    AVG(avg_val) FOR name IN (
        'PUMP-01' AS pump01,
        'PUMP-02' AS pump02,
        'PUMP-03' AS pump03
    )
)
ORDER BY rt;
```

### 사례 5: 일별 에너지 소비량 계산 (FIRST/LAST)

전력량계의 누적값에서 일별 소비량을 계산합니다.

```sql
CREATE ROLLUP _meter_ru_1h_ext ON energy_meter(kwh_total) INTERVAL 1 HOUR EXTENSION;

-- 일별 소비량 = 일 종료 값 - 일 시작 값
SELECT rt,
       LAST(time, kwh_total) - FIRST(time, kwh_total) AS daily_kwh
FROM (
    SELECT /*+ ROLLUP_TABLE(_meter_ru_1h_ext) */
           rollup('day', 1, time) AS rt,
           FIRST(time, kwh_total), LAST(time, kwh_total)
    FROM   energy_meter
    WHERE  name = 'METER-01'
      AND  time BETWEEN '2024-01-01' AND '2024-01-31'
    GROUP BY rt
) ORDER BY rt;
```
