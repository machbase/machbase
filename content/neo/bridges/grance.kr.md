---
title: 브리지와 구독자
type: docs
weight: 1
---

## 브리지

### 브리지 등록

SQLite 연결을 등록합니다.

~~~
bridge add -t sqlite sqlitedb file:/data/sqlite.db;
~~~

### 등록된 브리지 조회

~~~
bridge list
┌──────────┬────────┬────────────────────────┐
│ NAME     │ TYPE   │ CONNECTION             │
├──────────┼────────┼────────────────────────┤
│ sqlitedb │ sqlite │ file:/data/sqlite.db   │
└──────────┴────────┴────────────────────────┘
~~~

### 브리지에서 명령 실행

~~~
bridge exec sqlitedb CREATE TABLE IF NOT EXISTS example(id INTEGER NOT NULL PRIMARY KEY, name TEXT, age TEXT, address TEXT, UNIQUE(name));
~~~


### 브리지에서 조회 실행

> `bridge query` 명령은 "SQL" 타입 브리지에서만 사용할 수 있습니다.

~~~
bridge query sqlitedb select * from example;

┌────┬────────┬─────┬───────────────┐
│ ID │ NAME   │ AGE │ ADDRESS       │
├────┼────────┼─────┼───────────────┤
│  1 │ hong_1 │ 20  │ address for 1 │
│  2 │ hong_2 │ 20  │ address for 2 │
│  3 │ hong_3 │ 20  │ address for 3 │
└────┴────────┴─────┴───────────────┘
~~~


### TQL `SQL()`에서 브리지 사용

`SQL()` 함수는 "SQL" 타입 브리지와 함께 `bridge()` 옵션을 받아 지정한 SQL을 실행합니다.

~~~js
SQL(bridge("sqlitedb"), `select * from example`)
CSV()
~~~

### TQL `SCRIPT()`에서 브리지 사용

아래 예시처럼 `SCRIPT()` 내에서 `$.db({bridge:"name"})`를 호출하면 데이터베이스 타입 브리지에 접근할 수 있습니다.
이 기능은 8.0.27 버전부터 지원됩니다.

~~~js
SCRIPT({
    err = $.db({bridge:"mem"})
     .query("select company, employee, created_on from mem_example")
     .forEach( function(fields){
        $.yield(fields[0], fields[1], fields[2]);
     })
    if (err !== undefined) {
        console.error("result", ret);
    }
})
CSV()
~~~

### 다른 데이터베이스로 데이터 복사

다음 예시는 Machbase 데이터를 SQLite 브리지로 복사하는 방법을 보여 줍니다.

**브리지**

아래 설정으로 `sqlite` 브리지를 정의합니다.

- 타입: `SQLite`
- 연결 문자열: `file:///tmp/sqlite.db`

**SQL**

`/tmp/sqlite.db`에 위치한 SQLite 데이터베이스에 `example` 테이블을 생성합니다.

~~~sql
--env: bridge=sqlite
CREATE TABLE IF NOT EXISTS example (
    NAME TEXT,
    TIME DATETIME,
    VALUE REAL
);
-- env: reset
~~~

**TQL**

아래 TQL 스크립트는 `SQL()`로 데이터를 조회한 뒤, `INSERT()`에 `bridge("sqlite")`를 지정해 SQLite 데이터베이스로 적재합니다.

~~~js
SQL(`select name, time, value from example where name = 'my-car'`)
INSERT(bridge("sqlite"), "name", "time", "value", table("example"))
~~~

## 구독자

*Subscriber*는 외부 메시지 브로커와 연결해 스트리밍 메시지를 수신하고, TQL 스크립트로 데이터를 적재하는 역할을 합니다.

현재 machbase-neo는 외부 MQTT 브로커와의 연결을 지원하며, 향후 NATS와 Kafka도 지원할 예정입니다.

가장 단순한 사용 예시는 외부 MQTT 브로커에 대한 브리지를 만든 뒤, ① 해당 브리지 ② 구독할 토픽 ③ 메시지를 처리할 TQL 스크립트 경로를 지정해 구독자를 등록하는 것입니다.
이후 machbase-neo는 MQTT 클라이언트로 동작하며 메시지를 수신할 때마다 지정한 TQL 스크립트로 전달합니다.


~~~mermaid
flowchart RL
    external-system --PUBLISH--> machbase-neo
    machbase-neo --SUBSCRIBE--> external-system
    subgraph machbase-neo
        direction RL
        bridge --> subscriber
        subscriber["Subscriber
                    TQL"] --Write--> machbase
        machbase[("machbase
                    engine")]
    end
    subgraph external-system
        direction RL
        client["Client"] --PUBLISH--> mqtt[["MQTT
                                            Broker"]]
    end
~~~

### 구독자 등록

구독자를 등록합니다.

**형식:** `subscriber add [options] <name> <bridge> <topic> <tql-path>`

- 옵션
    - `--autostart` machbase-neo 시작 시 자동으로 구독자를 실행합니다. 비자동 모드에서는 `subscriber start <name>`, `subscriber stop <name>`으로 수동 제어합니다.
    - `--qos <int>` 브리지가 MQTT 타입일 때 토픽 구독의 QoS 레벨을 지정합니다. `0`, `1`을 지원하며 기본값은 `0`입니다.
    - `--queue <string>` 브리지가 NATS 타입일 때 사용할 Queue Group을 지정합니다.

- `<name>`      구독자 이름
- `<bridge>`    미리 정의한 브리지 이름(브로커 타입과 일치해야 합니다)
- `<topic>`     구독할 토픽
- `<tql-path>`  수신 메시지를 처리할 TQL 스크립트 경로


### 구독자 상태 확인

**형식:** `subscriber list`

- `STOP`
- `RUNNING`

### 구독자 시작/중지

**형식:** `subscriber [start | stop] <name>`

### 구독자 삭제

**형식:** `subscriber del <name>`
