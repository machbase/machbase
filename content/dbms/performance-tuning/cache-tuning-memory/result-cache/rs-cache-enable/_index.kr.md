---
type: docs
title: 'RS_CACHE_ENABLE'
weight: 10
---

`RS_CACHE_ENABLE`은 Result Cache 기능 자체를 활성화하거나 비활성화하는 스위치입니다.

## 프로퍼티 정보

| 항목 | 값 |
|-----|---|
| 최솟값 | 0 (비활성) |
| 최댓값 | 1 (활성) |
| 기본값 | 1 (True) |
| 런타임 변경 | 가능 (`ALTER SYSTEM SET`) |

## 설정 방법

### machbase.conf (서버 시작 시 적용)

```
RS_CACHE_ENABLE = 1
```

### ALTER SYSTEM SET (런타임 적용, 재시작 불필요)

```sql
-- Result Cache 활성화
ALTER SYSTEM SET RS_CACHE_ENABLE = 1;

-- Result Cache 비활성화
ALTER SYSTEM SET RS_CACHE_ENABLE = 0;
```

## 사용 지침

기본값은 1(활성)이며, 일반적인 운영 환경에서는 변경할 필요가 없습니다.

**0으로 설정하는 경우**: Result Cache와 관련된 모든 캐시 동작이 즉시 중단됩니다. 이미 저장된 캐시 항목도 더 이상 사용되지 않습니다.

주로 다음 목적으로 일시적으로 비활성화합니다.

- 쿼리 결과가 최신 데이터와 다르게 보이는 문제를 진단할 때
- Result Cache가 성능에 미치는 영향을 A/B 비교 측정할 때
- 메모리 부족 상황에서 즉각적인 메모리 확보가 필요할 때

문제 진단 후에는 `ALTER SYSTEM SET RS_CACHE_ENABLE = 1`로 다시 활성화하십시오.

> **참고**: `RS_CACHE_ENABLE = 0`으로 설정해도 기존 캐시 메모리가 즉시 해제되지 않을 수 있습니다. 캐시 메모리는 LRU 정책에 따라 점진적으로 해제됩니다.
