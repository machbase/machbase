---
type: docs
title: '센서 데이터 저장과 ROLLUP 분석'
weight: 10
---

산업 IoT 환경에서는 수십~수천 개의 센서가 초당 수만 건의 데이터를 발생시킵니다. 이 시나리오는 Machbase TAG 테이블에 센서 데이터를 저장하고, ROLLUP 집계로 분·시간·일 단위 통계를 빠르게 조회하는 전체 흐름을 단계별로 안내합니다.

**난이도**: 초급  
**소요 시간**: 30~45분  
**주요 기능**: TAG 테이블, 태그 메타데이터, ROLLUP, Append API

---

## 시나리오 개요

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

## 1단계: TAG 테이블 생성

TAG 테이블은 `(태그명, 시간, 값)` 패턴의 시계열 데이터를 저장하는 데 최적화된 테이블 유형입니다. `BASETIME` 컬럼이 시간축을 정의하고, `SUMMARIZED` 키워드가 붙은 컬럼이 ROLLUP 집계 대상이 됩니다.

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

> **참고**: 온도, 압력, 진동처럼 다양한 물리량을 하나의 테이블로 관리할 때 `name` 컬럼에 태그 이름을 구분자로 넣는 방식(예: `PUMP_01.TEMP`, `PUMP_01.PRESS`)을 흔히 사용합니다.

---

## 2단계: 태그 메타데이터 등록

TAG 테이블에 데이터를 입력하기 전에 태그 이름을 메타데이터로 먼저 등록합니다. 메타데이터는 태그의 설명, 단위, 임계값 등 부가 정보를 관리하는 데 활용됩니다.

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

## 3단계: 데이터 수집 — Append API (Python)

Machbase Python 드라이버의 `machbase()` 클래스를 사용하면 고속 Append API로 데이터를 입력할 수 있습니다. Append API는 INSERT 문보다 훨씬 빠른 대용량 입력에 적합합니다.

### 설치

```bash
pip install machbasedb
```

### Python 코드 예시

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

### SQL INSERT 방식 (소량 테스트용)

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

## 4단계: ROLLUP 테이블 생성

ROLLUP 테이블은 원시 데이터를 시간 단위로 자동 집계합니다. 미리 집계해 두기 때문에 대시보드 조회 시 수백만 건의 원시 데이터를 스캔하지 않아도 됩니다.

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

## 5단계: ROLLUP 집계 쿼리

ROLLUP 결과는 원본 TAG 테이블에 ROLLUP 힌트를 지정해 조회합니다. 내부 ROLLUP 테이블의
물리 컬럼명에 의존하지 않습니다.

### 1분 ROLLUP 조회 — 기본 집계

```sql
-- PUMP_01.TEMP 태그의 1분 평균 조회
SELECT /*+ ROLLUP(sensor_tag, min, AVG) */ time, value
  FROM sensor_tag
 WHERE name = 'PUMP_01.TEMP'
   AND time BETWEEN TO_DATE('2024-01-15 10:00:00', 'YYYY-MM-DD HH24:MI:SS')
                AND TO_DATE('2024-01-15 11:00:00', 'YYYY-MM-DD HH24:MI:SS')
 ORDER BY time;
```

### 1시간 ROLLUP 조회 — 여러 태그 비교

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

### 1일 ROLLUP 조회 — 월간 트렌드

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

## 6단계: 실시간 조회 + 과거 집계 비교 패턴

실제 대시보드에서는 최근 데이터는 원시 테이블에서, 과거 데이터는 ROLLUP 테이블에서 가져오는 패턴을 조합합니다.

### 최근 5분 원시 데이터 조회

```sql
-- 실시간 조회: 원시 데이터
SELECT name, time, value
FROM sensor_tag
WHERE name = 'PUMP_01.TEMP'
  AND time >= NOW() - INTERVAL '5' MINUTE
ORDER BY time DESC;
```

### 오늘 하루 1시간 집계 조회

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

### 원시 데이터와 ROLLUP 집계를 UNION으로 결합

최근 구간은 원시 데이터를, 과거 구간은 ROLLUP을 사용해 조회 성능을 유지하면서 연속적인 시계열 뷰를 제공합니다.

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

## 핵심 포인트 요약

| 항목 | 내용 |
|------|------|
| TAG 테이블 설계 | `name VARCHAR PRIMARY KEY`, `time DATETIME BASETIME`, `value DOUBLE SUMMARIZED` 기본 구조 |
| 메타데이터 등록 | 데이터 입력 전 `INSERT INTO ... METADATA VALUES` 로 태그 이름 등록 필요 |
| Append API | 대용량 수집에는 INSERT보다 Append API 사용. Python `machbasedb` 드라이버 지원 |
| ROLLUP 체인 | `ON tag(value) INTERVAL 1 MIN` → `FROM rollup_min INTERVAL 1 HOUR` 방식으로 단계적 집계 |
| ROLLUP 컬럼 | 각 ROLLUP 테이블에 `avg_value`, `min_value`, `max_value`, `cnt` 컬럼 자동 생성 |
| 실시간 + 집계 조합 | 최근 데이터는 원시 TAG 테이블, 과거 데이터는 ROLLUP 테이블에서 UNION ALL로 결합 |

---

## 다음 단계

- 텍스트 로그와 이벤트 데이터를 다루려면 [로그 데이터 저장과 텍스트 검색](../storage-log-text-search-logs/)을 참고합니다.
- 장비 마스터 정보를 함께 관리하려면 [장비 마스터 데이터와 알람 상태 관리](../state-master-status-equipment-alarm/)를 참고합니다.
- 이상 데이터 정정 후 ROLLUP을 재계산하려면 [이상 데이터 정정 후 ROLLUP Rebuild](../correction-abnormal-data-rollup-rebuild/)를 참고합니다.
