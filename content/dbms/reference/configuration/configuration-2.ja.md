---
type: docs
title: '16.2.2 クラスター設定プロパティ辞典'
weight: 20
toc: true
---

Cluster Editionでは、`$MACHBASE_COORDINATOR_HOME/conf/`、`$MACHBASE_BROKER_HOME/conf/`、`$MACHBASE_WAREHOUSE_HOME/conf/`にある各ノードの設定ファイルでクラスターの動作を制御します。

このページでは、運用時に頻繁に確認する主なクラスターのプロパティを示します。

## Coordinator 設定

Coordinatorは、クラスター全体のメタデータとノードの状態を管理します。

| プロパティ | デフォルト値 | 説明 |
|----------|--------|------|
| `CLUSTER_LINK_HOST` | - | CoordinatorがバインドするIPアドレス |
| `CLUSTER_LINK_PORT_NO` | 3868 | クラスター内部通信ポート |
| `CLUSTER_LINK_THREAD_COUNT` | 16 | クラスターリンク処理スレッド数 |
| `CLUSTER_LINK_MAX_LISTEN` | 512 | クラスターリンクの最大listen接続数 |
| `CLUSTER_LINK_MAX_POLL` | 4096 | クラスターリンクの最大pollイベント数 |
| `CLUSTER_LINK_BUFFER_SIZE` | 33554432 | クラスターリンクのバッファーサイズ（バイト）。デフォルトは32MB |
| `HTTP_ADMIN_PORT` | 5779 | Coordinator/Deployer管理RESTポート |
| `HTTP_THREAD_COUNT` | 2 | 管理RESTリクエスト処理スレッド数 |

`HTTP_ADMIN_PORT`は環境変数`MACHBASE_HTTP_ADMIN_PORT`でも指定できます。このポートは
クラスターの管理リクエスト専用であり、SQLクエリやデータ入力には使用しません。

## クラスターリンクのタイムアウト設定

すべての値の単位はマイクロ秒（μs）です。

| プロパティ | デフォルト値(μs) | 説明 |
|----------|-----------|------|
| `CLUSTER_LINK_ACCEPT_TIMEOUT` | 5000000 | acceptタイムアウト（5秒） |
| `CLUSTER_LINK_CHECK_INTERVAL` | 1000000 | 接続状態の確認間隔（1秒） |
| `CLUSTER_LINK_CONNECT_RETRY_TIMEOUT` | 60000000 | 接続再試行の最大時間（60秒） |
| `CLUSTER_LINK_CONNECT_TIMEOUT` | 5000000 | 接続タイムアウト（5秒） |
| `CLUSTER_LINK_HANDSHAKE_TIMEOUT` | 5000000 | ハンドシェイクタイムアウト（5秒） |
| `CLUSTER_LINK_RECEIVE_TIMEOUT` | 30000000 | 受信タイムアウト（30秒） |
| `CLUSTER_LINK_SEND_TIMEOUT` | 30000000 | 送信タイムアウト（30秒） |
| `CLUSTER_LINK_REQUEST_TIMEOUT` | 60000000 | リクエストタイムアウト（60秒） |
| `CLUSTER_LINK_SESSION_TIMEOUT` | 3600000000 | セッションタイムアウト（1時間） |
| `CLUSTER_LINK_LONG_WAIT_INTERVAL` | 1000000 | 長時間待機の間隔（1秒） |
| `CLUSTER_LINK_LONG_TERM_CALLBACK_INTERVAL` | 1000000 | 長期コールバック間隔（1秒） |

## Broker 設定

Brokerはクライアントのクエリを受け付け、Warehouseに分散して処理します。Brokerの`machbase.conf`には
サーバー共通の設定とクラスター設定を指定します。サポートするプロパティとデフォルト値はEditionと
ノードの役割によって異なるため、Standard Editionの設定ファイルをそのまま適用しないでください。

| プロパティ | デフォルト値 | 説明 |
|----------|--------|------|
| `PORT_NO` | 5656 | クライアント接続ポート |
| `QUERY_PARALLEL_FACTOR` | 4 | 並列クエリ処理スレッド数（Clusterのデフォルト値） |
| `CLUSTER_LINK_HOST` | - | Brokerがクラスター通信にバインドするIP |
| `CLUSTER_LINK_PORT_NO` | - | Brokerのクラスター通信ポート |

## Warehouse 設定

Warehouseは実データを保存・処理するノードです。ストレージ設定と併せて次のクラスター設定を
使用します。`DDL_LOCK_TIMEOUT`などStandard Edition専用のプロパティは、Cluster Editionでは
サポートしません。

| プロパティ | デフォルト値 | 説明 |
|----------|--------|------|
| `PORT_NO` | 5656 | Warehouseのサービスポート |
| `CLUSTER_LINK_HOST` | - | Warehouseがクラスター通信にバインドするIP |
| `CLUSTER_LINK_PORT_NO` | - | Warehouseのクラスター通信ポート |
| `DBS_PATH` | ?/dbs | Warehouseのデータファイル保存先 |

## クラスターの状態確認

`machcoordinatoradmin --configure`でクラスターの設定値を表示できます。

```bash
machcoordinatoradmin --configure
```

特定の設定値だけを確認するには、`--configuration=name`オプションを使用します。

```bash
machcoordinatoradmin --configuration=decision
```

## クラスターのポート構成例

単一ホストにクラスターを構成する場合のポート割り当て例です。

| ノード | サービスポート | HTTPポート | クラスターリンクポート |
|------|------------|-----------|------------------|
| Coordinator | - | 5102 | 5101 |
| Deployer | - | - | 5201 |
| Broker | 5757 | 5302 | 5301 |
| Warehouse-A1 | 5400 | 5402 | 5401 |
| Warehouse-A2 | 5500 | 5502 | 5501 |
