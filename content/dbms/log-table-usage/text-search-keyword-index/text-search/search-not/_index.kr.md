---
type: docs
title: '7.11.1.1 SEARCH / NOT SEARCH'
weight: 10
---

`SEARCH`는 KEYWORD 인덱스가 생성된 VARCHAR/TEXT 컬럼에서 키워드 단어를 고속으로 검색합니다.

## 사전 조건: KEYWORD 인덱스

```sql
-- KEYWORD 인덱스 생성
CREATE KEYWORD INDEX idx_msg ON event_log (message);
CREATE KEYWORD INDEX idx_id2 ON sensor_log (sensor_type);
```

## SEARCH

```sql
-- 'timeout' 단어가 포함된 로그
SELECT * FROM event_log WHERE message SEARCH 'timeout';

-- 복수 컬럼 SEARCH 조합
SELECT * FROM event_log
WHERE message SEARCH 'error' AND category SEARCH 'network';
```

## NOT SEARCH

SEARCH 결과가 아닌 레코드를 반환합니다.

```sql
-- 'timeout'이 포함되지 않은 로그
SELECT * FROM event_log WHERE message NOT SEARCH 'timeout';
```

## SEARCH vs LIKE

| 항목 | SEARCH | LIKE |
|------|--------|------|
| 인덱스 | KEYWORD 인덱스 필요 | 불필요 (인덱스 미사용) |
| 단어 단위 | O (공백·특수문자로 분리된 단어) | X (패턴 매칭) |
| 성능 | 고속 (인덱스 활용) | 느림 (전체 스캔) |
| 용도 | 영문·숫자 단어 단위 검색 | 부분 문자열 패턴 |

**팁**: 대용량 VARCHAR/TEXT 컬럼의 키워드 검색에는 반드시 KEYWORD 인덱스를 생성하고 SEARCH를 사용하세요. LIKE는 인덱스를 활용하지 못해 전체 스캔이 발생합니다.
