---
type: docs
title: '13.5 STREAM 자동 처리'
weight: 40
---
Machbase는 데이터 변환·이동·처리를 자동화하는 STREAM 기능을 제공합니다. STREAM은 원본 테이블에 새로 입력된 데이터를 감지해 사전 정의된 쿼리를 자동으로 실행하며, 그 결과를 대상 테이블에 저장합니다.

## 이 섹션의 구성

| 주제 | 설명 |
|------|------|
| [STREAM 개요](/dbms/operations-configuration-recovery/automation-stream/#stream) | STREAM의 개념과 동작 원리 |
| [활용 사례](/dbms/operations-configuration-recovery/automation-stream/#stream-use-cases-stream) | STREAM 적용 패턴 |
| [생성과 삭제](/dbms/operations-configuration-recovery/automation-stream/#stream-create-delete-stream) | STREAM_CREATE / STREAM_DROP |
| [시작](/dbms/operations-configuration-recovery/automation-stream/#stream-start-stream) | STREAM_START / STREAM_STOP |
| [사용자 실행 (BY USER)](/dbms/operations-configuration-recovery/automation-stream/#stream-stream-execute-user) | STREAM_EXECUTE 수동 호출 |
| [상태 확인](/dbms/operations-configuration-recovery/automation-stream/#stream-status-check-state-stream) | V$STREAMS |
| [활용 예시](/dbms/operations-configuration-recovery/automation-stream/#stream-examples-stream) | 실전 쿼리 예시 |
| [지원 범위](/dbms/operations-configuration-recovery/automation-stream/#stream-support-scope-stream-edition-cluster) | Edition별 지원 범위 |

> STREAM은 Standard Edition 전용 기능입니다. Cluster Edition에서는 지원되지 않습니다.


<a id="stream"></a>

## STREAM

STREAM은 원본 LOG 테이블에 새로 입력된 데이터를 실시간으로 감지해 미리 정의한 `INSERT ... SELECT` 쿼리를 자동 실행하는 기능입니다. CEP(복합 이벤트 처리), 실시간 집계, 데이터 라우팅에 활용합니다.

### 동작 원리

```
원본 테이블 (LOG)
  ↓ 새 데이터 입력 감지
STREAM 실행 엔진
  ↓ INSERT ... SELECT 실행
대상 테이블 (LOG, TAG 등)
```

STREAM은 마지막으로 처리한 행의 RID(Row ID)를 기억합니다. 다음 실행 때는 그 RID 이후의 새 데이터만 처리합니다. 서버 재시작 후에도 이 위치가 유지되어 연속적으로 처리됩니다.

### 실행 주기

| 실행 조건 | 동작 |
|-----------|------|
| 주기 없음 (기본) | 새 행이 입력될 때마다 즉시 실행 |
| `BY n SECOND` | 매 n초마다 누적 데이터를 집계해 실행 |
| `BY USER` | 사용자가 `EXEC STREAM_EXECUTE`를 호출할 때만 실행 |

주기를 설정하면 SUM, AVG 같은 집계 함수를 사용할 수 있습니다. 주기 없이 실행하면 집계 함수를 사용할 수 없습니다.

### 제약사항

- 쿼리는 `INSERT INTO target SELECT ... FROM source` 형태만 허용됩니다.
- 원본 테이블은 LOG 테이블이어야 합니다.
- STREAM은 Standard Edition 전용입니다.

> STREAM 기능은 **Standard Edition**에서만 지원됩니다. Cluster Edition에서 STREAM 생성을 시도하면 오류가 반환됩니다.

<a id="stream-use-cases-stream"></a>

### STREAM 활용 사례

STREAM은 데이터가 입력되는 시점에 자동으로 변환·필터링·집계를 처리합니다. 별도의 애플리케이션 없이 DB 레벨에서 실시간 파이프라인을 구성할 수 있습니다.

#### 사례 1: 이벤트 필터링

원본 로그에서 특정 조건의 이벤트만 별도 테이블로 분리합니다.

```sql
-- 에러 이벤트만 분리
EXEC STREAM_CREATE('stream_error_filter',
  'INSERT INTO error_log
   SELECT time, source, message
   FROM   event_log
   WHERE  level = ''ERROR''');

EXEC STREAM_START('stream_error_filter');
```

#### 사례 2: 실시간 1분 집계

매 60초마다 원본 데이터를 집계해 요약 테이블을 갱신합니다.

```sql
EXEC STREAM_CREATE('stream_agg_1min',
  'INSERT INTO event_summary
   SELECT source, COUNT(*), AVG(duration)
   FROM   event_log
   GROUP BY source
   BY 60 SECOND');

EXEC STREAM_START('stream_agg_1min');
```

#### 사례 3: 데이터 변환 (ETL)

원본 테이블의 컬럼을 가공해 다른 테이블로 이동합니다.

```sql
EXEC STREAM_CREATE('stream_etl',
  'INSERT INTO processed_log
   SELECT time, UPPER(source), value * 1000
   FROM   raw_log
   WHERE  value IS NOT NULL');

EXEC STREAM_START('stream_etl');
```

#### 사례 4: 수동 실행 (BY USER)

배치 작업이 완료된 시점에 명시적으로 집계를 트리거합니다.

```sql
-- BY USER 스트림 생성
EXEC STREAM_CREATE('stream_batch_aggr',
  'INSERT INTO batch_result
   SELECT DATE_TRUNC(''hour'', time), SUM(amount)
   FROM   transaction_log
   GROUP BY 1
   BY USER');

EXEC STREAM_START('stream_batch_aggr');

-- 배치 완료 후 수동 실행
EXEC STREAM_EXECUTE('stream_batch_aggr');
```

#### 사례 5: 멀티 스트림 파이프라인

여러 STREAM을 연결해 단계적 처리를 구성합니다.

```
raw_log → stream_filter → filtered_log → stream_agg_1min → summary_log
```

```sql
-- 1단계: 필터
EXEC STREAM_CREATE('stream_s1',
  'INSERT INTO filtered_log SELECT * FROM raw_log WHERE status > 0');

-- 2단계: 집계
EXEC STREAM_CREATE('stream_s2',
  'INSERT INTO summary_log
   SELECT DATE_TRUNC(''minute'', time), COUNT(*), AVG(value)
   FROM   filtered_log GROUP BY 1
   BY 60 SECOND');

EXEC STREAM_START('stream_s1');
EXEC STREAM_START('stream_s2');
```

<a id="stream-create-delete-stream"></a>

### STREAM 생성과 삭제

#### STREAM 생성

저장 프로시저 `STREAM_CREATE`로 STREAM을 등록합니다. 생성 시점에 쿼리 유효성을 검사합니다.

```sql
EXEC STREAM_CREATE(stream_name, stream_query_string);
```

| 파라미터 | 설명 |
|----------|------|
| stream_name | STREAM 이름 (DB 내에서 유일해야 함) |
| stream_query_string | `INSERT INTO ... SELECT ... FROM log_table [BY n SECOND | BY USER]` |

##### 즉시 실행 STREAM (주기 없음)

새 행이 입력될 때마다 실행됩니다. 집계 함수(SUM, AVG 등)는 사용할 수 없습니다.

```sql
EXEC STREAM_CREATE('stream_realtime',
  'INSERT INTO alert_log
   SELECT time, device_id, value
   FROM   sensor_log
   WHERE  value > 95.0');
```

##### 주기적 실행 STREAM (BY n SECOND)

설정한 초 단위마다 그 사이에 입력된 데이터를 처리합니다. 집계 함수를 사용할 수 있습니다.

```sql
EXEC STREAM_CREATE('stream_agg_10s',
  'INSERT INTO sensor_summary
   SELECT device_id, AVG(value), MAX(value), COUNT(*)
   FROM   sensor_log
   GROUP BY device_id
   BY 10 SECOND');
```

##### 사용자 호출 STREAM (BY USER)

`EXEC STREAM_EXECUTE`를 호출하기 전까지 실행되지 않습니다.

```sql
EXEC STREAM_CREATE('stream_on_demand',
  'INSERT INTO report_table
   SELECT department, SUM(sales)
   FROM   daily_log
   GROUP BY department
   BY USER');
```

#### STREAM 삭제

```sql
EXEC STREAM_DROP(stream_name);
```

> 실행 중인 STREAM은 삭제할 수 없습니다. 먼저 `EXEC STREAM_STOP`으로 중지해야 합니다.

```sql
-- 올바른 순서
EXEC STREAM_STOP('stream_realtime');
EXEC STREAM_DROP('stream_realtime');
```

#### 쿼리 작성 규칙

- `INSERT INTO target_table SELECT ... FROM source_log_table` 형태만 허용됩니다.
- 소스 테이블은 LOG 테이블이어야 합니다.
- 쿼리 문자열 내 작은따옴표는 두 번(`''`)으로 이스케이프합니다.
- `BY` 절은 쿼리 문자열의 가장 마지막에 위치합니다.

<a id="stream-start-stream"></a>

### STREAM 시작과 중지

#### STREAM 시작

등록된 STREAM을 실행합니다.

```sql
EXEC STREAM_START(stream_name);
```

한 번 시작된 STREAM은 서버 재시작 후에도 계속 동작합니다. 재시작 시 마지막으로 처리한 RID 이후 데이터부터 이어서 처리합니다.

```sql
-- 등록된 STREAM 시작
EXEC STREAM_START('stream_realtime');
EXEC STREAM_START('stream_agg_10s');
```

#### STREAM 중지

```sql
EXEC STREAM_STOP(stream_name);
```

중지된 STREAM은 데이터를 처리하지 않으며, 새로 입력된 데이터도 누적하지 않습니다. 재시작 후에는 중지 시점 이후에 입력된 데이터도 처리합니다.

```sql
EXEC STREAM_STOP('stream_realtime');
```

#### 시작 확인

`V$STREAMS`에서 현재 상태를 확인합니다.

```sql
SELECT NAME, STATE, LAST_EX_TIME
FROM   V$STREAMS
WHERE  NAME = 'stream_realtime';
```

| STATE 값 | 의미 |
|----------|------|
| RUNNING | 실행 중 |
| STOPPED | 중지됨 |
| ERROR | 오류 발생 |

#### 모든 STREAM 상태 확인

```sql
SELECT NAME, STATE, LAST_EX_TIME, ERROR_MSG
FROM   V$STREAMS
ORDER BY NAME;
```

오류가 있는 STREAM은 `ERROR_MSG` 컬럼에서 원인을 확인합니다.

<a id="stream-stream-execute-user"></a>

### BY USER와 STREAM_EXECUTE

`BY USER`로 생성된 STREAM은 사용자가 명시적으로 `EXEC STREAM_EXECUTE`를 호출해야만 실행됩니다. 배치 처리 완료 시점이나 특정 이벤트 발생 시 집계를 트리거하는 패턴에 적합합니다.

#### 생성

```sql
EXEC STREAM_CREATE('stream_on_demand',
  'INSERT INTO hourly_report
   SELECT DATE_TRUNC(''hour'', time), device_id, SUM(value), COUNT(*)
   FROM   sensor_log
   GROUP BY 1, device_id
   BY USER');

EXEC STREAM_START('stream_on_demand');
```

`STREAM_START` 없이는 `STREAM_EXECUTE`를 호출해도 실행되지 않습니다.

#### 수동 실행

```sql
EXEC STREAM_EXECUTE(stream_name);
```

호출 시 마지막 실행 이후 새로 추가된 증분 데이터에 대해서만 쿼리가 실행됩니다. 이전에 처리한 데이터는 다시 처리하지 않습니다.

```sql
-- 배치 로드 완료 후 수동 집계 실행
EXEC STREAM_EXECUTE('stream_on_demand');
```

#### BY USER vs 주기 실행 비교

| 항목 | BY n SECOND | BY USER |
|------|-------------|---------|
| 실행 시점 | 매 n초 자동 실행 | 명시적 호출 시만 실행 |
| 적용 사례 | 실시간 집계 | 배치 완료 트리거, 테스트 |
| 집계 함수 | 사용 가능 | 사용 가능 |

#### 주의사항

- `BY USER` STREAM이 START 상태가 아닌데 EXECUTE를 호출하면 오류가 발생합니다.
- `BY USER` 없이 일반 쿼리(주기 없음)로 생성된 STREAM에 EXECUTE를 호출하면 오류가 발생합니다.

```sql
-- 실행 전 상태 확인
SELECT NAME, STATE FROM V$STREAMS WHERE NAME = 'stream_on_demand';
-- STATE = 'RUNNING' 이어야 EXECUTE 가능
```

<a id="stream-status-check-state-stream"></a>

### STREAM 상태 확인 (V$STREAMS)

`V$STREAMS` 가상 테이블에서 등록된 모든 STREAM의 현재 상태를 조회할 수 있습니다.

#### V$STREAMS 컬럼

| 컬럼 | 설명 |
|------|------|
| NAME | STREAM 이름 |
| STATE | 현재 상태 (RUNNING / STOPPED / ERROR) |
| TABLE_NAME | 소스 테이블 이름 |
| END_RID | 마지막으로 처리한 행의 RID |
| LAST_EX_TIME | 마지막 실행 시각 |
| QUERY_TXT | 등록된 쿼리 원문 |
| FREQUENCY | 실행 주기 (나노초, 0이면 매 행마다 실행) |
| ERROR_MSG | 마지막 오류 메시지 (오류 없으면 NULL) |

#### 조회 예시

```sql
-- 전체 STREAM 상태 조회
SELECT NAME, STATE, TABLE_NAME, LAST_EX_TIME, ERROR_MSG
FROM   V$STREAMS
ORDER BY NAME;
```

```sql
-- 실행 중인 STREAM만 조회
SELECT NAME, LAST_EX_TIME, END_RID
FROM   V$STREAMS
WHERE  STATE = 'RUNNING';
```

```sql
-- 오류 발생 STREAM 확인
SELECT NAME, STATE, ERROR_MSG
FROM   V$STREAMS
WHERE  STATE = 'ERROR';
```

```sql
-- 특정 STREAM 쿼리 확인
SELECT QUERY_TXT
FROM   V$STREAMS
WHERE  NAME = 'stream_agg_10s';
```

#### 상태별 대응

| STATE | 의미 | 조치 |
|-------|------|------|
| RUNNING | 정상 실행 중 | 없음 |
| STOPPED | 중지됨 | 필요시 STREAM_START 재실행 |
| ERROR | 오류로 중단 | ERROR_MSG 확인 후 원인 해결, 재시작 |

#### FREQUENCY 해석

FREQUENCY 값은 나노초(ns) 단위입니다.

| FREQUENCY | 실행 조건 |
|-----------|-----------|
| 0 | 매 행 입력마다 즉시 실행 |
| 1,000,000,000 | 1초마다 실행 |
| 60,000,000,000 | 60초마다 실행 |
| -1 | BY USER (수동 실행) |

<a id="stream-examples-stream"></a>

### STREAM 활용 예시

#### 예시 1: 센서 알람 감지

임계값을 초과하는 센서 값을 알람 테이블에 자동으로 기록합니다.

```sql
-- 알람 대상 테이블
CREATE TABLE alarm_log (
    time     DATETIME,
    sensor   VARCHAR(40),
    value    DOUBLE,
    severity VARCHAR(10)
);

-- STREAM 등록: 90 초과 시 CRITICAL, 80 초과 시 WARNING
EXEC STREAM_CREATE('stream_alarm',
  'INSERT INTO alarm_log
   SELECT time, device_id, value,
          CASE WHEN value > 90 THEN ''CRITICAL'' ELSE ''WARNING'' END
   FROM   sensor_log
   WHERE  value > 80');

EXEC STREAM_START('stream_alarm');
```

#### 예시 2: 1분 단위 이동 집계

매 60초마다 소스 테이블의 신규 데이터를 집계합니다.

```sql
CREATE TABLE sensor_1min (
    time      DATETIME,
    sensor_id VARCHAR(40),
    avg_val   DOUBLE,
    max_val   DOUBLE,
    row_cnt   INTEGER
);

EXEC STREAM_CREATE('stream_1min',
  'INSERT INTO sensor_1min
   SELECT DATE_TRUNC(''minute'', time), device_id,
          AVG(value), MAX(value), COUNT(*)
   FROM   sensor_log
   GROUP BY 1, device_id
   BY 60 SECOND');

EXEC STREAM_START('stream_1min');
```

#### 예시 3: 데이터 정규화 및 라우팅

원본 데이터를 단위 변환해 다른 테이블로 라우팅합니다.

```sql
-- 온도 원본 (°F) → 변환 대상 (°C)
EXEC STREAM_CREATE('stream_unit_convert',
  'INSERT INTO temp_celsius
   SELECT time, sensor_id, (value - 32.0) * 5.0 / 9.0 AS temp_c
   FROM   temp_fahrenheit');

EXEC STREAM_START('stream_unit_convert');
```

#### 예시 4: 멀티 스트림으로 단계 처리

```sql
-- 1단계: 유효 데이터만 필터
EXEC STREAM_CREATE('stream_step1',
  'INSERT INTO valid_log
   SELECT * FROM raw_log WHERE value BETWEEN 0 AND 1000');

-- 2단계: 유효 데이터를 1분 집계
EXEC STREAM_CREATE('stream_step2',
  'INSERT INTO valid_summary
   SELECT DATE_TRUNC(''minute'', time), sensor_id, AVG(value)
   FROM   valid_log
   GROUP BY 1, sensor_id
   BY 60 SECOND');

EXEC STREAM_START('stream_step1');
EXEC STREAM_START('stream_step2');
```

#### 운영 체크

```sql
-- 모든 STREAM 상태 점검
SELECT NAME, STATE, LAST_EX_TIME,
       CASE WHEN ERROR_MSG IS NOT NULL THEN '오류: ' || ERROR_MSG ELSE '정상' END AS status
FROM   V$STREAMS
ORDER BY NAME;
```

<a id="stream-support-scope-stream-edition-cluster"></a>

### STREAM 지원 범위

#### Edition별 지원

| 기능 | Standard Edition | Cluster Edition |
|------|:---:|:---:|
| STREAM_CREATE | O | X |
| STREAM_DROP | O | X |
| STREAM_START | O | X |
| STREAM_STOP | O | X |
| STREAM_EXECUTE | O | X |
| V$STREAMS 조회 | O | X |

> STREAM은 **Standard Edition 전용** 기능입니다. Cluster Edition에서 STREAM 프로시저를 실행하면 오류가 반환됩니다.

#### 소스 테이블 제약

| 소스 테이블 타입 | STREAM 사용 가능 |
|----------------|:---:|
| LOG | O |
| TAG | X |
| RDB | X |
| VOLATILE | X |
| LOOKUP | X |

STREAM의 소스(`FROM` 대상)는 반드시 LOG 테이블이어야 합니다.

#### 지원 쿼리 패턴

| 패턴 | 지원 여부 |
|------|:---:|
| `INSERT INTO ... SELECT ... FROM log_table` | O |
| `INSERT INTO ... SELECT ... FROM log_table WHERE condition` | O |
| `INSERT INTO ... SELECT ... FROM log_table GROUP BY ... BY n SECOND` | O |
| `INSERT INTO ... SELECT ... FROM log_table GROUP BY ... BY USER` | O |
| 서브쿼리 / JOIN | 제한적 |
| 집계 함수 (주기 없음) | X |

#### 동시 실행 STREAM 수

서버당 동시에 실행 가능한 STREAM 수는 시스템 설정에 따라 달라집니다. 운영 중 STREAM이 많아지면 각 STREAM의 `LAST_ELAPSED_MSEC`를 모니터링해 부하를 확인하세요.

#### STREAM과 ROLLUP 비교

| 항목 | STREAM | ROLLUP |
|------|--------|--------|
| 대상 테이블 | LOG | TAG |
| 집계 방식 | INSERT...SELECT (사용자 정의) | 고정 집계 (MIN/MAX/SUM/COUNT) |
| 실행 트리거 | 데이터 입력 감지 | wakeup 스케줄 |
| Edition | Standard만 | Standard + Cluster |
| 재구성(Rebuild) | 미지원 | 지원 |
