---
toc: true
title: サービスマネージャー
type: docs
weight: 100
---

`servicectl`コマンドは、サービスコントローラーを介して、長時間実行するJSHサービスを管理します。
サービス設定の読み込み、インストールと削除、開始と停止、現在の実行状態の取得を行えます。

## 概要 {#개요}

`servicectl`コマンドは、実行中のサービスコントローラーとJSON-RPCで通信します。
サービスを直接起動せず、以下の管理リクエストをコントローラーに渡します。

- 設定ファイルの読み込み
- 設定変更の適用
- JSONファイルまたはインラインオプションによるサービスのインストール
- サービスの開始と停止
- サービス状態の取得
- サービス登録の削除

## コントローラーのアドレス {#controller-address}

このコマンドには、サービスコントローラーのエンドポイントが必要です。
`--controller`オプションで直接指定するか、`SERVICE_CONTROLLER`環境変数で渡せます。

`servicectl`をmachbase-neoランタイムから実行すると、ランタイムが`SERVICE_CONTROLLER`を自動的に
設定します。通常のJSHサービス管理では、`--controller`を毎回明示する必要はないため、
以下の例では、読みやすさのために省略します。

対応するコントローラーアドレスの形式は以下のとおりです。

- `host:port`
- `tcp://host:port`
- `unix://path`

<h6>構文</h6>

```sh
servicectl [--controller=<addr>] <command> [args...]
```

<h6>共通オプション</h6>

- `-c, --controller <endpoint>` TCPまたはUnixソケット形式のコントローラーアドレス
- `-t, --timeout <msec>` RPCのタイムアウト（ミリ秒）。既定値`5000`
- `-h, --help` ヘルプを表示

<h6>使用例</h6>

```sh
/work > servicectl status
```

## コマンド {#commands}

`servicectl`コマンドは、以下のサブコマンドに対応しています。

- `read`
- `update`
- `reload`
- `install <config.json>`
- `install --name <name> --executable <path> [--arg <arg> ...] [--working-dir <dir>] [--enable] [--env KEY=VALUE ...]`
- `uninstall <service_name>`
- `status [service_name]`
- `start <service_name>`
- `stop <service_name>`
- `details get <service_name> [key] [--format box|json]`
- `details set <service_name> <key> <value> [--detail-type <string|number|boolean|bool|object|json>]`
- `details delete <service_name> <key>`

## サービス設定の形式 {#서비스-설정-형식}

サービス定義はJSONオブジェクトです。

```json
{
  "name": "alpha",
  "enable": true,
  "working_dir": "/work/app",
  "environment": {
    "APP_MODE": "prod",
    "PORT": "8080"
  },
  "executable": "server.js",
  "args": ["--port", "8080"]
}
```

主なフィールドは以下のとおりです。

| フィールド | 型 | 説明 |
| --- | --- | --- |
| `name` | `String` | サービス名 |
| `enable` | `Boolean` | サービスを有効にするかどうか |
| `working_dir` | `String` | サービスプロセスの作業ディレクトリ |
| `environment` | `Object` | `KEY: VALUE`形式の環境変数マップ |
| `executable` | `String` | 実行ファイルのパスまたはコマンド名 |
| `args` | `Array<String>` | コマンドライン引数の一覧 |

## status {#status}

サービス一覧全体、または単一サービスの詳細を表示します。

<h6>構文</h6>

```sh
servicectl status [service_name]
```

サービス名を省略すると、名前、有効化状態、実行状態、PID、実行ファイルを表で出力します。

<h6>使用例: サービス一覧</h6>

```sh
/work > servicectl status
┌───────┬─────────┬─────────┬─────┬────────────┐
│ NAME  │ ENABLED │ STATUS  │ PID │ EXECUTABLE │
├───────┼─────────┼─────────┼─────┼────────────┤
│ alpha │ yes     │ running │ 101 │ echo       │
│ beta  │ no      │ stopped │ -   │ /bin/date  │
└───────┴─────────┴─────────┴─────┴────────────┘
```

サービス名を指定すると、作業ディレクトリ、環境変数、直近の出力行を含む詳細な状態を表示します。

<h6>使用例: 単一サービス</h6>

```sh
/work > servicectl status alpha
[alpha] ENABLED
  status: running
  exit_code: 0
  pid: 55
  start: echo [ hello, world ]
  cwd: /work
  environment:
    A=1
    B=2
  output:
    line-6
    ...
    line-25
```

## read {#read}

コントローラーの設定ディレクトリからサービス設定ファイルを読み込み、変更状態を報告します。

<h6>構文</h6>

```sh
servicectl read
```

結果は1つの表で出力し、各行の`STATUS`列に、
`UNCHANGED`、`ADDED`、`UPDATED`、`REMOVED`、`ERRORED`の状態を表示します。

この表は、`servicectl status`の一覧と同じpretty box形式で表示します。

<h6>使用例</h6>

```sh
/work > servicectl read
┌────────┬───────────┬────────────┬──────────────┬─────────────┬────────────┐
│ NAME   │ STATUS    │ EXECUTABLE │ READ_ERROR   │ START_ERROR │ STOP_ERROR │
├────────┼───────────┼────────────┼──────────────┼─────────────┼────────────┤
│ alpha  │ UNCHANGED │ echo       │              │             │            │
│ beta   │ ADDED     │ node       │              │             │            │
│ old    │ REMOVED   │ sleep      │              │             │            │
│ broken │ ERRORED   │            │ invalid json │             │            │
└────────┴───────────┴────────────┴──────────────┴─────────────┴────────────┘
```

## updateとreload {#update-와-reload}

両コマンドとも、コントローラーに設定変更の適用を要求します。

- `update`：読み込み済みの変更だけを適用します。追加、削除、変更されたサービスだけを反映し、他のサービスは維持します。
- `reload`：設定ファイルを再読み込みし、実行中のすべてのサービスを停止して変更を反映した後、`enable=true`のサービスだけを再起動します。

<h6>構文</h6>

```sh
servicectl update
servicectl reload
```

出力は、2つのセクションで構成されます。

- `ACTIONS`: `UPDATE stop`、`UPDATE start`、`RELOAD stop`、`RELOAD start`などの実行した操作の一覧
- `SERVICES`: 適用後のサービス状態表

## install {#install}

JSONファイルまたはインラインオプションでサービスをインストールします。
インストールに成功すると、コントローラーはサービス定義を`/etc/services/<name>.json`に保存します。
ファイル名は、JSONファイルの`name`値、または`--name`オプションで決まります。

### JSONファイルからのインストール {#json-파일로-설치}

<h6>構文</h6>

```sh
servicectl install <config.json>
```

<h6>使用例</h6>

```sh
/work > servicectl install svc.json
```

たとえば、`svc.json`に`"name": "alpha"`が含まれている場合、設定は
`/etc/services/alpha.json`に保存されます。

### インラインオプションでのインストール {#inline-옵션으로-설치}

<h6>構文</h6>

```sh
servicectl install \
  --name <service_name> \
  --executable <path> \
  [--working-dir <dir>] \
  [--enable] \
  [--arg <arg> ...] \
  [--env KEY=VALUE ...]
```

<h6>インラインインストールのオプション</h6>

- `-n, --name <name>` サービス名
- `-x, --executable <path>` 実行ファイルのパスまたはコマンド名
- `-w, --working-dir <dir>` 作業ディレクトリ
- `--enable` 直ちに有効化
- `-a, --arg <arg>` 実行引数を1つ追加。繰り返し指定可能
- `-e, --env KEY=VALUE` 環境変数を1つ追加。繰り返し指定可能

<h6>使用例</h6>

```sh
/work > servicectl install \
  --name svc-inline \
  --executable node \
  --working-dir /work/app \
  --enable \
  --arg app.js \
  --arg --port \
  --arg 8080 \
  --env APP_MODE=prod \
  --env PORT=8080
```

このインライン方式でも、コントローラー側に`/etc/services/svc-inline.json`ファイルを作成します。

このコマンドは、まず`RESULT`表を出力し、続いて`SERVICE`の詳細を表示します。

## startとstop {#start-와-stop}

指定したサービスを開始・停止します。

<h6>構文</h6>

```sh
servicectl start <service_name>
servicectl stop <service_name>
```

出力には、操作結果と現在のサービス状態が含まれます。

<h6>使用例</h6>

```sh
/work > servicectl start alpha
/work > servicectl stop alpha
```

## details {#details}

サービスが提供するランタイムのdetail値を取得・設定・削除します。
これらの値は静的なサービス設定とは別で、ヘルス状態、カウンター、ラベル、
ユーザー定義の構造化状態などのランタイムメタデータを保持するために使用します。

<h6>構文</h6>

```sh
servicectl details get <service_name> [key] [--format box|json]
servicectl details set <service_name> <key> <value> [--detail-type <string|number|boolean|bool|object|json>]
servicectl details delete <service_name> <key>
```

<h6>detailsオプション</h6>

- `--format <box|json>` `details get`の出力形式。既定値`box`
- `--detail-type <type>` `details set`の値の型。既定値`string`

対応するdetail値の型は以下のとおりです。

- `string`：`--detail-type`を省略した場合の既定値
- `number`
- `boolean`または`bool`
- `object`または`json`

型の処理規則は以下のとおりです。

- `string`は、入力した文字列をそのまま保存します
- `number`は、入力値をJSONのnumberとして解析します
- `boolean`と`bool`は、入力値をJSONの`true`または`false`として解析します
- `object`と`json`は、入力値をJSONオブジェクトとして解析し、配列やスカラーは許可しません

`details set`は、1回のRPCリクエストで処理し、upsertとして動作します。
キーが存在する場合は値を上書きし、なければ新規作成します。

`--format json`を使用すると、

- `servicectl details get <service_name>`は、detailsオブジェクト全体をJSONで出力します
- `servicectl details get <service_name> <key>`は、そのキーだけを含むJSONオブジェクトを出力します

<h6>使用例: box出力</h6>

```sh
/work > servicectl details get alpha
DETAILS (3)
┌─────────┬─────────┬────────────────────┐
│ KEY     │ TYPE    │ VALUE              │
├─────────┼─────────┼────────────────────┤
│ enabled │ boolean │ true               │
│ labels  │ object  │ {"tier":"gold"}    │
│ retries │ number  │ 3                  │
└─────────┴─────────┴────────────────────┘
```

<h6>使用例: JSON出力</h6>

```sh
/work > servicectl details get alpha labels --format json
{
  "labels": {
    "tier": "gold"
  }
}
```

<h6>使用例: 値の設定</h6>

```sh
/work > servicectl details set alpha mode warm
/work > servicectl details set alpha retries 3 --detail-type number
/work > servicectl details set alpha enabled true --detail-type bool
/work > servicectl details set alpha labels '{"tier":"gold"}' --detail-type json
```

<h6>使用例: キーの削除</h6>

```sh
/work > servicectl details delete alpha labels
```

## uninstall {#uninstall}

サービス登録を削除します。

<h6>構文</h6>

```sh
servicectl uninstall <service_name>
```

<h6>使用例</h6>

```sh
/work > servicectl uninstall alpha
RESULT
uninstall alpha yes removed
```

## 一般的な作業手順 {#일반적인-작업-순서}

まず、サービスのJSONファイルを用意します。

```json
{
  "name": "alpha",
  "enable": true,
  "working_dir": "/work",
  "executable": "echo",
  "args": ["hello", "world"]
}
```

次に、以下の手順で管理できます。

```sh
/work > servicectl install alpha.json
/work > servicectl status
/work > servicectl stop alpha
/work > servicectl start alpha
/work > servicectl uninstall alpha
```

## 注意 {#참고}

- `servicectl`コマンドには、アクセス可能なコントローラーエンドポイントが必要です。
- `status`は、引数がなければ全一覧を、引数があれば単一サービスの詳細を出力します。
- `install`では、設定ファイルのパスとインラインインストールのオプションを併用できません。
- インラインの`--env`値は、必ず`KEY=VALUE`形式にしてください。
- 相対パスの設定ファイルは、現在の作業ディレクトリを基準に解釈します。
