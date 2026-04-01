---
title: "readline"
type: docs
weight: 100
---

{{< neo_since ver="8.0.75" />}}

`readline` 모듈은 JSH 애플리케이션에서 대화형 한 줄 입력을 처리하기 위한 모듈입니다.
JSH 네이티브 readline 구현을 감싼 `ReadLine` 클래스 하나를 노출합니다.

일반적으로 아래처럼 사용합니다.

```js
const { ReadLine } = require('readline');
```

## ReadLine

대화형 line reader를 생성합니다.

<h6>사용 형식</h6>

```js
new ReadLine([options])
```

<h6>옵션</h6>

| 옵션 | 타입 | 기본값 | 설명 |
|:-----|:-----|:-------|:-----|
| history | String | `readline` | JSH 설정 디렉토리 아래에 저장할 history 파일 이름입니다. |
| prompt | Function | 내장 prompt | 각 줄마다 표시할 prompt 문자열을 반환하는 callback입니다. |
| submitOnEnterWhen | Function | 항상 submit | Enter 입력 시 현재 입력을 제출할지 결정하는 callback입니다. |
| autoInput | String[] |        | 주로 자동화 테스트에서 사용하는 입력 시퀀스입니다. |

`prompt`를 지정하지 않으면 첫 줄은 `> `, 다음 줄부터는 `. ` 형태의 continuation prompt를 사용합니다.
`history`를 지정하지 않으면 기본 history 파일 이름은 `readline`입니다.
`history` 옵션은 path가 아니라 파일 이름으로 취급되며, 실제 history 파일은 `$HOME/.config/.jsh/` 아래에 저장됩니다. `history`에는 base filename만 사용해야 하며, 디렉터리 구분자는 넣지 않는 것이 맞습니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const { ReadLine } = require('readline');

const reader = new ReadLine({
    prompt: (lineno) => lineno === 0 ? 'prompt> ' : '....... ',
});
```

## readLine()

하나의 논리적 입력 값을 읽습니다.

- 단일 줄 입력이면 문자열 하나를 반환합니다.
- multi-line 입력이면 각 줄을 `\n`으로 연결한 문자열을 반환합니다.
- 네이티브 reader가 오류로 종료되면 JSH에서는 `Error` 객체가 반환됩니다.

<h6>사용 형식</h6>

```js
reader.readLine([options])
```

`readLine()`은 constructor와 같은 형태의 옵션을 받습니다.
호출 시 전달한 옵션이 constructor 옵션보다 우선합니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const { ReadLine } = require('readline');

const reader = new ReadLine({
    prompt: () => 'input> ',
});
const line = reader.readLine();
if (line instanceof Error) {
    throw line;
}
console.println(line);
```

## addHistory()

한 줄을 readline history에 추가합니다.

<h6>사용 형식</h6>

```js
reader.addHistory(line)
```

같은 내용의 line이 이미 있으면 기존 항목을 제거한 뒤 끝에 다시 추가합니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const { ReadLine } = require('readline');

const reader = new ReadLine();
const line = reader.readLine();
if (line instanceof Error) {
    throw line;
}
reader.addHistory(line);
```

## close()

현재 readline 세션을 종료합니다.

<h6>사용 형식</h6>

```js
reader.close()
```

`readLine()`이 입력을 기다리는 중에 `close()`가 호출되면 대기 중인 호출은 `EOF`로 종료됩니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const { ReadLine } = require('readline');

const reader = new ReadLine();
const timer = setTimeout(() => {
    reader.close();
}, 200);
const line = reader.readLine();
clearTimeout(timer);
```

## prompt 옵션

`prompt`는 각 줄의 prompt 문자열을 생성합니다.

<h6>시그니처</h6>

```js
prompt(lineno) => string
```

- `lineno`는 0부터 시작합니다.
- 해당 줄에 표시할 prompt 문자열을 그대로 반환하면 됩니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const { ReadLine } = require('readline');

const reader = new ReadLine({
    prompt: (lineno) => lineno === 0 ? 'sql> ' : '...> ',
});
```

## submitOnEnterWhen 옵션

`submitOnEnterWhen`은 Enter 입력이 현재 값을 제출할지, 아니면 multi-line 편집을 계속할지 결정합니다.

<h6>시그니처</h6>

```js
submitOnEnterWhen(lines, idx) => boolean
```

- `lines`는 현재까지의 줄 배열입니다.
- `idx`는 현재 줄 index입니다.
- `true`를 반환하면 제출하고, `false`를 반환하면 편집을 계속합니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const { ReadLine } = require('readline');

const reader = new ReadLine({
    submitOnEnterWhen: (lines, idx) => {
        return lines[idx].endsWith(';');
    },
});
```

## autoInput 옵션

`autoInput`은 미리 준비한 입력을 reader에 주입합니다.
주 용도는 테스트와 비대화형 스크립트입니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const { ReadLine } = require('readline');

const reader = new ReadLine({
    autoInput: [
        'Hello World',
        ReadLine.CtrlJ,
    ],
});
```

## multi-line 입력 예시

`submitOnEnterWhen`은 현재 줄이 애플리케이션 규칙을 만족할 때까지 편집을 계속하도록 만드는 용도로 자주 사용합니다.

```js {linenos=table,linenostart=1}
const { ReadLine } = require('readline');

const reader = new ReadLine({
    autoInput: ['select *', ReadLine.Enter, 'from dual;', ReadLine.Enter],
    submitOnEnterWhen: (lines, idx) => {
        return lines[idx].endsWith(';');
    },
});
const text = reader.readLine();
console.println(text);
```

## 정적 키 상수

`ReadLine`은 simulated input이나 키 처리에 사용할 수 있는 다양한 키 상수를 제공합니다.
대표적인 항목은 다음과 같습니다.

- Control 키: `CtrlA` ... `CtrlZ`, `CtrlLeft`, `CtrlRight`, `CtrlUp`, `CtrlDown`
- Navigation 키: `Up`, `Down`, `Left`, `Right`, `Home`, `End`, `PageUp`, `PageDown`
- Editing 키: `Backspace`, `Delete`, `Enter`, `ShiftTab`, `Escape`
- Alt 키: `AltA` ... `AltZ`, `ALTBackspace`
- Function 키: `F1` ... `F24`

전체 이름 목록은 `ReadLine`의 static property를 참고하면 됩니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const { ReadLine } = require('readline');

console.printf('%X\n', ReadLine.CtrlJ);
```

## 동작 참고

- JavaScript 레벨에서는 callback 없이 동기적으로 읽습니다. `readLine()`은 완료된 값을 직접 반환합니다.
- 실제 line editing, cursor 이동, history, multi-line 입력은 네이티브 backend가 처리합니다.
- `readLine()`은 `Error` 객체를 반환할 수 있으므로, 실패를 직접 처리하려면 `line instanceof Error`를 확인하는 편이 안전합니다.
- `close()`는 timer나 다른 이벤트에서 대기 중인 입력을 중단할 때 주로 사용합니다.
