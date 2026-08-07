---
type: docs
title: '17.5 쿼리와 성능 문제'
weight: 50
toc: true
---
쿼리 응답이 느리거나, 검색 결과가 예상과 다르거나, 메모리가 부족하거나, TRANSACTION 테이블에서 잠금 충돌이 발생하는 경우 이 섹션에서 원인을 진단하고 해결 방법을 찾으십시오.

시계열 데이터에 최적화된 구조이지만, 설정 미조정이나 쿼리 작성 방식에 따라 성능이 크게 달라질 수 있습니다.

## 이 섹션의 구성

| 페이지 | 내용 |
|--------|------|
| [쿼리가 느릴 때](/dbms/troubleshooting/performance/#slow) | 느린 쿼리 탐지, EXPLAIN 분석, 인덱스 및 캐시 설정 |
| [검색 결과가 예상과 다를 때](/dbms/troubleshooting/performance/#search-results) | 빈 결과, 중복 데이터, 집계 오차, 타임존 문제 |
| [메모리 부족](/dbms/troubleshooting/performance/#memory-out-of) | OOM 증상, 메모리 사용량 확인, 캐시 파라미터 조정 |
| [TRANSACTION 테이블 트랜잭션/잠금 충돌](/dbms/rdb-table-usage/locking-conflict-timeout/#transaction-locking-conflict-rdb) | 잠금 현황 확인, 장시간 트랜잭션 종료, 예방 방법 |


<a id="slow"></a>

## 쿼리가 느릴 때

응답 시간이 갑자기 길어지거나 특정 쿼리만 느리다면, 먼저 어떤 쿼리가 오래 실행되고 있는지 파악해야 합니다.

### 느린 쿼리 탐지

현재 statement 상태를 확인합니다. `V$STMT`에는 시작 시각 컬럼이 없으므로,
오래 실행되는 쿼리는 같은 조회를 반복해 `state`와 `query`가 계속 유지되는지 확인합니다.

```sql
-- statement 상태 확인
SELECT sess_id, id, state, record_size, query
FROM v$stmt
ORDER BY sess_id, id;
```

동일한 `sess_id`, `id`, `query`가 계속 남아 있고 `state`가 진행 중 상태로 유지되면
해당 `sess_id`와 `query`를 기록해 두십시오.

### EXPLAIN 활용

`EXPLAIN`으로 쿼리 실행 계획을 확인하면 어느 단계에서 병목이 발생하는지 파악할 수 있습니다.

```sql
EXPLAIN SELECT *
  FROM sensor_tag
 WHERE name = 'sensor-01'
   AND time > ADD_TIME(SYSDATE, '0/0/0 -1:0:0');
```

출력 결과에서 다음을 확인합니다.

- `FULL SCAN`이 보이면 인덱스가 활용되지 않는 것입니다.
- `ROWS`가 예상보다 매우 크다면 필터 조건이 충분하지 않은 것입니다.
- `PARTITION SCAN`이 많다면 시간 범위 필터를 더 좁혀야 합니다.

### 원인별 해결 방법

#### 1. 인덱스 없는 테이블 스캔

**증상**: EXPLAIN에 `FULL SCAN` 표시, 데이터 양에 비례해 응답 시간이 선형 증가

**확인 방법**

```sql
-- 인덱스 노드 상태 확인
SELECT * FROM v$index_node_status;
```

**해결 방법**

- TAG 테이블은 `name` 컬럼으로 자동 인덱싱됩니다. `name` 조건 없이 조회하면 전체 스캔이 발생합니다. 쿼리에 `WHERE name = '...'` 조건을 추가합니다.
- LOG 테이블의 특정 컬럼을 자주 검색한다면 해당 컬럼에 인덱스를 추가합니다.

```sql
CREATE INDEX idx_sensor_id ON sensor_log (sensor_id);
```

#### 2. MINMAX 캐시 미활성화

**증상**: 시간 범위 쿼리가 전체 데이터를 스캔하는 것처럼 느림

컬럼형 테이블의 각 파티션에 대한 최솟값/최댓값 캐시가 꺼져 있으면 시간 범위 필터를 적용해도 불필요한 파티션까지 스캔합니다.

**확인 및 설정**

`machbase.conf`에서 다음 파라미터를 확인합니다.

```
DISK_COLUMNAR_TABLE_MINMAX_CACHE_MAX_SIZE = 131072
```

값이 `0`이면 캐시가 비활성화된 것입니다. 적절한 크기(단위: KB)로 설정하고 서버를 재시작합니다.

#### 3. 결과 캐시 미활성화

**증상**: 동일한 쿼리를 반복 실행해도 매번 느림

**확인 방법**

```sql
SELECT * FROM v$property WHERE name = 'RS_CACHE_ENABLE';
```

값이 `0`이면 결과 캐시가 꺼져 있는 것입니다.

**해결 방법**

`machbase.conf`에서 결과 캐시를 활성화합니다.

```
RS_CACHE_ENABLE = 1
RS_CACHE_MAX_MEMORY_SIZE = 536870912
```

설정 후 서버를 재시작합니다.

#### 4. 과도한 파티션 스캔

**증상**: 시간 범위 조건을 줬는데도 쿼리가 느림

시간 범위가 너무 넓거나 타임스탬프 조건 없이 쿼리를 실행하면 모든 파티션을 스캔합니다.

**해결 방법**

- 쿼리에 구체적인 시간 범위 조건을 추가합니다.

```sql
-- 나쁜 예: 시간 조건 없음
SELECT * FROM sensor_log WHERE value > 100;

-- 좋은 예: 시간 범위 명시
SELECT * FROM sensor_log
WHERE _ARRIVAL_TIME BETWEEN TO_DATE('2024-01-15', 'YYYY-MM-DD')
                        AND TO_DATE('2024-01-16', 'YYYY-MM-DD')
  AND value > 100;
```

### 느린 쿼리 강제 중단

응답하지 않는 쿼리는 `sess_id`를 확인한 뒤 강제로 취소합니다.

```sql
-- 쿼리 실행 중인 세션 확인
SELECT sess_id, id, state, record_size, query
FROM v$stmt
ORDER BY sess_id, id;

-- 해당 세션의 쿼리 취소
ALTER SYSTEM CANCEL SESSION <sess_id>;
```

`CANCEL SESSION`은 현재 실행 중인 쿼리만 취소하며 세션 연결은 유지됩니다. 세션 자체를 종료하려면 다음을 사용합니다.

```sql
ALTER SYSTEM KILL SESSION <sess_id>;
```

### 추가 참고

성능 튜닝에 관한 전반적인 내용은 [성능 튜닝](/dbms/performance-tuning/) 섹션을 참고하십시오.

<a id="search-results"></a>

## 검색 결과가 예상과 다를 때

쿼리가 오류 없이 실행됐는데 결과가 비어 있거나, 중복 데이터가 보이거나, 집계 값이 맞지 않는 경우입니다.

### 결과가 비어 있을 때

다음 순서로 확인합니다.

#### 1단계: 데이터 존재 여부 확인

```sql
SELECT COUNT(*) FROM sensor_tag;
```

건수가 `0`이면 데이터가 아직 입력되지 않은 것입니다. [입력이 실패할 때](/dbms/troubleshooting/item/#failure)를 참고하십시오.

#### 2단계: 시간 범위 확인

Machbase의 타임스탬프는 나노초(ns) 단위입니다. 밀리초나 초 단위의 값을 그대로 사용하면 시간 범위가 극히 짧거나 아예 벗어납니다.

```sql
-- 실제 저장된 시간 범위 확인
SELECT MIN(time), MAX(time) FROM sensor_tag WHERE name = 'sensor-01';
```

쿼리의 시간 조건과 실제 저장된 시간 범위가 겹치는지 확인합니다.

```sql
-- 나쁜 예: 밀리초 단위 값을 나노초 컬럼과 비교
SELECT * FROM sensor_tag WHERE time > 1705276200000;

-- 좋은 예: TO_DATE 함수 사용
SELECT * FROM sensor_tag
WHERE time > TO_DATE('2024-01-15 09:30:00', 'YYYY-MM-DD HH24:MI:SS');
```

#### 3단계: 태그명 대소문자 확인

TAG 테이블의 `name` 값은 대소문자를 구별합니다. `Sensor-01`과 `sensor-01`은 서로 다른 태그입니다.

```sql
-- 실제 저장된 태그명 확인
SELECT DISTINCT name FROM sensor_tag WHERE name LIKE '%sensor%';
```

#### 4단계: 타임존 설정 확인

서버와 클라이언트의 타임존 설정이 다를 경우 시간 범위 조건이 의도와 다르게 동작할 수 있습니다.

```sql
SELECT * FROM v$property WHERE name = 'DEFAULT_TIMEZONE';
```

서버 타임존이 `UTC`인데 현지 시간으로 조건을 입력하면 결과가 달라집니다. 아래를 참고하십시오.

### 타임존 이슈

서버 타임존과 클라이언트 기대 시간대가 다를 때 발생합니다.

**확인**

```sql
-- 서버 기본 타임존 확인
SELECT * FROM v$property WHERE name = 'DEFAULT_TIMEZONE';

-- 현재 서버 시각 확인
SELECT NOW();
```

**해결 방법**

- 쿼리에서 명시적으로 타임존을 변환합니다.

```sql
-- UTC 서버에서 KST(+9) 기준으로 조회할 때
SELECT * FROM sensor_tag
WHERE time > TO_DATE('2024-01-15 00:00:00', 'YYYY-MM-DD HH24:MI:SS') - INTERVAL '9' HOUR
  AND time < TO_DATE('2024-01-16 00:00:00', 'YYYY-MM-DD HH24:MI:SS') - INTERVAL '9' HOUR;
```

- 또는 `machbase.conf`에서 `DEFAULT_TIMEZONE`을 클라이언트 환경에 맞게 설정합니다.

### 중복 데이터가 보일 때

#### TAG 테이블의 특성

TAG 테이블은 동일한 `name`과 `time` 조합이 중복으로 입력될 수 있습니다. Append 방식은 중복 체크 없이 순차 기록하는 것이 기본 동작입니다.

**확인 방법**

```sql
-- 특정 시간에 중복 값이 있는지 확인
SELECT name, time, COUNT(*) AS cnt
FROM sensor_tag
WHERE name = 'sensor-01'
  AND time BETWEEN TO_DATE('2024-01-15', 'YYYY-MM-DD')
               AND TO_DATE('2024-01-16', 'YYYY-MM-DD')
GROUP BY name, time
HAVING COUNT(*) > 1;
```

**해결 방법**

- 중복 제거가 필요한 조회에서는 `DISTINCT`를 사용합니다.

```sql
SELECT DISTINCT name, time, value FROM sensor_tag WHERE name = 'sensor-01';
```

- 정기 집계에는 ROLLUP을 활용합니다. ROLLUP은 중복 데이터를 집계하므로 자연스럽게 중복이 희석됩니다.

### 집계 결과가 다를 때

#### ROLLUP 갱신 지연

ROLLUP 테이블은 실시간으로 갱신되지 않습니다. 가장 최근에 입력된 데이터가 아직 ROLLUP에 반영되지 않아 집계 결과에 차이가 생길 수 있습니다.

**확인 방법**

```sql
-- 원본 테이블의 집계
SELECT name, AVG(value)
FROM sensor_tag
WHERE name = 'sensor-01'
  AND time > ADD_TIME(SYSDATE, '0/0/0 -1:0:0')
GROUP BY name;

-- ROLLUP 테이블의 집계
SELECT name, AVG(avg_value)
FROM sensor_tag_rollup_1min
WHERE name = 'sensor-01'
  AND time > ADD_TIME(SYSDATE, '0/0/0 -1:0:0')
GROUP BY name;
```

두 결과의 차이가 크다면 ROLLUP이 지연된 것입니다.

**즉시 갱신**

```sql
ALTER SYSTEM FLUSH ROLLUP;
```

이 명령을 실행하면 아직 처리되지 않은 데이터를 즉시 ROLLUP 테이블에 반영합니다. 단, 대용량 데이터가 쌓인 경우 완료까지 시간이 걸릴 수 있습니다.

<a id="memory-out-of"></a>

## 메모리 부족

서버가 OOM(Out of Memory) 오류를 내거나 갑자기 종료되면 메모리 사용량과 설정 파라미터를 점검해야 합니다.

### 증상

- 서버 프로세스가 비정상 종료되고 트레이스 로그에 OOM 관련 메시지가 남음
- 쿼리 실행 중 `ERR: not enough memory` 오류 반환
- 시스템 전체의 메모리 사용률이 지속적으로 높게 유지됨
- Linux OOM Killer에 의해 Machbase 프로세스가 강제 종료됨

### 메모리 사용량 확인

#### Machbase 내부 메모리 통계

```sql
SELECT name, usage, max_usage
  FROM v$sysmem
 ORDER BY usage DESC;
```

각 항목의 의미:

| 항목 | 설명 |
|------|------|
| `NAME` | 메모리 통계 항목 이름 |
| `USAGE` | 현재 사용량 |
| `MAX_USAGE` | 관측된 최대 사용량 |

#### OS 레벨 메모리 확인

```bash
# 전체 메모리 사용량
free -h

# Machbase 프로세스의 메모리 사용량
ps aux | grep machbased | grep -v grep

# OOM Killer 이력 확인 (Linux)
dmesg | grep -i "oom\|out of memory" | tail -20
```

#### 트레이스 로그에서 OOM 오류 확인

```bash
grep -i "out of memory\|OOM\|memory" $MACHBASE_HOME/trc/machbase.trc | tail -20
```

### 원인별 해결 방법

#### 1. 결과 캐시 과다 사용

결과 캐시(`RS_CACHE`)가 메모리의 상당 부분을 점유하고 있는 경우 최대 크기를 줄입니다.

**확인**

```sql
SELECT * FROM v$property WHERE name LIKE 'RS_CACHE%';
```

**해결**

`machbase.conf`에서 최대 메모리 크기를 줄입니다.

```
RS_CACHE_MAX_MEMORY_SIZE = 268435456   # 256MB로 축소 (기본값 512MB)
```

설정 후 서버를 재시작합니다.

#### 2. 대용량 쿼리 동시 실행

여러 세션에서 대용량 쿼리를 동시에 실행하면 쿼리별 임시 메모리가 합산되어 OOM이 발생할 수 있습니다.

**확인**

```sql
-- 현재 실행 중인 쿼리 목록
SELECT sess_id, id, state, record_size, query
FROM v$stmt
ORDER BY sess_id, id;
```

**해결**

문제가 되는 세션을 종료합니다.

```sql
ALTER SYSTEM KILL SESSION <sess_id>;
```

이후 동시 실행 쿼리 수를 줄이거나 쿼리에 시간 범위 조건을 추가하여 스캔 범위를 좁힙니다.

#### 3. 버퍼 크기 과다 설정

`machbase.conf`의 버퍼 관련 파라미터가 물리 메모리에 비해 과하게 설정된 경우입니다.

**해결**

다음 파라미터를 조정합니다.

| 파라미터 | 기본값 | 설명 |
|---------|--------|------|
| `RS_CACHE_MAX_MEMORY_SIZE` | 536870912 (512MB) | 결과 캐시 최대 메모리 |
| `TAG_CACHE_MAX_MEMORY_SIZE` | 134217728 (128MB) | TAG 캐시 메모리 |
| `DISK_COLUMNAR_TABLE_MINMAX_CACHE_MAX_SIZE` | 131072 (128MB) | MINMAX 캐시 크기 (KB 단위) |

물리 메모리가 8GB라면 위 세 항목의 합계가 2GB를 넘지 않도록 설정하십시오. 남은 메모리는 OS 및 쿼리 실행용으로 확보해야 합니다.

### OOM 재발 방지

**단기 조치**

- 결과 캐시와 TAG 캐시 크기를 현재 값의 50%로 줄입니다.
- 동시 접속 수를 `MAX_SESSION_COUNT` 파라미터로 제한합니다.

**장기 조치**

- 불필요한 데이터를 주기적으로 삭제하거나 아카이빙합니다.
- 대용량 쿼리는 시간 범위를 나눠 실행하도록 애플리케이션을 수정합니다.
- 물리 메모리 증설을 검토합니다.

### 메모리 설정 파라미터 요약

| 파라미터 | 기본값 | 설명 |
|---------|--------|------|
| `RS_CACHE_ENABLE` | `1` | 결과 캐시 활성화 여부 (`0`으로 설정해 일시적으로 끌 수 있음) |
| `RS_CACHE_MAX_MEMORY_SIZE` | `536870912` | 결과 캐시 최대 메모리 (bytes) |
| `TAG_CACHE_MAX_MEMORY_SIZE` | `134217728` | TAG 캐시 최대 메모리 (bytes) |
| `MAX_SESSION_COUNT` | `1000` | 최대 동시 세션 수 |
