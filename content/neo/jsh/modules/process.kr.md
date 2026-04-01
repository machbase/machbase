---
title: "process"
type: docs
weight: 100
---

{{< neo_since ver="8.0.75" />}}

`process` 모듈은 JSH 애플리케이션에서 사용하도록 설계되었습니다.

## addShutdownHook()

현재 프로세스가 종료될 때 호출할 콜백 함수를 추가합니다.

<h6>사용 형식</h6>

```js
addShutdownHook(()=>{})
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
process.addShutdownHook(()=>{
    console.println("shutdown hook called.");
})
console.println("running...")

// Output:
// running...
// shutdown hook called.
```

## arch

호스트 머신의 운영체제 아키텍처를 식별하는 문자열입니다.
일반적인 값은 `amd64`, `aarch64`입니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
console.println(process.arch);
```

## argv

현재 프로세스에 전달된 명령행 인자 배열입니다.

- `argv[0]`: JSH 실행 파일의 절대 경로
- `argv[1]`: 실행 중인 스크립트 이름(또는 경로)
- `argv[2:]`: 스크립트에 전달된 나머지 인자

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
console.println('argv[0]:', process.argv[0]);
console.println('argv[1]:', process.argv[1]);
console.println('argv[2]:', process.argv[2]);
console.println('argv   :', process.argv);
```

## chdir()

현재 작업 디렉터리를 변경합니다.

`path`가 빈 문자열이면 JSH는 이를 `$HOME`으로 해석합니다.

<h6>사용 형식</h6>

```js
chdir(path)
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
console.println('before:', process.cwd());
process.chdir('/lib');
console.println('after :', process.cwd());
```

## cpuUsage()

CPU 사용량 정보를 반환합니다.

현재 구현은 두 필드 모두 숫자 `0`을 반환하는 플레이스홀더입니다.

<h6>반환 필드</h6>

- `user`
- `system`

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
const cpu = process.cpuUsage();
console.println(typeof cpu.user, typeof cpu.system);
```

## cwd()

현재 작업 디렉터리 경로를 반환합니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
console.println(process.cwd());
```

## exit()

현재 프로세스를 종료합니다. *code*를 생략하면 기본값은 `0`입니다.

<h6>사용 형식</h6>

```js
exit([code])
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
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

```js {linenos=table,linenostart=1}
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

```js {linenos=table,linenostart=1}
const process = require('process');
console.println(process.expand('$HOME/file.txt'));
console.println(process.expand('${HOME}/../lib/file.txt'));
```

## env

JSH 런타임 환경 객체입니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
console.println(process.env.get('HOME'));
```


## exec()

JavaScript 명령 파일을 실행하고 종료 코드를 반환합니다.

<h6>사용 형식</h6>

```js
exec(command, ...args)
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
const path = process.which('echo');
const code = process.exec(path, 'hello from exec');
console.println('exit code:', code);
```

## execPath

호스트 운영체제에서 현재 프로세스 실행 파일의 절대 경로입니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
console.println(process.execPath);
```

## execString()

문자열로 전달한 JavaScript 소스 코드를 실행하고 종료 코드를 반환합니다.

<h6>사용 형식</h6>

```js
execString(source, ...args)
```

<h6>사용 예시</h6>


## hrtime()

고해상도 시간 튜플 `[seconds, nanoseconds]`을 반환합니다.

이전 튜플을 전달하면 해당 시점부터의 경과 시간을 반환합니다.

<h6>사용 형식</h6>

```js
hrtime([previous])
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
const start = process.hrtime();
const diff = process.hrtime([start[0], start[1]]);
console.println(Array.isArray(diff), diff.length);
```

## kill()

지정한 프로세스 ID로 실제 OS 시그널을 전송합니다.

- `pid`는 양의 정수여야 합니다.
- `signal`을 생략하면 기본값은 `SIGTERM`입니다.
- 성공하면 `true`를 반환합니다.
- 실패하면 `Error` 객체를 반환합니다.
- `signal`에는 문자열 이름 또는 숫자 시그널 번호를 사용할 수 있습니다.

문자열 이름은 대소문자를 구분하지 않으며 `SIG` 접두어를 생략할 수 있습니다.

이 별칭 지원은 `process.kill()`에 적용됩니다.

예:

- `SIGTERM`
- `term`
- `sigint`

숫자 시그널은 현재 다음 값을 지원합니다.

| 숫자 | 리터럴 |
| --- | --- |
| `0` | 없음 |
| `1` | `SIGHUP` |
| `2` | `SIGINT` |
| `3` | `SIGQUIT` |
| `6` | `SIGABRT` |
| `9` | `SIGKILL` |
| `10` | `SIGUSR1` |
| `11` | `SIGSEGV` |
| `12` | `SIGUSR2` |
| `13` | `SIGPIPE` |
| `14` | `SIGALRM` |
| `15` | `SIGTERM` |

`signal` 값 `0`은 실제 시그널을 보내지 않고, 대상 프로세스 존재 여부와 권한을 검사할 때 사용할 수 있습니다.

Windows에서 `process.kill(pid, 'SIGINT')`는 Unix의 `kill(2)`처럼 실제 시그널을 직접 보내는 동작이 아닙니다.
대신 대상 프로세스 그룹이 `SIGINT`에 가까운 인터럽트로 관찰할 수 있도록 interrupt 성격의 console control event 전달을 시도합니다.
이 동작은 Windows에서 Node.js interrupt semantic에 가장 가깝게 맞춘 것이지만 best-effort입니다.
즉, 대상이 콘솔에 연결된 프로세스 그룹이어야 하며 Windows가 control event를 라우팅할 수 없는 경우 실패할 수 있습니다.

Windows에서 `SIGTERM`, `SIGQUIT`, `SIGKILL`은 Unix처럼 서로 다른 실제 시그널이라기보다 종료 요청으로 처리됩니다.

<h6>사용 형식</h6>

```js
kill(pid[, signal])
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
console.println(process.kill(12345, 'SIGKILL'));
console.println(process.kill(12345, 'term'));
console.println(process.kill(12345, 15));
```

<h6>Windows interrupt 예시</h6>

```js
const process = require('process');
console.println(process.kill(12345, 'SIGINT'));
```

Windows가 control event를 라우팅할 수 없으면 `process.kill()`은 `Error` 객체를 반환합니다.

<h6>프로세스 존재 여부 확인 예시</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
console.println(process.kill(process.pid, 0));
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

```js {linenos=table,linenostart=1}
const process = require('process');
const mem = process.memoryUsage();
console.println(typeof mem.rss, typeof mem.heapUsed);
```

## nextTick()

다음 이벤트 루프 턴에서 실행할 콜백을 예약합니다.

첫 번째 인자가 함수가 아니면 아무 동작도 하지 않고 `undefined`를 반환합니다.

<h6>사용 형식</h6>

```js
nextTick(callback, ...args)
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
console.println('main');
process.nextTick((a, b) => console.println('tick:', a, b), 'first', 'second');
```

## now()

현재 시각을 JavaScript 날짜-시간 객체로 반환합니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
const now = process.now();
console.println(typeof now); // object
```

## pid

현재 프로세스의 ID입니다.
값의 타입은 숫자(Number)이며, 현재 프로세스 ID를 나타냅니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
console.println(process.pid);
```

## platform

호스트 머신의 운영체제 플랫폼을 식별하는 문자열입니다.
일반적인 값은 `windows`, `linux`, `darwin`(macOS)입니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
console.println(process.platform);
```

## ppid

부모 프로세스의 ID입니다.
값의 타입은 숫자(Number)이며, 부모 프로세스 ID를 나타냅니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
console.println(process.ppid);
```

## Signal Events

`process`는 `EventEmitter`처럼 시그널 이벤트를 받을 수 있습니다.

현재 문서 시점 기준으로 다음 시그널 이름을 지원합니다.

- `SIGHUP`
- `SIGINT`
- `SIGQUIT`
- `SIGABRT`
- `SIGKILL`
- `SIGUSR1`
- `SIGSEGV`
- `SIGUSR2`
- `SIGPIPE`
- `SIGALRM`
- `SIGTERM`

시그널 이벤트 리스너는 대소문자를 구분하지 않습니다.
이벤트 이름은 `SIG` 접두어를 포함한 형태만 지원합니다.

예를 들어 아래 이름들은 동일하게 동작합니다.

- `SIGTERM`
- `sigterm`

`term` 같은 bare alias는 시그널 이벤트 이름으로 취급하지 않습니다.
이 값은 일반 `EventEmitter` 이벤트 이름으로 유지됩니다.

리스너를 등록하면 JSH가 해당 OS 시그널을 이벤트로 전달합니다.
리스너가 없으면 운영체제의 기본 시그널 동작을 따릅니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const process = require('process');

process.on('sigint', () => {
  console.println('caught SIGINT');
});
```

<h6>지원하는 리스너 등록 예</h6>

```js
process.on('sigterm', handler);
process.once('SIGTERM', handler);
process.addListener('sigquit', handler);
```

## stdin, stdout, stderr

`stdin`, `stdout`, `stderr` 스트림입니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
process.stdout.write('Enter text: ');
const text = process.stdin.readLine();
console.println('Your input:', text);

// Output:
// Enter text: hello?
// Your input: hello?
```

## title

현재 프로그램을 식별하는 문자열입니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
console.println(process.title);
```

## uptime()

프로세스 업타임(초)을 숫자로 반환합니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
const up = process.uptime();
console.println('uptime >= 0:', up >= 0);
```

## version

JSH 런타임 버전을 식별하는 문자열입니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
console.println(process.version);
```

## versions

런타임의 상세 버전 정보를 제공하는 객체입니다.

- `versions.jsh`: JSH 런타임 버전 문자열
- `versions.go`: Go 런타임 버전 문자열

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
console.println('jsh:', process.versions.jsh);
console.println('go :', process.versions.go);
```

## which()

`PATH`에서 JavaScript 명령을 찾아 해석된 파일 경로를 반환합니다.

명령에 `.js` 확장자가 없으면 자동으로 추가됩니다.

<h6>사용 형식</h6>

```js
which(command)
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
console.println(process.which('echo')); // 예: /sbin/echo.js
```

## dispatchEvent()

JSH 이벤트 루프에서 이벤트 이미터 객체로 이벤트를 디스패치합니다.

이 함수는 이벤트 스케줄링에 성공하면 `true`를, 이벤트 루프가 이미 종료되었으면 `false`를 반환합니다.

<h6>사용 형식</h6>

```js
dispatchEvent(target, eventName, ...args)
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
process.on('hello', (msg) => console.println(msg));
const ok = process.dispatchEvent(process, 'hello', 'from dispatchEvent');
console.println('scheduled:', ok);
```

## dumpStack()

디버깅을 위해 지정한 깊이만큼 현재 JavaScript 호출 스택을 출력합니다.

<h6>사용 형식</h6>

```js
dumpStack(depth)
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
function trace() {
  process.dumpStack(5);
}
trace();
```

## expand()

문자열에서 `$HOME`, `${HOME}` 같은 환경 변수를 확장합니다.

<h6>사용 형식</h6>

```js
expand(value)
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
console.println(process.expand('$HOME/file.txt'));
console.println(process.expand('${HOME}/../lib/file.txt'));
```
