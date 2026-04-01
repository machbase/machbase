---
title: "events"
type: docs
weight: 100
---

{{< neo_since ver="8.0.75" />}}

`events` 모듈은 JSH에서 사용할 수 있는 간단한 `EventEmitter` 구현을 제공합니다.
여러 JSH 내장 모듈이 event-driven API의 기반 클래스로 이 구현을 사용합니다.

일반적으로 아래처럼 사용합니다.

```js
const EventEmitter = require('events');
```

## EventEmitter

새 event emitter 인스턴스를 생성합니다.

<h6>사용 형식</h6>

```js
new EventEmitter()
```

이 구현은 이벤트 이름별로 listener를 저장하고, 대부분의 변경 메서드에서 emitter 자신을 반환하므로 체이닝할 수 있습니다.

## on()

이벤트 listener를 등록합니다.

<h6>사용 형식</h6>

```js
emitter.on(event, listener)
```

`listener`는 반드시 함수여야 하며, 아니면 `TypeError`가 발생합니다.

## addListener()

`on()`의 별칭입니다.

<h6>사용 형식</h6>

```js
emitter.addListener(event, listener)
```

## once()

한 번만 실행되는 listener를 등록합니다.

<h6>사용 형식</h6>

```js
emitter.once(event, listener)
```

첫 호출 뒤 자동으로 제거됩니다.

## removeListener()

일치하는 listener 하나를 제거합니다.

<h6>사용 형식</h6>

```js
emitter.removeListener(event, listener)
```

## off()

`removeListener()`의 별칭입니다.

<h6>사용 형식</h6>

```js
emitter.off(event, listener)
```

## removeAllListeners()

특정 이벤트의 모든 listener를 제거하거나, 인자가 없으면 모든 이벤트 listener를 제거합니다.

<h6>사용 형식</h6>

```js
emitter.removeAllListeners()
emitter.removeAllListeners(event)
```

## emit()

이벤트를 발생시키고, 나머지 인자를 listener에 전달합니다.

<h6>사용 형식</h6>

```js
emitter.emit(event, ...args)
```

<h6>반환값</h6>

- 해당 이벤트에 listener가 하나 이상 있으면 `true`
- 없으면 `false`

non-`error` 이벤트 처리 중 listener가 예외를 던졌고 emitter에 `error` listener가 있으면, 구현은 그 오류를 `emit('error', err)`로 전달합니다.

## 조회 helper

### listeners()

해당 이벤트에 등록된 listener 배열의 shallow copy를 반환합니다.

```js
emitter.listeners(event)
```

### listenerCount()

이벤트에 등록된 listener 수를 반환합니다.

```js
emitter.listenerCount(event)
```

### eventNames()

현재 등록된 이벤트 이름 목록을 반환합니다.

```js
emitter.eventNames()
```

## listener 제한

### setMaxListeners()

listener 수에 대한 warning 임계값을 설정합니다.

```js
emitter.setMaxListeners(n)
```

### getMaxListeners()

현재 listener warning 임계값을 반환합니다.

```js
emitter.getMaxListeners()
```

기본 최대값은 이벤트당 `10`개입니다.
이 한도를 넘으면 구현은 `console.warn()`으로 경고를 출력하지만, listener 등록 자체를 막지는 않습니다.

## 사용 예시

```js {linenos=table,linenostart=1}
const EventEmitter = require('events');

const emitter = new EventEmitter();
emitter.on('greet', function(name) {
    console.println('Hello, ' + name + '!');
});

emitter.emit('greet', 'Alice');
emitter.emit('greet', 'Bob');
```

## once() 예시

```js {linenos=table,linenostart=1}
const EventEmitter = require('events');

const emitter = new EventEmitter();
emitter.once('greet', function(name) {
    console.println('Hello, ' + name + '!');
});

emitter.emit('greet', 'Alice');
emitter.emit('greet', 'Bob');
```

## 동작 참고

- 이 모듈은 `EventEmitter` 클래스를 직접 export합니다.
- 이 구현은 경량 버전이며, Node.js `events`의 완전한 drop-in replacement는 아닙니다.
- `emit()` 시 listener 배열을 복사해서 순회하므로, emit 도중 listener를 제거해도 현재 dispatch에는 영향을 주지 않습니다.
- listener 수 초과에 대한 경고만 제공하며, 등록 자체를 차단하지는 않습니다.