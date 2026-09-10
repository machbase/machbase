---
layout : post
title : プロパティ（Cluster）
type : docs
toc: true
weight: 0
---


[共通プロパティ](../property)とは別に、Cluster Edition 専用の項目を説明します。

<a id="index"></a>
<a id="목차"></a>

# 目次

- [目次](#index)
  - [CLUSTER_LINK_ACCEPT_TIMEOUT](#cluster_link_accept_timeout)
  - [CLUSTER_LINK_BUFFER_SIZE](#cluster_link_buffer_size)
  - [CLUSTER_LINK_CHECK_INTERVAL](#cluster_link_check_interval)
  - [CLUSTER_LINK_CONNECT_RETRY_TIMEOUT](#cluster_link_connect_retry_timeout)
  - [CLUSTER_LINK_CONNECT_TIMEOUT](#cluster_link_connect_timeout)
  - [CLUSTER_LINK_ERROR_ADD_ORIGIN_HOST](#cluster_link_error_add_origin_host)
  - [CLUSTER_LINK_HANDSHAKE_TIMEOUT](#cluster_link_handshake_timeout)
  - [CLUSTER_LINK_SEND_RETRY_COUNT](#cluster_link_send_retry_count)
  - [CLUSTER_LINK_HOST](#cluster_link_host)
  - [CLUSTER_LINK_LONG_TERM_CALLBACK_INTERVAL](#cluster_link_long_term_callback_interval)
  - [CLUSTER_LINK_LONG_WAIT_INTERVAL](#cluster_link_long_wait_interval)
  - [CLUSTER_LINK_MAX_LISTEN](#cluster_link_max_listen)
  - [CLUSTER_LINK_MAX_POLL](#cluster_link_max_poll)
  - [CLUSTER_LINK_PORT_NO](#cluster_link_port_no)
  - [CLUSTER_LINK_RECEIVE_TIMEOUT](#cluster_link_receive_timeout)
  - [CLUSTER_LINK_REQUEST_TIMEOUT](#cluster_link_request_timeout)
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
特定ノードへの接続を受け付けてから、ハンドシェイクメッセージを受信するまでの上限時間です。

時間内に受信できない場合、接続は失敗します。

既定値は 5 秒です。

<table>
  <thead>
    <th style="background-color: lightyellow;">(usec)</th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2^64-1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">既定値</td>
      <td>5000000</td>
    </tr>
  </tbody>
</table>


## CLUSTER_LINK_BUFFER_SIZE {#cluster_link_buffer_size}

送受信要求用バッファーのサイズです。

不足する場合、送信時にバッファーが空くまで再試行します。

|(byte)|    値|
|------|---------|
|最小値|    1024768|
|最大値|    2^32 - 1|
|既定値|    33554432 (32M)|


## CLUSTER_LINK_CHECK_INTERVAL {#cluster_link_check_interval}
ノードに接続したソケットを監視するタイムアウトスレッドの確認間隔です。

RECEIVE_TIMEOUT と SESSION_TIMEOUT を確認します。

短いほど頻繁に確認しますが、タイムアウト判定は各設定値に従います。

既定値は 1 秒です。


<table>
  <thead>
    <th style="background-color: lightyellow;">(usec)</th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2^64-1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">既定値</td>
      <td>1000000</td>
    </tr>
  </tbody>
</table>


## CLUSTER_LINK_CONNECT_RETRY_TIMEOUT {#cluster_link_connect_retry_timeout}
接続失敗後に再接続を試みる期間です。

この時間内に接続できなければ、完全な切断と判断します。

既定値は 1 分です。


<table>
  <thead>
    <th style="background-color: lightyellow;">(usec)</th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2^64-1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">既定値</td>
      <td>60000000</td>
    </tr>
  </tbody>
</table>


## CLUSTER_LINK_CONNECT_TIMEOUT {#cluster_link_connect_timeout}
ノードへの接続試行の待ち時間です。

接続できなければ、CLUSTER_LINK_CONNECT_RETRY_TIMEOUT に達するまで再試行します。

既定値は 5 秒です。



<table>
  <thead>
    <th style="background-color: lightyellow;">(usec)</th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2^64-1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">既定値</td>
      <td>5000000</td>
    </tr>
  </tbody>
</table>


## CLUSTER_LINK_ERROR_ADD_ORIGIN_HOST {#cluster_link_error_add_origin_host}
クラスタ間通信のエラーに、発生元ホスト名を追加するかを指定します。

詳細を表示するには 1 にします。

既定値は 1 で、ホスト名を表示します。


<table>
  <thead>
    <th style="background-color: lightyellow;">(boolean)</th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">既定値</td>
      <td>1</td>
    </tr>
  </tbody>
</table>


## CLUSTER_LINK_HANDSHAKE_TIMEOUT {#cluster_link_handshake_timeout}
クラスタソケットの接続後に、ハンドシェイク応答を待つ時間です。

接続直後の 2 ノードは、小さなメッセージを交換して状態を確認します。

受け付け側が先に送信し、その応答を待つ時間を指定します。

既定値は 5 秒です。


<table>
  <thead>
    <th style="background-color: lightyellow;">(usec)</th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2^64-1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">既定値</td>
      <td>5000000</td>
    </tr>
  </tbody>
</table>


## CLUSTER_LINK_SEND_RETRY_COUNT {#cluster_link_send_retry_count}

* 5.6 以降で使用できます。
送信バッファーが空くまでの再試行回数です。

1 回ごとに 1 ms 待機します。上限を超えると切断します。

既定値は 5000 回（各回の待機時間だけで計約 5000 ms）です。


<table>
  <thead>
    <th style="background-color: lightyellow;">(count)</th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2^32 - 1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">既定値</td>
      <td>5000</td>
    </tr>
  </tbody>
</table>


## CLUSTER_LINK_HOST {#cluster_link_host}

他のノードとクラスタソケットで接続するための、自ノードのホスト名です。

|(string)|  値|
|--|--|
|既定値|    localhost|


## CLUSTER_LINK_LONG_TERM_CALLBACK_INTERVAL {#cluster_link_long_term_callback_interval}
受信メッセージを処理するコールバックが、この時間を超えると長時間コールバックと判定します。

受信スレッド数に限りがあるため、長時間占有しないようにします。

処理が指定時間を超えると、トレースログに記録します。

既定値は 1 秒です。


<table>
  <thead>
    <th style="background-color: lightyellow;">(usec)</th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2^64-1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">既定値</td>
      <td>1000000</td>
    </tr>
  </tbody>
</table>


## CLUSTER_LINK_LONG_WAIT_INTERVAL {#cluster_link_long_wait_interval}
メッセージの受信にかかる時間がこの値を超えると、長時間待機と判定します。

受信開始から完了までが長い場合、ネットワークの問題が考えられます。

指定時間を超えると、トレースログに記録します。

既定値は 1 秒です。


<table>
  <thead>
    <th style="background-color: lightyellow;">(usec)</th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2^64-1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">既定値</td>
      <td>1000000</td>
    </tr>
  </tbody>
</table>


## CLUSTER_LINK_MAX_LISTEN {#cluster_link_max_listen}
ソケットの接続受け付けキューの最大数です。

<table>
  <thead>
    <th style="background-color: lightyellow;">(count)</th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>1</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2^31-1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">既定値</td>
      <td>512</td>
    </tr>
  </tbody>
</table>



## CLUSTER_LINK_MAX_POLL {#cluster_link_max_poll}
1 回の poll で取得するイベントの最大数です。

<table>
  <thead>
    <th style="background-color: lightyellow;">(count)</th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>1</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2^31-1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">既定値</td>
      <td>4096</td>
    </tr>
  </tbody>
</table>


## CLUSTER_LINK_PORT_NO {#cluster_link_port_no}
クラスタソケットで他のノードと接続するための、自ノードのポートです。

<table>
  <thead>
    <th style="background-color: lightyellow;">(port)</th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>1024</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>65535</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">既定値</td>
      <td>3868</td>
    </tr>
  </tbody>
</table>


## CLUSTER_LINK_RECEIVE_TIMEOUT {#cluster_link_receive_timeout}
最終受信から、切断と判断するまでの時間です。

クラスタノード間の受信完了時に接続を終了するため、リンクリストに残る接続は受信を継続している必要があります。

指定時間が経っても最終受信時刻が更新されなければ、ログを記録してソケットを閉じます。


<table>
  <thead>
    <th style="background-color: lightyellow;">(usec)</th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2^64-1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">既定値</td>
      <td>30000000</td>
    </tr>
  </tbody>
</table>


## CLUSTER_LINK_REQUEST_TIMEOUT {#cluster_link_request_timeout}
要求送信から応答受信までの上限時間です。

メッセージの要求後に、応答を待つ時間を指定します。

時間内に応答がなければ、ログを記録してソケットを閉じます。

要求や処理の種類によって時間が変わるため、既定では 60 秒の余裕を持たせています。

<table>
  <thead>
    <th style="background-color: lightyellow;">(usec)</th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2^64-1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">既定値</td>
      <td>60000000</td>
    </tr>
  </tbody>
</table>


## CLUSTER_LINK_SEND_TIMEOUT {#cluster_link_send_timeout}
クラスタソケットでのメッセージ送信のタイムアウトです。

送信時に適用します。

時間内に完了しなければ、トレースログに記録します。


<table>
  <thead>
    <th style="background-color: lightyellow;">(usec)</th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2^64-1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">既定値</td>
      <td>30000000</td>
    </tr>
  </tbody>
</table>


## CLUSTER_LINK_SESSION_TIMEOUT {#cluster_link_session_timeout}
セッションの最終受信から、切断と判断するまでの時間です。

クラスタ接続は各メッセージのセッションを内部管理します。セッションが不定な状態になった場合の対処に使用します。

指定時間内に受信時刻が更新されなければ、ログを記録してセッションを閉じます。

既定値は 1 時間です。


<table>
  <thead>
    <th style="background-color: lightyellow;">(usec)</th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2^64-1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">既定値</td>
      <td>3600000000</td>
    </tr>
  </tbody>
</table>


## CLUSTER_LINK_THREAD_COUNT {#cluster_link_thread_count}
受信メッセージを処理するスレッド数です。

クラスタや処理量の拡大に応じて増やせます。

<table>
  <thead>
    <th style="background-color: lightyellow;">(count)</th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>1</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>4096</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">既定値</td>
      <td>16</td>
    </tr>
  </tbody>
</table>


## CLUSTER_QUERY_STAT_LOG_ENABLE {#cluster_query_stat_log_enable}
実行したクエリーの統計をトレースログに出力します。


<table>
  <thead>
    <th style="background-color: lightyellow;">(boolean)</th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">既定値</td>
      <td>0</td>
    </tr>
  </tbody>
</table>


## CLUSTER_REPLICATION_BLOCK_SIZE {#cluster_replication_block_size}
ノード追加時のレプリケーションで、1 回に送信するデータサイズです。

送信元となるアクティブ Warehouse に直接設定します。

既定値は 640 KB です。


<table>
  <thead>
    <th style="background-color: lightyellow;">(size)</th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>64 * 1024</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>100 * 1024 * 1024</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">既定値</td>
      <td>640 * 1024 (655360)</td>
    </tr>
  </tbody>
</table>


## CLUSTER_WAREHOUSE_DIRECT_DML_ENABLE {#cluster_warehouse_direct_dml_enable}
Warehouse に直接接続して DML を実行することを許可します。

* 1：実行可能。
* 0：実行不可。エラーを返します。

Broker 経由より高速ですが、同じグループの他ノードに DML が伝播しません。

データ不一致の緊急復旧など、不整合を考慮できる場合に限り使用してください。

対象 Warehouse に直接設定します。

既定値は 0 です。

{{<callout type="info">}}
この設定でグループ内に差異が生じても、Coordinator はデータ不一致を検出しません。
{{</callout>}}

<table>
  <thead>
    <th style="background-color: lightyellow;">(boolean)</th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">既定値</td>
      <td>0</td>
    </tr>
  </tbody>
</table>


## COORDINATOR_DBS_PATH {#coordinator_dbs_path}
Coordinator のデータファイルの保存先です。

既定値は ?/dbs で、? は $MACHBASE_COORDINATOR_HOME に置換されます。

つまり $MACHBASE_COORDINATOR_HOME/dbs です。

Coordinator に設定します。他のノードには効果がありません。


<table>
  <thead>
    <th style="background-color: lightyellow;">(path)</th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td style="background-color: #F0FFFF;">既定値</td>
      <td>?/dbs</td>
    </tr>
  </tbody>
</table>

## COORDINATOR_DDL_REQUEST_TIMEOUT {#coordinator_ddl_request_timeout}
Coordinator がノードに DDL を要求してから待つ上限時間です。

各ノードへの要求単位に適用します。

<table>
  <thead>
    <th style="background-color: lightyellow;">(usec)</th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2^64 - 1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">既定値</td>
      <td>300000000</td>
    </tr>
  </tbody>
</table>

## COORDINATOR_DDL_TIMEOUT {#coordinator_ddl_timeout}

Broker が Coordinator に DDL を要求してから待つ上限時間です。

クラスタ全体に対する DDL の完了待ちに適用します。

|(usec)|値|
|--|--|
|最小値|0|  
|最大値|2^64 - 1|
|既定値|300000000|

## COORDINATOR_DECISION_DELAY {#coordinator_decision_delay}
Coordinator が状態変更を要求してから、反映されるまでの上限時間です。

時間内に変わらなければ、クラスタを無効な状態にします。

アクティブ Warehouse の状態が変わらず、接続されたスタンバイがある場合はフェイルオーバーを開始します。

<table>
  <thead>
    <th style="background-color: lightyellow;">(usec)</th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2^64 - 1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">既定値</td>
      <td>1000000</td>
    </tr>
  </tbody>
</table>


## COORDINATOR_DECISION_INTERVAL {#coordinator_decision_interval}
Coordinator が状態変更を判断する間隔です。


<table>
  <thead>
    <th style="background-color: lightyellow;">(usec)</th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2^64 - 1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">既定値</td>
      <td>1000000</td>
    </tr>
  </tbody>
</table>


## COORDINATOR_HOST_RESOURCE_ENABLE {#coordinator_host_resource_enable}
Coordinator が各ノードのホストリソース情報を収集するかを指定します。

<table>
  <thead>
    <th style="background-color: lightyellow;">(boolean)</th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0 (false)</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>1 (true)</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">既定値</td>
      <td>0 (false)</td>
    </tr>
  </tbody>
</table>


## COORDINATOR_HOST_RESOURCE_COLLECT_INTERVAL {#coordinator_host_resource_collect_interval}
各ノードがホストリソースを収集する間隔です。

<table>
  <thead>
    <th style="background-color: lightyellow;">(usec)</th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2^64 - 1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">既定値</td>
      <td>1000000</td>
    </tr>
  </tbody>
</table>


## COORDINATOR_HOST_RESOURCE_INTERVAL {#coordinator_host_resource_interval}
Coordinator と各ノードがリソース情報を交換する間隔です。

<table>
  <thead>
    <th style="background-color: lightyellow;">(usec)</th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2^64 - 1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">既定値</td>
      <td>1000000</td>
    </tr>
  </tbody>
</table>


## COORDINATOR_HOST_RESOURCE_REQUEST_TIMEOUT {#coordinator_host_resource_request_timeout}
リソース情報を要求してから待つ上限時間です。


<table>
  <thead>
    <th style="background-color: lightyellow;">(usec)</th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2^64 - 1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">既定値</td>
      <td>10000000</td>
    </tr>
  </tbody>
</table>


## COORDINATOR_NODE_REQUEST_TIMEOUT {#coordinator_node_request_timeout}
ノードへコマンド実行を要求してから待つ上限時間です。

ノードやパッケージの追加、削除にはノード上の処理があるため、短すぎると完了前にタイムアウトする場合があります。

<table>
  <thead>
    <th style="background-color: lightyellow;">(usec)</th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2^64 - 1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">既定値</td>
      <td>600000000</td>
    </tr>
  </tbody>
</table>


## COORDINATOR_NODE_TIMEOUT {#coordinator_node_timeout}
ノードの障害と判断するまでの待ち時間です。

<table>
  <thead>
    <th style="background-color: lightyellow;">(usec)</th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2^64 - 1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">既定値</td>
      <td>30000000</td>
    </tr>
  </tbody>
</table>



## COORDINATOR_STARTUP_DELAY {#coordinator_startup_delay}
Coordinator 起動後に、判定スレッドを開始するまでの猶予時間です。

クラスタ全体の起動に時間がかかる場合は、大きくしてノード制御の開始を遅らせます。

全体の起動前に判定を始めると、誤判定の可能性が高くなります。

<table>
  <thead>
    <th style="background-color: lightyellow;">(usec)</th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2^64 - 1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">既定値</td>
      <td>3000000</td>
    </tr>
  </tbody>
</table>


## COORDINATOR_STATUS_NODE_INTERVAL {#coordinator_status_node_interval}
ノードの状態照会メッセージを交換する間隔です。

<table>
  <thead>
    <th style="background-color: lightyellow;">(usec)</th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2^64 - 1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">既定値</td>
      <td>1000000</td>
    </tr>
  </tbody>
</table>


## COORDINATOR_STATUS_NODE_REQUEST_TIMEOUT {#coordinator_status_node_request_timeout}
状態を要求してから応答を待つ時間です。

応答がなければ、該当ノードの状態を更新せずに続行します。

ネットワークが遅い場合は、値を増やすことを検討できます。

ただし、無応答の場合も、その分だけ待ち時間が長くなります。

<table>
  <thead>
    <th style="background-color: lightyellow;">(usec)</th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2^64 - 1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">既定値</td>
      <td>15000000</td>
    </tr>
  </tbody>
</table>


## COORDINATOR_DISK_FULL_UPPER_BOUND_RATIO {#coordinator_disk_full_upper_bound_ratio}
クラスタ内サーバーのディスク使用率がこの値を超えると、その Warehouse グループを DISKFULL にします。

DISKFULL では入力を制限し、検索と削除だけが可能です。

0 で無効になります。

<table>
  <thead>
    <th style="background-color: lightyellow;">(percent)</th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>99</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">既定値</td>
      <td>0</td>
    </tr>
  </tbody>
</table>


## COORDINATOR_DISK_FULL_LOWER_BOUND_RATIO {#coordinator_disk_full_lower_bound_ratio}
DISKFULL のサーバーの使用率がこの値未満になると、グループを通常状態へ戻します。

0 で無効になります。

<table>
  <thead>
    <th style="background-color: lightyellow;">(percent)</th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>99</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">既定値</td>
      <td>0</td>
    </tr>
  </tbody>
</table>

## DEPLOYER_DBS_PATH {#deployer_dbs_path}
Deployer のデータファイルの保存先です。

既定値は ?/dbs で、? は $MACHBASE_DEPLOYER_HOME に置換されます。

つまり $MACHBASE_DEPLOYER_HOME/dbs です。

Deployer に設定します。他のノードには効果がありません。

<table>
  <thead>
    <th style="background-color: lightyellow;">(path)</th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td style="background-color: #F0FFFF;">既定値</td>
      <td>?/dbs</td>
    </tr>
  </tbody>
</table>


## EXECUTION_STAGE_MEMORY_MAX {#execution_stage_memory_max}
SELECT を処理する Stage スレッドごとの最大メモリ量です。

Stage ごとの上限なので、複雑な検索で Stage が増えると、全体のメモリ量も増えます。

いずれかの Stage が上限を超えると、Stage とクエリーを取り消してエラーにします。

対象 Warehouse に直接設定します。

既定値は 1GB です。

<table>
  <thead>
    <th style="background-color: lightyellow;">(size)</th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2^64 - 1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">既定値</td>
      <td>1024 *1024 * 1024</td>
    </tr>
  </tbody>
</table>


## HTTP_ADMIN_PORT {#http_admin_port}
MWA または machcoordinatoradmin の要求を受けるポートです。

<table>
  <thead>
    <th style="background-color: lightyellow;">(port)</th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>1024</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>65535</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">既定値</td>
      <td>5779</td>
    </tr>
  </tbody>
</table>


## HTTP_CONNECT_TIMEOUT {#http_connect_timeout}
machcoordinatoradmin との接続時のタイムアウトです。


<table>
  <thead>
    <th style="background-color: lightyellow;">(usec)</th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2^64 - 1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">既定値</td>
      <td>30000000</td>
    </tr>
  </tbody>
</table>


## HTTP_RECEIVE_TIMEOUT {#http_receive_timeout}
machcoordinatoradmin との受信時のタイムアウトです。


<table>
  <thead>
    <th style="background-color: lightyellow;">(usec)</th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2^64 - 1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">既定値</td>
      <td>3600000000</td>
    </tr>
  </tbody>
</table>


## HTTP_SEND_TIMEOUT {#http_send_timeout}
machcoordinatoradmin との送信時のタイムアウトです。

<table>
  <thead>
    <th style="background-color: lightyellow;">(usec)</th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2^64 - 1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">既定値</td>
      <td>60000000</td>
    </tr>
  </tbody>
</table>



## INSERT_BULK_DATA_MAX_SIZE {#insert_bulk_data_max_size}
APPEND または INSERT-SELECT の入力ブロックの最大サイズです。


<table>
  <thead>
    <th style="background-color: lightyellow;">(size)</th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>1024</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>10 * 1024 * 1024</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">既定値</td>
      <td>1024 * 1024</td>
    </tr>
  </tbody>
</table>


## INSERT_RECORD_COUNT_PER_NODE {#insert_record_count_per_node}
入力先 Warehouse グループを切り替えるまでのレコード数です。


<table>
  <thead>
    <th style="background-color: lightyellow;">(count)</th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>1</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2^32 - 1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">既定値</td>
      <td>1000</td>
    </tr>
  </tbody>
</table>


## LOOKUPNODE_COMMAND_RETRY_MAX_COUNT {#lookupnode_command_retry_max_count}
Lookup への接続やコマンドが失敗した場合の最大再試行回数です。

<table>
  <thead>
    <th style="background-color: lightyellow;">(count)</th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>1</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>3600</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">既定値</td>
      <td>30</td>
    </tr>
  </tbody>
</table>


## STAGE_RESULT_BLOCK_SIZE {#stage_result_block_size}
1 Stage で作成するブロックの最大サイズです。

<table>
  <thead>
    <th style="background-color: lightyellow;">(size)</th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>1024</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2^32 - 1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">既定値</td>
      <td>1024 * 1024</td>
    </tr>
  </tbody>
</table>
