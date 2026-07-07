---
type: docs
title: 'V$RS_CACHE_* 확인'
weight: 40
---

Machbase는 Result Cache의 상태를 조회할 수 있는 두 가지 가상 테이블을 제공합니다.

## V$RS_CACHE_LIST

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

## V$RS_CACHE_STAT

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

## 히트율 해석 및 조치

`V$RS_CACHE_STAT`에는 캐시 미스 컬럼이 없으므로 이 뷰만으로 정확한 히트율을 계산할 수 없습니다. `CACHE_HIT` 증가 추세, `CACHE_COUNT`, `CACHE_REPLACED`, 애플리케이션의 전체 쿼리 실행 횟수를 함께 보며 효율을 판단합니다.

| 증상 | 원인 | 조치 |
|-----|------|------|
| `CACHE_HIT`가 낮고 `CACHE_COUNT`도 적음 | `RS_CACHE_TIME_BOUND_MSEC`가 너무 높아 캐시 대상 쿼리 부족 | `TIME_BOUND_MSEC` 값을 낮추어 더 많은 쿼리를 캐시 대상으로 포함 |
| `CACHE_HIT`가 낮고 `CACHE_COUNT`는 많음 | 쿼리 패턴 다양 (반복 실행 쿼리가 적음) | Result Cache 의존도를 낮추고 인덱스·모델링 튜닝 검토 |
| `CACHE_REPLACED`가 지속 증가 | 캐시 메모리 한도 부족으로 LRU 교체 빈발 | `RS_CACHE_MAX_MEMORY_SIZE` 증설 또는 `RS_CACHE_MAX_RECORD_PER_QUERY` 축소 |
| `CACHE_MEMORY_USAGE`가 `RS_CACHE_MAX_MEMORY_SIZE`에 근접 | 캐시 포화 상태 | `RS_CACHE_MAX_MEMORY_SIZE` 증설 검토 |

## 모니터링 예시

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
