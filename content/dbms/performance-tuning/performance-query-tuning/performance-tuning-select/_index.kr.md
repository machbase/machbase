---
type: docs
title: 'SELECT 성능 튜닝'
weight: 10
---

SELECT 쿼리의 성능은 WHERE 절 설계, 컬럼 선택, 실행 계획 확인 순서로 튜닝합니다. 이 페이지에서는 Machbase의 테이블 유형별 주요 튜닝 기법을 설명합니다.

## WHERE 절에서 인덱스 컬럼 우선 사용

Machbase 옵티마이저는 WHERE 절에 인덱스가 정의된 컬럼이 있으면 INDEX SCAN을 선택합니다. 인덱스 컬럼을 조건의 앞부분에 배치하고, 비인덱스 컬럼은 후처리 필터로 사용합니다.

```sql
-- 권장: 인덱스 컬럼(severity) 조건을 앞에 배치
SELECT _arrival_time, host, message
FROM   system_log
WHERE  severity = 'ERROR'
  AND  message LIKE '%timeout%'
  AND  _arrival_time >= '2025-01-01 00:00:00'
  AND  _arrival_time <  '2025-01-02 00:00:00';

-- 비권장: 함수로 감싼 컬럼은 인덱스를 사용하지 못함
SELECT _arrival_time, host, message
FROM   system_log
WHERE  UPPER(severity) = 'ERROR';   -- 인덱스 미적용, FULL SCAN 발생
```

## 시간 범위 조건 필수

LOG 테이블과 TAG 테이블은 시간 컬럼을 기준으로 파티션을 분산 저장합니다. 시간 범위를 지정하지 않으면 모든 파티션을 스캔하므로 성능이 크게 저하됩니다.

| 테이블 유형 | 시간 컬럼 | 파티션 Pruning 조건 |
|-------------|-----------|---------------------|
| LOG         | `_arrival_time` | `_arrival_time >= ... AND _arrival_time < ...` |
| TAG         | `time`          | `time BETWEEN ... AND ...` |

```sql
-- LOG 테이블: _arrival_time 범위 지정
SELECT _arrival_time, host, value
FROM   machine_log
WHERE  _arrival_time >= '2025-06-01 00:00:00'
  AND  _arrival_time <  '2025-06-02 00:00:00'
  AND  host = 'server-01';

-- TAG 테이블: time 범위 지정
SELECT time, name, value
FROM   sensor_tag
WHERE  name = 'TEMP-01'
  AND  time BETWEEN '2025-06-01 00:00:00' AND '2025-06-01 01:00:00';
```

시간 범위를 생략하면 스캔 범위를 좁히기 어렵고 전체 데이터 범위를 읽을 가능성이 커집니다. `EXPLAIN`에서는 `_arrival_time` 또는 `time` 조건이 `BITMAP RANGE`/TAG READ의 key range에 반영되는지 확인합니다.

## SELECT * 대신 필요한 컬럼만 조회

Machbase는 컬럼 기반 저장 구조를 사용합니다. 필요하지 않은 컬럼을 SELECT 목록에 포함하면 불필요한 I/O가 발생합니다.

```sql
-- 비권장: 모든 컬럼 읽기
SELECT * FROM sensor_tag WHERE name = 'TEMP-01' LIMIT 100;

-- 권장: 필요한 컬럼만 지정
SELECT time, value FROM sensor_tag WHERE name = 'TEMP-01' LIMIT 100;
```

## LIMIT 활용: 전체 스캔 방지

결과 건수를 제한할 수 있는 경우 LIMIT을 사용합니다. LOG 테이블은 기본적으로 최신 데이터부터 역방향으로 스캔하므로, 최신 N건을 빠르게 조회할 때 유용합니다.

```sql
-- 최신 로그 100건만 조회 (전체 스캔 없이 빠르게 반환)
SELECT _arrival_time, severity, message
FROM   system_log
WHERE  severity = 'ERROR'
LIMIT  100;

-- 오래된 데이터부터 순방향으로 N건 조회
SELECT /*+ SCAN_FORWARD(system_log) */ _arrival_time, severity, message
FROM   system_log
WHERE  severity = 'WARN'
LIMIT  50;
```

## EXPLAIN 결과 해석

`EXPLAIN` 명령으로 실행 계획을 확인합니다. `INDEX SCAN`, `FULL SCAN`, TAG 테이블의 `TAG READ (RAW)` 같은 실제 스캔 노드를 기준으로 최적화 방향을 결정합니다.

### INDEX SCAN (권장)

인덱스를 사용해 스캔 범위를 좁힌 경우입니다.

```sql
Mach> EXPLAIN SELECT _arrival_time, host, value
              FROM   machine_log
              WHERE  severity = 'ERROR'
                AND  _arrival_time >= '2025-06-01 00:00:00'
                AND  _arrival_time <  '2025-06-02 00:00:00';

PLAN
------------------------------------------------------------------------------------
 PROJECT
  INDEX SCAN (MACHINE_LOG)
   *BITMAP RANGE (table id:3, column id:2, index id:4)
   [KEY RANGE]
    * severity = 'ERROR'
   *BITMAP RANGE (table id:3, column id:0, index id:0)
   [KEY RANGE]
    * severity = 'ERROR'
    * _arrival_time >= '2025-06-01 00:00:00'
    * _arrival_time < '2025-06-02 00:00:00'
```

- `BITMAP RANGE`: BITMAP 인덱스를 사용해 조건에 맞는 RID 집합을 먼저 계산
- `KEY RANGE`: 인덱스로 처리된 조건
- `FILTER`: 인덱스 스캔 후 추가로 적용되는 조건

### PARALLEL INDEX SCAN (병렬 처리)

`PARALLEL` 힌트를 사용하거나 `QUERY_PARALLEL_FACTOR`가 설정된 경우 병렬 스캔이 적용됩니다.

```sql
Mach> EXPLAIN SELECT /*+ PARALLEL(machine_log, 4) */
              _arrival_time, AVG(value)
              FROM   machine_log
              WHERE  _arrival_time >= '2025-06-01 00:00:00'
                AND  _arrival_time <  '2025-06-02 00:00:00'
              GROUP BY DATE_TRUNC('hour', _arrival_time);

PLAN
------------------------------------------------------------------------------------
 PROJECT
  GROUP AGGREGATE
   PARALLEL INDEX SCAN (MACHINE_LOG)
    *BITMAP RANGE (table id:3, column id:1, index id:5)
    [KEY RANGE]
     * _arrival_time >= '2025-06-01 00:00:00'
     * _arrival_time < '2025-06-02 00:00:00'
```

### FULL SCAN (주의)

인덱스를 사용하지 못해 모든 레코드를 순차 스캔하는 경우입니다. 대용량 테이블에서 이 플랜이 나타나면 WHERE 절을 검토해야 합니다.

```sql
Mach> EXPLAIN SELECT * FROM machine_log WHERE value > 100.0;

PLAN
------------------------------------------------------------------------------------
 PROJECT
  FULL SCAN (MACHINE_LOG)
```

`value` 컬럼에 인덱스가 없거나, 함수로 감싼 컬럼을 조건에 사용한 경우 FULL SCAN이 발생합니다.

## 시간 범위 스캔 활성화 조건

시간 컬럼에 범위 조건(`>=`, `<=`, `BETWEEN`, `<`, `>`)이 있으면 스캔 범위를 줄일 수 있습니다. 이 빌드의 `EXPLAIN`에는 `PARTITION PRUNING`이라는 별도 문자열이 출력되지 않으므로, 시간 컬럼 조건이 `BITMAP RANGE`나 TAG READ의 key range에 포함되는지 확인합니다.

```sql
-- Pruning 활성화: 명시적 범위
WHERE _arrival_time >= '2025-06-01' AND _arrival_time < '2025-06-02'

-- Pruning 활성화: BETWEEN
WHERE time BETWEEN '2025-06-01 00:00:00' AND '2025-06-01 23:59:59'

-- Pruning 비활성화: 함수 적용
WHERE DATE_TRUNC('day', _arrival_time) = '2025-06-01'  -- Pruning 미동작

-- Pruning 비활성화: 동적 표현식 (서버가 계획 수립 시점에 범위를 알 수 없음)
WHERE _arrival_time >= NOW() - INTERVAL '1' HOUR       -- 일부 버전에서 미동작
```

시간 범위 조건이 효과적인지 확인하려면 `EXPLAIN` 결과의 스캔 노드와 key range를 확인하고, 조건 유무에 따른 실행 시간 차이를 비교합니다.

## 요약: 체크리스트

| 항목 | 확인 사항 |
|------|-----------|
| WHERE 절 | 인덱스 컬럼이 조건 앞에 배치되어 있는가 |
| 시간 조건 | LOG는 `_arrival_time`, TAG는 `time` 범위를 명시했는가 |
| 컬럼 선택 | `SELECT *` 대신 필요한 컬럼만 지정했는가 |
| 결과 제한 | 전체 집계가 아닌 경우 `LIMIT`을 사용했는가 |
| 실행 계획 | `EXPLAIN`으로 INDEX SCAN, FULL SCAN, TAG READ 및 key range 확인 |
