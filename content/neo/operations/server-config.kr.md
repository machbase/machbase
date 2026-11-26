---
title: 설정 파일
type: docs
weight: 11
---

## 새 설정 파일 만들기

`gen-config`로 machbase-neo를 실행하고 출력 결과를 기본 설정 파일로 저장합니다.

```sh
machbase-neo gen-config > ./machbase-neo.conf
```

생성된 설정 파일을 수정해 원하는 값으로 바꾼 뒤, `--config <path>` 또는 `-c <path>` 옵션으로 파일 경로를 지정해 machbase-neo를 실행하십시오.

```sh
machbase-neo serve --config ./machbase-neo.conf
```

`--config-dir <path>`를 사용하면 디렉터리의 `.conf` 파일을 파일 이름순으로 읽습니다.
두 옵션을 모두 지정하면 `--config`가 우선합니다. 둘 다 지정하지 않으면 내장된 기본 설정을 사용합니다.

## 설정 및 시작 규칙

`--` 뒤의 옵션은 `flag()`와 `flagOrError()`를 포함해 플래그로 해석하지 않습니다.
같은 플래그가 반복되면 HCL의 `flag()`는 첫 번째 값을 사용합니다. 부팅 옵션은 같은 표기의 마지막 값을 사용하며,
긴 표기와 짧은 별칭이 모두 있으면 긴 표기가 우선합니다.
`--config`, `--config-dir`, `--pid`, `--bootlog`, `--preset`, `--file` 등 값을 요구하는 부팅 옵션에
값이 없거나 비어 있으면 오류가 발생합니다. 불리언 부팅 플래그에 명시적으로 잘못된 값을 지정해도 오류가 발생합니다.
값 없이 지정한 불리언 부팅 플래그는 HCL 표현식에서 `true`입니다.
참조된 플래그에 값이 없으면 기본값이나 다음 옵션을 값으로 사용하지 않고 설정 오류가 발생합니다.
설정에서 참조하지 않는 알 수 없는 플래그는 무시합니다.
단독 `-`는 값으로 허용하며, 숫자가 아닌 다른 `-`로 시작하는 값은 `--name=-value` 형식으로 지정하십시오.

Unix에서 `--daemon`은 서버 시작이 완료된 후에만 성공을 반환합니다.
시작에 실패하거나 2분 안에 시작하지 못하면 오류를 반환합니다.
`--pid`를 지정하면 해당 PID 파일이 이미 존재해서는 안 됩니다.
프로세스는 파일을 배타적으로 생성하고 종료 시 자신이 생성한 파일을 삭제하며, 포그라운드 실행에도 같은 규칙이 적용됩니다.
오래된 PID 파일은 해당 프로세스가 더 이상 실행 중이 아닌지 확인한 후 수동으로 삭제하십시오.

Windows에서는 `arg()`와 `arglen()`이 서비스 프로세스의 원래 인자를 사용하며,
설치된 서비스의 경우 `service run`도 포함합니다. 서버 시작이 완료된 후에만 서비스가 실행 중으로 보고되며,
시작 또는 종료 중 반환된 오류는 Windows 이벤트 로그에 기록됩니다.

## 데이터베이스 디렉터리

`DataDir` 기본값은 `${execDir()}/machbase_home`으로, `machbase-neo` 실행 파일이 위치한 디렉터리 하위에 생성됩니다.

데이터베이스 파일을 저장할 새 경로로 변경하십시오. 폴더에 데이터베이스가 없으면 machbase-neo가 자동으로 새 데이터베이스를 생성합니다.

## 환경 설정 디렉터리

`PrefDir`의 기본값은 `prefDir("machbase")`이며, `$HOME/.config/machbase` 경로를 가리킵니다.

## 리스너

| Listener                  | Config                    | default                 |
|:--------------------------|:--------------------------|:------------------------|
| SSH Shell                 | Shell.Listeners           | `tcp://127.0.0.1:5652`  |
| MQTT                      | Mqtt.Listeners            | `tcp://127.0.0.1:5653` <br/> `unix://${tempDir()}/machbase-neo-mqtt.sock`  |
| HTTP                      | Http.Listeners            | `tcp://127.0.0.1:5654` <br/> `unix://${tempDir()}/machbase-neo.sock`  |
| Machbase native           | Machbase.PORT_NO          | `5656`                  |
|                           | Machbase.BIND_IP_ADDRESS  | `127.0.0.1`             |


{{< callout type="info" >}}
Machbase 네이티브 포트 `5656`은 JDBC, ODBC 등 네이티브 클라이언트가 사용합니다.
JDBC, ODBC 드라이버는 Machbase 홈페이지에서 내려받을 수 있습니다.
{{< /callout >}}

## 설정 참조

설정 파일은 HCL 문법을 따릅니다.

### functions

설정 항목 값으로 사용할 수 있는 여러 함수가 지원됩니다.

- `flag(A, B)` : 명령줄 플래그 A의 값을 가져오며, 지정되지 않으면 기본값 B를 사용합니다.
- `env(A, B)` : 환경 변수 A의 값을 가져오며, 지정되지 않으면 기본값 B를 사용합니다.
- `execDir()` : 실행 파일이 위치한 디렉터리 경로를 반환합니다.
- `tempDir()` : 시스템 임시 폴더 경로를 반환합니다. {{< neo_since ver="8.0.36" />}}
- `userDir()` : 사용자의 홈 디렉터리를 반환합니다. Linux/macOS에서는 `$HOME` 값을 사용합니다.
- `prefDir(subdir)` : 사용자의 환경 설정 디렉터리를 반환합니다. Linux/macOS에서는 `$HOME/.config/{subdir}` 실제 경로를 반환합니다.
- `envOrError(name)`, `flagOrError(name)` : 환경 변수 또는 플래그 값을 반환하며, 없으면 오류가 발생합니다.
- `arg(index, default)`, `argOrError(index)` : 0부터 시작하는 인덱스의 인자를 반환하며, 없으면 기본값 또는 오류를 반환합니다. 인자 목록에는 실행 파일과 별도로 지정한 플래그 값이 포함되지만 `-`로 시작하는 인자는 제외됩니다.
- `arglen()` : 실행 파일과 플래그를 포함한 원래 프로세스 인자의 개수를 반환합니다.
- `pname()`, `version()` : 프로세스 이름과 버전을 반환합니다.
- `execFile()`, `userConfDir()` : 실행 파일 경로와 사용자 설정 디렉터리를 반환합니다.
- `upper`, `lower`, `min`, `max`, `strlen`, `substr` : 문자열 및 숫자 함수입니다.

`define` 블록의 속성은 `<block>_<attribute>` 형식으로 참조할 수 있습니다.

{{< callout type="info">}}
**env()와 flag() 결합**<br/>
사용자 설정을 우선순위로 적용할 때는 명령줄 플래그 → 환경 변수 → 기본값 순으로 확인하는 것이 일반적입니다.
이를 위해 `flag("--my-var", env("MY_VAR", "myvalue"))`처럼 작성할 수 있습니다.
{{< /callout >}}

### define DEF

기본값을 정의하는 영역입니다. 여기서 정의한 변수는 다른 섹션에서 참조합니다.
사용자는 자신만의 변수를 정의하거나 명령줄 플래그 이름을 변경할 수도 있습니다.
예를 들어 아래에서 `LISTEN_HOST`는 명령줄 플래그 `--host` 값을 사용하지만, 플래그가 없으면 기본값 `"127.0.0.1"`을 적용합니다.

`"127.0.0.1"`을 `"192.168.1.10"`으로 바꾸면 기본값도 변경됩니다.

또한 `"--host"`를 `"--bind"`로 변경하면 명령줄 플래그 이름이 바뀌므로 이후에는 `machbase-neo serve --host` 대신 `machbase-neo serve --bind`를 사용할 수 있습니다.

```hcl
define DEF {
    LISTEN_HOST       = flag("--host", "127.0.0.1")
    SHELL_PORT        = flag("--shell-port", "5652")
    MQTT_PORT         = flag("--mqtt-port", "5653")
    HTTP_PORT         = flag("--http-port", "5654")
    MACH_PORT         = flag("--mach-port", "5656")
}
```

### define VARS

여기서는 자주 사용하는 변수를 정의합니다.

```hcl
define VARS {
    PREF_DIR              = flag("--pref", prefDir("machbase"))
    DATA_DIR              = flag("--data", "${execDir()}/machbase_home")
    FILE_DIR              = flag("--file", "${execDir()}")
    UI_DIR                = flag("--ui", "")
    MACH_LISTEN_HOST      = flag("--mach-listen-host", DEF_LISTEN_HOST)
    MACH_LISTEN_PORT      = flag("--mach-listen-port", DEF_MACH_PORT)
    SHELL_LISTEN_HOST     = flag("--shell-listen-host", DEF_LISTEN_HOST)
    SHELL_LISTEN_PORT     = flag("--shell-listen-port", DEF_SHELL_PORT)
    HTTP_LISTEN_HOST      = flag("--http-listen-host", DEF_LISTEN_HOST)
    HTTP_LISTEN_PORT      = flag("--http-listen-port", DEF_HTTP_PORT)
    MQTT_LISTEN_HOST      = flag("--mqtt-listen-host", DEF_LISTEN_HOST)
    MQTT_LISTEN_PORT      = flag("--mqtt-listen-port", DEF_MQTT_PORT)
    MQTT_MAXMESSAGE       = flag("--mqtt-max-message", 1048576) // 1MB

    HTTP_ENABLE_TOKENAUTH = flag("--http-enable-token-auth", false)
    MQTT_ENABLE_TOKENAUTH = flag("--mqtt-enable-token-auth", false)
    MQTT_ENABLE_TLS       = flag("--mqtt-enable-tls", false)

    HTTP_ENABLE_WEBUI     = flag("--http-enable-web", true)
    HTTP_DEBUG_MODE       = flag("--http-debug", false)

    EXPERIMENT_MODE       = flag("--experiment", false)

    MACHBASE_ENABLE_SIGHANDLER = flag("--machbase-enable-sighandler", false)
    MACHBASE_INIT_OPTION       = flag("--machbase-init-option", 2)

    CREATEDB_SCRIPT_FILES  = flag("--createdb-script-files", "")
}
```

### 로깅 설정

| Key                         | Type      | Desc                                                     |
|:----------------------------|:----------|----------------------------------------------------------|
| Console                     | bool      | 콘솔에 로그 메시지 출력                                  |
| Filename                    | string    | 로그 파일 경로(`-`는 stdout, 예: /logs/machbase-neo.log) |
| DefaultPrefixWidth          | int       | 로그 prefix 정렬 폭                                      |
| DefaultEnableSourceLocation | bool      | 소스 파일명과 줄 번호 기록 여부                         |
| DefaultLevel                | string    | `TRACE`, `DEBUG`, `INFO`, `WARN`, `ERROR`                |
| Levels                      | array     | 레벨 객체 배열                                           |
| Append                      | bool      | 기존 로그 파일에 이어쓰기                                |
| RotateSchedule              | string    | 로그 롤링 스케줄(예: "@midnight")                       |
| MaxSize                     | int       | 로그 파일 최대 크기(MB)                                  |
| MaxBackups                  | int       | 백업 파일 최대 개수                                      |
| MaxAge                      | int       | 백업 파일 보관 최대 일수                                 |
| Compress                    | bool      | 백업 파일 압축                                           |
| UTC                         | bool      | 로그 시간 UTC 사용                                       |

- Level object

| Key                         | Type      | Desc                                                     |
|:----------------------------|:----------|----------------------------------------------------------|
| Pattern                     | string    | 로거 이름에 대한 glob 패턴                               |
| Level                       | string    | 해당 로거에 적용할 로그 레벨                             |

```hcl
module "machbase.com/neo-logging" {
    name = "neolog"
    config {
        Console                     = false
        Filename                    = flag("--log-filename", "-")
        Append                      = flag("--log-append", true)
        RotateSchedule              = flag("--log-rotate-schedule", "@midnight")
        MaxSize                     = flag("--log-max-size", 10)
        MaxBackups                  = flag("--log-max-backups", 1)
        MaxAge                      = flag("--log-max-age", 7)
        Compress                    = flag("--log-compress", false)
        UTC                         = flag("--log-time-utc", false)
        DefaultPrefixWidth          = 16
        DefaultEnableSourceLocation = flag("--log-source-location", false)
        DefaultLevel                = flag("--log-level", "INFO")
        Levels = [
            { Pattern="neo*", Level="TRACE" },
            { Pattern="http-log", Level="DEBUG" },
        ]
    }
}
```

### 서버 설정

데이터베이스 서버와 관련된 항목으로, 아래 절에서 각각 설명합니다.

#### MachbaseHome

| Key                         | Type      | Desc                                                     |
|:----------------------------|:----------|----------------------------------------------------------|
| MachbaseHome                | string    | directory path where database files are stored           |

#### Machbase

Machbase 핵심 설정은
[Machbase 설정 프로퍼티 사전](/dbms/reference/configuration/configuration/)을
참고하십시오. 전체 매뉴얼은 [여기](/dbms)에서 확인할 수 있습니다.


#### Shell

SSH를 통해 machbase-neo 셸에 원격 접속할 수 있도록 설정합니다. 기본 `LISTEN_HOST`가 `"127.0.0.1"`이므로 동일 호스트에서만 접속할 수 있습니다. 원격 접속을 허용하려면 `"0.0.0.0"` 또는 호스트 IP 주소로 변경하십시오.

{{< callout type="warning" >}}
**Security**<br/>
원격 접속을 허용하기 전에 `SYS` 계정의 기본 비밀번호 `manager`를 변경하시기 바랍니다.
{{< /callout >}}

| Key                         | Type               | Desc                                                     |
|:----------------------------|:-------------------|----------------------------------------------------------|
| Listeners                   | array of string    | 수신 주소 (예: `tcp://127.0.0.1:5652`, `tcp://0.0.0.0:5652`)|
| IdleTimeout                 | duration           | 지정한 시간 동안 활동이 없으면 SSH 연결을 종료합니다 |


#### Http

서버의 HTTP 리스너 설정입니다.

| Key                         | Type               | Desc                                                     |
|:----------------------------|:-------------------|----------------------------------------------------------|
| Listeners                   | array of string    | 수신 주소                                                |
| EnableTokenAuth             | bool               | 토큰 기반 인증 활성화(기본값 `false`)                    |
| EnableWebUI                 | bool               | 웹 UI 활성화(기본값 `true`)                               |

#### Mqtt

| Key                         | Type               | Desc                                                     |
|:----------------------------|:-------------------|----------------------------------------------------------|
| Listeners                   | array of string    | 수신 주소                                                |
| MaxMessageSizeLimit         | int                | PUBLISH 페이로드 최대 크기(기본 1048576 = 1MB)             |
| EnableTokenAuth             | bool               | 토큰 기반 인증 활성화(기본값 `false`)                    |
| EnableTls                   | bool               | TCP 리스너 TLS 활성화(기본값 `false`)                     |

### neo-server config

```hcl
module "machbase.com/neo-server" {
    name = "neosvr"
    config {
        PrefDir          = VARS_PREF_DIR
        DataDir          = VARS_DATA_DIR
        FileDirs         = [ VARS_FILE_DIR ]
        ExperimentMode   = VARS_EXPERIMENT_MODE
        CreateDBScriptFiles = [ VARS_CREATEDB_SCRIPT_FILES ]
        Machbase         = {
            HANDLE_LIMIT     = 2048
            PORT_NO          = VARS_MACH_LISTEN_PORT
            BIND_IP_ADDRESS  = VARS_MACH_LISTEN_HOST
        }
        Shell = {
            Listeners        = [ "tcp://${VARS_SHELL_LISTEN_HOST}:${VARS_SHELL_LISTEN_PORT}" ]
            IdleTimeout      = "5m"
        }
        Http = {
            Listeners        = [ "tcp://${VARS_HTTP_LISTEN_HOST}:${VARS_HTTP_LISTEN_PORT}" ]
            WebDir           = VARS_UI_DIR
            EnableTokenAuth  = VARS_HTTP_ENABLE_TOKENAUTH
            DebugMode        = VARS_HTTP_DEBUG_MODE
            EnableWebUI      = VARS_HTTP_ENABLE_WEBUI
        }
        Mqtt = {
            Listeners           = [ "tcp://${VARS_MQTT_LISTEN_HOST}:${VARS_MQTT_LISTEN_PORT}"]
            EnableTokenAuth     = VARS_MQTT_ENABLE_TOKENAUTH
            EnableTls           = VARS_MQTT_ENABLE_TLS
            MaxMessageSizeLimit = VARS_MQTT_MAXMESSAGE
        }
        Jwt = {
            AtDuration = flag("--jwt-at-expire", "5m")
            RtDuration = flag("--jwt-rt-expire", "60m")
        }
        MachbaseInitOption       = VARS_MACHBASE_INIT_OPTION
        EnableMachbaseSigHandler = VARS_MACHBASE_ENABLE_SIGHANDLER
    }
}
```
