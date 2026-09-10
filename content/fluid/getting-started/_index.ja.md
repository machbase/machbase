---
title: はじめに
weight: 100
toc: true
---

## 概要

`fluid` は高速で柔軟なネットワークプロキシサーバーで、次の機能を提供します。
- FLUID リバースプロキシ
- FLUID 逆方向接続リレープロキシ

{{< children_toc />}}

## 設定

`fluid` の設定ファイルは YAML 形式で記述します。

### FLUID server の設定例

<details>
<summary>serve_1.yaml</summary>
<div markdown="1">

```yaml
MyID: 1 # 変更してください

HttpRouter:
- Host: [ example.com ]              # 単一ホストのマッチャー
  Route:
  - Path:
    - \~ /api/
    Proxy:
      Destination:
      - http://10.0.1.1:8888
- Host: [ 127.0.0.1, '\g local*' ]    # 複数ホストのマッチャー
  Server: [ http_8081, http_8080 ]
  Healthz:
    Path: /healthz
    AccessPolicy: allow-only-local
  Statz:
    Path: /statz
    AccessPolicy: allow-only-local
  AccessPolicy: allow-all
  Route:
  - Path:
    - \~ /db/                     # 前方一致
    - \g /web/*                   # glob 一致
    -    /web                     # 完全一致
    Proxy:
      Destination:
      - http://127.0.0.1:5654
      - http://127.0.0.1:5654
      Routing: hash                 # random, hash, hash-host（デフォルト: hash）
      Relay: local-relay
    # Rewriter: |
    #   REWRITE(topic(trimSuffix(HOST, ":8080") | replace(".", "_")))
    AccessPolicy: allow-only-local
  - Path:
    - \r .+(.yml|.yaml)$          # 正規表現
    - \e hasSuffix(PATH, '.yml')  # 式の評価
    Static:
      RootDir: ./serve/test/
    Rewriter: |                     # 複数行スクリプト。変数には 'let' を使用
      let rpath = trimPrefix(PATH, "/static/test/");
      let file = hasSuffix(rpath, ".yaml") ? trimSuffix(rpath, ".yaml") : trimSuffix(rpath, ".yml");
      REWRITE(path("/" + file + ".yaml"))
    AccessPolicy: allow-all
HttpLog: access-log

# HTTP リスナー '<ip_addr>:<port>' または '<ip_addr>:auto-cert'
# ':auto-cert' を指定すると <ip_addr>:443 と <ip_addr>:80 で待ち受ける
# Tls/Cert と Tls/Key の設定は無視される
# 例: 0.0.0.0:auto-cert
HttpServer:
- Name: http_8080
  Listen: 127.0.0.1:8080
  TlsCert:  # HTTPS を有効にする証明書（.PEM）のパス
  TlsKey:   # HTTPS を有効にする秘密鍵（.PEM）のパス
  AccessPolicy: allow-only-local
- Name: http_8081
  Listen: 127.0.0.1:8081
  AccessPolicy: allow-all

TcpServer:
- Name: tcp_8088
  Listen: 127.0.0.1:8088
  Destination: [ 127.0.0.1:5652 ]
  Relay: local-relay
  AccessPolicy: allow-only-local

Relay:
- Name: local-relay
  InTopic:  net-over-nats.to-fluid
  OutTopic: net-over-nats.from-fluid

AccessPolicy:
- Name: allow-all
  Policy: NONE
- Name: allow-only-local
  Policy: ALLOW
  Allow:
  - \~ 127.0.
- Name: deny-only-local
  Policy: DENY
  Deny:
  - \g 127.0.0.*            # glob 一致

AutoCert:
  Email: admin@example.com
  Store: fluid-auto-cert
  Replica: 1
  Blacklist:
  - stress.com

Log:
- Name: console-log  # "default" は fluid のデフォルトロガー用に予約
  Level: INFO        # DEBUG, INFO, WARN, ERROR
  AddSource: true
  Format: dev        # json, text, dev, http
- Name: file-log     # "default" は fluid のデフォルトロガー用に予約
  Level: DEBUG       # DEBUG, INFO, WARN, ERROR
  File:
    Filename: ./tmp/fluid.log
    MaxSize: 2       # 最大ファイルサイズ（MB）
    MaxAge: 3        # 古いログファイルの最大保持日数
    MaxBackups: 5    # 古いログファイルの最大保持数
    LocalTime: true  # UTC を使う場合は false
    Compress: false  # gzip 圧縮を使う場合は true      
- Name: access-log
  Level: DEBUG       # DEBUG, INFO, WARN, ERROR
  Format: http
  File:
    Filename: ./tmp/fluid-http.log
    MaxSize: 2       # 最大ファイルサイズ（MB）
    MaxAge: 3        # 古いログファイルの最大保持日数
    MaxBackups: 5    # 古いログファイルの最大保持数
    LocalTime: true  # UTC を使う場合は false
    Compress: false  # gzip 圧縮を使う場合は true      
- Name: tee-log
  Default: true
  Tee:
  - console-log
  - file-log

Broker:
  Listen: 127.0.0.1:3000
  StoreDir: ./tmp/data
  Authorization: s3creT
  Debug: true
  LogFile: ./tmp/fluid-nats.log
  NoLog: true
```

</div>
</details>

### FLUID serve broker の設定例
<details>
<summary>serve_brkd.yaml</summary>
<div markdown="1">

```yaml
MyID: 10 # 変更してください

Broker:
  Host: 127.0.0.1
  Port: 3000
  StoreDir: ./tmp/data
  Authorization: s3creT
  Debug: true
  LogFile: ./tmp/fluid-nats.log
  NoLog: true
```

</div>
</details>

### FLUID relay の設定例
<details>
<summary>relay_1.yaml</summary>
<div markdown="1">

```yaml
Relay:
- Broker:
  - nats://s3creT@127.0.0.1:3000
  Topic:  net-over-nats.from-fluid
  Channel: 1024
  ReadBufferSize: 524288 #512K
  Destination:
  - Host: 127.0.0.1/32
    Port: 5652-5654

Logs:
- Name: console-log
  Level: DEBUG # DEBUG, INFO, WARN, ERROR
  Default: true
  File:
    Filename: #./tmp/relay-1.log # デフォルトは標準出力
    Append: true     # fluid の起動・再起動時に新規ログを作る場合は false
    MaxSize: 2       # 最大ファイルサイズ（MB）
    MaxAge: 3        # 古いログファイルの最大保持日数
    MaxBackups: 5    # 古いログファイルの最大保持数
    LocalTime: true  # UTC を使う場合は false
    Compress: false  # gzip 圧縮を使う場合は true
```

</div>
</details>
