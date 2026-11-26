---
title: 設定ファイル
type: docs
weight: 11
toc: true
---

## 新しい設定ファイルの作成 {#새-설정-파일-만들기}

machbase-neo を `gen-config` で実行し、出力を基本設定ファイルとして保存します。

```sh
machbase-neo gen-config > ./machbase-neo.conf
```

生成した設定ファイルの値を変更し、`--config <path>` または `-c <path>` でファイルを指定して machbase-neo を起動してください。

```sh
machbase-neo serve --config ./machbase-neo.conf
```

`--config-dir <path>` を指定すると、ディレクトリ内の `.conf` ファイルを名前順に読み込みます。
両方を指定した場合は `--config` が優先されます。どちらも指定しない場合は内蔵のデフォルト設定を使用します。

## 設定と起動の規則

`--` 以降のオプションは、`flag()` と `flagOrError()` を含め、フラグとして解釈されません。
同じフラグを繰り返すと、HCL の `flag()` は最初の値を使用します。起動オプションは同じ表記の最後の値を使用し、
長い表記と短い別名の両方がある場合は長い表記が優先されます。
`--config`、`--config-dir`、`--pid`、`--bootlog`、`--preset`、`--file` など、
値が必要な起動オプションに値がない場合や空の場合はエラーになります。
真偽値の起動フラグに明示的に不正な値を指定した場合もエラーになります。
値を指定しない真偽値の起動フラグは HCL 式では `true` です。
参照されたフラグに値がない場合、デフォルト値や次のオプションを使用せず、設定エラーになります。
設定で参照されない不明なフラグは無視されます。単独の `-` は値として使用できます。
数値以外で `-` から始まる値は `--name=-value` の形式で指定してください。

Unix の `--daemon` はサーバーの起動完了後にのみ成功を返します。
起動に失敗した場合、または 2 分以内に起動しない場合はエラーを返します。
`--pid` を指定する場合、PID ファイルが既に存在していてはいけません。
プロセスはファイルを排他的に作成し、終了時に自分のファイルを削除します。
この規則はフォアグラウンド実行にも適用されます。古い PID ファイルは、該当するプロセスが
実行されていないことを確認してから手動で削除してください。

Windows では `arg()` と `arglen()` はサービスプロセスの元の引数を使用し、
インストール済みサービスでは `service run` も含まれます。サービスはサーバーの起動完了後に
実行中と報告され、起動または終了時のエラーは Windows イベントログに記録されます。

## データベースディレクトリ {#데이터베이스-디렉터리}

`DataDir` のデフォルトは `${execDir()}/machbase_home` で、`machbase-neo` 実行ファイルのディレクトリの下に作成します。

データベースファイルを保存する新しいパスに変更してください。そのフォルダーにデータベースがない場合、machbase-neo が自動的に作成します。

## 環境設定ディレクトリ {#환경-설정-디렉터리}

`PrefDir` のデフォルトは `prefDir("machbase")` で、`$HOME/.config/machbase` を指します。

## リスナー {#리스너}

| リスナー | 設定 | デフォルト |
|:--------------------------|:--------------------------|:------------------------|
| SSH シェル                 | Shell.Listeners           | `tcp://127.0.0.1:5652`  |
| MQTT                      | Mqtt.Listeners            | `tcp://127.0.0.1:5653` <br/> `unix://${tempDir()}/machbase-neo-mqtt.sock`  |
| HTTP                      | Http.Listeners            | `tcp://127.0.0.1:5654` <br/> `unix://${tempDir()}/machbase-neo.sock`  |
| Machbase ネイティブ           | Machbase.PORT_NO          | `5656`                  |
|                           | Machbase.BIND_IP_ADDRESS  | `127.0.0.1`             |


{{< callout type="info" >}}
Machbase のネイティブポート `5656` は、JDBC、ODBC などのネイティブクライアントが使用します。
JDBC・ODBC ドライバーは Machbase の Web サイトからダウンロードできます。
{{< /callout >}}

## 設定リファレンス {#설정-참조}

設定ファイルは HCL 構文を使用します。

### 関数 {#functions}

設定値には、次の関数を使用できます。

- `flag(A, B)`: コマンドラインフラグ A の値を取得します。未指定の場合はデフォルト値 B を使用します。
- `env(A, B)`: 環境変数 A の値を取得します。未指定の場合はデフォルト値 B を使用します。
- `execDir()`: 実行ファイルのディレクトリを返します。
- `tempDir()`: システムの一時ディレクトリを返します。{{< neo_since ver="8.0.36" />}}
- `userDir()`: ユーザーのホームディレクトリを返します。Linux/macOS では `$HOME` を使用します。
- `prefDir(subdir)`: ユーザーの環境設定ディレクトリを返します。Linux/macOS では `$HOME/.config/{subdir}` の実際のパスを返します。
- `envOrError(name)`、`flagOrError(name)`: 環境変数またはフラグの値を返し、存在しない場合はエラーになります。
- `arg(index, default)`、`argOrError(index)`: 0 から始まるインデックスの引数を返し、存在しない場合はデフォルト値またはエラーを返します。引数リストには実行ファイルと別に指定したフラグ値が含まれますが、`-` から始まる引数は除外されます。
- `arglen()`: 実行ファイルとフラグを含む元のプロセス引数の数を返します。
- `pname()`、`version()`: プロセス名とバージョンを返します。
- `execFile()`、`userConfDir()`: 実行ファイルのパスとユーザー設定ディレクトリを返します。
- `upper`、`lower`、`min`、`max`、`strlen`、`substr`: 文字列および数値の関数です。

`define` ブロックの属性は `<block>_<attribute>` の形式で参照できます。

{{< callout type="info">}}
**env() と flag() の組み合わせ**<br/>
ユーザー設定の優先順位は、通常、コマンドラインフラグ → 環境変数 → デフォルト値とします。
`flag("--my-var", env("MY_VAR", "myvalue"))` のように記述できます。
{{< /callout >}}

### DEF の定義 {#define-def}

デフォルト値を定義する領域です。ここで定義した変数は他のセクションから参照します。
独自の変数を定義したり、コマンドラインフラグ名を変更したりできます。
次の `LISTEN_HOST` は `--host` の値を使用し、フラグがない場合は `"127.0.0.1"` を使用します。

`"127.0.0.1"` を `"192.168.1.10"` に変更すると、デフォルト値が変わります。

また、`"--host"` を `"--bind"` に変更すると、`machbase-neo serve --host` の代わりに `machbase-neo serve --bind` を使用できます。

```hcl
define DEF {
    LISTEN_HOST       = flag("--host", "127.0.0.1")
    SHELL_PORT        = flag("--shell-port", "5652")
    MQTT_PORT         = flag("--mqtt-port", "5653")
    HTTP_PORT         = flag("--http-port", "5654")
    MACH_PORT         = flag("--mach-port", "5656")
}
```

### VARS の定義 {#define-vars}

よく使用する変数を定義します。

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

### ログ設定 {#로깅-설정}

| キー | 型 | 説明 |
|:----------------------------|:----------|----------------------------------------------------------|
| Console                     | bool      | コンソールへのログ出力                                  |
| Filename                    | string    | ログファイルのパス（`-` は標準出力。例: /logs/machbase-neo.log） |
| DefaultPrefixWidth          | int       | ログのプレフィックスの整列幅                                      |
| DefaultEnableSourceLocation | bool      | ソースファイル名と行番号を記録するかどうか                         |
| DefaultLevel                | string    | `TRACE`, `DEBUG`, `INFO`, `WARN`, `ERROR`                |
| Levels                      | array     | レベルオブジェクトの配列                                           |
| Append                      | bool      | 既存ログファイルへの追記                                |
| RotateSchedule              | string    | ログローテーションのスケジュール（例: "@midnight"）                       |
| MaxSize                     | int       | ログファイルの最大サイズ（MB）                                  |
| MaxBackups                  | int       | バックアップファイルの最大数                                      |
| MaxAge                      | int       | バックアップファイルの最大保持日数                                 |
| Compress                    | bool      | バックアップファイルの圧縮                                           |
| UTC                         | bool      | ログ時刻に UTC を使用                                       |

- レベルオブジェクト

| キー | 型 | 説明 |
|:----------------------------|:----------|----------------------------------------------------------|
| Pattern                     | string    | ロガー名の glob パターン                               |
| Level                       | string    | このロガーに適用するログレベル                             |

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

### サーバー設定 {#서버-설정}

データベースサーバーに関する設定を、以下で説明します。

#### MachbaseHome

| キー | 型 | 説明 |
|:----------------------------|:----------|----------------------------------------------------------|
| MachbaseHome                | string    | データベースファイルの保存ディレクトリ           |

#### Machbase

Machbase のコア設定は [設定プロパティリファレンス](/dbms/reference/configuration/configuration/) を参照してください。
[DBMS マニュアル全体](/dbms) も参照できます。


#### Shell

SSH で machbase-neo シェルにリモート接続するための設定です。`LISTEN_HOST` のデフォルトは `"127.0.0.1"` のため、同じホストからのみ接続できます。リモート接続を許可するには `"0.0.0.0"` またはホストの IP アドレスに変更してください。

{{< callout type="warning" >}}
**セキュリティ**<br/>
リモート接続を許可する前に、`SYS` アカウントのデフォルトパスワード `manager` を変更してください。
{{< /callout >}}

| キー | 型 | 説明 |
|:----------------------------|:-------------------|----------------------------------------------------------|
| Listeners                   | array of string    | 待ち受けアドレス（例: `tcp://127.0.0.1:5652`、`tcp://0.0.0.0:5652`）|
| IdleTimeout                 | duration           | 指定時間にわたって操作がない場合に SSH 接続を終了 |


#### Http

サーバーの HTTP リスナー設定です。

| キー | 型 | 説明 |
|:----------------------------|:-------------------|----------------------------------------------------------|
| Listeners                   | array of string    | 待ち受けアドレス                                                |
| EnableTokenAuth             | bool               | トークン認証を有効化（デフォルト `false`）                    |
| EnableWebUI                 | bool               | Web UI を有効化（デフォルト `true`）                               |

#### Mqtt

| キー | 型 | 説明 |
|:----------------------------|:-------------------|----------------------------------------------------------|
| Listeners                   | array of string    | 待ち受けアドレス                                                |
| MaxMessageSizeLimit         | int                | PUBLISH ペイロードの最大サイズ（デフォルト 1048576 = 1MB）             |
| EnableTokenAuth             | bool               | トークン認証を有効化（デフォルト `false`）                    |
| EnableTls                   | bool               | TCP リスナーの TLS を有効化（デフォルト `false`）                     |

### neo-server の設定 {#neo-server-config}

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
