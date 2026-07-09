---
type: docs
title: '13.3.10 FLUSH PAGE_CACHE'
weight: 100
---

```sql
ALTER SYSTEM FLUSH PAGE_CACHE;
```

Machbase가 관리하는 페이지 캐시를 강제로 비웁니다.

## 동작 설명

Machbase는 자주 접근하는 데이터 페이지를 메모리에 캐시하여 디스크 I/O를 줄입니다. 이 페이지 캐시는 서버 성능 향상을 위해 자동으로 관리되지만, 다음과 같은 상황에서 수동으로 비워야 할 때 `FLUSH PAGE_CACHE`를 사용합니다.

- 메모리 사용량이 급격히 증가했을 때 캐시를 해제하여 메모리 여유 확보
- 성능 벤치마크나 테스트에서 캐시 효과를 배제한 순수 디스크 I/O 성능 측정
- 캐시 관련 동작을 진단하기 위해 초기 상태로 리셋

> **주의**: 캐시를 비운 직후에는 데이터 페이지를 다시 디스크에서 읽어야 하므로, 잠시 쿼리 응답 시간이 느려질 수 있습니다.

## 사용 예시

```sql
-- 페이지 캐시 강제 초기화
ALTER SYSTEM FLUSH PAGE_CACHE;

-- 이후 쿼리는 캐시 없이 디스크에서 직접 읽음
SELECT COUNT(*) FROM log_table;
```

## 관련 설정

페이지 캐시 크기는 `DISK_COLUMNAR_PAGE_CACHE_MAX_SIZE` 파라미터로 제어합니다.

```sql
-- 현재 설정 확인
SELECT name, value FROM v$property WHERE name = 'DISK_COLUMNAR_PAGE_CACHE_MAX_SIZE';

-- 런타임에 크기 변경 (재시작 불필요)
ALTER SYSTEM SET DISK_COLUMNAR_PAGE_CACHE_MAX_SIZE = 536870912;
```
