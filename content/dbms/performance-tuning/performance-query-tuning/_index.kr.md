---
type: docs
title: '12.5 조회와 분석 성능 튜닝'
weight: 50
toc: true
---
SELECT 쿼리와 집계 분석의 응답 시간을 단축하기 위한 실무 튜닝 기법을 다룹니다.

## 핵심 원칙

조회 성능을 결정하는 핵심 요소는 네 가지입니다.

### 1. 인덱스 활용

LOG 테이블에는 BITMAP 인덱스, TAG 테이블에는 인메모리 해시 인덱스가 제공됩니다. WHERE 절에 인덱스가 정의된 컬럼을 우선 배치하면 스캔 범위를 크게 줄일 수 있습니다. `EXPLAIN` 명령으로 실행 계획을 확인해 INDEX SCAN이 적용되는지 반드시 검증하십시오.

### 2. 파티션 Pruning

LOG 테이블은 `_arrival_time`, TAG 테이블은 `time` 컬럼을 기준으로 데이터를 파티션에 분산
저장합니다. WHERE 절에 시간 범위를 명시하면 불필요한 파티션을 건너뜁니다. 시간 조건의
효과는 `EXPLAIN`과 실행 시간으로 확인합니다.

### 3. ROLLUP 사전 집계

원시 데이터를 매번 집계하는 대신 ROLLUP으로 미리 계산된 통계(MIN, MAX, AVG, COUNT 등)를
활용하면 반복 집계 비용을 줄일 수 있습니다. 분·시간·일 단위 추세 분석에 적합합니다.

### 4. 힌트 사용

옵티마이저 판단이 최적이 아닌 경우, `/*+ 힌트 */` 구문으로 병렬 처리 계수, 인덱스 사용 여부, ROLLUP 테이블 선택 등을 직접 제어할 수 있습니다. 힌트는 실행 계획을 확인한 뒤 필요한 경우에만 사용합니다.

## 이 섹션의 구성

| 주제 | 설명 |
|------|------|
| [SELECT 성능 튜닝](/dbms/performance-tuning/performance-query-tuning/#performance-tuning-select) | WHERE 절 설계, 시간 범위 조건, EXPLAIN 해석 |
| [검색 연산자 성능 튜닝](/dbms/performance-tuning/performance-query-tuning/#performance-operators-tuning) | 인덱스 활용 가능·불가 연산자, BITMAP vs LSM 선택 |
| [윈도우 함수와 PIVOT 성능 고려사항](/dbms/performance-tuning/performance-query-tuning/#performance-window-functions-considerations-pivot) | 메모리 주의사항, 서브쿼리 선처리 패턴 |
| [ROLLUP 활용 튜닝](/dbms/tag-rollup-usage/performance-tuning-rollup/#tuning-rollup) | ROLLUP 조회 패턴, 계층 설계, WAKEUP INTERVAL |
| [TAG 데이터 대량 정정 성능 고려사항](/dbms/tag-table-usage/tag-data-update-correction/#correction-performance-bulk-considerations-tag-data-update) | TAG data UPDATE 대상 범위와 롤업 재구성 |
| [LOOKUP DML 성능 고려사항](/dbms/lookup-table-usage/privilege-predicate-performance/#performance-considerations-lookup-predicate-dml) | PK fast path, 일반 predicate 대상 수집과 JSON SET 비용 |


<a id="performance-tuning-select"></a>

## SELECT 성능 튜닝

SELECT 쿼리의 성능은 WHERE 절 설계, 컬럼 선택, 실행 계획 확인 순서로 튜닝합니다.

### WHERE 절에서 인덱스 컬럼 우선 사용

옵티마이저는 WHERE 절에 인덱스가 정의된 컬럼이 있으면 INDEX SCAN을 선택합니다. 인덱스 컬럼을 조건의 앞부분에 배치하고, 비인덱스 컬럼은 후처리 필터로 사용합니다.

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

### 시간 범위 조건 필수

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

### SELECT * 대신 필요한 컬럼만 조회

컬럼 기반 저장 구조에서는 필요하지 않은 컬럼을 SELECT 목록에 포함하면 불필요한 I/O가 발생합니다.

```sql
-- 비권장: 모든 컬럼 읽기
SELECT * FROM sensor_tag WHERE name = 'TEMP-01' LIMIT 100;

-- 권장: 필요한 컬럼만 지정
SELECT time, value FROM sensor_tag WHERE name = 'TEMP-01' LIMIT 100;
```

### LIMIT 활용: 전체 스캔 방지

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

### EXPLAIN 결과 해석

`EXPLAIN` 명령으로 실행 계획을 확인합니다. `INDEX SCAN`, `FULL SCAN`, TAG 테이블의 `TAG READ (RAW)` 같은 실제 스캔 노드를 기준으로 최적화 방향을 결정합니다.

#### INDEX SCAN (권장)

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

#### PARALLEL INDEX SCAN (병렬 처리)

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

#### FULL SCAN (주의)

인덱스를 사용하지 못해 모든 레코드를 순차 스캔하는 경우입니다. 대용량 테이블에서 이 플랜이 나타나면 WHERE 절을 검토해야 합니다.

```sql
Mach> EXPLAIN SELECT * FROM machine_log WHERE value > 100.0;

PLAN
------------------------------------------------------------------------------------
 PROJECT
  FULL SCAN (MACHINE_LOG)
```

`value` 컬럼에 인덱스가 없거나, 함수로 감싼 컬럼을 조건에 사용한 경우 FULL SCAN이 발생합니다.

### 시간 범위 스캔 활성화 조건

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

### 요약: 체크리스트

| 항목 | 확인 사항 |
|------|-----------|
| WHERE 절 | 인덱스 컬럼이 조건 앞에 배치되어 있는가 |
| 시간 조건 | LOG는 `_arrival_time`, TAG는 `time` 범위를 명시했는가 |
| 컬럼 선택 | `SELECT *` 대신 필요한 컬럼만 지정했는가 |
| 결과 제한 | 전체 집계가 아닌 경우 `LIMIT`을 사용했는가 |
| 실행 계획 | `EXPLAIN`으로 INDEX SCAN, FULL SCAN, TAG READ 및 key range 확인 |

<a id="performance-operators-tuning"></a>

## 검색 연산자 성능 튜닝

WHERE 절에서 어떤 연산자를 사용하느냐에 따라 인덱스 활용 여부가 결정됩니다.

### 인덱스 사용 가능 연산자

다음 연산자는 BITMAP 또는 LSM 인덱스를 활용해 스캔 범위를 줄입니다.

| 연산자 | 설명 | 예시 |
|--------|------|------|
| `=` | 동등 비교 | `severity = 'ERROR'` |
| `<` | 미만 | `value < 100.0` |
| `<=` | 이하 | `value <= 100.0` |
| `>` | 초과 | `value > 50.0` |
| `>=` | 이상 | `value >= 50.0` |
| `BETWEEN` | 범위 | `value BETWEEN 10.0 AND 90.0` |
| 전방 LIKE | 접두어 일치 | `host LIKE 'server%'` |

```sql
-- 인덱스 활용: BETWEEN (내부적으로 >= AND <= 로 처리)
EXPLAIN SELECT * FROM machine_log
WHERE  response_code BETWEEN 400 AND 499
  AND  _arrival_time >= '2025-06-01' AND _arrival_time < '2025-06-02';

PLAN
------------------------------------------------------------------------------------
 PROJECT
  INDEX SCAN
   *BITMAP RANGE (table id:3, column id:4, index id:5)
   [KEY RANGE]
    * response_code >= 400
    * response_code <= 499
   [FILTER]
    * _arrival_time >= '2025-06-01 00:00:00'
    * _arrival_time < '2025-06-02 00:00:00'
```

### 인덱스 사용 불가 연산자

다음 패턴은 인덱스를 사용하지 못해 FULL SCAN이 발생합니다.

#### 중간/후방 LIKE

와일드카드가 앞에 오는 LIKE 패턴은 인덱스를 사용할 수 없습니다.

```sql
-- 인덱스 미사용: '%xxx%' 또는 '%xxx' 패턴
SELECT * FROM machine_log WHERE message LIKE '%timeout%';  -- FULL SCAN

-- 인덱스 사용 가능: 전방 LIKE (접두어 일치)
SELECT * FROM machine_log WHERE host LIKE 'server%';       -- INDEX SCAN
```

#### 컬럼에 함수 적용

WHERE 절에서 컬럼을 함수로 감싸면 옵티마이저가 인덱스를 사용하지 못합니다.

```sql
-- 인덱스 미사용: 함수 내부 컬럼
SELECT * FROM system_log WHERE UPPER(severity) = 'ERROR';   -- FULL SCAN
SELECT * FROM system_log WHERE LENGTH(message) > 100;       -- FULL SCAN

-- 권장: 비교 값을 변환
SELECT * FROM system_log WHERE severity = 'ERROR';           -- INDEX SCAN
```

#### OR 조건과 인덱스 결합

OR 조건에서 하나라도 인덱스가 없는 컬럼이 포함되면 전체 FULL SCAN으로 전환될 수 있습니다.

```sql
-- 인덱스 있는 컬럼끼리 OR: INDEX(OR) 사용
EXPLAIN SELECT * FROM machine_log WHERE code = 400 OR code = 500;

PLAN
------------------------------------------------------------------------------------
 PROJECT
  INDEX SCAN
   INDEX (OR)
    *BITMAP RANGE (table id:3, column id:4, index id:5)
    *BITMAP RANGE (table id:3, column id:4, index id:5)
   [KEY RANGE]
    * code = 400 or code = 500

-- 인덱스 없는 컬럼이 OR에 포함: FULL SCAN 전환
SELECT * FROM machine_log WHERE code = 400 OR message = 'ok'; -- FULL SCAN
```

OR 조건 대신 UNION ALL로 분리하면 각 쿼리에서 INDEX SCAN을 활용할 수 있습니다.

```sql
-- UNION ALL로 분리 (각각 INDEX SCAN 적용)
SELECT * FROM machine_log WHERE code = 400
UNION ALL
SELECT * FROM machine_log WHERE code = 500;
```

### BITMAP 인덱스 효과 (LOG 테이블)

LOG 테이블에서 기본으로 생성되는 BITMAP 인덱스는 카디널리티(서로 다른 값의 수)가 낮은 컬럼에 특히 효과적입니다.

| 컬럼 특성 | BITMAP 인덱스 효과 |
|-----------|-------------------|
| 카디널리티 낮음 (예: severity, status_code) | 매우 효과적 — 값당 비트 벡터로 빠른 RID 계산 |
| 카디널리티 높음 (예: session_id, message) | 효과 제한적 — 비트 벡터 밀도가 높아 이점 감소 |

```sql
-- 카디널리티 낮은 컬럼 (severity: ERROR/WARN/INFO) → BITMAP 효과적
CREATE INDEX idx_severity ON machine_log (severity);

-- 복합 조건에서 BITMAP 인덱스 AND 연산
EXPLAIN SELECT * FROM machine_log
WHERE  severity = 'ERROR' AND response_code = 500;

PLAN
------------------------------------------------------------------------------------
 PROJECT
  INDEX SCAN
   *BITMAP RANGE (table id:3, column id:2, index id:4)  -- severity 인덱스
   *BITMAP RANGE (table id:3, column id:5, index id:6)  -- response_code 인덱스
   [KEY RANGE]
    * severity = 'ERROR'
    * response_code = 500
```

두 인덱스의 비트 벡터를 AND 연산해 교집합 RID만 읽으므로 단일 인덱스보다 빠릅니다.

### LSM vs BITMAP 인덱스 선택 기준

LOG 테이블에는 두 가지 인덱스 유형을 사용할 수 있습니다.

| 구분 | LSM 인덱스 | BITMAP 인덱스 |
|------|-----------|--------------|
| 구조 | 정렬된 키 목록 | 값별 비트 벡터 |
| 적합 대상 | 숫자형, 날짜형, 고카디널리티 컬럼 | 문자열, 저카디널리티 컬럼 |
| 범위 검색 | 우수 | 보통 |
| 동등 검색 | 우수 | 우수 |
| 복합 AND | 제한적 | 비트 AND 연산으로 매우 빠름 |
| 생성 구문 | `CREATE INDEX ... INDEX_TYPE LSM` | `CREATE BITMAP INDEX ...` 또는 `CREATE INDEX ... INDEX_TYPE BITMAP` |

```sql
-- BITMAP 인덱스 생성 (문자열·저카디널리티 컬럼에 적합)
CREATE BITMAP INDEX idx_severity ON machine_log (severity);

-- LSM 인덱스 생성 (숫자형 범위 검색에 적합)
CREATE INDEX idx_ts ON machine_log (event_time) INDEX_TYPE LSM;
```

**선택 기준 요약:**
- 값의 종류가 수십~수백 개 이하(저카디널리티): BITMAP
- 숫자·날짜 컬럼의 범위 검색: LSM
- 복합 AND 조건으로 여러 컬럼 동시 필터링: BITMAP 조합이 효과적

### IP 타입 BETWEEN 조회 성능

IP 타입 컬럼은 내부적으로 정수로 저장되므로, BETWEEN 조건에서 인덱스 범위 검색이 효율적으로 동작합니다.

```sql
-- IP 범위 조회: BETWEEN으로 서브넷 필터링
SELECT _arrival_time, src_ip, dst_ip, bytes
FROM   network_log
WHERE  src_ip BETWEEN '192.168.1.0' AND '192.168.1.255'
  AND  _arrival_time >= '2025-06-01' AND _arrival_time < '2025-06-02';
```

IP 컬럼에 인덱스를 생성하면 BETWEEN 조건에 대해 INDEX SCAN이 적용됩니다.

```sql
CREATE INDEX idx_src_ip ON network_log (src_ip);
```

### 특정 인덱스 비활성화

옵티마이저가 선택한 인덱스보다 다른 인덱스가 더 효율적일 때 `NO_INDEX` 힌트로 특정 인덱스를 제외할 수 있습니다.

```sql
-- idx_code 인덱스를 제외하고 idx_severity 인덱스만 사용
SELECT /*+ NO_INDEX(machine_log, idx_code) */ *
FROM   machine_log
WHERE  code = 400 AND severity = 'ERROR';

PLAN
------------------------------------------------------------------------------------
 PROJECT
  INDEX SCAN
   *BITMAP RANGE (table id:3, column id:2, index id:4)  -- severity 인덱스만 사용
   [KEY RANGE]
    * severity = 'ERROR'
   [FILTER]
    * code = 400
```

### 요약: 연산자별 인덱스 활용 가능 여부

| 패턴 | 인덱스 활용 |
|------|-------------|
| `col = value` | O |
| `col < value`, `col <= value` | O |
| `col > value`, `col >= value` | O |
| `col BETWEEN v1 AND v2` | O |
| `col LIKE 'prefix%'` | O (전방 LIKE) |
| `col LIKE '%suffix'` | X |
| `col LIKE '%middle%'` | X |
| `FUNC(col) = value` | X |
| `col1 = v1 OR col2 = v2` (col2 인덱스 없음) | X (FULL SCAN) |
| `col1 = v1 OR col1 = v2` (같은 컬럼) | O (INDEX OR) |

<a id="performance-window-functions-considerations-pivot"></a>

## 윈도우 함수와 PIVOT 성능 고려사항

윈도우 함수와 PIVOT은 강력한 분석 도구이지만, 처리 방식에 따라 메모리와 응답 시간에 큰 영향을 줄 수 있습니다. 대용량 데이터 환경에서 안전하게 사용하려면 몇 가지 주의가 필요합니다.

### 윈도우 함수 성능 고려사항

#### 전체 결과셋 메모리 적재

윈도우 함수(`ROW_NUMBER`, `RANK`, `LAG`, `LEAD`, `SUM OVER` 등)는 정렬·분할할 결과가 많을수록
메모리 사용량과 응답 시간이 증가할 수 있습니다.

```sql
-- 주의: 넓은 시간 범위에 직접 윈도우 함수를 적용하면 메모리 사용량이 증가합니다
SELECT name, time, value,
       LAG(value, 1) OVER (PARTITION BY name ORDER BY time) AS prev_value
FROM   sensor_tag
WHERE  time BETWEEN '2025-01-01' AND '2025-06-30';  -- 6개월 전체 데이터
```

`MAX_QPX_MEM` 프로퍼티로 단일 쿼리의 메모리 상한을 설정해 시스템 전체 영향을 제한할 수 있습니다. 표준 샘플 설정의 기본값은 1073741824 bytes(1 GB)입니다.

```
# machbase.conf
MAX_QPX_MEM = 2147483648   # 2 GB
```

#### 서브쿼리로 결과셋을 줄인 후 윈도우 함수 적용

윈도우 함수를 적용하기 전에 서브쿼리에서 집계 또는 범위 제한을 수행해 처리 대상 행 수를 줄입니다.

```sql
-- 권장: 서브쿼리에서 1시간 단위로 집계 후 윈도우 함수 적용
SELECT name, bucket,
       avg_val,
       LAG(avg_val, 1) OVER (PARTITION BY name ORDER BY bucket) AS prev_avg,
       avg_val - LAG(avg_val, 1) OVER (PARTITION BY name ORDER BY bucket) AS delta
FROM (
    -- 서브쿼리에서 대용량 → 소용량으로 집계
    SELECT name,
           rollup('hour', 1, time) AS bucket,
           AVG(value)              AS avg_val
    FROM   sensor_tag
    WHERE  time BETWEEN '2025-01-01' AND '2025-06-30'
    GROUP BY name, bucket
) t
ORDER BY name, bucket;
```

서브쿼리에서 집계·필터링한 뒤 윈도우 함수를 적용하면 처리할 결과 수를 줄일 수 있습니다.

#### 윈도우 함수 적용 전 필터링

윈도우 함수는 정렬과 파티션별 상태를 유지해야 하므로 입력 행 수가 성능에 직접 영향을 줍니다. `PARTITION BY` 자체가 특별한 인덱스 최적화를 보장하는 것은 아니므로, 인덱스가 있는 컬럼과 시간 범위 조건으로 대상 행을 먼저 줄인 뒤 윈도우 함수를 적용합니다.

```sql
-- TAG 테이블: name/time 조건으로 대상 행을 줄인 뒤 윈도우 함수 적용
SELECT name, time, value,
       ROW_NUMBER() OVER (PARTITION BY name ORDER BY time) AS rn
FROM   sensor_tag
WHERE  name IN ('TEMP-01', 'TEMP-02')
  AND  time BETWEEN '2025-06-01' AND '2025-06-02';
```

### PIVOT 성능 고려사항

#### IN 목록 값 수와 컬럼 수

PIVOT의 IN 목록에 포함된 값 수만큼 결과 컬럼이 생성됩니다. 값 수가 많을수록 와이드 테이블이 되어 메모리 사용량과 처리 시간이 증가합니다.

```sql
-- 주의: IN 목록이 길면 결과 컬럼 수가 많아져 성능 저하
SELECT *
FROM (
    SELECT bucket, name, avg_val FROM agg_result
)
PIVOT (
    AVG(avg_val)
    FOR name IN (
        'SENSOR-001', 'SENSOR-002', 'SENSOR-003', ..., 'SENSOR-200'  -- 200개 컬럼
    )
);
```

**권장 사항:**
- IN 목록은 실제로 필요한 태그/값으로만 제한합니다. 불필요한 항목은 제거합니다.
- 태그 수가 수십 개를 초과하는 경우 PIVOT 대신 애플리케이션에서 행렬 변환을 수행하는 것을 검토합니다.

#### 서브쿼리로 집계 후 PIVOT 적용

원시 데이터에 직접 PIVOT을 적용하면 처리 대상 행과 결과 컬럼 수가 커질 수 있습니다. 먼저 일반 집계 서브쿼리나 별도 집계 테이블로 대상 행 수를 줄인 뒤 PIVOT을 적용하면 메모리 사용량을 줄일 수 있습니다.

```sql
-- 권장: 서브쿼리에서 집계 후 PIVOT
SELECT *
FROM (
    SELECT DATE_TRUNC('hour', time) AS bucket,
           name,
           AVG(value)              AS avg_val
    FROM   sensor_tag
    WHERE  name IN ('TEMP-01', 'TEMP-02', 'PRESS-01')
      AND  time BETWEEN '2025-06-01' AND '2025-06-02'
    GROUP BY bucket, name
)
PIVOT (
    AVG(avg_val)
    FOR name IN ('TEMP-01', 'TEMP-02', 'PRESS-01')
)
ORDER BY bucket;
```

이 빌드에서는 `rollup(...)`을 사용하는 ROLLUP 쿼리 위에 바로 PIVOT을 적용할 수 없습니다. ROLLUP 결과를 행렬 형태로 바꾸려면 애플리케이션에서 변환하거나, 필요한 집계 결과를 일반 테이블에 적재한 뒤 그 테이블을 PIVOT 입력으로 사용합니다.

#### PIVOT과 사전 집계 테이블 조합

반복 조회가 많은 경우에는 집계 결과를 별도 테이블에 저장한 뒤 PIVOT 입력으로 사용할 수 있습니다.

```sql
-- 일반 집계 테이블을 PIVOT 입력으로 사용
SELECT *
FROM (
    SELECT bucket,
           name,
           avg_val
    FROM   sensor_hourly_agg
    WHERE  name IN ('TEMP-01', 'TEMP-02')
      AND  bucket BETWEEN '2025-06-01 00:00:00' AND '2025-06-01 06:00:00'
)
PIVOT (
    AVG(avg_val)
    FOR name IN ('TEMP-01', 'TEMP-02')
)
ORDER BY bucket;
```

### 요약: 패턴별 권장 접근법

| 상황 | 권장 접근법 |
|------|-------------|
| 넓은 범위에 윈도우 함수 적용 | 서브쿼리에서 집계·필터링 후 윈도우 함수 적용 |
| PIVOT IN 목록이 수십 개 초과 | 필요한 항목만 선택, 또는 애플리케이션에서 처리 |
| 윈도우 함수 + 대용량 기간 | ROLLUP 또는 일반 집계로 입력 행 수를 줄인 뒤 적용 |
| 메모리 부족 오류 | `MAX_QPX_MEM` 설정 검토, 기간 범위 축소 |
