---
title: SCRIPT()
type: docs
weight: 55
---

TQL은 **SRC**와 **MAP** 컨텍스트에서 JavaScript를 활용할 수 있는 `SCRIPT()` 함수를 제공합니다 {{< neo_since ver="8.0.36" />}}.
익숙한 프로그래밍 언어로 로직을 작성해 보다 유연하고 강력한 스크립트를 구성할 수 있습니다.

*구문*: `SCRIPT({main_code})`

*구문*: `SCRIPT({init_code}, {main_code})`

*구문*: `SCRIPT({init_code}, {main_code}, {deinit_code})`

- *init_code*: 초기화 코드(선택 사항이며, *deinit_code*가 있을 경우 필수)
- *main_code*: 필수 실행 코드
- *deinit_code*: 종료 시 실행할 코드(선택 사항)

`init_code`는 선택 사항이며 처음 한 번만 실행됩니다. `main_code`는 반드시 작성해야 합니다.

**주의 사항**

현재 `SCRIPT()`는 Goja 기반 JavaScript 실행 환경을 사용합니다.
Typed Array, 템플릿 리터럴(백틱 문자열), `const`, 화살표 함수를 사용할 수 있습니다.
`"use strict"`를 사용한 엄격 모드도 동작합니다.
정규 표현식의 전방 탐색(`(?=...)`, `(?!...)`)과 역참조(`\1` 등)도 사용할 수 있습니다.
지원되는 언어 기능은 사용하는 Machbase Neo에 포함된 실행 환경의 버전을 따릅니다.

## JSH 모듈

{{< neo_since ver="8.0.52" />}}

`require()`를 통해 `SCRIPT()` 안에서 JSH 모듈을 가져올 수 있습니다.

```js
SCRIPT({
    const { arrange } = require("mathx")
    arrange(0, 6, 3).forEach((i) =>$.yield(i))
})
CSV()
```

## 컨텍스트 객체

Machbase Neo는 `$` 변수를 컨텍스트 객체로 제공합니다. JavaScript는 이 객체를 통해 레코드와 데이터베이스에 접근하거나 새로운 레코드를 방출할 수 있습니다.

- `$.payload` : 요청 본문 데이터. `SCRIPT()`가 SRC 노드일 때만 존재하며, 그렇지 않으면 `undefined`입니다.
- `$.params` : 요청의 쿼리 파라미터.
- `$.result` : `SCRIPT()` 함수가 방출할 결과 컬럼 이름과 타입을 지정합니다.
- `$.key`, `$.values` : 현재 레코드의 키와 값에 접근합니다. MAP 컨텍스트에서만 사용할 수 있습니다.
- `$.yield()` : 값만 전달해 새 레코드를 방출합니다.
- `$.yieldKey()` : 키와 값을 함께 전달해 새 레코드를 방출합니다.
- `$.yieldArray()` : `$.yield()`와 같지만, 여러 인자 대신 배열 타입 인자 하나만 받습니다.
- `$.db()` : 새로운 데이터베이스 연결을 반환합니다.
- `$.db().query()` : SQL 질의를 실행합니다.
- `$.db().exec()` : SELECT 이외의 SQL을 실행합니다.
- `$.request().do()` : 원격 서버로 HTTP 요청을 보냅니다.

### `$.payload`

`$.payload`를 통해 요청 본문 데이터를 읽을 수 있습니다. 입력 데이터가 없으면 `undefined`입니다.
SRC 노드로 사용할 때만 접근할 수 있습니다.

```js {{linenos=table,hl_lines=[2]}}
SCRIPT({
    var data = $.payload;
    if (data === undefined) {
        data = '{ "prefix": "name", "offset": 0, "limit": 10}';
    }
    var obj = JSON.parse(data);
    $.yield(obj.prefix, obj.offset, obj.limit);
})
CSV()
```

요청 본문 없이 호출하면 `$.payload`는 `undefined`입니다.

```sh
curl -o - -X POST http://127.0.0.1:5654/db/tql/test.tql
```

결과는 기본값 `name,0,10`이 됩니다.

요청 본문을 함께 전달하면 다음과 같이 동작합니다.

```sh
curl -o - -X POST http://127.0.0.1:5654/db/tql/test.tql \
-d '{"prefix":"testing", "offset":10, "limit":10}'
```

결과: `testing,10,10`

### `$.params`

`$.params`는 요청 쿼리 파라미터를 제공합니다.
점 표기(`$.params.name`)와 대괄호 표기(`$.params["name"]`)를 모두 사용할 수 있습니다.

```js {{linenos=table,hl_lines=["2-4"]}}
SCRIPT({
    var prefix = $.params.prefix ? $.params.prefix : "name";
    var offset = $.params.offset ? $.params.offset : 0;
    var limit = $.params.limit ? $.params.limit: 10;
    $.yield(prefix, offset, limit);
})
CSV()
```

파라미터 없이 호출하면:

```sh
curl -o - -X POST http://127.0.0.1:5654/db/tql/test.tql
```

결과: `name,0,10`

파라미터를 전달하면:

```sh
curl -o - -X POST "http://127.0.0.1:5654/db/tql/test.tql?prefix=testing&offset=12&limit=20"
```

결과: `testing,12,20`

### `$.result`

`SCRIPT`가 방출할 결과 컬럼과 타입을 정의합니다.
다음 예시처럼 초기화 코드 구간에서 설정합니다.

```js {{linenos=table,hl_lines=["2-5"]}}
SCRIPT({
    $.result = {
        columns: ["val", "sig"],
        types: ["double", "double"] 
    }
},{
    for (i = 1.0; i <= 5.0; i+=0.03) {
        val = Math.round(i*100)/100;
        sig = Math.sin( 1.2*2*Math.PI*val );
        $.yield( val, sig );
    }
})
JSON()
```

### `$.key`

현재 레코드의 키에 접근합니다. MAP 컨텍스트에서만 정의되며, SRC일 때는 `undefined`입니다.

```js {{linenos=table,hl_lines=["7"]}}
SCRIPT({
    for( i = 0; i < 3; i++) {
        $.yieldKey(i, "hello-"+(i+1));
    }
})
SCRIPT({
    $.yieldKey($.key, $.values[0], 'key is '+$.key);
})
CSV()
```

```csv
hello-1,key is 0
hello-2,key is 1
hello-3,key is 2
```

### `$.values`

현재 레코드의 값 배열에 접근합니다. MAP 컨텍스트에서만 사용할 수 있으며, SRC일 때는 `undefined`입니다.

```js {{linenos=table,hl_lines=["7"]}}
SCRIPT({
        $.yield("string", 10, 3.14);
})
SCRIPT({
    $.yield(
        "the first value is "+$.values[0],
        "2nd value is "+$.values[1],
        "3rd is "+$.values[2]
    );
})
CSV()
```

출력:

`the first value is string,2nd value is 10,3rd is 3.14`

### `$.yield()`

새 레코드를 다음 단계로 방출합니다. 키에는 순차적으로 증가하는 번호가 자동으로 할당됩니다.

```js
$.yield(field1, field2, field3);
```

### `$.yieldKey()`

`yieldKey()`는 `$.yield()`와 비슷하게 동작하지만, 첫 번째 인자로 레코드의 키를 지정합니다.

```js
$.yieldKey(key, field1, field2, field3);
```

### `$.yieldArray()`

{{< neo_since ver="8.0.39" />}}

배열에 담긴 레코드를 방출합니다.
가변 길이 인자를 받는 `$.yield()`와 달리, `$.yieldArray()`는 레코드를 나타내는 배열 하나를 인자로 받습니다.
배열을 다룰 때 유용합니다.

```js
var arr = [];
for( i = 0; i < unknown; i++) {
    arr.push(field_values[i]);
}
$.yieldArray(arr);
```

### `$.db()`

새로운 데이터베이스 연결을 반환합니다. 이 연결은 `query()`, `exec()` 함수를 제공합니다.

`$.db({bridge: "sqlite"})`처럼 *option* 객체를 인자로 지정하면,
Machbase 데이터베이스 대신 브리지로 연결한 데이터베이스에 대한 새 연결을 반환합니다.

**옵션**

option 파라미터는 다음 버전부터 지원합니다 {{< neo_since ver="8.0.37" />}}.

```js
{
    bridge: "name", // bridge name
}
```

### `$.db().query()`

JavaScript에서 `$.db().query()`로 데이터베이스를 조회할 수 있습니다.
`query()`의 반환값에 `forEach()`로 콜백 함수를 적용해 조회 결과를 순회합니다.

`.forEach()`의 콜백 함수가 명시적으로 `false`를 반환하면 순회가 즉시 중단됩니다.
콜백 함수가 `true`를 반환하거나 아무것도 반환하지 않으면(`undefined`를 반환하면),
조회 결과의 끝까지 순회를 계속합니다.

{{< tabs >}}

{{< tab name="MACHBASE" >}}

```js {{linenos=table,hl_lines=["7-10",14]}}
SCRIPT({
  var data = $.payload;
  if (data === undefined) {
    data = '{ "tag": "cpu.percent", "offset": 0, "limit": 3 }';
  }
  var obj = JSON.parse(data);
  $.db()
   .query("SELECT name, time, value FROM example WHERE name = ? LIMIT ?, ?",
    obj.tag, obj.offset, obj.limit
  ).forEach( function(row){
    name = row[0]
    time = row[1]
    value = row[2]
    $.yield(name, time, value);
  })
})
CSV()
```

```csv
cpu.percent,1725330085908925000,73.9
cpu.percent,1725343895315420000,73.6
cpu.percent,1725343898315887000,6.1
```

{{< /tab >}}

{{< tab name="BRIDGE-SQLITE" >}}

```js {{linenos=table,hl_lines=["7-10",14]}}
SCRIPT({
  var data = $.payload;
  if (data === undefined) {
    data = '{ "tag": "testing", "offset": 0, "limit": 3 }';
  }
  var obj = JSON.parse(data);
  $.db({bridge:"mem"})
   .query("SELECT name, time, value FROM example WHERE name = ? LIMIT ?, ?",
    obj.tag, obj.offset, obj.limit
  ).forEach( function(row){
    name = row[0]
    time = row[1]
    value = row[2]
    $.yield(name, time, value);
  })
})
CSV()
```

```csv
testing,1732589744886,16.70559756851126
testing,1732589744886,49.93214293713331
testing,1732589744886,54.485508690434905
```

{{< /tab >}}

{{< /tabs >}}

`$.db().query()`의 결과에서 특정 컬럼을 골라 `$.yield()`로 방출할 수 있습니다.
모든 컬럼을 한 번에 방출하려면 `$.yieldArray()`를 사용합니다 {{< neo_since ver="8.0.39" />}}.

```js {{linenos=table,hl_lines=["4"]}}
SCRIPT({
    var sql = "SELECT name, time, value FROM example WHERE name = 'cpu.percent' LIMIT 3";
    $.db().query(sql).forEach( function(row){
        $.yieldArray(row);
    });
})
CSV()
```

또는 `$.db().query().yield()`를 사용해 자동으로 방출할 수 있습니다 {{< neo_since ver="8.0.39" />}}.

```js {{linenos=table,hl_lines=["9"]}}
SCRIPT({
    var tags = ["mem.total", "mem.used", "mem.free"];
    for( i = 0; i < tags.length; i++) {
        $.yield(tags[i]);
    }
})
SCRIPT({
    var sql = "SELECT * FROM example WHERE name = ? LIMIT 1";
    $.db().query(sql, $.values[0]).yield();
})
CSV( header(true) )
```

### `$.db().exec()`

SELECT 문이 아닌 SQL은 `$.db().exec()`로 실행합니다. INSERT, DELETE, CREATE TABLE 문 등이 해당됩니다.

{{< tabs >}}

{{< tab name="MACHBASE" >}}

```js {{linenos=table,hl_lines=["10-14", "21-22"]}}
SCRIPT({
    for( i = 0; i < 3; i++) {
        ts = Date.now()*1000000; // ms to ns
        $.yield("testing", ts, Math.random()*100);
    }
})
SCRIPT({
    // This section contains initialization code
    // that runs once before processing the first record.
    err = $.db().exec("CREATE TAG TABLE IF NOT EXISTS example ("+
        "NAME varchar(80) primary key,"+
        "TIME datetime basetime,"+
        "VALUE double"+
    ")");
    if (err instanceof Error) {
        console.error("Fail to create table", err.message);
    }
}, {
    // This section contains the main code
    // that runs over every record.
    err = $.db().exec("INSERT INTO example values(?, ?, ?)", 
        $.values[0], $.values[1], $.values[2]);
    if (err instanceof Error) {
        console.error("Fail to insert", err.message);
    } else {
        $.yield($.values[0], $.values[1], $.values[2]);
    }
})
CSV()
```

{{< /tab >}}

{{< tab name="BRIDGE-SQLITE" >}}

```js {{linenos=table,hl_lines=["10-14", "21-22"]}}
SCRIPT({
    for( i = 0; i < 3; i++) {
        ts = Date.now(); // ms
        $.yield("testing", ts, Math.random()*100);
    }
})
SCRIPT({
    // This section contains initialization code
    // that runs once before processing the first record.
    err = $.db({bridge:"mem"}).exec("CREATE TABLE IF NOT EXISTS example ("+
        "NAME TEXT,"+
        "TIME INTEGER,"+
        "VALUE REAL"+
    ")");
    if (err instanceof Error) {
        console.error("Fail to create table", err.message);
    }
}, {
    // This section contains the main code
    // that runs over every record.
    err = $.db({bridge:"mem"}).exec("INSERT INTO example values(?, ?, ?)", 
        $.values[0], $.values[1], $.values[2]);
    if (err instanceof Error) {
        console.error("Fail to insert", err.message);
    } else {
        $.yield($.values[0], $.values[1], $.values[2]);
    }
})
CSV()
```

SQL 에디터에서 브리지로 연결한 데이터베이스를 조회하려면 쿼리에 `-- env: bridge=name` 표기를 사용합니다.

```sql
-- env: bridge=mem
SELECT
    name,
    datetime(time/1000, 'unixepoch', 'localtime') as time,
    value
FROM
    example;
-- env: reset
```

{{< figure src="/neo/tql/img/script_js_db_sqlite_exec.png" width="600px" >}}

{{< /tab >}}

{{< /tabs >}}

### `$.request().do()`

*구문*: `$.request(url [, option]).do(callback)`

**요청 옵션**

```js
{
    method: "GET|POST|PUT|DELETE", // default is "GET"
    headers: { "Authorization": "Bearer auth-token"}, // key value map
    body: "body content if the method is POST or PUT"
}
```

실제 요청은 응답을 처리할 콜백 함수를 지정해 `.do()`를 호출할 때 전송됩니다. 콜백 함수는 여러 속성과 메서드를 제공하는 Response 객체를 인자로 받습니다.

**응답**

| 속성             | 타입    | 설명         |
|:-----------------|:-------:|:-------------|
| `.ok`            | Boolean | 응답 상태 코드가 성공이면 `true` (`200<= status < 300`) |
| `.status`        | Number  | HTTP 응답 코드 |
| `.statusText`    | String  | 상태 코드와 메시지 (예: `200 OK`) |
| `.url`           | String  | 요청 URL |
| `.headers`       | Map     | 응답 헤더 |

Response 객체는 응답 본문을 가져오는 메서드를 제공합니다.

| 메서드                 | 설명         |
|:-----------------------|:-------------|
| `.text(callback(txt))` | 본문을 문자열로 콜백에 전달합니다 |
| `.blob(callback(bin))` | 본문을 바이너리 배열로 콜백에 전달합니다 |
| `.csv(callback(row))`  | 본문을 CSV로 파싱하고 각 행(레코드)마다 `callback()`을 호출합니다 |
<!-- | .json(callback(obj)) | 본문을 JSON 객체 또는 배열로 파싱하고 각 객체마다 callback()을 호출합니다. **아직 구현되지 않음** | -->

**사용법**

```js
$.request("https://server/path", {
    method: "GET",
    headers: { "Authorization": "Bearer auth-token" }
  }).do( function(rsp){
    console.log("ok:", rsp.ok);
    console.log("status:", rsp.status);
    console.log("statusText:", rsp.statusText);
    console.log("url:", rsp.url);
    console.log("Content-Type:", rsp.headers["Content-Type"]);
});
```

### finalize()

`SCRIPT()`의 JavaScript 코드에 `function finalize() {}`를 정의하면,
모든 레코드를 처리한 뒤 시스템이 이 함수를 자동으로 호출합니다.

다음 두 예제는 같게 동작하며, 둘 다 마지막 레코드로 `999`를 방출합니다.

```js
FAKE( arrange(1, 3, 1) )
SCRIPT({
    function finalize() {
        $.yield(999);
    }
    $.yield($.values[0]);
})
CSV()
```

```js
FAKE( arrange(1, 3, 1) )
SCRIPT({
    // init; do nothing
},{
    // main
    $.yield($.values[0]);
}, {
    // deinit;
    $.yield(999);
})
CSV()
```

이 예제는 `1`, `2`, `3`, `999`의 4개 레코드를 방출합니다.

## 예제

### Hello World

```js
SCRIPT({
    console.log("Hello World?");
})
DISCARD()
```

**결과**

{{< figure src="/neo/tql/img/script_js_helloworld.png" width="550px" >}}

### 내장 Math 객체

{{< tabs >}}

{{< tab name="JS" >}}

JavaScript 내장 함수를 사용할 수 있습니다.

```js {{linenos=table,hl_lines=["3-8"]}}
FAKE(meshgrid(linspace(0,2*3.1415,30), linspace(0, 3.1415, 20)))

SCRIPT({
  x = Math.cos($.values[0]) * Math.sin($.values[1]);
  y = Math.sin($.values[0]) * Math.sin($.values[1]);
  z = Math.cos($.values[1]);
  $.yield([x,y,z]);
})

CHART(
  plugins("gl"),
  size("600px", "600px"),
  chartOption({
    grid3D:{}, xAxis3D:{}, yAxis3D:{}, zAxis3D:{},
    visualMap:[{  min:-1, max:1, 
      inRange:{color:["#313695",  "#74add1", "#ffffbf","#f46d43", "#a50026"]
    }}],
    series:[ { type:"scatter3D", data: column(0)} ]
  })
)
```

{{< /tab >}}

{{< tab name="SET-MAP" >}}

JavaScript 대신 SET-MAP 함수로 같은 결과를 얻는 예제입니다.

```js {{linenos=table,hl_lines=["3-8"]}}
FAKE(meshgrid(linspace(0,2*3.1415,30), linspace(0, 3.1415, 20)))

SET(x, cos(value(0))*sin(value(1)))
SET(y, sin(value(0))*sin(value(1)))
SET(z, cos(value(1)))

MAPVALUE(0, list($x, $y, $z))
POPVALUE(1)

CHART(
  plugins("gl"),
  size("600px", "600px"),
  chartOption({
    grid3D:{}, xAxis3D:{}, yAxis3D:{}, zAxis3D:{},
    visualMap:[{  min:-1, max:1, 
      inRange:{color:["#313695",  "#74add1", "#ffffbf","#f46d43", "#a50026"]
    }}],
    series:[ { type:"scatter3D", data: column(0)} ]
  })
)
```

{{< /tab >}}

{{< /tabs >}}

**결과**

{{< figure src="/neo/tql/img/script_js_sphere.png" width="550px" >}}

### JSON 파싱

```js {{linenos=table,hl_lines=["11"]}}
SCRIPT({
    $.result = {
        columns: ["NAME", "AGE", "IS_MEMBER", "HOBBY"],
        types: ["string", "int32", "bool", "string"],
    }
},{
    content = $.payload;
    if (content === undefined) {
        content = '{"name":"James", "age": 24, "isMember": true, "hobby": ["book", "game"]}';
    }
    obj = JSON.parse(content);
    $.yield(obj.name, obj.age, obj.isMember, obj.hobby.join(","));
})
JSON()
```

**결과**

```json
{
    "data": {
        "columns": [ "NAME", "AGE", "IS_MEMBER", "HOBBY" ],
        "types": [ "string", "int32", "bool", "string" ],
        "rows": [ [ "James", 24, true, "book,game" ] ]
    },
    "success": true,
    "reason": "success",
    "elapse": "627.958µs"
}
```

### CSV 가져오기

```js {{linenos=table,hl_lines=["17-19"]}}
SCRIPT({
    $.result = {
        columns: ["SepalLen", "SepalWidth", "PetalLen", "PetalWidth", "Species"],
        types: ["double", "double", "double", "double", "string"]
    };
},{
    $.request("https://docs.machbase.com/assets/example/iris.csv")
     .do(function(rsp){
        console.log("ok:", rsp.ok);
        console.log("status:", rsp.status);
        console.log("statusText:", rsp.statusText);
        console.log("url:", rsp.url);
        console.log("Content-Type:", rsp.headers["Content-Type"]);
        if ( rsp.error() !== undefined) {
            console.error(rsp.error())
        }
        var err = rsp.csv(function(fields){
            $.yield(fields[0], fields[1], fields[2], fields[3], fields[4]);
        })
        if (err !== undefined) {
            console.warn(err);
        }
    })
})
CSV(header(true))
```

### JSON 텍스트 가져오기

이 예제는 원격 서버에서 JSON을 가져와 JavaScript로 파싱하는 방법을 보여 줍니다.

```js {{linenos=table,hl_lines=["17-23"]}}
SCRIPT({
    $.result = {
        columns: ["ID", "USER_ID", "TITLE", "COMPLETED"],
        types: ["int64", "int64", "string", "boolean"]
    };
},{
    $.request("https://jsonplaceholder.typicode.com/todos")
     .do(function(rsp){
        console.log("ok:", rsp.ok);
        console.log("status:", rsp.status);
        console.log("statusText:", rsp.statusText);
        console.log("URL:", rsp.url);
        console.log("Content-Type:", rsp.headers["Content-Type"]);
        if ( rsp.error() !== undefined) {
            console.error(rsp.error())
        }
        rsp.text( function(txt){
            list = JSON.parse(txt);
            for (i = 0; i < list.length; i++) {
                obj = list[i];
                $.yield(obj.id, obj.userId, obj.title, obj.completed);
            }
        })
    })
})
CSV(header(false))
```
