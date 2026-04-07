---
title : 'VIEW'
type: docs
weight: 25
toc: true
---

## 목차

* [저장 VIEW란?](#저장-view란)
* [Machbase에서 VIEW를 쓰는 이유](#machbase에서-view를-쓰는-이유)
* [기본 문법](#기본-문법)
* [기본 사용 예제](#기본-사용-예제)
* [컬럼 이름 결정 규칙](#컬럼-이름-결정-규칙)
* [지원되는 VIEW 형태](#지원되는-view-형태)
* [Machbase 특화 사용 예제](#machbase-특화-사용-예제)
* [메타 확인과 운영 점검](#메타-확인과-운영-점검)
* [성능과 제한](#성능과-제한)
* [자주 실패하는 사례](#자주-실패하는-사례)

## 저장 VIEW란?

이 문서에서 설명하는 VIEW는 `FROM (SELECT ...)` 형태의 인라인 뷰가 아니라,
`CREATE VIEW`로 저장해 두고 반복해서 사용하는 **저장 VIEW**입니다.

VIEW는 `SELECT` 결과를 이름 있는 논리 객체로 저장해 재사용하는 기능입니다.

* VIEW는 데이터를 별도로 저장하지 않습니다.
* 조회 시 저장된 VIEW 정의 SQL이 내부적으로 다시 전개되어 실행됩니다.
* 테이블처럼 `SELECT` 대상이 될 수 있지만, 물리 테이블을 대신 저장하는 기능은 아닙니다.
* 현재 문서 범위에서 확인된 사용 방식은 `CREATE VIEW`, `DROP VIEW`, `SELECT`,
  `DESC`, `SHOW VIEWS`, `M$SYS_VIEWS`, `EXPLAIN`입니다.

즉, VIEW는 "데이터를 복사해서 보관하는 기능"이 아니라, 자주 사용하는 조회식을
이름으로 고정해 재사용하는 기능으로 이해하면 됩니다.

## Machbase에서 VIEW를 쓰는 이유

Machbase에서 VIEW는 다음과 같은 상황에 특히 유용합니다.

* 반복해서 사용하는 조회 SQL을 간단한 이름으로 고정하고 싶을 때
* 복잡한 `JOIN`, `GROUP BY`, `CASE`, `UNION ALL`을 여러 곳에서 재사용하고 싶을 때
* Tag 테이블의 `BINARY` 컬럼을 `extract_*()` 함수로 해석한 결과를 논리 컬럼처럼
  노출하고 싶을 때
* 운영 중 `SHOW VIEWS`, `DESC`, `M$SYS_VIEWS`, `EXPLAIN`으로 메타 정보와 실행 계획을
  함께 확인하고 싶을 때

Machbase의 테이블 특성은 VIEW 위에서도 그대로 중요합니다.

* Lookup / Volatile 테이블 기반 VIEW는 원본 테이블의 기본 키 조건이 여전히 중요합니다.
* Tag 테이블 기반 VIEW는 `name`, `time` 조건과 `EXPLAIN` 결과를 함께 보는 것이 좋습니다.
* VIEW는 원본 테이블의 인덱스와 optimizer 판단을 이용하므로, 성능은 원본 조회식의
  영향을 그대로 받습니다.

## 기본 문법

### VIEW 생성

```sql
CREATE VIEW view_name AS
SELECT ...
FROM ...;
```

```sql
CREATE VIEW view_name (col1, col2, ...) AS
SELECT ...
FROM ...;
```

```sql
CREATE OR REPLACE VIEW view_name AS
SELECT ...
FROM ...;
```

* `view_name`은 `db.user.view_name` 형태의 schema-qualified 이름도 사용할 수 있습니다.
* `CREATE OR REPLACE VIEW`는 기존 VIEW 정의를 교체합니다.
* 같은 이름의 객체가 이미 table 등 VIEW가 아닌 객체이면 교체되지 않고 에러를 반환합니다.
* 현재 검증된 구현에서는 `CREATE OR REPLACE VIEW` 후에도 같은 object id를 유지합니다.
* 교체용 새 정의의 검증에 실패하면 기존 VIEW 정의는 그대로 유지됩니다.

### VIEW 삭제

```sql
DROP VIEW view_name;
DROP VIEW IF EXISTS view_name;
```

* `DROP VIEW IF EXISTS`는 대상이 없어도 통과합니다.
* 다른 VIEW가 해당 VIEW를 참조하고 있으면 `DROP VIEW`는 차단됩니다.
* `DROP TABLE view_name`으로 VIEW를 삭제할 수는 없습니다.

### 메타 확인

```sql
SHOW VIEWS;
DESC view_name;

SELECT USER_NAME, DB_NAME, VIEW_NAME, VIEW_SQL
FROM M$SYS_VIEWS;
```

## 기본 사용 예제

다음 예제는 가장 단순한 Lookup 기반 VIEW입니다.

```sql
CREATE LOOKUP TABLE customer (
    id INTEGER PRIMARY KEY,
    name VARCHAR(20),
    city VARCHAR(20),
    amount INTEGER
);

CREATE VIEW v_customer AS
SELECT id, name, city, amount
FROM customer;

SELECT name, city
FROM v_customer
WHERE id = 100;
```

컬럼 이름을 명시하고 싶다면 컬럼 리스트를 함께 줄 수 있습니다.

```sql
CREATE VIEW v_customer_short (cust_id, cust_name) AS
SELECT id, name
FROM customer;

SELECT cust_id, cust_name
FROM v_customer_short
WHERE cust_id = 100;
```

기존 VIEW 정의를 바꿀 때는 `CREATE OR REPLACE VIEW`를 사용합니다.

```sql
CREATE VIEW v_customer_amount AS
SELECT id, amount
FROM customer;

CREATE OR REPLACE VIEW v_customer_amount AS
SELECT id, amount * 10 AS amount
FROM customer
WHERE id <= 10;
```

## 컬럼 이름 결정 규칙

### 명시 컬럼 리스트를 준 경우

```sql
CREATE VIEW v_sales (sales_id, sales_name) AS
SELECT id, name
FROM t_sales;
```

이 경우 VIEW의 공식 컬럼명은 `sales_id`, `sales_name`입니다.

### 명시 컬럼 리스트를 생략한 경우

컬럼명은 다음 순서로 결정됩니다.

1. `SELECT` alias
2. 단일 컬럼 참조의 원본 컬럼명
3. 그 외 표현식은 자동 생성 이름(`EXPR1`, `EXPR2`, ...)

```sql
CREATE VIEW v_expr AS
SELECT id,
       name AS user_name,
       val + 10
FROM t1;
```

위 예제의 결과 컬럼명은 `ID`, `USER_NAME`, `EXPR3` 형태가 됩니다.

### `UNION ALL` VIEW의 컬럼명

`UNION ALL` VIEW는 가장 왼쪽 `SELECT`의 target 이름을 따릅니다.

```sql
CREATE VIEW v_union AS
SELECT id FROM t1
UNION ALL
SELECT id FROM t2;
```

따라서 `DESC v_union`에서는 `ID`가 보이고, `SELECT id FROM v_union`도 정상 동작합니다.

## 지원되는 VIEW 형태

현재 검증된 VIEW 형태는 다음과 같습니다.

* 단순 projection과 predicate
* expression, 함수, 상수, `CASE`
* `JOIN`
* subquery 포함 VIEW
* nested VIEW
* `GROUP BY`, `HAVING`
* `DISTINCT`
* `UNION ALL`

예를 들면 다음과 같은 VIEW가 모두 현재 구현 범위에서 검증되었습니다.

```sql
CREATE VIEW v_expr_case AS
SELECT id,
       CASE WHEN amount >= 100 THEN 'VIP' ELSE 'NORMAL' END AS grade,
       UPPER(city) AS city_upper
FROM customer;
```

```sql
CREATE VIEW v_city_sum AS
SELECT city, SUM(amount) AS total_amount
FROM customer
GROUP BY city
HAVING SUM(amount) >= 100;
```

```sql
CREATE VIEW v_union AS
SELECT id FROM customer WHERE city = 'SEOUL'
UNION ALL
SELECT id FROM customer WHERE city = 'BUSAN';
```

```sql
CREATE VIEW v_nested AS
SELECT id, total_amount
FROM v_city_sum
JOIN (
    SELECT city AS city_name, COUNT(*) AS city_cnt
    FROM customer
    GROUP BY city
) x
ON v_city_sum.city = x.city_name;
```

## Machbase 특화 사용 예제

### Tag / BINARY 컬럼 해석

Tag 테이블의 `BINARY` 컬럼을 해석해 논리 컬럼처럼 사용하는 것은 Machbase에서
실제 활용도가 높은 VIEW 패턴입니다.

```sql
CREATE TAG TABLE dam (
    name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    frame BINARY(16)
);

CREATE VIEW damdata AS
SELECT name,
       time,
       extract_bit(frame, 0) AS bit0,
       extract_ulong(frame, 0, 16) AS u16,
       extract_long(frame, 0, 16) AS s16,
       extract_float(frame, 0) AS f32,
       extract_scaled_double(frame, 0, 12, 0, 0.5, 0.5) AS sd12
FROM dam;
```

```sql
SELECT name, time, bit0, u16, s16, f32, sd12
FROM damdata
WHERE name = 'main'
  AND time >= TO_DATE('2024-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
  AND time <  TO_DATE('2024-01-01 00:01:00', 'YYYY-MM-DD HH24:MI:SS')
ORDER BY time;
```

이 경우에도 성능 확인은 원본 Tag 테이블과 마찬가지로 `name`, `time` 조건과
`EXPLAIN` 결과를 함께 보는 것이 좋습니다.

### 스키마와 인용부호 이름

VIEW 이름은 schema-qualified 이름과 quoted identifier를 모두 사용할 수 있습니다.

```sql
CREATE VIEW machbasedb.sys.v_local AS
SELECT id, val
FROM other_user.v_src
WHERE id >= 2;

CREATE VIEW "V_QUOTED" AS
SELECT id, val
FROM t1;

CREATE VIEW v_dep AS
SELECT id
FROM "V_QUOTED"
WHERE val >= 20;
```

* 같은 이름의 VIEW가 서로 다른 schema에 있어도 schema-qualified 이름으로 구분됩니다.
* quoted VIEW를 참조하는 dependent VIEW가 있으면 `DROP VIEW`는 차단됩니다.

## 메타 확인과 운영 점검

### `SHOW VIEWS`

`SHOW VIEWS`는 현재 사용자가 볼 수 있는 VIEW 목록과 정의 SQL을 함께 보여줍니다.

출력 컬럼은 다음과 같습니다.

* `USER_NAME`
* `DB_NAME`
* `VIEW_NAME`
* `VIEW_SQL`

```sql
SHOW VIEWS;
```

### `M$SYS_VIEWS`

`M$SYS_VIEWS`는 VIEW 정의 SQL을 확인하는 공개 메타 인터페이스입니다.

```sql
SELECT USER_NAME, DB_NAME, VIEW_NAME, VIEW_SQL
FROM M$SYS_VIEWS
WHERE VIEW_NAME = 'V_CUSTOMER';
```

다음과 같은 상황에서 유용합니다.

* VIEW 목록 확인
* 특정 VIEW의 정의 SQL 확인
* `CREATE OR REPLACE VIEW` 후 정의 변경 여부 확인

### `DESC`, `M$SYS_TABLES`, `M$SYS_COLUMNS`

```sql
DESC v_customer;

SELECT ID, NAME, TYPE
FROM M$SYS_TABLES
WHERE TYPE = 7;

SELECT TABLE_ID, ID, NAME, TYPE, LENGTH
FROM M$SYS_COLUMNS
WHERE TABLE_ID = (
    SELECT ID
    FROM M$SYS_TABLES
    WHERE TYPE = 7
      AND NAME = 'V_CUSTOMER'
);
```

* `DESC`는 VIEW의 노출 컬럼명과 타입을 보여줍니다.
* `M$SYS_TABLES`에서는 VIEW를 `TYPE = 7`로 확인할 수 있습니다.
* `M$SYS_COLUMNS`에서는 VIEW 컬럼 구성을 확인할 수 있습니다.
* `CREATE OR REPLACE VIEW`를 수행해도 `M$SYS_TABLES.ID`는 유지되고,
  `M$SYS_VIEWS.VIEW_SQL`이 새 정의로 갱신됩니다.

### `EXPLAIN`

VIEW는 물리 데이터를 따로 갖지 않기 때문에, 실제 성능은 원본 조회식과 optimizer
판단에 좌우됩니다. 운영에서는 `EXPLAIN`으로 실행 경로를 먼저 확인하는 것이 좋습니다.

```sql
EXPLAIN
SELECT *
FROM v_customer
WHERE id = 3;
```

## 성능과 제한

### 인덱스와 predicate pushdown

다음과 같은 경우에는 원본 테이블 쪽으로 조건이 잘 내려가 인덱스를 사용할 가능성이 높습니다.

* base column을 그대로 노출한 단순 projection VIEW
* 컬럼 이름만 바꾼 VIEW
* VIEW 내부에 단순 filter가 있고, outer predicate가 base column과 직접 연결되는 경우

다음과 같은 경우에는 full scan으로 돌아갈 수 있으므로 `EXPLAIN` 확인이 중요합니다.

* `DISTINCT`가 들어간 VIEW 위의 outer predicate
* `id + 1 AS id2`처럼 계산식으로 만든 컬럼 기준 predicate

### 단순 저장 VIEW 최적화

현재 검증된 구현에서는 단순한 저장 VIEW에 대해 다음 최적화가 적용될 수 있습니다.

* outer query가 실제로 참조하는 컬럼만 남기도록 projection을 줄이는 경로
* `COUNT(*)`와 pushdown 가능한 조건 조합에서 상단 projection을 우회하는 빠른 경로

반대로 `SELECT *`, `DISTINCT`, `GROUP BY`, `HAVING`, set-op, window, join이 무거운
형태는 전체 projection 경로로 처리될 수 있습니다.

### VIEW 정의 SQL 길이 제한

현재 검증된 구현에서는 `AS` 뒤의 VIEW 정의 SQL(`SELECT` 본문)이 최대 `256KB`까지
지원됩니다.

초과 시 다음 계열 오류를 반환합니다.

```text
ERR-02010: Syntax error: near token (VIEW_SQL_TOO_LONG).
```

### 삭제와 의존성

* dependent VIEW가 있으면 `DROP VIEW`는 차단됩니다.
* 의존성 판정은 실제 참조 객체 기준으로 수행됩니다.
* 이름이 문자열 리터럴이나 alias에만 들어 있는 경우는 dependency로 취급되지 않습니다.

## 자주 실패하는 사례

### 컬럼 수 불일치

```sql
CREATE VIEW v_bad (c1, c2, c3) AS
SELECT id, val
FROM t1;
```

### 자기 자신을 직접 참조하는 재귀 VIEW

```sql
CREATE VIEW v_recursive AS
SELECT id
FROM v_recursive;
```

### 중복 컬럼명과 `_RID`

```sql
CREATE VIEW v_dup AS
SELECT id AS c1, val AS c1
FROM t1;

CREATE VIEW v_rid (_RID) AS
SELECT id
FROM t1;
```

### VIEW가 아닌 객체를 `CREATE OR REPLACE VIEW`로 덮어쓰기

```sql
CREATE OR REPLACE VIEW t1 AS
SELECT id
FROM src_t1;
```

### 예약 이름 또는 잘못된 경로 사용

```sql
CREATE VIEW v$bad AS
SELECT id
FROM t1;

CREATE VIEW _tag_bad AS
SELECT id
FROM t1;

CREATE VIEW no_such_db.sys.v_bad AS
SELECT id
FROM t1;
```

### VIEW를 `DROP TABLE`로 삭제

```sql
DROP TABLE v_customer;
```

이 경우 VIEW는 삭제되지 않으며 에러가 반환됩니다.

## 관련 문서

* [DDL](../ddl)
* [SELECT](../select)
