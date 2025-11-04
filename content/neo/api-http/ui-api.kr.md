---
title: 사용자 인터페이스 API
type: docs
weight: 55
---

이 사용자 인터페이스 API는 JWT 기반 인증으로 클라이언트 요청을 검증합니다.

## 사용자 인증

### 로그인

**POST `/web/api/login`**

{{< tabs items="Request,Response">}}
{{< tab >}}
```json
{
    "loginName": "sys",
    "password": "manager"
}
```
{{< /tab >}}
{{< tab >}}
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

{{< tabs items="Request,Response">}}
{{< tab >}}
```json
{
    "refreshToken": "'login' 시 발급된 리프레시 토큰"
}
```
{{< /tab >}}
{{< tab >}}
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
    "refreshToken": "'login' 시 발급된 리프레시 토큰"
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
    "id": "셸 정의 ID(uuid)",
    "type": "유형",
    "icon": "아이콘 이름",
    "label": "표시 이름",
    "theme": "테마 이름",
    "command": "터미널 셸 명령",
    "attributes": [
        { "removable": true },
        { "cloneable": true },
        { "editable": true }
    ]
}
```

- types

| type | description        |
|:-----| :------------------|
| sql  | SQL 편집기          |
| tql  | TQL 편집기          |
| wrk  | 워크스페이스 편집기 |
| taz  | 태그 분석기         |
| term | 터미널              |

## 데이터베이스

### SQL 실행

**GET, POST `/web/machbase`**

`/db/query` API와 동일하게 동작하며, 차이점은 인증 방식입니다.
`/db/query`는 클라이언트 애플리케이션을 API 토큰으로 인증하는 반면,
`/web/machbase`는 사용자 상호작용을 위해 JWT를 검증합니다.

### 테이블 목록 조회

**GET `/web/api/tables?showall=false&name=pattern`**

테이블 목록을 반환합니다.

- `showall`을 `true`로 설정하면 숨김 테이블까지 모두 포함합니다.
- `name`은 테이블 이름을 필터링하는 패턴으로, `?` 또는 `*`가 포함된 glob 표현식이나 접두어(특수 문자가 없는 경우)를 사용할 수 있습니다.

```json
{
    "success": true,
    "reason": "성공 여부 또는 메시지",
    "elapse": "문자열 형식의 경과 시간",
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
    "reason": "성공 여부 또는 메시지",
    "elapse": "문자열 형식의 경과 시간",
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

**GET `/web/api/tables/:table/:tag/stat`**

지정한 테이블의 태그 통계를 반환합니다.

```json
{
    "success": true,
    "reason": "성공 여부 또는 메시지",
    "elapse": "문자열 형식의 경과 시간",
    "data": {
        "columns": ["ROWNUM", "NAME", "ROW_COUNT", "MIN_TIME", "MAX_TIME",
			"MIN_VALUE", "MIN_VALUE_TIME", "MAX_VALUE", "MAX_VALUE_TIME", "RECENT_ROW_TIME"],
        "types": ["int32", "string", "int64", "datetime", "datetime","double", 
            "datetime", "double", , "datetime",, "datetime"],
        "rows":[
            ["...omit...."],
        ]
    }
}
```

## 셸 및 터미널

### 데이터 채널

**`ws:///web/api/term/:term_id/data`**

터미널용 웹소켓입니다.

### 창 크기

**POST `/web/api/term/:term_id/windowsize`**

터미널 크기를 변경합니다.

`TerminalSize`

```json
{ "rows": 24, "cols": 80 }
```

### 셸 정의 조회

**GET `/web/api/shell/:id`**

지정한 ID에 대한 `ShellDefinition`을 반환합니다.

### 셸 정의 수정

**POST `/web/api/shell/:id`**

지정한 ID의 `ShellDefinition`을 업데이트합니다.

### 셸 복제

**GET `/web/api/shell/:id/copy`**

지정한 ID의 셸을 복제한 새 `ShellDefinition`을 반환합니다.

### 셸 정의 삭제 

**DELETE `/web/api/shell/:id`**

지정한 ID의 셸을 삭제합니다.

```json
{
    "success": true,
    "reason": "성공 또는 오류 메시지",
    "elapse": "문자열 형식의 시간"
}
```

## 서버 이벤트

### 이벤트 채널

**`ws:/web/api/console/:console_id/data`**

양방향 메시지를 위한 웹소켓입니다.

- 메시지 유형

```json
{
    "type": "아래 표 참고",
    "ping": {
        "tick": 1234
    },
    "log": {
        "level": "INFO",
        "message": "로그 메시지"
    }
}
```

| type           |  fields          | description                                                    |
|:---------------| :----------------| :-------------------------------------------------------------|
| `ping`         |                  | 핑 메시지                                                      |
|                | `ping.tick`      | 임의의 정수. 서버는 클라이언트가 보낸 숫자를 그대로 응답합니다. |
| `log`          | `log.level`      | 로그 레벨 `TRACE`, `DEBUG`, `INFO`, `WARN`, `ERROR`           |
|                | `log.message`    | 로그 메시지                                                    |
|                | `log.repeat`     | 동일 메시지가 연속 두 번 이상 반복될 때의 횟수                |


## TQL 및 워크스페이스

**TQL 컨텐츠 유형**

| Header <br/>`Content-Type` | Header <br/>`X-Chart-Type` |          Content                          |
|:--------------------------:| :-------------------------:| :---------------------------------------- |
| text/html                  | "echart", "geomap"         | 전체 HTML <br/>예: `<iframe>` 내부에 포함 |
| text/html                  | -                          | 전체 HTML <br/>예: `<iframe>` 내부에 포함 |
| text/csv                   | -                          | CSV                                       |
| text/markdown              | -                          | 마크다운                                  |
| application/json           | "echart", "geomap"         | JSON(echart 또는 geomap 데이터)           |
| application/json           | -                          | JSON                                      |
| application/xhtml+xml      | -                          | HTML 요소, 예: `<div>...</div>`           |


### TQL 파일 실행

**GET `/web/api/tql/*path`**

지정한 경로의 TQL을 실행합니다. 응답 형식은 위 ‘TQL 컨텐츠 유형’ 표를 참고해 주십시오.

**POST `/web/api/tql/*path`**

지정한 경로의 TQL을 실행합니다. 응답 형식은 위 ‘TQL 컨텐츠 유형’ 표를 참고해 주십시오.

### TQL 스크립트 실행

**POST `/web/api/tql`**

본문에 TQL 스크립트를 담아 전송하면 서버가 실행 결과를 반환합니다.
응답 형식은 ‘TQL 컨텐츠 유형’ 표를 참고해 주십시오.

요청에 `$`라는 쿼리 매개변수가 포함되어 있으면 해당 값을 TQL 스크립트로 간주하고,
본문은 데이터로 처리합니다. `$` 매개변수는 v8.0.17부터 사용할 수 있습니다.

### 마크다운 렌더링

**POST `/web/api/md`**

본문에 마크다운을 담아 전송하면 서버가 XHTML 형식의 렌더링 결과를 반환합니다.

## 파일 관리

### Content-Type

파일 유형과 Content-Type 매핑입니다.

| file type | Content-Type             |
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
    "content": "파일일 때 바이트 배열",
    "children": [{"디렉터리일 때의 SubEntry"}],
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

### 키 목록 조회

**GET `/web/api/keys/:id`**

키 정보를 반환합니다.

`response`

```json
{
    "success": true,
    "reason": "success",
    "data": [
        {
            "idx": 0,
            "id": "eleven",
            "notBefore": 1713171461,
            "notAfter": 2028531461
        }
    ],
    "elapse": "131.9µs"
}
```
### 키 생성

**POST `/web/api/keys`**

키를 생성합니다.
- `name`은 필수입니다.
- `notAfter`는 만료 시각입니다.

{{< tabs items="Request,Response">}}
{{< tab >}}
```json
{
    "name": "eleven",
    "notBefore": 0,
    "notAfter": 0
}
```
{{< /tab >}}
{{< tab >}}
```json
{
    "success": true,
    "reason": "success",
    "elapse": "5.4961ms",
    "certificate": "-----BEGIN CERTIFICATE-----\nXXXXXXXXXXXXXXXXXX\n-----END CERTIFICATE-----\n",
    "privateKey": "-----BEGIN EC PRIVATE KEY-----\nXXXXXXXXXXXXXXXX\n-----END EC PRIVATE KEY-----\n",
    "token": "eleven:b:XXXXXXXXXXXXXXXXX"
}
```
{{< /tab >}}
{{< /tabs >}}



### 키 삭제

**DELETE `/web/api/keys/:id`**

지정한 ID의 키를 삭제합니다.

`response`

```json
{
    "success": true,
    "reason": "success",
    "elapse": "112.8µs"
}
```

## SSH 키

### SSH 키 목록 조회

**GET `/web/api/sshkeys`**

SSH 키 정보를 반환합니다.

`response`

```json
{
    "data": [
        {
            "keyType": "ssh-rsa",
            "fingerprint": "f08h89fhf0dkv0v0v9c9x0cx9v9",
            "comment": "example@machbase.com"
        }
    ],
    "elapse": "67.6µs",
    "reason": "success",
    "success": true
}
```
### SSH 키 생성

**POST `/web/api/sshkeys`**

**SSH 공개 키 인증 사용**

machbase-neo 서버에 공개 키를 등록하면 `machbase-neo shell` 명령을 비밀번호 입력 없이 실행할 수 있습니다.

{{< tabs items="Request,Response">}}
{{< tab >}}
```json
{
    "key": "your publickey"
}
```
{{< /tab >}}
{{< tab >}}
```json
{
    "elapse": "138.801µs",
    "reason": "success",
    "success": true
}
```
{{< /tab >}}
{{< /tabs >}}



### SSH 키 삭제

**DELETE `/web/api/sshkeys/:fingerprint`**

지정한 지문(fingerprint)의 SSH 키를 삭제합니다.

`response`
```json
{
    "elapse": "198.8µs",
    "reason": "success",
    "success": true
}
```



## 타이머

### 타이머 조회

**GET `/web/api/timers/:name`**

타이머 정보를 반환합니다.

- 상태 값: `RUNNING`, `STARTING`, `STOP`, `STOPPING`, `FAILED`, `UNKNWON`

`response`

```json
{
    "success": true,
    "reason": "success",
    "data": [
        {
            "name": "ELEVEN",
            "type": "TIMER",
            "state": "STOP", 
            "task": "timer.tql",
            "schedule": "0 30 * * * *"
        }
    ],
    "elapse": "92.1µs"
}
```

### 타이머 목록

**GET `/web/api/timers`**

타이머 정보 목록을 반환합니다.
- 상태 값: `RUNNING`, `STARTING`, `STOP`, `STOPPING`, `FAILED`, `UNKNWON`

`response`

```json
{
    "success": true,
    "reason": "success",
    "data": [
        {
            "name": "ELEVEN",
            "type": "TIMER",
            "state": "STOP",
            "task": "timer.tql",
            "schedule": "0 30 * * * *"
        },
        {
            "name": "TWELVE",
            "type": "TIMER",
            "state": "RUNNING",
            "task": "timer2.tql",
            "schedule": "1 30 * * * *"
        }
    ],
    "elapse": "92.1µs"
}
```
### 타이머 추가

**POST `/web/api/timers`**

타이머를 추가합니다.
- `name`, `autoStart`, `schedule`, `path`는 필수입니다.

타이머 `schedule` 예시
- `0 30 * * * *`           매 시간 30분마다
- `@every 1h30m`           1시간 30분 간격
- `@daily`                 매일

{{< tabs items="Request,Response">}}
{{< tab >}}
```json
{
    "name":"eleven",
    "autoStart":false,
    "schedule":"@every 10s",
    "path":"timer.tql"
}
```
{{< /tab >}}
{{< tab >}}
```json
{
    "success": true,
    "reason": "success",
    "elapse": "4.9658ms"
}
```
{{< /tab >}}
{{< /tabs >}}

### 타이머 시작

**POST `/web/api/timers/:name/state`**

타이머를 시작합니다.
- `state` 값이 필요합니다.

{{< tabs items="Request,Response">}}
{{< tab >}}
```json
{
    "state":"start",
}
```
{{< /tab >}}
{{< tab >}}
```json
{
    "success": true,
    "reason": "success",
    "elapse": "822.601µs"
}
```
{{< /tab >}}
{{< /tabs >}}

### 타이머 중지

**POST `/web/api/timers/:name/state`**

타이머를 중지합니다.
- `state` 값이 필요합니다.

{{< tabs items="Request,Response">}}
{{< tab >}}
```json
{
    "state":"stop",
}
```
{{< /tab >}}
{{< tab >}}
```json
{
    "success": true,
    "reason": "success",
    "elapse": "26.2µs"
}
```
{{< /tab >}}
{{< /tabs >}}

### 타이머 수정

**PUT `/web/api/timers/:name`**

타이머 설정을 수정합니다.
- `autoStart`, `schedule`, `path`를 지정할 수 있습니다.

{{< tabs items="Request,Response">}}
{{< tab >}}
```json
{
    "audoStart" : true,
    "schedule":"@every 5s",
    "path":"timer.tql"
}
```
{{< /tab >}}
{{< tab >}}
```json
{
    "elapse": "459.6µs",
    "reason": "success",
    "success": true
}
```
{{< /tab >}}
{{< /tabs >}}



### 타이머 삭제

**DELETE `/web/api/timers/:name`**

타이머를 삭제합니다.

`Response`
```json
{
    "success": true,
    "reason": "success",
    "elapse": "4.8664ms"
}
```


## 브리지

### 브리지 목록

**GET `/web/api/bridges`**

브리지 정보를 반환합니다.

`response`

```json
{
    "success": true,
    "reason": "success",
    "data": [
        {
            "name": "pg",
            "type": "postgres",
            "path": "host=127.0.0.1 port=5432 user=postgres password=1234 dbname=bridgedb sslmode=disable"
        }
    ],
    "elapse": "1.328301ms"
}
```
### 브리지 추가

**POST `/web/api/bridges`**

브리지를 추가합니다.
- `name`, `type`, `path`는 필수입니다.
- 지원되는 브리지는 `SQLite`, `PostgreSql`, `Mysql`, `MSSQL`, `MQTT`입니다.

{{< tabs items="Request,Response">}}
{{< tab >}}
```json
{
    "name":"pg",
    "type":"postgres", // sqlite, postgres, mysql, mssql, mqtt 중 선택
    "path":"host=127.0.0.1 port=5432 user=postgres password=1234 dbname=bridgedb sslmode=disable"
}
```
{{< /tab >}}
{{< tab >}}
```json
{
    "success": true,
    "reason": "success",
    "elapse": "193.499µs"
}
```
{{< /tab >}}
{{< /tabs >}}

### 브리지 실행

**POST `/web/api/bridges/:name/state`**

브리지에서 명령을 실행합니다.
- `state`, `command`가 필요합니다.

{{< tabs items="Request,Response">}}
{{< tab >}}
```json
{
    "state":"exec",
    "command":"CREATE TABLE IF NOT EXISTS pg_example(id SERIAL PRIMARY KEY,company VARCHAR(50) UNIQUE NOT NULL,employee  INT,discount REAL,plan FLOAT(8),code UUID,valid BOOL, memo TEXT, created_on TIMESTAMP NOT NULL)"
}
```
{{< /tab >}}
{{< tab >}}
```json
{
    "success": true,
    "reason": "success",
    "elapse": "217.4µs"
}
```
{{< /tab >}}
{{< /tabs >}}

### 브리지 쿼리

**POST `/web/api/bridges/:name/state`**

브리지에서 쿼리를 수행합니다.
- `state`, `command`가 필요합니다.

{{< tabs items="Request,Response">}}
{{< tab >}}
```json
{
    "state":"query",
    "command":"select * from pg_example"
}
```
{{< /tab >}}
{{< tab >}}
```json
{
    "success": true,
    "reason": "success",
    "column": [
        "id",
        "company",
        "employee",
        "discount",
        "plan",
        "code",
        "valid",
        "memo",
        "created_on"
    ],
    "rows": [
        [
            2,
            "test-company",
            10,
            1.234,
            2.3456,
            "c2d29867-3d0b-d497-9191-18a9d8ee7830",
            true,
            "test memo",
            "2023-08-09T14:20:00+09:00"
        ],
        [
            3,
            "test-company2",
            10,
            1.234,
            2.3456,
            null,
            null,
            null,
            "2023-08-09T14:20:00+09:00"
        ]
    ],
    "elapse": "53.015905ms"
}
```
{{< /tab >}}
{{< /tabs >}}

### 브리지 테스트

**POST `/web/api/bridges/:name/state`**

브리지를 테스트합니다.

{{< tabs items="Request,Response">}}
{{< tab >}}
```json
{
    "state":"test",
}
```
{{< /tab >}}
{{< tab >}}
```json
{
    "success": true,
    "reason": "success",
    "elapse": "331.1µs"
}
```
{{< /tab >}}
{{< /tabs >}}


### 브리지 삭제

**DELETE `/web/api/bridges/:name`**

지정한 이름의 브리지를 삭제합니다.

`response`

```json
{
    "success": true,
    "reason": "success",
    "elapse": "112.8µs"
}
```

## 구독자

### 구독자 조회

**GET `/web/api/subscribers/:name`**

구독자 정보를 반환합니다.
- 상태 값: `RUNNING`, `STARTING`, `STOP`, `STOPPING`, `FAILED`, `UNKNWON`
- `autoStart`, `queue`, `QoS` 필드는 값이 없으면 생략됩니다.

`response`

```json
{
    "data": [
        {
            "name": "NATS_SUBR",
            "type": "SUBSCRIBER",
            "autoStart": true,  // 값이 없으면 생략
            "state": "RUNNING", 
            "task": "db/append/EXAMPLE:csv",
            "bridge": "my_nats",
            "topic": "iot.sensor",
            "queue":"", // 값이 없으면 생략
            "QoS":""    // 값이 없으면 생략
        }
    ],
    "elapse": "253.4µs",
    "reason": "success",
    "success": true
}
```

### 구독자 목록

**GET `/web/api/subscribers`**

구독자 정보 목록을 반환합니다.
- 상태 값: `RUNNING`, `STARTING`, `STOP`, `STOPPING`, `FAILED`, `UNKNWON`
- `autoStart`, `queue`, `QoS` 필드는 값이 없으면 생략됩니다.

`response`

```json
{
    "data": [
        {
            "name": "NATS_SUBR",
            "type": "SUBSCRIBER",
            "autoStart": true,  // 값이 없으면 생략
            "state": "RUNNING",
            "task": "db/append/EXAMPLE:csv",
            "bridge": "my_nats",
            "topic": "iot.sensor",
            "queue":"", // 값이 없으면 생략
            "QoS":""    // 값이 없으면 생략
        },
        {
            "name": "NATS_SUBR2",
            "type": "SUBSCRIBER",
            "autoStart": true,  // 값이 없으면 생략
            "state": "STARTING",
            "task": "db/insert/EXAMPLE2:csv",
            "bridge": "my_nats2",
            "topic": "iot.sensor2",
            "queue":"", // 값이 없으면 생략
            "QoS":""    // 값이 없으면 생략
        }
    ],
    "elapse": "253.4µs",
    "reason": "success",
    "success": true
}
```
### 구독자 추가

**POST `/web/api/subscribers`**

구독자를 추가합니다.
- `autostart`: `--autostart`를 지정하면 machbase-neo가 시작할 때 함께 시작합니다. 생략하면 수동으로 시작/중지할 수 있습니다.
- `name`: 예) `nats_subr`, 구독자 이름입니다.
- `bridge`: 예) `my_nats`, 구독자가 사용할 브리지 이름입니다.
- `topic`: 예) `iot.sensor`, 구독할 대상이며 NATS 주제 문법을 따라야 합니다.
- `task`: 예) `db/append/EXAMPLE:csv`, 데이터 형식과 쓰기 모드를 지정합니다. CSV 데이터를 EXAMPLE 테이블에 append 모드로 적재한다는 의미입니다.
- `autostart`가 false이면 `subscriber start <name>`, `subscriber stop <name>` 명령으로 수동 제어가 가능합니다.
- `QoS` <int>: 브리지가 MQTT 유형일 때 토픽 구독 QoS를 지정합니다. 0 또는 1을 사용할 수 있으며, 기본값은 0입니다.
- `queue` <string>: 브리지가 NATS 유형일 때 큐 그룹을 지정합니다.

자세한 설정은 nats-bridge 매뉴얼(https://docs.machbase.com/neo/bridges/31.nats/)을 참고해 주십시오.

{{< tabs items="Request,Response">}}
{{< tab >}}
```json
{
    "name":"nats_subr",
    "autoStart":true,
    "bridge":"my_nats",
    "topic":"iot.sensor",
    "task":"db/append/EXAMPLE:csv",
    "QoS": "",  // MQTT 브리지 옵션: 0 또는 1 (기본값 0)
    "queue": "" // NATS 브리지 옵션
}
```
{{< /tab >}}
{{< tab >}}
```json
{
    "elapse": "260µs",
    "reason": "success",
    "success": true
}
```
{{< /tab >}}
{{< /tabs >}}

### 구독자 시작

**POST `/web/api/subscribers/:name/state`**

- `state` 값이 필요합니다.

{{< tabs items="Request,Response">}}
{{< tab >}}
```json
{
    "state":"start",
}
```
{{< /tab >}}
{{< tab >}}
```json
{
    "elapse": "166.1µs",
    "reason": "success",
    "success": true
}
```
{{< /tab >}}
{{< /tabs >}}

### 구독자 중지

**POST `/web/api/subscribers/:name/state`**

- `state` 값이 필요합니다.

{{< tabs items="Request,Response">}}
{{< tab >}}
```json
{
    "state":"stop",
}
```
{{< /tab >}}
{{< tab >}}
```json
{
    "elapse": "54.2µs",
    "reason": "success",
    "success": true
}
```
{{< /tab >}}
{{< /tabs >}}


### 구독자 삭제

**DELETE `/web/api/subscribers/:name`**

지정한 이름의 구독자를 삭제합니다.

`response`

```json
{
    "elapse": "77.1µs",
    "reason": "success",
    "success": true
}
```

## 백업

### 백업 조회

**GET `/web/api/backup/archives`**

백업 목록을 반환합니다.
- 기본 백업 디렉터리는 `$MACHBASE_HOME/dbs/backup`입니다.
- machbase-neo를 `--backup-dir={path}` 옵션으로 실행해야 합니다.

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

데이터베이스를 백업합니다.</br>
- **전체 백업**: 전체 데이터를 백업합니다.
- **증분 백업**: 전체 백업 또는 이전 증분 백업 이후 추가된 데이터만 백업합니다.
- **기간 백업**: 특정 기간의 데이터를 백업합니다.

`request`
{{< tabs items="Full Backup,Incremental Backup,Time Backup, Table Backup">}}
{{< tab >}}
```json
{
    "type":"database", // database 또는 table
    "tableName":"",
    "duration":{
        "type":"full",
        "after":"",
        "from":"",
        "to":""
    },
    "path":"example_backup1" 
    // "path":"/home/neo/backups/example_backup1" // 절대 경로 예시
}
```
{{< /tab >}}
{{< tab >}}
```json
{
    "type":"database", // database 또는 table
    "tableName":"",
    "duration":{
        "type":"incremental",
        "after":"{previous_backup_dir}",
        "from":"",
        "to":""
    },
    "path":"example_backup1" 
    // "path":"/home/neo/backups/example_backup1" // 절대 경로 예시
}
```
{{< /tab >}}
{{< tab >}}
```json
{
    "type":"database", // database 또는 table
    "tableName":"",
    "duration":{
        "type":"time",
        "after":"",
        "from":"2024-08-01 00:00:00",
        "to":"2024-08-02 23:59:59"
    },
    "path":"example_backup1" 
    // "path":"/home/neo/backups/example_backup1" // 절대 경로 예시
}
```
{{< /tab >}}
{{< tab >}}
```json
{
    "type":"table", // database 또는 table
    "tableName":"example",
    "duration":{
        "type":"full",
        "after":"",
        "from":"",
        "to":""
    },
    "path":"example_backup1" 
    // "path":"/home/neo/backups/example_backup1" // 절대 경로 예시
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

백업 상태를 반환합니다.</br>

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

{{< tabs items="Request,Response">}}
{{< tab >}}
```json
{
    "path":"example_backup1" // 상대 경로
    // "path":"/home/machbase/machbase_home/dbs/example_backup1" // 절대 경로
}
```
{{< /tab >}}
{{< tab >}}
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

### 검색

**GET `/web/api/pkgs/search?name=pkg_name&possibles=10`**

`Query Parameter`
 - `name`: 패키지 이름, 필수
 - `possible`: 검색 개수 (`possible=0`이면 전체 검색)


`response`

```json
{
    "success": true,
    "reason": "success",
    "data":{},
    "elapse": "547.1µs"
}
```
### 동기화

**GET `/web/api/pkgs/sync`**

패키지 정보를 동기화합니다.

`response`

```json
{
    "success": true,
    "reason": "success",
    "elapse": "30.9144ms"
}
```


### 설치

**GET `/web/api/pkgs/insall/:name`**

 - `:name`: 설치할 패키지 이름, 필수

`response`
```json
{
    "success": true,
    "reason": "success",
    "data":{}, // 값이 없으면 생략
    "log":"",
    "elapse": "23.1491ms"
}
```

### 제거

**GET `/web/api/pkgs/uninsall/:name`**

 - `:name`: 제거할 패키지 이름, 필수

`response`
```json
{
    "success": true,
    "reason": "success",
    "data":{}, // 값이 없으면 생략
    "log":"",
    "elapse": "88.4133ms"
}
```


## 기타

### 참고 자료

**GET `/web/api/refs/*path`**

- `ReferenceGroup`
```json
{
    "label": "그룹 이름",
    "items":[{"ReferenceItem"}]
}
```

- `ReferenceItem`
```json
{
    "type": "type",
    "title": "표시 제목",
    "address": "URL 주소",
    "target": "브라우저 링크 대상"
}
```

- type: `url`, `wrk`, `tql`, `sql`
- address: `serverfile://<path>` 접두사가 있으면 서버의 파일을 가리키고,
  그렇지 않으면 `https://`로 시작하는 외부 웹 URL입니다.


### SQL 구문 분할기

**POST `/web/api/splitter/sql`**

```json
{
    "success": true,
    "reason": "성공 또는 오류 사유",
    "elapse": "경과 시간",
    "data": {
        "statements": [
            {
                "text": "-- env: bridge=sqlite",
                "beginLine": 1,
                "endLine": 1,
                "isComment": true,
                "env": {
                    "bridge": "sqlite",
                    "error": "`-- env: bridge=database`에 문법 오류가 있을 때"
                }
            },
            {
                "text": "select * from table",
                "beginLine": 2,
                "endLine": 2,
                "isComment": false,
                "env": {
                    "bridge": "sqlite",
                    "error": "`-- env: bridge=database`에 문법 오류가 있을 때"
                }
            },
            {
                "text": "-- comment",
                "beginLine": 3,
                "endLine": 3,
                "isComment": true,
                "env": {}
            }
        ]
    }
}
```

### 라이선스 정보

**GET `/web/api/license`**

```json
{
    "success": true,
    "reason": "성공 또는 오류 사유",
    "elapse": "경과 시간",
    "data": {
        "id": "라이선스 ID",
        "type": "유형",
        "customer": "고객",
        "project": "프로젝트",
        "countryCode": "국가 코드",
        "installDate": "설치 일자",
        "issueDate": "라이선스 발급 일자"
    }
}
```

### 라이선스 설치

**POST `/web/api/license`**

라이선스 파일을 설치합니다.


## WebSocket

```
ws://127.0.0.1:5654/web/ui/console/{console_id}/data?token={jwt_token}
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

서버는 사용자에게 친숙한 메시지를 전송하여 상태 업데이트나 오류 알림을 제공합니다.
이 메시지는 상태, 문제, 가이드를 명확하게 전달하여 원활한 상호작용과 문제 해결을 돕습니다.

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
- **task** (선택): 관련 작업 이름.
- **message**: 설명 메시지.
- **repeat** (선택): 동일한 로그 메시지가 연속으로 반복된 횟수로, 중복 출력을 줄이는 데 활용됩니다.

### RPC
{{< callout type="warning" >}}
WebSocket 기반 RPC 기능은 현재 활발히 개발 중입니다. 향후 릴리스에서 동작, 프로토콜 세부사항, 지원 메서드가 변경될 수 있습니다.
{{< /callout >}}

이 절에서는 JSON-RPC 사양을 따르는 WebSocket 기반 원격 프로시저 호출(RPC) 메커니즘을 설명합니다.
RPC를 사용하면 클라이언트가 서버 측 메서드를 호출하고 구조화된 응답을 받을 수 있어,
클라이언트 애플리케이션과 서버 간 통신 및 통합이 원활해집니다.

**요청**

- 방향: C -> S

```json
{
    "type": "rpc_req",
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


#### llmGetProviders

`llmGetProviders()`

*요청*

```json
{
    "type": "rpc_req",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 10,
        "method": "llmGetProviders"
    }
}
```

*응답*

```json
{
    "type": "rpc_rsp",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 10,
        "result": [
            {
                "name": "Ollama qweb3:0.6b",
                "provider": "ollama",
                "model": "qwen3:0.6b"
            },
            {
                "name": "claude Sonnet 4",
                "provider": "claude",
                "model": "claude-sonnet-4-20250514"
            },
        ]
    }
}
```

#### markdownRender

`markdownRender(markdown, darkmode)`

*매개변수*
- `markdown` *string*: 마크다운 본문
- `darkmode` *bool*: 다크 모드를 사용할 경우 `true`

*요청*

```json
{
    "type": "rpc_req",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "method": "markdownRender",
        "params": ["# Hello World\nThis is a **test**.", false]
    }
}
```

*응답*

```json
{
    "type": "rpc_rsp",
    "rpc": {
        "jsonrpc": "2.0",
        "id": 20,
        "result": "<h1>Hello World</h1>\n<p>This is a <strong>test</strong>.</p>\n"
    }
}
```

### MESSAGE

{{< callout type="warning" >}}
WebSocket 기반 MESSAGE 기능은 현재 활발히 개발 중입니다. 향후 릴리스에서 동작, 프로토콜 세부사항, 지원 메서드가 변경될 수 있습니다.
{{< /callout >}}

```json
{
    "type": "msg",
    "msg": {
        "ver": "1.0",
        "id": 1234,
        "type": "question",
        "body": {
        }
    }
}
```

- **ver**: 프로토콜 버전으로 반드시 `"1.0"`이어야 합니다.
- **id**: 현재 메시지 또는 질문을 식별하는 고유 시퀀스 번호입니다.
- **type**: 메시지 유형입니다. 사용할 수 있는 값은 `"question"`, `"stream-message-start"`, `"stream-message-delta"`, `"stream-message-stop"`, `"stream-block-start"`, `"stream-block-delta"`, `"stream-block-stop"`입니다.
- **body**: 메시지 유형에 해당하는 페이로드를 포함합니다.

**Question**

- 방향: C -> S

```json
{
    "type": "msg",
    "msg": {
        "ver": "1.0",
        "id": 1234,
        "type": "question",
        "body": {
            "provider": "ollama",
            "model": "qweb3.0:8b",
            "text": "어떤 종류의 테이블이 있나요?"
        }
    }
}
```

**Stream**

- 방향: S -> C

```json
{
    "type": "msg",
    "msg": {
        "ver": "1.0",
        "id": 1234,
        "type": "stream-block-delta",
        "body": {
            "data": "안녕하세요, 저는 machbase-neo 에이전트입니다",
        }
    }
}
```
