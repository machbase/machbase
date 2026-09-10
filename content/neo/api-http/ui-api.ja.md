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
{{< tab name="リクエスト" >}}
```json
{
    "loginName": "sys",
    "password": "manager"
}
```
{{< /tab >}}
{{< tab name="レスポンス" >}}
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
{{< tab name="リクエスト" >}}
```json
{
    "refreshToken": "login時に発行されたリフレッシュトークン"
}
```
{{< /tab >}}
{{< tab name="レスポンス" >}}
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
    "refreshToken": "login時に発行されたリフレッシュトークン"
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
    "id": "シェル定義ID（uuid）",
    "type": "種類",
    "icon": "アイコン名",
    "label": "表示名",
    "theme": "テーマ名",
    "command": "ターミナル シェルコマンド",
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

`/db/query` APIと同じ動作ですが、認証方式が異なります。
`/db/query`はクライアントアプリケーションをAPIトークンで認証し、
`/web/machbase`はユーザー操作用にJWTを検証します。

### テーブル一覧の取得 {#테이블-목록-조회}

**GET `/web/api/tables?showall=false&name=pattern`**

テーブル一覧を返します。

- `showall`を`true`にすると、非表示のテーブルもすべて含めます。
- `name`はテーブル名の絞り込みパターンです。`?`や`*`を含むglob式、または特殊文字を含まない接頭辞を指定できます。

```json
{
    "success": true,
    "reason": "成功状態またはメッセージ",
    "elapse": "文字列形式の経過時間",
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
    "reason": "成功状態またはメッセージ",
    "elapse": "文字列形式の経過時間",
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
    "reason": "成功状態またはメッセージ",
    "elapse": "文字列形式の経過時間",
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

## シェルとターミナル {#셸-및-터미널}

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

### シェル定義の取得 {#셸-정의-조회}

**GET `/web/api/shell/:id`**

指定IDの`ShellDefinition`を返します。

### シェル定義の変更 {#셸-정의-수정}

**POST `/web/api/shell/:id`**

指定IDの`ShellDefinition`を更新します。

### シェルの複製 {#셸-복제}

**GET `/web/api/shell/:id/copy`**

指定IDのシェルを複製し、新しい`ShellDefinition`を返します。

### シェル定義の削除  {#셸-정의-삭제-}

**DELETE `/web/api/shell/:id`**

指定IDのシェルを削除します。

```json
{
    "success": true,
    "reason": "成功またはエラーメッセージ",
    "elapse": "文字列形式の時間"
}
```

## サーバーイベント {#서버-이벤트}

### イベントチャネル {#이벤트-채널}

**`ws://127.0.0.1:5654/web/api/console/{console_id}/data?token={jwt_token}`**

双方向メッセージ用のWebSocketです。

- メッセージの種類

```json
{
    "type": "下表を参照",
    "ping": {
        "tick": 1234
    },
    "log": {
        "level": "INFO",
        "message": "ログメッセージ"
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

**POST `/web/api/md`**

ボディにMarkdownを送信すると、サーバーがXHTML形式のレンダリング結果を返します。

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
    "content": "ファイルの場合のバイト配列",
    "children": [{"ディレクトリの場合のSubEntry"}],
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

### キー一覧の取得 {#키-목록-조회}

**GET `/web/api/keys`**

キー情報を返します。

レスポンス

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
### キーの生成 {#키-생성}

**POST `/web/api/keys`**

キーを生成します。
- `name`は必須です。
- `notAfter`は有効期限です。

{{< tabs >}}
{{< tab name="リクエスト" >}}
```json
{
    "name": "eleven",
    "notBefore": 0,
    "notAfter": 0
}
```
{{< /tab >}}
{{< tab name="レスポンス" >}}
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



### キーの削除 {#키-삭제}

**DELETE `/web/api/keys/:id`**

指定IDのキーを削除します。

レスポンス

```json
{
    "success": true,
    "reason": "success",
    "elapse": "112.8µs"
}
```

## SSHキー {#ssh-키}

### SSHキー一覧の取得 {#ssh-키-목록-조회}

**GET `/web/api/sshkeys`**

SSHキー情報を返します。

レスポンス

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
### SSHキーの生成 {#ssh-키-생성}

**POST `/web/api/sshkeys`**

**SSH公開鍵認証の使用**

machbase-neoサーバーに公開鍵を登録すると、パスワードを入力せずに`machbase-neo shell`コマンドを実行できます。

{{< tabs >}}
{{< tab name="リクエスト" >}}
```json
{
    "key": "your publickey"
}
```
{{< /tab >}}
{{< tab name="レスポンス" >}}
```json
{
    "elapse": "138.801µs",
    "reason": "success",
    "success": true
}
```
{{< /tab >}}
{{< /tabs >}}



### SSHキーの削除 {#ssh-키-삭제}

**DELETE `/web/api/sshkeys/:fingerprint`**

指定したフィンガープリントのSSHキーを削除します。

レスポンス
```json
{
    "elapse": "198.8µs",
    "reason": "success",
    "success": true
}
```



## タイマー {#타이머}

### タイマーの取得 {#타이머-조회}

**GET `/web/api/timers/:name`**

タイマー情報を返します。

- 状態値： `RUNNING`, `STARTING`, `STOP`, `STOPPING`, `FAILED`, `UNKNOWN`

レスポンス

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

### タイマー一覧 {#타이머-목록}

**GET `/web/api/timers`**

タイマー情報の一覧を返します。
- 状態値： `RUNNING`, `STARTING`, `STOP`, `STOPPING`, `FAILED`, `UNKNOWN`

レスポンス

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
### タイマーの追加 {#타이머-추가}

**POST `/web/api/timers`**

タイマーを追加します。
- `name`、`autoStart`、`schedule`、`path`は必須です。

タイマーの`schedule`の例
- `0 30 * * * *`           毎時30分
- `@every 1h30m`           1時間30分間隔
- `@daily`                 毎日

{{< tabs >}}
{{< tab name="リクエスト" >}}
```json
{
    "name":"eleven",
    "autoStart":false,
    "schedule":"@every 10s",
    "path":"timer.tql"
}
```
{{< /tab >}}
{{< tab name="レスポンス" >}}
```json
{
    "success": true,
    "reason": "success",
    "elapse": "4.9658ms"
}
```
{{< /tab >}}
{{< /tabs >}}

### タイマーの開始 {#타이머-시작}

**POST `/web/api/timers/:name/state`**

タイマーを開始します。
- `state`値が必要です。

{{< tabs >}}
{{< tab name="リクエスト" >}}
```json
{
    "state":"start",
}
```
{{< /tab >}}
{{< tab name="レスポンス" >}}
```json
{
    "success": true,
    "reason": "success",
    "elapse": "822.601µs"
}
```
{{< /tab >}}
{{< /tabs >}}

### タイマーの停止 {#타이머-중지}

**POST `/web/api/timers/:name/state`**

タイマーを停止します。
- `state`値が必要です。

{{< tabs >}}
{{< tab name="リクエスト" >}}
```json
{
    "state":"stop",
}
```
{{< /tab >}}
{{< tab name="レスポンス" >}}
```json
{
    "success": true,
    "reason": "success",
    "elapse": "26.2µs"
}
```
{{< /tab >}}
{{< /tabs >}}

### タイマーの変更 {#타이머-수정}

**PUT `/web/api/timers/:name`**

タイマー設定を変更します。
- `autoStart`、`schedule`、`path`を指定できます。

{{< tabs >}}
{{< tab name="リクエスト" >}}
```json
{
    "audoStart" : true,
    "schedule":"@every 5s",
    "path":"timer.tql"
}
```
{{< /tab >}}
{{< tab name="レスポンス" >}}
```json
{
    "elapse": "459.6µs",
    "reason": "success",
    "success": true
}
```
{{< /tab >}}
{{< /tabs >}}



### タイマーの削除 {#타이머-삭제}

**DELETE `/web/api/timers/:name`**

タイマーを削除します。

レスポンス
```json
{
    "success": true,
    "reason": "success",
    "elapse": "4.8664ms"
}
```


## ブリッジ {#브리지}

### ブリッジ一覧 {#브리지-목록}

**GET `/web/api/bridges`**

ブリッジ情報を返します。

レスポンス

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
### ブリッジの追加 {#브리지-추가}

**POST `/web/api/bridges`**

ブリッジを追加します。
- `name`、`type`、`path`は必須です。
- 対応するブリッジは、`SQLite`、`PostgreSql`、`Mysql`、`MSSQL`、`MQTT`、`NATS`です。

{{< tabs >}}
{{< tab name="リクエスト" >}}
```json
{
    "name":"pg",
    "type":"postgres", // sqlite、postgres、mysql、mssql、mqtt、natsから選択
    "path":"host=127.0.0.1 port=5432 user=postgres password=1234 dbname=bridgedb sslmode=disable"
}
```
{{< /tab >}}
{{< tab name="レスポンス" >}}
```json
{
    "success": true,
    "reason": "success",
    "elapse": "193.499µs"
}
```
{{< /tab >}}
{{< /tabs >}}

### ブリッジの実行 {#브리지-실행}

**POST `/web/api/bridges/:name/state`**

ブリッジでコマンドを実行します。
- `state`と`command`が必要です。

{{< tabs >}}
{{< tab name="リクエスト" >}}
```json
{
    "state":"exec",
    "command":"CREATE TABLE IF NOT EXISTS pg_example(id SERIAL PRIMARY KEY,company VARCHAR(50) UNIQUE NOT NULL,employee  INT,discount REAL,plan FLOAT(8),code UUID,valid BOOL, memo TEXT, created_on TIMESTAMP NOT NULL)"
}
```
{{< /tab >}}
{{< tab name="レスポンス" >}}
```json
{
    "success": true,
    "reason": "success",
    "elapse": "217.4µs"
}
```
{{< /tab >}}
{{< /tabs >}}

### ブリッジのクエリ {#브리지-쿼리}

**POST `/web/api/bridges/:name/state`**

ブリッジでクエリを実行します。
- `state`と`command`が必要です。

{{< tabs >}}
{{< tab name="リクエスト" >}}
```json
{
    "state":"query",
    "command":"select * from pg_example"
}
```
{{< /tab >}}
{{< tab name="レスポンス" >}}
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

### ブリッジのテスト {#브리지-테스트}

**POST `/web/api/bridges/:name/state`**

ブリッジをテストします。

{{< tabs >}}
{{< tab name="リクエスト" >}}
```json
{
    "state":"test",
}
```
{{< /tab >}}
{{< tab name="レスポンス" >}}
```json
{
    "success": true,
    "reason": "success",
    "elapse": "331.1µs"
}
```
{{< /tab >}}
{{< /tabs >}}


### ブリッジの削除 {#브리지-삭제}

**DELETE `/web/api/bridges/:name`**

指定名のブリッジを削除します。

レスポンス

```json
{
    "success": true,
    "reason": "success",
    "elapse": "112.8µs"
}
```

## サブスクライバー {#구독자}

### サブスクライバーの取得 {#구독자-조회}

**GET `/web/api/subscribers/:name`**

サブスクライバー情報を返します。
- 状態値： `RUNNING`, `STARTING`, `STOP`, `STOPPING`, `FAILED`, `UNKNOWN`
- `autoStart`、`queue`、`QoS`フィールドは、値がない場合は省略されます。

レスポンス

```json
{
    "data": [
        {
            "name": "NATS_SUBR",
            "type": "SUBSCRIBER",
            "autoStart": true,  // 値がなければ省略
            "state": "RUNNING", 
            "task": "db/append/EXAMPLE:csv",
            "bridge": "my_nats",
            "topic": "iot.sensor",
            "queue":"", // 値がなければ省略
            "QoS":0    // 値がなければ省略
        }
    ],
    "elapse": "253.4µs",
    "reason": "success",
    "success": true
}
```

### サブスクライバー一覧 {#구독자-목록}

**GET `/web/api/subscribers`**

サブスクライバー情報の一覧を返します。
- 状態値： `RUNNING`, `STARTING`, `STOP`, `STOPPING`, `FAILED`, `UNKNOWN`
- `autoStart`、`queue`、`QoS`フィールドは、値がない場合は省略されます。

レスポンス

```json
{
    "data": [
        {
            "name": "NATS_SUBR",
            "type": "SUBSCRIBER",
            "autoStart": true,  // 値がなければ省略
            "state": "RUNNING",
            "task": "db/append/EXAMPLE:csv",
            "bridge": "my_nats",
            "topic": "iot.sensor",
            "queue":"", // 値がなければ省略
            "QoS":0    // 値がなければ省略
        },
        {
            "name": "NATS_SUBR2",
            "type": "SUBSCRIBER",
            "autoStart": true,  // 値がなければ省略
            "state": "STARTING",
            "task": "db/insert/EXAMPLE2:csv",
            "bridge": "my_nats2",
            "topic": "iot.sensor2",
            "queue":"", // 値がなければ省略
            "QoS":0    // 値がなければ省略
        }
    ],
    "elapse": "253.4µs",
    "reason": "success",
    "success": true
}
```
### サブスクライバーの追加 {#구독자-추가}

**POST `/web/api/subscribers`**

サブスクライバーを追加します。
- `autoStart`：`true`にすると、machbase-neoとともに起動します。省略または`false`の場合は、手動で開始・停止できます。
- `name`: 例：`nats_subr`。サブスクライバー名です。
- `bridge`: 例：`my_nats`。サブスクライバーが使用するブリッジ名です。
- `topic`: 例：`iot.sensor`。購読対象で、NATSのサブジェクト構文に従います。
- `task`: 例：`db/append/EXAMPLE:csv`。データ形式と書き込みモードを指定し、CSVデータをEXAMPLEテーブルにappendモードで取り込むことを表します。
- `autoStart`がfalseの場合は、`subscriber start <name>`、`subscriber stop <name>`コマンドで手動操作できます。
- `QoS` `int`: MQTTブリッジの場合、トピック購読のQoSを指定します。0または1を使用でき、既定値は0です。
- `quque` `string`：NATSブリッジのキューグループを指定します。現在のリクエストのJSONキーは`quque`です。レスポンスでは`queue`を使用します。

設定の詳細は、[NATSブリッジ](/neo/bridges/nats/)を参照してください。

{{< tabs >}}
{{< tab name="リクエスト" >}}
```json
{
    "name":"nats_subr",
    "autoStart":true,
    "bridge":"my_nats",
    "topic":"iot.sensor",
    "task":"db/append/EXAMPLE:csv",
    "QoS": 0,  // MQTTブリッジオプション：0または1（既定値0）
    "quque": "" // NATSブリッジオプション
}
```
{{< /tab >}}
{{< tab name="レスポンス" >}}
```json
{
    "elapse": "260µs",
    "reason": "success",
    "success": true
}
```
{{< /tab >}}
{{< /tabs >}}

### サブスクライバーの開始 {#구독자-시작}

**POST `/web/api/subscribers/:name/state`**

- `state`値が必要です。

{{< tabs >}}
{{< tab name="リクエスト" >}}
```json
{
    "state":"start",
}
```
{{< /tab >}}
{{< tab name="レスポンス" >}}
```json
{
    "elapse": "166.1µs",
    "reason": "success",
    "success": true
}
```
{{< /tab >}}
{{< /tabs >}}

### サブスクライバーの停止 {#구독자-중지}

**POST `/web/api/subscribers/:name/state`**

- `state`値が必要です。

{{< tabs >}}
{{< tab name="リクエスト" >}}
```json
{
    "state":"stop",
}
```
{{< /tab >}}
{{< tab name="レスポンス" >}}
```json
{
    "elapse": "54.2µs",
    "reason": "success",
    "success": true
}
```
{{< /tab >}}
{{< /tabs >}}


### サブスクライバーの削除 {#구독자-삭제}

**DELETE `/web/api/subscribers/:name`**

指定名のサブスクライバーを削除します。

レスポンス

```json
{
    "elapse": "77.1µs",
    "reason": "success",
    "success": true
}
```

## バックアップ {#백업}

### バックアップの取得 {#백업-조회}

**GET `/web/api/backup/archives`**

バックアップ一覧を返します。
- 既定のバックアップディレクトリは、machbase-neo実行ファイルのディレクトリ配下の`backups`です。
- 保存先を変更するには、`--backup-dir={path}`オプションを指定して起動します。既定値を使う場合、この指定は不要です。

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
{{< tab name="完全バックアップ" >}}
```json
{
    "type":"database", // databaseまたはtable
    "tableName":"",
    "duration":{
        "type":"full",
        "after":"",
        "from":"",
        "to":""
    },
    "path":"example_backup1" 
    // "path":"/home/neo/backups/example_backup1" // 絶対パスの例
}
```
{{< /tab >}}
{{< tab name="増分バックアップ" >}}
```json
{
    "type":"database", // databaseまたはtable
    "tableName":"",
    "duration":{
        "type":"incremental",
        "after":"{previous_backup_dir}",
        "from":"",
        "to":""
    },
    "path":"example_backup1" 
    // "path":"/home/neo/backups/example_backup1" // 絶対パスの例
}
```
{{< /tab >}}
{{< tab name="期間バックアップ" >}}
```json
{
    "type":"database", // databaseまたはtable
    "tableName":"",
    "duration":{
        "type":"time",
        "after":"",
        "from":"2024-08-01 00:00:00",
        "to":"2024-08-02 23:59:59"
    },
    "path":"example_backup1" 
    // "path":"/home/neo/backups/example_backup1" // 絶対パスの例
}
```
{{< /tab >}}
{{< tab name="テーブルバックアップ" >}}
```json
{
    "type":"table", // databaseまたはtable
    "tableName":"example",
    "duration":{
        "type":"full",
        "after":"",
        "from":"",
        "to":""
    },
    "path":"example_backup1" 
    // "path":"/home/neo/backups/example_backup1" // 絶対パスの例
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
{{< tab name="リクエスト" >}}
```json
{
    "path":"example_backup1" // 相対パス
    // "path":"/home/machbase/machbase_home/dbs/example_backup1" // 絶対パス
}
```
{{< /tab >}}
{{< tab name="レスポンス" >}}
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

### 検索 {#검색}

**GET `/web/api/pkgs/search?name=pkg_name&possibles=10`**

クエリパラメーター
 - `name`: 検索するパッケージ名。空の場合は、インストール済みとおすすめのパッケージを返します。
 - `possibles`: 類似するパッケージ候補の件数。`possibles=0`の場合は、指定した名前との完全一致だけを検索します。


レスポンス

```json
{
    "success": true,
    "reason": "success",
    "data":{},
    "elapse": "547.1µs"
}
```
### 同期 {#동기화}

**GET `/web/api/pkgs/sync`**

パッケージ情報を同期します。

レスポンス

```json
{
    "success": true,
    "reason": "success",
    "elapse": "30.9144ms"
}
```


### インストール {#설치}

**GET `/web/api/pkgs/install/:name`**

 - `:name`: インストールするパッケージ名。必須

レスポンス
```json
{
    "success": true,
    "reason": "success",
    "data":{}, // 値がなければ省略
    "log":"",
    "elapse": "23.1491ms"
}
```

### 削除 {#제거}

**GET `/web/api/pkgs/uninstall/:name`**

 - `:name`: 削除するパッケージ名。必須

レスポンス
```json
{
    "success": true,
    "reason": "success",
    "data":{}, // 値がなければ省略
    "log":"",
    "elapse": "88.4133ms"
}
```


## その他 {#기타}

### 参考資料 {#참고-자료}

**GET `/web/api/refs/*path`**

- `ReferenceGroup`
```json
{
    "label": "グループ名",
    "items":[{"ReferenceItem"}]
}
```

- `ReferenceItem`
```json
{
    "type": "type",
    "title": "表示タイトル",
    "address": "URLアドレス",
    "target": "ブラウザーのリンク先"
}
```

- type: `url`, `wrk`, `tql`, `sql`
- address: `serverfile://<path>`接頭辞がある場合は、サーバー上のファイルを指し、
  それ以外は、`https://`で始まる外部Web URLです。


### SQL文の分割 {#sql-구문-분할기}

**POST `/web/api/splitter/sql`**

```json
{
    "success": true,
    "reason": "成功またはエラーの理由",
    "elapse": "経過時間",
    "data": {
        "statements": [
            {
                "text": "-- env: bridge=sqlite",
                "beginLine": 1,
                "endLine": 1,
                "isComment": true,
                "env": {
                    "bridge": "sqlite",
                    "error": "`-- env: bridge=database`に構文エラーがある場合"
                }
            },
            {
                "text": "select * from table",
                "beginLine": 2,
                "endLine": 2,
                "isComment": false,
                "env": {
                    "bridge": "sqlite",
                    "error": "`-- env: bridge=database`に構文エラーがある場合"
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

### ライセンス情報 {#라이선스-정보}

**GET `/web/api/license`**

```json
{
    "success": true,
    "reason": "成功またはエラーの理由",
    "elapse": "経過時間",
    "data": {
        "id": "ライセンスID",
        "type": "種類",
        "customer": "顧客",
        "project": "プロジェクト",
        "countryCode": "国コード",
        "installDate": "インストール日",
        "issueDate": "ライセンス発行日"
    }
}
```

### ライセンスのインストール {#라이선스-설치}

**POST `/web/api/license`**

ライセンスファイルをインストールします。


## WebSocket {#websocket}

```
ws://127.0.0.1:5654/web/ui/console/{console_id}/data?token={jwt_token}
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

管理サーバーが実装します。

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

- `array<object<KeyInfo>>|error`

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
        "result": []
    }
}
```

</details>

#### key.generate {#keygenerate}

`key.generate(id, typ, notBefore, notAfter, store)`

*パラメーター*
- `id` *string*
- `typ` *string* - 生成するキーの種類。RSAまたはECDSAが必要
- `notBefore` *int64* - キーの有効期間の開始時刻（Unixタイムスタンプ、秒）
    省略または0の場合は、現在時刻を使用します
- `notAfter` *int64* - キーの有効期間の終了時刻（Unixタイムスタンプ、秒）
    省略または0の場合は、既定の10年間を使用します
- `store` *bool* - キーペアをサーバーのキーストアに保存するかどうか

*戻り値*

- `any|error` - 生成したキー情報
    - `id`: キーペアの識別子
    - `certificate`: キーペアの証明書
    - `key`: キーペアの秘密鍵
    - `token`: キーペアに関連付けられたトークン
    - `serverKey`: サーバー証明書（storeがtrueの場合）
    - `zip`: キーペアとサーバー証明書を含むZIPアーカイブ（storeがtrueの場合）

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
            "string",
            "string",
            0,
            0,
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

#### key.delete {#keydelete}

`key.delete(id)`

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
        "method": "key.delete",
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


### スケジュール {#schedule}

#### schedule.list {#schedulelist}

`schedule.list()`

*パラメーター*

- なし

*戻り値*

- `array<object<scheduler.Schedule>>|error`

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
        "method": "schedule.list",
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

#### schedule.timer.add {#scheduletimeradd}

`schedule.timer.add(name, spec, command, autoStart)`

*パラメーター*
- `name` *string*
- `spec` *string*
- `command` *string*
- `autoStart` *bool*

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
        "method": "schedule.timer.add",
        "params": [
            "string",
            "string",
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

#### schedule.subscriber.add {#schedulesubscriberadd}

`schedule.subscriber.add(name, bridge, command, autoStart, topic, qos)`

*パラメーター*
- `name` *string*
- `bridge` *string*
- `command` *string*
- `autoStart` *bool*
- `topic` *string*
- `qos` *int*

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
        "method": "schedule.subscriber.add",
        "params": [
            "string",
            "string",
            "string",
            false,
            "string",
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
        "result": null
    }
}
```

</details>

#### schedule.delete {#scheduledelete}

`schedule.delete(name)`

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
        "method": "schedule.delete",
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

#### schedule.start {#schedulestart}

`schedule.start(name)`

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
        "method": "schedule.start",
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

#### schedule.stop {#schedulestop}

`schedule.stop(name)`

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
        "method": "schedule.stop",
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


### HTTP {#http}

#### http.debug.set {#httpdebugset}

`http.debug.set(m)`

*パラメーター*
- `m` *object* - enableとlogLatencyキーを持つデバッグ設定マップ

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

