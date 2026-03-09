---
title: "process"
type: docs
weight: 100
---

{{< neo_since ver="8.0.73" />}}

`process` 모듈은 JSH 애플리케이션에서 사용하도록 설계되었습니다.

## env

JSH 런타임 환경 객체입니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const process = require('process');
console.println(process.env.get('HOME'));
```

## execPath

호스트 운영체제에서 현재 프로세스 실행 파일의 절대 경로입니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const process = require('process');
console.println(process.execPath);
```

## pid

현재 프로세스의 ID입니다.
값의 타입은 숫자(Number)이며, 현재 프로세스 ID를 나타냅니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const process = require('process');
console.println(process.pid);
```

## ppid

부모 프로세스의 ID입니다.
값의 타입은 숫자(Number)이며, 부모 프로세스 ID를 나타냅니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const process = require('process');
console.println(process.ppid);
```

## platform

호스트 머신의 운영체제 플랫폼을 식별하는 문자열입니다.
일반적인 값은 `windows`, `linux`, `darwin`(macOS)입니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const process = require('process');
console.println(process.platform);
```

## arch

호스트 머신의 운영체제 아키텍처를 식별하는 문자열입니다.
일반적인 값은 `amd64`, `aarch64`입니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const process = require('process');
console.println(process.arch);
```

## version

JSH 런타임 버전을 식별하는 문자열입니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const process = require('process');
console.println(process.version);
```

## versions

런타임의 상세 버전 정보를 제공하는 객체입니다.

- `versions.jsh`: JSH 런타임 버전 문자열
- `versions.go`: Go 런타임 버전 문자열

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[2,3]}
const process = require('process');
console.println('jsh:', process.versions.jsh);
console.println('go :', process.versions.go);
```

## title

현재 프로그램을 식별하는 문자열입니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const process = require('process');
console.println(process.title);
```


## stdin, stdout, stderr

`stdin`, `stdout`, `stderr` 스트림입니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[2,3]}
const process = require('process');
process.stdout.write('Enter text: ');
const text = process.stdin.readLine();
console.println('Your input:', text);

// Output:
// Enter text: hello?
// Your input: hello?
```

## addShutdownHook()

현재 프로세스가 종료될 때 호출할 콜백 함수를 추가합니다.

<h6>사용 형식</h6>

```js
addShutdownHook(()=>{})
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const process = require('process');
process.addShutdownHook(()=>{
    console.println("shutdown hook called.");
})
console.println("running...")

// Output:
// running...
// shutdown hook called.
```

## exit()

현재 프로세스를 종료합니다. *code*를 생략하면 기본값은 `0`입니다.

<h6>사용 형식</h6>

```js
exit([code])
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const process = require('process');
process.exit(-1);
```


## which()

`PATH`에서 JavaScript 명령을 찾아 해석된 파일 경로를 반환합니다.

명령에 `.js` 확장자가 없으면 자동으로 추가됩니다.

<h6>사용 형식</h6>

```js
which(command)
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const process = require('process');
console.println(process.which('echo')); // 예: /sbin/echo.js
```

## expand()

문자열에서 `$HOME`, `${HOME}` 같은 환경 변수를 확장합니다.

<h6>사용 형식</h6>

```js
expand(value)
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[2,3]}
const process = require('process');
console.println(process.expand('$HOME/file.txt'));
console.println(process.expand('${HOME}/../lib/file.txt'));
```

## exec()

JavaScript 명령 파일을 실행하고 종료 코드를 반환합니다.

<h6>사용 형식</h6>

```js
exec(command, ...args)
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[3]}
const process = require('process');
const path = process.which('echo');
const code = process.exec(path, 'hello from exec');
console.println('exit code:', code);
```

## execString()

문자열로 전달한 JavaScript 소스 코드를 실행하고 종료 코드를 반환합니다.

<h6>사용 형식</h6>

```js
execString(source, ...args)
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const process = require('process');
const code = process.execString("console.println('hello from execString')");
console.println('exit code:', code);
```

## dispatchEvent()

JSH 이벤트 루프에서 이벤트 이미터 객체로 이벤트를 디스패치합니다.

이 함수는 이벤트 스케줄링에 성공하면 `true`를, 이벤트 루프가 이미 종료되었으면 `false`를 반환합니다.

<h6>사용 형식</h6>

```js
dispatchEvent(target, eventName, ...args)
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[3]}
const process = require('process');
process.on('hello', (msg) => console.println(msg));
const ok = process.dispatchEvent(process, 'hello', 'from dispatchEvent');
console.println('scheduled:', ok);
```

## now()

현재 시각을 JavaScript 날짜-시간 객체로 반환합니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[2,3]}
const process = require('process');
const now = process.now();
console.println(typeof now); // object
```

## chdir()

현재 작업 디렉터리를 변경합니다.

`path`가 빈 문자열이면 JSH는 이를 `$HOME`으로 해석합니다.

<h6>사용 형식</h6>

```js
chdir(path)
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[3,4]}
const process = require('process');
console.println('before:', process.cwd());
process.chdir('/lib');
console.println('after :', process.cwd());
```

## cwd()

현재 작업 디렉터리 경로를 반환합니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const process = require('process');
console.println(process.cwd());
```

## nextTick()

다음 이벤트 루프 턴에서 실행할 콜백을 예약합니다.

첫 번째 인자가 함수가 아니면 아무 동작도 하지 않고 `undefined`를 반환합니다.

<h6>사용 형식</h6>

```js
nextTick(callback, ...args)
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[3]}
const process = require('process');
console.println('main');
process.nextTick((a, b) => console.println('tick:', a, b), 'first', 'second');
```

## memoryUsage()

메모리 사용량 정보를 객체로 반환합니다.

현재 구현은 모든 필드를 숫자 `0`으로 반환하는 플레이스홀더입니다.

<h6>반환 필드</h6>

- `rss`
- `heapTotal`
- `heapUsed`
- `external`
- `arrayBuffers`

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[3]}
const process = require('process');
const mem = process.memoryUsage();
console.println(typeof mem.rss, typeof mem.heapUsed);
```

## cpuUsage()

CPU 사용량 정보를 반환합니다.

현재 구현은 두 필드 모두 숫자 `0`을 반환하는 플레이스홀더입니다.

<h6>반환 필드</h6>

- `user`
- `system`

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[3]}
const process = require('process');
const cpu = process.cpuUsage();
console.println(typeof cpu.user, typeof cpu.system);
```

## uptime()

프로세스 업타임(초)을 숫자로 반환합니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[3]}
const process = require('process');
const up = process.uptime();
console.println('uptime >= 0:', up >= 0);
```

## hrtime()

고해상도 시간 튜플 `[seconds, nanoseconds]`을 반환합니다.

이전 튜플을 전달하면 해당 시점부터의 경과 시간을 반환합니다.

<h6>사용 형식</h6>

```js
hrtime([previous])
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[2,3]}
const process = require('process');
const start = process.hrtime();
const diff = process.hrtime([start[0], start[1]]);
console.println(Array.isArray(diff), diff.length);
```

## kill()

지정한 프로세스 ID로 시그널 전송을 요청합니다.

현재 구현은 플레이스홀더 동작입니다.

- `pid`가 없으면 `Error` 객체를 반환합니다.
- `pid`가 있으면 `true`를 반환합니다. (`signal` 기본값: `SIGTERM`)

<h6>사용 형식</h6>

```js
kill(pid[, signal])
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const process = require('process');
console.println(process.kill(12345, 'SIGKILL'));
```

## dumpStack()

디버깅을 위해 지정한 깊이만큼 현재 JavaScript 호출 스택을 출력합니다.

<h6>사용 형식</h6>

```js
dumpStack(depth)
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[3]}
const process = require('process');
function trace() {
  process.dumpStack(5);
}
trace();
```
