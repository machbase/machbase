---
type: docs
title: '13.3.7 FLUSH RESULT_CACHE'
weight: 70
---

```sql
ALTER SYSTEM FLUSH RESULT_CACHE;
```

Result Cache(쿼리 결과 캐시)에 저장된 모든 캐시 항목을 초기화합니다.

## Result Cache란

Machbase의 Result Cache는 자주 실행되는 SELECT 쿼리의 결과를 메모리에 저장하여, 동일한 쿼리가 다시 요청될 때 실제 연산 없이 캐시된 결과를 반환하는 기능입니다. Result Cache 사용 여부는 세션 단위(`ALTER SESSION SET RS_CACHE_ENABLE`)로 제어할 수 있습니다.

`FLUSH RESULT_CACHE`를 실행하면 모든 세션에 걸쳐 캐시된 결과가 즉시 삭제됩니다.

## 사용 시점

| 상황 | 설명 |
|---|---|
| 데이터 변경 후 캐시 불일치 | 대량 INSERT/DELETE 후 캐시된 결과가 최신 데이터를 반영하지 않을 때 |
| 메모리 확보 | Result Cache가 차지하는 메모리를 즉시 해제해야 할 때 |
| 캐시 동작 테스트 | 캐시를 초기화하고 히트율 등 동작을 새로 측정할 때 |

## 사용 예시

```sql
-- Result Cache 전체 초기화
ALTER SYSTEM FLUSH RESULT_CACHE;

-- 세션별 Result Cache 제어 (비활성화)
ALTER SESSION SET RS_CACHE_ENABLE = 0;

-- 캐시 상태 확인
SELECT name, value FROM v$property WHERE name LIKE '%CACHE%';
```

## 관련 세션 설정

| 속성 | 설명 |
|---|---|
| `RS_CACHE_ENABLE` | 세션의 Result Cache 사용 여부 (0=비활성, 1=활성) |
| `RS_CACHE_TIME_BOUND_MSEC` | 캐시 저장 기준 실행 시간 (밀리초, 0이면 모든 쿼리 결과 저장 대상) |
| `RS_CACHE_MAX_MEMORY_PER_QUERY` | 쿼리당 최대 캐시 메모리 |
| `RS_CACHE_MAX_RECORD_PER_QUERY` | 쿼리당 최대 캐시 레코드 수 |
