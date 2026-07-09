---
type: docs
title: '12.6.1.1 RS_CACHE_ENABLE'
weight: 10
---

`RS_CACHE_ENABLE`은 Result Cache 기능 자체를 활성화하거나 비활성화하는 스위치입니다.

## 프로퍼티 정보

| 항목 | 값 |
|-----|---|
| 최솟값 | 0 (비활성) |
| 최댓값 | 1 (활성) |
| 기본값 | 1 (True) |
| 런타임 변경 | 세션 단위 가능 (`ALTER SESSION SET`) |

## 설정 방법

### machbase.conf (서버 시작 시 적용)

```
RS_CACHE_ENABLE = 1
```

### ALTER SESSION SET (현재 세션 적용)

```sql
-- Result Cache 활성화
ALTER SESSION SET RS_CACHE_ENABLE = 1;

-- Result Cache 비활성화
ALTER SESSION SET RS_CACHE_ENABLE = 0;
```

## 사용 지침

기본값은 1(활성)이며, 일반적인 운영 환경에서는 변경할 필요가 없습니다.

**0으로 설정하는 경우**: 현재 세션에서 Result Cache 사용이 중단됩니다. 이미 저장된 전역 캐시 엔트리가 즉시 삭제되는 것은 아닙니다.

주로 다음 목적으로 일시적으로 비활성화합니다.

- 쿼리 결과가 최신 데이터와 다르게 보이는 문제를 진단할 때
- Result Cache가 성능에 미치는 영향을 A/B 비교 측정할 때
- 특정 세션에서 Result Cache 영향을 배제하고 비교 측정할 때

문제 진단 후에는 `ALTER SESSION SET RS_CACHE_ENABLE = 1`로 다시 활성화하십시오.

> **참고**: 기존 캐시 엔트리를 명시적으로 제거해야 하면 `ALTER SYSTEM FLUSH RESULT_CACHE`를 사용합니다.
