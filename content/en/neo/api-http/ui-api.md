---
title: User Interface API
type: docs
weight: 55
---

These user interface API validates the requests from clients with JWT based authentication.

## User Authenticate

### Login

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


### Refresh token

**POST `/web/api/relogin`**

{{< tabs items="Request,Response">}}
{{< tab >}}
```json
{
    "refreshToken": "refresh token that was issued with 'login'"
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

Validates current  token status.

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
| sql  | sql editor       |
| tql  | tql editor       |
| wrk  | workspace editor |
| taz  | tag analyzer     |
| term | terminal         |

## Database

### Execute SQL

**GET,POST `/web/machbase`**

It works as same as `/db/query` API, the only difference is the way of authentication.
The `/db/query` authorize the client applications by API Token, while `/web/machbase` validates JWT for user interactions.

### List tables

**GET `/web/api/tables?showall=false&name=pattern`**

Return table list

- `showall` returns includes all hidden tables if set `true`
- `name` table name filtering pattern, the pattern can be a glob (includes `?` or `*`) or prefix (which has no `?` and `*`)

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

Returns tag list of the table

- `name` returns only tags those name starts with the given prefix

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

**GET `/web/api/tables/:table/:tag/stat`**

Returns the stat of tag of the table

```json
{
    "success": true,
    "reason": "success or other message",
    "elapse": "elapse time in string format",
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

## Shell & Terminal

### Data channel

**`ws:///web/api/term/:term_id/data`**

Web socket for terminal

### Window size

**POST `/web/api/term/:term_id/windowsize`**

Change terminal size

`TerminalSize`

```json
{ "rows": 24, "cols": 80 }
```

### Get Shell Definition

**GET `/web/api/shell/:id`**

Returns `ShellDefinition` for the given id

### Update Shell Definition

**POST `/web/api/shell/:id`**

Update the `ShellDefinition` of the given id

### Make copy of Shell

**GET `/web/api/shell/:id/copy`**

Returns `ShellDefinition` for a new copy of the shell of the given id

### Delete Shell Definition 

**DELETE `/web/api/shell/:id`**

Delete the shell of the given id

```json
{
    "success": true,
    "reason": "success of error message",
    "elapse": "time represents in text"
}
```

## Server events

### Event channel

**`ws:/web/api/console/:console_id/data`**

Web socket for the bi-directional messages

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
| `ping`         |                  | ping message       |
|                | `ping.tick`      | any integer number, server will respond with the same number that client sends |
| `log`          | `log.level`      | log level `TRACE`, `DEBUG`, `INFO`, `WARN`, `ERROR`|
|                | `log.message`    | log message        |
|                | `log.repeat`     | count, if the same message repeats more than two times in serial |


## TQL & Workspace

**Content-types of TQL**

| Header <br/>`Content-Type` | Header <br/>`X-Chart-Type` |          Content            |
|:--------------------------:| :-------------------------:| :-------------------------- |
| text/html                  | "echart"                   | Full HTML (echart) <br/>ex) It may be inside of `<iframe>`|
| text/html                  | -                          | Full HTML <br/>ex) It may be inside of `<iframe>` |
| text/csv                   | -                          | CSV                         |
| text/markdown              | -                          | Markdown                    |
| application/json           | "echart"                   | JSON (echart data)          |
| application/json           | -                          | JSON                        |
| application/xhtml+xml      | -                          | HTML Element, ex) `<div>...</div>` |


### Run tql file

**GET `/web/api/tql/*path`**

Run the tql of the path, refer the section of 'Content-types of TQL' for the response

**POST `/web/api/tql/*path`**

Run the tql of the path, refer the section of 'Content-types of TQL' for the response

### Run tql script

**POST `/web/api/tql`**

Post tql script as content payload, server will response the execution result.
refer the section of 'Content-types of TQL' for the response

### Markdown rendering

**POST `/web/api/md`**

Post markdown as content payload, sever will response the rendering result in xhtml

## File management

### Content-Type

File types and content-type

| file type | Content-Type             |
|:----------|:-------------------------|
| .sql      | text/plain               |
| .tql      | text/plain               |
| .taz      | application/json         |
| .wrk      | application/json         |
| unknown   | application/octet-stream |

### Read file

**GET `/web/api/files/*path`**

Returns the content of the file if the path is pointing a file.

Returns Dir entries if the path is pointing a directory.

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

- if the `path` points a file, it will write the payload content into the file.

- if the `path` is a directory and request with no content, it will create a empty directory.
  and returns the `Entry` of the directory

- if the `path` is a directory and payload is json of `GitCloneReq`,
  it will clone the remote git repository to the `path` and returns `Entry` of the directory.

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

Rename(move) a file (or a directory).

`RenameReq`

```json
{
    "destination": "target path",
}
```

This api returns status code `200 OK` if the operation has done successfully.


### Remove file

**DELETE `/web/api/files/*path`**

Delete the file at the `path`, if the path is pointing a directory and is not empty, it will return error.

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
- address: if address has prefix `serverfile://<path>` it points a server side file, 
  otherwise external web url that starts with `https://`



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

Install license file
