---
type: docs
title: 'RS_CACHE_MAX_RECORD_PER_QUERY'
weight: 30
---

`RS_CACHE_MAX_RECORD_PER_QUERY`는 Result Cache에 저장할 수 있는 쿼리 결과의 최대 레코드 수를 지정합니다. 결과 레코드 수가 이 값 이상이면 해당 쿼리는 캐시되지 않습니다.

## 프로퍼티 정보

| 항목 | 값 |
|-----|---|
| 최솟값 | 1 |
| 최댓값 | 2^64 - 1 |
| 기본값 | 50000 |
| 런타임 변경 | 가능 (`ALTER SYSTEM SET`) |

## 설정 방법

### machbase.conf

```
RS_CACHE_MAX_RECORD_PER_QUERY = 50000
```

### ALTER SYSTEM SET

```sql
-- 결과 1,000건 이하 쿼리만 캐시
ALTER SYSTEM SET RS_CACHE_MAX_RECORD_PER_QUERY = 1000;

-- 결과 50,000건 이하 쿼리까지 캐시
ALTER SYSTEM SET RS_CACHE_MAX_RECORD_PER_QUERY = 50000;
```

## 동작 원리

대용량 결과셋을 캐시하면 그만큼 많은 메모리가 소비되어 다른 쿼리의 캐시 공간을 잠식합니다. 이 상한을 통해 개별 쿼리가 캐시 메모리를 독점하는 것을 방지합니다.

레코드 수 제한과 함께 `RS_CACHE_MAX_MEMORY_PER_QUERY`(쿼리당 최대 캐시 메모리, 기본 16MB)도 함께 적용됩니다. 두 조건 중 하나라도 초과하면 해당 쿼리는 캐시되지 않습니다.

## 워크로드별 권장 설정

| 워크로드 | 권장 설정 | 이유 |
|---------|---------|------|
| 대시보드용 집계 (수십~수백 건 반환) | 기본값 50000으로 충분 | 결과셋이 작아 메모리 부담 없음 |
| 롤업 테이블 조회 (수천 건) | 10000~50000 | 적절한 메모리 사용 |
| 원시 데이터 대량 조회 (수만 건 이상) | 캐시 대상에서 제외 권장 | 메모리 낭비, LRU 교체 빈발 |

## 튜닝 가이드

현재 캐시된 쿼리의 레코드 수 분포를 확인합니다.

```sql
SELECT query, record_count, hit_count
FROM v$rs_cache_list
ORDER BY record_count DESC;
```

- 레코드 수가 많은 쿼리가 캐시를 점유하고 있다면 `RS_CACHE_MAX_RECORD_PER_QUERY`를 낮춰 해당 쿼리를 캐시 대상에서 제외합니다.
- 캐시 히트율이 낮고 `CACHE_REPLACED` 횟수가 많으면 `RS_CACHE_MAX_MEMORY_SIZE`를 늘리거나 `RS_CACHE_MAX_RECORD_PER_QUERY`를 줄여 캐시 용량을 확보합니다.
