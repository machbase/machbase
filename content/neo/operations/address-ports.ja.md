---
toc: true
title: IPアドレスとポート
type: docs
weight: 12
---

## バインドアドレス {#바인드-주소}

machbase-neoは、セキュリティのため既定ではlocalhostでのみ待ち受けます。リモートホストのクライアントがネットワーク経由でデータを読み書きするには、起動時に`--host <bind address>`オプションでバインドアドレスを指定してください。

すべてのアドレスで接続を受け付けるには、`0.0.0.0`を使用します。

```sh
machbase-neo serve --host 0.0.0.0
```

特定のアドレスでのみ接続を受け付けるには、ホストのIPアドレスを指定します。

```sh
machbase-neo serve --host 192.168.1.10
```

## 待ち受けポート {#수신-포트}

プロトコル別のポートを制御するフラグは以下のとおりです。

| フラグ             | 既定値          | 説明                                      |
|:-----------------|:----------------:|-------------------------------------------|
| `--shell-port`   | `5652`           | SSHの待ち受けポート                              |
| `--mqtt-port`    | `5653`           | MQTTの待ち受けポート                             |
| `--http-port`    | `5654`           | HTTPの待ち受けポート                             |
| `--grpc-port`    | `5655`           | gRPCの待ち受けポート                             |
| `--grpc-sock`    | `mach-grpc.sock` | gRPCのUnixドメインソケット                    |
| `--grpc-insecure`| `false`          | gRPCの待ち受けポートでTLSを無効化            |
| `--mach-port`    | `5656`           | JDBC/ODBCドライバー用のMachbaseネイティブポート |

特定のネットワークインターフェースにのみバインドするには、以下の待ち受けホスト/ポートのフラグを使用します。

| フラグ                   | 既定値                | 説明                                  |
|:-----------------------|:-----------------------|---------------------------------------|
| `--mach-listen-host`   | `--host`の値            |                                       |
| `--mach-listen-port`   | `--mach-port`の値       |                                       |
| `--shell-listen-host`  | `--host`の値            |                                       |
| `--shell-listen-port`  | `--shell-port`の値      |                                       |
| `--grpc-listen-host`   | `--host`の値            |                                       |
| `--grpc-listen-port`   | `--grpc-port`の値       |                                       |
| `--grpc-listen-sock`   | `--grpc-sock`の値       |                                       |
| `--http-listen-host`   | `--host`の値            |                                       |
| `--http-listen-port`   | `--http-port`の値       |                                       |
| `--mqtt-listen-host`   | `--host`の値            |                                       |
| `--mqtt-listen-port`   | `--mqtt-port`の値       |                                       |
