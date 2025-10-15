---
title: "@jsh/system"
type: docs
weight: 5
---

{{< neo_since ver="8.0.52" />}}

## now()

현재 시간을 네이티브 객체로 반환합니다.

<h6>사용 형식</h6>

```js
now()
```

<h6>매개변수</h6>

없음.

<h6>반환값</h6>

네이티브 시간 객체.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const m = require("@jsh/system")
console.log("now =", m.now())
```


## parseTime()

문자열이나 에포크 값을 지정한 형식으로 파싱해 시간 객체로 변환합니다.

<h6>사용 형식</h6>

```js
parseTime(epoch, epoch_format)
parseTime(datetime, format)
parseTime(datetime, format, location)
```

<h6>매개변수</h6>

- `epoch` `Number` 기준 에포크 값입니다.
- `epoch_format` `String` `"s"`, `"ms"`, `"us"`, `"ns"` 가운데 하나를 지정합니다.
- `datetime` `String` 변환할 날짜/시간 문자열입니다.
- `format` `String` Go 시간 서식 문자열입니다.
- `location` `Location` 시간대 정보입니다. 생략하면 `"Local"`이 기본값이며 `system.location("EST")`, `system.location("America/New_York")`처럼 지정할 수 있습니다.

<h6>반환값</h6>

네이티브 시간 객체.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const {println} = require("@jsh/process");
const system = require("@jsh/system");
ts = system.parseTime(
    "2023-10-01 12:00:00",
    "2006-01-02 15:04:05",
    system.location("UTC"));
println(ts.In(system.location("UTC")).Format("2006-01-02 15:04:05"));

// 2023-10-01 12:00:00
```


## location()

시간대 문자열을 네이티브 위치 객체로 변환합니다.

<h6>사용 형식</h6>

```js
location(timezone)
```

<h6>매개변수</h6>

- `timezone` `String` `"UTC"`, `"Local"`, `"GMT"`, `"ETS"`, `"America/New_York"` 등과 같은 시간대 식별자입니다.

<h6>반환값</h6>

네이티브 위치 객체.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const {println} = require("@jsh/process");
const system = require("@jsh/system");
ts = system.time(1).In(system.location("UTC"));
println(ts.Format("2006-01-02 15:04:05"));

// 1970-01-01 00:00:01
```

## Log

애플리케이션 로깅을 위한 헬퍼 클래스입니다.

<h6>생성</h6>

| 생성자                  | 설명                                  |
|:------------------------|:----------------------------------------------|
| new Log(*name*)         | 지정한 이름으로 로거를 생성합니다             |

<h6>옵션</h6>

- `name` `String` 로거 이름입니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const system = require("@jsh/system");
const log = new system.Log("testing");

log.info("hello", "world");

// 로그 출력:
//
// 2025/05/13 14:08:41.937 INFO  testing    hello world
```

### trace()

<h6>사용 형식</h6>

```js
trace(...args)
```

<h6>매개변수</h6>

- `args` `any` 로그 메시지에 사용할 가변 길이 인자입니다.

<h6>반환값</h6>

없음.

### debug()

<h6>사용 형식</h6>

```js
debug(...args)
```

<h6>매개변수</h6>

- `args` `any` 로그 메시지에 사용할 가변 길이 인자입니다.

<h6>반환값</h6>

없음.

### info()

<h6>사용 형식</h6>

```js
info(...args)
```

<h6>매개변수</h6>

- `args` `any` 로그 메시지에 사용할 가변 길이 인자입니다.

<h6>반환값</h6>

없음.

### warn()

<h6>사용 형식</h6>

```js
warn(...args)
```

<h6>매개변수</h6>

- `args` `any` 로그 메시지에 사용할 가변 길이 인자입니다.

<h6>반환값</h6>

없음.

### error()

<h6>사용 형식</h6>

```js
error(...args)
```

<h6>매개변수</h6>

- `args` `any` 로그 메시지에 사용할 가변 길이 인자입니다.

<h6>반환값</h6>

없음.
