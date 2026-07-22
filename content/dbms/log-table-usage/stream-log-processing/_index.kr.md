---
title: '7.15 STREAM으로 LOG 데이터 처리'
weight: 150
toc: true
---

STREAM 기능을 사용하여 LOG 테이블의 데이터를 TAG 테이블에 자동 적재하는 방법을 다룹니다.


<a id="stream-log-tag"></a>

## STREAM으로 LOG를 TAG로 자동 적재

### 시나리오 개요

STREAM을 이용해 LOG 테이블에 삽입되는 데이터를 실시간으로 TAG 테이블에 자동 적재하는 파이프라인입니다.

외부 수집기(Collector, OPC-UA 클라이언트, MQTT 브로커 등)가 LOG 테이블에만 데이터를 기록할 수 있는 환경에서, TAG 테이블의 ROLLUP 집계와 시계열 분석 기능을 함께 활용하기 위한 패턴입니다. 애플리케이션 코드 변경 없이 LOG에서 TAG로의 변환을 데이터베이스 내부에서 처리합니다.

**적합한 상황:**

- 기존 수집기가 LOG 테이블 형식(가변 컬럼 스키마)으로만 데이터를 전달하는 경우
- TAG 테이블의 ROLLUP 집계나 `RECENT` 쿼리를 활용하고 싶은 경우
- 다중 센서 채널(V0, V1, C0 ... C15 등)을 각각 별도의 TAG 이름으로 분리해야 하는 경우

### 1단계: 테이블 스키마 설계

#### LOG 테이블 생성

수집기로부터 데이터를 수신할 LOG 테이블을 생성합니다.

```sql
-- PLC 장비 데이터를 수신하는 LOG 테이블
CREATE LOG TABLE plc_log (
    tm      DATETIME,
    v0      DOUBLE,
    v1      DOUBLE,
    c0      DOUBLE,
    c1      DOUBLE,
    c2      DOUBLE
);
```

#### TAG 테이블 생성

ROLLUP 집계 및 시계열 분석을 위한 TAG 테이블을 생성합니다.

```sql
-- 센서 데이터를 저장하는 TAG 테이블
CREATE TAG TABLE sensor_tag (
    name    VARCHAR(80) PRIMARY KEY,
    time    DATETIME    BASETIME,
    value   DOUBLE      SUMMARIZED
);
```

TAG 테이블은 `name` 컬럼으로 각 센서 채널을 구분하므로, STREAM에서 채널별로 태그 이름을 지정합니다.

### 2단계: STREAM 생성

`EXEC STREAM_CREATE` 프로시저로 STREAM을 생성합니다. LOG 테이블의 신규 레코드를 감지하여 지정된 INSERT 쿼리를 자동 실행합니다.

```sql
-- v0 채널을 TAG_V00 이름으로 적재하는 STREAM 생성
EXEC STREAM_CREATE(stream_v0,
    'INSERT INTO sensor_tag SELECT ''TAG_V00'', tm, v0 FROM plc_log;');

-- v1 채널을 TAG_V01 이름으로 적재하는 STREAM 생성
EXEC STREAM_CREATE(stream_v1,
    'INSERT INTO sensor_tag SELECT ''TAG_V01'', tm, v1 FROM plc_log;');

-- c0 채널을 TAG_C00 이름으로 적재하는 STREAM 생성
EXEC STREAM_CREATE(stream_c0,
    'INSERT INTO sensor_tag SELECT ''TAG_C00'', tm, c0 FROM plc_log;');
```

> **문자열 이스케이프**: STREAM 쿼리 내 문자열 리터럴은 작은따옴표를 두 번 겹쳐(`''`) 이스케이프합니다.

### 3단계: STREAM 시작

생성된 STREAM을 시작합니다. 이후부터 LOG 테이블에 새 레코드가 삽입될 때마다 STREAM이 자동으로 동작합니다.

```sql
EXEC STREAM_START(stream_v0);
EXEC STREAM_START(stream_v1);
EXEC STREAM_START(stream_c0);
```

### 4단계: 동작 확인

#### STREAM 상태 조회

`v$streams` 가상 테이블로 실행 중인 STREAM의 상태를 확인합니다.

```sql
SELECT state, name, table_name, query_txt FROM v$streams;
```

출력 예:

```
STATE    NAME       TABLE_NAME  QUERY_TXT
--------------------------------------------------------------------------------------------
RUNNING  STREAM_V0  PLC_LOG     INSERT INTO sensor_tag SELECT 'TAG_V00', tm, v0 FROM plc_log;
RUNNING  STREAM_V1  PLC_LOG     INSERT INTO sensor_tag SELECT 'TAG_V01', tm, v1 FROM plc_log;
RUNNING  STREAM_C0  PLC_LOG     INSERT INTO sensor_tag SELECT 'TAG_C00', tm, c0 FROM plc_log;
```

`v$streams` 컬럼 설명:

| 컬럼 | 설명 |
|------|------|
| `NAME` | STREAM 이름 |
| `LAST_EX_TIME` | 마지막 실행 시각 |
| `TABLE_NAME` | 소스 LOG 테이블 이름 |
| `END_RID` | 소스 테이블에서 마지막으로 처리한 레코드 ID |
| `STATE` | `RUNNING` / `STOPPED` |
| `QUERY_TXT` | STREAM이 실행하는 INSERT 쿼리 |
| `ERROR_MSG` | 오류 발생 시 메시지 |
| `FREQUENCY` | STREAM 실행 빈도 (내부 통계) |

#### 데이터 입력 후 검증

LOG 테이블에 데이터를 삽입하면 STREAM이 즉시 TAG 테이블로 전달합니다.

```sql
-- LOG 테이블에 데이터 삽입
INSERT INTO plc_log VALUES (NOW, 1.23, 4.56, 7.89, 0.12, 3.45);

-- TAG 테이블에 데이터가 적재되었는지 확인
SELECT * FROM sensor_tag RECENT 10;
```

### 5단계: 다중 STREAM 패턴

실제 산업 환경에서는 하나의 LOG 테이블에 수십 개의 센서 채널이 포함되는 경우가 많습니다. 각 채널마다 STREAM을 생성하여 개별 TAG로 분산합니다.

```sql
-- 다중 채널 STREAM 일괄 생성 예시
EXEC STREAM_CREATE(stream_c1,
    'INSERT INTO sensor_tag SELECT ''TAG_C01'', tm, c1 FROM plc_log;');
EXEC STREAM_CREATE(stream_c2,
    'INSERT INTO sensor_tag SELECT ''TAG_C02'', tm, c2 FROM plc_log;');

-- 일괄 시작
EXEC STREAM_START(stream_c1);
EXEC STREAM_START(stream_c2);
```

다중 STREAM 상태 확인:

```sql
SELECT name, state, end_rid FROM v$streams;
```

출력 예 (처리 진행 중):

```
NAME       STATE    END_RID
-------------------------------
STREAM_V0  RUNNING  909912
STREAM_V1  RUNNING  1584671
STREAM_C0  RUNNING  1312416
STREAM_C1  RUNNING  1268520
STREAM_C2  RUNNING  1636800
```

`end_rid`가 LOG 테이블의 총 레코드 수와 동일해지면 모든 데이터가 처리된 상태입니다.

### 6단계: 성능 고려사항

#### STREAM 처리 지연 모니터링

STREAM은 비동기로 동작하므로 삽입 시점과 TAG 테이블 반영 시점 사이에 약간의 지연이 발생할 수 있습니다.

```sql
-- LOG 테이블 레코드 수와 STREAM end_rid 비교
SELECT
    (SELECT COUNT(*) FROM plc_log) AS log_count,
    s.name,
    s.end_rid,
    (SELECT COUNT(*) FROM plc_log) - s.end_rid AS lag
FROM v$streams s;
```

#### STREAM 수와 부하

STREAM 개수가 많을수록 LOG 테이블 삽입 시 처리 부하가 증가합니다. 채널 수가 100개 이상인 경우 다음 대안을 고려합니다.

- 여러 LOG 테이블로 채널을 분산하고 STREAM을 분배
- 애플리케이션 레벨에서 TAG 테이블로 직접 Append

### 7단계: STREAM 중지 및 삭제

#### STREAM 중지

```sql
EXEC STREAM_STOP(stream_v0);
EXEC STREAM_STOP(stream_v1);
EXEC STREAM_STOP(stream_c0);
```

중지된 STREAM은 `v$streams`에서 `STATE = STOPPED`로 표시됩니다. `STREAM_START`로 재시작하면 중지 시점 이후의 레코드부터 처리를 재개합니다.

#### STREAM 삭제

불필요한 STREAM은 먼저 중지한 뒤 삭제합니다.

```sql
EXEC STREAM_STOP(stream_v0);
EXEC STREAM_DROP(stream_v0);
```

### 요약

| 단계 | 작업 | 명령 |
|------|------|------|
| 1 | LOG / TAG 테이블 생성 | `CREATE LOG TABLE`, `CREATE TAG TABLE` |
| 2 | STREAM 생성 | `EXEC STREAM_CREATE(이름, 쿼리)` |
| 3 | STREAM 시작 | `EXEC STREAM_START(이름)` |
| 4 | 상태 확인 | `SELECT * FROM v$streams` |
| 5 | STREAM 중지 | `EXEC STREAM_STOP(이름)` |
| 6 | STREAM 삭제 | `EXEC STREAM_DROP(이름)` |

### 관련 문서

- [TAG 테이블 개요](/dbms/core-concepts/concepts/)
- [ROLLUP 집계 분석](/dbms/tag-rollup-usage/patterns-scenarios/#storage-sensor-data-rollup)
- [대량 데이터 적재 파이프라인](/dbms/scenario-guides/bulk-pipeline/)
