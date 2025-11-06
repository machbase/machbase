---
title: 브리지 - SQLite
type: docs
weight: 11
---

## SQLite 브리지 등록

SQLite에 연결하는 브리지를 등록합니다.

```
bridge add -t sqlite sqlitedb file:/data/sqlite.db;
```

SQLite는 아래와 같이 메모리 전용 모드도 지원합니다.

```
bridge add -t sqlite mem file::memory:?cache=shared
```

아래 명령은 그림과 같은 웹 UI에서 수행하는 설정과 동일합니다.

{{< figure src="/neo/bridges/img/sqlite-add.png" width="500" >}}


## 브리지 연결 테스트

```
machbase-neo» bridge test mem;
Test bridge mem connectivity... success 11.917µs
```

{{< figure src="/neo/bridges/img/sqlite-test.png" width="600" >}}

## 테이블 생성

machbase-neo 셸에서 `mem` 브리지를 통해 `mem_example` 테이블을 생성합니다.

```sh
bridge exec mem CREATE TABLE IF NOT EXISTS mem_example(
    id         INTEGER NOT NULL PRIMARY KEY,
    company    TEXT,
    employee   INTEGER,
    discount   REAL,
    code       TEXT,
    valid      BOOLEAN,
    memo       BLOB,
    created_on DATETIME NOT NULL
);
```
표준 SQL 에디터에서 `-- env: bridge=<name>` 주석을 사용하면 해당 브리지에 SQL을 실행할 수 있습니다.
`-- env: reset`으로 초기화하기 전까지 주석 설정이 유지됩니다.

```sql
-- env: bridge=mem
CREATE TABLE IF NOT EXISTS mem_example(
    id         INTEGER NOT NULL PRIMARY KEY,
    company    TEXT,
    employee   INTEGER,
    discount   REAL,
    code       TEXT,
    valid      BOOLEAN,
    memo       BLOB,
    created_on DATETIME NOT NULL
);
-- env: reset
```

{{< figure src="/neo/bridges/img/sqlite-sql-create-table.png" width="600" >}}

## SQL 에디터에서 DML 수행

```sql
-- env: bridge=mem
INSERT INTO mem_example(company, employee, created_on) 
    values('Fedel-Gaylord', 12, datetime('now'));

INSERT INTO mem_example(company, employee, created_on) 
    values('Simoni', 23, datetime('now'));

SELECT company, employee, datetime(created_on, 'localtime') from mem_example;

DELETE from mem_example;
-- env: reset
```

{{< figure src="/neo/bridges/img/sqlite-sql-dml.png" width="600" >}}

## SQLite에 TQL로 쓰기

```js {linenos=table,hl_lines=["10"],linenostart=1}
FAKE( json({
    ["COMPANY", "EMPLOYEE"],
    ["NovaWave", 10],
    ["Sunflower", 20]
}))

DROP(1) // skip header
MAPVALUE(2, time("now"))

INSERT(bridge("mem"), table("mem_example"), "company", "employee", "created_on")
```

```
machbase-neo» bridge query mem select * from mem_example;
╭────┬─────────┬──────────┬──────────┬───────┬───────┬──────┬──────────────────────────────────────╮
│ ID │ COMPANY │ EMPLOYEE │ DISCOUNT │ CODE  │ VALID │ MEMO │ CREATED_ON                           │
├────┼─────────┼──────────┼──────────┼───────┼───────┼──────┼──────────────────────────────────────┤
│  1 │ acme    │       10 │ <nil>    │ <nil> │ <nil> │ []   │ 2023-08-10 14:33:08.667491 +0900 KST │
╰────┴─────────┴──────────┴──────────┴───────┴───────┴──────┴──────────────────────────────────────╯
```

## SQLite에서 TQL로 읽기

아래 코드를 `sqlite.tql`로 저장합니다.

```js
SQL(bridge('mem'), "select company, employee, created_on from mem_example")
CSV()
```

그런 다음 `curl` 명령이나 브라우저로 엔드포인트를 호출합니다.

```sh
curl -o - http://127.0.0.1:5654/db/tql/sqlite.tql
```

```csv
NovaWave,10,1704866777160399000
Sunflower,20,1704866777160407000
```

## SQLite 간 데이터 복사

다음 예시는 Machbase 데이터를 SQLite 브리지로 복사하는 방법을 보여 줍니다.

**브리지**

아래 설정으로 `sqlite` 브리지를 정의합니다.

- 타입: `SQLite`
- 연결 문자열: `file:///tmp/sqlite.db`

**SQL**

`/tmp/sqlite.db`에 위치한 SQLite 데이터베이스에 `example` 테이블을 생성합니다.

```sql
--env: bridge=sqlite
CREATE TABLE IF NOT EXISTS example (
    NAME TEXT,
    TIME DATETIME,
    VALUE REAL
);
-- env: reset
```

**TQL**

아래 TQL 스크립트는 `SQL()`로 데이터를 조회한 뒤, `INSERT()`에 `bridge("sqlite")`를 지정해 SQLite로 적재합니다.

```js
SQL(`select name, time, value from example where name = 'my-car'`)
INSERT(bridge("sqlite"), "name", "time", "value", table("example"))
```

**SQL**

```sql
--env: bridge=sqlite
SELECT * FROM example order by TIME;
-- env: reset
```
