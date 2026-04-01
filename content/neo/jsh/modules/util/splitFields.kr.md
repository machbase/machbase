---
title: "splitFields"
type: docs
weight: 100
---

{{< neo_since ver="8.0.75" />}}

`util/splitFields` 모듈은 공백 문자를 기준으로 문자열을 필드로 나누되, 따옴표로 감싼 부분은 하나의 필드로 유지합니다.
`require('util/splitFields')`와 `require('util').splitFields` 두 형태로 모두 사용할 수 있습니다.

## splitFields()

공백, 탭, 개행, 캐리지 리턴을 구분자로 사용해 문자열을 분리합니다.
작은따옴표와 큰따옴표로 감싼 텍스트는 하나의 필드로 유지됩니다.

<h6>사용 형식</h6>

```js
splitFields(str[, options])
```

<h6>매개변수</h6>

- `str` `String`: 분리할 입력 문자열
- `options` `Object`: 선택적 설정 객체. 현재 구현은 이 매개변수를 받지만 실제로 사용하지는 않습니다.

<h6>반환값</h6>

`String[]`

## 사용 예시

```js {linenos=table,linenostart=1}
const { splitFields } = require('util');

console.println(JSON.stringify(splitFields('cmd "arg 1" "arg 2"')));
console.println(JSON.stringify(splitFields("hello 'world foo' bar")));
console.println(JSON.stringify(splitFields('foo\tbar\nbaz')));
```

## 동작 방식

- 연속된 공백은 하나의 구분자로 처리합니다.
- 빈 필드는 결과에 포함되지 않습니다.
- 반환값에는 따옴표 문자가 포함되지 않습니다.
- 닫히지 않은 따옴표는 문자열 끝까지 계속 같은 필드로 처리됩니다.
- 따옴표 내부의 탭과 개행은 그대로 유지됩니다.

## 예제

기본 공백 분리:

```js
splitFields('  foo   bar baz  ');
// ['foo', 'bar', 'baz']
```

큰따옴표 처리:

```js
splitFields('hello "world foo" bar');
// ['hello', 'world foo', 'bar']
```

작은따옴표 처리:

```js
splitFields("hello 'world foo' bar");
// ['hello', 'world foo', 'bar']
```

혼합 따옴표 처리:

```js
splitFields("a \"b c\" d 'e f' g");
// ['a', 'b c', 'd', 'e f', 'g']
```

## 참고 사항

- 입력값은 반드시 문자열이어야 하며, 아니면 `TypeError`가 발생합니다.
- 따옴표 내부의 escape sequence를 특별히 해석하지는 않습니다.
- 완전한 명령행 파싱까지는 필요 없고 shell 비슷한 token 분리만 필요할 때 유용합니다.