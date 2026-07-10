---
type: docs
title: '17.3.4 V$RS_CACHE_* 사전'
weight: 40
toc: true
---

Result Cache 관련 가상 테이블은 쿼리 결과를 캐시하는 기능의 상태와 통계를 제공합니다. `V$RS_CACHE_LIST`와 `V$RS_CACHE_STAT` 두 테이블로 구성됩니다.

## V$RS_CACHE_LIST

현재 캐시에 저장된 쿼리 결과 목록을 표시합니다.

| 컬럼 이름 | 타입 | 설명 |
|----------|------|------|
| `TOUCH_TIME` | DATETIME | 캐시를 마지막으로 사용하거나 생성한 시각 |
| `USER_ID` | INTEGER | 캐시를 생성한 사용자 ID |
| `QUERY` | VARCHAR | 캐시를 만든 쿼리문 |
| `TIME_SPENT` | INTEGER | 결과 생성까지 경과 시간 (밀리초) |
| `RECORD_COUNT` | INTEGER | 결과 레코드 개수 |
| `HIT_COUNT` | INTEGER | 캐시 히트 횟수 |

## V$RS_CACHE_STAT

Result Cache 전체 통계를 표시합니다.

| 컬럼 이름 | 타입 | 설명 |
|----------|------|------|
| `CACHE_COUNT` | INTEGER | 현재 캐시된 쿼리 개수 |
| `CACHE_HIT` | INTEGER | 총 캐시 히트 횟수 |
| `AGGR_HIT` | INTEGER | 집계 결과의 캐시 히트 횟수 |
| `CACHE_REPLACED` | INTEGER | 캐시 교체(만료) 횟수 |
| `CACHE_MEMORY_USAGE` | INTEGER | 캐시 메모리 사용량 (바이트) |

## SQL 예제

```sql
-- Result Cache 전체 통계
SELECT cache_count, cache_hit, aggr_hit,
       cache_replaced, cache_memory_usage
  FROM v$rs_cache_stat;

-- 캐시 히트율 계산
SELECT cache_hit,
       cache_hit + cache_replaced AS total_access,
       cache_hit * 100.0 / NULLIF(cache_hit + cache_replaced, 0) AS hit_ratio
  FROM v$rs_cache_stat;

-- 히트 횟수가 높은 캐시 쿼리 확인
SELECT query, hit_count, record_count, time_spent
  FROM v$rs_cache_list
 ORDER BY hit_count DESC
 LIMIT 10;

-- 최근에 사용된 캐시 확인
SELECT query, touch_time, hit_count
  FROM v$rs_cache_list
 ORDER BY touch_time DESC
 LIMIT 10;

-- 생성 비용이 큰 쿼리 (캐시 효과가 높은 후보)
SELECT query, time_spent, hit_count, record_count
  FROM v$rs_cache_list
 WHERE time_spent > 1000
 ORDER BY time_spent DESC;
```

## 캐시 효과 판단 기준

| 지표 | 설명 | 권고 |
|------|------|------|
| `HIT_COUNT` | 캐시가 재사용된 횟수 | 값이 클수록 캐시 효과가 큼 |
| `TIME_SPENT` | 원래 쿼리 실행 시간 (밀리초) | 값이 클수록 캐시 절감 효과가 큼 |
| `CACHE_REPLACED` | 캐시가 만료·교체된 횟수 | 높으면 캐시 크기 증가 또는 TTL 조정 검토 |

> Result Cache 활성화와 설정은 `machbase.conf`의 `RS_CACHE_ENABLE`, `RS_CACHE_TIME_BOUND_MSEC`, `RS_CACHE_MAX_MEMORY_SIZE` 항목을 참고하십시오.
