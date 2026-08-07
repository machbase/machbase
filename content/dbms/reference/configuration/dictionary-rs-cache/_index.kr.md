---
type: docs
title: '18.2.3 RS Cache 프로퍼티 사전'
weight: 30
toc: true
---

RS(Result Set) Cache는 쿼리 결과를 메모리에 캐시하여 동일하거나 유사한 쿼리의 응답 속도를 높입니다. 시계열 데이터의 집계 쿼리에 특히 효과적입니다.

## 프로퍼티 목록

| 프로퍼티 | 기본값 | 범위 | 동적 변경 | 설명 |
|----------|--------|------|----------|------|
| `RS_CACHE_ENABLE` | 1 | 0~1 | 가능 | RS Cache 활성화 여부. 0=비활성, 1=활성 |
| `RS_CACHE_TIME_BOUND_MSEC` | 1000 | 0~2^64-1 | 가능 | 캐시 저장 최소 실행 시간(ms). 이보다 빨리 완료된 쿼리는 캐시하지 않음 |
| `RS_CACHE_MAX_MEMORY_SIZE` | 536870912 | 32KB~2^64-1 | 가능 | RS Cache 전체 최대 메모리(바이트). 기본 512MB |
| `RS_CACHE_MAX_MEMORY_PER_QUERY` | 16777216 | 1024~2^64-1 | 가능 | 쿼리 1개 결과의 최대 캐시 메모리(바이트). 기본 16MB |
| `RS_CACHE_MAX_RECORD_PER_QUERY` | 10000 | 1~2^64-1 | 가능 | 캐시되는 쿼리 결과의 최대 레코드 수. 배포 샘플은 `50000`으로 설정되어 있을 수 있음 |
| `RS_CACHE_APPROXIMATE_RESULT_ENABLE` | 0 | 0~1 | 가능 | 추측 모드 활성화. 1이면 약간 부정확하지만 매우 빠른 결과 반환 |

## 프로퍼티 상세

### RS_CACHE_ENABLE

결과값 캐시 사용 여부를 설정합니다.

```
RS_CACHE_ENABLE = 1
```

### RS_CACHE_TIME_BOUND_MSEC

이 값보다 짧은 시간에 완료된 쿼리는 캐시에 저장하지 않습니다. 0으로 설정하면 모든 쿼리 결과를 캐시합니다. 빠르게 실행되는 쿼리의 결과까지 캐시하면 메모리 낭비가 될 수 있으므로 적절한 임계값 설정을 권장합니다.

```
RS_CACHE_TIME_BOUND_MSEC = 1000   # 1초 이상 걸린 쿼리만 캐시
```

### RS_CACHE_MAX_MEMORY_SIZE

RS Cache 전체에 할당되는 최대 메모리입니다. 캐시가 이 한도에 도달하면 가장 오래된 캐시 항목부터 제거됩니다.

```
RS_CACHE_MAX_MEMORY_SIZE = 1073741824   # 1GB
```

### RS_CACHE_MAX_MEMORY_PER_QUERY

단일 쿼리 결과가 이 값을 초과하면 해당 쿼리 결과는 캐시에 저장되지 않습니다.

```
RS_CACHE_MAX_MEMORY_PER_QUERY = 33554432   # 32MB
```

### RS_CACHE_MAX_RECORD_PER_QUERY

단일 쿼리 결과의 레코드 수가 이 값을 초과하면 캐시에 저장되지 않습니다. 대용량 결과셋의 무분별한 캐시를 방지합니다.

```
RS_CACHE_MAX_RECORD_PER_QUERY = 50000
```

### RS_CACHE_APPROXIMATE_RESULT_ENABLE

추측 모드를 활성화하면 캐시된 결과를 검증 없이 즉시 반환하므로 응답 속도가 매우 빠르지만 최신 데이터가 반영되지 않을 수 있습니다. 실시간 정확도가 중요하지 않은 대시보드 조회 등에 적합합니다.

```
RS_CACHE_APPROXIMATE_RESULT_ENABLE = 0   # 정확한 결과 (기본값)
```

## 동적 변경

```sql
-- RS Cache 활성화/비활성화
ALTER SYSTEM SET RS_CACHE_ENABLE = 1;

-- 캐시 저장 최소 시간을 2초로 설정
ALTER SYSTEM SET RS_CACHE_TIME_BOUND_MSEC = 2000;

-- 최대 메모리를 1GB로 설정
ALTER SYSTEM SET RS_CACHE_MAX_MEMORY_SIZE = 1073741824;

-- 쿼리당 최대 레코드 수 조정
ALTER SYSTEM SET RS_CACHE_MAX_RECORD_PER_QUERY = 20000;
```

## 캐시 초기화

RS Cache를 강제로 비우려면 다음 명령을 사용합니다.

```sql
ALTER SYSTEM FLUSH RESULT_CACHE;
```

## 캐시 상태 확인

```sql
SELECT name, value
  FROM v$property
 WHERE name LIKE 'RS_CACHE%'
 ORDER BY name;
```

## 권장 설정

| 용도 | RS_CACHE_TIME_BOUND_MSEC | RS_CACHE_MAX_MEMORY_SIZE | RS_CACHE_MAX_RECORD_PER_QUERY |
|------|--------------------------|--------------------------|-------------------------------|
| 실시간 대시보드 | 500 | 512MB | 10000 |
| 집계 보고서 | 2000 | 1GB | 50000 |
| 정확도 우선 | 1000 | 512MB | 10000 (approximate=0) |
