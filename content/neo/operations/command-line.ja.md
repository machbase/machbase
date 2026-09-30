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
| `--server`        | `127.0.0.1:5654` | machbase-neo HTTP アドレス<br/> 例: `--server 127.0.0.1:5654`<br/>環境変数: `NEOSHELL_HOST` |
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

どちらの方法でも指定されていない値は、シェルがデフォルト値（`127.0.0.1:5654`、`SYS`、`manager`）を示して入力を求めます。Enter キーを押すと、デフォルト値を使用します。

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
┌────────┬──────────────────────────────────────────────────┐
│ ROWNUM │ BINARY_SIGNATURE                                 │
├────────┼──────────────────────────────────────────────────┤
│      1 │ 8.7.0.official-DARWIN-ARM_M1-64-release-standard │
└────────┴──────────────────────────────────────────────────┘
a row selected.
```

**テーブルの作成**

```sh
machbase-neo» create tag table if not exists example (
  name varchar(20) primary key,
  time datetime basetime,
  value double summarized
);
table created.
```

**スキーマの確認**

```sh
machbase-neo» desc example;
┌────────┬────────┬──────────┬────────┬────────────┬───────┐
│ ROWNUM │ COLUMN │ TYPE     │ LENGTH │ FLAG       │ INDEX │
├────────┼────────┼──────────┼────────┼────────────┼───────┤
│      1 │ NAME   │ varchar  │     20 │ tag name   │       │
│      2 │ TIME   │ datetime │     31 │ base time  │       │
│      3 │ VALUE  │ double   │     17 │ summarized │       │
└────────┴────────┴──────────┴────────┴────────────┴───────┘
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
│ ROWNUM │ NAME │ TIME                │ VALUE │
├────────┼──────┼─────────────────────┼───────┤
│      1 │ tag0 │ 2021-08-12 00:00:00 │   100 │
└────────┴──────┴─────────────────────┴───────┘
a row selected.
```

**テーブルの削除**

```sh
machbase-neo» drop table example;
table dropped.
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
     * name = 'tag.1'
```

#### export

```
Usage: export [options] <table>

Arguments:
  table - table name to read

Options:
  -h, --help         Show this help message
  -o, --output       output file (default:'-' stdout) (default: -)
      --compress     compression type (none, gzip) (default: none)
  -f, --format       output format (box, csv, tsv, json, ndjson) (default: csv)
  -t, --timeformat   time format [ns|us|ms|s|<timeformat>] (default: ns)
      --tz           time zone for handling datetime (default: time zone) (default: local)
  -p, --precision    set precision of float value to force round (default: -1)
      --[no-]header  print header (default: false)
      --null-value   string to represent null values (default: )
      --[no-]silent  suppress progress output (default: false)
```

#### import

```
Usage: import [options] <table>

Arguments:
  table - table name to read

Options:
  -h, --help          Show this help message
  -i, --input         input file (default:'-' stdin) (default: -)
      --compress      compression type (none, gzip) (default: none)
  -f, --format        input format (csv, tsv, ndjson) (default: csv)
  -t, --timeformat    time format [ns|us|ms|s|<timeformat>] (default: ns)
      --tz            time zone for handling datetime (default: time zone) (default: local)
      --header        header option [skip|columns|none] (default: none)
      --null-value    string to represent null values (default: NULL)
      --[no-]dry-run  run in dry mode (default: false)
      --[no-]verbose  verbose mode, it works only with --dry-run (default: false)
```

#### show info

サーバー情報を表示します。

```sh
machbase-neo» show info;
┌────────┬────────────────────┬──────────────────────────────┐
│ ROWNUM │ NAME               │ VALUE                        │
├────────┼────────────────────┼──────────────────────────────┤
│      1 │ build.engine       │ static_standard_darwin_arm64 │
│      2 │ build.hash         │ b55f8170                     │
│      3 │ build.timestamp    │ 2026-09-10T05:43:13          │
│      4 │ build.version      │ v8.7.1-snapshot              │
│      5 │ mem.frees          │ 397,853,948                  │
│      6 │ mem.heap_alloc     │ 32.8MB                       │
│      7 │ mem.heap_in_use    │ 40.0MB                       │
│      8 │ mem.heap_sys       │ 547.9MB                      │
│      9 │ mem.lives          │ 253,315                      │
│     10 │ mem.mallocs        │ 398,107,263                  │
│     11 │ mem.stack_in_use   │ 1.5MB                        │
│     12 │ mem.stack_sys      │ 1.5MB                        │
│     13 │ mem.sys            │ 564.2MB                      │
│     14 │ runtime.arch       │ arm64                        │
│     15 │ runtime.goroutines │ 32                           │
│     16 │ runtime.os         │ darwin                       │
│     17 │ runtime.pid        │ 35507                        │
│     18 │ runtime.processes  │ 10                           │
│     19 │ runtime.uptime     │ 6 days 4h 4m 42s             │
└────────┴────────────────────┴──────────────────────────────┘
```

#### show ports

サーバーのインターフェイスポートを表示します。

```sh
machbase-neo» show ports;
┌────────┬────────────┬─────────────────────────────────────────┐
│ ROWNUM │ PORT       │ ADDRESS                                 │
├────────┼────────────┼─────────────────────────────────────────┤
│      1 │ http       │ tcp://127.0.0.1:5654                    │
│      2 │ http       │ unix:///tmp/machbase-neo-http-5654.sock │
│      3 │ mach       │ tcp://127.0.0.1:5656                    │
│      4 │ mqtt       │ tcp://127.0.0.1:5653                    │
│      5 │ mqtt       │ unix:///tmp/machbase-neo-mqtt-5653.sock │
│      6 │ servicectl │ tcp://127.0.0.1:62978                   │
│      7 │ shell      │ tcp://127.0.0.1:5652                    │
└────────┴────────────┴─────────────────────────────────────────┘
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
| `show table [-a] <table>` | O | - | - | - |
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
┌────────┬───────────────┬───────────┬────────────┬──────────┬────────────┬────────────┐
│ ROWNUM │ DATABASE_NAME │ USER_NAME │ TABLE_NAME │ TABLE_ID │ TABLE_TYPE │ TABLE_FLAG │
├────────┼───────────────┼───────────┼────────────┼──────────┼────────────┼────────────┤
│      1 │ MACHBASEDB    │ SYS       │ EXAMPLE    │      770 │ Tag        │            │
└────────┴───────────────┴───────────┴────────────┴──────────┴────────────┴────────────┘
```

#### show table

構文: `show table [-a] <table>`

テーブルの列一覧を表示します。`-a` を指定すると、非表示の列も含めます。

```sh
machbase-neo» show table -a example;
┌────────┬────────┬──────────┬────────┬────────────┬───────┐
│ ROWNUM │ COLUMN │ TYPE     │ LENGTH │ FLAG       │ INDEX │
├────────┼────────┼──────────┼────────┼────────────┼───────┤
│      1 │ NAME   │ varchar  │     20 │ tag name   │       │
│      2 │ TIME   │ datetime │     31 │ base time  │       │
│      3 │ VALUE  │ double   │     17 │ summarized │       │
│      4 │ _RID   │ long     │     20 │            │       │
└────────┴────────┴──────────┴────────┴────────────┴───────┘
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
┌────────┬─────────┬────────────────────────┬───────┐
│ ROWNUM │      ID │ NAME                   │ TYPE  │
├────────┼─────────┼────────────────────────┼───────┤
│      1 │ 1000019 │ M$SYS_TABLESPACES      │ Fixed │
│      2 │ 1000023 │ M$SYS_TABLESPACE_DISKS │ Fixed │
│      3 │ 1000049 │ M$SYS_TABLES           │ Fixed │
│      4 │ 1000052 │ M$SYS_VIEWS            │ Fixed │
│      5 │ 1000054 │ M$TABLES               │ Fixed │
│      6 │ 1000056 │ M$SYS_COLUMNS          │ Fixed │
......
```

#### show virtual-tables

```sh
machbase-neo» show virtual-tables;
┌────────┬─────────┬─────────────────────────────────────────┬───────┐
│ ROWNUM │      ID │ NAME                                    │ TYPE  │
├────────┼─────────┼─────────────────────────────────────────┼───────┤
│      1 │     769 │ V$EXAMPLE_STAT                          │ Fixed │
│      2 │ 1000000 │ V$SYSSTAT                               │ Fixed │
│      3 │ 1000001 │ V$SYSTIME                               │ Fixed │
│      4 │ 1000002 │ V$SYSMEM                                │ Fixed │
│      5 │ 1000003 │ V$PROPERTY                              │ Fixed │
│      6 │ 1000004 │ V$MUTEX                                 │ Fixed │
......
```

#### show users

```sh
machbase-neo» show users;
┌────────┬─────────┬──────┐
│ ROWNUM │ USER_ID │ NAME │
├────────┼─────────┼──────┤
│      1 │       1 │ SYS  │
└────────┴─────────┴──────┘
```

#### show license

```sh
machbase-neo» show license;
┌────────┬──────────┬───────────┬──────────┬─────────┬──────────────┬─────────────────────┬────────────┬────────┐
│ ROWNUM │ ID       │ TYPE      │ CUSTOMER │ PROJECT │ COUNTRY_CODE │ INSTALL_DATE        │ ISSUE_DATE │ STATUS │
├────────┼──────────┼───────────┼──────────┼─────────┼──────────────┼─────────────────────┼────────────┼────────┤
│      1 │ 00000000 │ COMMUNITY │ NONE     │ NONE    │ KR           │ 2026-09-10 10:06:19 │ 20991231   │ VALID  │
└────────┴──────────┴───────────┴──────────┴─────────┴──────────────┴─────────────────────┴────────────┴────────┘
```

#### session list

構文: `session list` {{< neo_since ver="8.0.17" />}}

接続中のセッション一覧は`show sessions`で確認します。

```sh
machbase-neo» show sessions;
┌────────┬──────┬───────────┬─────────┬─────────────────────────┬──────┬───────────┬─────────────┐
│ ROWNUM │   ID │ USER_NAME │ USER_ID │ LOGIN_TIME              │ TYPE │ USER_IP   │ MAX_QPX_MEM │
├────────┼──────┼───────────┼─────────┼─────────────────────────┼──────┼───────────┼─────────────┤
│      1 │ 2484 │ SYS       │       1 │ 2026-09-17 17:35:01.139 │ CLI  │ 127.0.0.1 │ 1.1GB       │
└────────┴──────┴───────────┴─────────┴─────────────────────────┴──────┴───────────┴─────────────┘
```

#### session kill

構文: `session kill <ID>` {{< neo_since ver="8.0.17" />}}

#### session stat

構文: `session stat` {{< neo_since ver="8.0.17" />}}

```sh
machbase-neo» session stat;
┌────────┬──────────────────────┬───────┐
│ ROWNUM │ METRIC               │ VALUE │
├────────┼──────────────────────┼───────┤
│      1 │ OPEN CONN            │     1 │
│      2 │ IDLE                 │     1 │
│      3 │ IN USE               │     0 │
│      4 │ MAX IDLE CLOSED      │   268 │
│      5 │ MAX IDLE TIME CLOSED │   410 │
│      6 │ MAX LIFETIME CLOSED  │   852 │
│      7 │ WAIT COUNT           │     0 │
│      8 │ WAIT DURATION (AVG)  │    0s │
└────────┴──────────────────────┴───────┘
```

#### desc

構文: `desc [-a] <table>`

テーブル構造を確認します。

```sh
machbase-neo» desc example;
┌────────┬────────┬──────────┬────────┬────────────┬───────┐
│ ROWNUM │ COLUMN │ TYPE     │ LENGTH │ FLAG       │ INDEX │
├────────┼────────┼──────────┼────────┼────────────┼───────┤
│      1 │ NAME   │ varchar  │     20 │ tag name   │       │
│      2 │ TIME   │ datetime │     31 │ base time  │       │
│      3 │ VALUE  │ double   │     17 │ summarized │       │
└────────┴────────┴──────────┴────────┴────────────┴───────┘
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
