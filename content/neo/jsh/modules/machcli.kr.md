---
title: "machcli"
type: docs
weight: 100
---

{{< neo_since ver="8.0.73" />}}

`machcli` 모듈은 JSH 애플리케이션에서 Machbase 데이터베이스를 사용할 수 있는 클라이언트 API를 제공합니다.

## Client

데이터베이스 클라이언트를 생성합니다.

<h6>사용 형식</h6>

```js
new Client(config)
```

<h6>설정 필드</h6>

- `host` (기본값: `127.0.0.1`)
- `port` (기본값: `5656`)
- `user` (기본값: `sys`)
- `password` (기본값: `manager`)
- `alternativeHost` (선택)
- `alternativePort` (선택)

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const { Client } = require('machcli');
const db = new Client({ host: '127.0.0.1', port: 5656, user: 'sys', password: 'manager' });
```

**Client.connect()**

연결을 열고 `Connection` 객체를 반환합니다.

<h6>사용 형식</h6>

```js
connect()
```

**Client.close()**

내부 데이터베이스 클라이언트를 종료합니다.

<h6>사용 형식</h6>

```js
close()
```

**Client.user()**

설정된 사용자 이름(대문자)을 반환합니다.

<h6>사용 형식</h6>

```js
user()
```

**Client.normalizeTableName()**

테이블 이름을 `[database, user, table]` 형식으로 정규화합니다.

<h6>사용 형식</h6>

```js
normalizeTableName(tableName)
```

## Connection

`Client.connect()`가 반환하는 연결 객체입니다.

**Connection.query()**

조회 SQL을 실행하고 `Rows` 객체를 반환합니다.

<h6>사용 형식</h6>

```js
query(sql[, ...params])
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[12]}
const { Client } = require('machcli');
var db, conn, rows;
const conf = {
    host: '127.0.0.1',
    port: 5656,
    user: 'sys',
    password: 'manager' 
};
try {
    db = new Client(conf);
    conn = db.connect();
    rows = conn.query('SELECT NAME, TIME, VALUE FROM TAG LIMIT ?', 1);
    for (const row of rows) {
        console.println(row.NAME, row.TIME, row.VALUE);
    }
} catch( e ) {
    console.println("ERROR", e.message);
}
rows && rows.close();
conn && conn.close();
db && db.close();
```

**Connection.queryRow()**

조회 SQL을 실행하고 단일 행 객체를 반환합니다.

반환 객체에는 `_ROWNUM`과 각 컬럼명이 프로퍼티로 포함됩니다.

<h6>사용 형식</h6>

```js
queryRow(sql[, ...params])
```

**Connection.exec()**

DDL/DML을 실행하고 결과 객체를 반환합니다.

반환 필드:

- `rowsAffected`
- `message`

<h6>사용 형식</h6>

```js
exec(sql[, ...params])
```

**Connection.explain()**

실행 계획 문자열을 반환합니다.

<h6>사용 형식</h6>

```js
explain(sql[, ...params])
```

**Connection.append()**

대량 입력용 appender 객체를 생성합니다.

반환된 appender는 `append()`, `flush()`, `close()` 같은 메서드를 지원합니다.

<h6>사용 형식</h6>

```js
append(tableName)
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[4,6]}
const { Client } = require('machcli');
const db = new Client({ host: '127.0.0.1', port: 5656, user: 'sys', password: 'manager' });
const conn = db.connect();
const appender = conn.append('TAG');
appender.append('sensor-1', new Date(), 12.34);
appender.flush();
const result = appender.close();
console.println(result);
conn.close();
db.close();
```

**Connection.close()**

연결을 종료합니다.

<h6>사용 형식</h6>

```js
close()
```

## Rows

`Connection.query()`가 반환하는 결과 집합 객체입니다.

**Rows.message**

조회 실행 결과 메시지입니다.

**Rows.isFetchable()**

행을 가져올 수 있는 결과인지 반환합니다.

<h6>사용 형식</h6>

```js
isFetchable()
```

**Rows.next()**

이터레이터 결과 객체를 반환합니다.

- 행이 있으면 `{ value: Row, done: false }`
- 완료되면 `{ done: true }`

<h6>사용 형식</h6>

```js
next()
```

**Rows.close()**

결과 집합을 닫습니다.

<h6>사용 형식</h6>

```js
close()
```

## Row

조회된 행을 나타내는 객체입니다.

- 각 컬럼은 `row.COLUMN_NAME`으로 접근할 수 있습니다.
- `for...of` 반복을 지원합니다.

## queryDatabaseId()

마운트된 데이터베이스의 backup tablespace ID를 반환합니다.

- 기본 DB(`''` 또는 `MACHBASEDB`)는 `-1` 반환
- 데이터베이스가 없으면 예외를 발생시킵니다.

<h6>사용 형식</h6>

```js
queryDatabaseId(conn, dbName)
```

## queryTableType()

정규화된 테이블 이름 토큰으로 테이블 타입 코드를 반환합니다.

<h6>사용 형식</h6>

```js
queryTableType(conn, names)
```

## TableType

**stringTableType()**

테이블 타입 상수와 문자열 변환 함수입니다.

<h6>TableType 값</h6>

- `Log`, `Fixed`, `Volatile`, `Lookup`, `KeyValue`, `Tag`

<h6>사용 형식</h6>

```js
stringTableType(type)
```

## TableFlag

**stringTableFlag()**

테이블 플래그 상수와 문자열 변환 함수입니다.

<h6>TableFlag 값</h6>

- `None`, `Data`, `Rollup`, `Meta`, `Stat`

<h6>사용 형식</h6>

```js
stringTableFlag(flag)
```

**stringTableDescription()**

테이블 타입/플래그를 결합한 설명 문자열을 반환합니다.

<h6>사용 형식</h6>

```js
stringTableDescription(type, flag)
```

## ColumnType

**stringColumnType()**

컬럼 타입 상수와 문자열 변환 함수입니다.

<h6>주요 ColumnType 값</h6>

- `Short`, `UShort`, `Integer`, `UInteger`, `Long`, `ULong`
- `Float`, `Double`, `Varchar`, `Text`, `Clob`, `Blob`, `Binary`
- `Datetime`, `IPv4`, `IPv6`, `JSON`

<h6>사용 형식</h6>

```js
stringColumnType(columnType)
```

**columnWidth()**

컬럼 타입의 기본 표시 폭을 반환합니다.

<h6>사용 형식</h6>

```js
columnWidth(columnType, length)
```

## ColumnFlag

**stringColumnFlag()**

컬럼 플래그 상수와 문자열 변환 함수입니다.

<h6>ColumnFlag 값</h6>

- `TagName`
- `Basetime`
- `Summarized`
- `MetaColumn`

<h6>사용 형식</h6>

```js
stringColumnFlag(flag)
```
