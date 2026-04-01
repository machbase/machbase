---
title: "parser"
type: docs
weight: 100
---

{{< neo_since ver="8.0.75" />}}

`parser` 모듈은 CSV와 NDJSON 데이터를 위한 스트리밍 디코더를 제공합니다.
JSH 스트림과 함께 사용하도록 설계되어 있으며, 파싱된 객체를 이벤트로 전달합니다.

일반적으로 다음과 같이 사용합니다.

```js
const parser = require('parser');
```

## 내보내는 구성원

- `csv(options)`
- `ndjson(options)`
- `CSVParser`
- `NDJSONParser`

## csv()

CSV 파서 스트림을 생성합니다.

<h6>구문</h6>

```js
parser.csv([options])
```

<h6>옵션</h6>

| Option | Type | Default | Description |
|:-------|:-----|:--------|:------------|
| `separator` | String | `,` | 필드 구분자 |
| `quote` | String | `"` | 인용부호 문자 |
| `escape` | String | `quote`와 동일 | 이스케이프 문자 |
| `headers` | `true` / `false` / `String[]` | `true` | 헤더 처리 방식 |
| `skipLines` | Number | `0` | 처음에 건너뛸 줄 수 |
| `skipComments` | Boolean \| String | `false` | 주석 줄을 건너뜀. 문자열이면 해당 접두 문자를 사용 |
| `strict` | Boolean | `false` | 열 개수가 다르면 실패 |
| `mapHeaders` | Function | | 헤더 이름 변환 함수 |
| `mapValues` | Function | | 행을 내보내기 전에 값 변환 |
| `trimLeadingSpace` | Boolean | `true` | 각 필드의 앞 공백 제거 |

<h6>반환값</h6>

`CSVParser` 인스턴스를 반환합니다.

## CSVParser

모듈이 내보내는 CSV 파서 클래스입니다.

<h6>생성</h6>

```js
new parser.CSVParser([options])
```

생성자는 `parser.csv()`와 같은 옵션을 받습니다.

<h6>이벤트</h6>

- `headers`: 헤더 행이 파싱되면 한 번 발생
- `data`: 파싱된 각 행 객체마다 발생
- `error`: strict 파싱 실패 시 발생
- `end`: 상위 스트림이 종료되면 발생

<h6>속성</h6>

- `bytesWritten`: 입력으로 받은 바이트 수
- `bytesRead`: 파서가 소비한 바이트 수

<h6>행 구조</h6>

- `headers`를 생략하거나 `true`로 두면 첫 유효 행을 헤더로 사용합니다.
- `headers`가 `false`이면 필드는 `"0"`, `"1"`, `"2"`처럼 노출됩니다.
- `headers`가 배열이면 그 이름들을 사용하고 첫 줄은 데이터로 처리합니다.
- non-strict 모드에서 추가 열은 `_3` 같은 `_N` 필드로 노출됩니다.

## ndjson()

NDJSON 파서 스트림을 생성합니다.

<h6>구문</h6>

```js
parser.ndjson([options])
```

<h6>옵션</h6>

| Option | Type | Default | Description |
|:-------|:-----|:--------|:------------|
| `strict` | Boolean | `true` | 잘못된 JSON 줄에서 실패할지, 건너뛸지 결정 |

<h6>반환값</h6>

`NDJSONParser` 인스턴스를 반환합니다.

## NDJSONParser

모듈이 내보내는 NDJSON 파서 클래스입니다.

<h6>생성</h6>

```js
new parser.NDJSONParser([options])
```

생성자는 `parser.ndjson()`와 같은 옵션을 받습니다.

<h6>이벤트</h6>

- `data`: 파싱된 JSON 객체마다 발생
- `warning`: `strict: false`에서 잘못된 줄을 건너뛸 때 발생
- `error`: strict 파싱 실패 시 발생
- `end`: 상위 스트림이 종료되면 발생

`warning` 이벤트 객체는 다음 필드를 가집니다.

| Property | Type | Description |
|:---------|:-----|:------------|
| `line` | Number | 건너뛴 레코드의 줄 번호 |
| `data` | String | 원본 줄 텍스트 |
| `error` | String | 파싱 오류 메시지 |

<h6>속성</h6>

- `bytesWritten`: 입력으로 받은 바이트 수
- `bytesRead`: 파서가 소비한 바이트 수

## CSV 예제

```js {linenos=table,linenostart=1}
const fs = require('fs');
const parser = require('parser');

fs.createReadStream('/work/sample.csv')
    .pipe(parser.csv({
        headers: true,
        mapValues: ({ header, value }) => header === 'age' ? parseInt(value, 10) : value,
    }))
    .on('headers', (headers) => {
        console.println(headers.join(','));
    })
    .on('data', (row) => {
        console.println(row.name, row.age);
    });
```

## NDJSON 예제

```js {linenos=table,linenostart=1}
const fs = require('fs');
const parser = require('parser');

fs.createReadStream('/work/sample.ndjson')
    .pipe(parser.ndjson({ strict: false }))
    .on('data', (obj) => {
        console.println(obj.id);
    })
    .on('warning', (warn) => {
        console.println('Skipped line:', warn.line);
    });
```

## 진행률 예제

두 파서 스트림은 `bytesWritten`, `bytesRead`를 제공하므로 스트리밍 중 진행률을 추적할 수 있습니다.

```js {linenos=table,linenostart=1}
const fs = require('fs');
const parser = require('parser');

const decoder = parser.csv();

fs.createReadStream('/work/sample.csv', { highWaterMark: 8 })
    .pipe(decoder)
    .on('data', () => {
        console.println(decoder.bytesWritten, decoder.bytesRead);
    });
```

## 동작 메모

- 두 파서 클래스는 JSH `stream.Transform` 구현을 상속합니다.
- 파싱된 행과 객체는 `data` 이벤트로 전달됩니다.
- 두 파서 모두 빈 줄은 무시합니다.
- `NDJSONParser`는 각 줄을 파싱 전에 `trim()` 처리합니다.
- `CSVParser`는 `\r\n` 입력을 처리하기 위해 줄 끝의 `\r`을 제거합니다.