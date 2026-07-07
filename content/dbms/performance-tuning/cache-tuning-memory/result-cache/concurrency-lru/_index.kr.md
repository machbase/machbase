---
type: docs
title: 'LRU와 동시성'
weight: 50
---

Result Cache는 메모리 한도에 도달했을 때 LRU(Least Recently Used) 정책으로 오래된 캐시 항목을 제거합니다. 고동시성 환경에서 캐시를 안정적으로 운영하려면 LRU 동작과 동시성 특성을 이해해야 합니다.

## LRU 교체 정책

캐시 메모리가 `RS_CACHE_MAX_MEMORY_SIZE` 한도에 도달하면 가장 오랫동안 사용(히트)되지 않은 항목부터 순서대로 제거합니다.

- `V$RS_CACHE_STAT`의 `CACHE_REPLACED` 값이 지속적으로 증가하면 LRU 교체가 빈번하게 발생하고 있다는 신호입니다.
- 교체가 빈발하면 새로 추가된 캐시가 히트되기 전에 제거되는 악순환이 생길 수 있습니다.

**대응**: `RS_CACHE_MAX_MEMORY_SIZE`를 늘리거나, `RS_CACHE_MAX_RECORD_PER_QUERY`를 낮춰 개별 엔트리 크기를 제한합니다.

```sql
-- 교체 횟수 확인
SELECT cache_replaced FROM v$rs_cache_stat;

-- 메모리 한도 증설 예시 (1GB로 설정)
ALTER SYSTEM SET RS_CACHE_MAX_MEMORY_SIZE = 1073741824;
```

## 동시성 처리

Result Cache의 동시성은 Machbase 내부에서 자동으로 관리되므로 별도의 사용자 설정이 필요하지 않습니다.

- 여러 세션이 동시에 동일한 쿼리를 실행하면, 첫 번째 세션이 캐시를 생성하는 동안 나머지 세션도 캐시 결과를 안전하게 공유할 수 있도록 내부 락(lock)이 관리됩니다.
- 캐시 히트가 많을수록 실제 쿼리 실행이 줄어들어 **lock contention**이 감소하고 동시 처리 처리량이 향상됩니다.

## 고동시성 환경 권장 설정

| 상황 | 권장 조치 |
|-----|---------|
| 세션 수가 많고 동일 쿼리 반복 실행 | `RS_CACHE_MAX_MEMORY_SIZE`를 충분히 크게 설정하여 히트율 유지 |
| 짧은 주기로 대시보드 갱신 (초 단위) | `RS_CACHE_TIME_BOUND_MSEC`를 낮춰 더 많은 쿼리를 캐시 대상으로 포함 |
| 세션별로 쿼리가 제각각 (반복 패턴 없음) | Result Cache 의존도를 낮추고 캐시 메모리 상한을 적게 할당 |

## TOUCH_TIME을 통한 활성 캐시 확인

`V$RS_CACHE_LIST`의 `TOUCH_TIME`은 해당 캐시 항목이 마지막으로 사용된 시각입니다. `TOUCH_TIME`이 오래된 항목은 LRU 교체 후보가 됩니다.

```sql
-- 오래 사용되지 않은 캐시 항목 확인
SELECT touch_time, query, hit_count
FROM v$rs_cache_list
ORDER BY touch_time ASC;
```
