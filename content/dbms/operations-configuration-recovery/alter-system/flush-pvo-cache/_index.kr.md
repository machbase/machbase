---
type: docs
title: 'FLUSH PVO_CACHE'
weight: 80
---

```sql
ALTER SYSTEM FLUSH PVO_CACHE;
```

PVO(Partition Value Object) Statement Cache를 초기화합니다.

## PVO 캐시란

PVO Statement Cache는 Machbase Standard 에디션에서 사용하는 글로벌 SQL 실행 계획 캐시입니다. 동일한 SQL 문에 대한 파싱, 검증, 최적화 결과를 캐시하여 반복 실행 시 처리 비용을 줄입니다.

`FLUSH PVO_CACHE`를 실행하면 캐시된 모든 SQL 실행 계획이 제거됩니다. DDL이 성공적으로 실행될 때도 내부적으로 PVO 캐시가 자동으로 플러시됩니다.

> **참고**: PVO 캐시는 Result Cache(`FLUSH RESULT_CACHE`)와 독립적으로 동작합니다.

## PVO 캐시 설정

PVO 캐시 관련 속성은 `ALTER SYSTEM SET`으로 런타임에 조정할 수 있습니다.

| 속성 | 설명 | 재시작 필요 |
|---|---|:---:|
| `PVO_CACHE_ENABLE` | 캐시 활성화 여부 (0/1) | 아니요 |
| `PVO_CACHE_MAX_MEMORY_SIZE` | 캐시 최대 메모리 크기 (바이트) | 아니요 |
| `PVO_CACHE_MAX_PLANS_PER_SQL` | SQL당 최대 저장 실행 계획 수 | 아니요 |
| `PVO_CACHE_MAX_SQL_ENTRIES` | 최대 SQL 엔트리 수 (0=무제한) | 아니요 |
| `PVO_CACHE_SHARD_COUNT` | 캐시 샤드 수 | 예 |

## 사용 예시

```sql
-- PVO 캐시 즉시 초기화
ALTER SYSTEM FLUSH PVO_CACHE;

-- 캐시 비활성화 후 초기화
ALTER SYSTEM SET PVO_CACHE_ENABLE = 0;
ALTER SYSTEM FLUSH PVO_CACHE;

-- 캐시 크기 변경
ALTER SYSTEM SET PVO_CACHE_MAX_MEMORY_SIZE = 268435456;

-- 현재 설정 확인
SELECT name, value FROM v$property WHERE name LIKE 'PVO_CACHE%';
```

## 사용 시점

| 상황 | 설명 |
|---|---|
| 캐시된 실행 계획이 잘못되었을 때 | 테이블 구조 변경 후 오래된 실행 계획을 강제 제거 |
| 메모리 사용량 절감이 필요할 때 | 캐시가 차지하는 메모리를 즉시 해제 |
| 성능 문제 진단 시 | 캐시를 비운 후 재빌드되는 과정에서 실행 계획 문제 확인 |
