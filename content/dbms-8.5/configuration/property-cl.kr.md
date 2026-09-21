---
layout : post
title : '프로퍼티 (클러스터)'
type: docs
weight: 0
---

[Property](../property)와 별개로, Cluster Edition에서만 사용할 수 있는 Property를 정리합니다.

## 목차

- [목차](#목차)
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

## CLUSTER_LINK_ACCEPT_TIMEOUT

특정 Node와 연결할 때, Accept 후 Handshake 메시지를 수신할 때까지의 Timeout입니다.

Timeout이 지날 때까지 수신하지 못하면 해당 연결은 실패합니다.

기본값은 5초입니다.

|(usec)|Value|
|---|---|
|최소값|0|
|최대값|2^64 - 1|
|기본값|5000000|

## CLUSTER_LINK_BUFFER_SIZE

송신/수신 버퍼의 크기입니다.

이 크기가 부족하면 송신 시 버퍼가 비워질 때까지 재시도합니다.

|(byte)|Value|
|---|---|
|최소값|1024768|
|최대값|2^32 - 1|
|기본값|33554432 (32M)|

## CLUSTER_LINK_CHECK_INTERVAL

특정 Node와 연결된 Socket들을 검사하는 Timeout Thread의 검사 주기입니다.

`RECEIVE_TIMEOUT`, `SESSION_TIMEOUT`을 검사하는 Timeout Thread가 있습니다.

주기를 짧게 할수록 자주 검사하지만, Timeout 판단은 각 Timeout 값에 따라 이루어집니다.

기본값은 1초입니다.

|(usec)|Value|
|---|---|
|최소값|0|
|최대값|2^64 - 1|
|기본값|1000000|

## CLUSTER_LINK_CONNECT_RETRY_TIMEOUT

특정 Node와 연결에 실패한 뒤 재연결 시도를 반복하는 Timeout입니다.

Timeout이 지날 때까지 재연결되지 않으면 완전히 단절되었다고 판단합니다.

기본값은 1분입니다.

|(usec)|Value|
|---|---|
|최소값|0|
|최대값|2^64 - 1|
|기본값|60000000|

## CLUSTER_LINK_CONNECT_TIMEOUT

특정 Node와 연결을 시도할 때 기다리는 시간입니다.

Timeout이 지날 때까지 연결되지 않으면 `CLUSTER_LINK_CONNECT_RETRY_TIMEOUT`이 지나기 전까지 재연결을 시도합니다.

기본값은 5초입니다.

|(usec)|Value|
|---|---|
|최소값|0|
|최대값|2^64 - 1|
|기본값|5000000|

## CLUSTER_LINK_ERROR_ADD_ORIGIN_HOST

Cluster 간 통신 중 발생하는 에러 메시지에 오류가 발생한 호스트 이름을 추가할지 여부를 선택합니다.

자세한 에러 메시지를 표시하려면 이 Property를 1로 설정해야 합니다.

기본값은 1이며, 호스트 이름이 출력됩니다.

|(boolean)|Value|
|---|---|
|최소값|0|
|최대값|1|
|기본값|1|

## CLUSTER_LINK_HANDSHAKE_TIMEOUT

특정 Node와 Cluster Socket으로 연결된 상태에서 Handshake 메시지를 수신할 때까지의 Timeout입니다.

연결이 막 완료된 두 Node는 연결 상태를 점검하기 위해 작은 크기의 Handshake 메시지를 주고받습니다.

Accept한 Node가 Handshake 메시지를 먼저 보내며, 그 응답을 기다리는 시간을 여기서 설정합니다.

기본값은 5초입니다.

|(usec)|Value|
|---|---|
|최소값|0|
|최대값|2^64 - 1|
|기본값|5000000|

## CLUSTER_LINK_HOST

특정 Node와 Cluster Socket을 연결하기 위한 현재 Node의 호스트 이름입니다.

|(string)|Value|
|---|---|
|기본값|localhost|

## CLUSTER_LINK_LONG_TERM_CALLBACK_INTERVAL

Cluster Socket으로 수신되는 메시지를 처리하는 Receive Callback의 수행 시간이 이 값을 넘으면 Long-Term Callback으로 인식합니다.

수신 Thread의 개수가 제한적이므로, Receive Callback은 가급적 오랜 시간 동안 메시지를 처리하지 않아야 합니다.

이 시간이 지나도록 Receive Callback이 메시지를 처리하고 있으면 Long-Term Callback으로 인식하고 Trace Log에 기록을 남깁니다.

기본값은 1초입니다.

|(usec)|Value|
|---|---|
|최소값|0|
|최대값|2^64 - 1|
|기본값|1000000|

## CLUSTER_LINK_LONG_WAIT_INTERVAL

Cluster Socket으로 수신되는 메시지가 도착할 때까지의 시간이 이 값을 넘으면 Long-Wait Message로 인식합니다.

수신 시작부터 수신 종료까지의 시간이 길면 네트워크 환경의 문제로 볼 수 있습니다.

이 시간이 지나도록 수신 메시지가 도착하지 않으면 Long-Wait Message로 인식하고 Trace Log에 기록을 남깁니다.

기본값은 1초입니다.

|(usec)|Value|
|---|---|
|최소값|0|
|최대값|2^64 - 1|
|기본값|1000000|

## CLUSTER_LINK_MAX_LISTEN

특정 Node와 연결할 때 Socket의 Accept Queue의 최대 크기입니다.

|(count)|Value|
|---|---|
|최소값|1|
|최대값|2^31 - 1|
|기본값|512|

## CLUSTER_LINK_MAX_POLL

특정 Node와 통신할 때 Poll에 의해 한 번에 조회할 수 있는 최대 Event 수입니다.

|(count)|Value|
|---|---|
|최소값|1|
|최대값|2^31 - 1|
|기본값|4096|

## CLUSTER_LINK_PORT_NO

특정 Node와 Cluster Socket을 연결하기 위한 현재 Node의 포트 번호입니다.

|(port)|Value|
|---|---|
|최소값|1024|
|최대값|65535|
|기본값|3868|

## CLUSTER_LINK_RECEIVE_TIMEOUT

Timeout Thread가 마지막 수신 이후 연결이 끊겼다고 판단할 때까지의 Timeout입니다.

Cluster Node 간 연결은 수신이 완료되면 종료되므로, '연결 리스트'에 있는 연결들은 계속 수신을 받고 있어야 합니다.

이 시간이 지나도록 마지막 수신 시각이 갱신되지 않으면 Timeout Thread는 Trace Log에 기록을 남기고 해당 Socket을 닫습니다.

|(usec)|Value|
|---|---|
|최소값|0|
|최대값|2^64 - 1|
|기본값|30000000|

## CLUSTER_LINK_REQUEST_TIMEOUT

Cluster Socket에서 요청 메시지를 보낸 뒤 요청에 대한 응답이 올 때까지의 Timeout입니다.

특정 메시지에 대해 Request 이후 Answer가 전송될 때까지 대기할 수 있는 시간을 지정합니다.

이 시간이 지나도록 응답 메시지가 도착하지 않으면 Trace Log에 기록을 남기고 해당 Socket을 닫습니다.

기본값은 60초입니다. 메시지 종류와 수신 처리가 어떻게 될지 알 수 없으므로 Timeout을 길게 잡았습니다.

|(usec)|Value|
|---|---|
|최소값|0|
|최대값|2^64 - 1|
|기본값|60000000|

## CLUSTER_LINK_SEND_RETRY_COUNT

* 5.6부터 사용할 수 있습니다.

송신 버퍼가 비워질 때까지 송신을 재시도하는 횟수입니다.

재시도할 때마다 1ms씩 쉽니다. 이 횟수를 넘어 재시도하게 되면 연결을 해제합니다.

기본값은 5000회입니다(재시도마다 쉬는 1ms만 합쳐도 약 5000ms).

|(count)|Value|
|---|---|
|최소값|0|
|최대값|2^32 - 1|
|기본값|5000|

## CLUSTER_LINK_SEND_TIMEOUT

Cluster Socket을 통해 메시지를 송신할 때 설정하는 Timeout입니다.

송신할 때 이 Timeout을 설정합니다.

Timeout까지 송신이 완료되지 않으면 Trace Log에 기록을 남깁니다.

|(usec)|Value|
|---|---|
|최소값|0|
|최대값|2^64 - 1|
|기본값|30000000|

## CLUSTER_LINK_SESSION_TIMEOUT

Timeout Thread가 특정 세션에서 마지막 수신 이후 연결이 끊겼다고 판단할 때까지의 Timeout입니다.

Cluster 연결은 내부적으로 모든 메시지의 세션을 관리합니다. 이 Property는 갑자기 세션을 정리하지 못하게 된 상황에 필요합니다.

이 시간이 지나도록 해당 세션의 마지막 수신 시각이 갱신되지 않으면 Timeout Thread는 Trace Log에 기록을 남기고 해당 세션을 닫습니다.

기본값은 1시간입니다.

|(usec)|Value|
|---|---|
|최소값|0|
|최대값|2^64 - 1|
|기본값|3600000000|

## CLUSTER_LINK_THREAD_COUNT

특정 Node와 통신할 때 수신된 메시지를 처리할 Thread의 수입니다.

Cluster의 규모가 커지거나 처리해야 할 연산이 많아져 수신 Thread에 여유가 없을 때 늘릴 수 있습니다.

|(count)|Value|
|---|---|
|최소값|1|
|최대값|4096|
|기본값|16|

## CLUSTER_QUERY_STAT_LOG_ENABLE

수행한 질의에 대한 통계 정보를 trace log에 출력합니다.

|(boolean)|Value|
|---|---|
|최소값|0|
|최대값|1|
|기본값|0|

## CLUSTER_REPLICATION_BLOCK_SIZE

Cluster Edition에서 Node 추가로 Replication을 진행할 때 한 번에 실어 보내는 데이터 크기입니다.

Replication Active가 되는 Warehouse(전송하는 Warehouse)에 직접 Property를 적용해야 합니다.

기본값은 640KB입니다.

|(size)|Value|
|---|---|
|최소값|64 * 1024|
|최대값|100 * 1024 * 1024|
|기본값|640 * 1024 (655360)|

## CLUSTER_WAREHOUSE_DIRECT_DML_ENABLE

Cluster Edition에서 Warehouse에 직접 접속해 DML을 수행할 수 있게 합니다.

* 1: 수행할 수 있습니다.
* 0: 수행할 수 없습니다. 에러가 반환됩니다.

Warehouse에 직접 DML을 수행하면 Broker를 통하는 것보다 성능상 이점이 있지만, 같은 Group에 DML이 전파되지 않는 문제가 있습니다.
따라서 데이터 불일치로 인한 비상 복구용이거나, Group의 데이터 불일치를 감안해도 되는 경우에만 사용합니다.

원하는 특정 Warehouse에 직접 Property를 적용해야 합니다.

기본값은 0입니다.

{{< callout type="info" >}}
이 Property를 켠 상태에서 Group 내 Warehouse 간에 데이터 차이가 발생하더라도, Coordinator는 데이터 불일치 여부를 따로 검사하지 않습니다.
{{< /callout >}}

|(boolean)|Value|
|---|---|
|최소값|0|
|최대값|1|
|기본값|0|

## COORDINATOR_DBS_PATH

Coordinator의 데이터 파일이 생성될 디렉터리를 지정합니다.

기본값은 `?/dbs`이며, `?`는 `$MACHBASE_COORDINATOR_HOME` 환경 변수로 치환됩니다.
즉 `$MACHBASE_COORDINATOR_HOME/dbs` 디렉터리를 의미합니다.

Coordinator에 적용해야 하며, 다른 Node에는 아무런 효과가 없습니다.

|(path)|Value|
|---|---|
|기본값|?/dbs|

## COORDINATOR_DDL_REQUEST_TIMEOUT

Coordinator가 Node에게 DDL 수행을 요청한 후 대기하는 Timeout입니다.

이 값은 Coordinator가 각 Node에게 DDL 수행을 요청한 후 대기하는 시간을 의미합니다.

|(usec)|Value|
|---|---|
|최소값|0|
|최대값|2^64 - 1|
|기본값|300000000|

## COORDINATOR_DDL_TIMEOUT

Broker가 Coordinator에게 DDL 수행을 요청한 후 대기하는 Timeout입니다.

이 값은 Broker가 Cluster 전체에 대한 DDL 수행을 Coordinator에게 요청한 후 대기하는 시간을 의미합니다.

|(usec)|Value|
|---|---|
|최소값|0|
|최대값|2^64 - 1|
|기본값|300000000|

## COORDINATOR_DECISION_DELAY

Coordinator가 상태 변경을 요청한 후 실제로 반영될 때까지의 Timeout입니다.

이 시간이 지나도록 실제로 상태가 변경되지 않으면 Cluster 상태를 비활성화합니다.

Warehouse Active의 상태가 변경되지 않았는데 연결된 Standby가 있으면 Fail-Over 작업을 시작합니다.

|(usec)|Value|
|---|---|
|최소값|0|
|최대값|2^64 - 1|
|기본값|1000000|

## COORDINATOR_DECISION_INTERVAL

Coordinator가 상태 변경을 얼마나 자주 결정할지 정하는 시간입니다.

|(usec)|Value|
|---|---|
|최소값|0|
|최대값|2^64 - 1|
|기본값|1000000|

## COORDINATOR_HOST_RESOURCE_ENABLE

Coordinator가 Cluster Node들의 Host Resource를 수집할지 여부입니다.

|(boolean)|Value|
|---|---|
|최소값|0 (false)|
|최대값|1 (true)|
|기본값|0 (false)|

## COORDINATOR_HOST_RESOURCE_COLLECT_INTERVAL

Cluster Node들이 Host Resource를 수집하는 주기입니다.

|(usec)|Value|
|---|---|
|최소값|0|
|최대값|2^64 - 1|
|기본값|1000000|

## COORDINATOR_HOST_RESOURCE_INTERVAL

Coordinator가 Node들과 Host Resource를 주고받는 주기입니다.

|(usec)|Value|
|---|---|
|최소값|0|
|최대값|2^64 - 1|
|기본값|1000000|

## COORDINATOR_HOST_RESOURCE_REQUEST_TIMEOUT

Coordinator가 Node들에게 Host Resource 정보를 요청한 후 대기하는 시간입니다.

|(usec)|Value|
|---|---|
|최소값|0|
|최대값|2^64 - 1|
|기본값|10000000|

## COORDINATOR_NODE_REQUEST_TIMEOUT

Coordinator가 Node에게 명령 수행을 요청한 후 대기하는 Timeout입니다.

Add/Remove-node, Add/Remove-Package 등의 Node 명령 수행이 포함되므로, 너무 짧게 설정하면 해당 명령 처리가 완료되지 못할 수 있습니다.

|(usec)|Value|
|---|---|
|최소값|0|
|최대값|2^64 - 1|
|기본값|600000000|

## COORDINATOR_NODE_TIMEOUT

Coordinator가 Node의 장애를 판단하기까지 기다리는 시간입니다.

|(usec)|Value|
|---|---|
|최소값|0|
|최대값|2^64 - 1|
|기본값|30000000|

## COORDINATOR_STARTUP_DELAY

Coordinator가 시작된 직후 Decision Thread를 작동시킬 때까지의 유예 시간입니다.

Cluster 전체 구동에 오랜 시간이 걸리면 이 값을 크게 설정해 Coordinator의 Node 제어를 더 늦게 시작할 수 있습니다.

전체 구동이 끝나기 전에 Decision Thread가 작동하면 Coordinator가 오판할 가능성이 높아집니다.

|(usec)|Value|
|---|---|
|최소값|0|
|최대값|2^64 - 1|
|기본값|3000000|

## COORDINATOR_STATUS_NODE_INTERVAL

Coordinator가 Node들과 상태 조회 메시지를 주고받는 주기입니다.

|(usec)|Value|
|---|---|
|최소값|0|
|최대값|2^64 - 1|
|기본값|1000000|

## COORDINATOR_STATUS_NODE_REQUEST_TIMEOUT

Coordinator가 Node들에게 상태 조회를 요청한 후 대기하는 시간입니다.

이 시간 동안 상태 조회 응답이 없으면 Coordinator는 해당 Node의 상태를 갱신하지 않고 계속 진행합니다.

네트워크 상황이 좋지 않은데 상태를 반드시 갱신해야 한다면 값을 늘리는 것을 고려할 수 있습니다.

대신 상태 조회 응답이 없으면 늘린 만큼 Coordinator가 반드시 기다리게 됩니다.

|(usec)|Value|
|---|---|
|최소값|0|
|최대값|2^64 - 1|
|기본값|15000000|

## COORDINATOR_DISK_FULL_UPPER_BOUND_RATIO

Cluster를 구성하는 일부 서버의 디스크 사용량이 이 값을 넘으면, 해당 호스트가 속한 Warehouse group이 DISKFULL 상태로 전환됩니다.

DISKFULL 상태의 group은 입력이 제한되고 조회 및 삭제만 가능합니다.

값이 0이면 이 기능이 비활성화됩니다.

|(percent)|Value|
|---|---|
|최소값|0|
|최대값|99|
|기본값|0|

## COORDINATOR_DISK_FULL_LOWER_BOUND_RATIO

DISKFULL 상태로 동작 중인 서버의 디스크 사용량이 이 값 미만으로 떨어지면 해당 group이 normal 상태로 전환됩니다.

값이 0이면 이 기능이 비활성화됩니다.

|(percent)|Value|
|---|---|
|최소값|0|
|최대값|99|
|기본값|0|

## DEPLOYER_DBS_PATH

Deployer의 데이터 파일이 생성될 디렉터리를 지정합니다.

기본값은 `?/dbs`이며, `?`는 `$MACHBASE_DEPLOYER_HOME` 환경 변수로 치환됩니다.
즉 `$MACHBASE_DEPLOYER_HOME/dbs` 디렉터리를 의미합니다.

Deployer에 적용해야 하며, 다른 Node에는 아무런 효과가 없습니다.

|(path)|Value|
|---|---|
|기본값|?/dbs|

## EXECUTION_STAGE_MEMORY_MAX

Cluster Edition에서 SELECT 쿼리를 수행하는 Stage Thread가 사용하는 Memory의 최대 크기입니다.

각 Stage의 최대 크기이므로, Stage 개수가 늘어나는 복잡한 SELECT 쿼리는 더 많은 메모리가 필요할 수 있습니다.
최대 크기를 넘는 Stage가 있으면 해당 Stage는 취소되고, Query도 에러와 함께 취소됩니다.

원하는 특정 Warehouse에 직접 Property를 적용해야 합니다.

기본값은 1GB입니다.

|(size)|Value|
|---|---|
|최소값|0|
|최대값|2^64 - 1|
|기본값|1024 * 1024 * 1024|

## HTTP_ADMIN_PORT

MWA 또는 `machcoordinatoradmin`으로부터 요청을 받을 포트 번호입니다.

|(port)|Value|
|---|---|
|최소값|1024|
|최대값|65535|
|기본값|5779|

## HTTP_CONNECT_TIMEOUT

`machcoordinatoradmin`과 연결할 때 사용하는 Timeout입니다.

|(usec)|Value|
|---|---|
|최소값|0|
|최대값|2^64 - 1|
|기본값|30000000|

## HTTP_RECEIVE_TIMEOUT

`machcoordinatoradmin`과 통신할 때 수신에 사용하는 Timeout입니다.

|(usec)|Value|
|---|---|
|최소값|0|
|최대값|2^64 - 1|
|기본값|3600000000|

## HTTP_SEND_TIMEOUT

`machcoordinatoradmin`과 통신할 때 송신에 사용하는 Timeout입니다.

|(usec)|Value|
|---|---|
|최소값|0|
|최대값|2^64 - 1|
|기본값|60000000|

## INSERT_BULK_DATA_MAX_SIZE

Append 또는 INSERT-SELECT를 수행할 때 입력 data block의 최대 크기입니다.

|(size)|Value|
|---|---|
|최소값|1024|
|최대값|10 * 1024 * 1024|
|기본값|1024 * 1024|

## INSERT_RECORD_COUNT_PER_NODE

입력을 수행할 때 Warehouse group 전환을 유도하는 데이터 입력 개수입니다.

|(count)|Value|
|---|---|
|최소값|1|
|최대값|2^32 - 1|
|기본값|1000|

## LOOKUPNODE_COMMAND_RETRY_MAX_COUNT

Lookup 노드에 대한 명령 및 접속이 실패했을 때의 재시도 횟수입니다.

|(count)|Value|
|---|---|
|최소값|1|
|최대값|3600|
|기본값|30|

## STAGE_RESULT_BLOCK_SIZE

하나의 Stage에서 만드는 최대 block 크기입니다.

|(size)|Value|
|---|---|
|최소값|1024|
|최대값|2^32 - 1|
|기본값|1024 * 1024|
