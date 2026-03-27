---
title: 서비스 관리자
type: docs
weight: 100
---

`service` 명령은 서비스 컨트롤러를 통해 장시간 실행되는 JSH 서비스를 관리합니다.
서비스 설정 읽기, 설치 및 제거, 시작과 중지, 현재 실행 상태 조회를 수행할 수 있습니다.

## 개요

`service` 명령은 실행 중인 서비스 컨트롤러와 JSON-RPC로 통신합니다.
직접 서비스를 실행하는 것이 아니라, 다음과 같은 관리 요청을 컨트롤러에 전달합니다.

- 설정 파일 읽기
- 설정 변경 적용
- JSON 파일 또는 inline 옵션으로 서비스 설치
- 서비스 시작 및 중지
- 서비스 상태 조회
- 서비스 등록 제거

## Controller Address

이 명령은 서비스 컨트롤러 endpoint가 필요합니다.
`--controller` 옵션으로 직접 지정하거나 `SERVICE_CONTROLLER` 환경 변수로 전달할 수 있습니다.

`service` 명령이 machbase-neo runtime에서 실행되면 runtime이 `SERVICE_CONTROLLER`를 자동으로
설정합니다. 일반적인 JSH 서비스 관리 흐름에서는 `--controller`를 매번 명시하실 필요가 없으므로,
아래 예시에서는 가독성을 위해 생략합니다.

지원하는 endpoint 형식은 다음과 같습니다.

- `host:port`
- `tcp://host:port`
- `unix://path`

<h6>사용 형식</h6>

```sh
service [--controller=<host:port|tcp://host:port|unix://path>] <command> [args...]
```

<h6>공통 옵션</h6>

- `-c, --controller <endpoint>` TCP 또는 Unix socket 형식의 컨트롤러 주소
- `-t, --timeout <msec>` RPC timeout, 기본값 `5000`
- `-h, --help` 도움말 표시

<h6>사용 예시</h6>

```sh
/work > service status
```

## Commands

`service` 명령은 다음 서브커맨드를 지원합니다.

- `read`
- `update`
- `reload`
- `install <config.json>`
- `install --name <name> --executable <path> [--arg <arg> ...] [--working-dir <dir>] [--enable] [--env KEY=VALUE ...]`
- `uninstall <service_name>`
- `status [service_name]`
- `start <service_name>`
- `stop <service_name>`

## 서비스 설정 형식

서비스 정의는 JSON 객체입니다.

```json
{
  "name": "alpha",
  "enable": true,
  "working_dir": "/work/app",
  "environment": {
    "APP_MODE": "prod",
    "PORT": "8080"
  },
  "executable": "node",
  "args": ["server.js", "--port", "8080"]
}
```

주요 필드는 다음과 같습니다.

| 필드 | 타입 | 설명 |
| --- | --- | --- |
| `name` | `String` | 서비스 이름 |
| `enable` | `Boolean` | 서비스 활성화 여부 |
| `working_dir` | `String` | 서비스 프로세스의 작업 디렉터리 |
| `environment` | `Object` | `KEY: VALUE` 형식의 환경 변수 맵 |
| `executable` | `String` | 실행 파일 경로 또는 명령 이름 |
| `args` | `Array<String>` | 명령행 인자 목록 |

## status

서비스 목록 전체 또는 단일 서비스 상세 정보를 표시합니다.

<h6>사용 형식</h6>

```sh
service status [service_name]
```

서비스 이름 없이 호출하면 이름, 활성화 상태, 실행 상태, PID, executable을 표로 출력합니다.

<h6>사용 예시: 서비스 목록</h6>

```sh
/work > service status
NAME   ENABLED STATUS  PID EXECUTABLE
alpha  yes     running 101 echo
beta   no      stopped -   /bin/date
```

서비스 이름을 함께 주면 작업 디렉터리, 환경 변수, 최근 출력 라인까지 포함한 상세 상태를 보여줍니다.

<h6>사용 예시: 단일 서비스</h6>

```sh
/work > service status alpha
[alpha] ENABLED
  status: running
  exit_code: 0
  pid: 55
  start: echo [ hello, world ]
  cwd: /work
  environment:
    A=1
    B=2
  output:
    line-6
    ...
    line-25
```

## read

컨트롤러의 설정 디렉터리에서 서비스 설정 파일을 읽고 변경 상태를 보고합니다.

<h6>사용 형식</h6>

```sh
service read
```

결과는 `UNCHANGED`, `ADDED`, `UPDATED`, `REMOVED`, `ERRORED` 섹션으로 나뉘어 출력됩니다.

<h6>사용 예시</h6>

```sh
/work > service read
UNCHANGED (1)
  - alpha exec=echo
ADDED (1)
  - beta exec=node
UPDATED (0)
  (none)
REMOVED (1)
  - old exec=sleep
ERRORED (1)
  - broken read_error=invalid json
```

## update 와 reload

두 명령 모두 컨트롤러에게 설정 변경 적용을 요청합니다.

- `update` 현재 설정 상태를 적용합니다.
- `reload` 설정 파일을 다시 읽고 그 결과를 적용합니다.

<h6>사용 형식</h6>

```sh
service update
service reload
```

출력은 두 섹션으로 구성됩니다.

- `ACTIONS`: `UPDATE stop`, `UPDATE start` 같은 수행 작업 목록
- `SERVICES`: 적용 후의 서비스 상태 표

## install

JSON 파일 또는 inline 옵션으로 서비스를 설치합니다.
설치에 성공하면 컨트롤러는 서비스 정의를 `/etc/services/<name>.json` 파일로 저장합니다.
파일 이름은 JSON 파일 안의 `name` 값 또는 `--name` 옵션 값으로 결정됩니다.

### JSON 파일로 설치

<h6>사용 형식</h6>

```sh
service install <config.json>
```

<h6>사용 예시</h6>

```sh
/work > service install svc.json
```

예를 들어 `svc.json`에 `"name": "alpha"`가 들어 있으면 설치된 설정은
`/etc/services/alpha.json`으로 저장됩니다.

### inline 옵션으로 설치

<h6>사용 형식</h6>

```sh
service install \
  --name <service_name> \
  --executable <path> \
  [--working-dir <dir>] \
  [--enable] \
  [--arg <arg> ...] \
  [--env KEY=VALUE ...]
```

<h6>inline 설치 옵션</h6>

- `-n, --name <name>` 서비스 이름
- `-x, --executable <path>` 실행 파일 경로 또는 명령 이름
- `-w, --working-dir <dir>` 작업 디렉터리
- `--enable` 즉시 활성화
- `-a, --arg <arg>` 실행 인자 1개 추가, 반복 가능
- `-e, --env KEY=VALUE` 환경 변수 1개 추가, 반복 가능

<h6>사용 예시</h6>

```sh
/work > service install \
  --name svc-inline \
  --executable node \
  --working-dir /work/app \
  --enable \
  --arg app.js \
  --arg --port \
  --arg 8080 \
  --env APP_MODE=prod \
  --env PORT=8080
```

이 inline 방식도 컨트롤러 쪽에 `/etc/services/svc-inline.json` 파일을 생성합니다.

이 명령은 먼저 `RESULT` 표를 출력하고, 이어서 `SERVICE` 상세 섹션을 보여줍니다.

## start 와 stop

지정한 서비스를 시작하거나 중지합니다.

<h6>사용 형식</h6>

```sh
service start <service_name>
service stop <service_name>
```

출력에는 수행 결과와 현재 서비스 상태가 함께 포함됩니다.

<h6>사용 예시</h6>

```sh
/work > service start alpha
/work > service stop alpha
```

## uninstall

서비스 등록을 제거합니다.

<h6>사용 형식</h6>

```sh
service uninstall <service_name>
```

<h6>사용 예시</h6>

```sh
/work > service uninstall alpha
RESULT
uninstall alpha yes removed
```

## 일반적인 작업 순서

먼저 서비스 JSON 파일을 준비합니다.

```json
{
  "name": "alpha",
  "enable": true,
  "working_dir": "/work",
  "executable": "echo",
  "args": ["hello", "world"]
}
```

그 다음 아래와 같은 흐름으로 관리할 수 있습니다.

```sh
/work > service install alpha.json
/work > service status
/work > service stop alpha
/work > service start alpha
/work > service uninstall alpha
```

## 참고

- `service` 명령은 접근 가능한 컨트롤러 endpoint가 필요합니다.
- `status`는 인자가 없으면 전체 목록을, 인자가 있으면 단일 서비스 상세 정보를 출력합니다.
- `install`은 config file 경로와 inline 설치 옵션을 섞어서 사용할 수 없습니다.
- inline `--env` 값은 반드시 `KEY=VALUE` 형식이어야 합니다.
- 상대 경로 config file은 현재 작업 디렉터리를 기준으로 해석됩니다.