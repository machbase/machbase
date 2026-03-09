---
title: "os"
type: docs
weight: 100
---

{{< neo_since ver="8.0.73" />}}

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

## type()

`Darwin`, `Linux`, `Windows_NT` 같은 OS 타입 문자열을 반환합니다.

<h6>사용 형식</h6>

```js
type()
```

## release()

커널 릴리스/버전 문자열을 반환합니다.

<h6>사용 형식</h6>

```js
release()
```

## hostname()

호스트 이름을 반환합니다.

<h6>사용 형식</h6>

```js
hostname()
```

## homedir()

현재 사용자 홈 디렉터리 경로를 반환합니다.

<h6>사용 형식</h6>

```js
homedir()
```

## tmpdir()

운영체제 기본 임시 디렉터리 경로를 반환합니다.

<h6>사용 형식</h6>

```js
tmpdir()
```

## endianness()

CPU 엔디언을 반환합니다. 값은 `BE` 또는 `LE`입니다.

<h6>사용 형식</h6>

```js
endianness()
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

## bootTime()

시스템 부팅 시각(Unix timestamp)을 반환합니다.

<h6>사용 형식</h6>

```js
bootTime()
```

## loadavg()

로드 평균을 `[1분, 5분, 15분]` 배열로 반환합니다.

<h6>사용 형식</h6>

```js
loadavg()
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

## userInfo()

현재 사용자 정보를 반환합니다.

반환 필드:

- `username`, `homedir`, `shell`
- `uid`, `gid`

<h6>사용 형식</h6>

```js
userInfo([options])
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

## diskIOCounters()

디스크 I/O 카운터를 반환합니다.

- `names` 생략/빈 배열: 전체 디바이스
- `names` 지정: 선택한 디바이스

<h6>사용 형식</h6>

```js
diskIOCounters([names])
```

## netProtoCounters()

네트워크 프로토콜 카운터를 반환합니다.

<h6>사용 형식</h6>

```js
netProtoCounters([proto])
```

## constants

OS 상수 객체입니다.

<h6>주요 필드</h6>

- `constants.signals`
  - `SIGHUP`, `SIGINT`, `SIGQUIT`, `SIGILL`, `SIGTRAP`, `SIGABRT`, `SIGBUS`, `SIGFPE`, `SIGKILL`, `SIGUSR1`, `SIGSEGV`, `SIGUSR2`, `SIGPIPE`, `SIGALRM`, `SIGTERM`
- `constants.priority`
  - `PRIORITY_LOW`, `PRIORITY_BELOW_NORMAL`, `PRIORITY_NORMAL`, `PRIORITY_ABOVE_NORMAL`, `PRIORITY_HIGH`, `PRIORITY_HIGHEST`

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[2,3]}
const os = require('os');
console.println(os.constants.signals.SIGINT);
console.println(os.constants.priority.PRIORITY_NORMAL);
```
