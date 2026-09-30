---
toc: true
title: ユーザーインターフェースAPI
type: docs
weight: 55
---

ユーザーインターフェースAPIは、JWT認証でクライアントのリクエストを検証します。

## ユーザー認証 {#사용자-인증}

### ログイン {#로그인}

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

### トークンの更新 {#토큰-갱신}

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

### ログアウト {#로그아웃}

**POST `/web/api/logout`**

- `LogoutReq`:

```json
{
    "refreshToken": "refresh token that was issued with 'login'"
}
```

### 状態の確認 {#상태-확인}

**GET `/web/api/check`**

現在のトークンの状態を検証します。

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

- 種類

| 型 | 説明        |
|:-----| :------------------|
| sql  | SQLエディター          |
| tql  | TQLエディター          |
| wrk  | ワークスペースエディター |
| taz  | タグアナライザー         |
| term | ターミナル              |

## データベース {#데이터베이스}

### SQLの実行 {#sql-실행}

**GET, POST `/web/machbase`**

`/db/query` APIと同じように動作し、認証方式だけが異なります。
`/db/query`はクライアントアプリケーションをAPIトークンで認証し、
`/web/machbase`はユーザー操作用にJWTを検証します。

### テーブル一覧の取得 {#테이블-목록-조회}

**GET `/web/api/tables?showall=false&name=pattern`**

テーブル一覧を返します。

- `showall`を`true`にすると、非表示のテーブルもすべて含めます。
- `name`はテーブル名の絞り込みパターンです。`?`や`*`を含むglob式、または`?`と`*`を含まない接頭辞を指定できます。

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

### タグ一覧の取得 {#태그-목록-조회}

**GET `/web/api/tables/:table/tags?name=prefix`**

指定テーブルのタグ一覧を返します。

- `name`を指定すると、その接頭辞で始まるタグだけを返します。

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

### タグ統計 {#태그-통계}

**GET `/web/api/tables/:table/tags/:tag/stat`**

指定テーブルのタグ統計を返します。

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

## シェルとターミナル {#셸-및-터미널}

シェル定義の取得・追加・複製・変更・削除には、JSON-RPCの[`shell.*`](#shelllist)メソッドを使用します。

### データチャネル {#데이터-채널}

**`ws://{server_address}/web/api/term/:term_id/data`**

ターミナル用のWebSocketです。

### ウィンドウサイズ {#창-크기}

**POST `/web/api/term/:term_id/windowsize`**

ターミナルのサイズを変更します。

`TerminalSize`

```json
{ "rows": 24, "cols": 80 }
```

## サーバーイベント {#서버-이벤트}

### イベントチャネル {#이벤트-채널}

**`ws://127.0.0.1:5654/web/api/console/{console_id}/data?token={jwt_token}`**

双方向メッセージ用のWebSocketです。

- メッセージの種類

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

| 型           |  フィールド          | 説明                                                    |
|:---------------| :----------------| :-------------------------------------------------------------|
| `ping`         |                  | pingメッセージ                                                      |
|                | `ping.tick`      | 任意の整数。サーバーは、クライアントが送信した数値をそのまま返します。 |
| `log`          | `log.level`      | ログレベル：`TRACE`、`DEBUG`、`INFO`、`WARN`、`ERROR`           |
|                | `log.message`    | ログメッセージ                                                    |
|                | `log.repeat`     | 同じメッセージが連続して2回以上繰り返された場合の回数                |

## TQLとワークスペース {#tql-및-워크스페이스}

**TQLのコンテンツタイプ**

| ヘッダー<br/>`Content-Type` | ヘッダー<br/>`X-Chart-Type` |          内容                          |
|:--------------------------:| :-------------------------:| :---------------------------------------- |
| text/html                  | "echart", "geomap"         | 完全なHTML。<br/>例：`<iframe>`内に埋め込む |
| text/html                  | -                          | 完全なHTML。<br/>例：`<iframe>`内に埋め込む |
| text/csv                   | -                          | CSV                                       |
| text/markdown              | -                          | Markdown                                  |
| application/json           | "echart", "geomap"         | JSON（echartまたはgeomapのデータ）           |
| application/json           | -                          | JSON                                      |
| application/xhtml+xml      | -                          | HTML要素。例：`<div>...</div>`           |

### TQLファイルの実行 {#tql-파일-실행}

**GET `/web/api/tql/*path`**

指定パスのTQLを実行します。応答形式は、前述の「TQLのコンテンツタイプ」表を参照してください。

**POST `/web/api/tql/*path`**

指定パスのTQLを実行します。応答形式は、前述の「TQLのコンテンツタイプ」表を参照してください。

### TQLスクリプトの実行 {#tql-스크립트-실행}

**POST `/web/api/tql`**

ボディにTQLスクリプトを送信すると、サーバーが実行結果を返します。
応答形式は、「TQLのコンテンツタイプ」表を参照してください。

リクエストに`$`クエリパラメーターがある場合は、その値をTQLスクリプトとして扱い、
ボディをデータとして処理します。`$`パラメーターは、v8.0.17以降で使用できます。

### Markdownのレンダリング {#마크다운-렌더링}

Markdownのレンダリングには、JSON-RPCの[`markdown.render`](#markdownrender)メソッドを使用します。

## ファイル管理 {#파일-관리}

### Content-Type {#content-type}

ファイルの種類とContent-Typeの対応です。

| ファイルの種類 | Content-Type             |
|:----------|:-------------------------|
| .sql      | text/plain               |
| .tql      | text/plain               |
| .taz      | application/json         |
| .wrk      | application/json         |
| unknown   | application/octet-stream |

### ファイルの読み取り {#파일-읽기}

**GET `/web/api/files/*path`**

パスがファイルを指す場合は、その内容を返します。

パスがディレクトリを指す場合は、エントリの一覧を返します。

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

### ファイルの書き込み {#파일-쓰기}

**POST `/web/api/files/*path`**

- `path`がファイルを指す場合は、ボディの内容をそのファイルに書き込みます。

- `path`がディレクトリでボディが空の場合は、空のディレクトリを作成し、その`Entry`を返します。

- `path`がディレクトリでボディが`GitCloneReq` JSONの場合は、リモートGitリポジトリをそのパスにクローンし、ディレクトリの`Entry`を返します。

`GitCloneReq`

```json
{
    "command": "clone",
    "url": "https://github.com/machbase/neo-samples.git"
}
```

- `command` : `clone`, `pull`

### ファイルの名前変更・移動 {#파일-이름-변경이동}

**PUT `/web/api/files/*path`**

ファイルまたはディレクトリの名前を変更するか、移動します。

`RenameReq`

```json
{
    "destination": "target path",
}
```

操作が正常に完了すると、APIは`200 OK`を返します。

### ファイルの削除 {#파일-삭제}

**DELETE `/web/api/files/*path`**

`path`のファイルを削除します。パスが空でないディレクトリを指す場合は、エラーを返します。

## キー管理 {#키-관리}

キーはJSON-RPCの[`key.*`](#keylist)メソッドで、APIトークンは[`token.*`](#tokenlist)メソッドで管理します。

## SSHキー {#ssh-키}

SSHキーは、JSON-RPCの[`sshkey.*`](#sshkeylist)メソッドで管理します。

## タイマー {#타이머}

タイマーは、JSON-RPCの[`timer.*`](#timerlist)メソッドで管理します。

## ブリッジ {#브리지}

ブリッジの管理とコマンドの実行には、JSON-RPCの[`bridge.*`](#bridgelist)メソッドを使用します。

## サブスクライバー {#구독자}

サブスクライバーは、JSON-RPCの[`subscriber.*`](#subscriberlist)メソッドで管理します。

## バックアップ {#백업}

### バックアップの取得 {#백업-조회}

**GET `/web/api/backup/archives`**

バックアップ一覧を返します。

- 既定のバックアップディレクトリは、machbase-neo実行ファイルのディレクトリ配下の`backups`です。
- 保存先を変更するには、`--backup-dir={path}`オプションを指定してmachbase-neoを起動します。既定値を使う場合、このオプションは不要です。

レスポンス

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
### DBのバックアップ {#db-백업}

**POST `/web/api/backup/archive`**

データベースをバックアップします。<br/>

- **完全バックアップ**：全データをバックアップします。
- **増分バックアップ**：完全バックアップまたは前回の増分バックアップ以降に追加されたデータだけをバックアップします。
- **期間バックアップ**：指定期間のデータをバックアップします。

リクエスト

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

レスポンス

```json
{
    "success": true,
    "reason": "success",
    "elapse": "231.3µs"
}
```

### バックアップ状態 {#백업-상태}

**GET `/web/api/backup/archive/status`**

バックアップ状態を返します。<br/>

レスポンス

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

## マウント {#마운트}

### マウント一覧 {#마운트-목록}

**GET `/web/api/backup/mounts`**

マウント一覧を返します。

レスポンス

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
### DBのマウント {#db-마운트}

**POST `/web/api/backup/mounts/:name`**

データベースをマウントします。

- `:name`: マウント名
- `path`: バックアップデータベースのパス（絶対パスと相対パスの両方を使用可能）

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

### DBのアンマウント {#db-언마운트}

**DELETE `/web/api/backup/mounts/:name`**

データベースをアンマウントします。

- `:name`: アンマウントする名前

レスポンス

```json
{
    "elapse": "46.8694ms",
    "reason": "success",
    "success": true
}
```


## パッケージ {#패키지}

パッケージのインストールと削除は、JSHの[`pkg`コマンド](/neo/jsh/packages/)で行います。

## その他 {#기타}

### 参考資料 {#참고-자료}

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
- address：`serverfile://<path>`接頭辞がある場合はサーバー側のファイルを指し、
  それ以外の場合は`https://`で始まる外部WebのURLです。

### SQL文の分割 {#sql-구문-분할기}

SQL文の分割には、JSON-RPCの[`sql.split`](#sqlsplit)メソッドを使用します。

### ライセンス情報 {#라이선스-정보}

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

### ライセンスのインストール {#라이선스-설치}

**POST `/web/api/license`**

ライセンスファイルをインストールします。

## WebSocket {#websocket}

```
ws://127.0.0.1:5654/web/api/console/{console_id}/data?token={jwt_token}
```

`console_id`には、セッションを正しく管理するため、クライアントアプリケーションが生成した一意の識別子を指定します。

このエンドポイントでは、HTTPの`Authorization`ヘッダーではなく、クエリパラメーター（`token={jwt_token}`）でJWTトークンを渡します。

このエンドポイントでは、サーバーとクライアントがJSONオブジェクトを交換し、構造化された安全な形式で通信します。

### PING {#ping}

クライアントは、現在時刻をUNIXエポック形式で含む*PING*メッセージを送信できます。
サーバーは同じペイロードを返すため、往復遅延時間を正確に測定できます。
この仕組みは、接続を維持し、アイドルタイムアウトを防ぐためにも役立ちます。

- 方向： C -> S

```json
{
    "type": "ping",
    "ping": {
        "tick": 1759127437000
    }
}
```

### LOG {#log}

サーバーは、ユーザー向けのメッセージで状態更新やエラーを通知します。
状態、問題、対処方法を明確に伝え、操作や問題解決を支援します。

- 方向： S -> C

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

- **timestamp**: ログの発生時刻。ナノ秒単位のUNIXエポック時刻です。
- **level**: ログの重要度。`"TRACE"`、`"DEBUG"`、`"INFO"`、`"WARN"`、`"ERROR"`のいずれかです。
- **task** (省略可能): 関連する処理の名前。
- **message**: 説明メッセージ。
- **repeat** (省略可能): 同じログメッセージが連続して繰り返された回数。重複出力を減らすために使用します。

## JSON-RPC {#json-rpc}

この節では、JSON-RPC仕様に従うWebSocketベースのリモートプロシージャ呼び出し（RPC）を説明します。
RPCでは、クライアントがサーバー側メソッドを呼び出して構造化された応答を受信でき、
クライアントアプリケーションとサーバーの通信・連携を容易にします。

Web UIは、管理機能用のJSON-RPCエンドポイントを提供します。

- HTTP POSTエンドポイント： `/web/api/rpc`
- WebSocketエンドポイント： `/web/api/console/:console_id/data?token={jwt_token}`

単純なリクエスト・レスポンス形式の呼び出しには、`/web/api/rpc`を推奨します。
コンソールセッションとともに双方向メッセージを処理する場合は、`/web/api/console/:console_id/data?token={jwt_token}`を使用できます。

### HTTP JSON-RPCのリクエスト形式 {#http-json-rpc-요청-형식}

**POST `/web/api/rpc`**

リクエストの例：

```json
{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "shell.list",
    "params": []
}
```

成功レスポンスの例：

```json
{
    "jsonrpc": "2.0",
    "id": 1,
    "result": []
}
```

エラーレスポンスの例：

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

注意：

- 応答のHTTPステータスは、通常は`200 OK`です。
- 成功したかどうかは、HTTPステータスではなく`error`フィールドの有無で判断してください。

### WebSocket JSON-RPCのリクエスト形式 {#websocket-json-rpc-요청-형식}

**`ws://{server_address}/web/api/console/:console_id/data?token={jwt_token}`**

WebSocketでは、`rpc_req`と`rpc_rsp`イベントを使用します。
`session`フィールドは、UIクライアントが応答を関連付けるタブやビューを識別するための値です。

**リクエスト**

- 方向： C -> S

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

**レスポンス**

- 方向： S -> C

**成功**

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

**エラー**

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

### Markdown {#markdown}

#### markdown.render {#markdownrender}

`markdown.render(markdown, darkMode, referer)`

*パラメーター*
- `markdown` *string*
- `darkMode` *bool*
- `referer` *string* - 参照元URL

*戻り値*

- `string|error`

<details>
<summary>リクエスト・レスポンスのJSON</summary>

*リクエスト*

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

*レスポンス*

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

### Vizspec {#vizspec}

#### vizspec.render {#vizspecrender}

`vizspec.render(vizspec)`

*パラメーター*
- `vizspec` *object*

*戻り値*

- `object|error`

<details>
<summary>リクエスト・レスポンスのJSON</summary>

*リクエスト*

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

*レスポンス*

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

#### vizspec.export {#vizspecexport}

`vizspec.export(vizspec, format)`

*パラメーター*
- `vizspec` *object*
- `format` *string*

*戻り値*

- `object|error`

<details>
<summary>リクエスト・レスポンスのJSON</summary>

*リクエスト*

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

*レスポンス*

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

### サーバー {#server}

#### server.info.get {#serverinfoget}

`server.info.get()`

*パラメーター*

- なし

*戻り値*

- `object<ServerInfoResponse>|error`

<details>
<summary>リクエスト・レスポンスのJSON</summary>

*リクエスト*

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

*レスポンス*

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

#### server.info.statz {#serverinfostatz}

`server.info.statz(names)`

*パラメーター*
- `names` *array<string>* - メトリクス名

*戻り値*

- `object<ServerStatzResponse>|error` - 名前ごとにグループ化した可視化仕様

<details>
<summary>リクエスト・レスポンスのJSON</summary>

*リクエスト*

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

*レスポンス*

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

#### server.info.query {#serverinfoquery}

`server.info.query(maxRows, pattern)`

*パラメーター*
- `maxRows` *int* - 最大行数
- `pattern` *array<string>* - メトリクスキーのワイルドカードフィルター

*戻り値*

- `object<StatzQueryResult>|error` - 表形式のメトリクスクエリ結果

<details>
<summary>リクエスト・レスポンスのJSON</summary>

*リクエスト*

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

*レスポンス*

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

#### server.info.keys {#serverinfokeys}

`server.info.keys(pattern)`

*パラメーター*
- `pattern` *array<string>* - メトリクスキーのワイルドカードフィルター

*戻り値*

- `array<string>|error` - ソート済みのメトリクスキー名

<details>
<summary>リクエスト・レスポンスのJSON</summary>

*リクエスト*

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

*レスポンス*

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

#### server.certificate.get {#servercertificateget}

`server.certificate.get()`

*パラメーター*

- なし

*戻り値*

- `string|error`

<details>
<summary>リクエスト・レスポンスのJSON</summary>

*リクエスト*

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

*レスポンス*

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

#### server.shutdown {#servershutdown}

管理（mgmt）サーバーが実装します。

`server.shutdown()`

*パラメーター*

- なし

*戻り値*

- `object<ShutdownResponse>|error`

<details>
<summary>リクエスト・レスポンスのJSON</summary>

*リクエスト*

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

*レスポンス*

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

### サービス {#service}

#### service.port.list {#serviceportlist}

`service.port.list(svc)`

*パラメーター*
- `svc` *string*

*戻り値*

- `array<object<model.ServicePort>>|error`

<details>
<summary>リクエスト・レスポンスのJSON</summary>

*リクエスト*

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

*レスポンス*

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

### プロキシ {#proxy}

#### proxy.register {#proxyregister}

`proxy.register(req)`

*パラメーター*
- `req` *object<ProxyRegisterRequest>*

*戻り値*

- `object<ProxyEntrySnapshot>|error`

<details>
<summary>リクエスト・レスポンスのJSON</summary>

*リクエスト*

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

*レスポンス*

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

#### proxy.unregister {#proxyunregister}

`proxy.unregister(req)`

*パラメーター*
- `req` *object<ProxyUnregisterRequest>*

*戻り値*

- `array<object<ProxyEntrySnapshot>>|error`

<details>
<summary>リクエスト・レスポンスのJSON</summary>

*リクエスト*

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

*レスポンス*

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

#### proxy.list {#proxylist}

`proxy.list(service)`

*パラメーター*
- `service` *string*

*戻り値*

- `array<object<ProxyEntrySnapshot>>|error`

<details>
<summary>リクエスト・レスポンスのJSON</summary>

*リクエスト*

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

*レスポンス*

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

#### proxy.get {#proxyget}

`proxy.get(req)`

*パラメーター*
- `req` *object<ProxyGetRequest>*

*戻り値*

- `object<ProxyEntrySnapshot>|error`

<details>
<summary>リクエスト・レスポンスのJSON</summary>

*リクエスト*

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

*レスポンス*

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

### シェル {#shell}

#### shell.list {#shelllist}

`shell.list()`

*パラメーター*

- なし

*戻り値*

- `array<object<model.ShellDefinition>>|error`

<details>
<summary>リクエスト・レスポンスのJSON</summary>

*リクエスト*

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

*レスポンス*

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

#### shell.add {#shelladd}

`shell.add(name, command)`

*パラメーター*
- `name` *string*
- `command` *string*

*戻り値*

- `string|error`

<details>
<summary>リクエスト・レスポンスのJSON</summary>

*リクエスト*

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

*レスポンス*

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

#### shell.copy {#shellcopy}

指定したシェル定義を複製し、新しいIDが割り当てられたシェル定義を返します。

`shell.copy(srcId)`

*パラメーター*
- `srcId` *string* - 複製するシェル定義のID

*戻り値*

- `object<model.ShellDefinition>|error` - 複製されたシェル定義

<details>
<summary>リクエスト・レスポンスのJSON</summary>

*リクエスト*

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

*レスポンス*

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

#### shell.update {#shellupdate}

シェル定義を変更します。対象は`id`で指定し、シェル定義全体を渡します。

`shell.update(shell)`

*パラメーター*
- `shell` *object<model.ShellDefinition>* - `id`、`type`、`label`、`command`、`icon`、`theme`、`attributes`を含むシェル定義
    `command`が空の場合はエラーを返します

*戻り値*

- `object<model.ShellDefinition>|error` - 変更後のシェル定義

<details>
<summary>リクエスト・レスポンスのJSON</summary>

*リクエスト*

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

*レスポンス*

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

#### shell.delete {#shelldelete}

`shell.delete(id)`

*パラメーター*
- `id` *string*

*戻り値*

- `null|error`

<details>
<summary>リクエスト・レスポンスのJSON</summary>

*リクエスト*

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

*レスポンス*

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

### ブリッジ {#bridge}

#### bridge.list {#bridgelist}

`bridge.list()`

*パラメーター*

- なし

*戻り値*

- `array<object<bridge.BridgeInfo>>|error`

<details>
<summary>リクエスト・レスポンスのJSON</summary>

*リクエスト*

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

*レスポンス*

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

#### bridge.get {#bridgeget}

`bridge.get(name)`

*パラメーター*
- `name` *string*

*戻り値*

- `object<bridge.BridgeInfo>|error`

<details>
<summary>リクエスト・レスポンスのJSON</summary>

*リクエスト*

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

*レスポンス*

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

#### bridge.add {#bridgeadd}

`bridge.add(name, typ, conn)`

*パラメーター*
- `name` *string*
- `typ` *string*
- `conn` *string*

*戻り値*

- `null|error`

<details>
<summary>リクエスト・レスポンスのJSON</summary>

*リクエスト*

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

*レスポンス*

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

#### bridge.delete {#bridgedelete}

`bridge.delete(name)`

*パラメーター*
- `name` *string*

*戻り値*

- `null|error`

<details>
<summary>リクエスト・レスポンスのJSON</summary>

*リクエスト*

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

*レスポンス*

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

#### bridge.test {#bridgetest}

`bridge.test(name)`

*パラメーター*
- `name` *string*

*戻り値*

- `bool|error`

<details>
<summary>リクエスト・レスポンスのJSON</summary>

*リクエスト*

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

*レスポンス*

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

#### bridge.stats {#bridgestats}

`bridge.stats(name)`

*パラメーター*
- `name` *string*

*戻り値*

- `object<BridgeStats>|error`

<details>
<summary>リクエスト・レスポンスのJSON</summary>

*リクエスト*

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

*レスポンス*

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

#### bridge.exec {#bridgeexec}

`bridge.exec(name, command)`

*パラメーター*
- `name` *string*
- `command` *string*

*戻り値*

- `object<BridgeExecResult>|error`

<details>
<summary>リクエスト・レスポンスのJSON</summary>

*リクエスト*

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

*レスポンス*

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

#### bridge.query {#bridgequery}

`bridge.query(name, query)`

*パラメーター*
- `name` *string*
- `query` *string*

*戻り値*

- `object<BridgeQueryResult>|error`

<details>
<summary>リクエスト・レスポンスのJSON</summary>

*リクエスト*

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

*レスポンス*

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

#### bridge.result.fetch {#bridgeresultfetch}

`bridge.result.fetch(handle)`

*パラメーター*
- `handle` *string*

*戻り値*

- `object<BridgeQueryRow>|error`

<details>
<summary>リクエスト・レスポンスのJSON</summary>

*リクエスト*

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

*レスポンス*

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

#### bridge.result.close {#bridgeresultclose}

`bridge.result.close(handle)`

*パラメーター*
- `handle` *string*

*戻り値*

- `null|error`

<details>
<summary>リクエスト・レスポンスのJSON</summary>

*リクエスト*

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

*レスポンス*

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

### SSHキー {#sshkey}

#### sshkey.list {#sshkeylist}

`sshkey.list()`

*パラメーター*

- なし

*戻り値*

- `array<object<AuthorizedSshKey>>|error`

<details>
<summary>リクエスト・レスポンスのJSON</summary>

*リクエスト*

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

*レスポンス*

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

#### sshkey.add {#sshkeyadd}

`sshkey.add(keyType, key, comment)`

*パラメーター*
- `keyType` *string*
- `key` *string*
- `comment` *string*

*戻り値*

- `null|error`

<details>
<summary>リクエスト・レスポンスのJSON</summary>

*リクエスト*

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

*レスポンス*

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

#### sshkey.delete {#sshkeydelete}

`sshkey.delete(key)`

*パラメーター*
- `key` *string*

*戻り値*

- `null|error`

<details>
<summary>リクエスト・レスポンスのJSON</summary>

*リクエスト*

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

*レスポンス*

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

### キー {#key}

#### key.list {#keylist}

`key.list()`

*パラメーター*

- なし

*戻り値*

- `array<object<KeyInfo>>|error` - サーバーのキーストアに保存されたキーの一覧
    - `idx`：一覧内の順番
    - `id`：キーID。`key.delete`に指定します
    - `name`：キー名
    - `notBefore`、`notAfter`：有効期間の開始時刻と終了時刻（Unixタイムスタンプ、秒）

<details>
<summary>リクエスト・レスポンスのJSON</summary>

*リクエスト*

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

*レスポンス*

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

#### key.generate {#keygenerate}

`key.generate(name, typ, notBefore, notAfter, store)`

*パラメーター*
- `name` *string* - キー名。小文字に変換して保存されます
- `typ` *string* - 生成するキーの種類。`RSA`または`ECDSA`を指定する必要があります
- `notBefore` *int64* - キーの有効期間の開始時刻（Unixタイムスタンプ、秒）
    省略または0の場合は、現在時刻を使用します
- `notAfter` *int64* - キーの有効期間の終了時刻（Unixタイムスタンプ、秒）
    省略または0の場合は、既定の10年間を使用します
- `store` *bool* - キーペアをサーバーのキーストアに保存するかどうか
    `false`の場合は保存しないため、`key.list`にも表示されません

*戻り値*

- `any|error` - 生成したキー情報
    - `id`：キーID。`store`がfalseの場合は`0`です
    - `name`：キー名
    - `certificate`：キーペアの証明書
    - `key`：キーペアの秘密鍵
    - `serverKey`：サーバー証明書（`store`がtrueの場合）
    - `zip`：キーペアとサーバー証明書を含むZIPアーカイブをbase64でエンコードした文字列（`store`がtrueの場合）

<details>
<summary>リクエスト・レスポンスのJSON</summary>

*リクエスト*

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

*レスポンス*

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

#### key.delete {#keydelete}

`key.delete(id)`

*パラメーター*
- `id` *int64* - `key.list`または`key.generate`が返したキーID

*戻り値*

- `null|error`

<details>
<summary>リクエスト・レスポンスのJSON</summary>

*リクエスト*

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

*レスポンス*

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

### トークン {#token}

発行したトークンの使い方は、[APIセキュリティ](/neo/security/)を参照してください。

#### token.list {#tokenlist}

`token.list()`

*パラメーター*

- なし

*戻り値*

- `array<object<ApiTokenInfo>>|error` - 呼び出したユーザーのAPIトークン一覧
    - `id`：トークンID。`token.delete`に指定します
    - `name`：トークン名
    - `user`：トークンを所有するユーザー
    - `hint`：一部を伏せたトークン値
    - `createdAt`：発行時刻（Unixタイムスタンプ、秒）
    - `notAfter`：有効期限（Unixタイムスタンプ、秒）
    - `lastUsedAt`：最後に使用した時刻（Unixタイムスタンプ、秒）。一度も使用していない場合は省略されます

<details>
<summary>リクエスト・レスポンスのJSON</summary>

*リクエスト*

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

*レスポンス*

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

#### token.generate {#tokengenerate}

`token.generate(name, notAfter)`

*パラメーター*
- `name` *string* - トークン名。空の場合はエラーを返します
- `notAfter` *int64* - 有効期限（Unixタイムスタンプ、秒）
    0の場合は、発行から10年後に設定します

*戻り値*

- `object<GeneratedApiToken>|error` - `token.list`の項目と同じフィールドに、トークンの原文である`token`が加わります
    トークンの原文は、このレスポンスでしか受け取れません

<details>
<summary>リクエスト・レスポンスのJSON</summary>

*リクエスト*

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

*レスポンス*

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

#### token.delete {#tokendelete}

`token.delete(id)`

*パラメーター*
- `id` *int64* - `token.list`または`token.generate`が返したトークンID

*戻り値*

- `null|error`

<details>
<summary>リクエスト・レスポンスのJSON</summary>

*リクエスト*

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

*レスポンス*

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

### タイマー {#timer}

タイマーは、`timer.list`または`timer.add`が返すIDで指定します。同じ名前で追加しても、新しいIDで登録されます。実行周期の書式は[タイマー](/neo/timer/)を参照してください。

#### timer.list {#timerlist}

`timer.list()`

*パラメーター*

- なし

*戻り値*

- `array<object<timer.Info>>|error` - タイマー一覧
    - `id`：タイマーID
    - `userName`、`execUser`：タイマーを所有するユーザーと実行するユーザー
    - `name`：タイマー名
    - `autoStart`：自動起動するかどうか。`false`の場合は省略されます
    - `state`：`RUNNING`、`STARTING`、`STOP`、`STOPPING`、`FAILED`、`UNKNOWN`のいずれか
    - `task`：実行するTQLファイルのパス
    - `schedule`：実行周期

<details>
<summary>リクエスト・レスポンスのJSON</summary>

*リクエスト*

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

*レスポンス*

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

#### timer.get {#timerget}

`timer.get(id)`

*パラメーター*
- `id` *int64* - タイマーID

*戻り値*

- `object<timer.Info>|error` - タイマー情報。フィールドは`timer.list`と同じです

<details>
<summary>リクエスト・レスポンスのJSON</summary>

*リクエスト*

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

*レスポンス*

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

#### timer.add {#timeradd}

`timer.add(req)`

*パラメーター*
- `req` *object*
    - `name` *string* - タイマー名。大文字に変換して保存されます
    - `spec` *string* - 実行周期。例：`0 30 * * * *`（毎時30分）、`@every 1h30m`（1時間30分ごと）、`@daily`（毎日）
    - `command` *string* - 実行するTQLファイルのパス。ファイルが存在しない場合はエラーを返します
    - `autoStart` *bool* - `true`の場合は追加と同時に開始し、machbase-neoの起動時にも自動で開始します

*戻り値*

- `int64|error` - 作成したタイマーのID

<details>
<summary>リクエスト・レスポンスのJSON</summary>

*リクエスト*

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

*レスポンス*

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

#### timer.update {#timerupdate}

`id`で指定したタイマーの設定を、リクエストの内容に置き換えます。

`timer.update(req)`

*パラメーター*
- `req` *object*
    - `id` *int64* - タイマーID
    - `spec` *string* - 実行周期
    - `command` *string* - 実行するTQLファイルのパス。省略するとエラーを返します
    - `autoStart` *bool* - 自動起動するかどうか。省略すると`false`になります

*戻り値*

- `null|error`

<details>
<summary>リクエスト・レスポンスのJSON</summary>

*リクエスト*

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

*レスポンス*

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

#### timer.delete {#timerdelete}

`timer.delete(id)`

*パラメーター*
- `id` *int64* - タイマーID

*戻り値*

- `null|error`

<details>
<summary>リクエスト・レスポンスのJSON</summary>

*リクエスト*

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

*レスポンス*

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

#### timer.start {#timerstart}

`timer.start(id)`

*パラメーター*
- `id` *int64* - タイマーID

*戻り値*

- `null|error`

<details>
<summary>リクエスト・レスポンスのJSON</summary>

*リクエスト*

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

*レスポンス*

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

#### timer.stop {#timerstop}

`timer.stop(id)`

*パラメーター*
- `id` *int64* - タイマーID

*戻り値*

- `null|error`

<details>
<summary>リクエスト・レスポンスのJSON</summary>

*リクエスト*

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

*レスポンス*

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

### サブスクライバー {#subscriber}

サブスクライバーは、`subscriber.list`または`subscriber.add`が返すIDで指定します。ブリッジの設定は、[MQTTブリッジ](/neo/bridges/mqtt/)と[NATSブリッジ](/neo/bridges/nats/)を参照してください。

#### subscriber.list {#subscriberlist}

`subscriber.list()`

*パラメーター*

- なし

*戻り値*

- `array<object<subscriber.Info>>|error` - サブスクライバー一覧
    - `id`：サブスクライバーID
    - `userName`、`execUser`：サブスクライバーを所有するユーザーと実行するユーザー
    - `name`：サブスクライバー名
    - `autoStart`：自動起動するかどうか
    - `state`：`RUNNING`、`STARTING`、`STOP`、`STOPPING`、`FAILED`、`UNKNOWN`のいずれか
    - `task`：書き込み記述子
    - `bridge`：ブリッジ名
    - `topic`：購読するMQTTトピックまたはNATSサブジェクト
    - `qos`、`queue`、`stream`：ブリッジのオプション
    - `autoStart`、`qos`、`queue`、`stream`フィールドは、値がない場合は省略されます

<details>
<summary>リクエスト・レスポンスのJSON</summary>

*リクエスト*

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

*レスポンス*

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

#### subscriber.get {#subscriberget}

`subscriber.get(id)`

*パラメーター*
- `id` *int64* - サブスクライバーID

*戻り値*

- `object<subscriber.Info>|error` - サブスクライバー情報。フィールドは`subscriber.list`と同じです

<details>
<summary>リクエスト・レスポンスのJSON</summary>

*リクエスト*

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

*レスポンス*

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

#### subscriber.add {#subscriberadd}

`subscriber.add(req)`

*パラメーター*
- `req` *object*
    - `name` *string* - サブスクライバー名。大文字に変換して保存されます
    - `bridge` *string* - サブスクライバーが使用するブリッジ名
    - `command` *string* - 例：`db/append/EXAMPLE:csv`。書き込み記述子です。この例は、CSV形式で受信したデータを`EXAMPLE`テーブルにappendモードで書き込むことを表します
    - `autoStart` *bool* - `true`にすると、machbase-neoとともにサブスクライバーも起動します
    - `mqtt` *object* - MQTTブリッジのオプション
        - `topic` *string* - 購読するトピック
        - `qos` *int* - トピック購読のQoSレベル。`0`と`1`に対応し、既定値は`0`です
    - `nats` *object* - NATSブリッジのオプション
        - `subject` *string* - 購読するサブジェクト
        - `queue` *string* - キューグループ
        - `stream` *string* - ストリーム名
- `name`、`bridge`、`command`とトピック（`mqtt.topic`または`nats.subject`）は必須です。
- `mqtt`と`nats`は同時に指定できません。

*戻り値*

- `int64|error` - 作成したサブスクライバーのID

<details>
<summary>リクエスト・レスポンスのJSON</summary>

*リクエスト*

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

*レスポンス*

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

#### subscriber.update {#subscriberupdate}

`id`で指定したサブスクライバーの設定を、リクエストの内容に置き換えます。

`subscriber.update(req)`

*パラメーター*
- `req` *object*
    - `id` *int64* - サブスクライバーID
    - `bridge`、`command`、`autoStart`、`mqtt`、`nats` - `subscriber.add`と同じです

*戻り値*

- `null|error`

<details>
<summary>リクエスト・レスポンスのJSON</summary>

*リクエスト*

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

*レスポンス*

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

#### subscriber.delete {#subscriberdelete}

`subscriber.delete(id)`

*パラメーター*
- `id` *int64* - サブスクライバーID

*戻り値*

- `null|error`

<details>
<summary>リクエスト・レスポンスのJSON</summary>

*リクエスト*

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

*レスポンス*

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

#### subscriber.start {#subscriberstart}

`subscriber.start(id)`

*パラメーター*
- `id` *int64* - サブスクライバーID

*戻り値*

- `null|error`

<details>
<summary>リクエスト・レスポンスのJSON</summary>

*リクエスト*

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

*レスポンス*

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

#### subscriber.stop {#subscriberstop}

`subscriber.stop(id)`

*パラメーター*
- `id` *int64* - サブスクライバーID

*戻り値*

- `null|error`

<details>
<summary>リクエスト・レスポンスのJSON</summary>

*リクエスト*

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

*レスポンス*

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

### HTTP {#http}

#### http.debug.set {#httpdebugset}

`http.debug.set(m)`

*パラメーター*
- `m` *object* - `enable`と`logLatency`キーを持つデバッグ設定マップ

*戻り値*

- `object|error`

<details>
<summary>リクエスト・レスポンスのJSON</summary>

*リクエスト*

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

*レスポンス*

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

#### http.split {#httpsplit}

`http.split(content)`

*パラメーター*
- `content` *string* - HTTPスクリプトのテキスト

*戻り値*

- `array<object<util.HttpStatement>>|error` - 解析したHTTP文の配列

<details>
<summary>リクエスト・レスポンスのJSON</summary>

*リクエスト*

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

*レスポンス*

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

### セッション {#session}

#### session.list {#sessionlist}

`session.list()`

*パラメーター*

- なし

*戻り値*

- `array<object<Session>>|error`

<details>
<summary>リクエスト・レスポンスのJSON</summary>

*リクエスト*

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

*レスポンス*

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

#### session.kill {#sessionkill}

`session.kill(id, force)`

*パラメーター*
- `id` *string*
- `force` *bool*

*戻り値*

- `null|error`

<details>
<summary>リクエスト・レスポンスのJSON</summary>

*リクエスト*

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

*レスポンス*

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

#### session.stat {#sessionstat}

`session.stat(reset)`

*パラメーター*
- `reset` *bool*

*戻り値*

- `object<server_api.Statz>|error`

<details>
<summary>リクエスト・レスポンスのJSON</summary>

*リクエスト*

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

*レスポンス*

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

#### session.limit.get {#sessionlimitget}

`session.limit.get()`

*パラメーター*

- なし

*戻り値*

- `object<SessionLimit>|error`

<details>
<summary>リクエスト・レスポンスのJSON</summary>

*リクエスト*

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

*レスポンス*

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

#### session.limit.set {#sessionlimitset}

`session.limit.set(m)`

*パラメーター*
- `m` *object*

*戻り値*

- `null|error`

<details>
<summary>リクエスト・レスポンスのJSON</summary>

*リクエスト*

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

*レスポンス*

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

### SQL {#sql}

#### sql.split {#sqlsplit}

`sql.split(content)`

*パラメーター*
- `content` *string*

*戻り値*

- `array<object<util.SqlStatement>>|error`

<details>
<summary>リクエスト・レスポンスのJSON</summary>

*リクエスト*

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

*レスポンス*

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

### LSP {#lsp}

#### lsp.diagnostics {#lspdiagnostics}

`lsp.diagnostics(req)`

*パラメーター*
- `req` *object<lspDocumentRequest>*

*戻り値*

- `object|error`

<details>
<summary>リクエスト・レスポンスのJSON</summary>

*リクエスト*

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

*レスポンス*

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

#### lsp.completion {#lspcompletion}

`lsp.completion(req)`

*パラメーター*
- `req` *object<lspDocumentRequest>*

*戻り値*

- `object|error`

<details>
<summary>リクエスト・レスポンスのJSON</summary>

*リクエスト*

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

*レスポンス*

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

#### lsp.hover {#lsphover}

`lsp.hover(req)`

*パラメーター*
- `req` *object<lspDocumentRequest>*

*戻り値*

- `object|error`

<details>
<summary>リクエスト・レスポンスのJSON</summary>

*リクエスト*

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

*レスポンス*

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

#### lsp.signature {#lspsignature}

`lsp.signature(req)`

*パラメーター*
- `req` *object<lspDocumentRequest>*

*戻り値*

- `object|error`

<details>
<summary>リクエスト・レスポンスのJSON</summary>

*リクエスト*

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

*レスポンス*

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

#### lsp.metadata {#lspmetadata}

`lsp.metadata(req)`

*パラメーター*
- `req` *object<lspMetadataRequest>*

*戻り値*

- `object|error`

<details>
<summary>リクエスト・レスポンスのJSON</summary>

*リクエスト*

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

*レスポンス*

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

