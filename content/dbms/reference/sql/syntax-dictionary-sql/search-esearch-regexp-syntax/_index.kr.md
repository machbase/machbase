---
type: docs
title: 'SEARCH / ESEARCH / REGEXP syntax'
weight: 30
---

Machbase는 텍스트 데이터 검색을 위해 `SEARCH`, `ESEARCH`, `REGEXP` 세 가지 WHERE 절 연산자를 제공합니다. `SEARCH`와 `ESEARCH`는 KEYWORD 인덱스를 활용해 빠른 검색을 수행하고, `REGEXP`는 정규 표현식 기반의 패턴 매칭을 지원합니다.

## SEARCH

KEYWORD 인덱스가 생성된 VARCHAR 또는 TEXT 컬럼에서 단어 단위 검색을 수행합니다.

```sql
column_name SEARCH 'search_term'
column_name NOT SEARCH 'search_term'
```

- KEYWORD 인덱스가 반드시 존재해야 합니다.
- 단어(토큰) 단위로 검색하며, AND 연산으로 여러 조건을 조합할 수 있습니다.

```sql
CREATE TABLE app_log (id INTEGER, message VARCHAR(200), detail VARCHAR(200));
CREATE KEYWORD INDEX idx_msg    ON app_log (message);
CREATE KEYWORD INDEX idx_detail ON app_log (detail);

INSERT INTO app_log VALUES (1, 'error timeout occurred', 'connection reset');
INSERT INTO app_log VALUES (2, 'info service started', 'port 8080');

-- 단일 단어 검색
SELECT * FROM app_log WHERE message SEARCH 'error';

-- 다중 단어 검색 (AND)
SELECT * FROM app_log WHERE message SEARCH 'error' AND message SEARCH 'timeout';

-- 여러 컬럼 동시 검색
SELECT * FROM app_log WHERE message SEARCH 'error' AND detail SEARCH 'reset';

-- NOT SEARCH: 해당 단어가 없는 행 반환
SELECT * FROM app_log WHERE message NOT SEARCH 'error';
```

## ESEARCH

KEYWORD 인덱스를 활용하면서 `%` 와일드카드 패턴으로 부분 문자열을 검색합니다. `LIKE`의 단점(`%` 앞 전체 스캔)을 보완합니다.

```sql
column_name ESEARCH 'pattern%'
column_name ESEARCH '%pattern%'
```

- `%`는 임의의 문자열과 매칭됩니다.
- `NOT ESEARCH`는 지원하지 않습니다.

```sql
CREATE TABLE realdual (id1 INTEGER, id2 VARCHAR(20), id3 VARCHAR(20));
CREATE KEYWORD INDEX idx_id2 ON realdual (id2);
CREATE KEYWORD INDEX idx_id3 ON realdual (id3);

INSERT INTO realdual VALUES (1, 'aaa bbb1', 'cdf def1');
INSERT INTO realdual VALUES (2, 'bbb ccc1', 'bcd cdf1');
INSERT INTO realdual VALUES (3, 'abc bbb2', 'abc bcd1');

-- 'bbb'로 시작하는 단어가 있는 행 검색
SELECT id2 FROM realdual WHERE id2 ESEARCH 'bbb%';

-- 'cd'를 포함하는 단어가 있는 행 검색
SELECT id3 FROM realdual WHERE id3 ESEARCH '%cd%';
```

## REGEXP

정규 표현식 패턴으로 데이터를 검색합니다. KEYWORD 인덱스를 사용하지 않으므로 인덱스 조건과 함께 사용해 검색 범위를 줄이는 것이 좋습니다.

```sql
column_name REGEXP 'pattern'
column_name NOT REGEXP 'pattern'
```

- 인덱스가 적용되지 않으므로, 전체 스캔이 발생할 수 있습니다.
- 먼저 `SEARCH`나 `ESEARCH`로 범위를 좁힌 후 `REGEXP`를 적용하면 효율적입니다.

```sql
CREATE TABLE realdual (id1 INTEGER, id2 VARCHAR(20), id3 VARCHAR(20));

INSERT INTO realdual VALUES (1, 'time1', 'series1 series21');
INSERT INTO realdual VALUES (2, 'time2', 'series2 series22');
INSERT INTO realdual VALUES (3, 'time3', 'series3 series32');

-- 단순 패턴 매칭
SELECT * FROM realdual WHERE id2 REGEXP 'time';

-- 문자 클래스 사용
SELECT * FROM realdual WHERE id2 REGEXP 'time[12]';

-- 부정 매칭
SELECT * FROM realdual WHERE id2 NOT REGEXP 'time[12]';

-- 복합 조건: SEARCH로 범위를 줄이고 REGEXP로 정밀 검색
SELECT * FROM app_log
 WHERE message SEARCH 'error'
   AND message REGEXP '^ERROR:.*timeout';
```

### 함수 형태 REGEXP

스칼라 표현식에서 REGEXP를 함수처럼 사용할 수 있습니다. 일치하면 1, 불일치하면 0을 반환합니다.

```sql
SELECT 'abcde' REGEXP 'a[bcd]{1,10}e' FROM dual;
-- 결과: 1
```

## 성능 권장사항

| 상황 | 권장 연산자 |
|------|-------------|
| 정확한 단어 검색 | `SEARCH` |
| 단어 접두사/내부 패턴 검색 | `ESEARCH` |
| 복잡한 정규식 패턴 검색 | `SEARCH` 또는 `ESEARCH` 선행 후 `REGEXP` 추가 |

## 관련 문서

- [INDEX syntax](../index-syntax/) — KEYWORD 인덱스 생성
