---
title: "path"
type: docs
weight: 100
---

{{< neo_since ver="8.0.75" />}}

`path` 모듈은 Node.js와 비슷한 경로 조작 helper를 제공합니다.
JSH에서는 기본 export가 POSIX 구현이며, `path.posix`, `path.win32` namespace도 함께 제공합니다.

일반적으로 아래처럼 사용합니다.

```js
const path = require('path');
```

## 기본 export

`require('path')`는 POSIX path 구현을 반환합니다.

즉 기본 동작은 다음과 같습니다.

- 경로 구분자는 `/`
- 목록 구분자는 `:`
- `join()`, `resolve()` 같은 함수는 POSIX 스타일로 동작

추가로 다음 namespace도 사용할 수 있습니다.

- `path.posix`
- `path.win32`

## 공통 속성

| 속성 | POSIX | win32 |
|:-----|:------|:------|
| `sep` | `/` | `\\` |
| `delimiter` | `:` | `;` |

## resolve()

여러 경로 조각을 절대 경로로 해석합니다.

<h6>사용 형식</h6>

```js
path.resolve(...segments)
```

기본 구현은 기준 경로가 필요할 때 현재 작업 디렉터리를 사용합니다.

## normalize()

경로 구분자를 정리하고 `.` 및 `..` 세그먼트를 해석합니다.

<h6>사용 형식</h6>

```js
path.normalize(value)
```

## isAbsolute()

경로가 절대 경로인지 반환합니다.

<h6>사용 형식</h6>

```js
path.isAbsolute(value)
```

## join()

경로 조각을 현재 path 스타일에 맞게 결합하고 결과를 normalize합니다.

<h6>사용 형식</h6>

```js
path.join(...segments)
```

## relative()

한 경로에서 다른 경로로 가는 상대 경로를 반환합니다.

<h6>사용 형식</h6>

```js
path.relative(from, to)
```

## dirname()

경로의 디렉터리 부분을 반환합니다.

<h6>사용 형식</h6>

```js
path.dirname(value)
```

## basename()

경로의 마지막 구성 요소를 반환합니다.
`ext`를 지정하면 일치하는 suffix를 제거합니다.

<h6>사용 형식</h6>

```js
path.basename(value)
path.basename(value, ext)
```

## extname()

앞의 점을 포함한 파일 확장자를 반환합니다.

<h6>사용 형식</h6>

```js
path.extname(value)
```

## parse()

경로를 구조화된 필드로 분해합니다.

<h6>사용 형식</h6>

```js
path.parse(value)
```

<h6>반환값</h6>

`parse()`는 다음 필드를 가진 객체를 반환합니다.

- `root`
- `dir`
- `base`
- `ext`
- `name`

## format()

parsed path object로부터 다시 경로 문자열을 구성합니다.

<h6>사용 형식</h6>

```js
path.format(pathObject)
```

`pathObject`에는 `dir`, `root`, `base`, `name`, `ext`를 넣을 수 있습니다.

## 사용 예시

```js {linenos=table,linenostart=1}
const path = require('path');

console.println(path.join('/work', 'demo', 'file.txt'));
console.println(path.dirname('/work/demo/file.txt'));
console.println(path.basename('/work/demo/file.txt', '.txt'));
console.println(path.extname('/work/demo/file.txt'));
```

## parse()/format() 예시

```js {linenos=table,linenostart=1}
const path = require('path');

const parsed = path.parse('/work/demo/file.txt');
console.println(JSON.stringify(parsed));

const rebuilt = path.format({
    dir: '/work/demo',
    name: 'file',
    ext: '.txt'
});
console.println(rebuilt);
```

## POSIX / win32 namespace

기본 동작과 무관하게 명시적으로 POSIX 또는 Windows 경로 규칙을 쓰고 싶다면 `path.posix`, `path.win32`를 사용합니다.

```js {linenos=table,linenostart=1}
const path = require('path');

console.println(path.posix.join('/a', 'b', 'c.txt'));
console.println(path.win32.join('C:\\temp', 'demo', 'file.txt'));
```

## 동작 참고

- JSH의 기본 export는 POSIX 기준입니다.
- 공개 함수는 필요한 위치에서 문자열 인자를 요구하며, 잘못된 입력에는 `TypeError`를 발생시킵니다.
- `parse()`와 `format()`은 Node.js와 비슷한 object shape를 사용합니다.
- JSH가 Windows가 아닌 시스템에서 실행되더라도 `path.win32`는 사용할 수 있습니다.