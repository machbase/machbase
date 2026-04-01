---
title: "stream"
type: docs
weight: 100
draft: true
---

`stream` 모듈은 JSH 애플리케이션에서 사용할 수 있는 Node.js 스타일의 스트림 기본 타입을 제공합니다.
이 모듈은 Go의 `io.Reader`, `io.Writer`를 감싸는 래퍼와 함께, JavaScript로 구현된 `Transform`, 메모리 기반 `PassThrough` 스트림을 제공합니다.

일반적으로 아래처럼 사용합니다.

```js
const { Readable, Writable, Duplex, PassThrough, Transform } = require('stream');
```

## Exported classes

- `Readable`
- `Writable`
- `Duplex`
- `PassThrough`
- `Transform`

## Readable

네이티브 reader를 감싸 읽기 가능한 스트림 인터페이스를 제공합니다.

<h6>사용 형식</h6>

```js
new Readable(reader)
```

- `reader`는 Go의 `io.Reader`를 backend로 가지는 네이티브 객체여야 합니다.

<h6>메서드</h6>

- `read([size])`: 다음 chunk를 읽어 `Buffer` 또는 `null`을 반환합니다.
- `readString([size[, encoding]])`: 다음 chunk를 읽어 문자열로 반환합니다.
- `pause()`: 스트림을 paused 상태로 표시하고 네이티브 pause 신호를 보냅니다.
- `resume()`: 스트림을 flowing 상태로 표시하고 네이티브 resume 신호를 보냅니다.
- `isPaused()`: 현재 paused 상태를 반환합니다.
- `pipe(destination[, options])`: `data` 이벤트를 writable destination으로 전달합니다. 기본적으로 source가 끝나면 destination도 `end()` 됩니다.
- `unpipe([destination])`: piping을 중단합니다. 현재 구현은 source의 `data` listener를 제거하는 방식으로 동작합니다.
- `destroy([error])`: 스트림을 닫고, `error`가 있으면 먼저 emit합니다.
- `close()`: `destroy()`의 별칭입니다.

<h6>속성</h6>

- `readable`
- `readableEnded`
- `readableFlowing`
- `readableHighWaterMark`

<h6>이벤트</h6>

- `data`
- `end`
- `error`
- `close`
- `pause`
- `resume`

## Writable

네이티브 writer를 감싸 쓰기 가능한 스트림 인터페이스를 제공합니다.

<h6>사용 형식</h6>

```js
new Writable(writer)
```

- `writer`는 Go의 `io.Writer`를 backend로 가지는 네이티브 객체여야 합니다.

<h6>메서드</h6>

- `write(chunk[, encoding][, callback])`: chunk를 씁니다. 지원 타입은 `string`, `Buffer`, `Uint8Array`입니다.
- `end([chunk][, encoding][, callback])`: 필요하면 마지막 chunk를 기록한 뒤 writable side를 종료합니다.
- `destroy([error])`: 스트림을 닫고, `error`가 있으면 먼저 emit합니다.
- `close()`: `destroy()`의 별칭입니다.

`write()`는 성공하면 `true`, 더 이상 쓸 수 없거나 오류가 발생하면 `false`를 반환합니다.

<h6>속성</h6>

- `writable`
- `writableEnded`
- `writableFinished`
- `writableHighWaterMark`

<h6>이벤트</h6>

- `finish`
- `error`
- `close`

## Duplex

읽기와 쓰기 기능을 하나의 스트림으로 결합한 타입입니다.

<h6>사용 형식</h6>

```js
new Duplex(reader, writer)
```

- `reader`는 Go의 `io.Reader` backend를 가져야 합니다.
- `writer`는 Go의 `io.Writer` backend를 가져야 합니다.

`Duplex`는 `Readable`의 읽기 메서드와 `Writable`의 쓰기 메서드를 함께 제공하며, `pipe()`, `pause()`, `resume()`, `isPaused()`, `destroy()`, `close()`도 지원합니다.

## PassThrough

기록한 데이터를 그대로 통과시키는 메모리 기반 duplex 스트림을 생성합니다.

<h6>사용 형식</h6>

```js
new PassThrough()
```

`PassThrough`는 테스트, 임시 버퍼링, 외부 네이티브 reader/writer 없이 stream 스타일 코드를 연결할 때 유용합니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const { PassThrough } = require('stream');

const stream = new PassThrough();
stream.on('data', (chunk) => {
    console.println(chunk.toString());
});

stream.write('Hello, ');
stream.end('stream');

const data = stream.read();
if (data !== null) {
    console.println(data.toString());
}
```

## Transform

JavaScript로 커스텀 변환기를 만들기 위한 base class입니다.

<h6>사용 형식</h6>

```js
new Transform([options])
```

현재 constructor는 선택적 `options` 객체를 받지만, 내장 구현에서 실제로 소비하는 옵션은 아직 없습니다.

<h6>서브클래스 hook</h6>

- `_transform(chunk, encoding, callback)`: 입력 chunk를 처리하도록 override합니다.
- `_flush(callback)`: 종료 직전에 남은 출력이 있으면 내보내도록 override합니다.

현재 런타임에서는 `_transform()` 안에서 직접 출력을 내보내는 방식이 기준입니다. 바이트 chunk는 `this.push(...)`로 전달하고, object 스타일 출력은 `data`를 직접 emit하는 방식이 더 안전합니다. callback의 두 번째 반환값은 내장 구현에서 사용하지 않습니다.

<h6>메서드</h6>

- `write(chunk[, encoding][, callback])`
- `end([chunk][, encoding][, callback])`
- `push(chunk)`: 읽기 side로 출력을 밀어 넣습니다. `null`을 전달하면 readable side가 종료됩니다.
- `pipe(destination[, options])`
- `destroy([error])`
- `pause()`
- `resume()`

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const { Transform } = require('stream');

class UpperCase extends Transform {
    _transform(chunk, encoding, callback) {
        this.push(chunk.toString('utf8').toUpperCase());
        callback();
    }
}

const stream = new UpperCase();
stream.on('data', (chunk) => console.println(chunk.toString()));
stream.write('hello');
stream.end();
```

## Common behavior

- 모든 export 클래스는 `EventEmitter`를 상속합니다.
- `Readable`, `Writable`, `Duplex`, `PassThrough`의 high-water mark는 `16384`로 고정되어 있습니다.
- `read()`와 `readString()`은 EOF에서 각각 `null`, 빈 문자열을 반환하고 `readableEnded`를 갱신합니다.
- writable stream의 `end()`는 writable side를 종료 상태로 바꾸고 `finish`를 emit합니다. 실제 underlying stream이 닫히면 `close`가 emit됩니다.
- `Transform.end()`는 `finish`를 emit한 다음 내부적으로 `push(null)`을 호출해 readable side도 종료합니다.

## Compatibility notes

- 이 모듈은 Node.js와 비슷한 API 모양을 제공하지만, Node.js stream의 완전한 drop-in replacement는 아닙니다.
- `Readable.unpipe()`는 현재 destination을 개별 추적하지 않고 source의 `data` listener를 제거하는 방식으로 동작합니다.
- `Transform`은 subclass를 만들어 `_transform()` 안에서 직접 출력을 emit하는 방식으로 사용하는 것이 적합합니다.
- 바이트 기반 transform은 `this.push(...)`를 사용하고, object 기반 parser는 `data`를 직접 emit하는 패턴이 JSH에서 더 안전합니다.