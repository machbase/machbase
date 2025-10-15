---
title: "@jsh/db"
type: docs
weight: 10
---

{{< neo_since ver="8.0.52" />}}


## Client

데이터베이스 클라이언트 객체입니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const db = require("@jsh/db");
const client = new db.Client();
try {    
    conn = client.connect();
    rows = conn.query("select * from example limit 10")
    cols = rows.columns()
    console.log("cols.names:", JSON.stringify(cols.columns));
    console.log("cols.types:", JSON.stringify(cols.types));
    
    count = 0;
    for (const rec of rows) {
        console.log(...rec);
        count++;
    }
    console.log("rows:", count, "selected" );
} catch(e) {
    console.log("Error:", e);
} finally {
    if (rows) rows.close();
    if (conn) conn.close();
}
```

<h6>생성</h6>

| 생성자               | 설명                                      |
|:---------------------|:------------------------------------------|
| new Client(*options*) | 옵션과 함께 데이터베이스 클라이언트를 생성합니다. |

`bridge`와 `driver`를 모두 지정하지 않으면 기본적으로 내부 Machbase DBMS에 연결합니다.

<h6>옵션</h6>

| 옵션                | 타입        | 기본값    | 설명                                              |
|:--------------------|:------------|:----------|:--------------------------------------------------|
| lowerCaseColumns    | Boolean     | `false`   | 결과 객체에 컬럼 이름을 소문자로 매핑합니다.      |

드라이버 옵션

사전 정의된 브리지가 없어도 `driver`와 `dataSource`를 이용해 `sqlite`, `mysql`, `mssql`, `postgresql`, `machbase`에 직접 연결할 수 있습니다.

| 옵션                | 타입        | 기본값    | 설명                       |
|:--------------------|:------------|:----------|:---------------------------|
| driver              | String      |           | 사용할 드라이버 이름       |
| dataSource          | String      |           | 데이터베이스 연결 문자열   |

브리지 옵션

미리 정의된 브리지를 사용해 Client를 생성할 수도 있습니다.

| 옵션                | 타입        | 기본값    | 설명                       |
|:--------------------|:------------|:----------|:---------------------------|
| bridge              | String      |           | 사용할 브리지 이름        |

<h6>프로퍼티</h6>

| 프로퍼티           | 타입       | 설명                                         |
|:-------------------|:-----------|:---------------------------------------------|
| supportAppend      | Boolean    | "Append" 모드를 지원하면 `true`입니다.       |

### connect()

데이터베이스에 연결합니다.

<h6>반환값</h6>

- `Object` [Conn](#Conn)


## Conn

### close()

연결을 종료하고 자원을 해제합니다.

<h6>사용 형식</h6>

```js
close()
```

### query()

<h6>사용 형식</h6>

```js
query(String *sqlText*, any ...*args*)
```

<h6>반환값</h6>

- `Object` [Rows](#rows)

### queryRow()

<h6>사용 형식</h6>

```js
queryRow(String *sqlText*, any ...*args*)
```

<h6>반환값</h6>

- `Object` [Row](#Row)


### exec()

<h6>사용 형식</h6>

```js
exec(sqlText, ...args)
```

<h6>매개변수</h6>

- `sqlText` `String` 실행할 SQL 문자열입니다.
- `args` `any` SQL에 바인딩할 가변 인자입니다.

<h6>반환값</h6>

- `Object` [Result](#result)

### appender()

새로운 "appender"를 생성합니다.

<h6>사용 형식</h6>

```js
appender(table_name, ...columns)
```

<h6>매개변수</h6>

- `table_name` `String` 데이터를 추가할 테이블 이름입니다.
- `columns` `String` 가변 길이 컬럼 목록입니다. 생략하면 테이블의 모든 컬럼 순서대로 사용합니다.

<h6>반환값</h6>

- `Object` [Appender](#appender)

## Rows

Rows 객체는 쿼리 실행 결과 집합을 캡슐화합니다.

`Symbol.iterator`를 구현하여 다음 두 가지 패턴을 모두 지원합니다.

```js
for(rec := rows.next(); rec != null; rec = rows.next()) {
    console.log(...rec);
}

for (rec of rows) {
    console.log(...rec);
}
```

### close()

데이터베이스 스테이트먼트를 해제합니다.

<h6>사용 형식</h6>

```js
close()
```

<h6>매개변수</h6>

없음.

<h6>반환값</h6>

- `any[]`

### next()

다음 레코드를 읽어옵니다. 더 이상 레코드가 없으면 `null`을 반환합니다.

<h6>사용 형식</h6>

```js
next()
```

<h6>매개변수</h6>

없음.

<h6>반환값</h6>

- `any[]`

### columns()

<h6>사용 형식</h6>

```js
columns()
```

<h6>매개변수</h6>

없음.

<h6>반환값</h6>

- `Object` [Columns](#columns)

### columnNames()

<h6>사용 형식</h6>

```js
columnNames()
```

<h6>매개변수</h6>

없음.

<h6>반환값</h6>

- `String[]`

### columnTypes()

<h6>사용 형식</h6>

```js
columnTypes()
```

<h6>매개변수</h6>

없음.

<h6>반환값</h6>

- `String[]`


## Row

Row 객체는 단일 레코드를 반환하는 `queryRow` 결과를 다룹니다.

### columns()

<h6>사용 형식</h6>

```js
columns()
```

<h6>매개변수</h6>

없음.

<h6>반환값</h6>

- `Object` [Columns](#columns)


### columnNames()

결과 컬럼 이름을 반환합니다.

<h6>사용 형식</h6>

```js
columnNames()
```

<h6>매개변수</h6>

없음.

<h6>반환값</h6>

- `String[]`

### columnTypes()

결과 컬럼 타입을 반환합니다.

<h6>사용 형식</h6>

```js
columnTypes()
```

<h6>매개변수</h6>

없음.

<h6>반환값</h6>

- `String[]`

### values()

컬럼 값을 배열로 반환합니다.

<h6>사용 형식</h6>

```js
values()
```

<h6>매개변수</h6>

없음.

<h6>반환값</h6>

- `any[]`

## Result

Result 객체는 `exec()` 실행 결과와 부가 정보를 제공합니다.

<h6>프로퍼티</h6>

| 프로퍼티           | 타입       | 설명               |
|:-------------------|:-----------|:-------------------|
| message            | String     | 결과 메시지        |
| rowsAffected       | Number     | 영향을 받은 행 수  |

## Columns

<h6>프로퍼티</h6>

| 프로퍼티           | 타입       | 설명                 |
|:-------------------|:-----------|:---------------------|
| columns            | String[]   | 결과 컬럼 이름 목록  |
| types              | String[]   | 결과 컬럼 타입 목록  |

## Appender

### append()

컬럼 순서에 맞춰 값을 지정하여 행을 추가합니다.

<h6>사용 형식</h6>

```js
append(...values)
```

<h6>매개변수</h6>

- `values` `any` 지정한 컬럼 순서에 맞춰 삽입할 값 목록입니다.

<h6>반환값</h6>

없음.

### close()

Appender를 닫습니다.

<h6>사용 형식</h6>

```js
close()
```

<h6>매개변수</h6>

없음.

<h6>반환값</h6>

없음.

### result()

Appender를 닫은 뒤 마지막 append 결과를 반환합니다.

<h6>사용 형식</h6>

```js
result()
```

<h6>매개변수</h6>

없음.

<h6>반환값</h6>

- `Object`

| Property           | Type       | Description        |
|:-------------------|:-----------|:-------------------|
| success            | Number     |                    |
| faile              | Number     |                    |
