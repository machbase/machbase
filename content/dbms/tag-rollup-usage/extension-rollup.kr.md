---
type: docs
title: '6.7 확장 ROLLUP과 FIRST/LAST'
weight: 70
toc: true
aliases:
  - /dbms/tag-rollup-usage/first-last-rollup/
---

<a id="rollup-extension"></a>

## EXTENSION과 원본 FIRST/LAST의 차이

EXTENSION은 ROLLUP에 첫·마지막 값과 관련 시각 정보를 추가합니다.
일반 원본 GROUP BY에서 FIRST/LAST를 사용하는 것과, 저장된 ROLLUP에서 FIRST/LAST를
조회하는 것은 다릅니다. 후자에는 적용 가능한 확장 ROLLUP이 필요합니다.

시간 전용 EXTENSION은 첫·마지막 값과 시각을 저장합니다. 정렬 EXTENSION은 후보의 보조 키도 저장합니다. MIN, MAX, SUM, COUNT와
제곱합인 SUMSQ는 일반 ROLLUP에도 함께 저장됩니다. SUMSQ로 분산과 표준편차를
계산하는 방법은 [SUMSQ와 분산·표준편차](../query-syntax-rollup/#query-sumsq-stddev-rollup)를
참고합니다.

## 준비와 입력

```sql
CREATE TAG TABLE ch6_ext (
    code VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    price DOUBLE
);
CREATE ROLLUP ch6_ext_first
  ON ch6_ext(price) INTERVAL 1 MIN EXTENSION;
CREATE ROLLUP ch6_ext_plain
  ON ch6_ext(price) INTERVAL 1 MIN;
INSERT INTO ch6_ext VALUES ('AAPL', TO_DATE('2026-01-01 09:00:00', 'YYYY-MM-DD HH24:MI:SS'), 100);
INSERT INTO ch6_ext VALUES ('AAPL', TO_DATE('2026-01-01 09:00:10', 'YYYY-MM-DD HH24:MI:SS'), 105);
INSERT INTO ch6_ext VALUES ('AAPL', TO_DATE('2026-01-01 09:00:20', 'YYYY-MM-DD HH24:MI:SS'), 99);
INSERT INTO ch6_ext VALUES ('AAPL', TO_DATE('2026-01-01 09:00:30', 'YYYY-MM-DD HH24:MI:SS'), 103);
EXEC TABLE_FLUSH(ch6_ext);
ALTER ROLLUP ch6_ext_first FORCE;
ALTER ROLLUP ch6_ext_plain FORCE;
```

## 원본과 OHLC 비교

```sql
SELECT DATE_TRUNC('minute', time) AS bucket,
       FIRST(time, price) AS open_price, MAX(price) AS high_price,
       MIN(price) AS low_price, LAST(time, price) AS close_price
  FROM ch6_ext WHERE code = 'AAPL'
 GROUP BY bucket ORDER BY bucket;

SELECT /*+ ROLLUP_TABLE(ch6_ext_first) */
       rollup('min', 1, time) AS bucket,
       FIRST(time, price) AS open_price, MAX(price) AS high_price,
       MIN(price) AS low_price, LAST(time, price) AS close_price
  FROM ch6_ext WHERE code = 'AAPL'
 GROUP BY bucket ORDER BY bucket;
```

두 쿼리는 09:00 버킷에 Open=100, High=105, Low=99, Close=103을 반환합니다.
시간 단독 ROLLUP의 FIRST/LAST 첫 인자는 BASETIME, 두 번째는 집계 대상 컬럼을 사용합니다.
같은 시각의 행에 업무상 순서가 필요하면 아래 복합 키 정렬 정의를 사용합니다.

## 일반 후보와 확장 후보가 함께 있을 때

일반 ROLLUP이 확장 ROLLUP보다 무조건 우선하는 것은 아닙니다. 같은 조건·간격의 후보는
등록 순서의 영향을 받습니다. 이 예제는 확장을 먼저 만들었지만, 결과가 특정 후보에
의존해야 한다면 위처럼 명시합니다. 확장만 적용 가능한 환경에서는 힌트 없이 선택될 수도 있습니다.

다음은 일반 ROLLUP을 강제하므로 의도적으로 실패하는 조회입니다.

```sql
SELECT /*+ ROLLUP_TABLE(ch6_ext_plain) */
       rollup('min', 1, time) AS bucket, FIRST(time, price)
  FROM ch6_ext WHERE code = 'AAPL'
 GROUP BY bucket;
```

자동 계층에 확장이 필요하면 별도 테이블의 CREATE에서
`WITH ROLLUP (SEC) EXTENSION`을 사용합니다. FROM으로 계층을 만들 때도 확장 속성을
일치시켜야 합니다. Custom OHLCV 재집계는 [Custom 예제](../custom-rollup/)을 참고합니다.

## 정리

```sql
DROP ROLLUP ch6_ext_plain;
DROP ROLLUP ch6_ext_first;
DROP TABLE ch6_ext;
```

<a id="composite-first-last"></a>

## 복합 키 FIRST/LAST와 정렬 ROLLUP

> 복합 정렬 키 구문은 해당 기능이 반영된 엔진 빌드에서 사용합니다. 사용 중인 제품 버전의 지원 여부를 확인해야 합니다.

공개 ROWID 정렬 키는 이 문서의 지원 범위에 포함하지 않습니다.

### 예제 데이터

raw_tab은 ROLLUP 없는 원본 TAG이며 rollup_tab은 정렬 ROLLUP의 집계 대상 TAG입니다.
동명 객체가 없는 별도 환경을 전제로 합니다. 첫 키는 시간이고 입력 순서는 업무 키 순서와 다릅니다.
종목별 각 분 시작 시각에 같은 code/time의 레코드가 3건씩 있습니다.

```sql
CREATE TAG TABLE raw_tab (
    code     VARCHAR(20) PRIMARY KEY,
    time     DATETIME BASETIME,
    price    DOUBLE SUMMARIZED,
    seq      INTEGER,
    event_id INTEGER
);

INSERT INTO raw_tab VALUES ('A', TO_DATE('2026-10-22 09:00:00'), 102, 1, 2);
INSERT INTO raw_tab VALUES ('A', TO_DATE('2026-10-22 09:00:50'), 105, 1, 2);
INSERT INTO raw_tab VALUES ('A', TO_DATE('2026-10-22 09:00:00'), 103, 2, 1);
INSERT INTO raw_tab VALUES ('A', TO_DATE('2026-10-22 09:00:00'), 101, 1, 1);
INSERT INTO raw_tab VALUES ('A', TO_DATE('2026-10-22 09:00:50'), 104, 1, 1);

INSERT INTO raw_tab VALUES ('A', TO_DATE('2026-10-22 09:01:00'), 202, 1, 2);
INSERT INTO raw_tab VALUES ('A', TO_DATE('2026-10-22 09:01:50'), 205, 1, 2);
INSERT INTO raw_tab VALUES ('A', TO_DATE('2026-10-22 09:01:00'), 203, 2, 1);
INSERT INTO raw_tab VALUES ('A', TO_DATE('2026-10-22 09:01:00'), 201, 1, 1);
INSERT INTO raw_tab VALUES ('A', TO_DATE('2026-10-22 09:01:50'), 204, 1, 1);

INSERT INTO raw_tab VALUES ('B', TO_DATE('2026-10-22 09:00:00'), 302, 1, 2);
INSERT INTO raw_tab VALUES ('B', TO_DATE('2026-10-22 09:00:50'), 305, 1, 2);
INSERT INTO raw_tab VALUES ('B', TO_DATE('2026-10-22 09:00:00'), 303, 2, 1);
INSERT INTO raw_tab VALUES ('B', TO_DATE('2026-10-22 09:00:00'), 301, 1, 1);
INSERT INTO raw_tab VALUES ('B', TO_DATE('2026-10-22 09:00:50'), 304, 1, 1);

INSERT INTO raw_tab VALUES ('B', TO_DATE('2026-10-22 09:01:00'), 402, 1, 2);
INSERT INTO raw_tab VALUES ('B', TO_DATE('2026-10-22 09:01:50'), 405, 1, 2);
INSERT INTO raw_tab VALUES ('B', TO_DATE('2026-10-22 09:01:00'), 403, 2, 1);
INSERT INTO raw_tab VALUES ('B', TO_DATE('2026-10-22 09:01:00'), 401, 1, 1);
INSERT INTO raw_tab VALUES ('B', TO_DATE('2026-10-22 09:01:50'), 404, 1, 1);

EXEC TABLE_FLUSH(raw_tab);

SELECT COUNT(*) AS row_count FROM raw_tab;
```

### 원본 조회와 동률

시간만으로 선택하면 A의 09:00 FIRST는 101/102/103, LAST는 104/105 중 하나입니다.
(time, seq)에서는 FIRST 후보가 101/102로 줄지만 time/seq까지 같아 특정 행을 보장하지 않습니다.
아래 3키 조회는 event_id까지 비교해 후보를 결정합니다.

```sql
SELECT code, DATE_TRUNC('minute', time) AS bucket,
       FIRST(time, price) AS first_price,
       LAST(time, price) AS last_price
  FROM raw_tab
 WHERE time >= TO_DATE('2026-10-22 09:00:00')
   AND time <  TO_DATE('2026-10-22 09:02:00')
 GROUP BY code, bucket
 ORDER BY code, bucket;
```

```sql
SELECT code, DATE_TRUNC('minute', time) AS bucket,
       FIRST((time, seq), price) AS first_price,
       LAST((time, seq), price) AS last_price
  FROM raw_tab
 WHERE time >= TO_DATE('2026-10-22 09:00:00')
   AND time <  TO_DATE('2026-10-22 09:02:00')
 GROUP BY code, bucket
 ORDER BY code, bucket;
```

```sql
SELECT code, DATE_TRUNC('minute', time) AS bucket,
       FIRST((time, seq, event_id), price) AS first_price,
       LAST((time, seq, event_id), price) AS last_price
  FROM raw_tab
 WHERE time >= TO_DATE('2026-10-22 09:00:00')
   AND time <  TO_DATE('2026-10-22 09:02:00')
 GROUP BY code, bucket
 ORDER BY code, bucket;
```

| code | bucket | first_price | last_price |
|---|---|---:|---:|
| A | 2026-10-22 09:00:00 | 101 | 105 |
| A | 2026-10-22 09:01:00 | 201 | 205 |
| B | 2026-10-22 09:00:00 | 301 | 305 |
| B | 2026-10-22 09:01:00 | 401 | 405 |

### 키별 방향

```sql
SELECT code, DATE_TRUNC('minute', time) AS bucket,
       FIRST((time ASC, seq ASC, event_id DESC), price) AS first_price,
       LAST((time ASC, seq ASC, event_id DESC), price) AS last_price
  FROM raw_tab
 WHERE time >= TO_DATE('2026-10-22 09:00:00')
   AND time <  TO_DATE('2026-10-22 09:02:00')
 GROUP BY code, bucket
 ORDER BY code, bucket;
```

event_id만 DESC로 지정하면 결과는 A=102/104, 202/204, B=302/304, 402/404입니다.

### 정렬 ROLLUP 정의와 조회

rollup_tab에 같은 데이터를 저장한 뒤 정렬 정의와 동일한 키로 조회합니다.
ROLLUP_TABLE 힌트는 이 예제에서 저장된 ROLLUP을 명시적으로 선택합니다.

```sql
CREATE TAG TABLE rollup_tab (
    code     VARCHAR(20) PRIMARY KEY,
    time     DATETIME BASETIME,
    price    DOUBLE SUMMARIZED,
    seq      INTEGER,
    event_id INTEGER
);

INSERT INTO rollup_tab SELECT * FROM raw_tab;
EXEC TABLE_FLUSH(rollup_tab);

CREATE ROLLUP price_1m_ordered
    ON rollup_tab(price)
    INTERVAL 1 MIN
    EXTENSION ORDER BY time ASC, seq ASC, event_id ASC;

ALTER ROLLUP price_1m_ordered FORCE;
```

```sql
SELECT /*+ ROLLUP_TABLE(price_1m_ordered) */
       code, ROLLUP('min', 1, time) AS bucket,
       FIRST((time, seq, event_id), price) AS first_price,
       LAST((time, seq, event_id), price) AS last_price
  FROM rollup_tab
 WHERE time >= TO_DATE('2026-10-22 09:00:00')
   AND time <  TO_DATE('2026-10-22 09:02:00')
 GROUP BY code, bucket
 ORDER BY code, bucket;
```

결과는 위 원본 3키 ASC 조회와 같습니다. DESC 조회에는 같은 방향으로 만든 별도 정의가 필요합니다.

```sql
CREATE ROLLUP price_1m_desc
    ON rollup_tab(price)
    INTERVAL 1 MIN
    EXTENSION ORDER BY time ASC, seq ASC, event_id DESC;

ALTER ROLLUP price_1m_desc FORCE;

SELECT /*+ ROLLUP_TABLE(price_1m_desc) */
       code, ROLLUP('min', 1, time) AS bucket,
       FIRST((time, seq, event_id DESC), price) AS first_price,
       LAST((time, seq, event_id DESC), price) AS last_price
  FROM rollup_tab
 WHERE time >= TO_DATE('2026-10-22 09:00:00')
   AND time <  TO_DATE('2026-10-22 09:02:00')
 GROUP BY code, bucket
 ORDER BY code, bucket;
```

### 상위 ROLLUP

```sql
CREATE ROLLUP price_1h_ordered
    FROM price_1m_ordered
    INTERVAL 1 HOUR EXTENSION;

ALTER ROLLUP price_1h_ordered FORCE;

SELECT /*+ ROLLUP_TABLE(price_1h_ordered) */
       code, ROLLUP('hour', 1, time) AS bucket,
       FIRST((time, seq, event_id), price) AS first_price,
       LAST((time, seq, event_id), price) AS last_price
  FROM rollup_tab
 GROUP BY code, bucket
 ORDER BY code, bucket;
```

상위 ROLLUP은 하위의 정렬 정의와 원본 후보 키를 상속합니다. 이 예제의 시간별 결과는 A=101/205, B=301/405입니다.

### 정의 일치와 변경 제약

- 첫 키는 원본 TAG의 BASETIME이며 보조 키는 지원되는 일반 데이터 컬럼입니다.
  TAG 이름·메타데이터 컬럼, 계산식, 테이블 한정 컬럼 참조는 정의에 사용할 수 없습니다.
- 숫자 대상의 정렬 EXTENSION을 지원합니다. JSON_PATH/JSON_SUMMARY 조합은 지원하지 않습니다.
- 조회의 키 개수·컬럼·순서·방향·타입이 정의와 맞아야 합니다. 다른 방향의 ROLLUP을 강제하면 오류가 발생합니다.
- 기존 시간 전용 ROLLUP에는 보조 키가 없습니다. 새 정의로 원본을 다시 집계해야 하며 삭제된 원본의 키는 복구할 수 없습니다.
- 저장된 후보 키가 일반 WHERE·GROUP BY·출력에서 해당 원본 컬럼의 사용 범위를 넓히지는 않습니다.
- 정렬 메타데이터와 생성 SQL 길이 제한을 넘는 정의는 생성 시 거부합니다.
- Standard에서 참조 키 컬럼의 RENAME은 ERR-02686으로 거부합니다. STOP 상태와 상위 의존성도 적용됩니다.
  관련 상위·하위 ROLLUP을 모두 DROP한 뒤 컬럼을 변경하고 새 이름으로 다시 생성합니다.
- 원본 UPDATE의 자동 재집계를 추가한 기능은 아닙니다.
- Cluster의 모든 broker·warehouse는 기능을 지원하는 동일 빌드를 사용해야 합니다.

### 예제 객체 삭제

```sql
DROP ROLLUP price_1h_ordered;
DROP ROLLUP price_1m_desc;
DROP ROLLUP price_1m_ordered;
DROP TABLE rollup_tab;
DROP TABLE raw_tab;
```
