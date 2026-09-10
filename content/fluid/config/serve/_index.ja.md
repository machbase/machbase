---
title: Server 設定ファイル
weight: 320
toc: true
---

## Server 設定ファイル

### トップレベル

| キー | 型 | 必須 | 説明 |
|:---------------------|:------------:|:----:|:--------------------|
| MyID | int | | 任意の数値、0～1000 |
| HttpServer | obj array | | HTTP リスナー情報の一覧 |
| HttpRouter | obj array | O | HTTP ルーター情報の一覧 |
| HttpLog | string | | HTTP ロガー名 |
| TcpServer | obj array | | TCP リスナー情報の一覧 |
| Relay | obj array | | リレー情報の一覧 |
| AccessPolicy | obj array | | アクセスポリシー名 |
| AutoCert | obj | | 自動証明書管理（無停止での証明書自動更新） |
| Log | obj array | | ロガー情報の一覧 |
| Verbose | boolean | | --verbose、真偽値（true、false） |
| ShutdownTimeout | int | | シャットダウンの最大待機時間（秒） |
| Broker | obj | | Broker 情報 |

### TcpServer
TCP リスナーの情報です。

| キー | 型 | 必須 | 説明 |
|:---------------------|:------------:|:----:|:--------------------|
| Name | string | | TcpServer 名 |
| Listen | string | O | ip:port |
| Destination | string array | | 接続先一覧。複数の場合はラウンドロビンで使用 |
| Routing | string | | `random`、`hash-host`（src+dst）、`hash`（src）。デフォルト: `random` |
| Relay | string | | リレー名 |
| ConnectTimeout | int | | 接続タイムアウト（秒） |
| KeepAlive | int | | キープアライブのタイムアウト（秒） |
| AccessPolicy | string | | アクセスポリシー名 |


### HttpServer
HTTP リスナー情報。`<ip_addr>:<port>` または `<ip_addr>:auto-cert` を指定します。
`:auto-cert` の場合、fluid は `<ip_addr>:443` と `<ip_addr>:80` で待ち受け、
`Tls/Cert` と `Tls/Key` の設定を無視します。
例: 0.0.0.0:auto-cert

| キー | 型 | 必須 | 説明 |
|:---------------------|:------------:|:----:|:--------------------|
| Name | string | O | HttpServer 名 |
| Listen | string | O | ip:port |
| ReadTimeout | int | | 読み取りタイムアウト。デフォルト: 0 |
| WriteTimeout | int | | 書き込みタイムアウト。デフォルト: 0 |
| IdleTimeout | int | | アイドルタイムアウト。デフォルト: 0 |
| SockLinger | int | | SO_LINGER。デフォルト: 0 |
| SockDelay | bool | | `true` なら SO_NODELAY を無効化。デフォルト: false |
| TlsCert | string | | 証明書ファイルのパス |
| TlsKey | string | | 秘密鍵ファイルのパス |
| AccessPolicy | string | | アクセスポリシー名 |

### HttpRouter
`Host` には後述のマッチャーを使用できます。

| キー | 型 | 必須 | 説明 |
|:---------------------|:------------:|:----:|:--------------------|
| Server | string array | | HttpServer 名 |
| Host | string array | | HTTP ホスト名 |
| Route | obj array | | |
| Healthz | obj | | |
| AccessPolicy | string | | アクセスポリシー名 |

### HttpRouter/Route
`Path` と `Method` には後述のマッチャーを使用できます。
  
| キー | 型 | 必須 | 説明 |
|:---------------------|:------------:|:----:|:--------------------|
| Path | string array | | |
| Method | string array | | |
| Rewriter | string | | |
| Proxy | obj | | |
| Static | obj | | |
| AccessPolicy | string | | アクセスポリシー名 |

### HttpRouter/Route/Proxy

| キー | 型 | 必須 | 説明 |
|:---------------------|:------------:|:----:|:--------------------|
| Destination | string array | | |
| Routing | string | | random、hash、hash-host（デフォルト: hash） |
| InsecureSkipVerify | bool | | |
| ForwardProxy | string | | |
| Relay | string | | |
| Timeout | int | | デフォルト3 |
| KeepAlive | int | | サポートされる場合のネットワークキープアライブ |
| DisableKeepAlives | bool | | true なら HTTP キープアライブを無効化 |
| TLSHandshakeTimeout | int | | デフォルト10 |
| DisableCompression | bool | | true なら Transport の圧縮を禁止 |
| MaxIdleConns | int | | デフォルト10 |
| MaxIdleConnsPerHost | int | | デフォルト2 |
| MaxConnsPerHost | int | | デフォルト0、無制限 |
| IdleConnTimeout | int | | デフォルト60 |
| ResponseHeaderTimeout | int | | デフォルト30 |
| ExpectContinueTimeout | int | | デフォルト0 |
| ForceAttemptHTTP2 | bool | | デフォルトfalse |
| WriteBufferSize | int | | ゼロの場合はデフォルト4096 |
| ReadBufferSize | int | | ゼロの場合はデフォルト4096 |


### HttpRouter/Route/Static

| キー | 型 | 必須 | 説明 |
|:---------------------|:------------:|:----:|:--------------------|
| RootDir | string | | |

### HttpRouter/Healthz

| キー | 型 | 必須 | 説明 |
|:---------------------|:------------:|:----:|:--------------------|
| Path | string | | デフォルト `/healthz` |
| Status | int | | デフォルト `200` |
| Text | string | | デフォルト `ready.` |
| AccessPolicy | string | | アクセスポリシー名 |

### AutoCert

| キー | 型 | 必須 | 説明 |
|:---------------------|:------------:|:----:|:--------------------|
| Email | string | | |
| Blacklist | string array | | |
| RenewBefore | int | | 日数 |

- 共有ストア

| キー | 型 | 必須 | 説明 |
|:---------------------|:------------:|:----:|:--------------------|
| Store | string | | |
| Replica | int | | |
| Broker | string array | | |
| MaxReconnect | int | | 負の値なら再接続を無期限に試行 |

- ディレクトリストア

| キー | 型 | 必須 | 説明 |
|:---------------------|:------------:|:----:|:--------------------|
| StoreDir | string | | |

### AccessPolicy
`Allow` と `Deny` には後述のマッチャーを使用できます。

| キー | 型 | 必須 | 説明 |
|:---------------------|:------------:|:----:|:--------------------|
| Name | string | O | |
| Policy | string | O | NONE, DENY, ALLOW, DENY_ALLOW, ALLOW_DENY |
| Allow | string array | | 許可リスト |
| Deny | string array | | 拒否リスト |

### Relay

| キー | 型 | 必須 | 説明 |
|:---------------------|:------------:|:----:|:--------------------|
| Name | string | O | |
| Broker | string array | | 空の場合は内部 Broker を使用 |
| InTopic | string | O | |
| OutTopic | string | O | |
| ConnectTimeout | int | | デフォルト3 |
| ReadTimeout | int | | デフォルト3 |
| WriteTimeout | int | | デフォルト3 |

### Broker

| キー | 型 | 必須 | 説明 |
|:---------------------|:------------:|:----:|:--------------------|
| ServerName | string | | デフォルト: `fluid_`+host_addr |
| Listen | string | O | Broker の待ち受けアドレス。デフォルト: `127.0.0.1:3000` |
| ClientAdvertise | string | | |
| StoreDir | string | O | |
| ReadyTimeout | int | | 秒。デフォルト: `5` |
| LogTime | bool | | デフォルト: `true` |
| NoLog | bool | | デフォルト: `false` |
| LogSizeLimit | int | | デフォルト: `104857600`（100M） |
| LogMaxFiles | int | | デフォルト: `1` |
| TraceVerbose | bool | | デフォルト: `false` |
| Authorization | string | | |
| JetStream | bool | | デフォルト: `true` |
| JetStreamMaxMemory | int | | デフォルト: `1073741824`（1G） |
| JetStreamMaxStore | int | | デフォルト: `5250048000`（5G） |
| Cluster | obj | | クラスターの有効化 |
| Routes | string array | | クラスターのルーティング |

### Broker/Cluster

| キー | 型 | 必須 | 説明 |
|:---------------------|:------------:|:----:|:--------------------|
| Name | string | O | ノード名 |
| Listen | string | O | クラスターノードの待ち受けアドレス（host:port） |
| Advertise | string | | アドバタイズするアドレス |
| NoAdvertise | bool | | デフォルト: `false` |
| ConnectRetries | int | | |
| PoolSize | int | | |

### Log

| キー | 型 | 必須 | 説明 |
|:---------------------|:------------:|:----:|:--------------------|
| Name | string | O | ロガー名 |
| Level | string | O | DEBUG, INFO, WARN, ERROR |
| AddSource | bool | | ソースファイル名と行番号を追加 |
| Format | string | | `json`, `text`, `dev` |
| File | obj | | ファイルロガー設定 |
| Tee | string array | | Tee ロガー。ロガー名の配列 |

`File` と `Tee` が未定義の場合、ログを標準出力へ出力します。

### Log/File

| キー | 型 | 必須 | 説明 |
|:---------------------|:------------:|:----:|:--------------------|
| Filename | string | | ファイルパス |
| MaxSize | int | | ログファイルの最大サイズ（MB） |
| MaxAge | int | | バックアップログの保持日数 |
| MaxBackups | int | | 保持するバックアップログ数 |
| LocalTime | bool | | UTC ではなく現地時刻を使用 |
| Compress | bool | | バックアップログを圧縮 |

### マッチャー
| マッチャー           | 接頭辞 | 例                 |
|:---------------------|:------:|:---------------------|
| 前方一致         | `\~`   | `\~ /db/`            |
| glob 一致           | `\g`   | `\g /web/*`          |
| 完全一致          | なし   | `/web`               |
| 正規表現   | `\r`   | `\r .+(.yml|.yaml)$` |
| 式の評価       | `\e`   | `\e hasSuffix(PATH, '.yml')` |
