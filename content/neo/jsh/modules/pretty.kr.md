---
title: "pretty"
type: docs
weight: 100
---

{{< neo_since ver="8.0.75" />}}

`pretty` 모듈은 JSH 애플리케이션에서 값 포맷팅과 터미널 친화적인 출력 생성을 담당합니다.
읽기 쉬운 표, 사람이 보기 좋은 바이트 및 시간 문자열, 장시간 작업의 진행률 표시가 필요할 때 유용합니다.

작업에 따라 다음 API를 선택하면 됩니다.

- 상자형 표, CSV, TSV, JSON, NDJSON, HTML, Markdown 형식이 필요하면 `Table()`을 사용합니다.
- 사람이 읽기 쉬운 숫자와 시간 문자열이 필요하면 `Bytes()`, `Ints()`, `Durations()`를 사용합니다.
- 장시간 실행 작업의 진행 상태를 터미널에 표시하려면 `Progress()`를 사용합니다.

## 설치

```js
const pretty = require('pretty');
```

## Table()

테이블 writer를 생성합니다.

<h6>사용 형식</h6>

```js
Table(config)
```

<h6>주요 옵션</h6>

| 옵션 | 타입 | 설명 | 기본값 |
| --- | --- | --- | --- |
| `format` | `String` | `box`, `csv`, `tsv`, `json`, `ndjson`, `html`, `md` 같은 출력 형식 | `box` |
| `boxStyle` | `String` | `light`, `double`, `bold`, `rounded`, `simple`, `compact` 같은 박스 스타일 | `light` |
| `rownum` | `Boolean` | 앞에 `ROWNUM` 열을 추가할지 여부 | `true` |
| `timeformat` | `String` | 날짜/시간 포맷 | `default` |
| `tz` | `String` | `local`, `UTC`, 또는 IANA 타임존 이름 | `local` |
| `precision` | `Number` | `0` 이상이면 부동소수점 값을 반올림 | `-1` |
| `header` | `Boolean` | 헤더 행 출력 여부 | `true` |
| `footer` | `Boolean` | 푸터 또는 캡션 출력 여부 | `true` |
| `pause` | `Boolean` | 터미널 페이지 단위 일시정지 여부 | `true` |
| `nullValue` | `String` | null 값을 표시할 문자열 | `NULL` |
| `stringEscape` | `Boolean` | 출력 불가능한 문자를 `\uXXXX`로 이스케이프 | `false` |

<h6>주요 메서드</h6>

- `appendHeader(values)` 헤더 행 추가
- `appendRow(row)` 단일 행 추가
- `appendRows(rows)` 여러 행 추가
- `append(values)` 행 또는 행 목록 추가
- `row(...values)` 테이블 변환 규칙이 적용되는 행 생성
- `render()` 현재 결과를 문자열로 반환
- `close()` 남아 있는 행을 마저 렌더링하고 마지막 결과 반환
- `resetRows()` 버퍼된 행 초기화
- `pauseAndWait()` 페이지 모드에서 키 입력 대기

<h6>사용 예시: 기본 box 테이블</h6>

```js {linenos=table,linenostart=1}
const pretty = require('pretty');
const tw = pretty.Table({ boxStyle: 'light' });
tw.appendHeader(['Name', 'Age']);
tw.appendRow(tw.row('Alice', 30));
tw.appendRow(tw.row('Bob', 25));
console.println(tw.render());
```

출력:

```text
┌────────┬───────┬─────┐
│ ROWNUM │ NAME  │ AGE │
├────────┼───────┼─────┤
│      1 │ Alice │  30 │
│      2 │ Bob   │  25 │
└────────┴───────┴─────┘
```

<h6>사용 예시: 부동소수점 반올림</h6>

```js {linenos=table,linenostart=1}
const pretty = require('pretty');
const tw = pretty.Table({ boxStyle: 'light', precision: 2 });
tw.appendHeader(['Item', 'Price']);
tw.appendRow(tw.row('Apple', 1.234));
tw.appendRow(tw.row('Orange', 2.567));
console.println(tw.render());
```

출력:

```text
┌────────┬────────┬───────┐
│ ROWNUM │ ITEM   │ PRICE │
├────────┼────────┼───────┤
│      1 │ Apple  │  1.23 │
│      2 │ Orange │  2.57 │
└────────┴────────┴───────┘
```

<h6>사용 예시: 시간 포맷</h6>

```js {linenos=table,linenostart=1}
const pretty = require('pretty');
const tw = pretty.Table({ boxStyle: 'light', timeformat: 'DATETIME', tz: 'UTC' });
tw.appendHeader(['Event', 'Time']);
tw.append(['Start', new Date('2024-03-15T14:30:45.000Z')]);
tw.append(['End', new Date('2024-03-15T18:20:30.000Z')]);
console.println(tw.render());
```

출력:

```text
┌────────┬───────┬─────────────────────┐
│ ROWNUM │ EVENT │ TIME                │
├────────┼───────┼─────────────────────┤
│      1 │ Start │ 2024-03-15 14:30:45 │
│      2 │ End   │ 2024-03-15 18:20:30 │
└────────┴───────┴─────────────────────┘
```

기본 제공되는 `timeformat` 키워드는 `DATETIME`, `DATE`, `TIME`, `RFC3339`, `RFC1123`,
`ANSIC`, `KITCHEN`, `STAMP`, `STAMPMILLI`, `STAMPMICRO`, `STAMPNANO`입니다.
필요하면 Go 스타일 시간 레이아웃 문자열을 직접 전달할 수도 있습니다.

<h6>사용 예시: box 스타일</h6>

```js {linenos=table,linenostart=1}
const pretty = require('pretty');
for (const style of ['light', 'double', 'bold', 'rounded', 'compact']) {
	const tw = pretty.Table({ boxStyle: style, rownum: false });
	tw.appendHeader(['Col']);
	tw.appendRow(tw.row('Val'));
	console.println(style + ':');
	console.println(tw.render());
}
```

일부 출력 예시는 다음과 같습니다.

```text
light:
┌─────┐
│ COL │
├─────┤
│ Val │
└─────┘

double:
╔═════╗
║ COL ║
╠═════╣
║ Val ║
╚═════╝

compact:
 COL 
─────
 Val 
```

<h6>사용 예시: JSON 출력</h6>

```js {linenos=table,linenostart=1}
const pretty = require('pretty');
const tw = pretty.Table({ format: 'json', rownum: false });
tw.appendHeader(['ID', 'Status', 'Value']);
tw.append([1, 'active', 42.5]);
tw.append([2, 'pending', 31.2]);
console.println(tw.render());
```

출력:

```json
{"columns":["ID","Status","Value"],"rows":[[1,"active",42.5],[2,"pending",31.2]]}
```

<h6>사용 예시: CSV 출력</h6>

```js {linenos=table,linenostart=1}
const pretty = require('pretty');
const tw = pretty.Table({ format: 'csv', rownum: false });
tw.appendHeader(['Name', 'Score']);
tw.append(['Alice', 98]);
tw.append(['Bob', 87]);
console.println(tw.render());
```

출력:

```text
Name,Score
Alice,98
Bob,87
```

<h6>사용 예시: TSV 출력</h6>

```js {linenos=table,linenostart=1}
const pretty = require('pretty');
const tw = pretty.Table({ format: 'tsv', rownum: false });
tw.appendHeader(['Name', 'Score']);
tw.append(['Alice', 98]);
tw.append(['Bob', 87]);
console.println(tw.render());
```

출력:

```text
Name	Score
Alice	98
Bob	87
```

<h6>사용 예시: NDJSON 출력</h6>

```js {linenos=table,linenostart=1}
const pretty = require('pretty');
const tw = pretty.Table({ format: 'ndjson', rownum: false });
tw.appendHeader(['Name', 'Score']);
tw.append(['Alice', 98]);
tw.append(['Bob', 87]);
console.println(tw.render());
```

출력:

```json
{"Name":"Alice","Score":98}
{"Name":"Bob","Score":87}
```

<h6>사용 예시: Markdown 출력</h6>

```js {linenos=table,linenostart=1}
const pretty = require('pretty');
const tw = pretty.Table({ format: 'md', rownum: false });
tw.appendHeader(['Name', 'Score']);
tw.append(['Alice', 98]);
tw.append(['Bob', 87]);
console.println(tw.render());
```

출력:

```md
| Name  | Score |
| ----- | ----: |
| Alice |    98 |
| Bob   |    87 |
```

<h6>사용 예시: 비가시 문자 이스케이프</h6>

```js {linenos=table,linenostart=1}
const pretty = require('pretty');
const tw = pretty.Table({ stringEscape: true, rownum: false });
tw.appendHeader(['Value']);
tw.appendRow(tw.row('hello\u0007world'));
console.println(tw.render());
```

`stringEscape`가 `true`이면 출력 가능한 문자가 아닌 값은 이스케이프된 유니코드 문자열로 표시됩니다.

## MakeRow()

지정한 크기의 빈 행 배열을 생성합니다.

<h6>사용 형식</h6>

```js
MakeRow(size)
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const pretty = require('pretty');
const row = pretty.MakeRow(3);
console.println(row.length);
console.println(Array.isArray(row));
```

## Progress()

터미널용 진행률 writer를 생성합니다.

<h6>사용 형식</h6>

```js
Progress(options)
```

<h6>옵션</h6>

- `showPercentage` `Boolean` 백분율 표시 여부, 기본값 `true`
- `showETA` `Boolean` 예상 남은 시간 표시 여부, 기본값 `true`
- `showSpeed` `Boolean` 처리 속도 표시 여부, 기본값 `true`
- `updateFrequency` `Number` 갱신 주기(밀리초), 기본값 `250`
- `trackerLength` `Number` 진행률 바 길이, 기본값 `20`

반환된 writer는 `tracker(options)`를 제공합니다.
tracker는 `message`, `total`을 받으며, `increment(n)`, `value()`, `markAsDone()`, `isDone()`을 지원합니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const pretty = require('pretty');
const pw = pretty.Progress({ showPercentage: true, showETA: true });
const tracker = pw.tracker({ message: 'Processing', total: 100 });

let interval = setInterval(function() {
	tracker.increment(10);
	if (tracker.value() >= 100) {
		tracker.markAsDone();
		clearInterval(interval);
	}
}, 200);
```

이 기능은 대화형 터미널 세션을 위한 것입니다. 테스트나 비대화형 실행에서는 실제 바 출력보다
`isDone()` 상태에 도달하는지가 핵심 동작입니다.

## Bytes()

바이트 수를 사람이 읽기 쉬운 문자열로 포맷합니다.

<h6>사용 형식</h6>

```js
Bytes(value)
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const pretty = require('pretty');
console.println(pretty.Bytes(512));
console.println(pretty.Bytes(1536));
console.println(pretty.Bytes(1048576));
console.println(pretty.Bytes(1073741824));
```

출력:

```text
512B
1.5KB
1.0MB
1.0GB
```

## Ints()

정수를 자리 구분 기호가 포함된 문자열로 포맷합니다.

<h6>사용 형식</h6>

```js
Ints(value)
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const pretty = require('pretty');
console.println(pretty.Ints(1234567890));
console.println(pretty.Ints(0));
console.println(pretty.Ints(-999));
```

출력:

```text
1,234,567,890
0
-999
```

## Durations()

나노초 단위 시간을 짧고 읽기 쉬운 문자열로 포맷합니다.

<h6>사용 형식</h6>

```js
Durations(nanoseconds)
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const pretty = require('pretty');
console.println(pretty.Durations(1234));
console.println(pretty.Durations(2340000));
console.println(pretty.Durations(3010000000));
console.println(pretty.Durations(3661000000000));
console.println(pretty.Durations(86400000000000));
```

출력:

```text
1.23μs
2.34ms
3.01s
1h 1m
1d 0h
```

60초 미만 값은 `μs`, `ms`, `s` 같은 소수 단위로 표시합니다.
그보다 긴 시간은 `2m 5s`, `1h 1m`, `2d 0h`처럼 상위 두 단위만 표시합니다.

## Align

고급 열 설정에서 사용할 정렬 상수를 제공합니다.

사용 가능한 상수는 `default`, `left`, `center`, `justify`, `right`, `auto`입니다.

## Terminal helpers

모듈은 다음 헬퍼도 함께 제공합니다.

- `isTerminal()` stdin이 터미널에 연결되어 있는지 반환
- `getTerminalSize()` 터미널 너비와 높이 반환
- `pauseTerminal()` 키 입력을 기다리고 `q` 또는 `Q`면 `false` 반환
- `parseTime(value, format, tz)` 문자열을 시간 값으로 파싱

이 헬퍼들은 `Table()`이나 `Progress()` 기반의 대화형 터미널 도구를 만들 때 주로 유용합니다.
