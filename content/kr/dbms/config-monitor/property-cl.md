---
layout : post
title : 'Property (Cluster)'
type: docs
---

[Property](../property)와 별개로, Cluster Edition 에서만 사용 가능한 Property 를 정리한다.

# 목차
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

특정 Node와 연결할 때, Accept 후 Handshake 메시지를 수신할 때까지의 Timeout.

Timeout 이후까지 수신에 실패하면, 해당 연결은 실패한다.

기본값은 5초.

|(usec)|	Value|
|------|---------|
|최소값|    0|
|최대값|	2^64 - 1|
|기본값|	5000000|

## CLUSTER_LINK_BUFFER_SIZE

송신/수신 버퍼의 크기를 의미한다.

이 크기가 모자라면 송신시 버퍼가 비워질 때 까지 재시도하게 된다.

|(byte)|	Value|
|------|---------|
|최소값|	1024768|
|최대값|	2^32 - 1|
|기본값|	33554432 (32M)|

## CLUSTER_LINK_CHECK_INTERVAL

특정 Node와 연결된 Socket들을 검사하는, Timeout Thread의 검사 주기.

RECEIVE_TIMEOUT, SESSION_TIMEOUT 을 검사하는 Timeout Thread가 존재한다.
주기를 짧게 할 수록, 자주 검사하지만 Timeout 판단은 아래의 값에 따라 이루어진다.

기본값은 1초.

|(usec)|	Value|
|------|---------|
|최소값|	0|
|최대값|	2^64 - 1|
|기본값|	1000000|

## CLUSTER_LINK_CONNECT_RETRY_TIMEOUT

특정 Node와 연결이 실패한 이후, 재연결 시도를 반복하는 Timeout

Timeout 이후까지 재연결되지 않는다면, 완전히 단절되었다고 판단한다.

기본값은 1분.

|(usec)|	Value|
|------|---------|
|최소값|	0|
|최대값|	2^64 - 1|
|기본값|	60000000|

## CLUSTER_LINK_CONNECT_TIMEOUT

특정 Node와 연결을 시도할 때, 기다리는 시간.

Timeout 이후까지 연결되지 않는다면, CLUSTER_LINK_CONNECT_RETRY_TIMEOUT 이 지나기 전 까지 재연결을 시도한다.

기본값은 5초.

|(usec)|	Value|
|------|---------|
|최소값|	0|
|최대값|	2^64 - 1|
|기본값|	5000000|

## CLUSTER_LINK_ERROR_ADD_ORIGIN_HOST

Cluster 간 통신 중 발생하는 에러 메시지에, 오류가 발생한 호스트 이름을 추가할지 여부를 선택할 수 있다.

자세한 에러 메시지를 표시하고자 한다면, 해당 Property를 켜야 한다.

기본값은 'No' (=0). 호스트 이름이 출력되지 않는다.

|(boolean)|	Value|
|------|---------|
|최소값|	0|
|최대값|	1|
|기본값|	0|

## CLUSTER_LINK_HANDSHAKE_TIMEOUT

특정 Node와 Cluster Socket으로 연결된 상태에서, Handshake 메시지를 수신할 때까지의 Timeout

연결이 막 완료된 두 Node는, 연결 상태를 점검하는 차원에서 작은 크기의 Handshake 메시지를 주고 받는다.
Accept한 Node가 Handshake 메시지를 먼저 보내는데, 그 응답을 기다리는 시간을 여기서 설정한다.

기본값은 5초.

|(usec)|	Value|
|------|---------|
|최소값|	0|
|최대값|	2^64 - 1|
|기본값|	5000000|

## CLUSTER_LINK_HOST

특정 Node와 Cluster Socket 을 연결하기 위한, 현재 Node의 호스트 이름

|(string)|	Value|
|--|--|
|기본값|	localhost|

## CLUSTER_LINK_LONG_TERM_CALLBACK_INTERVAL

Cluster Socket 으로 수신 되는 메시지를 처리할 Receive Callback 이 수행한 시간을 Long-Term Callback 으로 인식할 시간

수신 Thread의 개수가 제한적이므로, 가급적이면 Receive Callback은 오랜 시간 동안 메시지를 처리하고 있으면 안 된다.
이 시간이 지나도록 Receive Callback이 메시지를 처리하고 있다면, Long-Term Callback 으로 인식하고 Trace Log에 그 기록을 남긴다.

기본값은 1초.

|(usec)|	Value|
|------|---------|
|최소값|	0|
|최대값|	2^64 - 1|
|기본값|	1000000|

## CLUSTER_LINK_LONG_WAIT_INTERVAL

Cluster Socket 으로 수신 되는 메시지가 도착할 때 까지의 시간을 Long-Wait Message 로 인식할 시간

수신 시작~수신 종료 까지의 시간이 길면 네트워크 환경의 문제로 볼 수 있다.
이 시간이 지나도록 수신 메시지가 도착하지 않는다면, Long-Wait Message 로 인식하고 Trace Log에 그 기록을 남긴다.

기본값은 1초.

|(usec)|	Value|
|------|---------|
|최소값|	0|
|최대값|	2^64 - 1|
|기본값|	1000000|

## CLUSTER_LINK_MAX_LISTEN

특정 Node와 연결할 때, Socket의 Accept Queue 의 최대 숫자

|(count)|	Value|
|------|---------|
|최소값|	1|
|최대값|	2^32 - 1|
|기본값|	512|

## CLUSTER_LINK_MAX_POLL

특정 Node와 통신할 때, Poll에 의헤서 한번에 조회할 수 있는 최대 Event 수

|(count)|	Value|
|------|---------|
|최소값|	1|
|최대값|	2^32 - 1|
|기본값|	4096|

## CLUSTER_LINK_PORT_NO

특정 Node와 Cluster Socket 을 연결하기 위한, 현재 Node의 포트 번호

|(port)|	Value|
|------|---------|
|최소값|    1024|
|최대값|	65535|
|기본값|	3868|

## CLUSTER_LINK_RECEIVE_TIMEOUT

Timeout Thread가, 마지막 수신 이후로 연결이 끊긴 것을 판단할 때 까지의 Timeout

Cluster Node 간 연결은, 수신이 완료되면 종료되기 때문에 '연결 리스트' 에 존재하는 연결들은 지속적으로 수신을 받고 있어야 한다.
이 시간이 지나도록 마지막 수신 시각이 갱신되지 않으면, Timeout Thread는 Trace Log에 기록을 남기고 해당 Socket을 닫는다.

|(usec)|	Value|
|------|---------|
|최소값|	0|
|최대값|	2^64 - 1|
|기본값|	30000000|

## CLUSTER_LINK_REQUEST_TIMEOUT

Cluster Socket에서 요청 메시지를 보냈을 때, 요청에 대한 응답이 올 때 까지의 Timeout

특정 메시지의 경우 Request 이후 Answer 전송까지 대기할 수 있는 시간을 따로 지정한다.
이 시간이 지나도록 응답 메시지가 도착하지 않으면, Trace Log에 기록을 남기고 해당 Socket을 닫는다.

기본값은 60초. 메시지 종류와 수신 처리가 어떻게 될지 모르므로, Timeout이 길다.

|(usec)|	Value|
|------|---------|
|최소값|	0|
|최대값|	2^64 - 1|
|기본값|	60000000|

## CLUSTER_LINK_SEND_RETRY_COUNT

* 5.6 부터 사용 가능합니다.

재시도를 할 때 마다 1ms 씩 쉬게 된다. 이 회수를 넘어서서 재시도하게 될 경우 연결을 해제하게 된다.송신 버퍼가 비워질 때 까지 송신을 재시도하는 회수.

기본값은 5000.

|(count)|   Value|
|------|---------|
|최소값|	0|
|최대값|	2^32 - 1|
|기본값|	5000|

## CLUSTER_LINK_SEND_TIMEOUT

Cluster Socket을 통해 메시지를 송신할 때 설정하는 Timeout

송신할 때 해당 Timeout 을 설정하며, 
Timeout 까지 송신이 완료되지 않으면 Trace Log에 그 기록을 남긴다.

|(usec)|	Value|
|------|---------|
|최소값|	0|
|최대값|	2^64 - 1|
|기본값|	30000000|

## CLUSTER_LINK_SESSION_TIMEOUT

Timeout Thread가, 특정 세션에서 마지막 수신 이후로 연결이 끊긴 것을 판단할 때 까지의 Timeout

Cluster 연결은, 내부적으로 모든 메시지의 세션을 관리하고 있다. 갑자기 세션 정리를 하지 못하게 된 상황에서 필요한 Property 이다.
이 시간이 지나도록 해당 세션에 대한 마지막 수신 시각이 갱신되지 않으면, Timeout Thread는 Trace Log에 기록을 남기고 해당 세션을 닫는다.

기본값은 1시간.

|(usec)|	Value|
|------|---------|
|최소값|	0|
|최대값|	2^64 - 1|
|기본값|	3600000000|

## CLUSTER_LINK_THREAD_COUNT

특정 Node와 통신할 때, 수신된 메시지를 처리할 Thread의 수

Cluster의 규모가 커지거나, 처리해야 할 연산의 개수가 많아져서 수신 가능한 Thread 가 여유가 없을 때 늘릴 수 있다.

|(count)|	Value|
|------|---------|
|최소값|	1|
|최대값|	4096|
|기본값|	8|

## CLUSTER_QUERY_STAT_LOG_ENABLE

수행한 질의에 대한 통계정보를 trace log에 출력한다.

|(boolean)|	Value|
|------|---------|
|최소값|	0|
|최대값|	1|
|기본값|	0|

## CLUSTER_REPLICATION_BLOCK_SIZE

Cluster Edition 에서, Node 추가로 Replication 을 진행할 때, 한번에 실어 보내는 데이터 크기.

Replication Active 가 되는 Warehouse (=전송을 하는 Warehouse) 에 직접 Property 를 적용해야 한다.

기본값은 640KB 이다.

|(size)|	Value|
|------|---------|
|최소값|	64 * 1024|
|최대값|    100 * 1024 * 1024|
|기본값|	640 * 1024 (655360)|


## CLUSTER_WAREHOUSE_DIRECT_DML_ENABLE

Cluster Edition 에서, Warehouse 에 곧바로 접속해 DML 을 수행할 수 있도록 한다.

* 1 : 수행 가능
* 2 : 수행 불가능. 에러가 반환된다.

Warehouse 에 직접 DML 을 수행할 경우 Broker 를 통한 것보다 성능 이점이 있지만, 동일 Group 에 DML 이 전파되지 않는 문제가 있다. 
따라서, 데이터 불일치로 인한 비상 복구용 혹은 Group 의 데이터 불일치를 감안해도 되는 경우에 한해 사용한다.

원하는 특정 Warehouse 에 직접 Property 를 적용해야 한다.

기본값은 0이다.

{{<callout type="info">}}
해당 Property 를 켠 채로 Group 내 Warehouse 간의 데이터 차이가 발생하더라도, Coordinator 는 데이터 불일치 여부를 별도로 검사하지 않는다.
{{</callout>}}

|(boolean)|	Value|
|------|---------|
|최소값|	0|
|최대값|	1|
|기본값|	0|

## COORDINATOR_DBS_PATH

Coordinator 의 데이터 파일이 생성될 디렉터리를 지정한다.

기본값은 ?/dbs 로 설정되어 있으며, ? 는 $MACHBASE_COORDINATOR_HOME 환경변수로 치환된다.
이는 환경변수 $MACHBASE_COORDINATOR_HOME/dbs 디렉터리라는 의미이다.

Coordinator 에 적용해야 하며, 다른 Node 에는 아무런 효과가 없다.

|(path)|	Value|
|------|---------|
|기본값|	?/dbs|


## COORDINATOR_DDL_REQUEST_TIMEOUT

Coordinator가 Node에게 DDL 수행을 요청한 후 대기할 때 까지의 Timeout

이 값은 Coordinator가 각 Node에게 DDL 수행을 요청한 후 대기할 때 까지를 말한다.

|(usec)|	Value|
|------|---------|
|최소값|	0|
|최대값|	2^64 - 1|
|기본값|	300000000|

## COORDINATOR_DDL_TIMEOUT

Broker가 Coordinator에게 DDL 수행을 요청한 후 대기할 때 까지의 Timeout

이 값은 Broker가 Cluster 전체에 대한 DDL 수행을 Coordinator에게 요청한 후 대기할 때 까지를 의미한다.

|(usec)|	Value|
|------|---------|
|최소값|	0|
|최대값|	2^64 - 1|
|기본값|	3600000000|

## COORDINATOR_DECISION_DELAY

Coordinator가 상태 변경을 요청하고 실제로 반영할 때 까지의 Timeout.

이 시간이 지나도록 실제로 상태가 변경되지 않는 경우, Cluster 상태를 비활성화시킨다.
만약 Warehouse Active의 상태가 변경되지 않았는데 연결된 Standby가 존재하는 경우, Fail-Over 작업을 시작한다.

|(usec)|	Value|
|------|---------|
|최소값|	0|
|최대값|	2^64 - 1|
|기본값|	1000000|

## COORDINATOR_DECISION_INTERVAL

Coordinator가 상태 변경을 얼마나 자주 할지 결정할 시간.

|(usec)|	Value|
|------|---------|
|최소값|	0|
|최대값|	2^64 - 1|
|기본값|	1000000|

## COORDINATOR_HOST_RESOURCE_ENABLE

Coordinator가 Cluster Node들의 Host Resource 수집 여부

|(boolean)|	Value|
|------|---------|
|최소값|	0(false)|
|최대값|	1(true)|
|기본값|	0(false)|

## COORDINATOR_HOST_RESOURCE_COLLECT_INTERVAL

Cluster Node들이 Host Resource를 수집하는 주기

|(usec)|	Value|
|------|---------|
|최소값|	0|
|최대값|	2^64 - 1|
|기본값|	1000000|

## COORDINATOR_HOST_RESOURCE_INTERVAL

Coordinator가 Node들과 Host Resource를 주고받는 주기

|(usec)|	Value|
|------|---------|
|최소값|	0|
|최대값|	2^64 - 1|
|기본값|	1000000|

## COORDINATOR_HOST_RESOURCE_REQUEST_TIMEOUT

Coordinator가 Node들에게 Host Resource 정보를 요청한 이후 대기할 시간

|(usec)|	Value|
|------|---------|
|최소값|	0|
|최대값|	2^64 - 1|
|기본값|	10000000|

## COORDINATOR_NODE_REQUEST_TIMEOUT

Coordinator가 Node에게 명령을 수행하도록 요청한 후 대기할 때 까지의 Timeout

Add/Remove-node, Add/Remove-Package 등의 Node 명령 수행이 포함되어 있어, 짧은 시간으로 잡을 경우 해당 명령 처리가 완료되지 못할 수 있다.

|(usec)|	Value|
|------|---------|
|최소값|	0|
|최대값|	2^64 - 1|
|기본값|	600000000|

## COORDINATOR_NODE_TIMEOUT

Coordinator가 Node의 장애를 판단하기 까지 기다릴 시간.

|(usec)|	Value|
|------|---------|
|최소값|	0|
|최대값|	2^64 - 1|
|기본값|	30000000|

## COORDINATOR_STARTUP_DELAY

Coordinator 시작 직후 Decision Thread를 작동시킬 때 까지의 유예 시간.

Cluster 전체 구동에 오랜 시간이 소요되는 경우, 해당 값을 크게 설정해서 Coordinator의 Node 제어를 더욱 늦게 시작할 수 있다.
전체 구동도 하기 전에 Decision Thread가 작동하는 경우, Coordinator가 오판할 가능성이 높아진다.

|(usec)|	Value|
|------|---------|
|최소값|	0|
|최대값|	2^64 - 1|
|기본값|	3000000|

## COORDINATOR_STATUS_NODE_INTERVAL

Coordinator가 Node들과 상태 조회 메시지를 주고 받을 주기

|(usec)|	Value|
|------|---------|
|최소값|	0|
|최대값|	2^64 - 1|
|기본값|	1000000|

## COORDINATOR_STATUS_NODE_REQUEST_TIMEOUT

Coordinator가 Node들에게 상태 조회 요청을 한 이후 대기할 시간.

해당 시간동안 상태 조회 응답이 없으면, Coordinator는 해당 Node의 상태를 갱신하지 않고 계속 진행한다.
네트워크 상황이 좋지 않은데 상태 갱신을 반드시 해야 하는 경우엔, 값을 늘리는 것을 고려해 볼 수 있다.
대신, 상태 조회 응답이 없을 경우엔 값을 늘린 만큼 Coordinator에서 반드시 기다리게 된다.

|(usec)|	Value|
|------|---------|
|최소값|	0|
|최대값|	2^64 - 1|
|기본값|	15000000|

## COORDINATOR_DISK_FULL_UPPER_BOUND_RATIO

Cluster 로 구성중인 일부 서버의 디스크 사용량이 프로퍼티 값을 넘어가면 해당 host 가 속한 group 이 DISKFULL 상태로 전환된다.
DISKFULL 상태의 group 에 대해서는 입력이 제한되고 조회 및 삭제만 가능하다.

프로퍼티 값이 0 인 경우 해당 기능이 disable 된다.

|(percent)|	Value|
|------|---------|
|최소값|	0|
|최대값|	99|
|기본값|	0|

## COORDINATOR_DISK_FULL_LOWER_BOUND_RATIO

DISKFULL 상태로 동작중인 서버의  디스크 사용량이 프로퍼티 값 이하로 떨어질 경우 해당 group 이 normal 상태로 전환된다.

프로퍼티 값이 0 인 경우 해당 기능이 disable 된다.

|(percent)|	Value|
|------|---------|
|최소값|	0|
|최대값|    99|
|기본값|	0|

## DEPLOYER_DBS_PATH

Deployer 의 데이터 파일이 생성될 디렉터리를 지정한다.

기본값은 ?/dbs 로 설정되어 있으며, ? 는 $MACHBASE_DEPLOYER_HOME 환경변수로 치환된다.
이는 환경변수 $MACHBASE_DEPLOYER_HOME /dbs 디렉터리라는 의미이다.

Deployer 에 적용해야 하며, 다른 Node 에는 아무런 효과가 없다.

|(path)|	Value|
|------|---------|
|기본값|	?/dbs|

## EXECUTION_STAGE_MEMORY_MAX

Cluster Edition 에서, SELECT 쿼리를 수행하는 Stage Thread 가 사용하는 Memory 의 최대 크기.

각 Stage 의 최대 크기이므로, Stage 개수가 늘어나는 복잡한 SELECT 쿼리의 경우 요구 메모리가 더 커질 수 있다.
최대 크기를 넘는 Stage 가 존재하는 경우, 해당 Stage 는 취소되고 Query 역시 에러와 함께 취소된다.

원하는 특정 Warehouse 에 직접 Property 를 적용해야 한다.

기본값은 1GB 이다.

|(size)|    Value|
|------|---------|
|최소값|	1024|
|최대값|	2^64 - 1|
|기본값|	1024 *1024 * 1024|

## HTTP_ADMIN_PORT

MWA 또는 machcoordinatoradmin 으로부터 요청을 받을 port number

|(port)|    Value|
|------|---------|
|최소값|	1024|
|최대값|	65535|
|기본값|	5779|

## HTTP_CONNECT_TIMEOUT

machcoordinatoradmin 과 연결할 때 사용하는 timeout

|(usec)|	Value|
|------|---------|
|최소값|	0|
|최대값|	2^64 - 1|
|기본값|	30000000|

## HTTP_RECEIVE_TIMEOUT

machcoordinatoradmin 과 통신할 때 사용하는 timeout

|(usec)|	Value|
|------|---------|
|최소값|	0|
|최대값|	2^64 - 1|
|기본값|	3600000000|

## HTTP_SEND_TIMEOUT

machcoordinatoradmin 과 통신할 때 사용하는 timeout

|(usec)|	Value|
|------|---------|
|최소값|	0|
|최대값|	2^64 - 1|
|기본값|	60000000|

## INSERT_BULK_DATA_MAX_SIZE

Append 또는 INSERT-SELECT 수행 시 입력 data block의 최대 크기

|(size)|	Value|
|------|---------|
|최소값|	1024|
|최대값|	10 * 1024 * 1024|
|기본값|	1024 * 1024|

## INSERT_RECORD_COUNT_PER_NODE

입력 수행시 warehouse group 전환을 유도하는 data 입력 개수.

|(count)|	Value|
|------|---------|
|최소값|	1|
|최대값|	2^64 - 1|
|기본값|	10000|

## LOOKUPNODE_COMMAND_RETRY_MAX_COUNT

Lookup 노드에 명령 및 접속 실패시 재시도 횟수

|(count)|   Value|
|------|---------|
|최소값|	1|
|최대값|	3600|
|기본값|	30|

## STAGE_RESULT_BLOCK_SIZE

하나의 stage 에서 만드는 최대 block 크기

|(size)|    Value|
|------|---------|
|최소값|	1024|
|최대값|	2^64 - 1|
|기본값|	1024 * 1024|

