---
title: コマンドライン
type: docs
weight: 10
toc: true
---

## machbase-neo serve

machbase-neo サーバープロセスを起動します。

### フラグ

**一般フラグ**
             
| フラグ | 説明 |
|:-----------------|:----------------------------------------------------------------- |
| `--host`         | 待ち受けネットワークアドレス（デフォルト `127.0.0.1`）<br/> 例: `--host 0.0.0.0`                  |
| `-c`, `--config` | 設定ファイルのパス<br/> 例: `--config /data/machbase-neo.conf`|
| `--pid`          | PID ファイルのパス<br/> 例: `--pid /data/machbase-neo.pid`    |
| `--data`         | データベースのパス（デフォルト `./machbase_home`）<br/> 例: `--data /data/machbase`                 |
| `--file`         | ファイルの保存パス（デフォルト `.`）<br/> 例: `--file /data/files`                       |
| `--backup-dir`   | バックアップディレクトリのパス（デフォルト `./backups`）<br/> 例: `--backup-dir /data/backups` {{< neo_since ver="8.0.26" />}} |
| `--pref`         | 環境設定ディレクトリのパス<br/>(デフォルト `~/.config/machbase`)                                |
| `--preset`       | データベースのプリセット `auto`、`fog`、`edge`（デフォルト `auto`）<br/> 例: `--preset edge`    |

**データベースセッションのフラグ**

{{< neo_since ver="8.5.5" />}}

| フラグ | 説明 |
|:-------------------------|:----------------------------------------------------------------- |
| `--max-open-conn`        | データベースの最大接続数。<br/>(デフォルト `-1` 無制限) |
| `--max-idle-conn`        | 接続プールの最大アイドル接続数。<br/> `<=0` ではアイドル接続を保持しません。<br/> (デフォルト 2) |
| `--conn-max-lifetime`    | 接続を再使用できる最大時間。<br/> 期限切れの接続は、再使用前に遅延して閉じられる場合があります。<br/> `<= 0` では接続時間による終了はありません。 (デフォルト `10m`) |
| `--conn-max-idletime`    | 接続がアイドル状態でいられる最大時間。<br/> 期限切れの接続は、再使用前に遅延して閉じられる場合があります。<br/> `<= 0` ではアイドル時間による終了はありません。 (デフォルト `1m`)|

**HTTP フラグ**

{{< neo_since ver="8.0.43" />}}

| フラグ | デフォルト | 説明 |
|:------------------------|:------------|:------------------------------------------------------------------------- |
| `--http-linger`         | `-1`        | HTTP ソケットオプション。`-1` で SO_LINGER を無効化し、`>=0` で設定します。           |
| `--http-readbuf-size`   | `0`         | HTTP ソケットの読み取りバッファーサイズ。`0` ではシステムのデフォルトを使用。                          |
| `--http-writebuf-size`  | `0`         | HTTP ソケットの書き込みバッファーサイズ。`0` ではシステムのデフォルトを使用。                          |
| `--http-debug`          | `false`     | HTTP デバッグログを有効化                                                    |
| `--http-debug-latency`  | `"0"`       | 指定時間を超えたリクエストだけを記録（例: "3s"）。"0" はすべて記録。      |
| `--http-allow-statz`    |             | `/db/statz` API へのアクセスを許可する送信元 IP（カンマ区切り）。デフォルトは `127.0.0.1` のみ。 |

**ログのフラグ**

| フラグ | デフォルト | 説明 |
|:------------------------|:------------|:---------------------------------------------------------------------- |
| `--log-filename`        | `-` (stdout)| ログファイルのパス<br/> 例: `--log-filename /data/logs/machbase-neo.log`       |
| `--log-level`           | `INFO`      | ログレベル: TRACE、DEBUG、INFO、WARN、ERROR<br/> 例: `--log-level INFO`    |
| `--log-append`          | `true`      | 既存ログファイルに追記                                                    |
| `--log-rotate-schedule` | `@midnight` | ログローテーションのスケジュール                                                           |
| `--log-max-size`        | `10`        | ログファイルの最大サイズ（MB）                                                    |
| `--log-max-backups`     | `1`         | バックアップログの最大ファイル数                                                    |
| `--log-max-age`         | `7`         | バックアップファイルの保持日数                                                        |
| `--log-compress`        | `false`     | バックアップファイルを gzip 圧縮                                                       |
| `--log-time-utc`        | `false`     | ログのタイムスタンプを UTC で記録                                                 |

**リスナーのフラグ**

| フラグ | デフォルト | 説明 |
|:-----------------|:----------|-------------------------------------------|
| `--shell-port`   | `5652`    | SSH 待ち受けポート                              |
| `--mqtt-port`    | `5653`    | MQTT 待ち受けポート                             |
| `--mqtt-sock`    | `/tmp/machbase-neo-mqtt-5653.sock`| MQTT UNIX ソケット    |
| `--http-port`    | `5654`    | HTTP 待ち受けポート                             |
| `--http-sock`    | `/tmp/machbase-neo-http-5654.sock` | HTTP UNIX ソケット   |
| `--mach-port`    | `5656`    | Machbase ネイティブの待ち受けポート                |

{{< callout type="info" emoji="📌">}}
**注意**<br/>
`--host` のデフォルトはループバックアドレスのため、リモートホストから machbase-neo にアクセスできません。<br/>
リモートクライアントの接続を許可するには、`--host <host-address>` または `--host 0.0.0.0` を指定してください。
{{< /callout >}}

フラグなしで `machbase-neo serve` を実行すると、

```sh
$ machbase-neo serve
```

次のコマンドと同じ動作になります。

```sh
$ machbase-neo serve --host 127.0.0.1 --data ./machbase_home --file . --preset auto
```

## machbase-neo shell

machbase-neo シェルを起動します。他の引数がない場合は対話モードになります。

**フラグ**

| フラグ（ロング形式） | デフォルト | 説明 |
|:------------------|:-----------------|:-----------------------------------------------------------------|
| `-s`, `--server`  | `127.0.0.1:5654` | machbase-neo HTTP アドレス<br/> 例: `--server 127.0.0.1:5654`<br/>環境変数: `NEOSHELL_HOST` |
| `--user`          | `sys`            | ユーザー名<br/>環境変数: `NEOSHELL_USER`                            |
| `--password`      | `manager`        | パスワード<br/>環境変数: `NEOSHELL_PASSWORD`                          |

シェルは起動時に OS 環境変数 `NEOSHELL_HOST`、`NEOSHELL_USER`、`NEOSHELL_PASSWORD` からサーバーアドレス、ユーザー名、パスワードを取得します。
`--server`、`--user`、`--password` を指定した場合は、その値を優先します。

### ユーザー名とパスワードの優先順位

{{% steps %}}

### コマンドラインフラグ

`--server`、`--user`、`--password` が指定されている場合は、その値を使用します。

### 環境変数

`$NEOSHELL_HOST`（Windows では `%NEOSHELL_HOST%`）が設定されている場合は、サーバーアドレスに使用します。

`$NEOSHELL_USER`（Windows では `%NEOSHELL_USER%`）が設定されている場合は、ユーザー名に使用します。

`$NEOSHELL_PASSWORD`（Windows では `%NEOSHELL_PASSWORD%`）が設定されている場合は、パスワードに使用します。

### デフォルト値

上記がいずれも指定されていない場合は、デフォルトの `127.0.0.1:5654`、`sys`、`manager` を使用します。

{{% /steps %}}

### 使用例

セキュリティのため、次のようにコマンド実行時に環境変数を設定することを推奨します。

```sh
$ NEOSHELL_PASSWORD='my-secret' machbase-neo shell --user sys
```

`--password` を使用すると、次のように `ps` コマンドでパスワードが表示される場合がある点に注意してください。

```sh
$ machbase-neo shell --user sys --password manager
```

```sh
$ ps -aef |grep machbase-neo
  501 13551  3598   0  9:33AM ttys000    0:00.07 machbase-neo shell --user sys --password manager
```

**クエリの実行**
  
```sh
machbase-neo» select binary_signature from v$version;
┌────────┬─────────────────────────────────────────────┐
│ ROWNUM │ BINARY_SIGNATURE                            │
├────────┼─────────────────────────────────────────────┤
│      1 │ 8.0.2.develop-LINUX-X86-64-release-standard │
└────────┴─────────────────────────────────────────────┘
a row fetched.
```

**テーブルの作成**

```sh
machbase-neo» create tag table if not exists example (
  name varchar(20) primary key,
  time datetime basetime,
  value double summarized
);
executed.
```

**スキーマの確認**

```sh
machbase-neo» desc example;
┌────────┬───────┬──────────┬────────┐
│ ROWNUM │ NAME  │ TYPE     │ LENGTH │
├────────┼───────┼──────────┼────────┤
│      1 │ NAME  │ varchar  │     20 │
│      2 │ TIME  │ datetime │      8 │
│      3 │ VALUE │ double   │      8 │
└────────┴───────┴──────────┴────────┘
```

**データの挿入**

```sh
machbase-neo» insert into example values('tag0', to_date('2021-08-12'), 100);
a row inserted.
```

**データの検索**

```sh
machbase-neo» select * from example;
┌────────┬──────┬─────────────────────┬───────┐
│ ROWNUM │ NAME │ TIME(LOCAL)         │ VALUE │
├────────┼──────┼─────────────────────┼───────┤
│      1 │ tag0 │ 2021-08-12 00:00:00 │ 100   │
└────────┴──────┴─────────────────────┴───────┘
a row fetched.
```

**テーブルの削除**

```sh
machbase-neo» drop table example;
executed.
```

### サブコマンド

#### explain

構文: `explain [--full] <sql>`

SQL の実行計画を表示します。

```sh
machbase-neo» explain select * from example where name = 'tag.1';
 PROJECT
  TAG READ (RAW)
   KEYVALUE INDEX SCAN (_EXAMPLE_DATA_0)
    [KEY RANGE]
     * IN ()
   VOLATILE INDEX SCAN (_EXAMPLE_META)
    [KEY RANGE]
     *
```

#### export

```
  export [options] <table>
  arguments:
    table                    読み取るテーブル名
  options:
    -o,--output <file>       出力ファイル（デフォルト: `-`、標準出力）
    -f,--format <format>     出力形式
                csv          CSV 形式（デフォルト）
                json         JSON 形式
       --compress <method>   圧縮方式 [gzip]（デフォルトは非圧縮）
       --[no-]heading        ヘッダー出力の有無（デフォルト:false）
       --[no-]footer         フッター出力の有無（デフォルト:false）
    -d,--delimiter           CSV 区切り文字（デフォルト `,`）
       --tz                  datetime 処理のタイムゾーンを指定
    -t,--timeformat          時刻形式 [ns|ms|s|<timeformat>]（デフォルト `ns`）
                             詳細は "help timeformat" を参照
    -p,--precision <int>     浮動小数点値を丸める桁数を指定
```

#### import

```
  import [options] <table>
  arguments:
    table                 データを書き込むテーブル名
  options:
    -i,--input <file>     入力ファイル（デフォルト: `-`、標準入力）
    -f,--format <fmt>     ファイル形式 [csv]（デフォルト `csv`）
       --compress <alg>   入力データの圧縮方式（対応: gzip）
       --no-header        ヘッダーなし。最初の行をスキップしない（デフォルト）
       --charset          入力が UTF-8 以外の場合に文字エンコーディングを指定
       --header           最初の行がヘッダーの場合はスキップ
       --method           書き込み方式 [insert|append]（デフォルト `insert`）
       --create-table     テーブルがない場合は作成（デフォルト:false）
       --truncate-table   新しいデータの取り込み前にテーブルを空にする（デフォルト:false）
    -d,--delimiter        CSV 区切り文字（デフォルト `,`）
       --tz               datetime 処理のタイムゾーンを指定
    -t,--timeformat       時刻形式 [ns|ms|s|<timeformat>]（デフォルト `ns`）
                          詳細は "help timeformat" を参照
       --eof <string>     EOF 行を指定。[a-zA-Z0-9]+ に一致する文字列を使用（デフォルト '.'）
```

#### show info

サーバー情報を表示します。

```sh
machbase-neo» show info;
┌────────────────────┬─────────────────────────────┐
│ NAME               │ VALUE                       │
├────────────────────┼─────────────────────────────┤
│ build.version      │ v2.0.0                      │
│ build.hash         │ #c953293f                   │
│ build.timestamp    │ 2023-08-29T08:08:00         │
│ build.engine       │ static_standard_linux_amd64 │
│ runtime.os         │ linux                       │
│ runtime.arch       │ amd64                       │
│ runtime.pid        │ 57814                       │
│ runtime.uptime     │ 2h 30m 57s                  │
│ runtime.goroutines │ 45                          │
│ mem.sys            │ 32.6 MB                     │
│ mem.heap.sys       │ 19.0 MB                     │
│ mem.heap.alloc     │ 9.7 MB                      │
│ mem.heap.in-use    │ 13.0 MB                     │
│ mem.stack.sys      │ 1,024.0 KB                  │
│ mem.stack.in-use   │ 1,024.0 KB                  │
└────────────────────┴─────────────────────────────┘
```

#### show ports

サーバーのインターフェイスポートを表示します。

```sh
machbase-neo» show ports;
┌─────────┬────────────────────────────────────────┐
│ SERVICE │ PORT                                   │
├─────────┼────────────────────────────────────────┤
│ http    │ tcp://127.0.0.1:5654                   │
│ mach    │ tcp://127.0.0.1:5656                   │
│ mqtt    │ tcp://127.0.0.1:5653                   │
│ shell   │ tcp://127.0.0.1:5652                   │
└─────────┴────────────────────────────────────────┘
```

#### show tables

構文: `show tables [FROM <database>[.<user>]] [LIKE <pattern>] [WITH ALL]`

{{< neo_since ver="8.7.0" />}}

一部の `show` サブコマンドは `FROM` と `LIKE` に対応します。
`FROM <database>[.<user>]` は検索対象のデータベースとユーザーを指定し、`LIKE <pattern>` は名前のパターンで結果を絞り込みます。
パターンは一重または二重引用符で囲む SQL `LIKE` パターンです。`%` は 0 文字以上、`_` は 1 文字に一致します。
`FROM` の代わりに `IN` を使用できます。`WITH ALL` は非表示の項目を含めます。

```sh
machbase-neo» show tables from MACHBASEDB.SYS like 'TAG%' with all;
machbase-neo» show indexes like 'IDX_%';
```

| コマンド | `FROM` | `LIKE` | `WITH ALL` | `LIKE` の適用対象 |
|:--------|:------:|:------:|:----------:|:-----------------|
| `show tables` | O | O | O | テーブル名 |
| `show indexes` | O | O | - | インデックス名 |
| `show table <table>` | O | - | O | - |
| `show index <index>` | O | - | - | - |
| `show tags <table> [tag...]` | O | O | - | タグ名 |
| `show storage` | O | O | - | テーブル名 |
| `show table-usage` | O | O | - | テーブル名 |
| `show lsm` | O | O | - | テーブル名 |
| `show indexgap` | O | O | - | テーブル名 |
| `show tagindexgap` | O | O | - | テーブル名 |
| `show rollupgap` | O | O | - | テーブル名 |
| `show users` | - | O | - | ユーザー名 |
| `show databases` | - | O | - | データベース名 |
| `show meta-tables` | - | O | - | テーブル名 |
| `show virtual-tables` | - | O | - | テーブル名 |
| `show sessions` | - | O | - | ユーザー名 |
| `show statements` | - | O | - | クエリテキスト |

`show table`、`show index`、`show tags` など、対象名を引数に取るコマンドでは、`<database>.<user>.<name>` 形式の修飾名と `FROM` を併用できません。
`show tags` でタグ名を明示した場合は、`LIKE` を併用できません。

テーブル一覧を表示します。`WITH ALL` を指定すると、非表示のテーブルも含めます。

```sh
machbase-neo» show tables;
┌────────┬────────────┬──────┬─────────────┬───────────┐
│ ROWNUM │ DB         │ USER │ NAME        │ TYPE      │
├────────┼────────────┼──────┼─────────────┼───────────┤
│      1 │ MACHBASEDB │ SYS  │ EXAMPLE     │ Tag Table │
│      2 │ MACHBASEDB │ SYS  │ TAG         │ Tag Table │
│      3 │ MACHBASEDB │ SYS  │ TAGDATA     │ Tag Table │
└────────┴────────────┴──────┴─────────────┴───────────┘
```

#### show table

構文: `show table <table> [WITH ALL]`

テーブルの列一覧を表示します。`WITH ALL` を指定すると、非表示の列も含めます。

```sh
machbase-neo» show table example with all;
┌────────┬───────┬──────────┬────────┬──────────┐
│ ROWNUM │ NAME  │ TYPE     │ LENGTH │ DESC     │
├────────┼───────┼──────────┼────────┼──────────┤
│      1 │ NAME  │ varchar  │    100 │ tag name │
│      2 │ TIME  │ datetime │     31 │ basetime │
│      3 │ VALUE │ double   │     17 │          │
│      4 │ _RID  │ long     │     20 │          │
└────────┴───────┴──────────┴────────┴──────────┘
```

#### show indexes

構文: `show indexes [FROM <database>[.<user>]] [LIKE <pattern>]`

インデックス一覧を表示します。`FROM` で検索範囲を指定し、`LIKE` でインデックス名を絞り込めます。

```sh
machbase-neo» show indexes from MACHBASEDB.SYS like 'TAG%';
```

#### show meta-tables

```sh
machbase-neo» show meta-tables;
┌────────┬─────────┬────────────────────────┬─────────────┐
│ ROWNUM │      ID │ NAME                   │ TYPE        │
├────────┼─────────┼────────────────────────┼─────────────┤
│      1 │ 1000020 │ M$SYS_TABLESPACES      │ Fixed Table │
│      2 │ 1000024 │ M$SYS_TABLESPACE_DISKS │ Fixed Table │
│      3 │ 1000049 │ M$SYS_TABLES           │ Fixed Table │
│      4 │ 1000051 │ M$TABLES               │ Fixed Table │
│      5 │ 1000053 │ M$SYS_COLUMNS          │ Fixed Table │
│      6 │ 1000054 │ M$COLUMNS              │ Fixed Table │
......
```

#### show virtual-tables

```sh
machbase-neo» show virtual-tables;
┌────────┬─────────┬─────────────────────────────────────────┬────────────────────┐
│ ROWNUM │      ID │ NAME                                    │ TYPE               │
├────────┼─────────┼─────────────────────────────────────────┼────────────────────┤
│      1 │      65 │ V$HOME_STAT                             │ Fixed Table (stat) │
│      2 │      93 │ V$DEMO_STAT                             │ Fixed Table (stat) │
│      3 │     227 │ V$SAMPLEBENCH_STAT                      │ Fixed Table (stat) │
│      4 │     319 │ V$TAGDATA_STAT                          │ Fixed Table (stat) │
│      5 │     382 │ V$EXAMPLE_STAT                          │ Fixed Table (stat) │
│      6 │     517 │ V$TAG_STAT                              │ Fixed Table (stat) │
......
```

#### show users

```sh
machbase-neo» show users;
┌────────┬───────────┐
│ ROWNUM │ USER_NAME │
├────────┼───────────┤
│      1 │ SYS       │
└────────┴───────────┘
a row fetched.
```

#### show license

```sh
 machbase-neo» show license;
┌────────┬──────────┬──────────────┬──────────┬────────────┬──────────────┬─────────────────────┐
│ ROWNUM │ ID       │ TYPE         │ CUSTOMER │ PROJECT    │ COUNTRY_CODE │ INSTALL_DATE        │
├────────┼──────────┼──────────────┼──────────┼────────────┼──────────────┼─────────────────────┤
│      1 │ 00000023 │ FOGUNLIMITED │ VUTECH   │ FORESTFIRE │ KR           │ 2024-04-22 15:56:14 │
└────────┴──────────┴──────────────┴──────────┴────────────┴──────────────┴─────────────────────┘
a row fetched.
```

#### session list

構文: `session list` {{< neo_since ver="8.0.17" />}}

```sh
 machbase-neo» session list;
┌────┬───────────┬─────────┬────────────┬─────────┬─────────┬──────────┐
│ ID │ USER_NAME │ USER_ID │ STMT_COUNT │ CREATED │ LAST    │ LAST SQL │
├────┼───────────┼─────────┼────────────┼─────────┼─────────┼──────────┤
│ 25 │ SYS       │ 1       │          1 │ 1.667ms │ 1.657ms │ CONNECT  │
└────┴───────────┴─────────┴────────────┴─────────┴─────────┴──────────┘
```

#### session kill

構文: `session kill <ID>` {{< neo_since ver="8.0.17" />}}

#### session stat

構文: `session stat` {{< neo_since ver="8.0.17" />}}

```sh
machbase-neo» session stat;
┌────────────────┬───────┐
│ NAME           │ VALUE │
├────────────────┼───────┤
│ CONNS          │ 1     │
│ CONNS_USED     │ 17    │
│ STMTS          │ 0     │
│ STMTS_USED     │ 20    │
│ APPENDERS      │ 0     │
│ APPENDERS_USED │ 0     │
│ RAW_CONNS      │ 1     │
└────────────────┴───────┘
```

#### desc

構文: `desc [-a] <table>`

テーブル構造を確認します。

```sh
machbase-neo» desc example;
┌────────┬───────┬──────────┬────────┬──────────┐
│ ROWNUM │ NAME  │ TYPE     │ LENGTH │ DESC     │
├────────┼───────┼──────────┼────────┼──────────┤
│      1 │ NAME  │ varchar  │    100 │ tag name │
│      2 │ TIME  │ datetime │     31 │ basetime │
│      3 │ VALUE │ double   │     17 │          │
└────────┴───────┴──────────┴────────┴──────────┘
```

## machbase-neo restore

構文: `machbase-neo restore --data <machbase_home_dir> <backup_dir>` {{< neo_since ver="8.0.17" />}}

バックアップからデータベースを復元します。

```sh
$ machbase-neo restore --data <machbase home dir>  <backup dir>
```

## machbase-neo version

バージョンとエンジンの情報を表示します。

![machbase-neo_version](/neo/operations/img/machbase-neo-version.png)

## machbase-neo gen-config

デフォルトの設定テンプレートを出力します。

```
$ machbase-neo gen-config ↵

define DEF {
    LISTEN_HOST       = flag("--host", "127.0.0.1")
    SHELL_PORT        = flag("--shell-port", "5652")
    MQTT_PORT         = flag("--mqtt-port", "5653")
    HTTP_PORT         = flag("--http-port", "5654")
......
```
