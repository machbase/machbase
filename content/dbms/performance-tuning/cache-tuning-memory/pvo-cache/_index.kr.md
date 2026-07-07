---
type: docs
title: 'PVO Cache 운영 (Standard Edition 중심)'
weight: 20
---

PVO(Partition Value Object) Statement Cache는 SQL 실행 계획(Plan)을 메모리에 캐시하여, 동일한 SQL이 반복 실행될 때 파싱과 최적화 비용을 절감합니다. **Standard Edition에서만 동작**합니다.

## 동작 원리

1. SQL이 처음 실행되면 파싱 및 최적화를 거쳐 실행 계획(Plan)을 생성합니다.
2. 생성된 Plan을 SQL 텍스트를 키로 하여 PVO Cache에 저장합니다.
3. 동일한 SQL이 다시 실행되면 캐시에서 Plan을 재사용하여 파싱·최적화 단계를 건너뜁니다.

파라미터 값이 달라도 SQL 텍스트가 같으면 동일 엔트리로 처리됩니다. (바인드 변수 활용 시 효과가 높음)

## 주요 프로퍼티

| 프로퍼티 | 기본값 | 설명 |
|--------|------|------|
| `PVO_CACHE_ENABLE` | 1 | PVO Cache 활성화 여부 |
| `PVO_CACHE_MAX_MEMORY_SIZE` | 256 MB | 전체 PVO Cache 최대 메모리 크기 (바이트) |
| `PVO_CACHE_MAX_PLANS_PER_SQL` | 512 | SQL당 최대 캐시 플랜 수 |
| `PVO_CACHE_MAX_SQL_ENTRIES` | 0 (무제한) | 캐시 가능한 최대 SQL 엔트리 수 |
| `PVO_CACHE_SHARD_COUNT` | 16 | 캐시 샤드 수 (서버 재시작 필요) |

> **참고**: `PVO_CACHE_SHARD_COUNT`는 초기화 시점에만 적용되며, 변경 시 서버 재시작이 필요합니다. 나머지 프로퍼티는 `ALTER SYSTEM SET`으로 런타임 변경이 가능합니다.

## 설정 방법

### machbase.conf

```
PVO_CACHE_ENABLE          = 1
PVO_CACHE_MAX_MEMORY_SIZE = 268435456
PVO_CACHE_MAX_PLANS_PER_SQL = 512
PVO_CACHE_MAX_SQL_ENTRIES = 0
PVO_CACHE_SHARD_COUNT     = 16
```

### ALTER SYSTEM SET

```sql
-- PVO Cache 메모리 한도를 512MB로 증설
ALTER SYSTEM SET PVO_CACHE_MAX_MEMORY_SIZE = 536870912;

-- SQL당 최대 플랜 수 조정
ALTER SYSTEM SET PVO_CACHE_MAX_PLANS_PER_SQL = 256;
```

## V$PVO_CACHE_STAT으로 상태 확인

```sql
SELECT * FROM v$pvo_cache_stat;
```

| 컬럼 이름 | 설명 |
|---------|------|
| CACHE_ENTRY_COUNT | 캐시에 적재된 SQL 엔트리 수 |
| CACHE_HANDLE_COUNT | 캐시된 플랜(핸들) 총 수 |
| CACHE_MEMORY_USAGE | 현재 사용 중인 캐시 메모리 크기 |
| CACHE_MAX_MEMORY_SIZE | 설정된 캐시 메모리 한도 |
| CACHE_HIT | 캐시 히트 횟수 |
| CACHE_MISS | 캐시 미스 횟수 |
| BUILD_COUNT | 플랜 빌드 시도 횟수 |
| INVALIDATE_COUNT | 무효화된 플랜 수 |
| EVICT_COUNT | 메모리 한도 초과로 캐시 축출된 횟수 |

## V$PVO_CACHE_LIST로 SQL별 상세 확인

```sql
-- 히트 횟수가 많은 SQL Top 10
SELECT touch_time, query, hit_count, handle_count
FROM v$pvo_cache_list
ORDER BY hit_count DESC
LIMIT 10;
```

## 튜닝 가이드

| 증상 | 원인 | 조치 |
|-----|------|------|
| `CACHE_MISS`가 많고 `CACHE_HIT`가 낮음 | 쿼리 다양성이 높거나 캐시 공간 부족 | `PVO_CACHE_MAX_MEMORY_SIZE` 증설, `PVO_CACHE_MAX_SQL_ENTRIES` 확인 |
| `EVICT_COUNT`가 지속 증가 | 메모리 한도 부족으로 빈번한 축출 | `PVO_CACHE_MAX_MEMORY_SIZE` 증설 |
| `INVALIDATE_COUNT`가 많음 | 테이블 DDL 변경이 잦음 | 스키마 변경 빈도 감소 또는 캐시 크기 여유 확보 |
| `SINGLEFLIGHT_WAIT`가 높음 | 동일 SQL 동시 빌드 경합 | 일시적 현상으로 대부분 자동 해소됨 |

> **주의**: PVO Cache는 Standard Edition 전용 기능입니다. Cluster Edition 환경에서는 이 설정이 적용되지 않습니다.
