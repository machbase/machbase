---
title: Relay 設定ファイル
weight: 340
toc: true
---

## Relay 設定ファイル

### トップレベル

| キー | 型 | 必須 | 説明 |
|:---------------------|:------------:|:----:|:--------------------|
| Verbose | boolean | | |
| Relay | obj array | | |
| Log | obj array | | |
| ShutdownTimeout | int | | シャットダウンの最大待機時間（秒） |


### Relay

| キー | 型 | 必須 | 説明 |
|:---------------------|:------------:|:----:|:--------------------|
| Broker | string array | O | 未指定なら `--broker` で指定したデフォルト Broker を使用 |
| Topic | string | O | 未指定なら `--topic` で指定したデフォルトトピックを使用 |
| Destination | obj array | O | |
| ReadBufferSize | int | | デフォルト32768（32K） |
| Channel | int | | チャネルバッファサイズ。デフォルト1000 |


### Destination

| キー | 型 | 必須 | 説明 |
|:---------------------|:------------:|:----:|:--------------------|
| Net | string | | デフォルト `tcp` |
| Host | string | | CIDR 形式。例: `192.168.1.1/24` |
| Port | string | | カンマ（,）区切りのポート範囲。例: `8080,5652-5656` |


## 例

### 基本例

```yaml
Relay:
- Broker:
  - nats://secret@127.0.0.1:3000
  Topic:  net-over-nats.from-fluid
  Channel: 1024
  ReadBufferSize: 524288 #512K
  Destination:
  - Host: '127.0.0.1/32'
    Port: 5652-5654

Logs:
- Name: console-log
  Level: INFO     # DEBUG, INFO, WARN, ERROR
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
