---
title: '7.11 텍스트 검색과 KEYWORD 인덱스'
weight: 110
toc: true
---

<a id="text-search"></a>
<a id="original-85-text-search"></a>

## 텍스트 검색

KEYWORD 인덱스를 활용하면 VARCHAR/TEXT 컬럼에서 단어 기반 텍스트 검색을 수행할 수 있습니다.

### 이 절에서 다루는 내용

- **[SEARCH / NOT SEARCH](/dbms/log-table-usage/text-search-keyword-index/#search-not)**: 키워드 인덱스 기반 단어 검색
- **[ESEARCH](/dbms/log-table-usage/text-search-keyword-index/#esearch)**: 패턴(%) 확장 검색
- **[LIKE / NOT LIKE](/dbms/log-table-usage/text-search-keyword-index/#like-not)**: 일반 패턴 매칭

<a id="search-not"></a>
<a id="text-search-search-not"></a>

### SEARCH / NOT SEARCH

`SEARCH`는 KEYWORD 인덱스가 생성된 VARCHAR/TEXT 컬럼에서 키워드 단어를 고속으로 검색합니다.

#### 사전 조건: KEYWORD 인덱스

```sql
-- KEYWORD 인덱스 생성
CREATE KEYWORD INDEX idx_msg ON event_log (message);
CREATE KEYWORD INDEX idx_id2 ON sensor_log (sensor_type);
```

#### SEARCH

```sql
-- 'timeout' 단어가 포함된 로그
SELECT * FROM event_log WHERE message SEARCH 'timeout';

-- 복수 컬럼 SEARCH 조합
SELECT * FROM event_log
WHERE message SEARCH 'error' AND category SEARCH 'network';
```

#### NOT SEARCH

SEARCH 결과가 아닌 레코드를 반환합니다.

```sql
-- 'timeout'이 포함되지 않은 로그
SELECT * FROM event_log WHERE message NOT SEARCH 'timeout';
```

#### SEARCH vs LIKE

| 항목 | SEARCH | LIKE |
|------|--------|------|
| 인덱스 | KEYWORD 인덱스 필요 | 불필요 (인덱스 미사용) |
| 단어 단위 | O (공백·특수문자로 분리된 단어) | X (패턴 매칭) |
| 성능 | 고속 (인덱스 활용) | 느림 (전체 스캔) |
| 용도 | 영문·숫자 단어 단위 검색 | 부분 문자열 패턴 |

반복적인 단어 검색에는 KEYWORD 인덱스와 SEARCH를 사용합니다. LIKE는 KEYWORD 인덱스를
사용하지 않으므로 시간 조건 등으로 검색 범위를 먼저 줄입니다.

#### 다국어 검색

KEYWORD 인덱스는 UTF-8 문자열을 검색할 수 있습니다. 공백으로 단어 경계가 명확하지 않은
한국어와 일본어 문자열은 2-gram 단위로 색인되므로 연속된 문자열 일부를 SEARCH 조건으로
지정할 수 있습니다. 실제 분리 결과는 대표 데이터로 확인합니다.

<a id="text-search-esearch"></a>

### ESEARCH

`ESEARCH`는 KEYWORD 인덱스를 사용하면서 `%` 와일드카드 패턴까지 지원하는 확장 검색입니다. `LIKE`와 달리 인덱스를 활용하므로 부분 문자열 패턴도 빠르게 검색됩니다.

#### ESEARCH 패턴

```text
col ESEARCH 'pattern%'    -- pattern으로 시작하거나 포함하는 단어
col ESEARCH '%pattern%'   -- pattern을 포함하는 단어
```

`%`는 단어 경계 이상의 범위를 나타냅니다.

#### 사전 조건

```sql
-- KEYWORD 인덱스 필요
CREATE KEYWORD INDEX idx_msg ON event_log (message);
```

#### 예시

```sql
-- 'bbb'로 시작하는 단어 포함 (bbb1, bbb_test 등)
SELECT * FROM event_log WHERE message ESEARCH 'bbb%';

-- 'cd'가 포함된 단어 (abcd, cdf, bcd/cdf 등)
SELECT * FROM event_log WHERE message ESEARCH '%cd%';

-- 오류 코드 부분 검색
SELECT * FROM event_log WHERE error_code ESEARCH 'ERR-10%';
```

#### ESEARCH vs LIKE

| 항목 | ESEARCH | LIKE |
|------|---------|------|
| KEYWORD 인덱스 | 필요 | 불필요 |
| 성능 | 고속 (인덱스 활용) | 느림 (전체 스캔) |
| 패턴 앞 `%` | 지원 (`%pattern`) | 지원 (인덱스 미사용) |
| 대소문자 | 대소문자 구분 | 대소문자 구분 |

> `NOT ESEARCH`는 지원하지 않습니다. 반대 패턴이 필요하면 `NOT SEARCH`나 `NOT LIKE`를 사용하십시오.

<a id="like-not"></a>
<a id="text-search-like-not"></a>

### LIKE / NOT LIKE

`LIKE`는 SQL 표준 패턴 매칭 연산자입니다. 인덱스를 사용하지 않으므로 대용량 테이블에서는 성능에 주의합니다.

#### 패턴 문자

| 문자 | 의미 |
|------|------|
| `%` | 0개 이상의 임의 문자 |
| `_` | 정확히 1개의 임의 문자 |

#### 예시

```sql
-- 'TEMP'로 시작하는 sensor_id
SELECT * FROM sensor_log WHERE sensor_id LIKE 'TEMP%';

-- '-01'로 끝나는 sensor_id
SELECT * FROM sensor_log WHERE sensor_id LIKE '%-01';

-- 중간에 'ERR' 포함
SELECT * FROM event_log WHERE message LIKE '%ERR%';

-- 4자리 코드 패턴 (___)
SELECT * FROM sensor_log WHERE code LIKE 'T___';
```

#### NOT LIKE

```sql
-- 'TEMP'로 시작하지 않는 센서
SELECT * FROM sensor_log WHERE sensor_id NOT LIKE 'TEMP%';
```

#### 성능 고려사항

- `LIKE '%pattern'` 또는 `LIKE '%pattern%'`처럼 앞에 `%`가 오면 인덱스를 사용할 수 없어 전체 스캔이 발생합니다.
- 대용량 LOG/TAG 테이블의 VARCHAR 컬럼에 자주 검색한다면 KEYWORD 인덱스를 생성하고 `SEARCH` 또는 `ESEARCH`를 사용하는 것이 성능상 유리합니다.


<a id="design-text-search"></a>

## 전문 검색 설계

`TEXT` 타입 컬럼에 KEYWORD 인덱스를 생성하면 `SEARCH` 연산자로 전문 검색(full-text search)을 수행할 수 있습니다.

### TEXT 컬럼 사용

```sql
CREATE TABLE app_log (
    event_time  DATETIME,
    level       VARCHAR(8),
    message     TEXT        -- 전문 검색 대상
);

CREATE KEYWORD INDEX idx_app_log_msg ON app_log(message);
```

### 전문 검색 쿼리

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

### LIKE와의 차이

| 방식 | 인덱스 | 특성 |
|------|--------|------|
| `LIKE '%keyword%'` | 미사용 (풀스캔) | 단순 문자열 매칭 |
| `col SEARCH 'keyword'` | 역인덱스 사용 | 단어 단위 검색, 고성능 |

### 주의사항

- `TEXT` 컬럼은 최대 64MB 저장 가능합니다.
- 영문 기준 단어 분리(공백, 구두점)를 기반으로 역인덱스를 구성합니다.
- 매우 긴 텍스트는 `VARCHAR(n)` 대신 `TEXT`를 사용합니다.
- `TEXT` 컬럼에는 정렬(`ORDER BY`)이나 집계(`GROUP BY`)를 적용하지 않는 것을 권장합니다.
