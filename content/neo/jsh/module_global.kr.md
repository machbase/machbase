---
title: "global"
type: docs
weight: 10
---

별도의 모듈 로딩 없이 바로 사용할 수 있는 전역 함수와 객체입니다.

타이머 관련 API는 JSH 이벤트 루프에 포함된 구현을 사용하며, `console` 객체는 기본 출력과 로그
출력을 제공합니다.

## setTimeout()

지정한 시간(ms) 이후에 콜백을 한 번 실행합니다.

추가 인자를 전달하면 콜백 함수의 인자로 그대로 전달됩니다.

<h6>사용 형식</h6>

```js
setTimeout(callback, delayMs[, ...args])
```

<h6>반환값</h6>

- 타이머 핸들 객체. `clearTimeout()`에 전달해 실행을 취소할 수 있습니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[2,3,4]}
setTimeout((name, count) => {
	console.println("Timeout with args:", name, count);
}, 50, "test", 42);

// Output:
// Timeout with args: test 42
```

## clearTimeout()

`setTimeout()`으로 등록한 작업이 아직 실행되지 않았다면 취소합니다.

이미 실행이 끝났거나 이미 취소된 타이머에 다시 호출해도 추가 동작 없이 무시됩니다.

<h6>사용 형식</h6>

```js
clearTimeout(timer)
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[2,3]}
const timer = setTimeout(() => {
	console.println("should not run");
}, 100);

clearTimeout(timer);
clearTimeout(timer);
```

## setInterval()

지정한 간격(ms)마다 콜백을 반복 실행합니다.

반복 실행을 중단하려면 반환된 핸들을 `clearInterval()`에 전달합니다.

<h6>사용 형식</h6>

```js
setInterval(callback, delayMs[, ...args])
```

<h6>반환값</h6>

- 인터벌 핸들 객체. `clearInterval()`에 전달해 반복 실행을 중단할 수 있습니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[4,6]}
let count = 0;
const timer = setInterval(() => {
	count++;
	console.println("count:", count);
	if (count >= 3) {
		clearInterval(timer);
	}
}, 100);
```

## clearInterval()

`setInterval()`로 등록한 반복 작업을 중지합니다.

<h6>사용 형식</h6>

```js
clearInterval(interval)
```

## setImmediate()

현재 실행이 끝난 뒤 다음 이벤트 루프 순환에서 콜백을 가능한 한 빨리 실행합니다.

타이머 지연값 없이 비동기 후속 작업을 예약할 때 유용합니다.

<h6>사용 형식</h6>

```js
setImmediate(callback[, ...args])
```

<h6>반환값</h6>

- 즉시 실행 작업 핸들 객체. `clearImmediate()`에 전달해 실행을 취소할 수 있습니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[2,3]}
console.println("Add event loop");
setImmediate(() => {
	console.println("event loop called");
});

// Output:
// Add event loop
// event loop called
```

## clearImmediate()

`setImmediate()`로 예약한 콜백이 아직 실행되지 않았다면 취소합니다.

<h6>사용 형식</h6>

```js
clearImmediate(immediate)
```

## console

전역 `console` 객체는 로그 출력과 표준 출력용 메서드를 제공합니다.

## console.log()

정보 레벨 로그를 출력합니다. 출력에는 `INFO` 레벨 문자열이 포함됩니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
console.log("Hello, World!");

// Output:
// INFO  Hello, World!
```

## console.debug()

디버그 레벨 로그를 출력합니다.

## console.info()

정보 레벨 로그를 출력합니다. `console.log()`와 같은 레벨을 사용합니다.

## console.warn()

경고 레벨 로그를 출력합니다.

## console.error()

오류 레벨 로그를 출력합니다.

## console.print()

개행 없이 값을 이어서 출력합니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
console.print("hello", "world");

// Output:
// helloworld
```

## console.println()

값 사이에 공백을 넣어 출력하고 마지막에 개행을 추가합니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
console.println("hello", "world");

// Output:
// hello world
```

## console.printf()

형식 문자열을 사용해 출력합니다.

<h6>사용 형식</h6>

```js
console.printf(format, ...args)
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
console.printf("value=%d, name=%s\n", 42, "neo");

// Output:
// value=42, name=neo
```

