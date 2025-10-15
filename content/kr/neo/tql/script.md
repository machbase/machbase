---
title: SCRIPT()
type: docs
weight: 55
---

TQL은 **SRC**와 **MAP** 컨텍스트에서 JavaScript(ECMA5)를 활용할 수 있는 `SCRIPT()` 함수를 제공합니다 {{< neo_since ver="8.0.36" />}}.  
익숙한 프로그래밍 언어로 로직을 작성해 보다 유연하고 강력한 스크립트를 구성하실 수 있습니다.

*구문*: `SCRIPT({main_code})`

*구문*: `SCRIPT({init_code}, {main_code})`

*구문*: `SCRIPT({init_code}, {main_code}, {deinit_code})`

- *init_code*: 초기화 코드(선택 사항이며, *deinit_code*가 있을 경우 필수)
- *main_code*: 필수 실행 코드
- *deinit_code*: 종료 시 실행할 코드(선택 사항)

`init_code`는 처음 한 번만 실행됩니다. `main_code`는 반드시 작성해야 합니다.

**주의 사항**

- `use strict`는 효과가 없습니다.
- ECMA5만 지원합니다. Typed Array, 백틱 문자열 등 ES6 기능은 사용할 수 없습니다.
- 정규 표현식은 ECMA5와 완전히 호환되지 않습니다.
    호환되지 않는 문법 예:
    
    - `(?=)`  전방 탐색(positive) → 구문 오류 발생
    - `(?!)`  전방 부정 탐색 → 구문 오류 발생
    - `\1`,`\2`,`\3`, ...  역참조 → 구문 오류 발생

## JSH 모듈

{{< neo_since ver="8.0.52" />}}

`require()`를 통해 `SCRIPT()` 안에서 JSH 모듈을 가져올 수 있습니다.  
`@jsh/process`는 JSH 애플리케이션 내부에서만 사용 가능하며, 그 외 `@jsh` 모듈은 모두 사용할 수 있습니다.

```js
SCRIPT({
    const { arrange } = require("@jsh/generator")
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
- `$.yieldArray()` : 배열 하나만 인자로 받아 레코드를 방출합니다.
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
