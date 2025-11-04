---
title: 기초
type: docs
weight: 02
---

## 기본 타입

TQL은 문자열(`string`), 숫자(`number`), 불리언(`boolean`)과 시간(`time`) 타입을 지원합니다.

### 문자열(string)

문자열은 작은따옴표('), 큰따옴표("), 백틱(`)으로 감쌀 수 있습니다. 백틱은 여러 줄 문자열이나 따옴표를 포함한 긴 SQL 문을 작성할 때 편리합니다.

```js
SQL( 'select * from example where name=\'temperature\' limit 10' )
CSV()
```

```js
SQL( "select * from example where name='temperature' limit 10" )
CSV()
```

```js
SQL( `select *
      from example
      where name='temperature'
      limit 10` )
CSV()
```

중괄호 두 개(`{{ }}`)를 사용하면 JSON 문자열을 손쉽게 표현할 수 있어 따옴표 이스케이프가 필요하지 않습니다.

```js
STRING({{
    "name": "Connan",
    "hired": true,
    "company": {
        "name":"acme",
        "employee": 123
    }
}})
CSV()
```

### 숫자(number)

모든 숫자 리터럴은 64비트 부동소수점으로 처리됩니다.

```js
SQL_SELECT('time', 'value', from('example', 'temperature'), limit(10))
CSV()
```

```js
FAKE( oscillator( freq(12.34, 20), range("now", "1s", "100ms")) )
CSV()
```

### 불리언(boolean)

불리언 상수는 `true`, `false` 입니다.

```js
FAKE( linspace(0, 1, 1))
CSV( heading(false) )
```

### 시간(time)

`time()`, `parseTime()` 함수로 생성하거나 SQL 결과의 `DATETIME` 컬럼으로부터 얻을 수 있습니다.

### 타임존(timeZone)

`tz()` 함수를 사용해 시간대를 지정할 수 있습니다. 예) `tz('UTC')`, `tz('Local')`, `tz('Asia/Seoul')`

### 리스트(list)

`list()` 함수로 값의 배열을 생성합니다. 예) `list(1, 2, 3)`

### 딕셔너리(dictionary)

`dict()` 함수는 문자열 키와 값을 쌍으로 갖는 사전을 만듭니다. 예) `dict("name", "pi", "value", 3.14)`

## 문장 작성 규칙

문자열·숫자·불리언 리터럴을 제외한 모든 문장은 함수 호출 형태여야 합니다.

```js
// 주석은 '//' 로 작성합니다.
SQL_SELECT(
    'time', 'value',
    from('example', 'temperature'),
    limit(10)
)
CSV()
```

## SRC와 SINK

`.tql` 스크립트는 데이터를 생성하는 **소스(SRC)** 함수로 시작해야 합니다. `SQL()`, `SQL_SELECT()`, `SCRIPT()` 등이 이에 해당합니다. 마지막 문장은 결과를 출력하거나 저장하는 **싱크(SINK)** 함수여야 하며 `CSV()`, `JSON()`, `APPEND()`, `CHART()` 등이 대표적입니다.

## MAP 함수

소스와 싱크 사이에는 0개 이상의 MAP 함수를 넣을 수 있습니다. MAP 함수 이름은 대문자로 시작하며 내부 옵션은 소문자 카멜 표기 함수로 지정합니다.

```js
SQL_SELECT(
    'time', 'value',
    from('example', 'temperature'),
    limit(10)
)
DROP(5)
TAKE(5)
CSV()
```

## 파라미터(param)

HTTP로 `.tql` 스크립트를 호출할 때 쿼리 파라미터를 전달할 수 있으며 `param()` 함수로 값을 읽습니다.

```js
SQL_SELECT(
    'time', 'value',
    from('example', param('name')),
    limit( param('count') )
)
CSV()
```

예를 들어 파일을 `hello2.tql`로 저장하고 `http://127.0.0.1:5654/db/tql/hello2.tql?name=temperature&count=10` 으로 호출하면 `param('name')`은 `"temperature"`, `param('count')`는 `10`을 반환합니다.

{{% steps %}}

### `param()` 사용

`example.tql` 파일에 다음 코드를 저장합니다.

```js
SQL( `select * from example where name = ?`, param('name'))
CSV()
```

### 클라이언트 GET 요청

`curl` 명령으로 TQL을 호출합니다.

```
curl "http://127.0.0.1:5654/db/tql/param.tql?name=TAG0"
```

{{% /steps %}}

## 연산자

### 산술 연산자

`+`, `-`, `*`, `/` 네 가지 산술 연산을 지원합니다.
