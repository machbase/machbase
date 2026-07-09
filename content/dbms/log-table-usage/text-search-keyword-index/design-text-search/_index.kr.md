---
type: docs
title: '전문 검색 설계'
weight: 40
---

LOG 테이블의 `TEXT` 타입 컬럼은 전문 검색(full-text search)을 지원합니다. `SEARCH` 연산자를 사용하여 특정 단어나 패턴을 포함하는 레코드를 빠르게 찾을 수 있습니다.

## TEXT 컬럼 사용

```sql
CREATE TABLE app_log (
    event_time  DATETIME,
    level       VARCHAR(8),
    message     TEXT        -- 전문 검색 대상
);

CREATE KEYWORD INDEX idx_app_log_msg ON app_log(message);
```

## 전문 검색 쿼리

```sql
-- 'error' 단어를 포함하는 로그 조회
SELECT _arrival_time, level, message
FROM app_log
WHERE message SEARCH 'error';

-- 여러 단어 AND 조건
SELECT _arrival_time, message
FROM app_log
WHERE message SEARCH 'connection refused';

-- _arrival_time 범위와 함께 사용
SELECT _arrival_time, message
FROM app_log
WHERE _arrival_time >= '2024-01-01 00:00:00'
  AND message SEARCH 'timeout';
```

## LIKE와의 차이

| 방식 | 인덱스 | 특성 |
|------|--------|------|
| `LIKE '%keyword%'` | 미사용 (풀스캔) | 단순 문자열 매칭 |
| `col SEARCH 'keyword'` | 역인덱스 사용 | 단어 단위 검색, 고성능 |

## 주의사항

- `TEXT` 컬럼은 최대 64MB 저장 가능합니다.
- 영문 기준 단어 분리(공백, 구두점)를 기반으로 역인덱스를 구성합니다.
- 매우 긴 텍스트는 `VARCHAR(n)` 대신 `TEXT`를 사용합니다.
- `TEXT` 컬럼에는 정렬(`ORDER BY`)이나 집계(`GROUP BY`)를 적용하지 않는 것을 권장합니다.
