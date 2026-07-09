---
type: docs
title: '12.6.1.2 RS_CACHE_TIME_BOUND_MSEC'
weight: 20
---

`RS_CACHE_TIME_BOUND_MSEC`는 Result Cache에 저장할 쿼리의 최소 실행 시간(밀리초)을 지정합니다. 실행 시간이 이 값보다 짧은 쿼리는 캐시하지 않습니다.

## 프로퍼티 정보

| 항목 | 값 |
|-----|---|
| 최솟값 | 0 |
| 최댓값 | 2^64 - 1 (ms) |
| 기본값 | 1000 (1초) |
| 런타임 변경 | 세션 단위 가능 (`ALTER SESSION SET`) |

## 설정 방법

### machbase.conf

```
RS_CACHE_TIME_BOUND_MSEC = 1000
```

### ALTER SESSION SET

```sql
-- 500ms 이상 걸린 쿼리만 캐시
ALTER SESSION SET RS_CACHE_TIME_BOUND_MSEC = 500;

-- 모든 쿼리 결과를 캐시 (0 = 제한 없음)
ALTER SESSION SET RS_CACHE_TIME_BOUND_MSEC = 0;
```

## 동작 원리

빠르게 완료되는 쿼리는 캐시에 저장하고 조회하는 비용이 실제 쿼리를 다시 실행하는 비용보다 클 수 있습니다. 이 임곗값을 두어 캐시 대상을 "비용이 큰 쿼리"로 제한함으로써 캐시 메모리를 효율적으로 사용합니다.

- **기본값 1000ms**: 1초 이상 걸리는 쿼리만 캐시 대상이 됩니다. 대부분의 집계 쿼리 환경에 적합한 출발점입니다.
- **0으로 설정**: 실행 시간에 관계없이 모든 쿼리 결과를 캐시합니다. 캐시 항목이 급증하여 메모리 사용량이 늘어날 수 있습니다.

## 튜닝 가이드

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
