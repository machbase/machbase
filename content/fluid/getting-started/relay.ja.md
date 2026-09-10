---
title: FLUID リレー
weight: 180
toc: true
---

## FLUID relay
リレープロキシは、クライアントとサーバーの間でメッセージを中継します。
FLUID リレープロキシは、ファイアウォールなどで遮断された環境で利用するため、
ファイアウォールの外にある FLUID サーバーの Broker に接続して中継します。

{{< figure src="../img/fluid-relay.jpg" width="700" >}}

- リバースプロキシと同じ機能を提供

## コマンドライン
```bash
fluid relay --config <path>
```

| フラグ | 短縮形 | 環境変数 | 必須 | 説明 |
|:-------------------|:------------:|:--------------------:|:----:|:----------------------|
| `--config <file>` | `-c <file>` | `FLUID_RELAY_CONFIG` | O | |
| `--verbose` | `-v` | | | 詳細なログを出力 |
| `--dry-run` | | | | 設定ファイルのエラーを確認 |
| `--broker` | | `FLUID_RELAY_BROKER` | | デフォルトの Broker アドレス |
| `--topic` | | `FLUID_RELAY_TOPIC` | | デフォルトのトピック |

複数の Broker を使う場合は、`--broker` を繰り返すか、アドレスをカンマ（,）で区切ります。

**環境変数の使用**
```sh
FLUID_RELAY_BROKER=secret@192.168.1.10:3000,secret@192.168.1.20:3000 fluid relay -c relay_config.yaml
```
