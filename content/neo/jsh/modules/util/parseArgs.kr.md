---
title: "parseArgs"
type: docs
weight: 100
---

{{< neo_since ver="8.0.75" />}}

`util/parseArgs` 모듈은 명령행 스타일의 인자 배열을 파싱합니다.
`require('util/parseArgs')`와 `require('util').parseArgs` 두 형태로 모두 사용할 수 있습니다.

## parseArgs()

하나 이상의 설정 객체를 사용해 인자 배열을 해석합니다.

<h6>사용 형식</h6>

```js
parseArgs(args, ...configs)
```

<h6>매개변수</h6>

- `args` `String[]`: 파싱할 인자 배열
- `...configs` `Object`: 하나 이상의 파서 설정

여러 config를 넘기고 그중 일부에 `command`가 있으면, parser는 `args[0]`과 command 이름을 비교해 일치하는 설정을 선택합니다.

<h6>설정 필드</h6>

| 필드 | 타입 | 기본값 | 설명 |
|:-----|:-----|:-------|:-----|
| `command` | String |        | `args[0]`와 매칭할 sub-command 이름 |
| `options` | Object | `{}` | 옵션 정의 |
| `strict` | Boolean | `true` | 알 수 없는 옵션이나 예상하지 않은 positional에서 예외 발생 |
| `allowNegative` | Boolean | `false` | boolean long option에 `--no-` 형식 허용 |
| `tokens` | Boolean | `false` | 결과에 token 정보를 포함 |
| `allowPositionals` | Boolean | `positionals`에 따라 결정 | positional 인자 허용 여부 |
| `positionals` | Array |        | positional 정의 목록 |
| `usage` | String |        | `formatHelp()`에서 사용 |
| `description` | String |        | `formatHelp()`에서 사용 |
| `longDescription` | String |        | multi-command help에서 사용 |

## 옵션 정의

`config.options`의 각 항목 키는 JavaScript 속성 이름입니다.
parser는 camelCase 이름을 자동으로 kebab-case CLI 플래그로 변환합니다.

예를 들어 `maxRetryCount`는 `--max-retry-count`로 매핑됩니다.

| 필드 | 타입 | 설명 |
|:-----|:-----|:-----|
| `type` | String | `boolean`, `string`, `integer`, `float` 중 하나 |
| `short` | String | `-v` 같은 한 글자 short flag |
| `multiple` | Boolean | 반복 지정된 값을 배열로 수집 |
| `default` | any | 파싱 전에 미리 적용할 기본값 |
| `description` | String | `formatHelp()`에서 사용할 설명 |

지원하는 입력 형식:

- `--output file.txt` 같은 long option
- `--output=file.txt` 같은 inline long value
- `-o file.txt` 같은 short option
- `-o=file.txt` 같은 inline short value
- `-abc` 같은 short boolean group
- 옵션 종료자 `--`

## positional 정의

`positionals`는 간단한 문자열 배열 또는 상세 객체 배열을 사용할 수 있습니다.

간단한 형식:

```js
positionals: ['inputFile', 'outputFile']
```

상세 형식:

```js
positionals: [
    { name: 'input-file' },
    { name: 'output-file', optional: true, default: 'stdout' },
    { name: 'files', variadic: true }
]
```

규칙:

- variadic positional은 반드시 마지막에 와야 합니다.
- 필수 positional이 없으면 `TypeError`가 발생합니다.
- `result.namedPositionals`의 키는 kebab-case에서 camelCase로 변환됩니다.

## 반환값

`parseArgs()`는 다음 필드를 가진 객체를 반환합니다.

| 필드 | 타입 | 설명 |
|:-----|:-----|:-----|
| `values` | Object | 파싱된 옵션 값 |
| `positionals` | String[] | 순서대로 저장된 positional 값 |
| `namedPositionals` | Object | `positionals` 설정이 있을 때 포함 |
| `tokens` | Object[] | `tokens: true`일 때 포함 |
| `command` | String | sub-command 설정이 매칭됐을 때 포함 |

## 사용 예시

```js {linenos=table,linenostart=1}
const { parseArgs } = require('util');

const result = parseArgs(['-v', '--output', 'file.txt', 'input.sql'], {
    options: {
        verbose: { type: 'boolean', short: 'v' },
        output: { type: 'string' }
    },
    allowPositionals: true,
    positionals: ['input-file']
});

console.println(JSON.stringify(result.values));
console.println(JSON.stringify(result.namedPositionals));
```

## 숫자 파싱

정수는 `integer`, 실수는 `float`를 사용합니다.

- `integer`는 소수점이 포함된 값을 허용하지 않습니다.
- `integer`, `float` 모두 JavaScript number를 반환합니다.

```js {linenos=table,linenostart=1}
const { parseArgs } = require('util');

const result = parseArgs(['--port', '8080', '--ratio', '0.75'], {
    options: {
        port: { type: 'integer' },
        ratio: { type: 'float' }
    }
});
```

## negative boolean

`allowNegative: true`를 지정하면 boolean long option에 `--no-...` 형식을 사용할 수 있습니다.

```js {linenos=table,linenostart=1}
const { parseArgs } = require('util');

const result = parseArgs(['--no-color', '--verbose'], {
    options: {
        color: { type: 'boolean' },
        verbose: { type: 'boolean' }
    },
    allowNegative: true
});
```

## sub-command 파싱

여러 config를 전달하면 첫 번째 인자로 command별 설정을 선택할 수 있습니다.

```js {linenos=table,linenostart=1}
const parseArgs = require('util/parseArgs');

const commitConfig = {
    command: 'commit',
    options: {
        message: { type: 'string', short: 'm' },
        all: { type: 'boolean', short: 'a' }
    }
};

const pushConfig = {
    command: 'push',
    options: {
        force: { type: 'boolean', short: 'f' }
    },
    allowPositionals: true,
    positionals: ['remote', { name: 'branch', optional: true }]
};

const result = parseArgs(['push', '-f', 'origin', 'main'], commitConfig, pushConfig);
console.println(result.command);
console.println(JSON.stringify(result.namedPositionals));
```

## parseArgs.formatHelp()

`parseArgs()`와 같은 설정 구조를 받아 사람이 읽기 좋은 help text를 생성합니다.

<h6>사용 형식</h6>

```js
parseArgs.formatHelp(...configs)
```

다음 두 경우를 모두 지원합니다.

- 단일 명령 help 출력
- command 요약과 command별 상세 섹션을 포함하는 multi-command help 출력

```js {linenos=table,linenostart=1}
const parseArgs = require('util/parseArgs');

const help = parseArgs.formatHelp({
    usage: 'Usage: myapp [options] <file>',
    options: {
        userName: { type: 'string', short: 'u', description: 'User name', default: 'guest' },
        enableDebug: { type: 'boolean', short: 'd', description: 'Enable debug mode', default: false }
    },
    positionals: [
        { name: 'file', description: 'Input file to process' }
    ]
});

console.println(help);
```

## parseArgs.toKebabCase()

JavaScript camelCase 옵션 이름을 CLI용 kebab-case 문자열로 변환합니다.

<h6>사용 형식</h6>

```js
parseArgs.toKebabCase(name)
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const parseArgs = require('util/parseArgs');

console.println(parseArgs.toKebabCase('maxRetryCount'));
```

## 동작 참고

- 첫 번째 인자는 반드시 배열이어야 하며, 아니면 `TypeError`가 발생합니다.
- `strict` 모드에서는 알 수 없는 옵션과 예상하지 않은 positional에서 `TypeError`가 발생합니다.
- `multiple: true`는 반복된 값을 배열로 수집합니다.
- 기본값은 실제 옵션 값을 파싱하기 전에 먼저 적용됩니다.
- `require('util').parseArgs`와 `require('util/parseArgs')`를 모두 사용할 수 있습니다.