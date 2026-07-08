---
type: docs
title: '쿼리가 느릴 때'
weight: 10
---

쿼리 응답 시간이 갑자기 길어지거나 특정 쿼리만 느린 경우, 먼저 어떤 쿼리가 오래 실행되고 있는지 파악한 뒤 원인을 찾아야 합니다.

## 느린 쿼리 탐지

현재 실행 중인 쿼리와 경과 시간을 확인합니다.

```sql
-- 오래 실행 중인 쿼리 확인
SELECT sess_id, id, state, query,
       DATEDIFF(SECOND, start_time, NOW) AS elapsed_sec
FROM v$stmt
WHERE state != 'IDLE'
ORDER BY elapsed_sec DESC;
```

`elapsed_sec`이 비정상적으로 큰 쿼리가 있다면 해당 `sess_id`와 `query`를 기록해 두십시오.

## EXPLAIN 활용

`EXPLAIN`으로 쿼리 실행 계획을 확인하면 어느 단계에서 병목이 발생하는지 파악할 수 있습니다.

```sql
EXPLAIN SELECT * FROM sensor_tag WHERE name = 'sensor-01' AND time > DATEADD(HOUR, -1, NOW);
```

출력 결과에서 다음을 확인합니다.

- `FULL SCAN`이 보이면 인덱스가 활용되지 않는 것입니다.
- `ROWS`가 예상보다 매우 크다면 필터 조건이 충분하지 않은 것입니다.
- `PARTITION SCAN`이 많다면 시간 범위 필터를 더 좁혀야 합니다.

## 원인별 해결 방법

### 1. 인덱스 없는 테이블 스캔

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

### 2. MINMAX 캐시 미활성화

**증상**: 시간 범위 쿼리가 전체 데이터를 스캔하는 것처럼 느림

컬럼형 테이블의 각 파티션에 대한 최솟값/최댓값 캐시가 꺼져 있으면 시간 범위 필터를 적용해도 불필요한 파티션까지 스캔합니다.

**확인 및 설정**

`machbase.conf`에서 다음 파라미터를 확인합니다.

```
DISK_COLUMNAR_TABLE_MINMAX_CACHE_MAX_SIZE = 131072
```

값이 `0`이면 캐시가 비활성화된 것입니다. 적절한 크기(단위: KB)로 설정하고 서버를 재시작합니다.

### 3. 결과 캐시 미활성화

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

### 4. 과도한 파티션 스캔

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

## 느린 쿼리 강제 중단

응답하지 않는 쿼리는 `sess_id`를 확인한 뒤 강제로 취소합니다.

```sql
-- 쿼리 실행 중인 세션 확인
SELECT sess_id, id, state, query,
       DATEDIFF(SECOND, start_time, NOW) AS elapsed_sec
FROM v$stmt
WHERE state != 'IDLE'
ORDER BY elapsed_sec DESC;

-- 해당 세션의 쿼리 취소
ALTER SYSTEM CANCEL SESSION <sess_id>;
```

`CANCEL SESSION`은 현재 실행 중인 쿼리만 취소하며 세션 연결은 유지됩니다. 세션 자체를 종료하려면 다음을 사용합니다.

```sql
ALTER SYSTEM KILL SESSION <sess_id>;
```

## 추가 참고

성능 튜닝에 관한 전반적인 내용은 [성능 튜닝](/dbms/performance-tuning/) 섹션을 참고하십시오.
