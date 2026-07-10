---
type: docs
title: '12.6 캐시와 메모리 튜닝'
weight: 60
---
반복 쿼리의 처리 비용을 줄이기 위해 여러 종류의 캐시를 제공합니다. 캐시와 메모리 설정을 올바르게 구성하면 조회 응답 시간을 단축하고 전체 처리량을 높일 수 있습니다.

## Machbase의 주요 캐시

| 캐시 종류 | 설명 | 관련 프로퍼티 |
|---------|------|------------|
| **Result Cache** | 동일한 SELECT 쿼리의 결과를 메모리에 저장하여 재사용 | `RS_CACHE_*` |
| **PVO Cache** | SQL 실행 계획(Plan)을 캐시하여 파싱/최적화 비용 절감 (Standard Edition) | `PVO_CACHE_*` |
| **Min-Max Cache** | 컬럼별 최솟값/최댓값 정보를 캐시하여 파티션 프루닝 가속 | `DISK_COLUMNAR_TABLE_COLUMN_MINMAX_CACHE_SIZE` |

## 메모리 예산 배분 원칙

Machbase 서버의 메모리 예산을 배분할 때는 다음 원칙을 참고하십시오.

```
전체 물리 메모리
  ├── OS 및 기타 프로세스: 약 20%
  ├── 캐시 (Result Cache + PVO Cache 합산): 30~40%
  └── Machbase 처리 공간 (정렬, 집계, 인덱스 빌드 등): 나머지
```

- **Result Cache**(`RS_CACHE_MAX_MEMORY_SIZE`)와 **PVO Cache**(`PVO_CACHE_MAX_MEMORY_SIZE`)의 합이 전체 메모리의 40%를 넘지 않도록 설정합니다.
- Min-Max Cache는 파티션 수에 비례하여 메모리를 사용하므로, 대규모 LOG 테이블 환경에서는 `_ARRIVAL_TIME` 기본값과 필요한 LOG 일반 컬럼의 `MINMAX_CACHE_SIZE`를 함께 검토합니다.
- 메모리 부족(OOM killer 발생, swap 급증)이 감지되면 캐시 상한을 낮추고 `PROCESS_MAX_SIZE`로 프로세스 최대 메모리를 제한하십시오.

## 이 섹션의 구성

- [Result Cache 운영](/dbms/performance-tuning/cache-tuning-memory/#result-cache) — 반복 집계 쿼리의 결과를 캐시하는 방법과 무효화 동작
- [PVO Cache 운영](/dbms/performance-tuning/cache-tuning-memory/#pvo-cache) — SQL 실행 계획 캐시 (Standard Edition)
- [메모리 설정 튜닝](/dbms/performance-tuning/cache-tuning-memory/#tuning-memory-configuration) — 전체 메모리 배분 및 Min-Max Cache 조정


<a id="result-cache"></a>

## Result Cache 운영

Result Cache는 동일한 SELECT 쿼리가 반복 실행될 때 이전에 계산한 결과를 메모리에 저장해 두었다가 즉시 반환하는 기능입니다. 집계 연산이 많은 대시보드나 주기적으로 같은 조건을 조회하는 워크로드에서 응답 시간을 크게 줄일 수 있습니다.

### 동작 원리

1. 클라이언트가 SELECT 쿼리를 실행합니다.
2. 동일한 쿼리가 이미 캐시되어 있고 유효한 상태이면 저장된 결과를 즉시 반환합니다.
3. 캐시가 없거나 무효화된 경우 쿼리를 실제로 실행하고, 조건(`RS_CACHE_TIME_BOUND_MSEC`, `RS_CACHE_MAX_RECORD_PER_QUERY` 등)을 충족하면 결과를 캐시에 저장합니다.

쿼리 텍스트가 완전히 동일해야 캐시 히트가 발생합니다. 리터럴 값, 공백, 대소문자가 달라져 SQL 텍스트가 바뀌면 별도의 캐시 엔트리로 처리됩니다. 바인드 실행은 Result Cache 대상이 아니므로, 반복 조회를 캐시하려면 실제 실행되는 SELECT 텍스트가 동일한지 확인합니다.

### 적합한 워크로드

| 워크로드 유형 | Result Cache 효과 |
|------------|-----------------|
| 대시보드의 주기적 갱신 (30초~수 분 간격) | 높음 |
| 반복 실행되는 집계 쿼리 (COUNT, SUM, AVG 등) | 높음 |
| 배치 Append 후 조회 패턴 (적재 완료 후 일정 시간 조회) | 높음 |
| 실시간 센서 스트림 연속 조회 (매 초 새 데이터 Append) | 낮음 (Append마다 캐시 무효화) |
| 조건이 매번 바뀌는 임시 분석 쿼리 | 낮음 (캐시 히트 없음) |

### 주요 설정 항목

| 프로퍼티 | 기본값 | 설명 |
|--------|------|------|
| [`RS_CACHE_ENABLE`](/dbms/performance-tuning/cache-tuning-memory/#rs-cache-enable) | 1 | Result Cache 활성화 여부 |
| [`RS_CACHE_TIME_BOUND_MSEC`](/dbms/performance-tuning/cache-tuning-memory/#rs-cache-time-bound-msec) | 1000 ms | 이 시간보다 빠른 쿼리는 캐시하지 않음 |
| [`RS_CACHE_MAX_RECORD_PER_QUERY`](/dbms/performance-tuning/cache-tuning-memory/#rs-cache-max-record-per-query) | 기본값 10000, 표준 샘플 50000 | 결과 레코드 수 상한 (초과 시 캐시 안 함) |
| `RS_CACHE_MAX_MEMORY_PER_QUERY` | 16 MB | 쿼리당 최대 캐시 메모리 |
| `RS_CACHE_MAX_MEMORY_SIZE` | 512 MB | 전체 Result Cache 최대 메모리 |
| `RS_CACHE_APPROXIMATE_RESULT_ENABLE` | 0 | 근사 결과 허용 여부 (1이면 더 빠르지만 부정확할 수 있음) |

### 이 섹션의 구성

- [RS_CACHE_ENABLE](/dbms/performance-tuning/cache-tuning-memory/#rs-cache-enable) — Result Cache 전체 활성화/비활성화
- [RS_CACHE_TIME_BOUND_MSEC](/dbms/performance-tuning/cache-tuning-memory/#rs-cache-time-bound-msec) — 캐시 대상 쿼리의 최소 실행 시간 기준
- [RS_CACHE_MAX_RECORD_PER_QUERY](/dbms/performance-tuning/cache-tuning-memory/#rs-cache-max-record-per-query) — 결과 레코드 수 상한 설정
- [V$RS_CACHE_* 확인](/dbms/performance-tuning/cache-tuning-memory/#vrs-cache) — 캐시 상태 모니터링
- [LRU와 동시성](/dbms/performance-tuning/cache-tuning-memory/#concurrency-lru) — 교체 정책 및 고동시성 환경 고려 사항
- [Append invalidation](/dbms/performance-tuning/cache-tuning-memory/#append-invalidation) — 캐시 무효화 동작과 워크로드별 적합성

<a id="rs-cache-enable"></a>
<a id="result-cache-rs-cache-enable"></a>

### RS_CACHE_ENABLE

`RS_CACHE_ENABLE`은 Result Cache 기능 자체를 활성화하거나 비활성화하는 스위치입니다.

#### 프로퍼티 정보

| 항목 | 값 |
|-----|---|
| 최솟값 | 0 (비활성) |
| 최댓값 | 1 (활성) |
| 기본값 | 1 (True) |
| 런타임 변경 | 세션 단위 가능 (`ALTER SESSION SET`) |

#### 설정 방법

##### machbase.conf (서버 시작 시 적용)

```
RS_CACHE_ENABLE = 1
```

##### ALTER SESSION SET (현재 세션 적용)

```sql
-- Result Cache 활성화
ALTER SESSION SET RS_CACHE_ENABLE = 1;

-- Result Cache 비활성화
ALTER SESSION SET RS_CACHE_ENABLE = 0;
```

#### 사용 지침

기본값은 1(활성)이며, 일반적인 운영 환경에서는 변경할 필요가 없습니다.

**0으로 설정하는 경우**: 현재 세션에서 Result Cache 사용이 중단됩니다. 이미 저장된 전역 캐시 엔트리가 즉시 삭제되는 것은 아닙니다.

주로 다음 목적으로 일시적으로 비활성화합니다.

- 쿼리 결과가 최신 데이터와 다르게 보이는 문제를 진단할 때
- Result Cache가 성능에 미치는 영향을 A/B 비교 측정할 때
- 특정 세션에서 Result Cache 영향을 배제하고 비교 측정할 때

문제 진단 후에는 `ALTER SESSION SET RS_CACHE_ENABLE = 1`로 다시 활성화하십시오.

> **참고**: 기존 캐시 엔트리를 명시적으로 제거해야 하면 `ALTER SYSTEM FLUSH RESULT_CACHE`를 사용합니다.

<a id="rs-cache-time-bound-msec"></a>
<a id="result-cache-rs-cache-time-bound-msec"></a>

### RS_CACHE_TIME_BOUND_MSEC

`RS_CACHE_TIME_BOUND_MSEC`는 Result Cache에 저장할 쿼리의 최소 실행 시간(밀리초)을 지정합니다. 실행 시간이 이 값보다 짧은 쿼리는 캐시하지 않습니다.

#### 프로퍼티 정보

| 항목 | 값 |
|-----|---|
| 최솟값 | 0 |
| 최댓값 | 2^64 - 1 (ms) |
| 기본값 | 1000 (1초) |
| 런타임 변경 | 세션 단위 가능 (`ALTER SESSION SET`) |

#### 설정 방법

##### machbase.conf

```
RS_CACHE_TIME_BOUND_MSEC = 1000
```

##### ALTER SESSION SET

```sql
-- 500ms 이상 걸린 쿼리만 캐시
ALTER SESSION SET RS_CACHE_TIME_BOUND_MSEC = 500;

-- 모든 쿼리 결과를 캐시 (0 = 제한 없음)
ALTER SESSION SET RS_CACHE_TIME_BOUND_MSEC = 0;
```

#### 동작 원리

빠르게 완료되는 쿼리는 캐시에 저장하고 조회하는 비용이 실제 쿼리를 다시 실행하는 비용보다 클 수 있습니다. 이 임곗값을 두어 캐시 대상을 "비용이 큰 쿼리"로 제한함으로써 캐시 메모리를 효율적으로 사용합니다.

- **기본값 1000ms**: 1초 이상 걸리는 쿼리만 캐시 대상이 됩니다. 대부분의 집계 쿼리 환경에 적합한 출발점입니다.
- **0으로 설정**: 실행 시간에 관계없이 모든 쿼리 결과를 캐시합니다. 캐시 항목이 급증하여 메모리 사용량이 늘어날 수 있습니다.

#### 튜닝 가이드

1. `V$RS_CACHE_LIST`에서 `TIME_SPENT` 분포를 확인합니다.

   ```sql
   SELECT query, time_spent, hit_count
   FROM v$rs_cache_list
   ORDER BY time_spent DESC;
   ```

2. 반복 실행되는 집계 쿼리의 평균 실행 시간을 파악합니다.

3. 평균 실행 시간의 절반 정도로 `RS_CACHE_TIME_BOUND_MSEC`를 설정합니다.
   - 예: 평균 2초짜리 집계 쿼리 → `RS_CACHE_TIME_BOUND_MSEC = 1000`
   - 예: 평균 500ms짜리 집계 쿼리 → `RS_CACHE_TIME_BOUND_MSEC = 250`

4. `V$RS_CACHE_STAT`의 `CACHE_HIT` 증가 추세와 `V$RS_CACHE_LIST`의 반복 조회 쿼리를 확인하고, 캐시 대상 쿼리가 부족하면 임곗값을 낮추는 방향으로 조정합니다.

> **주의**: 임곗값을 너무 낮게 설정하면 짧은 쿼리까지 캐시되어 `RS_CACHE_MAX_MEMORY_SIZE` 한도에 빠르게 도달하고 LRU 교체가 빈번해질 수 있습니다.

<a id="rs-cache-max-record-per-query"></a>
<a id="result-cache-rs-cache-max-record-per-query"></a>

### RS_CACHE_MAX_RECORD_PER_QUERY

`RS_CACHE_MAX_RECORD_PER_QUERY`는 Result Cache에 저장할 수 있는 쿼리 결과의 최대 레코드 수를 지정합니다. 결과 레코드 수가 이 값을 초과하면 해당 쿼리는 캐시되지 않습니다.

#### 프로퍼티 정보

| 항목 | 값 |
|-----|---|
| 최솟값 | 1 |
| 최댓값 | 2^64 - 1 |
| 기본값 | 10000 |
| 표준 샘플 설정값 | 50000 |
| 런타임 변경 | 세션 단위 가능 (`ALTER SESSION SET`) |

#### 설정 방법

##### machbase.conf

```
RS_CACHE_MAX_RECORD_PER_QUERY = 50000
```

##### ALTER SESSION SET

```sql
-- 결과 1,000건 이하 쿼리만 캐시
ALTER SESSION SET RS_CACHE_MAX_RECORD_PER_QUERY = 1000;

-- 결과 50,000건 이하 쿼리까지 캐시
ALTER SESSION SET RS_CACHE_MAX_RECORD_PER_QUERY = 50000;
```

#### 동작 원리

대용량 결과셋을 캐시하면 그만큼 많은 메모리가 소비되어 다른 쿼리의 캐시 공간을 잠식합니다. 이 상한을 통해 개별 쿼리가 캐시 메모리를 독점하는 것을 방지합니다.

레코드 수 제한과 함께 `RS_CACHE_MAX_MEMORY_PER_QUERY`(쿼리당 최대 캐시 메모리, 기본 16MB)도 함께 적용됩니다. 두 조건 중 하나라도 초과하면 해당 쿼리는 캐시되지 않습니다.

#### 워크로드별 권장 설정

| 워크로드 | 권장 설정 | 이유 |
|---------|---------|------|
| 대시보드용 집계 (수십~수백 건 반환) | 기본값 10000 또는 표준 샘플 50000으로 충분 | 결과셋이 작아 메모리 부담 없음 |
| 롤업 테이블 조회 (수천 건) | 10000~50000 | 적절한 메모리 사용 |
| 원시 데이터 대량 조회 (수만 건 이상) | 캐시 대상에서 제외 권장 | 메모리 낭비, LRU 교체 빈발 |

#### 튜닝 가이드

현재 캐시된 쿼리의 레코드 수 분포를 확인합니다.

```sql
SELECT query, record_count, hit_count
FROM v$rs_cache_list
ORDER BY record_count DESC;
```

- 레코드 수가 많은 쿼리가 캐시를 점유하고 있다면 `RS_CACHE_MAX_RECORD_PER_QUERY`를 낮춰 해당 쿼리를 캐시 대상에서 제외합니다.
- 캐시 히트율이 낮고 `CACHE_REPLACED` 횟수가 많으면 `RS_CACHE_MAX_MEMORY_SIZE`를 늘리거나 `RS_CACHE_MAX_RECORD_PER_QUERY`를 줄여 캐시 용량을 확보합니다.

<a id="vrs-cache"></a>
<a id="result-cache-vrs-cache"></a>

### V$RS_CACHE_* 확인

Machbase는 Result Cache의 상태를 조회할 수 있는 두 가지 가상 테이블을 제공합니다.

#### V$RS_CACHE_LIST

현재 캐시에 저장된 쿼리 목록과 각 엔트리의 상세 정보를 보여줍니다.

| 컬럼 이름 | 설명 |
|---------|------|
| TOUCH_TIME | 캐시를 사용하거나 생성한 마지막 시각 |
| USER_ID | 캐시를 생성한 사용자 식별자 |
| QUERY | 캐시를 만든 쿼리문 |
| TIME_SPENT | 결과를 생성하기까지 경과 시간 |
| TABLE_COUNT | 쿼리문과 연관된 테이블 개수 |
| RECORD_COUNT | 결과 레코드 개수 |
| REFERENCE_COUNT | 현재 참조 중인 세션 수 |
| HIT_COUNT | 이 캐시 엔트리의 히트 횟수 |
| AGGR_TOUCH_TIME | 집계 결과인 경우, 캐시를 사용하거나 생성한 시각 |
| AGGR_HIT_COUNT | 집계 결과인 경우, 캐시 히트 횟수 |

```sql
-- 현재 캐시된 쿼리 목록 (히트 횟수 많은 순)
SELECT touch_time, query, time_spent, record_count, hit_count
FROM v$rs_cache_list
ORDER BY hit_count DESC;
```

#### V$RS_CACHE_STAT

서버 전역 Result Cache 통계 정보를 보여줍니다.

| 컬럼 이름 | 설명 |
|---------|------|
| CACHE_COUNT | 현재 캐시된 엔트리 수 |
| CACHE_HIT | 총 캐시 히트 횟수 |
| AGGR_HIT | 집계 결과의 총 캐시 히트 횟수 |
| CACHE_REPLACED | 캐시 교체 횟수 (LRU에 의해 제거된 횟수) |
| CACHE_MEMORY_USAGE | 캐시가 사용 중인 메모리 크기 (바이트) |

```sql
-- 캐시 히트율 및 교체 현황 확인
SELECT cache_count, cache_hit, aggr_hit, cache_replaced, cache_memory_usage
FROM v$rs_cache_stat;
```

#### 히트율 해석 및 조치

`V$RS_CACHE_STAT`에는 캐시 미스 컬럼이 없으므로 이 뷰만으로 정확한 히트율을 계산할 수 없습니다. `CACHE_HIT` 증가 추세, `CACHE_COUNT`, `CACHE_REPLACED`, 애플리케이션의 전체 쿼리 실행 횟수를 함께 보며 효율을 판단합니다.

| 증상 | 원인 | 조치 |
|-----|------|------|
| `CACHE_HIT`가 낮고 `CACHE_COUNT`도 적음 | `RS_CACHE_TIME_BOUND_MSEC`가 너무 높아 캐시 대상 쿼리 부족 | `TIME_BOUND_MSEC` 값을 낮추어 더 많은 쿼리를 캐시 대상으로 포함 |
| `CACHE_HIT`가 낮고 `CACHE_COUNT`는 많음 | 쿼리 패턴 다양 (반복 실행 쿼리가 적음) | Result Cache 의존도를 낮추고 인덱스·모델링 튜닝 검토 |
| `CACHE_REPLACED`가 지속 증가 | 캐시 메모리 한도 부족으로 LRU 교체 빈발 | `RS_CACHE_MAX_MEMORY_SIZE` 증설 또는 `RS_CACHE_MAX_RECORD_PER_QUERY` 축소 |
| `CACHE_MEMORY_USAGE`가 `RS_CACHE_MAX_MEMORY_SIZE`에 근접 | 캐시 포화 상태 | `RS_CACHE_MAX_MEMORY_SIZE` 증설 검토 |

#### 모니터링 예시

```sql
-- 가장 많이 캐시 히트된 쿼리 Top 10
SELECT query, hit_count, record_count, time_spent
FROM v$rs_cache_list
ORDER BY hit_count DESC
LIMIT 10;

-- 캐시 메모리 사용 현황 요약
SELECT
    cache_count,
    cache_hit,
    cache_replaced,
    cache_memory_usage / 1024 / 1024 AS memory_mb
FROM v$rs_cache_stat;
```

<a id="concurrency-lru"></a>
<a id="result-cache-concurrency-lru"></a>

### LRU와 동시성

Result Cache는 메모리 한도에 도달했을 때 LRU(Least Recently Used) 정책으로 오래된 캐시 항목을 제거합니다. 고동시성 환경에서 캐시를 안정적으로 운영하려면 LRU 동작과 동시성 특성을 이해해야 합니다.

#### LRU 교체 정책

캐시 메모리가 `RS_CACHE_MAX_MEMORY_SIZE` 한도에 도달하면 가장 오랫동안 사용(히트)되지 않은 항목부터 순서대로 제거합니다.

- `V$RS_CACHE_STAT`의 `CACHE_REPLACED` 값이 지속적으로 증가하면 LRU 교체가 빈번하게 발생하고 있다는 신호입니다.
- 교체가 빈발하면 새로 추가된 캐시가 히트되기 전에 제거되는 악순환이 생길 수 있습니다.

**대응**: 설정 파일에서 `RS_CACHE_MAX_MEMORY_SIZE`를 늘린 뒤 재시작하거나, 세션 단위 `RS_CACHE_MAX_RECORD_PER_QUERY`를 낮춰 개별 엔트리 크기를 제한합니다.

```sql
-- 교체 횟수 확인
SELECT cache_replaced FROM v$rs_cache_stat;

-- 큰 캐시 엔트리를 줄이기 위한 세션 설정 예시
ALTER SESSION SET RS_CACHE_MAX_RECORD_PER_QUERY = 1000;
```

#### 동시성 처리

Result Cache의 동시성은 Machbase 내부에서 자동으로 관리되므로 별도의 사용자 설정이 필요하지 않습니다.

- 여러 세션이 동시에 동일한 쿼리를 실행하면, 첫 번째 세션이 캐시를 생성하는 동안 나머지 세션도 캐시 결과를 안전하게 공유할 수 있도록 내부 락(lock)이 관리됩니다.
- 캐시 히트가 많을수록 실제 쿼리 실행이 줄어들어 **lock contention**이 감소하고 동시 처리 처리량이 향상됩니다.

#### 고동시성 환경 권장 설정

| 상황 | 권장 조치 |
|-----|---------|
| 세션 수가 많고 동일 쿼리 반복 실행 | `RS_CACHE_MAX_MEMORY_SIZE`를 충분히 크게 설정하여 히트율 유지 |
| 짧은 주기로 대시보드 갱신 (초 단위) | `RS_CACHE_TIME_BOUND_MSEC`를 낮춰 더 많은 쿼리를 캐시 대상으로 포함 |
| 세션별로 쿼리가 제각각 (반복 패턴 없음) | Result Cache 의존도를 낮추고 캐시 메모리 상한을 적게 할당 |

#### TOUCH_TIME을 통한 활성 캐시 확인

`V$RS_CACHE_LIST`의 `TOUCH_TIME`은 해당 캐시 항목이 마지막으로 사용된 시각입니다. `TOUCH_TIME`이 오래된 항목은 LRU 교체 후보가 됩니다.

```sql
-- 오래 사용되지 않은 캐시 항목 확인
SELECT touch_time, query, hit_count
FROM v$rs_cache_list
ORDER BY touch_time ASC;
```

<a id="result-cache-append-invalidation"></a>

### append invalidation

Machbase의 Result Cache는 캐시 생성 시점의 테이블 상태를 함께 기록합니다. 테이블에 Append 또는 Insert가 발생하면 다음 캐시 조회 시 테이블 상태 차이를 감지해 기존 엔트리를 재사용하지 않고 실제 쿼리를 다시 실행합니다.

#### 무효화 동작

- TAG 테이블 또는 LOG 테이블에 `APPEND` 또는 `INSERT`가 발생하면, 해당 테이블을 참조하는 기존 캐시 엔트리는 다음 조회에서 재사용되지 않습니다.
- 재사용할 수 없는 엔트리는 실제 쿼리 실행 후 조건을 만족하면 새 결과로 다시 캐시됩니다.
- 캐시 엔트리를 즉시 제거해야 하는 운영 작업에는 `ALTER SYSTEM FLUSH RESULT_CACHE`를 사용합니다.

#### 워크로드별 캐시 효과

##### 실시간 스트리밍 환경 (캐시 효과 낮음)

센서 데이터가 매 초, 혹은 더 짧은 간격으로 Append되는 환경에서는 캐시가 무효화되는 빈도가 매우 높아 사실상 캐시 히트가 발생하지 않습니다.

```
시각  T=0   T=1   T=2   T=3
      Append Append Append Append
      기존 캐시 재사용 실패 반복 → 캐시 효과 낮음
```

이런 환경에서는 `RS_CACHE_ENABLE = 0`으로 비활성화하거나, 롤업(Rollup) 테이블을 별도로 구성하여 집계 결과를 롤업 테이블에서 조회하는 방식을 권장합니다.

##### 배치 Append 패턴 (캐시 효과 높음)

데이터가 주기적으로 일괄 적재되고, 적재 완료 후 일정 시간 동안 조회만 이루어지는 환경에서는 캐시 효과가 극대화됩니다.

```
시각  T=0      T=30분    T=60분
      배치 적재  → 조회만  → 배치 적재  → 조회만
      캐시 재생성  캐시 히트  캐시 재생성   캐시 히트
```

배치 적재 직후에는 캐시가 재구성되므로 첫 번째 조회는 실제 실행되지만, 이후 동일한 쿼리는 캐시에서 즉시 반환됩니다.

#### 명시적 캐시 비우기

```sql
ALTER SYSTEM FLUSH RESULT_CACHE;
```

`RS_CACHE_APPROXIMATE_RESULT_ENABLE`은 설정 파일에서 지정하는 프로퍼티입니다. 이 빌드에서는 `ALTER SYSTEM SET` 또는 `ALTER SESSION SET`으로 런타임 변경할 수 없습니다.

<a id="pvo-cache"></a>

## PVO Cache 운영 (Standard Edition 중심)

PVO(Partition Value Object) Statement Cache는 SQL 실행 계획(Plan)을 메모리에 캐시하여, 동일한 SQL이 반복 실행될 때 파싱과 최적화 비용을 절감합니다. **Standard Edition에서만 동작**합니다.

### 동작 원리

1. SQL이 처음 실행되면 파싱 및 최적화를 거쳐 실행 계획(Plan)을 생성합니다.
2. 생성된 Plan을 SQL 텍스트와 사용자, 기본 날짜 포맷, 시간대, 숨김 컬럼 표시 여부, 쿼리 병렬도 같은 세션 속성을 키로 하여 PVO Cache에 저장합니다.
3. 동일한 SQL이 다시 실행되면 캐시에서 Plan을 재사용하여 파싱·최적화 단계를 건너뜁니다.

바인드 변수를 사용하면 SQL 텍스트가 같게 유지되어 파싱·최적화 비용을 줄이는 데 유리합니다. 다만 위 세션 속성이 다르면 서로 다른 캐시 엔트리로 처리될 수 있습니다.

### 주요 프로퍼티

| 프로퍼티 | 기본값 | 설명 |
|--------|------|------|
| `PVO_CACHE_ENABLE` | 1 | PVO Cache 활성화 여부 |
| `PVO_CACHE_MAX_MEMORY_SIZE` | 256 MB | 전체 PVO Cache 최대 메모리 크기 (바이트) |
| `PVO_CACHE_MAX_PLANS_PER_SQL` | 512 | SQL당 최대 캐시 플랜 수 |
| `PVO_CACHE_MAX_SQL_ENTRIES` | 0 (무제한) | 캐시 가능한 최대 SQL 엔트리 수 |
| `PVO_CACHE_SHARD_COUNT` | 16 | 캐시 샤드 수 (서버 재시작 필요) |

> **참고**: `PVO_CACHE_SHARD_COUNT`는 초기화 시점에만 적용되며, 변경 시 서버 재시작이 필요합니다. 나머지 프로퍼티는 `ALTER SYSTEM SET`으로 런타임 변경이 가능합니다.

### 설정 방법

#### machbase.conf

```
PVO_CACHE_ENABLE          = 1
PVO_CACHE_MAX_MEMORY_SIZE = 268435456
PVO_CACHE_MAX_PLANS_PER_SQL = 512
PVO_CACHE_MAX_SQL_ENTRIES = 0
PVO_CACHE_SHARD_COUNT     = 16
```

#### ALTER SYSTEM SET

```sql
-- PVO Cache 메모리 한도를 512MB로 증설
ALTER SYSTEM SET PVO_CACHE_MAX_MEMORY_SIZE = 536870912;

-- SQL당 최대 플랜 수 조정
ALTER SYSTEM SET PVO_CACHE_MAX_PLANS_PER_SQL = 256;
```

### V$PVO_CACHE_STAT으로 상태 확인

```sql
SELECT * FROM v$pvo_cache_stat;
```

| 컬럼 이름 | 설명 |
|---------|------|
| CACHE_ENTRY_COUNT | 캐시에 적재된 SQL 엔트리 수 |
| CACHE_HANDLE_COUNT | 캐시된 플랜(핸들) 총 수 |
| CACHE_MEMORY_USAGE | 현재 사용 중인 캐시 메모리 크기 |
| CACHE_MAX_MEMORY_SIZE | 설정된 캐시 메모리 한도 |
| CACHE_MAX_PLANS_PER_SQL | SQL당 최대 플랜 수 |
| CACHE_MAX_SQL_ENTRIES | 최대 SQL 엔트리 수 |
| CACHE_SHARD_COUNT | 캐시 샤드 수 |
| CACHE_HIT | 캐시 히트 횟수 |
| CACHE_MISS | 캐시 미스 횟수 |
| SINGLEFLIGHT_WAIT | 동일 SQL 동시 빌드 대기 횟수 |
| BUILD_COUNT | 플랜 빌드 시도 횟수 |
| BUILD_FAIL | 플랜 빌드 실패 횟수 |
| INVALIDATE_COUNT | 무효화된 플랜 수 |
| EVICT_COUNT | 메모리 한도 초과로 캐시 축출된 횟수 |
| FLUSH_COUNT | 명시적 flush 횟수 |

### V$PVO_CACHE_LIST로 SQL별 상세 확인

```sql
-- 히트 횟수가 많은 SQL Top 10
SELECT touch_time, query, hit_count, handle_count
FROM v$pvo_cache_list
ORDER BY hit_count DESC
LIMIT 10;
```

### 튜닝 가이드

| 증상 | 원인 | 조치 |
|-----|------|------|
| `CACHE_MISS`가 많고 `CACHE_HIT`가 낮음 | 쿼리 다양성이 높거나 캐시 공간 부족 | `PVO_CACHE_MAX_MEMORY_SIZE` 증설, `PVO_CACHE_MAX_SQL_ENTRIES` 확인 |
| `EVICT_COUNT`가 지속 증가 | 메모리 한도 부족으로 빈번한 축출 | `PVO_CACHE_MAX_MEMORY_SIZE` 증설 |
| `INVALIDATE_COUNT`가 많음 | 테이블 DDL 변경이 잦음 | 스키마 변경 빈도 감소 또는 캐시 크기 여유 확보 |
| `SINGLEFLIGHT_WAIT`가 높음 | 동일 SQL 동시 빌드 경합 | 일시적 현상으로 대부분 자동 해소됨 |

> **주의**: PVO Cache는 Standard Edition 전용 기능입니다. Cluster Edition 환경에서는 이 설정이 적용되지 않습니다.

<a id="tuning-memory-configuration"></a>

## 메모리 설정 튜닝

Machbase 서버의 안정적인 운영을 위해서는 캐시, 처리 공간, OS 예약분을 고려한 전체 메모리 예산 계획이 필요합니다.

### 전체 메모리 배분 원칙

```
전체 물리 메모리 (예: 64GB)
  ├── OS 및 기타 프로세스:  ~20%   (~12.8 GB)
  ├── 캐시 (Result + PVO):  30~40% (~19~25 GB)
  │    ├── RS_CACHE_MAX_MEMORY_SIZE     (예: 8 GB)
  │    └── PVO_CACHE_MAX_MEMORY_SIZE    (예: 256 MB)
  └── Machbase 처리 공간:   나머지
       (정렬·집계 버퍼, 인덱스 빌드, 세션 처리 등)
```

- 캐시 합산이 전체 메모리의 40%를 넘지 않도록 유지합니다.
- 메모리 여유가 충분할 때만 캐시를 늘리고, 인덱스 빌드 등 일시적으로 메모리를 많이 쓰는 작업이 있을 때는 캐시 한도를 보수적으로 설정합니다.

### RS_CACHE_MAX_MEMORY_SIZE 설정

전체 Result Cache가 사용할 수 있는 최대 메모리 크기입니다.

| 항목 | 값 |
|-----|---|
| 최솟값 | 32 KB |
| 최댓값 | 2^64 - 1 바이트 |
| 기본값 | 512 MB |
| 런타임 변경 | 불가 (설정 파일 변경 후 재시작) |

```
# machbase.conf
RS_CACHE_MAX_MEMORY_SIZE = 2147483648
```

### Min-Max Cache 조정

Min-Max Cache는 컬럼의 파티션별 최솟값·최댓값 정보를 메모리에 유지하여, 조회 시 불필요한 파티션을 건너뛰는 파티션 프루닝(pruning)을 가속합니다.

관련 프로퍼티: `DISK_COLUMNAR_TABLE_COLUMN_MINMAX_CACHE_SIZE`

| 항목 | 값 |
|-----|---|
| 기본값 | 104857600 bytes (100 MB) |
| 런타임 변경 | 불가 (서버 재시작 필요) |

이 프로퍼티는 LOG 테이블의 `_ARRIVAL_TIME` 숨김 컬럼에 적용되는 기본 Min-Max Cache 크기입니다. 일반 사용자 컬럼의 `MINMAX_CACHE_SIZE` 기본값은 0이며, 필요한 LOG 컬럼에는 테이블 생성 시 `PROPERTY(MINMAX_CACHE_SIZE = ...)`를 지정하거나 `ALTER TABLE ... MODIFY COLUMN ... SET MINMAX_CACHE_SIZE`로 변경합니다.

| 환경 | 권장 MINMAX_CACHE_SIZE |
|-----|----------------------|
| `_ARRIVAL_TIME` 시간 범위 조회 위주 | 기본값 100 MB 유지 |
| LOG 일반 컬럼 범위 조회 | 컬럼별 100 KB 이상부터 검토 |
| 파티션 수가 많고 특정 컬럼 범위 조회가 잦음 | 컬럼별 1 MB 이상 검토 |

```
# machbase.conf (서버 재시작 필요)
DISK_COLUMNAR_TABLE_COLUMN_MINMAX_CACHE_SIZE = 104857600
```

### PROCESS_MAX_SIZE로 프로세스 메모리 상한 설정

`PROCESS_MAX_SIZE`는 Machbase 서버 프로세스가 사용할 수 있는 최대 메모리 크기를 바이트 단위로 제한합니다. OOM killer 발생 전에 Machbase 스스로 메모리 사용을 억제하는 안전망 역할을 합니다.

```
# machbase.conf
PROCESS_MAX_SIZE = 51539607552   # 48 GB
```

### 메모리 부족 신호 및 진단

| 신호 | 의미 | 조치 |
|-----|------|------|
| OOM killer 로그 (`/var/log/syslog` 또는 `dmesg`) | 메모리 초과로 프로세스 강제 종료 | `PROCESS_MAX_SIZE` 설정, 캐시 한도 축소 |
| `free -h`에서 swap 사용량 급증 | 물리 메모리 부족으로 swap 활용 | 캐시 한도 축소 또는 메모리 증설 |
| `RS_CACHE_MAX_MEMORY_SIZE`에 `CACHE_MEMORY_USAGE`가 근접 | Result Cache 포화 | `RS_CACHE_MAX_MEMORY_SIZE` 증설 또는 캐시 정책 조정 |

```bash
# 현재 메모리 사용 현황 확인
free -h

# swap 사용량 추세 확인
vmstat 5 10
```

```sql
-- Result Cache 메모리 사용량 확인
SELECT
    cache_count,
    cache_memory_usage / 1024 / 1024 AS cache_memory_mb,
    cache_replaced
FROM v$rs_cache_stat;
```

### 설정 변경 순서 권장 사항

1. `free -h` 및 `V$RS_CACHE_STAT`으로 현재 상태 파악
2. 필요한 캐시 크기 계산 후 `machbase.conf`의 `RS_CACHE_MAX_MEMORY_SIZE` 조정 및 서버 재시작
3. Min-Max Cache 조정이 필요하면 `machbase.conf` 수정 후 서버 재시작
4. 변경 후 일정 시간 모니터링하여 `CACHE_REPLACED`, swap 사용량 등 재확인
