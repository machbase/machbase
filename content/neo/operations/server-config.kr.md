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
| gRPC                      | Grpc.Listeners            | `tcp://127.0.0.1:5655` <br/> `unix://${execDir()}/mach-grpc.sock` |
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
    GRPC_PORT         = flag("--grpc-port", "5655")
    GRPC_SOCK         = flag("--grpc-sock", "${execDir()}/mach-grpc.sock")
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
    GRPC_LISTEN_HOST      = flag("--grpc-listen-host", DEF_LISTEN_HOST)
    GRPC_LISTEN_PORT      = flag("--grpc-listen-port", DEF_GRPC_PORT)
    GRPC_LISTEN_SOCK      = flag("--grpc-listen-sock", DEF_GRPC_SOCK)
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

Machbase 핵심 설정은 [Machbase 매뉴얼의 Property 섹션](/dbms/config-monitor/property/)을 참고하십시오. 전체 매뉴얼은 [여기](/dbms)에서 확인할 수 있습니다.


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


#### Grpc

machbase-neo의 gRPC 수신 주소와 메시지 크기 제한을 설정합니다.

| Key                         | Type               | Desc                                                     |
|:----------------------------|:-------------------|----------------------------------------------------------|
| Listeners                   | array of string    | 수신 주소                                                |
| MaxRecvMsgSize              | int                | 서버가 받을 수 있는 최대 메시지 크기(MB)                 |
| MaxSendMsgSize              | int                | 서버가 보낼 수 있는 최대 메시지 크기(MB)                 |

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
        Grpc = {
            Listeners        = [ 
                "unix://${VARS_GRPC_LISTEN_SOCK}",
                "tcp://${VARS_GRPC_LISTEN_HOST}:${VARS_GRPC_LISTEN_PORT}",
            ]
            MaxRecvMsgSize   = 4
            MaxSendMsgSize   = 4
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
