---
title: '7.11 텍스트 검색과 KEYWORD 인덱스'
weight: 110
toc: true
---
텍스트 검색과 KEYWORD 인덱스에 해당하는 세부 문서를 모았습니다.


<a id="text-search"></a>

## 텍스트 검색

Machbase는 KEYWORD 인덱스를 활용한 고속 텍스트 검색 기능을 제공합니다.

### 이 절에서 다루는 내용

- **[SEARCH / NOT SEARCH](/dbms/log-table-usage/text-search-keyword-index/#search-not)**: 키워드 인덱스 기반 단어 검색
- **[ESEARCH](/dbms/log-table-usage/text-search-keyword-index/#esearch)**: 패턴(%) 확장 검색
- **[LIKE / NOT LIKE](/dbms/log-table-usage/text-search-keyword-index/#like-not)**: 일반 패턴 매칭

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

**팁**: 대용량 VARCHAR/TEXT 컬럼의 키워드 검색에는 반드시 KEYWORD 인덱스를 생성하고 SEARCH를 사용하세요. LIKE는 인덱스를 활용하지 못해 전체 스캔이 발생합니다.

<a id="text-search-esearch"></a>

### ESEARCH

`ESEARCH`는 KEYWORD 인덱스를 사용하면서 `%` 와일드카드 패턴을 지원하는 확장 검색입니다. 일반 `LIKE`의 단점(인덱스 미사용)을 극복하여 부분 문자열 패턴을 고속으로 검색할 수 있습니다.

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

> `NOT ESEARCH`는 지원하지 않습니다. 반대 패턴이 필요하면 `NOT SEARCH`나 `NOT LIKE`를 사용하세요.

<a id="text-search-like-not"></a>

### LIKE / NOT LIKE

`LIKE`는 SQL 표준 패턴 매칭 연산자입니다. 인덱스를 사용하지 않으므로 대용량 테이블에서는 성능에 주의가 필요합니다.

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
- 앞쪽이 고정된 패턴(`LIKE 'prefix%'`)이라면 인덱스가 있을 경우 활용될 수 있습니다.

<a id="original-85-text-search"></a>

## 텍스트 검색

> **8.5 원문 보강 자료**: 이 문서는 기존 8.5 매뉴얼의 내용을 새 장 구조에 맞춰 보존한 것입니다. Machbase 8.6 기준과 표현이 다른 부분은 같은 절의 최신 리뉴얼 문서를 우선합니다.

이 문서는 키워드 인덱스를 사용한 텍스트 검색을 다룹니다.

텍스트 검색은 원하는 문자열 패턴을 검색하기 위해 "역인덱스"라고 하는 특별한 종류의 인덱스를 검색하기 때문에 비교 가능한 DBMS의 LIKE 검색보다 빠릅니다. 키워드 인덱스는 가변 길이 문자 컬럼인 varchar 및 text 타입 컬럼에만 생성할 수 있습니다. 그러나 검색 대상 문자열은 정확히 일치해야 합니다. Machbase는 특수 문자나 형태소 분석 기반의 키워드를 수행하지 않습니다.

### SEARCH

```sql
SELECT  column_name(s)
FROM    table_name
WHERE   column_name
SEARCH  pattern;
```

```sql
Mach> CREATE TABLE search_table (id INTEGER, name VARCHAR(20));
Created successfully.

Mach> INSERT INTO search_table VALUES(1, 'time flys');
1 row(s) inserted.

Mach> INSERT INTO search_table VALUES(1, 'time runs');
1 row(s) inserted.

Mach> CREATE INDEX idx_SEARCH ON search_table (name) INDEX_TYPE KEYWORD;
Created successfully.

Mach> SELECT * FROM search_table WHERE name SEARCH 'time' OR name SEARCH 'runs2' ;
ID          NAME
-------------------------------------
1           time runs
1           time flys
[2] row(s) selected.

Mach> SELECT * FROM search_table WHERE name SEARCH 'time' AND name SEARCH 'runs2' ;
ID          NAME
-------------------------------------
[0] row(s) selected.

Mach> SELECT * FROM search_table WHERE name SEARCH 'flys' OR name SEARCH 'runs2' ;
ID          NAME
-------------------------------------
1           time flys
[1] row(s) selected.
```


### 다국어 검색

Machbase는 ASCII 및 UTF-8로 저장된 다양한 종류의 언어의 가변 길이 문자열을 검색할 수 있습니다. 한국어나 일본어와 같은 언어에서 문장의 일부만 검색하기 위해 2-gram 기법을 사용합니다.

```sql
SELECT  column_name(s)
FROM    table_name
WHERE   column_name
SEARCH  pattern;
```

```sql
Mach> CREATE TABLE multi_table (message varchar(100));
Created successfully.

Mach> INSERT INTO multi_table VALUES("Machbase is the combination of ideal solutions");
1 row(s) inserted.

Mach> INSERT INTO multi_table VALUES("Machbase is a columnar DBMS");
1 row(s) inserted.

Mach> INSERT INTO multi_table VALUES("Machbaseは理想的なソリューションの組み合わせです");
1 row(s) inserted.

Mach> INSERT INTO multi_table VALUES("Machbaseは円柱状のDBMSです");
1 row(s) inserted.

Mach> CREATE INDEX idx_multi ON multi_table(message) INDEX_TYPE KEYWORD;
Created successfully.

Mach>  SELECT * from multi_table WHERE message SEARCH 'Machbase DBMS';
MESSAGE
------------------------------------------------------------------------------------
Machbaseは円柱状のDBMSです
Machbase is a columnar DBMS
[2] row(s) selected.

Mach> SELECT * from multi_table WHERE message SEARCH 'DBMS is';
MESSAGE
------------------------------------------------------------------------------------
Machbase is a columnar DBMS
[1] row(s) selected.

Mach> SELECT * from multi_table WHERE message SEARCH 'DBMS' OR message SEARCH 'ideal';
MESSAGE
------------------------------------------------------------------------------------
Machbaseは円柱状のDBMSです
Machbase is a columnar DBMS
Machbase is the combination of ideal solutions
[3] row(s) selected.

Mach> SELECT * from multi_table WHERE message SEARCH '組み合わせ';
MESSAGE
------------------------------------------------------------------------------------
Machbaseは理想的なソリューションの組み合わせです
[1] row(s) selected.
Elapsed time: 0.001
Mach> SELECT * from multi_table WHERE message SEARCH '円柱';
MESSAGE
------------------------------------------------------------------------------------
Machbaseは円柱状のDBMSです
[1] row(s) selected.
```

입력 데이터가 "대한민국"일 때, "대한," "한민," "민국" 세 단어가 인덱스에 기록됩니다. 따라서 "대한" 또는 "민국" 키워드로 "대한민국"을 검색할 수 있습니다.

기본적으로 검색 문에 입력된 키워드는 AND 조건으로 검색되므로 세 단어만 입력해도 결과가 매우 정확하게 표시됩니다. 예를 들어, 검색 대상 키워드가 "컴퓨터 활용 가이드"인 경우 "컴퓨터", "활용", "가이드" 세 단어가 AND 조건으로 설정됩니다.

### ESEARCH

ESEARCH 연산자는 검색 대상 키워드를 확장하는 데 사용됩니다. 검색 대상 키워드는 ASCII여야 합니다. % 문자를 사용하여 검색 키워드를 설정할 수 있습니다. LIKE 조건과 같이 % 문자로 시작하는 키워드를 사용하면 모든 레코드를 검색하지만, 키워드 인덱스의 단어에 대해 이 조건을 검색하므로 LIKE보다 검색이 빠릅니다. 이 기능은 알파벳 문자열(오류 문 또는 코드 등)을 빠르게 검색하는 데 유용합니다.

```sql
SELECT  column_name(s)
FROM    table_name
WHERE   column_name
ESEARCH pattern;
```

```sql
Mach> CREATE TABLE esearch_table(id INTEGER, name VARCHAR(20), data VARCHAR(40));
Created successfully.

Mach> INSERT INTO esearch_table VALUES(1, 'machbase', 'Real-time search technology');
1 row(s) inserted.

Mach> INSERT INTO esearch_table VALUES(2, 'mach2flux', 'Real-time data compression');
1 row(s) inserted.

Mach> INSERT INTO esearch_table VALUES(3, 'DB MS', 'Memory cache technology');
1 row(s) inserted.

Mach> INSERT INTO esearch_table VALUES(4, 'ファ ッションアドバイザー、', 'errors');
1 row(s) inserted.

Mach> INSERT INTO esearch_table VALUES(5, '인피 니 플럭스', 'socket232');
1 row(s) inserted.

Mach> CREATE INDEX idx1 ON esearch_table(name) INDEX_TYPE KEYWORD;
Created successfully.

Mach> CREATE INDEX idx2 ON esearch_table(data) INDEX_TYPE KEYWORD;
Created successfully.

Mach> SELECT * FROM esearch_table where name ESEARCH '%base';
ID          NAME                  DATA
--------------------------------------------------------------------------------
1           machbase            Real-time search technology
[1] row(s) selected.
Elapsed time: 0.001
Mach> SELECT * FROM esearch_table where data ESEARCH '%echn%';
ID          NAME                  DATA
--------------------------------------------------------------------------------
3           DB MS                 Memory cache technology
1           machbase            Real-time search technology
[2] row(s) selected.

Mach> SELECT * FROM esearch_table where name ESEARCH '%피니%럭스';
ID          NAME                  DATA
--------------------------------------------------------------------------------
[0] row(s) selected.

Mach> SELECT * FROM esearch_table where data ESEARCH '%232';
ID          NAME                  DATA
--------------------------------------------------------------------------------
5           인피 니 플럭스  socket232
[1] row(s) selected.
```


### REGEXP

REGEXP 연산자는 정규 표현식을 통해 데이터에 대한 텍스트 검색을 수행하는 데 사용됩니다. REGEXP 연산자는 대상 컬럼에 대해 정규 표현식을 수행하여 실행되며, 인덱스를 사용할 수 없기 때문에 검색 성능이 저하될 수 있습니다. 따라서 인덱스를 사용할 수 있는 다른 검색 조건을 AND 연산자로 추가하여 검색 속도를 향상시키는 것이 좋습니다.

특정 정규 표현식 패턴을 검색하기 전에 인덱스를 사용할 수 있는 SEARCH 또는 ESEARCH 연산자를 적용하는 것은 먼저 결과 집합을 줄인 다음 REGEXP를 사용하여 검색 성능을 향상시키는 좋은 방법입니다.

```sql
Mach> CREATE TABLE regexp_table(id INTEGER, name VARCHAR(20), data VARCHAR(40));
Created successfully.

Mach> INSERT INTO regexp_table VALUES(1, 'machbase', 'Real-time search technology');
1 row(s) inserted.

Mach> INSERT INTO regexp_table VALUES(2, 'mach2base', 'Real-time data compression');
1 row(s) inserted.

Mach> INSERT INTO regexp_table VALUES(3, 'DBMS', 'Memory cache technology');
1 row(s) inserted.

Mach> INSERT INTO regexp_table VALUES(4, 'ファ ッショ', 'errors');
1 row(s) inserted.

Mach> INSERT INTO regexp_table VALUES(5, '인피니플럭스', 'socket232');
1 row(s) inserted.

Mach> SELECT * FROM regexp_table WHERE name REGEXP 'mach';
ID          NAME                  DATA
--------------------------------------------------------------------------------
2           mach2base           Real-time data compression
1           machbase            Real-time search technology
[2] row(s) selected.

Mach> SELECT * FROM regexp_table WHERE data REGEXP 'mach[1]';
ID          NAME                  DATA
--------------------------------------------------------------------------------
[0] row(s) selected.

Mach> SELECT * FROM regexp_table WHERE data REGEXP '[A-Za-z]';
ID          NAME                  DATA
--------------------------------------------------------------------------------
5           인피니플럭스  socket232
4           ファ ッショ      errors
3           DBMS                  Memory cache technology
2           mach2base           Real-time data compression
1           machbase            Real-time search technology
[5] row(s) selected.
```


### LIKE

Machbase는 SQL 표준 LIKE 연산자도 지원합니다. LIKE 연산자는 한국어, 일본어 및 중국어에서 사용할 수 있습니다.

```sql
SELECT  column_name(s)
FROM    table_name
WHERE   column_name
LIKE    pattern;
```

예제:

```sql
Mach> CREATE TABLE like_table (id INTEGER, name VARCHAR(20), data VARCHAR(40));
Created successfully.

Mach> INSERT INTO like_table VALUES(1, 'machbase', 'Real-time search technology');
1 row(s) inserted.

Mach> INSERT INTO like_table VALUES(2, 'mach2base', 'Real-time data compression');
1 row(s) inserted.

Mach> INSERT INTO like_table VALUES(3, 'DBMS', 'Memory cache technology');
1 row(s) inserted.

Mach> INSERT INTO like_table VALUES(4, 'ファ ッションアドバイザー、', 'errors');
1 row(s) inserted.

Mach> INSERT INTO like_table VALUES(5, '인피 니 플럭스', 'socket232');
1 row(s) inserted.

Mach> SELECT * FROM like_table WHERE name LIKE 'mach%';
ID          NAME                  DATA
--------------------------------------------------------------------------------
2           mach2base           Real-time data compression
1           machbase            Real-time search technology
[2] row(s) selected.

Mach> SELECT * FROM like_table WHERE name LIKE '%니%';
ID          NAME                  DATA
--------------------------------------------------------------------------------
5           인피 니 플럭스  socket232
[1] row(s) selected.

Mach> SELECT * FROM like_table WHERE data LIKE '%technology';
ID          NAME                  DATA
--------------------------------------------------------------------------------
3           DBMS                  Memory cache technology
1           machbase            Real-time search technology
[2] row(s) selected.
```

<a id="design-text-search"></a>

## 전문 검색 설계

LOG 테이블의 `TEXT` 타입 컬럼은 전문 검색(full-text search)을 지원합니다. `SEARCH` 연산자를 사용하여 특정 단어나 패턴을 포함하는 레코드를 빠르게 찾을 수 있습니다.

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
