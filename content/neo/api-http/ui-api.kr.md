---
title: 사용자 인터페이스 API
type: docs
weight: 55
---

이 사용자 인터페이스 API는 JWT 기반 인증으로 클라이언트 요청을 검증합니다.

## 사용자 인증

### 로그인

**POST `/web/api/login`**

{{< tabs >}}
{{< tab name="Request" >}}
```json
{
    "loginName": "sys",
    "password": "manager"
}
```
{{< /tab >}}
{{< tab name="Response" >}}
```json
{
    "success": true,
    "accessToken": "jwt-access-token",
    "refreshToken": "jwt-refresh-token",
    "reason": "string",
    "elapse": "string",
    "server": { "version": "v1.2.3" }
}
```
{{< /tab >}}
{{< /tabs >}}

### 토큰 갱신

**POST `/web/api/relogin`**

{{< tabs >}}
{{< tab name="Request" >}}
```json
{
    "refreshToken": "refresh token that was issued with 'login'"
}
```
{{< /tab >}}
{{< tab name="Response" >}}
```json
{
    "success": true,
    "accessToken": "jwt access token",
    "refreshToken": "jwt refresh token",
    "reason": "string",
    "elapse": "string",
    "server": { "version": "v1.2.3" }
}
```
{{< /tab >}}
{{< /tabs >}}

### 로그아웃

**POST `/web/api/logout`**

- `LogoutReq`:

```json
{
    "refreshToken": "refresh token that was issued with 'login'"
}
```

### 상태 확인

**GET `/web/api/check`**

현재 토큰 상태를 검증합니다.

- `LoginCheckRsp`

```json
{
    "success": true,
    "reason": "string",
    "elapse": "string",
    "experimentMode": false,
    "server": {"version":"v1.2.3"},
    "shells": [{"ShellDefinition"}]
}
```

- `ShellDefinition`

```json
{
    "id": "shell definition id (uuid)",
    "type": "type",
    "icon": "icon name",
    "label": "display name",
    "theme": "theme name",
    "command": "terminal shell command",
    "attributes": [
        { "removable": true },
        { "cloneable": true },
        { "editable": true }
    ]
}
```

- 유형

| 유형 | 설명               |
|:-----| :------------------|
| sql  | SQL 편집기          |
| tql  | TQL 편집기          |
| wrk  | 워크스페이스 편집기 |
| taz  | 태그 분석기         |
| term | 터미널              |

## 데이터베이스

### SQL 실행

**GET, POST `/web/machbase`**

`/db/query` API와 동일하게 동작하며, 인증 방식만 다릅니다.
`/db/query`는 클라이언트 애플리케이션을 API 토큰으로 인증하는 반면,
`/web/machbase`는 사용자 상호작용을 위해 JWT를 검증합니다.

### 테이블 목록 조회

**GET `/web/api/tables?showall=false&name=pattern`**

테이블 목록을 반환합니다.

- `showall`을 `true`로 설정하면 숨김 테이블까지 모두 포함합니다.
- `name`은 테이블 이름을 필터링하는 패턴입니다. `?` 또는 `*`가 포함된 glob 표현식이나, `?`와 `*`가 없는 접두어를 사용할 수 있습니다.

```json
{
    "success": true,
    "reason": "success or other message",
    "elapse": "elapse time in string format",
    "data": {
        "columns": ["ROWNUM", "DB", "USER", "NAME", "TYPE"],
        "types": ["int32", "string", "string", "string", "string"],
        "rows":[
            [1, "MACHBASE", "SYS", "TABLENAME", "TAG TABLE"],
        ]
    }
}
```

### 태그 목록 조회

**GET `/web/api/tables/:table/tags?name=prefix`**

해당 테이블의 태그 목록을 반환합니다.

- `name`을 지정하면 해당 접두어로 시작하는 태그만 반환합니다.

```json
{
    "success": true,
    "reason": "success or other message",
    "elapse": "elapse time in string format",
    "data": {
        "columns": ["ROWNUM", "NAME"],
        "types": ["int32", "string"],
        "rows":[
            [1, "temperature"],
        ]
    }
}
```

### 태그 통계

**GET `/web/api/tables/:table/tags/:tag/stat`**

지정한 테이블의 태그 통계를 반환합니다.

```json
{
    "success": true,
    "reason": "success or other message",
    "elapse": "elapse time in string format",
    "data": {
        "columns": ["ROWNUM", "NAME", "ROW_COUNT", "MIN_TIME", "MAX_TIME",
            "MIN_VALUE", "MIN_VALUE_TIME", "MAX_VALUE", "MAX_VALUE_TIME", "RECENT_ROW_TIME"],
        "types": ["int32", "string", "int64", "datetime", "datetime",
            "double", "datetime", "double", "datetime", "datetime"],
        "rows":[
            ["...omit...."],
        ]
    }
}
```

## 셸 및 터미널

셸 정의는 JSON-RPC [`shell.*`](#shelllist) 메서드로 조회, 추가, 복제, 수정, 삭제합니다.

### 데이터 채널

**`ws://{server_address}/web/api/term/:term_id/data`**

터미널용 WebSocket입니다.

### 창 크기

**POST `/web/api/term/:term_id/windowsize`**

터미널 크기를 변경합니다.

`TerminalSize`

```json
{ "rows": 24, "cols": 80 }
```

## 서버 이벤트

### 이벤트 채널

**`ws://127.0.0.1:5654/web/api/console/{console_id}/data?token={jwt_token}`**

양방향 메시지를 위한 WebSocket입니다.

- 메시지 유형

```json
{
    "type": "type(see below)",
    "ping": {
        "tick": 1234
    },
    "log": {
        "level": "INFO",
        "message": "log message"
    }
}
```

| 유형           |  필드            | 설명                                                           |
|:---------------| :----------------| :-------------------------------------------------------------|
| `ping`         |                  | 핑 메시지                                                      |
|                | `ping.tick`      | 임의의 정수. 서버는 클라이언트가 보낸 숫자를 그대로 응답합니다. |
| `log`          | `log.level`      | 로그 레벨 `TRACE`, `DEBUG`, `INFO`, `WARN`, `ERROR`           |
|                | `log.message`    | 로그 메시지                                                    |
|                | `log.repeat`     | 같은 메시지가 연속으로 두 번 이상 반복될 때의 반복 횟수        |

## TQL 및 워크스페이스

**TQL 콘텐츠 유형**

| 헤더 <br/>`Content-Type`   | 헤더 <br/>`X-Chart-Type`   |          내용                             |
|:--------------------------:| :-------------------------:| :---------------------------------------- |
| text/html                  | "echart", "geomap"         | 전체 HTML <br/>예: `<iframe>` 안에 포함 |
| text/html                  | -                          | 전체 HTML <br/>예: `<iframe>` 안에 포함 |
| text/csv                   | -                          | CSV                                       |
| text/markdown              | -                          | 마크다운                                  |
| application/json           | "echart", "geomap"         | JSON(echart 또는 geomap 데이터)           |
| application/json           | -                          | JSON                                      |
| application/xhtml+xml      | -                          | HTML 요소, 예: `<div>...</div>`           |

### TQL 파일 실행

**GET `/web/api/tql/*path`**

지정한 경로의 TQL을 실행합니다. 응답 형식은 위의 'TQL 콘텐츠 유형' 표를 참고합니다.

**POST `/web/api/tql/*path`**

지정한 경로의 TQL을 실행합니다. 응답 형식은 위의 'TQL 콘텐츠 유형' 표를 참고합니다.

### TQL 스크립트 실행

**POST `/web/api/tql`**

본문에 TQL 스크립트를 담아 전송하면 서버가 실행 결과를 반환합니다.
응답 형식은 'TQL 콘텐츠 유형' 표를 참고합니다.

요청에 `$`라는 쿼리 매개변수가 있으면 그 값을 TQL 스크립트로 간주하고,
본문은 데이터로 처리합니다. `$` 매개변수는 v8.0.17부터 사용할 수 있습니다.

### 마크다운 렌더링

마크다운 렌더링은 JSON-RPC [`markdown.render`](#markdownrender) 메서드를 사용합니다.

## 파일 관리

### Content-Type

파일 유형과 Content-Type의 대응 관계입니다.

| 파일 유형 | Content-Type             |
|:----------|:-------------------------|
| .sql      | text/plain               |
| .tql      | text/plain               |
| .taz      | application/json         |
| .wrk      | application/json         |
| unknown   | application/octet-stream |

### 파일 읽기

**GET `/web/api/files/*path`**

경로가 파일을 가리키면 파일 내용을 반환합니다.

경로가 디렉터리를 가리키면 디렉터리 항목 목록을 반환합니다.

- `Entry`

```json
{
    "isDir": true,
    "name": "name",
    "content": "bytes array, if the entry is a file",
    "children": [{"SubEntry, if the entry is a directory"}],
}
```

- `SubEntry`

```json
{
    "isDir": true,
    "name": "name",
    "type": "type",
    "size": 1234,
    "lastModifiedUnixMillis": 169384757
}
```

### 파일 쓰기

**POST `/web/api/files/*path`**

- `path`가 파일을 가리키면 본문 내용을 해당 파일에 기록합니다.

- `path`가 디렉터리이고 본문이 비어 있으면 빈 디렉터리를 생성하고 생성된 디렉터리의 `Entry`를 반환합니다.

- `path`가 디렉터리이고 본문이 `GitCloneReq` JSON이면 원격 Git 저장소를 해당 경로로 복제하고 디렉터리의 `Entry`를 반환합니다.

`GitCloneReq`

```json
{
    "command": "clone",
    "url": "https://github.com/machbase/neo-samples.git"
}
```

- `command` : `clone`, `pull`

### 파일 이름 변경/이동

**PUT `/web/api/files/*path`**

파일(또는 디렉터리)의 이름을 바꾸거나 이동합니다.

`RenameReq`

```json
{
    "destination": "target path",
}
```

작업이 성공적으로 완료되면 API는 `200 OK` 상태 코드를 반환합니다.

### 파일 삭제

**DELETE `/web/api/files/*path`**

`path` 위치의 파일을 삭제합니다. 경로가 디렉터리를 가리키고 비어 있지 않으면 오류를 반환합니다.

## 키 관리

키는 JSON-RPC [`key.*`](#keylist) 메서드로, API 토큰은 [`token.*`](#tokenlist) 메서드로 관리합니다.

## SSH 키

SSH 키는 JSON-RPC [`sshkey.*`](#sshkeylist) 메서드로 관리합니다.

## 타이머

타이머는 JSON-RPC [`timer.*`](#timerlist) 메서드로 관리합니다.

## 브리지

브리지 관리와 명령 실행에는 JSON-RPC [`bridge.*`](#bridgelist) 메서드를 사용합니다.

## 구독자

구독자는 JSON-RPC [`subscriber.*`](#subscriberlist) 메서드로 관리합니다.

## 백업

### 백업 조회

**GET `/web/api/backup/archives`**

백업 목록을 반환합니다.

- 기본 백업 디렉터리는 machbase-neo 실행 파일이 있는 디렉터리 아래의 `backups`입니다.
- 저장 위치를 바꾸려면 machbase-neo를 `--backup-dir={path}` 옵션으로 실행합니다. 기본값을 사용할 때는 이 옵션이 필요하지 않습니다.

`response`

```json
{
    "data": [
        {
            "path": "example_backup1",
            "isMount": true,
            "mountName": "backup1"
        },
        {
            "path": "example_backup2",
            "isMount": false
        }
    ],
    "elapse": "6.562299ms",
    "reason": "success",
    "success": true
}
```
### DB 백업

**POST `/web/api/backup/archive`**

데이터베이스를 백업합니다.<br/>

- **전체 백업**: 전체 데이터를 백업합니다.
- **증분 백업**: 전체 백업 또는 이전 증분 백업 이후 추가된 데이터만 백업합니다.
- **기간 백업**: 특정 기간의 데이터를 백업합니다.

`request`

{{< tabs >}}
{{< tab name="Full Backup" >}}
```json
{
    "type":"database", // database or table
    "tableName":"",
    "duration":{
        "type":"full",
        "after":"",
        "from":"",
        "to":""
    },
    "path":"example_backup1"
    // "path":"/home/neo/backups/example_backup1" // Absolute Path
}
```
{{< /tab >}}
{{< tab name="Incremental Backup" >}}
```json
{
    "type":"database", // database or table
    "tableName":"",
    "duration":{
        "type":"incremental",
        "after":"{previous_backup_dir}",
        "from":"",
        "to":""
    },
    "path":"example_backup1"
    // "path":"/home/neo/backups/example_backup1" // Absolute Path
}
```
{{< /tab >}}
{{< tab name="Time Backup" >}}
```json
{
    "type":"database", // database or table
    "tableName":"",
    "duration":{
        "type":"time",
        "after":"",
        "from":"2024-08-01 00:00:00",
        "to":"2024-08-02 23:59:59"
    },
    "path":"example_backup1"
    // "path":"/home/neo/backups/example_backup1" // Absolute Path
}
```
{{< /tab >}}
{{< tab name="Table Backup" >}}
```json
{
    "type":"table", // database or table
    "tableName":"example",
    "duration":{
        "type":"full",
        "after":"",
        "from":"",
        "to":""
    },
    "path":"example_backup1"
    // "path":"/home/neo/backups/example_backup1" // Absolute Path
}
```
{{< /tab >}}
{{< /tabs >}}

`response`

```json
{
    "success": true,
    "reason": "success",
    "elapse": "231.3µs"
}
```

### 백업 상태

**GET `/web/api/backup/archive/status`**

백업 상태를 반환합니다.<br/>

`response`

```json
{
    "data": {
        "type": "database",
        "tableName": "",
        "duration": {
            "type": "full",
            "after": "",
            "from": "",
            "to": ""
        },
        "path": "/home/neo/neo-server/tmp/machbase_home/dbs/example_backup1",
    },
    "elapse": "1.1µs",
    "reason": "success",
    "success": true
}
```

## 마운트

### 마운트 목록

**GET `/web/api/backup/mounts`**

마운트 목록을 반환합니다.

`response`

```json
{
    "data": [
        {
            "name": "machbase_backup_19700101090000_20240726104832_15",
            "path": "backup1",
            "tbsid": 23,
            "scn": 15,
            "mountdb": "MOUNT_BACKUP1",
            "dbBeginTime": "1970-01-01 09:00:00",
            "dbEndTime": "2024-07-26 10:48:32",
            "backupBeginTime": "2024-07-26 10:48:32",
            "backupEndTime": "2024-07-26 10:48:34",
            "flag": 0
        }
    ],
    "elapse": "424.3µs",
    "reason": "success",
    "success": true
}
```
### DB 마운트

**POST `/web/api/backup/mounts/:name`**

데이터베이스를 마운트합니다.

- `:name`: 마운트 이름
- `path`: 백업 데이터베이스 경로(절대 경로 또는 상대 경로 모두 사용 가능)

{{< tabs >}}
{{< tab name="Request" >}}
```json
{
    "path":"example_backup1" // Relative Path
    // "path":"/home/machbase/machbase_home/dbs/example_backup1" // Absolute Path
}
```
{{< /tab >}}
{{< tab name="Response" >}}
```json
{
    "elapse": "46.8694ms",
    "reason": "success",
    "success": true
}
```
{{< /tab >}}
{{< /tabs >}}

### DB 언마운트

**DELETE `/web/api/backup/mounts/:name`**

데이터베이스를 언마운트합니다.

- `:name`: 언마운트할 이름

`response`

```json
{
    "elapse": "46.8694ms",
    "reason": "success",
    "success": true
}
```


## 패키지

패키지는 JSH [`pkg` 명령](/neo/jsh/packages/)으로 설치하고 제거합니다.

## 기타

### 참고 자료

**GET `/web/api/refs/*path`**

- `ReferenceGroup`

```json
{
    "label": "group name",
    "items":[{"ReferenceItem"}]
}
```

- `ReferenceItem`

```json
{
    "type": "type",
    "title": "display title",
    "address": "url address",
    "target": "browser link target"
}
```

- type: `url`, `wrk`, `tql`, `sql`
- address: `serverfile://<path>` 접두어가 있으면 서버 쪽 파일을 가리키고,
  그렇지 않으면 `https://`로 시작하는 외부 웹 URL입니다.

### SQL 구문 분할기

SQL 구문 분할에는 JSON-RPC [`sql.split`](#sqlsplit) 메서드를 사용합니다.

### 라이선스 정보

**GET `/web/api/license`**

```json
{
    "success": true,
    "reason": "success or error reason",
    "elapse": "elapse time",
    "data": {
        "id": "license id",
        "type": "type",
        "customer": "customer",
        "project": "project",
        "countryCode": "country code",
        "installDate": "installation date",
        "issueDate": "license issue date"
    }
}
```

### 라이선스 설치

**POST `/web/api/license`**

라이선스 파일을 설치합니다.

## WebSocket

```
ws://127.0.0.1:5654/web/api/console/{console_id}/data?token={jwt_token}
```

`console_id`는 세션을 올바르게 관리하기 위해 클라이언트 애플리케이션이 생성한 고유 식별자여야 합니다.

이 엔드포인트는 HTTP `Authorization` 헤더 대신 쿼리 매개변수(`token={jwt_token}`)로 JWT 토큰을 전달해야 합니다.

이 엔드포인트에서는 서버와 클라이언트가 JSON 객체를 교환하여 구조화되고 안전한 방식으로 통신합니다.

### PING

클라이언트는 현재 시간을 UNIX 에포크 형식으로 포함한 *PING* 메시지를 보낼 수 있습니다.
서버는 동일한 페이로드로 응답하므로 왕복 지연 시간을 정확하게 측정할 수 있습니다.
이 메커니즘은 연결을 유지하고 유휴 타임아웃을 방지하는 데도 도움이 됩니다.

- 방향: C -> S

```json
{
    "type": "ping",
    "ping": {
        "tick": 1759127437000
    }
}
```

### LOG

서버는 사용자가 이해하기 쉬운 메시지를 보내 상태 변경이나 오류를 알립니다.
이 메시지는 상태, 문제, 조치 방법을 명확하게 전달하여 원활한 상호작용과 문제 해결을 돕습니다.

- 방향: S -> C

```json
{
    "type": "log",
    "log": {
        "timestamp": 1759127437000000000,
        "level": "INFO",
        "task": "task-name",
        "message": "Fail to convert from string to number",
        "repeat": 10
    }
}
```

- **timestamp**: 로그 발생 시각으로, 나노초 단위 UNIX 에포크입니다.
- **level**: 로그 심각도. `"TRACE"`, `"DEBUG"`, `"INFO"`, `"WARN"`, `"ERROR"` 중 하나입니다.
- **task** (선택): 관련 작업의 이름.
- **message**: 설명 메시지.
- **repeat** (선택): 동일한 로그 메시지가 연속으로 반복된 횟수로, 중복 출력을 줄이는 데 활용됩니다.

## JSON-RPC

이 절에서는 JSON-RPC 사양을 따르는 WebSocket 기반 원격 프로시저 호출(RPC) 메커니즘을 설명합니다.
RPC를 사용하면 클라이언트가 서버 측 메서드를 호출하고 구조화된 응답을 받을 수 있어,
클라이언트 애플리케이션과 서버 간 통신 및 통합이 원활해집니다.

Web UI는 관리 기능을 위해 JSON-RPC endpoint를 제공합니다.

- HTTP POST endpoint: `/web/api/rpc`
- WebSocket endpoint: `/web/api/console/:console_id/data?token={jwt_token}`

단순 요청/응답 형태의 호출에는 `/web/api/rpc`를 사용하는 것을 권장합니다.
콘솔 세션과 함께 양방향 메시지를 처리해야 하는 경우에는 `/web/api/console/:console_id/data?token={jwt_token}`를 사용할 수 있습니다.

### HTTP JSON-RPC 요청 형식

**POST `/web/api/rpc`**

요청 예시:

```json
{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "shell.list",
    "params": []
}
```

성공 응답 예시:

```json
{
    "jsonrpc": "2.0",
    "id": 1,
    "result": []
}
```

오류 응답 예시:

```json
{
    "jsonrpc": "2.0",
    "id": 1,
    "error": {
        "code": -32000,
        "message": "error message"
    }
}
```

참고:

- 응답의 HTTP status는 일반적으로 `200 OK`입니다.
- 성공 여부는 HTTP status가 아니라 `error` 필드가 있는지로 판단합니다.

### WebSocket JSON-RPC 요청 형식

**`ws://{server_address}/web/api/console/:console_id/data?token={jwt_token}`**

WebSocket에서는 `rpc_req` / `rpc_rsp` 이벤트를 사용합니다.
`session` 필드는 UI 클라이언트가 응답을 어느 탭 또는 어느 뷰에 연결할지 구분하기 위한 식별자입니다.

**요청**

- 방향: C -> S

```json
{
    "type": "rpc_req",
    "session": "{\"view\":\"shell-tab-2\",\"requestId\":\"req-001\"}",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 1234,
        "method": "add",
        "params": [1, 2]
    }
}
```

**응답**

- 방향: S -> C

**성공**

```json
{
    "type": "rpc_rsp",
    "session": "{\"view\":\"shell-tab-2\",\"requestId\":\"req-001\"}",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 1234,
        "result": 3
    }
}
```

**오류**

```json
{
    "type": "rpc_rsp",
    "session": "{\"view\":\"shell-tab-2\",\"requestId\":\"req-001\"}",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 1234,
        "error": {
            "code": -32000,
            "message": "some error message"
        }
    }
}
```

### Markdown

#### markdown.render

`markdown.render(markdown, darkMode, referer)`

*매개변수*
- `markdown` *string*
- `darkMode` *bool*
- `referer` *string* - 참조 URL

*반환값*

- `string|error`

<details>
<summary>요청/응답 JSON</summary>

*요청*

```json
{
    "type": "rpc_req",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "method": "markdown.render",
        "params": [
            "string",
            false,
            "string"
        ]
    }
}
```

*응답*

```json
{
    "type": "rpc_rsp",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "result": "string"
    }
}
```

</details>

### Vizspec

#### vizspec.render

`vizspec.render(vizspec)`

*매개변수*
- `vizspec` *object*

*반환값*

- `object|error`

<details>
<summary>요청/응답 JSON</summary>

*요청*

```json
{
    "type": "rpc_req",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "method": "vizspec.render",
        "params": [
            {}
        ]
    }
}
```

*응답*

```json
{
    "type": "rpc_rsp",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "result": {}
    }
}
```

</details>

#### vizspec.export

`vizspec.export(vizspec, format)`

*매개변수*
- `vizspec` *object*
- `format` *string*

*반환값*

- `object|error`

<details>
<summary>요청/응답 JSON</summary>

*요청*

```json
{
    "type": "rpc_req",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "method": "vizspec.export",
        "params": [
            {},
            "string"
        ]
    }
}
```

*응답*

```json
{
    "type": "rpc_rsp",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "result": {}
    }
}
```

</details>

### Server

#### server.info.get

`server.info.get()`

*매개변수*

- 없음

*반환값*

- `object<ServerInfoResponse>|error`

<details>
<summary>요청/응답 JSON</summary>

*요청*

```json
{
    "type": "rpc_req",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "method": "server.info.get",
        "params": []
    }
}
```

*응답*

```json
{
    "type": "rpc_rsp",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "result": {}
    }
}
```

</details>

#### server.info.statz

`server.info.statz(names)`

*매개변수*
- `names` *array<string>* - 메트릭 이름

*반환값*

- `object<ServerStatzResponse>|error` - 이름별로 묶은 시각화 사양

<details>
<summary>요청/응답 JSON</summary>

*요청*

```json
{
    "type": "rpc_req",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "method": "server.info.statz",
        "params": [
            []
        ]
    }
}
```

*응답*

```json
{
    "type": "rpc_rsp",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "result": {}
    }
}
```

</details>

#### server.info.query

`server.info.query(maxRows, pattern)`

*매개변수*
- `maxRows` *int* - 최대 행 수
- `pattern` *array<string>* - 메트릭 키에 대한 와일드카드 필터

*반환값*

- `object<StatzQueryResult>|error` - 표 형식의 메트릭 조회 결과

<details>
<summary>요청/응답 JSON</summary>

*요청*

```json
{
    "type": "rpc_req",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "method": "server.info.query",
        "params": [
            0,
            []
        ]
    }
}
```

*응답*

```json
{
    "type": "rpc_rsp",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "result": {}
    }
}
```

</details>

#### server.info.keys

`server.info.keys(pattern)`

*매개변수*
- `pattern` *array<string>* - 메트릭 키에 대한 와일드카드 필터

*반환값*

- `array<string>|error` - 정렬된 메트릭 키 이름

<details>
<summary>요청/응답 JSON</summary>

*요청*

```json
{
    "type": "rpc_req",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "method": "server.info.keys",
        "params": [
            []
        ]
    }
}
```

*응답*

```json
{
    "type": "rpc_rsp",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "result": []
    }
}
```

</details>

#### server.certificate.get

`server.certificate.get()`

*매개변수*

- 없음

*반환값*

- `string|error`

<details>
<summary>요청/응답 JSON</summary>

*요청*

```json
{
    "type": "rpc_req",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "method": "server.certificate.get",
        "params": []
    }
}
```

*응답*

```json
{
    "type": "rpc_rsp",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "result": "string"
    }
}
```

</details>

#### server.shutdown

관리(mgmt) 서버에서 구현합니다.

`server.shutdown()`

*매개변수*

- 없음

*반환값*

- `object<ShutdownResponse>|error`

<details>
<summary>요청/응답 JSON</summary>

*요청*

```json
{
    "type": "rpc_req",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "method": "server.shutdown",
        "params": []
    }
}
```

*응답*

```json
{
    "type": "rpc_rsp",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "result": {}
    }
}
```

</details>

### Service

#### service.port.list

`service.port.list(svc)`

*매개변수*
- `svc` *string*

*반환값*

- `array<object<model.ServicePort>>|error`

<details>
<summary>요청/응답 JSON</summary>

*요청*

```json
{
    "type": "rpc_req",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "method": "service.port.list",
        "params": [
            "string"
        ]
    }
}
```

*응답*

```json
{
    "type": "rpc_rsp",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "result": []
    }
}
```

</details>

### Proxy

#### proxy.register

`proxy.register(req)`

*매개변수*
- `req` *object<ProxyRegisterRequest>*

*반환값*

- `object<ProxyEntrySnapshot>|error`

<details>
<summary>요청/응답 JSON</summary>

*요청*

```json
{
    "type": "rpc_req",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "method": "proxy.register",
        "params": [
            {}
        ]
    }
}
```

*응답*

```json
{
    "type": "rpc_rsp",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "result": {}
    }
}
```

</details>

#### proxy.unregister

`proxy.unregister(req)`

*매개변수*
- `req` *object<ProxyUnregisterRequest>*

*반환값*

- `array<object<ProxyEntrySnapshot>>|error`

<details>
<summary>요청/응답 JSON</summary>

*요청*

```json
{
    "type": "rpc_req",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "method": "proxy.unregister",
        "params": [
            {}
        ]
    }
}
```

*응답*

```json
{
    "type": "rpc_rsp",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "result": []
    }
}
```

</details>

#### proxy.list

`proxy.list(service)`

*매개변수*
- `service` *string*

*반환값*

- `array<object<ProxyEntrySnapshot>>|error`

<details>
<summary>요청/응답 JSON</summary>

*요청*

```json
{
    "type": "rpc_req",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "method": "proxy.list",
        "params": [
            "string"
        ]
    }
}
```

*응답*

```json
{
    "type": "rpc_rsp",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "result": []
    }
}
```

</details>

#### proxy.get

`proxy.get(req)`

*매개변수*
- `req` *object<ProxyGetRequest>*

*반환값*

- `object<ProxyEntrySnapshot>|error`

<details>
<summary>요청/응답 JSON</summary>

*요청*

```json
{
    "type": "rpc_req",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "method": "proxy.get",
        "params": [
            {}
        ]
    }
}
```

*응답*

```json
{
    "type": "rpc_rsp",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "result": {}
    }
}
```

</details>

### Shell

#### shell.list

`shell.list()`

*매개변수*

- 없음

*반환값*

- `array<object<model.ShellDefinition>>|error`

<details>
<summary>요청/응답 JSON</summary>

*요청*

```json
{
    "type": "rpc_req",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "method": "shell.list",
        "params": []
    }
}
```

*응답*

```json
{
    "type": "rpc_rsp",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "result": []
    }
}
```

</details>

#### shell.add

`shell.add(name, command)`

*매개변수*
- `name` *string*
- `command` *string*

*반환값*

- `string|error`

<details>
<summary>요청/응답 JSON</summary>

*요청*

```json
{
    "type": "rpc_req",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "method": "shell.add",
        "params": [
            "string",
            "string"
        ]
    }
}
```

*응답*

```json
{
    "type": "rpc_rsp",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "result": "string"
    }
}
```

</details>

#### shell.copy

지정한 셸 정의를 복제하고, 새 ID가 부여된 셸 정의를 반환합니다.

`shell.copy(srcId)`

*매개변수*
- `srcId` *string* - 복제할 셸 정의의 ID

*반환값*

- `object<model.ShellDefinition>|error` - 복제된 셸 정의

<details>
<summary>요청/응답 JSON</summary>

*요청*

```json
{
    "type": "rpc_req",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "method": "shell.copy",
        "params": [
            "23"
        ]
    }
}
```

*응답*

```json
{
    "type": "rpc_rsp",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "result": {
            "id": "24",
            "type": "term",
            "icon": "console-network-outline",
            "label": "CUSTOM SHELL",
            "command": "/bin/sh",
            "attributes": [
                {
                    "removable": true
                },
                {
                    "cloneable": true
                },
                {
                    "editable": true
                }
            ]
        }
    }
}
```

</details>

#### shell.update

셸 정의를 수정합니다. `id`로 대상을 지정하고 셸 정의 전체를 전달합니다.

`shell.update(shell)`

*매개변수*
- `shell` *object<model.ShellDefinition>* - `id`, `type`, `label`, `command`, `icon`, `theme`, `attributes`를 담은 셸 정의
    `command`가 비어 있으면 오류를 반환합니다.

*반환값*

- `object<model.ShellDefinition>|error` - 수정된 셸 정의

<details>
<summary>요청/응답 JSON</summary>

*요청*

```json
{
    "type": "rpc_req",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "method": "shell.update",
        "params": [
            {
                "id": "24",
                "type": "term",
                "icon": "console-network-outline",
                "label": "_docgen_uiapi_s2",
                "command": "/bin/bash",
                "attributes": [
                    {
                        "removable": true
                    },
                    {
                        "cloneable": true
                    },
                    {
                        "editable": true
                    }
                ],
                "theme": "dark"
            }
        ]
    }
}
```

*응답*

```json
{
    "type": "rpc_rsp",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "result": {
            "id": "24",
            "type": "term",
            "icon": "console-network-outline",
            "label": "_docgen_uiapi_s2",
            "theme": "dark",
            "command": "/bin/bash",
            "attributes": [
                {
                    "removable": true
                },
                {
                    "cloneable": true
                },
                {
                    "editable": true
                }
            ]
        }
    }
}
```

</details>

#### shell.delete

`shell.delete(id)`

*매개변수*
- `id` *string*

*반환값*

- `null|error`

<details>
<summary>요청/응답 JSON</summary>

*요청*

```json
{
    "type": "rpc_req",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "method": "shell.delete",
        "params": [
            "string"
        ]
    }
}
```

*응답*

```json
{
    "type": "rpc_rsp",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "result": null
    }
}
```

</details>

### Bridge

#### bridge.list

`bridge.list()`

*매개변수*

- 없음

*반환값*

- `array<object<bridge.BridgeInfo>>|error`

<details>
<summary>요청/응답 JSON</summary>

*요청*

```json
{
    "type": "rpc_req",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "method": "bridge.list",
        "params": []
    }
}
```

*응답*

```json
{
    "type": "rpc_rsp",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "result": []
    }
}
```

</details>

#### bridge.get

`bridge.get(name)`

*매개변수*
- `name` *string*

*반환값*

- `object<bridge.BridgeInfo>|error`

<details>
<summary>요청/응답 JSON</summary>

*요청*

```json
{
    "type": "rpc_req",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "method": "bridge.get",
        "params": [
            "string"
        ]
    }
}
```

*응답*

```json
{
    "type": "rpc_rsp",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "result": {}
    }
}
```

</details>

#### bridge.add

`bridge.add(name, typ, conn)`

*매개변수*
- `name` *string*
- `typ` *string*
- `conn` *string*

*반환값*

- `null|error`

<details>
<summary>요청/응답 JSON</summary>

*요청*

```json
{
    "type": "rpc_req",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "method": "bridge.add",
        "params": [
            "string",
            "string",
            "string"
        ]
    }
}
```

*응답*

```json
{
    "type": "rpc_rsp",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "result": null
    }
}
```

</details>

#### bridge.delete

`bridge.delete(name)`

*매개변수*
- `name` *string*

*반환값*

- `null|error`

<details>
<summary>요청/응답 JSON</summary>

*요청*

```json
{
    "type": "rpc_req",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "method": "bridge.delete",
        "params": [
            "string"
        ]
    }
}
```

*응답*

```json
{
    "type": "rpc_rsp",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "result": null
    }
}
```

</details>

#### bridge.test

`bridge.test(name)`

*매개변수*
- `name` *string*

*반환값*

- `bool|error`

<details>
<summary>요청/응답 JSON</summary>

*요청*

```json
{
    "type": "rpc_req",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "method": "bridge.test",
        "params": [
            "string"
        ]
    }
}
```

*응답*

```json
{
    "type": "rpc_rsp",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "result": false
    }
}
```

</details>

#### bridge.stats

`bridge.stats(name)`

*매개변수*
- `name` *string*

*반환값*

- `object<BridgeStats>|error`

<details>
<summary>요청/응답 JSON</summary>

*요청*

```json
{
    "type": "rpc_req",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "method": "bridge.stats",
        "params": [
            "string"
        ]
    }
}
```

*응답*

```json
{
    "type": "rpc_rsp",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "result": {}
    }
}
```

</details>

#### bridge.exec

`bridge.exec(name, command)`

*매개변수*
- `name` *string*
- `command` *string*

*반환값*

- `object<BridgeExecResult>|error`

<details>
<summary>요청/응답 JSON</summary>

*요청*

```json
{
    "type": "rpc_req",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "method": "bridge.exec",
        "params": [
            "string",
            "string"
        ]
    }
}
```

*응답*

```json
{
    "type": "rpc_rsp",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "result": {}
    }
}
```

</details>

#### bridge.query

`bridge.query(name, query)`

*매개변수*
- `name` *string*
- `query` *string*

*반환값*

- `object<BridgeQueryResult>|error`

<details>
<summary>요청/응답 JSON</summary>

*요청*

```json
{
    "type": "rpc_req",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "method": "bridge.query",
        "params": [
            "string",
            "string"
        ]
    }
}
```

*응답*

```json
{
    "type": "rpc_rsp",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "result": {}
    }
}
```

</details>

#### bridge.result.fetch

`bridge.result.fetch(handle)`

*매개변수*
- `handle` *string*

*반환값*

- `object<BridgeQueryRow>|error`

<details>
<summary>요청/응답 JSON</summary>

*요청*

```json
{
    "type": "rpc_req",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "method": "bridge.result.fetch",
        "params": [
            "string"
        ]
    }
}
```

*응답*

```json
{
    "type": "rpc_rsp",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "result": {}
    }
}
```

</details>

#### bridge.result.close

`bridge.result.close(handle)`

*매개변수*
- `handle` *string*

*반환값*

- `null|error`

<details>
<summary>요청/응답 JSON</summary>

*요청*

```json
{
    "type": "rpc_req",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "method": "bridge.result.close",
        "params": [
            "string"
        ]
    }
}
```

*응답*

```json
{
    "type": "rpc_rsp",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "result": null
    }
}
```

</details>

### Sshkey

#### sshkey.list

`sshkey.list()`

*매개변수*

- 없음

*반환값*

- `array<object<AuthorizedSshKey>>|error`

<details>
<summary>요청/응답 JSON</summary>

*요청*

```json
{
    "type": "rpc_req",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "method": "sshkey.list",
        "params": []
    }
}
```

*응답*

```json
{
    "type": "rpc_rsp",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "result": []
    }
}
```

</details>

#### sshkey.add

`sshkey.add(keyType, key, comment)`

*매개변수*
- `keyType` *string*
- `key` *string*
- `comment` *string*

*반환값*

- `null|error`

<details>
<summary>요청/응답 JSON</summary>

*요청*

```json
{
    "type": "rpc_req",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "method": "sshkey.add",
        "params": [
            "string",
            "string",
            "string"
        ]
    }
}
```

*응답*

```json
{
    "type": "rpc_rsp",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "result": null
    }
}
```

</details>

#### sshkey.delete

`sshkey.delete(key)`

*매개변수*
- `key` *string*

*반환값*

- `null|error`

<details>
<summary>요청/응답 JSON</summary>

*요청*

```json
{
    "type": "rpc_req",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "method": "sshkey.delete",
        "params": [
            "string"
        ]
    }
}
```

*응답*

```json
{
    "type": "rpc_rsp",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "result": null
    }
}
```

</details>

### Key

#### key.list

`key.list()`

*매개변수*

- 없음

*반환값*

- `array<object<KeyInfo>>|error` - 서버 키 저장소에 저장된 키 목록
    - `idx`: 목록 안의 순번
    - `id`: 키 ID. `key.delete`에 지정합니다.
    - `name`: 키 이름
    - `notBefore`, `notAfter`: 유효 기간의 시작 시각과 종료 시각(Unix 타임스탬프, 초)

<details>
<summary>요청/응답 JSON</summary>

*요청*

```json
{
    "type": "rpc_req",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "method": "key.list",
        "params": []
    }
}
```

*응답*

```json
{
    "type": "rpc_rsp",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "result": [
            {
                "idx": 0,
                "id": 8,
                "name": "_docgen_uiapi_key",
                "notBefore": 1789632914,
                "notAfter": 2104992914
            }
        ]
    }
}
```

</details>

#### key.generate

`key.generate(name, typ, notBefore, notAfter, store)`

*매개변수*
- `name` *string* - 키 이름. 소문자로 바뀌어 저장됩니다.
- `typ` *string* - 생성할 키의 유형. `RSA` 또는 `ECDSA`여야 합니다.
- `notBefore` *int64* - 키 유효 기간의 시작 시각(Unix 타임스탬프, 초)
    지정하지 않거나 0이면 현재 시각을 사용합니다.
- `notAfter` *int64* - 키 유효 기간의 종료 시각(Unix 타임스탬프, 초)
    지정하지 않거나 0이면 기본 기간인 10년을 사용합니다.
- `store` *bool* - 키 쌍을 서버의 키 저장소에 저장할지 여부
    `false`이면 저장하지 않으므로 `key.list`에도 나타나지 않습니다.

*반환값*

- `any|error` - 생성된 키 정보
    - `id`: 키 ID. `store`가 false이면 `0`입니다.
    - `name`: 키 이름
    - `certificate`: 키 쌍의 인증서
    - `key`: 키 쌍의 개인 키
    - `serverKey`: 서버 인증서(`store`가 true인 경우)
    - `zip`: 키 쌍과 서버 인증서를 담은 ZIP 아카이브를 base64로 인코딩한 문자열(`store`가 true인 경우)

<details>
<summary>요청/응답 JSON</summary>

*요청*

```json
{
    "type": "rpc_req",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "method": "key.generate",
        "params": [
            "_docgen_uiapi_key",
            "ecdsa",
            0,
            0,
            true
        ]
    }
}
```

*응답*

```json
{
    "type": "rpc_rsp",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "result": {
            "certificate": "-----BEGIN CERTIFICATE-----\nXXXXXXXXXXXXXXXXXX\n-----END CERTIFICATE-----\n",
            "id": 8,
            "key": "-----BEGIN EC PRIVATE KEY-----\nXXXXXXXXXXXXXXXX\n-----END EC PRIVATE KEY-----\n",
            "name": "_docgen_uiapi_key",
            "serverKey": "-----BEGIN CERTIFICATE-----\nXXXXXXXXXXXXXXXXXX\n-----END CERTIFICATE-----\n",
            "zip": "UEsDBXXXXXXXXXXXXXXXX"
        }
    }
}
```

</details>

#### key.delete

`key.delete(id)`

*매개변수*
- `id` *int64* - `key.list`나 `key.generate`가 반환한 키 ID

*반환값*

- `null|error`

<details>
<summary>요청/응답 JSON</summary>

*요청*

```json
{
    "type": "rpc_req",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "method": "key.delete",
        "params": [
            8
        ]
    }
}
```

*응답*

```json
{
    "type": "rpc_rsp",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "result": null
    }
}
```

</details>

### Token

발급한 토큰의 사용법은 [API 보안](/neo/security/)을 참고합니다.

#### token.list

`token.list()`

*매개변수*

- 없음

*반환값*

- `array<object<ApiTokenInfo>>|error` - 호출한 사용자의 API 토큰 목록
    - `id`: 토큰 ID. `token.delete`에 지정합니다.
    - `name`: 토큰 이름
    - `user`: 토큰을 소유한 사용자
    - `hint`: 일부를 가린 토큰 값
    - `createdAt`: 발급 시각(Unix 타임스탬프, 초)
    - `notAfter`: 만료 시각(Unix 타임스탬프, 초)
    - `lastUsedAt`: 마지막으로 사용한 시각(Unix 타임스탬프, 초). 사용한 적이 없으면 생략됩니다.

<details>
<summary>요청/응답 JSON</summary>

*요청*

```json
{
    "type": "rpc_req",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "method": "token.list",
        "params": []
    }
}
```

*응답*

```json
{
    "type": "rpc_rsp",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "result": [
            {
                "id": 11,
                "name": "_docgen_uiapi_token",
                "user": "SYS",
                "hint": "nt_b_XXXX****XXXX",
                "createdAt": 1789632914,
                "notAfter": 2105252114
            }
        ]
    }
}
```

</details>

#### token.generate

`token.generate(name, notAfter)`

*매개변수*
- `name` *string* - 토큰 이름. 비어 있으면 오류를 반환합니다.
- `notAfter` *int64* - 만료 시각(Unix 타임스탬프, 초)
    0이면 발급 시점부터 10년 뒤로 설정합니다.

*반환값*

- `object<GeneratedApiToken>|error` - `token.list` 항목과 같은 필드에 토큰 원문인 `token`이 더해집니다.
    토큰 원문은 이 응답에서만 받을 수 있습니다.

<details>
<summary>요청/응답 JSON</summary>

*요청*

```json
{
    "type": "rpc_req",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "method": "token.generate",
        "params": [
            "_docgen_uiapi_token",
            0
        ]
    }
}
```

*응답*

```json
{
    "type": "rpc_rsp",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "result": {
            "id": 11,
            "name": "_docgen_uiapi_token",
            "user": "SYS",
            "hint": "nt_b_XXXX****XXXX",
            "createdAt": 1789632914,
            "notAfter": 2105252114,
            "token": "nt_b_XXXXXXXXXXXXXXXX"
        }
    }
}
```

</details>

#### token.delete

`token.delete(id)`

*매개변수*
- `id` *int64* - `token.list`나 `token.generate`가 반환한 토큰 ID

*반환값*

- `null|error`

<details>
<summary>요청/응답 JSON</summary>

*요청*

```json
{
    "type": "rpc_req",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "method": "token.delete",
        "params": [
            11
        ]
    }
}
```

*응답*

```json
{
    "type": "rpc_rsp",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "result": null
    }
}
```

</details>

### Timer

타이머는 `timer.list`나 `timer.add`가 반환하는 ID로 지정합니다. 같은 이름으로 다시 추가해도 새 ID로 등록됩니다. 실행 주기의 문법은 [타이머](/neo/timer/)를 참고합니다.

#### timer.list

`timer.list()`

*매개변수*

- 없음

*반환값*

- `array<object<timer.Info>>|error` - 타이머 목록
    - `id`: 타이머 ID
    - `userName`, `execUser`: 타이머를 소유한 사용자와 실행하는 사용자
    - `name`: 타이머 이름
    - `autoStart`: 자동 시작 여부. `false`이면 생략됩니다.
    - `state`: `RUNNING`, `STARTING`, `STOP`, `STOPPING`, `FAILED`, `UNKNOWN` 중 하나
    - `task`: 실행할 TQL 파일 경로
    - `schedule`: 실행 주기

<details>
<summary>요청/응답 JSON</summary>

*요청*

```json
{
    "type": "rpc_req",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "method": "timer.list",
        "params": []
    }
}
```

*응답*

```json
{
    "type": "rpc_rsp",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "result": [
            {
                "id": 9,
                "userName": "SYS",
                "execUser": "sys",
                "name": "_DOCGEN_UIAPI_TIMER",
                "state": "STOP",
                "task": "_docgen_uiapi_timer.tql",
                "schedule": "@every 1h"
            }
        ]
    }
}
```

</details>

#### timer.get

`timer.get(id)`

*매개변수*
- `id` *int64* - 타이머 ID

*반환값*

- `object<timer.Info>|error` - 타이머 정보. 필드는 `timer.list`와 같습니다.

<details>
<summary>요청/응답 JSON</summary>

*요청*

```json
{
    "type": "rpc_req",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "method": "timer.get",
        "params": [
            9
        ]
    }
}
```

*응답*

```json
{
    "type": "rpc_rsp",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "result": {
            "id": 9,
            "userName": "SYS",
            "execUser": "sys",
            "name": "_DOCGEN_UIAPI_TIMER",
            "state": "STOP",
            "task": "_docgen_uiapi_timer.tql",
            "schedule": "@every 1h"
        }
    }
}
```

</details>

#### timer.add

`timer.add(req)`

*매개변수*
- `req` *object*
    - `name` *string* - 타이머 이름. 대문자로 바뀌어 저장됩니다.
    - `spec` *string* - 실행 주기. 예) `0 30 * * * *`(매시 30분), `@every 1h30m`(1시간 30분 간격), `@daily`(매일)
    - `command` *string* - 실행할 TQL 파일 경로. 파일이 없으면 오류를 반환합니다.
    - `autoStart` *bool* - `true`이면 추가하는 즉시 시작하고, machbase-neo가 시작할 때도 자동으로 시작합니다.

*반환값*

- `int64|error` - 생성된 타이머 ID

<details>
<summary>요청/응답 JSON</summary>

*요청*

```json
{
    "type": "rpc_req",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "method": "timer.add",
        "params": [
            {
                "name": "_docgen_uiapi_timer",
                "spec": "@every 1h",
                "command": "_docgen_uiapi_timer.tql",
                "autoStart": false
            }
        ]
    }
}
```

*응답*

```json
{
    "type": "rpc_rsp",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "result": 9
    }
}
```

</details>

#### timer.update

`id`로 지정한 타이머의 설정을 요청 내용으로 바꿉니다.

`timer.update(req)`

*매개변수*
- `req` *object*
    - `id` *int64* - 타이머 ID
    - `spec` *string* - 실행 주기
    - `command` *string* - 실행할 TQL 파일 경로. 생략하면 오류를 반환합니다.
    - `autoStart` *bool* - 자동 시작 여부. 생략하면 `false`가 됩니다.

*반환값*

- `null|error`

<details>
<summary>요청/응답 JSON</summary>

*요청*

```json
{
    "type": "rpc_req",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "method": "timer.update",
        "params": [
            {
                "id": 9,
                "spec": "0 30 * * * *",
                "command": "_docgen_uiapi_timer.tql",
                "autoStart": true
            }
        ]
    }
}
```

*응답*

```json
{
    "type": "rpc_rsp",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "result": null
    }
}
```

</details>

#### timer.delete

`timer.delete(id)`

*매개변수*
- `id` *int64* - 타이머 ID

*반환값*

- `null|error`

<details>
<summary>요청/응답 JSON</summary>

*요청*

```json
{
    "type": "rpc_req",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "method": "timer.delete",
        "params": [
            9
        ]
    }
}
```

*응답*

```json
{
    "type": "rpc_rsp",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "result": null
    }
}
```

</details>

#### timer.start

`timer.start(id)`

*매개변수*
- `id` *int64* - 타이머 ID

*반환값*

- `null|error`

<details>
<summary>요청/응답 JSON</summary>

*요청*

```json
{
    "type": "rpc_req",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "method": "timer.start",
        "params": [
            9
        ]
    }
}
```

*응답*

```json
{
    "type": "rpc_rsp",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "result": null
    }
}
```

</details>

#### timer.stop

`timer.stop(id)`

*매개변수*
- `id` *int64* - 타이머 ID

*반환값*

- `null|error`

<details>
<summary>요청/응답 JSON</summary>

*요청*

```json
{
    "type": "rpc_req",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "method": "timer.stop",
        "params": [
            9
        ]
    }
}
```

*응답*

```json
{
    "type": "rpc_rsp",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "result": null
    }
}
```

</details>

### Subscriber

구독자는 `subscriber.list`나 `subscriber.add`가 반환하는 ID로 지정합니다. 브리지 설정은 [MQTT 브리지](/neo/bridges/mqtt/)와 [NATS 브리지](/neo/bridges/nats/)를 참고합니다.

#### subscriber.list

`subscriber.list()`

*매개변수*

- 없음

*반환값*

- `array<object<subscriber.Info>>|error` - 구독자 목록
    - `id`: 구독자 ID
    - `userName`, `execUser`: 구독자를 소유한 사용자와 실행하는 사용자
    - `name`: 구독자 이름
    - `autoStart`: 자동 시작 여부
    - `state`: `RUNNING`, `STARTING`, `STOP`, `STOPPING`, `FAILED`, `UNKNOWN` 중 하나
    - `task`: 쓰기 설명자
    - `bridge`: 브리지 이름
    - `topic`: 구독하는 MQTT 토픽 또는 NATS subject
    - `qos`, `queue`, `stream`: 브리지 옵션
    - `autoStart`, `qos`, `queue`, `stream` 필드는 값이 없으면 생략됩니다.

<details>
<summary>요청/응답 JSON</summary>

*요청*

```json
{
    "type": "rpc_req",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "method": "subscriber.list",
        "params": []
    }
}
```

*응답*

```json
{
    "type": "rpc_rsp",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "result": [
            {
                "id": 4,
                "userName": "SYS",
                "execUser": "sys",
                "name": "_DOCGEN_UIAPI_SUBR",
                "state": "STOP",
                "task": "db/append/EXAMPLE:csv",
                "bridge": "_docgen_uiapi_mqtt",
                "topic": "_docgen_uiapi/sensor",
                "qos": 1
            }
        ]
    }
}
```

</details>

#### subscriber.get

`subscriber.get(id)`

*매개변수*
- `id` *int64* - 구독자 ID

*반환값*

- `object<subscriber.Info>|error` - 구독자 정보. 필드는 `subscriber.list`와 같습니다.

<details>
<summary>요청/응답 JSON</summary>

*요청*

```json
{
    "type": "rpc_req",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "method": "subscriber.get",
        "params": [
            4
        ]
    }
}
```

*응답*

```json
{
    "type": "rpc_rsp",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "result": {
            "id": 4,
            "userName": "SYS",
            "execUser": "sys",
            "name": "_DOCGEN_UIAPI_SUBR",
            "state": "STOP",
            "task": "db/append/EXAMPLE:csv",
            "bridge": "_docgen_uiapi_mqtt",
            "topic": "_docgen_uiapi/sensor",
            "qos": 1
        }
    }
}
```

</details>

#### subscriber.add

`subscriber.add(req)`

*매개변수*
- `req` *object*
    - `name` *string* - 구독자 이름. 대문자로 바뀌어 저장됩니다.
    - `bridge` *string* - 구독자가 사용할 브리지 이름
    - `command` *string* - 예) `db/append/EXAMPLE:csv`. 쓰기 설명자로, 이 예는 CSV 형식으로 들어온 데이터를 `EXAMPLE` 테이블에 append 모드로 기록한다는 의미입니다.
    - `autoStart` *bool* - `true`이면 machbase-neo가 시작할 때 구독자도 함께 시작합니다.
    - `mqtt` *object* - MQTT 브리지 옵션
        - `topic` *string* - 구독할 토픽
        - `qos` *int* - 토픽 구독의 QoS 레벨. `0`과 `1`을 지원하며 기본값은 `0`입니다.
    - `nats` *object* - NATS 브리지 옵션
        - `subject` *string* - 구독할 subject
        - `queue` *string* - 큐 그룹
        - `stream` *string* - 스트림 이름
- `name`, `bridge`, `command`와 토픽(`mqtt.topic` 또는 `nats.subject`)은 필수입니다.
- `mqtt`와 `nats`는 함께 지정할 수 없습니다.

*반환값*

- `int64|error` - 생성된 구독자 ID

<details>
<summary>요청/응답 JSON</summary>

*요청*

```json
{
    "type": "rpc_req",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "method": "subscriber.add",
        "params": [
            {
                "name": "_docgen_uiapi_subr",
                "bridge": "_docgen_uiapi_mqtt",
                "command": "db/append/EXAMPLE:csv",
                "autoStart": false,
                "mqtt": {
                    "topic": "_docgen_uiapi/sensor",
                    "qos": 1
                }
            }
        ]
    }
}
```

*응답*

```json
{
    "type": "rpc_rsp",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "result": 4
    }
}
```

</details>

#### subscriber.update

`id`로 지정한 구독자의 설정을 요청 내용으로 바꿉니다.

`subscriber.update(req)`

*매개변수*
- `req` *object*
    - `id` *int64* - 구독자 ID
    - `bridge`, `command`, `autoStart`, `mqtt`, `nats` - `subscriber.add`와 같습니다.

*반환값*

- `null|error`

<details>
<summary>요청/응답 JSON</summary>

*요청*

```json
{
    "type": "rpc_req",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "method": "subscriber.update",
        "params": [
            {
                "id": 4,
                "bridge": "_docgen_uiapi_mqtt",
                "command": "db/append/EXAMPLE:json",
                "autoStart": false,
                "mqtt": {
                    "topic": "_docgen_uiapi/sensor2",
                    "qos": 0
                }
            }
        ]
    }
}
```

*응답*

```json
{
    "type": "rpc_rsp",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "result": null
    }
}
```

</details>

#### subscriber.delete

`subscriber.delete(id)`

*매개변수*
- `id` *int64* - 구독자 ID

*반환값*

- `null|error`

<details>
<summary>요청/응답 JSON</summary>

*요청*

```json
{
    "type": "rpc_req",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "method": "subscriber.delete",
        "params": [
            4
        ]
    }
}
```

*응답*

```json
{
    "type": "rpc_rsp",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "result": null
    }
}
```

</details>

#### subscriber.start

`subscriber.start(id)`

*매개변수*
- `id` *int64* - 구독자 ID

*반환값*

- `null|error`

<details>
<summary>요청/응답 JSON</summary>

*요청*

```json
{
    "type": "rpc_req",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "method": "subscriber.start",
        "params": [
            4
        ]
    }
}
```

*응답*

```json
{
    "type": "rpc_rsp",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "result": null
    }
}
```

</details>

#### subscriber.stop

`subscriber.stop(id)`

*매개변수*
- `id` *int64* - 구독자 ID

*반환값*

- `null|error`

<details>
<summary>요청/응답 JSON</summary>

*요청*

```json
{
    "type": "rpc_req",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "method": "subscriber.stop",
        "params": [
            4
        ]
    }
}
```

*응답*

```json
{
    "type": "rpc_rsp",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "result": null
    }
}
```

</details>

### Http

#### http.debug.set

`http.debug.set(m)`

*매개변수*
- `m` *object* - `enable`, `logLatency` 키를 가진 디버그 설정 맵

*반환값*

- `object|error`

<details>
<summary>요청/응답 JSON</summary>

*요청*

```json
{
    "type": "rpc_req",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "method": "http.debug.set",
        "params": [
            {}
        ]
    }
}
```

*응답*

```json
{
    "type": "rpc_rsp",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "result": {}
    }
}
```

</details>

#### http.split

`http.split(content)`

*매개변수*
- `content` *string* - HTTP 스크립트 텍스트

*반환값*

- `array<object<util.HttpStatement>>|error` - 파싱된 HTTP 구문 배열

<details>
<summary>요청/응답 JSON</summary>

*요청*

```json
{
    "type": "rpc_req",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "method": "http.split",
        "params": [
            "string"
        ]
    }
}
```

*응답*

```json
{
    "type": "rpc_rsp",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "result": []
    }
}
```

</details>

### Session

#### session.list

`session.list()`

*매개변수*

- 없음

*반환값*

- `array<object<Session>>|error`

<details>
<summary>요청/응답 JSON</summary>

*요청*

```json
{
    "type": "rpc_req",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "method": "session.list",
        "params": []
    }
}
```

*응답*

```json
{
    "type": "rpc_rsp",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "result": []
    }
}
```

</details>

#### session.kill

`session.kill(id, force)`

*매개변수*
- `id` *string*
- `force` *bool*

*반환값*

- `null|error`

<details>
<summary>요청/응답 JSON</summary>

*요청*

```json
{
    "type": "rpc_req",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "method": "session.kill",
        "params": [
            "string",
            false
        ]
    }
}
```

*응답*

```json
{
    "type": "rpc_rsp",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "result": null
    }
}
```

</details>

#### session.stat

`session.stat(reset)`

*매개변수*
- `reset` *bool*

*반환값*

- `object<server_api.Statz>|error`

<details>
<summary>요청/응답 JSON</summary>

*요청*

```json
{
    "type": "rpc_req",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "method": "session.stat",
        "params": [
            false
        ]
    }
}
```

*응답*

```json
{
    "type": "rpc_rsp",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "result": {}
    }
}
```

</details>

#### session.limit.get

`session.limit.get()`

*매개변수*

- 없음

*반환값*

- `object<SessionLimit>|error`

<details>
<summary>요청/응답 JSON</summary>

*요청*

```json
{
    "type": "rpc_req",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "method": "session.limit.get",
        "params": []
    }
}
```

*응답*

```json
{
    "type": "rpc_rsp",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "result": {}
    }
}
```

</details>

#### session.limit.set

`session.limit.set(m)`

*매개변수*
- `m` *object*

*반환값*

- `null|error`

<details>
<summary>요청/응답 JSON</summary>

*요청*

```json
{
    "type": "rpc_req",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "method": "session.limit.set",
        "params": [
            {}
        ]
    }
}
```

*응답*

```json
{
    "type": "rpc_rsp",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "result": null
    }
}
```

</details>

### Sql

#### sql.split

`sql.split(content)`

*매개변수*
- `content` *string*

*반환값*

- `array<object<util.SqlStatement>>|error`

<details>
<summary>요청/응답 JSON</summary>

*요청*

```json
{
    "type": "rpc_req",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "method": "sql.split",
        "params": [
            "string"
        ]
    }
}
```

*응답*

```json
{
    "type": "rpc_rsp",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "result": []
    }
}
```

</details>

### Lsp

#### lsp.diagnostics

`lsp.diagnostics(req)`

*매개변수*
- `req` *object<lspDocumentRequest>*

*반환값*

- `object|error`

<details>
<summary>요청/응답 JSON</summary>

*요청*

```json
{
    "type": "rpc_req",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "method": "lsp.diagnostics",
        "params": [
            {}
        ]
    }
}
```

*응답*

```json
{
    "type": "rpc_rsp",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "result": {}
    }
}
```

</details>

#### lsp.completion

`lsp.completion(req)`

*매개변수*
- `req` *object<lspDocumentRequest>*

*반환값*

- `object|error`

<details>
<summary>요청/응답 JSON</summary>

*요청*

```json
{
    "type": "rpc_req",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "method": "lsp.completion",
        "params": [
            {}
        ]
    }
}
```

*응답*

```json
{
    "type": "rpc_rsp",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "result": {}
    }
}
```

</details>

#### lsp.hover

`lsp.hover(req)`

*매개변수*
- `req` *object<lspDocumentRequest>*

*반환값*

- `object|error`

<details>
<summary>요청/응답 JSON</summary>

*요청*

```json
{
    "type": "rpc_req",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "method": "lsp.hover",
        "params": [
            {}
        ]
    }
}
```

*응답*

```json
{
    "type": "rpc_rsp",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "result": {}
    }
}
```

</details>

#### lsp.signature

`lsp.signature(req)`

*매개변수*
- `req` *object<lspDocumentRequest>*

*반환값*

- `object|error`

<details>
<summary>요청/응답 JSON</summary>

*요청*

```json
{
    "type": "rpc_req",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "method": "lsp.signature",
        "params": [
            {}
        ]
    }
}
```

*응답*

```json
{
    "type": "rpc_rsp",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "result": {}
    }
}
```

</details>

#### lsp.metadata

`lsp.metadata(req)`

*매개변수*
- `req` *object<lspMetadataRequest>*

*반환값*

- `object|error`

<details>
<summary>요청/응답 JSON</summary>

*요청*

```json
{
    "type": "rpc_req",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "method": "lsp.metadata",
        "params": [
            {}
        ]
    }
}
```

*응답*

```json
{
    "type": "rpc_rsp",
    "session": "client-session-#1",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "result": {}
    }
}
```

</details>

