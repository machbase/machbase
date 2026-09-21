---
layout : post
title : プロパティ（Cluster）
type : docs
toc: true
weight: 0
---

[共通プロパティ](../property)とは別に、Cluster Edition でのみ使用できるプロパティを説明します。

## 目次 {#index}

- [目次](#index)
  - [CLUSTER_LINK_ACCEPT_TIMEOUT](#cluster_link_accept_timeout)
  - [CLUSTER_LINK_BUFFER_SIZE](#cluster_link_buffer_size)
  - [CLUSTER_LINK_CHECK_INTERVAL](#cluster_link_check_interval)
  - [CLUSTER_LINK_CONNECT_RETRY_TIMEOUT](#cluster_link_connect_retry_timeout)
  - [CLUSTER_LINK_CONNECT_TIMEOUT](#cluster_link_connect_timeout)
  - [CLUSTER_LINK_ERROR_ADD_ORIGIN_HOST](#cluster_link_error_add_origin_host)
  - [CLUSTER_LINK_HANDSHAKE_TIMEOUT](#cluster_link_handshake_timeout)
  - [CLUSTER_LINK_HOST](#cluster_link_host)
  - [CLUSTER_LINK_LONG_TERM_CALLBACK_INTERVAL](#cluster_link_long_term_callback_interval)
  - [CLUSTER_LINK_LONG_WAIT_INTERVAL](#cluster_link_long_wait_interval)
  - [CLUSTER_LINK_MAX_LISTEN](#cluster_link_max_listen)
  - [CLUSTER_LINK_MAX_POLL](#cluster_link_max_poll)
  - [CLUSTER_LINK_PORT_NO](#cluster_link_port_no)
  - [CLUSTER_LINK_RECEIVE_TIMEOUT](#cluster_link_receive_timeout)
  - [CLUSTER_LINK_REQUEST_TIMEOUT](#cluster_link_request_timeout)
  - [CLUSTER_LINK_SEND_RETRY_COUNT](#cluster_link_send_retry_count)
  - [CLUSTER_LINK_SEND_TIMEOUT](#cluster_link_send_timeout)
  - [CLUSTER_LINK_SESSION_TIMEOUT](#cluster_link_session_timeout)
  - [CLUSTER_LINK_THREAD_COUNT](#cluster_link_thread_count)
  - [CLUSTER_QUERY_STAT_LOG_ENABLE](#cluster_query_stat_log_enable)
  - [CLUSTER_REPLICATION_BLOCK_SIZE](#cluster_replication_block_size)
  - [CLUSTER_WAREHOUSE_DIRECT_DML_ENABLE](#cluster_warehouse_direct_dml_enable)
  - [COORDINATOR_DBS_PATH](#coordinator_dbs_path)
  - [COORDINATOR_DDL_REQUEST_TIMEOUT](#coordinator_ddl_request_timeout)
  - [COORDINATOR_DDL_TIMEOUT](#coordinator_ddl_timeout)
  - [COORDINATOR_DECISION_DELAY](#coordinator_decision_delay)
  - [COORDINATOR_DECISION_INTERVAL](#coordinator_decision_interval)
  - [COORDINATOR_HOST_RESOURCE_ENABLE](#coordinator_host_resource_enable)
  - [COORDINATOR_HOST_RESOURCE_COLLECT_INTERVAL](#coordinator_host_resource_collect_interval)
  - [COORDINATOR_HOST_RESOURCE_INTERVAL](#coordinator_host_resource_interval)
  - [COORDINATOR_HOST_RESOURCE_REQUEST_TIMEOUT](#coordinator_host_resource_request_timeout)
  - [COORDINATOR_NODE_REQUEST_TIMEOUT](#coordinator_node_request_timeout)
  - [COORDINATOR_NODE_TIMEOUT](#coordinator_node_timeout)
  - [COORDINATOR_STARTUP_DELAY](#coordinator_startup_delay)
  - [COORDINATOR_STATUS_NODE_INTERVAL](#coordinator_status_node_interval)
  - [COORDINATOR_STATUS_NODE_REQUEST_TIMEOUT](#coordinator_status_node_request_timeout)
  - [COORDINATOR_DISK_FULL_UPPER_BOUND_RATIO](#coordinator_disk_full_upper_bound_ratio)
  - [COORDINATOR_DISK_FULL_LOWER_BOUND_RATIO](#coordinator_disk_full_lower_bound_ratio)
  - [DEPLOYER_DBS_PATH](#deployer_dbs_path)
  - [EXECUTION_STAGE_MEMORY_MAX](#execution_stage_memory_max)
  - [HTTP_ADMIN_PORT](#http_admin_port)
  - [HTTP_CONNECT_TIMEOUT](#http_connect_timeout)
  - [HTTP_RECEIVE_TIMEOUT](#http_receive_timeout)
  - [HTTP_SEND_TIMEOUT](#http_send_timeout)
  - [INSERT_BULK_DATA_MAX_SIZE](#insert_bulk_data_max_size)
  - [INSERT_RECORD_COUNT_PER_NODE](#insert_record_count_per_node)
  - [LOOKUPNODE_COMMAND_RETRY_MAX_COUNT](#lookupnode_command_retry_max_count)
  - [STAGE_RESULT_BLOCK_SIZE](#stage_result_block_size)

## CLUSTER_LINK_ACCEPT_TIMEOUT {#cluster_link_accept_timeout}

特定ノードとの接続で、Accept してからハンドシェイクメッセージを受信するまでの上限時間です。

時間内に受信できない場合、接続は失敗します。

既定値は 5 秒です。

|(usec)|値|
|---|---|
|最小値|0|
|最大値|2^64 - 1|
|既定値|5000000|

## CLUSTER_LINK_BUFFER_SIZE {#cluster_link_buffer_size}

送受信バッファーのサイズです。

不足する場合、送信時にバッファーが空くまで再試行します。

|(byte)|値|
|---|---|
|最小値|1024768|
|最大値|2^32 - 1|
|既定値|33554432 (32M)|

## CLUSTER_LINK_CHECK_INTERVAL {#cluster_link_check_interval}

特定ノードに接続したソケットを監視するタイムアウトスレッドの確認間隔です。

タイムアウトスレッドは `RECEIVE_TIMEOUT` と `SESSION_TIMEOUT` を確認します。

短いほど頻繁に確認しますが、タイムアウトの判定は各タイムアウト値に従います。

既定値は 1 秒です。

|(usec)|値|
|---|---|
|最小値|0|
|最大値|2^64 - 1|
|既定値|1000000|

## CLUSTER_LINK_CONNECT_RETRY_TIMEOUT {#cluster_link_connect_retry_timeout}

特定ノードとの接続に失敗した後、再接続を繰り返す上限時間です。

この時間内に再接続できなければ、完全に切断されたと判断します。

既定値は 1 分です。

|(usec)|値|
|---|---|
|最小値|0|
|最大値|2^64 - 1|
|既定値|60000000|

## CLUSTER_LINK_CONNECT_TIMEOUT {#cluster_link_connect_timeout}

特定ノードへの接続を試みるときの待ち時間です。

時間内に接続できなければ、`CLUSTER_LINK_CONNECT_RETRY_TIMEOUT` に達するまで再接続を試みます。

既定値は 5 秒です。

|(usec)|値|
|---|---|
|最小値|0|
|最大値|2^64 - 1|
|既定値|5000000|

## CLUSTER_LINK_ERROR_ADD_ORIGIN_HOST {#cluster_link_error_add_origin_host}

クラスタ内の通信で発生したエラーメッセージに、エラーが発生したホスト名を追加するかを指定します。

詳細なエラーメッセージを表示するには 1 にします。

既定値は 1 で、ホスト名を表示します。

|(boolean)|値|
|---|---|
|最小値|0|
|最大値|1|
|既定値|1|

## CLUSTER_LINK_HANDSHAKE_TIMEOUT {#cluster_link_handshake_timeout}

特定ノードとクラスタソケットで接続した状態で、ハンドシェイクメッセージを受信するまでの上限時間です。

接続直後の 2 つのノードは、接続状態を確認するために小さなハンドシェイクメッセージを交換します。

Accept した側のノードが先にハンドシェイクメッセージを送信し、その応答を待つ時間をここで指定します。

既定値は 5 秒です。

|(usec)|値|
|---|---|
|最小値|0|
|最大値|2^64 - 1|
|既定値|5000000|

## CLUSTER_LINK_HOST {#cluster_link_host}

特定ノードとクラスタソケットで接続するための、自ノードのホスト名です。

|(string)|値|
|---|---|
|既定値|localhost|

## CLUSTER_LINK_LONG_TERM_CALLBACK_INTERVAL {#cluster_link_long_term_callback_interval}

クラスタソケットで受信したメッセージを処理する Receive Callback の実行時間がこの値を超えると、Long-Term Callback と判定します。

受信スレッド数には限りがあるため、Receive Callback が長時間メッセージを処理し続けないようにします。

この時間を過ぎても処理中の場合は Long-Term Callback と判定し、トレースログに記録します。

既定値は 1 秒です。

|(usec)|値|
|---|---|
|最小値|0|
|最大値|2^64 - 1|
|既定値|1000000|

## CLUSTER_LINK_LONG_WAIT_INTERVAL {#cluster_link_long_wait_interval}

クラスタソケットでメッセージが届くまでの時間がこの値を超えると、Long-Wait Message と判定します。

受信開始から完了までが長い場合は、ネットワーク環境の問題が考えられます。

この時間を過ぎても受信メッセージが届かない場合は Long-Wait Message と判定し、トレースログに記録します。

既定値は 1 秒です。

|(usec)|値|
|---|---|
|最小値|0|
|最大値|2^64 - 1|
|既定値|1000000|

## CLUSTER_LINK_MAX_LISTEN {#cluster_link_max_listen}

特定ノードとの接続時に使用する、ソケットの Accept キューの最大数です。

|(count)|値|
|---|---|
|最小値|1|
|最大値|2^31 - 1|
|既定値|512|

## CLUSTER_LINK_MAX_POLL {#cluster_link_max_poll}

特定ノードとの通信時に、1 回の poll で取得できるイベントの最大数です。

|(count)|値|
|---|---|
|最小値|1|
|最大値|2^31 - 1|
|既定値|4096|

## CLUSTER_LINK_PORT_NO {#cluster_link_port_no}

特定ノードとクラスタソケットで接続するための、自ノードのポート番号です。

|(port)|値|
|---|---|
|最小値|1024|
|最大値|65535|
|既定値|3868|

## CLUSTER_LINK_RECEIVE_TIMEOUT {#cluster_link_receive_timeout}

タイムアウトスレッドが、最終受信以降に接続が切れたと判断するまでの時間です。

クラスタノード間の接続は受信が完了すると終了するため、リンクリストに残る接続は受信を継続している必要があります。

この時間が経っても最終受信時刻が更新されなければ、タイムアウトスレッドはトレースログに記録してソケットを閉じます。

|(usec)|値|
|---|---|
|最小値|0|
|最大値|2^64 - 1|
|既定値|30000000|

## CLUSTER_LINK_REQUEST_TIMEOUT {#cluster_link_request_timeout}

クラスタソケットで要求メッセージを送信してから、その応答を受信するまでの上限時間です。

特定のメッセージについて、要求後に応答が送信されるまで待つ時間を指定します。

時間内に応答メッセージが届かなければ、トレースログに記録してソケットを閉じます。

既定値は 60 秒です。メッセージの種類や受信側の処理が事前に分からないため、長めに設定しています。

|(usec)|値|
|---|---|
|最小値|0|
|最大値|2^64 - 1|
|既定値|60000000|

## CLUSTER_LINK_SEND_RETRY_COUNT {#cluster_link_send_retry_count}

* 5.6 以降で使用できます。

送信バッファーが空くまで送信を再試行する回数です。

再試行のたびに 1 ms 待機します。この回数を超えて再試行することになると、接続を切断します。

既定値は 5000 回です（各回の待機時間だけで計約 5000 ms）。

|(count)|値|
|---|---|
|最小値|0|
|最大値|2^32 - 1|
|既定値|5000|

## CLUSTER_LINK_SEND_TIMEOUT {#cluster_link_send_timeout}

クラスタソケットでメッセージを送信するときのタイムアウトです。

送信時にこのタイムアウトを適用します。

時間内に送信が完了しなければ、トレースログに記録します。

|(usec)|値|
|---|---|
|最小値|0|
|最大値|2^64 - 1|
|既定値|30000000|

## CLUSTER_LINK_SESSION_TIMEOUT {#cluster_link_session_timeout}

タイムアウトスレッドが、特定セッションの最終受信以降に接続が切れたと判断するまでの時間です。

クラスタ接続は、すべてのメッセージのセッションを内部で管理します。このプロパティは、セッションを突然整理できなくなった場合に必要です。

この時間が経ってもセッションの最終受信時刻が更新されなければ、タイムアウトスレッドはトレースログに記録してセッションを閉じます。

既定値は 1 時間です。

|(usec)|値|
|---|---|
|最小値|0|
|最大値|2^64 - 1|
|既定値|3600000000|

## CLUSTER_LINK_THREAD_COUNT {#cluster_link_thread_count}

特定ノードとの通信時に、受信したメッセージを処理するスレッド数です。

クラスタの規模が大きくなったり処理する演算が増えたりして、受信スレッドに余裕がない場合に増やせます。

|(count)|値|
|---|---|
|最小値|1|
|最大値|4096|
|既定値|16|

## CLUSTER_QUERY_STAT_LOG_ENABLE {#cluster_query_stat_log_enable}

実行したクエリーの統計情報をトレースログに出力します。

|(boolean)|値|
|---|---|
|最小値|0|
|最大値|1|
|既定値|0|

## CLUSTER_REPLICATION_BLOCK_SIZE {#cluster_replication_block_size}

Cluster Edition でノード追加によるレプリケーションを行うときに、1 回で送信するデータサイズです。

Replication Active となる Warehouse（送信側の Warehouse）に直接設定する必要があります。

既定値は 640KB です。

|(size)|値|
|---|---|
|最小値|64 * 1024|
|最大値|100 * 1024 * 1024|
|既定値|640 * 1024 (655360)|

## CLUSTER_WAREHOUSE_DIRECT_DML_ENABLE {#cluster_warehouse_direct_dml_enable}

Cluster Edition で、Warehouse に直接接続して DML を実行できるようにします。

* 1：実行できます。
* 0：実行できません。エラーを返します。

Warehouse で直接 DML を実行すると Broker 経由より性能面で有利ですが、同じグループに DML が伝播しません。
そのため、データ不一致からの緊急復旧や、グループ内のデータ不一致を許容できる場合に限り使用してください。

対象の Warehouse に直接設定する必要があります。

既定値は 0 です。

{{< callout type="info" >}}
このプロパティを有効にした状態でグループ内の Warehouse 間にデータの差異が生じても、Coordinator はデータ不一致を検査しません。
{{< /callout >}}

|(boolean)|値|
|---|---|
|最小値|0|
|最大値|1|
|既定値|0|

## COORDINATOR_DBS_PATH {#coordinator_dbs_path}

Coordinator のデータファイルを作成するディレクトリを指定します。

既定値は `?/dbs` で、`?` は環境変数 `$MACHBASE_COORDINATOR_HOME` に置換されます。
つまり `$MACHBASE_COORDINATOR_HOME/dbs` ディレクトリを意味します。

Coordinator に設定します。他のノードには効果がありません。

|(path)|値|
|---|---|
|既定値|?/dbs|

## COORDINATOR_DDL_REQUEST_TIMEOUT {#coordinator_ddl_request_timeout}

Coordinator がノードに DDL の実行を要求してから待つ上限時間です。

この値は、Coordinator が各ノードに DDL の実行を要求してから待つ時間を意味します。

|(usec)|値|
|---|---|
|最小値|0|
|最大値|2^64 - 1|
|既定値|300000000|

## COORDINATOR_DDL_TIMEOUT {#coordinator_ddl_timeout}

Broker が Coordinator に DDL の実行を要求してから待つ上限時間です。

この値は、Broker がクラスタ全体に対する DDL の実行を Coordinator に要求してから待つ時間を意味します。

|(usec)|値|
|---|---|
|最小値|0|
|最大値|2^64 - 1|
|既定値|300000000|

## COORDINATOR_DECISION_DELAY {#coordinator_decision_delay}

Coordinator が状態変更を要求してから、実際に反映されるまでの上限時間です。

この時間内に状態が実際に変わらなければ、クラスタの状態を無効にします。

Warehouse Active の状態が変わっておらず、接続されたスタンバイがある場合は、フェイルオーバーを開始します。

|(usec)|値|
|---|---|
|最小値|0|
|最大値|2^64 - 1|
|既定値|1000000|

## COORDINATOR_DECISION_INTERVAL {#coordinator_decision_interval}

Coordinator が状態変更を判断する頻度を決める時間です。

|(usec)|値|
|---|---|
|最小値|0|
|最大値|2^64 - 1|
|既定値|1000000|

## COORDINATOR_HOST_RESOURCE_ENABLE {#coordinator_host_resource_enable}

Coordinator がクラスタノードのホストリソースを収集するかを指定します。

|(boolean)|値|
|---|---|
|最小値|0 (false)|
|最大値|1 (true)|
|既定値|0 (false)|

## COORDINATOR_HOST_RESOURCE_COLLECT_INTERVAL {#coordinator_host_resource_collect_interval}

クラスタノードがホストリソースを収集する間隔です。

|(usec)|値|
|---|---|
|最小値|0|
|最大値|2^64 - 1|
|既定値|1000000|

## COORDINATOR_HOST_RESOURCE_INTERVAL {#coordinator_host_resource_interval}

Coordinator とノードがホストリソース情報を交換する間隔です。

|(usec)|値|
|---|---|
|最小値|0|
|最大値|2^64 - 1|
|既定値|1000000|

## COORDINATOR_HOST_RESOURCE_REQUEST_TIMEOUT {#coordinator_host_resource_request_timeout}

Coordinator がノードにホストリソース情報を要求してから待つ時間です。

|(usec)|値|
|---|---|
|最小値|0|
|最大値|2^64 - 1|
|既定値|10000000|

## COORDINATOR_NODE_REQUEST_TIMEOUT {#coordinator_node_request_timeout}

Coordinator がノードにコマンドの実行を要求してから待つ上限時間です。

Add/Remove-node、Add/Remove-Package などのノードコマンドの実行を含むため、短すぎるとコマンドの処理が完了しない場合があります。

|(usec)|値|
|---|---|
|最小値|0|
|最大値|2^64 - 1|
|既定値|600000000|

## COORDINATOR_NODE_TIMEOUT {#coordinator_node_timeout}

Coordinator がノードの障害と判断するまでの待ち時間です。

|(usec)|値|
|---|---|
|最小値|0|
|最大値|2^64 - 1|
|既定値|30000000|

## COORDINATOR_STARTUP_DELAY {#coordinator_startup_delay}

Coordinator の起動直後から、判定スレッド（Decision Thread）を開始するまでの猶予時間です。

クラスタ全体の起動に時間がかかる場合は、この値を大きくして Coordinator によるノード制御の開始を遅らせることができます。

全体の起動が終わる前に判定スレッドが動作すると、Coordinator が誤判定する可能性が高くなります。

|(usec)|値|
|---|---|
|最小値|0|
|最大値|2^64 - 1|
|既定値|3000000|

## COORDINATOR_STATUS_NODE_INTERVAL {#coordinator_status_node_interval}

Coordinator がノードと状態照会メッセージを交換する間隔です。

|(usec)|値|
|---|---|
|最小値|0|
|最大値|2^64 - 1|
|既定値|1000000|

## COORDINATOR_STATUS_NODE_REQUEST_TIMEOUT {#coordinator_status_node_request_timeout}

Coordinator がノードに状態照会を要求してから待つ時間です。

この時間内に応答がなければ、Coordinator は該当ノードの状態を更新せずに続行します。

ネットワークの状態が悪く、状態を必ず更新する必要がある場合は、値を増やすことを検討できます。

ただし、応答がない場合は、増やした分だけ Coordinator が必ず待つことになります。

|(usec)|値|
|---|---|
|最小値|0|
|最大値|2^64 - 1|
|既定値|15000000|

## COORDINATOR_DISK_FULL_UPPER_BOUND_RATIO {#coordinator_disk_full_upper_bound_ratio}

クラスタを構成する一部のサーバーでディスク使用率がこの値を超えると、そのホストが属する Warehouse グループを DISKFULL 状態にします。

DISKFULL 状態のグループでは入力が制限され、検索と削除だけが可能です。

0 の場合、この機能は無効です。

|(percent)|値|
|---|---|
|最小値|0|
|最大値|99|
|既定値|0|

## COORDINATOR_DISK_FULL_LOWER_BOUND_RATIO {#coordinator_disk_full_lower_bound_ratio}

DISKFULL 状態で動作しているサーバーのディスク使用率がこの値未満になると、そのグループを通常状態へ戻します。

0 の場合、この機能は無効です。

|(percent)|値|
|---|---|
|最小値|0|
|最大値|99|
|既定値|0|

## DEPLOYER_DBS_PATH {#deployer_dbs_path}

Deployer のデータファイルを作成するディレクトリを指定します。

既定値は `?/dbs` で、`?` は環境変数 `$MACHBASE_DEPLOYER_HOME` に置換されます。
つまり `$MACHBASE_DEPLOYER_HOME/dbs` ディレクトリを意味します。

Deployer に設定します。他のノードには効果がありません。

|(path)|値|
|---|---|
|既定値|?/dbs|

## EXECUTION_STAGE_MEMORY_MAX {#execution_stage_memory_max}

Cluster Edition で SELECT クエリーを実行する Stage スレッドが使用するメモリの最大量です。

Stage ごとの上限なので、Stage 数が増える複雑な SELECT クエリーでは、必要なメモリが増える場合があります。
上限を超える Stage があると、その Stage は取り消され、クエリーもエラーとともに取り消されます。

対象の Warehouse に直接設定する必要があります。

既定値は 1GB です。

|(size)|値|
|---|---|
|最小値|0|
|最大値|2^64 - 1|
|既定値|1024 * 1024 * 1024|

## HTTP_ADMIN_PORT {#http_admin_port}

MWA または `machcoordinatoradmin` からの要求を受け付けるポート番号です。

|(port)|値|
|---|---|
|最小値|1024|
|最大値|65535|
|既定値|5779|

## HTTP_CONNECT_TIMEOUT {#http_connect_timeout}

`machcoordinatoradmin` との接続時に使用するタイムアウトです。

|(usec)|値|
|---|---|
|最小値|0|
|最大値|2^64 - 1|
|既定値|30000000|

## HTTP_RECEIVE_TIMEOUT {#http_receive_timeout}

`machcoordinatoradmin` との通信で、受信時に使用するタイムアウトです。

|(usec)|値|
|---|---|
|最小値|0|
|最大値|2^64 - 1|
|既定値|3600000000|

## HTTP_SEND_TIMEOUT {#http_send_timeout}

`machcoordinatoradmin` との通信で、送信時に使用するタイムアウトです。

|(usec)|値|
|---|---|
|最小値|0|
|最大値|2^64 - 1|
|既定値|60000000|

## INSERT_BULK_DATA_MAX_SIZE {#insert_bulk_data_max_size}

Append または INSERT-SELECT の実行時に使用する入力データブロックの最大サイズです。

|(size)|値|
|---|---|
|最小値|1024|
|最大値|10 * 1024 * 1024|
|既定値|1024 * 1024|

## INSERT_RECORD_COUNT_PER_NODE {#insert_record_count_per_node}

入力時に、入力先の Warehouse グループを切り替えるまでのデータ入力件数です。

|(count)|値|
|---|---|
|最小値|1|
|最大値|2^32 - 1|
|既定値|1000|

## LOOKUPNODE_COMMAND_RETRY_MAX_COUNT {#lookupnode_command_retry_max_count}

Lookup ノードへのコマンドや接続が失敗した場合の再試行回数です。

|(count)|値|
|---|---|
|最小値|1|
|最大値|3600|
|既定値|30|

## STAGE_RESULT_BLOCK_SIZE {#stage_result_block_size}

1 つの Stage で作成するブロックの最大サイズです。

|(size)|値|
|---|---|
|最小値|1024|
|最大値|2^32 - 1|
|既定値|1024 * 1024|
