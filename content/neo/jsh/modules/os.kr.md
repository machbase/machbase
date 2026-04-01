---
title: "os"
type: docs
weight: 100
---

{{< neo_since ver="8.0.75" />}}

`os` 모듈은 JSH 애플리케이션에서 사용할 수 있는 Node.js 호환 운영체제 정보 API를 제공합니다.

## arch()

CPU 아키텍처를 반환합니다.

<h6>사용 형식</h6>

```js
arch()
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const os = require('os');
console.println(os.arch());
```

## platform()

`darwin`, `linux`, `windows` 같은 플랫폼 이름을 반환합니다.

<h6>사용 형식</h6>

```js
platform()
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const os = require('os');
console.println(os.platform());
```

## type()

`Darwin`, `Linux`, `Windows_NT` 같은 OS 타입 문자열을 반환합니다.

<h6>사용 형식</h6>

```js
type()
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const os = require('os');
console.println(os.type());
```

## release()

커널 릴리스/버전 문자열을 반환합니다.

<h6>사용 형식</h6>

```js
release()
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const os = require('os');
console.println(os.release());
```

## hostname()

호스트 이름을 반환합니다.

<h6>사용 형식</h6>

```js
hostname()
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const os = require('os');
console.println(os.hostname());
```

## homedir()

현재 사용자 홈 디렉터리 경로를 반환합니다.

<h6>사용 형식</h6>

```js
homedir()
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const os = require('os');
console.println(os.homedir());
```

## tmpdir()

운영체제 기본 임시 디렉터리 경로를 반환합니다.

<h6>사용 형식</h6>

```js
tmpdir()
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const os = require('os');
console.println(os.tmpdir());
```

## endianness()

CPU 엔디언을 반환합니다. 값은 `BE` 또는 `LE`입니다.

<h6>사용 형식</h6>

```js
endianness()
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const os = require('os');
console.println(os.endianness());
```

## EOL

플랫폼별 줄바꿈 문자열입니다.

- POSIX: `\n`
- Windows: `\r\n`

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const os = require('os');
console.println(JSON.stringify(os.EOL));
```

## totalmem(), freemem()

시스템 전체/가용 메모리(바이트)를 반환합니다.

<h6>사용 형식</h6>

```js
totalmem()
freemem()
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[2,3]}
const os = require('os');
console.println('total:', os.totalmem());
console.println('free :', os.freemem());
```

## uptime()

시스템 업타임(초)을 반환합니다.

<h6>사용 형식</h6>

```js
uptime()
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const os = require('os');
console.println(os.uptime() >= 0);
```

## bootTime()

시스템 부팅 시각(Unix timestamp)을 반환합니다.

<h6>사용 형식</h6>

```js
bootTime()
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const os = require('os');
console.println(os.bootTime() > 0);
```

## loadavg()

로드 평균을 `[1분, 5분, 15분]` 배열로 반환합니다.

<h6>사용 형식</h6>

```js
loadavg()
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[3]}
const os = require('os');
const avg = os.loadavg();
console.println(Array.isArray(avg), avg.length);
```

## cpus()

CPU 코어별 정보 배열을 반환합니다.

각 항목에는 다음과 같은 필드가 포함됩니다.

- `model`, `speed`, `cores`
- `vendor`, `family`, `model`, `stepping`
- `times.user`, `times.nice`, `times.sys`, `times.idle`, `times.irq` (밀리초)

<h6>사용 형식</h6>

```js
cpus()
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[3]}
const os = require('os');
const list = os.cpus();
console.println(Array.isArray(list), list.length > 0);
```

## cpuCounts()

CPU 개수를 반환합니다.

- `true`: 논리 코어 수
- `false`: 물리 코어 수

<h6>사용 형식</h6>

```js
cpuCounts(logical)
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[2,3]}
const os = require('os');
console.println(os.cpuCounts(true));
console.println(os.cpuCounts(false));
```

## cpuPercent()

CPU 사용률(%) 배열을 반환합니다.

- `intervalSec`: 샘플링 간격(초), `0`이면 즉시 값
- `perCPU`: `true`면 코어별 배열 반환

<h6>사용 형식</h6>

```js
cpuPercent(intervalSec, perCPU)
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const os = require('os');
console.println(Array.isArray(os.cpuPercent(0, true)));
```

## networkInterfaces()

네트워크 인터페이스 정보를 객체로 반환합니다.

반환 형태는 다음과 같습니다.

- key: 인터페이스 이름
- value: 주소 정보 배열
  - `address`
  - `family` (`IPv4`/`IPv6`)
  - `internal` (boolean)

<h6>사용 형식</h6>

```js
networkInterfaces()
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[3]}
const os = require('os');
const ifaces = os.networkInterfaces();
console.println(typeof ifaces);
```

## hostInfo()

호스트 시스템 정보 객체를 반환합니다.

주요 필드는 다음과 같습니다.

- `hostname`, `uptime`, `bootTime`, `procs`
- `os`, `platform`, `platformFamily`, `platformVersion`
- `kernelVersion`, `kernelArch`
- `virtualizationSystem`, `virtualizationRole`, `hostId`

<h6>사용 형식</h6>

```js
hostInfo()
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[3]}
const os = require('os');
const info = os.hostInfo();
console.println(typeof info.hostname, typeof info.uptime);
```

## userInfo()

현재 사용자 정보를 반환합니다.

반환 필드:

- `username`, `homedir`, `shell`
- `uid`, `gid`

<h6>사용 형식</h6>

```js
userInfo([options])
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[3]}
const os = require('os');
const user = os.userInfo();
console.println(user.username, user.homedir);
```

## diskPartitions()

디스크 파티션 목록을 반환합니다.

<h6>사용 형식</h6>

```js
diskPartitions([all])
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[3]}
const os = require('os');
const parts = os.diskPartitions();
console.println(Array.isArray(parts), parts.length >= 0);
```

## diskUsage()

지정한 경로의 디스크 사용량 정보를 반환합니다.

일반적으로 `total`, `used`, `free`, `usedPercent` 필드를 포함합니다.

<h6>사용 형식</h6>

```js
diskUsage(path)
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[3]}
const os = require('os');
const usage = os.diskUsage('.');
console.println(typeof usage.total, typeof usage.usedPercent);
```

## diskIOCounters()

디스크 I/O 카운터를 반환합니다.

- `names` 생략/빈 배열: 전체 디바이스
- `names` 지정: 선택한 디바이스

<h6>사용 형식</h6>

```js
diskIOCounters([names])
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[3]}
const os = require('os');
const counters = os.diskIOCounters();
console.println(typeof counters);
```

## netProtoCounters()

네트워크 프로토콜 카운터를 반환합니다.

<h6>사용 형식</h6>

```js
netProtoCounters([proto])
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[3]}
const os = require('os');
const counters = os.netProtoCounters();
console.println(typeof counters);
```

## constants

운영체제 관련 상수 객체입니다.

현재 다음 하위 객체를 제공합니다.

- `os.constants.signals`
- `os.constants.priority`

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[3,4]}
const os = require('os');

console.println(typeof os.constants.signals.SIGINT);
console.println(typeof os.constants.priority.PRIORITY_NORMAL);
```

## os.constants.signals

시그널 이름과 숫자 값을 제공하는 상수 객체입니다.

이 상수들은 API 호환성을 위해 정규화된 Unix 스타일 시그널 번호를 사용합니다.
Windows에서는 모든 숫자 값이 서로 다른 네이티브 시그널 동작에 일대일 대응하지는 않습니다.

예를 들어 다음 항목을 포함합니다.

| 리터럴 | 숫자 |
| --- | --- |
| `SIGHUP` | `1` |
| `SIGINT` | `2` |
| `SIGQUIT` | `3` |
| `SIGABRT` | `6` |
| `SIGKILL` | `9` |
| `SIGUSR1` | `10` |
| `SIGSEGV` | `11` |
| `SIGUSR2` | `12` |
| `SIGPIPE` | `13` |
| `SIGALRM` | `14` |
| `SIGTERM` | `15` |

이 값들은 `process.kill()`에 숫자 시그널로 전달할 때 사용할 수 있습니다.

Windows에서 `SIGINT`는 특별하게 처리됩니다.
JSH는 이를 가능한 한 interrupt 성격의 console control event로 전달하려고 시도합니다.
반면 `SIGTERM`, `SIGQUIT`, `SIGKILL`은 Windows에서 종료 요청으로 동작합니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[4]}
const os = require('os');
const process = require('process');

process.kill(12345, os.constants.signals.SIGTERM);
```

## process 시그널 API와의 관계

`os.constants.signals`는 시그널 번호를 제공하고, 실제 시그널 처리와 전송은 `process` 모듈에서 수행합니다.

- 시그널 수신: `process.on('SIGINT', handler)`
- 시그널 전송: `process.kill(pid, os.constants.signals.SIGTERM)`

`process.on()`은 대소문자를 구분하지 않지만, 시그널 이벤트 이름은 `SIGINT`, `sigint`처럼 `SIG` 접두어를 포함한 정규 이름만 사용해야 합니다.
`term` 같은 bare alias는 시그널 리스너 이름이 아닙니다.

반대로 `process.kill()`은 canonical 이름 외에도 `term` 같은 alias를 허용합니다.
`os.constants.signals`는 정규화된 상수 이름만 제공합니다.

Windows에서 `process.kill(pid, os.constants.signals.SIGINT)`는 best-effort 동작이며, Windows 콘솔 라우팅 제약에 따라 실패할 수 있습니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[4,8]}
const os = require('os');
const process = require('process');

process.on('sigint', () => {
  console.println('caught');
});

process.kill(process.pid, os.constants.signals.SIGINT);
```

## os.constants.priority

프로세스 우선순위 수준을 나타내는 상수 객체입니다.

<h6>주요 필드</h6>

| 상수 | 설명 |
| --- | --- |
| `PRIORITY_LOW` | 낮은 우선순위 |
| `PRIORITY_BELOW_NORMAL` | 보통보다 낮은 우선순위 |
| `PRIORITY_NORMAL` | 기본 우선순위 |
| `PRIORITY_ABOVE_NORMAL` | 보통보다 높은 우선순위 |
| `PRIORITY_HIGH` | 높은 우선순위 |
| `PRIORITY_HIGHEST` | 가장 높은 우선순위 |

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[2,3]}
const os = require('os');
console.println(os.constants.priority.PRIORITY_NORMAL);
console.println(os.constants.priority.PRIORITY_HIGH);
```
