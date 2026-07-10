---
title: '5.14 TAG cache와 운영 튜닝'
weight: 140
toc: true
---

TAG 테이블의 메타데이터 캐시를 관리하고 크기를 조정하는 방법을 다룬다.

<a id="flush-tag-cache"></a>

## FLUSH TAG_CACHE

```sql
ALTER SYSTEM FLUSH TAG_CACHE;
```

TAG 테이블의 메타데이터 캐시를 초기화합니다.

### TAG 캐시란

TAG 테이블의 태그 이름, 메타데이터 컬럼 값 등은 메모리에 캐시되어 조회 성능을 높인다. 태그 수가 많을수록 캐시 효과가 크며, `TAG_CACHE_MAX_MEMORY_SIZE` 파라미터로 크기를 제어한다.

`FLUSH TAG_CACHE`를 실행하면 현재 캐시된 TAG 메타데이터가 모두 비워지고, 이후 조회 시 캐시가 다시 채워진다.

### 사용 시점

| 상황 | 설명 |
|---|---|
| TAG 메타데이터 변경 후 즉시 반영 | `UPDATE TAG METADATA` 후 캐시된 구 메타데이터를 제거 |
| 캐시 관련 문제 진단 | 캐시를 비운 후 재빌드 과정에서 메타데이터 정합성 확인 |
| 메모리 해제 | TAG 캐시가 차지하는 메모리를 즉시 반환 |

### 사용 예시

```sql
-- TAG 메타데이터 변경 후 캐시 초기화
UPDATE TAG METADATA SET tag_name = 'SENSOR_NEW' WHERE tag_name = 'SENSOR_OLD';
ALTER SYSTEM FLUSH TAG_CACHE;

-- 변경된 메타데이터로 조회
SELECT * FROM tag WHERE name = 'SENSOR_NEW' LIMIT 10;
```

### TAG 캐시 크기 설정

```sql
-- 현재 TAG 캐시 크기 확인
SELECT name, value FROM v$property WHERE name = 'TAG_CACHE_MAX_MEMORY_SIZE';

-- 런타임에 TAG 캐시 크기 변경
ALTER SYSTEM SET TAG_CACHE_MAX_MEMORY_SIZE = 536870912;
```
