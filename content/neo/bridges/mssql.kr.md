---
title: 브리지 - MSSQL
type: docs
weight: 15
---

## MSSQL 브리지 등록

MSSQL 데이터베이스에 연결할 브리지를 등록합니다.

연결 문자열은 MSSQL 규격을 따릅니다.

```
bridge add -t mssql  ms server=127.0.0.1:1433 user=sa pass=changeme database=master encrypt=disable
```

**연결 옵션**

| Option               | 별칭                    | 설명                                              | example                 |
| :-----------         | :-----------            | :-------------------------------------------------| :-------------          |
| `server`             |                          | MSSQL 서버 주소                                   | `server=127.0.0.1:1433` |
| `database`           |                          | 데이터베이스 이름                                 | `database=master`       |
| `user id`            | `user`, `user-id`        | 사용자 이름                                       | `user=sa`               |
| `password`           | `pass`                   | 사용자 비밀번호                                   | `password=changeme`     |
| `connection timeout` | `connection-timeout`     | DB 연결 대기 시간(초)                              | `connection-timeout=5`  |
| `dial timeout`       | `dial-timeout`           | TCP 핸드셰이크 타임아웃(초)                        | `dial-timeout=3`        |
| `app name`           | `app-name`               | 애플리케이션 이름(기본값 `neo-bridge`)             |                         |
| `encrypt`            |                          | 암호화 모드 (`disable`, `true`, `false`)           | (see below)             |

- `encrypt`
  - `disable` : 클라이언트-서버 간 데이터가 암호화되지 않습니다.
  - `false` : 로그인 패킷을 제외한 나머지 데이터는 암호화되지 않습니다.
  - `true` : 클라이언트-서버 간 모든 데이터가 암호화됩니다.

```
machbase-neo» bridge list;
╭────────┬──────────┬───────────────────────────────────────────────────────────╮
│ NAME   │ TYPE     │ CONNECTION                                                │
├────────┼──────────┼───────────────────────────────────────────────────────────┤
│ ms     │ mssql    │ server=127.0.0.1:1433 user=SA pass=secret database=master │
╰────────┴──────────┴───────────────────────────────────────────────────────────╯
```

연결 테스트

```
machbase-neo» bridge test ms;
Test bridge ms connectivity... success 3.042458ms
```

## 테이블 생성

machbase-neo 셸에서 아래 명령을 실행해 `ms` 브리지를 통해 `ms_example` 테이블을 생성합니다.

```sh
bridge exec ms CREATE TABLE ms_example(
    id         INT NOT NULL PRIMARY KEY,
    company    VARCHAR(50) UNIQUE NOT NULL,
    employee   INT,
    discount   REAL,
    pricePlan  NUMERIC(7,2),
    code       BINARY,
    valid      SMALLINT,
    memo       TEXT,
    created_on DATETIME NOT NULL,
    UNIQUE(company)
);
```

```
machbase-neo» bridge query ms select * from ms_example;
╭────┬─────────┬──────────┬──────────┬───────────┬──────┬───────┬──────┬────────────╮
│ ID │ COMPANY │ EMPLOYEE │ DISCOUNT │ PRICEPLAN │ CODE │ VALID │ MEMO │ CREATED_ON │
├────┼─────────┼──────────┼──────────┼───────────┼──────┼───────┼──────┼────────────┤
╰────┴─────────┴──────────┴──────────┴───────────┴──────┴───────┴──────┴────────────╯
```


## MSSQL에 TQL로 쓰기

```js
BYTES(payload() ?? `{
  "id":1,
  "company": "acme",
  "employee": 10
}`)
SCRIPT("tengo", {
  // get current time
  times := import("times")
  ts := times.now()
  // get tql context
  ctx := import("context")
  val := ctx.value()
  // parse json
  json := import("json")
  msg := json.decode(val[0])
  ctx.yield(msg.id, msg.company, msg.employee, ts)
})
INSERT(bridge("ms"), table("ms_example"), "id", "company", "employee", "created_on")
```

```
machbase-neo» bridge query ms select id, company, employee, created_on from ms_example;
╭────┬─────────┬──────────┬───────────────────────────────────╮
│ ID │ COMPANY │ EMPLOYEE │ CREATED_ON                        │
├────┼─────────┼──────────┼───────────────────────────────────┤
│  1 │ acme    │       10 │ 2023-08-11 20:55:49.527 +0900 KST │
╰────┴─────────┴──────────┴───────────────────────────────────╯
```

## MSSQL에서 TQL로 읽기

```js
SQL(bridge('ms'), "select * from ms_example")
CSV()
```
