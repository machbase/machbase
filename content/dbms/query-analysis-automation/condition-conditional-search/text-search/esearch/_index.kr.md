---
type: docs
title: 'ESEARCH'
weight: 20
---

`ESEARCH`는 KEYWORD 인덱스를 사용하면서 `%` 와일드카드 패턴을 지원하는 확장 검색입니다. 일반 `LIKE`의 단점(인덱스 미사용)을 극복하여 부분 문자열 패턴을 고속으로 검색할 수 있습니다.

## ESEARCH 패턴

```text
col ESEARCH 'pattern%'    -- pattern으로 시작하거나 포함하는 단어
col ESEARCH '%pattern%'   -- pattern을 포함하는 단어
```

`%`는 단어 경계 이상의 범위를 나타냅니다.

## 사전 조건

```sql
-- KEYWORD 인덱스 필요
CREATE KEYWORD INDEX idx_msg ON event_log (message);
```

## 예시

```sql
-- 'bbb'로 시작하는 단어 포함 (bbb1, bbb_test 등)
SELECT * FROM event_log WHERE message ESEARCH 'bbb%';

-- 'cd'가 포함된 단어 (abcd, cdf, bcd/cdf 등)
SELECT * FROM event_log WHERE message ESEARCH '%cd%';

-- 오류 코드 부분 검색
SELECT * FROM event_log WHERE error_code ESEARCH 'ERR-10%';
```

## ESEARCH vs LIKE

| 항목 | ESEARCH | LIKE |
|------|---------|------|
| KEYWORD 인덱스 | 필요 | 불필요 |
| 성능 | 고속 (인덱스 활용) | 느림 (전체 스캔) |
| 패턴 앞 `%` | 지원 (`%pattern`) | 지원 (인덱스 미사용) |
| 대소문자 | 대소문자 구분 | 대소문자 구분 |

> `NOT ESEARCH`는 지원하지 않습니다. 반대 패턴이 필요하면 `NOT SEARCH`나 `NOT LIKE`를 사용하세요.
