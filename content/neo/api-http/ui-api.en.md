---
title: User Interface API
type: docs
weight: 55
---

The user interface API validates requests from clients with JWT-based authentication.

## User Authenticate

### Login

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

### Refresh token

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

### Logout

**POST `/web/api/logout`**

- `LogoutReq`:

```json
{
    "refreshToken": "refresh token that was issued with 'login'"
}
```

### Status

**GET `/web/api/check`**

Validates the current token status.

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

- types

| type | description      |
|:-----| :------------    |
| sql  | SQL editor       |
| tql  | TQL editor       |
| wrk  | Workspace editor |
| taz  | Tag analyzer     |
| term | Terminal         |

## Database

### Execute SQL

**GET, POST `/web/machbase`**

It works the same as the `/db/query` API; the only difference is the authentication method.
`/db/query` authorizes client applications with an API token,
while `/web/machbase` validates a JWT for user interactions.

### List tables

**GET `/web/api/tables?showall=false&name=pattern`**

Returns the table list.

- `showall`: if set to `true`, the list includes all hidden tables.
- `name`: table name filtering pattern. The pattern can be a glob (includes `?` or `*`) or a prefix (has no `?` or `*`).

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

### List tags

**GET `/web/api/tables/:table/tags?name=prefix`**

Returns the tag list of the table.

- `name`: returns only the tags whose names start with the given prefix.

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

### Tag stat

**GET `/web/api/tables/:table/tags/:tag/stat`**

Returns the statistics of the tag in the table.

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

## Shell & Terminal

Shell definitions are listed, added, copied, updated, and deleted with the JSON-RPC [`shell.*`](#shelllist) methods.

### Data channel

**`ws://{server_address}/web/api/term/:term_id/data`**

WebSocket for the terminal.

### Window size

**POST `/web/api/term/:term_id/windowsize`**

Changes the terminal size.

`TerminalSize`

```json
{ "rows": 24, "cols": 80 }
```

## Server events

### Event channel

**`ws://127.0.0.1:5654/web/api/console/{console_id}/data?token={jwt_token}`**

WebSocket for bi-directional messages.

- message type

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

| type           |  fields          | description        |
|:---------------| :----------------| :------------------|
| `ping`         |                  | Ping message       |
|                | `ping.tick`      | Any integer. The server responds with the same number that the client sent. |
| `log`          | `log.level`      | Log level: `TRACE`, `DEBUG`, `INFO`, `WARN`, `ERROR`|
|                | `log.message`    | Log message        |
|                | `log.repeat`     | Repeat count when the same message occurs two or more times in a row |

## TQL & Workspace

**Content-types of TQL**

| Header <br/>`Content-Type` | Header <br/>`X-Chart-Type` |          Content            |
|:--------------------------:| :-------------------------:| :-------------------------- |
| text/html                  | "echart", "geomap"         | Full HTML <br/>e.g., embedded in an `<iframe>` |
| text/html                  | -                          | Full HTML <br/>e.g., embedded in an `<iframe>` |
| text/csv                   | -                          | CSV                         |
| text/markdown              | -                          | Markdown                    |
| application/json           | "echart", "geomap"         | JSON (echart or geomap data)|
| application/json           | -                          | JSON                        |
| application/xhtml+xml      | -                          | HTML element, e.g., `<div>...</div>` |

### Run tql file

**GET `/web/api/tql/*path`**

Runs the TQL at the path. For the response format, refer to the 'Content-types of TQL' table above.

**POST `/web/api/tql/*path`**

Runs the TQL at the path. For the response format, refer to the 'Content-types of TQL' table above.

### Run tql script

**POST `/web/api/tql`**

Post a TQL script as the content payload, and the server responds with the execution result.
For the response format, refer to the 'Content-types of TQL' table.

If the request has a query parameter named `$`, its value is taken as the TQL script,
and the payload is treated as data. This `$` query parameter is available since v8.0.17.

### Markdown rendering

To render Markdown, use the JSON-RPC [`markdown.render`](#markdownrender) method.

## File management

### Content-Type

File types and their content types.

| file type | Content-Type             |
|:----------|:-------------------------|
| .sql      | text/plain               |
| .tql      | text/plain               |
| .taz      | application/json         |
| .wrk      | application/json         |
| unknown   | application/octet-stream |

### Read file

**GET `/web/api/files/*path`**

Returns the content of the file if the path points to a file.

Returns the directory entries if the path points to a directory.

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

### Write file

**POST `/web/api/files/*path`**

- If the `path` points to a file, it writes the payload content into the file.

- If the `path` is a directory and the request has no content, it creates an empty directory
  and returns the `Entry` of the directory.

- If the `path` is a directory and the payload is `GitCloneReq` JSON,
  it clones the remote Git repository to the `path` and returns the `Entry` of the directory.

`GitCloneReq`

```json
{
    "command": "clone",
    "url": "https://github.com/machbase/neo-samples.git"
}
```

- `command` : `clone`, `pull`

### Rename/move file

**PUT `/web/api/files/*path`**

Renames (moves) a file or a directory.

`RenameReq`

```json
{
    "destination": "target path",
}
```

This API returns status code `200 OK` if the operation completes successfully.

### Remove file

**DELETE `/web/api/files/*path`**

Deletes the file at the `path`. If the path points to a directory that is not empty, it returns an error.

## Key management

Keys are managed with the JSON-RPC [`key.*`](#keylist) methods, and API tokens with the [`token.*`](#tokenlist) methods.

## Ssh Key

SSH keys are managed with the JSON-RPC [`sshkey.*`](#sshkeylist) methods.

## Timer

Timers are managed with the JSON-RPC [`timer.*`](#timerlist) methods.

## Bridge

To manage bridges and run commands on them, use the JSON-RPC [`bridge.*`](#bridgelist) methods.

## Subscriber

Subscribers are managed with the JSON-RPC [`subscriber.*`](#subscriberlist) methods.

## Backup

### Get Backup

**GET `/web/api/backup/archives`**

Returns the backup list.

- The default backup directory is `backups` under the directory of the machbase-neo executable.
- To change the location, start machbase-neo with the `--backup-dir={path}` option. This option is not required when using the default.

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

### DB Backup

**POST `/web/api/backup/archive`**

Backs up the database.<br/>

- **Full backup**: backs up the entire data.
- **Incremental backup**: backs up the data added after the full or previous incremental backup.
- **Time duration backup**: backs up the data for a specific period.

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

### Status Backup

**GET `/web/api/backup/archive/status`**

Returns the backup status.<br/>

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

## Mount

### Mount List

**GET `/web/api/backup/mounts`**

Returns the mount list.

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

### DB Mount

**POST `/web/api/backup/mounts/:name`**

Mounts a database.

- `:name`: mount name
- `path`: backup database path (both absolute and relative paths are available)

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

### DB Unmount

**DELETE `/web/api/backup/mounts/:name`**

Unmounts a database.

- `:name`: name to unmount

`response`

```json
{
    "elapse": "46.8694ms",
    "reason": "success",
    "success": true
}
```

## Package

Packages are installed and removed with the JSH [`pkg` command](/neo/jsh/packages/).

## Others

### References

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
- address: if the address has the prefix `serverfile://<path>`, it points to a server-side file;
  otherwise, it is an external web URL that starts with `https://`.

### SQL statements splitter

To split SQL statements, use the JSON-RPC [`sql.split`](#sqlsplit) method.

### License info

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

### License install

**POST `/web/api/license`**

Installs a license file.

## WebSocket

```
ws://127.0.0.1:5654/web/api/console/{console_id}/data?token={jwt_token}
```

The `console_id` must be a unique identifier generated by the client application to ensure proper session management.

This endpoint requires a JWT token to be provided as a query parameter (`token={jwt_token}`), rather than using the HTTP `Authorization` header.

Communication through this endpoint is performed by exchanging JSON objects between the server and client, enabling structured and secure data transfer.

### PING

A client can send a *PING* message containing the current time in Unix epoch format.
Upon receiving this message, the server responds with the same payload,
allowing the client to accurately measure the round-trip latency.
This mechanism also helps maintain the connection and prevents idle timeouts.

- Direction: C -> S

```json
{
    "type": "ping",
    "ping": {
        "tick": 1759127437000
    }
}
```

### LOG

The server transmits user-friendly messages to provide informative updates or error notifications.
These messages are designed to clearly communicate status, issues, or guidance to the client, ensuring effective interaction and troubleshooting.

- Direction: S -> C

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

- **timestamp**: The log event time, represented as a Unix epoch in nanoseconds.
- **level**: Log severity, one of `"TRACE"`, `"DEBUG"`, `"INFO"`, `"WARN"`, or `"ERROR"`.
- **task** (optional): The name of the related task.
- **message**: The descriptive log message.
- **repeat** (optional): The number of consecutive occurrences of the same log message, used to reduce redundant output.

## JSON-RPC

This section describes the remote procedure call (RPC) mechanism over WebSocket,
which follows the JSON-RPC specification.
RPC enables clients to invoke server-side methods and receive structured responses,
facilitating seamless communication and integration between client applications and the server.

The Web UI provides JSON-RPC endpoints for management-oriented features.

- HTTP POST endpoint: `/web/api/rpc`
- WebSocket endpoint: `/web/api/console/:console_id/data?token={jwt_token}`

For simple request/response interactions, use `/web/api/rpc`.
When you need bi-directional messaging over an existing console session, use `/web/api/console/:console_id/data?token={jwt_token}`.

### HTTP JSON-RPC request format

**POST `/web/api/rpc`**

Request example:

```json
{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "shell.list",
    "params": []
}
```

Success response example:

```json
{
    "jsonrpc": "2.0",
    "id": 1,
    "result": []
}
```

Error response example:

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

Notes:

- The HTTP status is normally `200 OK`.
- Detect failures by checking the `error` field, not by the HTTP status code.

### WebSocket JSON-RPC request format

**`ws://{server_address}/web/api/console/:console_id/data?token={jwt_token}`**

Over WebSocket, use `rpc_req` and `rpc_rsp` event wrappers.
The `session` field is an identifier that the UI client can use to route the response back to the correct tab or view.

**Request**

- Direction: C -> S

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

**Response**

- Direction: S -> C

**success**

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

**error**

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

*Params*
- `markdown` *string*
- `darkMode` *bool*
- `referer` *string* - the referer URL

*Return*

- `string|error`

<details>
<summary>Request/Response JSON</summary>

*Request*

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

*Response*

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

*Params*
- `vizspec` *object*

*Return*

- `object|error`

<details>
<summary>Request/Response JSON</summary>

*Request*

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

*Response*

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

*Params*
- `vizspec` *object*
- `format` *string*

*Return*

- `object|error`

<details>
<summary>Request/Response JSON</summary>

*Request*

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

*Response*

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

*Params*

- none

*Return*

- `object<ServerInfoResponse>|error`

<details>
<summary>Request/Response JSON</summary>

*Request*

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

*Response*

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

*Params*
- `names` *array<string>* - metric names

*Return*

- `object<ServerStatzResponse>|error` - visualization specifications grouped by name

<details>
<summary>Request/Response JSON</summary>

*Request*

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

*Response*

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

*Params*
- `maxRows` *int* - maximum row count
- `pattern` *array<string>* - wildcard filters for metric keys

*Return*

- `object<StatzQueryResult>|error` - tabular metric query result

<details>
<summary>Request/Response JSON</summary>

*Request*

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

*Response*

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

*Params*
- `pattern` *array<string>* - wildcard filters for metric keys

*Return*

- `array<string>|error` - sorted metric key names

<details>
<summary>Request/Response JSON</summary>

*Request*

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

*Response*

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

*Params*

- none

*Return*

- `string|error`

<details>
<summary>Request/Response JSON</summary>

*Request*

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

*Response*

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

Implemented by the management (mgmt) server.

`server.shutdown()`

*Params*

- none

*Return*

- `object<ShutdownResponse>|error`

<details>
<summary>Request/Response JSON</summary>

*Request*

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

*Response*

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

*Params*
- `svc` *string*

*Return*

- `array<object<model.ServicePort>>|error`

<details>
<summary>Request/Response JSON</summary>

*Request*

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

*Response*

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

*Params*
- `req` *object<ProxyRegisterRequest>*

*Return*

- `object<ProxyEntrySnapshot>|error`

<details>
<summary>Request/Response JSON</summary>

*Request*

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

*Response*

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

*Params*
- `req` *object<ProxyUnregisterRequest>*

*Return*

- `array<object<ProxyEntrySnapshot>>|error`

<details>
<summary>Request/Response JSON</summary>

*Request*

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

*Response*

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

*Params*
- `service` *string*

*Return*

- `array<object<ProxyEntrySnapshot>>|error`

<details>
<summary>Request/Response JSON</summary>

*Request*

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

*Response*

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

*Params*
- `req` *object<ProxyGetRequest>*

*Return*

- `object<ProxyEntrySnapshot>|error`

<details>
<summary>Request/Response JSON</summary>

*Request*

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

*Response*

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

*Params*

- none

*Return*

- `array<object<model.ShellDefinition>>|error`

<details>
<summary>Request/Response JSON</summary>

*Request*

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

*Response*

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

*Params*
- `name` *string*
- `command` *string*

*Return*

- `string|error`

<details>
<summary>Request/Response JSON</summary>

*Request*

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

*Response*

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

Copies the given shell definition and returns the copy with a new id.

`shell.copy(srcId)`

*Params*
- `srcId` *string* - id of the shell definition to copy

*Return*

- `object<model.ShellDefinition>|error` - the copied shell definition

<details>
<summary>Request/Response JSON</summary>

*Request*

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

*Response*

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

Updates a shell definition. The target is identified by `id`, and the whole definition is sent.

`shell.update(shell)`

*Params*
- `shell` *object<model.ShellDefinition>* - shell definition with `id`, `type`, `label`, `command`, `icon`, `theme`, and `attributes`
    returns an error if `command` is empty

*Return*

- `object<model.ShellDefinition>|error` - the updated shell definition

<details>
<summary>Request/Response JSON</summary>

*Request*

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

*Response*

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

*Params*
- `id` *string*

*Return*

- `null|error`

<details>
<summary>Request/Response JSON</summary>

*Request*

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

*Response*

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

*Params*

- none

*Return*

- `array<object<bridge.BridgeInfo>>|error`

<details>
<summary>Request/Response JSON</summary>

*Request*

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

*Response*

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

*Params*
- `name` *string*

*Return*

- `object<bridge.BridgeInfo>|error`

<details>
<summary>Request/Response JSON</summary>

*Request*

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

*Response*

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

*Params*
- `name` *string*
- `typ` *string*
- `conn` *string*

*Return*

- `null|error`

<details>
<summary>Request/Response JSON</summary>

*Request*

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

*Response*

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

*Params*
- `name` *string*

*Return*

- `null|error`

<details>
<summary>Request/Response JSON</summary>

*Request*

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

*Response*

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

*Params*
- `name` *string*

*Return*

- `bool|error`

<details>
<summary>Request/Response JSON</summary>

*Request*

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

*Response*

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

*Params*
- `name` *string*

*Return*

- `object<BridgeStats>|error`

<details>
<summary>Request/Response JSON</summary>

*Request*

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

*Response*

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

*Params*
- `name` *string*
- `command` *string*

*Return*

- `object<BridgeExecResult>|error`

<details>
<summary>Request/Response JSON</summary>

*Request*

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

*Response*

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

*Params*
- `name` *string*
- `query` *string*

*Return*

- `object<BridgeQueryResult>|error`

<details>
<summary>Request/Response JSON</summary>

*Request*

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

*Response*

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

*Params*
- `handle` *string*

*Return*

- `object<BridgeQueryRow>|error`

<details>
<summary>Request/Response JSON</summary>

*Request*

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

*Response*

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

*Params*
- `handle` *string*

*Return*

- `null|error`

<details>
<summary>Request/Response JSON</summary>

*Request*

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

*Response*

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

*Params*

- none

*Return*

- `array<object<AuthorizedSshKey>>|error`

<details>
<summary>Request/Response JSON</summary>

*Request*

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

*Response*

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

*Params*
- `keyType` *string*
- `key` *string*
- `comment` *string*

*Return*

- `null|error`

<details>
<summary>Request/Response JSON</summary>

*Request*

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

*Response*

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

*Params*
- `key` *string*

*Return*

- `null|error`

<details>
<summary>Request/Response JSON</summary>

*Request*

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

*Response*

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

*Params*

- none

*Return*

- `array<object<KeyInfo>>|error` - the keys stored in the server key store
    - `idx`: position in the list
    - `id`: key id, the value to pass to `key.delete`
    - `name`: key name
    - `notBefore`, `notAfter`: start and end of the validity period in Unix timestamp (sec.)

<details>
<summary>Request/Response JSON</summary>

*Request*

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

*Response*

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

*Params*
- `name` *string* - key name, stored in lowercase
- `typ` *string* - the type of key to generate, must be `RSA` or `ECDSA`
- `notBefore` *int64* - the start time of the key's validity period in Unix timestamp (sec.)
    if not specified or 0, the current time will be used
- `notAfter` *int64* - the end time of the key's validity period in Unix timestamp (sec.)
    if not specified or 0, the default period of 10 years will be used
- `store` *bool* - whether to store the key pair in the server's key store
    if `false`, the key pair is not stored and does not appear in `key.list`

*Return*

- `any|error` - the generated key information
    - `id`: key id; `0` if `store` is false
    - `name`: key name
    - `certificate`: the certificate of the key pair
    - `key`: the private key of the key pair
    - `serverKey`: the server's certificate (if `store` is true)
    - `zip`: a base64-encoded zip archive containing the key pair and server certificate (if `store` is true)

<details>
<summary>Request/Response JSON</summary>

*Request*

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

*Response*

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

*Params*
- `id` *int64* - key id returned by `key.list` or `key.generate`

*Return*

- `null|error`

<details>
<summary>Request/Response JSON</summary>

*Request*

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

*Response*

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

For how to use an issued token, see [API Security](/neo/security/).

#### token.list

`token.list()`

*Params*

- none

*Return*

- `array<object<ApiTokenInfo>>|error` - the caller's API tokens
    - `id`: token id, the value to pass to `token.delete`
    - `name`: token name
    - `user`: the user who owns the token
    - `hint`: the token value, partially masked
    - `createdAt`: issue time in Unix timestamp (sec.)
    - `notAfter`: expiration time in Unix timestamp (sec.)
    - `lastUsedAt`: last use time in Unix timestamp (sec.), omitted if the token has never been used

<details>
<summary>Request/Response JSON</summary>

*Request*

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

*Response*

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

*Params*
- `name` *string* - token name; an empty name returns an error
- `notAfter` *int64* - expiration time in Unix timestamp (sec.)
    if 0, the token expires 10 years after it is issued

*Return*

- `object<GeneratedApiToken>|error` - the same fields as a `token.list` item, plus `token`, the plain token value
    the plain token value is available only in this response

<details>
<summary>Request/Response JSON</summary>

*Request*

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

*Response*

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

*Params*
- `id` *int64* - token id returned by `token.list` or `token.generate`

*Return*

- `null|error`

<details>
<summary>Request/Response JSON</summary>

*Request*

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

*Response*

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

A timer is identified by the id that `timer.list` or `timer.add` returns. Adding a timer with an existing name registers it under a new id. For the schedule syntax, see [Timer](/neo/timer/).

#### timer.list

`timer.list()`

*Params*

- none

*Return*

- `array<object<timer.Info>>|error` - timer list
    - `id`: timer id
    - `userName`, `execUser`: the user who owns the timer and the user who runs it
    - `name`: timer name
    - `autoStart`: whether the timer starts automatically, omitted if `false`
    - `state`: one of `RUNNING`, `STARTING`, `STOP`, `STOPPING`, `FAILED`, `UNKNOWN`
    - `task`: path of the TQL file to run
    - `schedule`: the schedule

<details>
<summary>Request/Response JSON</summary>

*Request*

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

*Response*

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

*Params*
- `id` *int64* - timer id

*Return*

- `object<timer.Info>|error` - timer information, with the same fields as `timer.list`

<details>
<summary>Request/Response JSON</summary>

*Request*

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

*Response*

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

*Params*
- `req` *object*
    - `name` *string* - timer name, stored in uppercase
    - `spec` *string* - the schedule, e.g., `0 30 * * * *` (every hour on the half hour), `@every 1h30m` (every 1 hour 30 minutes), `@daily` (every day)
    - `command` *string* - path of the TQL file to run; returns an error if the file does not exist
    - `autoStart` *bool* - if `true`, the timer starts as soon as it is added and also starts along with machbase-neo

*Return*

- `int64|error` - id of the created timer

<details>
<summary>Request/Response JSON</summary>

*Request*

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

*Response*

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

Replaces the settings of the timer given by `id` with the request.

`timer.update(req)`

*Params*
- `req` *object*
    - `id` *int64* - timer id
    - `spec` *string* - the schedule
    - `command` *string* - path of the TQL file to run; returns an error if omitted
    - `autoStart` *bool* - whether the timer starts automatically; becomes `false` if omitted

*Return*

- `null|error`

<details>
<summary>Request/Response JSON</summary>

*Request*

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

*Response*

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

*Params*
- `id` *int64* - timer id

*Return*

- `null|error`

<details>
<summary>Request/Response JSON</summary>

*Request*

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

*Response*

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

*Params*
- `id` *int64* - timer id

*Return*

- `null|error`

<details>
<summary>Request/Response JSON</summary>

*Request*

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

*Response*

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

*Params*
- `id` *int64* - timer id

*Return*

- `null|error`

<details>
<summary>Request/Response JSON</summary>

*Request*

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

*Response*

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

A subscriber is identified by the id that `subscriber.list` or `subscriber.add` returns. For bridge settings, see [MQTT bridge](/neo/bridges/mqtt/) and [NATS bridge](/neo/bridges/nats/).

#### subscriber.list

`subscriber.list()`

*Params*

- none

*Return*

- `array<object<subscriber.Info>>|error` - subscriber list
    - `id`: subscriber id
    - `userName`, `execUser`: the user who owns the subscriber and the user who runs it
    - `name`: subscriber name
    - `autoStart`: whether the subscriber starts automatically
    - `state`: one of `RUNNING`, `STARTING`, `STOP`, `STOPPING`, `FAILED`, `UNKNOWN`
    - `task`: the writing descriptor
    - `bridge`: bridge name
    - `topic`: the MQTT topic or NATS subject to subscribe to
    - `qos`, `queue`, `stream`: bridge options
    - `autoStart`, `qos`, `queue`, and `stream` are omitted if they have no value.

<details>
<summary>Request/Response JSON</summary>

*Request*

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

*Response*

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

*Params*
- `id` *int64* - subscriber id

*Return*

- `object<subscriber.Info>|error` - subscriber information, with the same fields as `subscriber.list`

<details>
<summary>Request/Response JSON</summary>

*Request*

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

*Response*

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

*Params*
- `req` *object*
    - `name` *string* - subscriber name, stored in uppercase
    - `bridge` *string* - the name of the bridge that the subscriber uses
    - `command` *string* - e.g., `db/append/EXAMPLE:csv`. The writing descriptor; this example means the incoming data is in CSV format and is written into the table `EXAMPLE` in append mode.
    - `autoStart` *bool* - if `true`, the subscriber starts along with machbase-neo
    - `mqtt` *object* - MQTT bridge options
        - `topic` *string* - the topic to subscribe to
        - `qos` *int* - the QoS level of the subscription; `0` and `1` are supported, and the default is `0`
    - `nats` *object* - NATS bridge options
        - `subject` *string* - the subject to subscribe to
        - `queue` *string* - queue group
        - `stream` *string* - stream name
- `name`, `bridge`, `command`, and the topic (`mqtt.topic` or `nats.subject`) are required.
- `mqtt` and `nats` cannot be set together.

*Return*

- `int64|error` - id of the created subscriber

<details>
<summary>Request/Response JSON</summary>

*Request*

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

*Response*

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

Replaces the settings of the subscriber given by `id` with the request.

`subscriber.update(req)`

*Params*
- `req` *object*
    - `id` *int64* - subscriber id
    - `bridge`, `command`, `autoStart`, `mqtt`, `nats` - same as `subscriber.add`

*Return*

- `null|error`

<details>
<summary>Request/Response JSON</summary>

*Request*

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

*Response*

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

*Params*
- `id` *int64* - subscriber id

*Return*

- `null|error`

<details>
<summary>Request/Response JSON</summary>

*Request*

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

*Response*

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

*Params*
- `id` *int64* - subscriber id

*Return*

- `null|error`

<details>
<summary>Request/Response JSON</summary>

*Request*

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

*Response*

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

*Params*
- `id` *int64* - subscriber id

*Return*

- `null|error`

<details>
<summary>Request/Response JSON</summary>

*Request*

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

*Response*

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

*Params*
- `m` *object* - debug setting map with `enable` and `logLatency` keys

*Return*

- `object|error`

<details>
<summary>Request/Response JSON</summary>

*Request*

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

*Response*

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

*Params*
- `content` *string* - HTTP script text

*Return*

- `array<object<util.HttpStatement>>|error` - parsed HTTP statements array

<details>
<summary>Request/Response JSON</summary>

*Request*

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

*Response*

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

*Params*

- none

*Return*

- `array<object<Session>>|error`

<details>
<summary>Request/Response JSON</summary>

*Request*

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

*Response*

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

*Params*
- `id` *string*
- `force` *bool*

*Return*

- `null|error`

<details>
<summary>Request/Response JSON</summary>

*Request*

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

*Response*

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

*Params*
- `reset` *bool*

*Return*

- `object<server_api.Statz>|error`

<details>
<summary>Request/Response JSON</summary>

*Request*

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

*Response*

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

*Params*

- none

*Return*

- `object<SessionLimit>|error`

<details>
<summary>Request/Response JSON</summary>

*Request*

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

*Response*

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

*Params*
- `m` *object*

*Return*

- `null|error`

<details>
<summary>Request/Response JSON</summary>

*Request*

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

*Response*

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

*Params*
- `content` *string*

*Return*

- `array<object<util.SqlStatement>>|error`

<details>
<summary>Request/Response JSON</summary>

*Request*

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

*Response*

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

*Params*
- `req` *object<lspDocumentRequest>*

*Return*

- `object|error`

<details>
<summary>Request/Response JSON</summary>

*Request*

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

*Response*

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

*Params*
- `req` *object<lspDocumentRequest>*

*Return*

- `object|error`

<details>
<summary>Request/Response JSON</summary>

*Request*

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

*Response*

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

*Params*
- `req` *object<lspDocumentRequest>*

*Return*

- `object|error`

<details>
<summary>Request/Response JSON</summary>

*Request*

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

*Response*

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

*Params*
- `req` *object<lspDocumentRequest>*

*Return*

- `object|error`

<details>
<summary>Request/Response JSON</summary>

*Request*

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

*Response*

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

*Params*
- `req` *object<lspMetadataRequest>*

*Return*

- `object|error`

<details>
<summary>Request/Response JSON</summary>

*Request*

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

*Response*

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

