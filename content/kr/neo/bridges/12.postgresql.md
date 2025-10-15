---
title: 브리지 - PostgreSQL
type: docs
weight: 12
---

## PostgreSQL 브리지 등록

PostgreSQL 데이터베이스에 연결할 브리지를 등록합니다.

```
bridge add -t postgres pg host=127.0.0.1 port=5432 user=dbuser dbname=postgres sslmode=disable;
```

연결 옵션은 다음과 같습니다.

| Option            | 설명                                                         | example         |
| :-----------      | :------------------------------------------------------------ | :-------------  |
| `dbname`          | 연결할 데이터베이스 이름                                      |                 |
| `user`            | 접속에 사용할 사용자 이름                                     |                 |
| `password`        | 사용자 비밀번호                                               |                 |
| `host`            | 접속할 호스트. `/`로 시작하면 유닉스 도메인 소켓을 의미하며 기본값은 localhost | `host=127.0.0.1` |
| `port`            | 포트 번호, 기본값은 `5432`                                    |                 |
| `sslmode`         | SSL 사용 여부(기본값 `require`), 아래 표 참고                 | (see below)     |
| `connect_timeout` | 접속 대기 시간(초). 0 또는 미지정 시 무한 대기               |                 |
| `sslcert`         | PEM 형식 인증서 파일 경로                                     |                 |
| `sslkey`          | PEM 형식 개인 키 파일 경로                                    |                 |
| `sslrootcert`     | PEM 형식 루트 인증서 파일 경로                                |                 |

<!-- | `fallback_application_name` | An application_name to fall back to if one isn't provided. | -->

`sslmode`에는 다음 값이 가능합니다.

| sslmode       | 설명                                                                                     |
|:------------  | :----------------------------------------------------------------------------------------|
| `disable`     | SSL 사용 안 함                                                                           |
| `require`     | 항상 SSL 사용(인증서 검증 생략)                                                          |
| `verify-ca`   | 항상 SSL 사용(서버 인증서가 신뢰할 수 있는 CA에 의해 서명되었는지 검증)                 |
| `verify-full` | 항상 SSL 사용(서버 인증서를 검증하고 인증서의 호스트명이 실제 호스트와 일치하는지 확인) |


## 테이블 생성

machbase-neo 셸에서 아래 명령을 실행해 `pg` 브리지를 통해 `pg_example` 테이블을 생성합니다.

```sh
bridge exec pg CREATE TABLE IF NOT EXISTS pg_example(
    id         SERIAL PRIMARY KEY,
    company    VARCHAR(50) UNIQUE NOT NULL,
    employee   INT,
    discount   REAL,
    plan       FLOAT(8),
    code       UUID,
    valid      BOOL,
    memo       TEXT,
    created_on TIMESTAMP NOT NULL
);
```

`psql` 커맨드라인 도구로 테이블이 생성되었는지 확인할 수 있습니다.

```
postgres=# \d pg_example;
                                        Table "public.pg_example"
   Column   |            Type             | Collation | Nullable |                Default                 
------------+-----------------------------+-----------+----------+----------------------------------------
 id         | integer                     |           | not null | nextval('pg_example_id_seq'::regclass)
 company    | character varying(50)       |           | not null | 
 employee   | integer                     |           |          | 
 discount   | real                        |           |          | 
 plan       | real                        |           |          | 
 code       | uuid                        |           |          | 
 valid      | boolean                     |           |          | 
 memo       | text                        |           |          | 
 created_on | timestamp without time zone |           | not null | 
Indexes:
    "pg_example_pkey" PRIMARY KEY, btree (id)
    "pg_example_company_key" UNIQUE CONSTRAINT, btree (company)

```

## PostgreSQL에 TQL로 쓰기

```js
BYTES(payload() ?? `{
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
  ctx.yield(msg.company, msg.employee, ts)
})
INSERT(bridge("pg"), table("pg_example"), "company", "employee", "created_on")
```

```
postgres=# select * from pg_example;
 id | company | employee | discount | plan | code | valid | memo |         created_on         
----+---------+----------+----------+------+------+-------+------+----------------------------
  1 | acme    |       10 |          |      |      |       |      | 2023-08-09 11:05:30.039961
(1 row)
```

## PostgreSQL에서 TQL로 읽기

```js
SQL(bridge('pg'), "select * from pg_example")
CSV()
```
