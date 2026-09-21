---
layout : post
title : Property (Cluster)
type : docs
weight: 0
---

Separate from [Property](../property), this page lists the properties available only in Cluster Edition.

## Index

- [Index](#index)
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

Timeout until a Handshake message is received after Accept when connecting to a specific Node.

If the message is not received within the timeout, the connection fails.

The default value is 5 seconds.

|(usec)|Value|
|---|---|
|Minimum|0|
|Maximum|2^64 - 1|
|Default|5000000|

## CLUSTER_LINK_BUFFER_SIZE

The size of the send/receive buffer.

If this size is insufficient, sending is retried until the buffer is emptied.

|(byte)|Value|
|---|---|
|Minimum|1024768|
|Maximum|2^32 - 1|
|Default|33554432 (32M)|

## CLUSTER_LINK_CHECK_INTERVAL

Check interval of the Timeout Thread that checks the Sockets connected to a specific Node.

A Timeout Thread checks `RECEIVE_TIMEOUT` and `SESSION_TIMEOUT`.

The shorter the interval, the more often the check runs, but timeouts are still determined by the respective timeout values.

The default value is 1 second.

|(usec)|Value|
|---|---|
|Minimum|0|
|Maximum|2^64 - 1|
|Default|1000000|

## CLUSTER_LINK_CONNECT_RETRY_TIMEOUT

Timeout during which reconnection attempts are repeated after a connection to a specific Node fails.

If the connection is not restored within the timeout, the Node is considered completely disconnected.

The default value is 1 minute.

|(usec)|Value|
|---|---|
|Minimum|0|
|Maximum|2^64 - 1|
|Default|60000000|

## CLUSTER_LINK_CONNECT_TIMEOUT

Time to wait when trying to connect to a specific Node.

If the connection is not made within the timeout, reconnection is attempted until `CLUSTER_LINK_CONNECT_RETRY_TIMEOUT` has passed.

The default value is 5 seconds.

|(usec)|Value|
|---|---|
|Minimum|0|
|Maximum|2^64 - 1|
|Default|5000000|

## CLUSTER_LINK_ERROR_ADD_ORIGIN_HOST

Selects whether to add the name of the host where the error occurred to error messages raised during communication within the Cluster.

To display detailed error messages, set this property to 1.

The default value is 1, which means the host name is displayed.

|(boolean)|Value|
|---|---|
|Minimum|0|
|Maximum|1|
|Default|1|

## CLUSTER_LINK_HANDSHAKE_TIMEOUT

Timeout until a Handshake message is received while connected to a specific Node through a Cluster Socket.

Two Nodes that have just connected exchange small Handshake messages to check the connection status.

The accepting Node sends the Handshake message first, and this property sets how long to wait for the response.

The default value is 5 seconds.

|(usec)|Value|
|---|---|
|Minimum|0|
|Maximum|2^64 - 1|
|Default|5000000|

## CLUSTER_LINK_HOST

Host name of the current Node used to connect to a specific Node through a Cluster Socket.

|(string)|Value|
|---|---|
|Default|localhost|

## CLUSTER_LINK_LONG_TERM_CALLBACK_INTERVAL

If the Receive Callback that processes a message received on a Cluster Socket runs longer than this value, it is recognized as a Long-Term Callback.

Since the number of receive Threads is limited, a Receive Callback should not process messages for a long time.

If a Receive Callback is still processing a message after this time, it is recognized as a Long-Term Callback and recorded in the Trace Log.

The default value is 1 second.

|(usec)|Value|
|---|---|
|Minimum|0|
|Maximum|2^64 - 1|
|Default|1000000|

## CLUSTER_LINK_LONG_WAIT_INTERVAL

If the time until a message arrives on a Cluster Socket exceeds this value, it is recognized as a Long-Wait Message.

A long time from the start to the end of receiving can indicate a problem in the network environment.

If the message has not arrived after this time, it is recognized as a Long-Wait Message and recorded in the Trace Log.

The default value is 1 second.

|(usec)|Value|
|---|---|
|Minimum|0|
|Maximum|2^64 - 1|
|Default|1000000|

## CLUSTER_LINK_MAX_LISTEN

The maximum size of the Socket Accept Queue when connecting to a specific Node.

|(count)|Value|
|---|---|
|Minimum|1|
|Maximum|2^31 - 1|
|Default|512|

## CLUSTER_LINK_MAX_POLL

The maximum number of Events that can be retrieved at a time by Poll when communicating with a specific Node.

|(count)|Value|
|---|---|
|Minimum|1|
|Maximum|2^31 - 1|
|Default|4096|

## CLUSTER_LINK_PORT_NO

Port number of the current Node used to connect to a specific Node through a Cluster Socket.

|(port)|Value|
|---|---|
|Minimum|1024|
|Maximum|65535|
|Default|3868|

## CLUSTER_LINK_RECEIVE_TIMEOUT

Timeout until the Timeout Thread determines that a connection has been lost since the last receive.

Because a connection between Cluster Nodes is closed when receiving is complete, connections in the 'Linked List' must keep receiving.

If the last receive time is not updated within this time, the Timeout Thread records it in the Trace Log and closes the Socket.

|(usec)|Value|
|---|---|
|Minimum|0|
|Maximum|2^64 - 1|
|Default|30000000|

## CLUSTER_LINK_REQUEST_TIMEOUT

Timeout from sending a request message on a Cluster Socket until the response to the request is received.

For specific messages, this sets how long to wait after the request until the answer is sent.

If the response message does not arrive within this time, it is recorded in the Trace Log and the Socket is closed.

The default value is 60 seconds. The timeout is long because the kind of message and how it will be processed on the receiving side are not known in advance.

|(usec)|Value|
|---|---|
|Minimum|0|
|Maximum|2^64 - 1|
|Default|60000000|

## CLUSTER_LINK_SEND_RETRY_COUNT

* Available from 5.6.

Number of times to retry sending until the send buffer is emptied.

Each retry pauses for 1 ms. If retries exceed this number, the connection is closed.

The default value is 5000 retries (about 5000 msec in total from the 1 ms pauses alone).

|(count)|Value|
|---|---|
|Minimum|0|
|Maximum|2^32 - 1|
|Default|5000|

## CLUSTER_LINK_SEND_TIMEOUT

Timeout set when sending messages through a Cluster Socket.

This timeout is applied when sending.

If sending is not completed within the timeout, it is recorded in the Trace Log.

|(usec)|Value|
|---|---|
|Minimum|0|
|Maximum|2^64 - 1|
|Default|30000000|

## CLUSTER_LINK_SESSION_TIMEOUT

Timeout until the Timeout Thread determines that a connection has been lost since the last receive in a specific session.

A Cluster connection manages the sessions of all messages internally. This property is needed when sessions suddenly cannot be cleaned up.

If the last receive time for the session is not updated within this time, the Timeout Thread records it in the Trace Log and closes the session.

The default value is 1 hour.

|(usec)|Value|
|---|---|
|Minimum|0|
|Maximum|2^64 - 1|
|Default|3600000000|

## CLUSTER_LINK_THREAD_COUNT

The number of Threads that process received messages when communicating with a specific Node.

If the Cluster grows or the number of operations to process increases so that no receive Thread is free, you can increase this value.

|(count)|Value|
|---|---|
|Minimum|1|
|Maximum|4096|
|Default|16|

## CLUSTER_QUERY_STAT_LOG_ENABLE

Outputs statistics about executed queries to the trace log.

|(boolean)|Value|
|---|---|
|Minimum|0|
|Maximum|1|
|Default|0|

## CLUSTER_REPLICATION_BLOCK_SIZE

The size of data sent at once when Replication runs for a Node being added in Cluster Edition.

The property must be applied directly to the Warehouse that becomes Replication Active (the sending Warehouse).

The default value is 640KB.

|(size)|Value|
|---|---|
|Minimum|64 * 1024|
|Maximum|100 * 1024 * 1024|
|Default|640 * 1024 (655360)|

## CLUSTER_WAREHOUSE_DIRECT_DML_ENABLE

Allows DML to be executed by connecting directly to a Warehouse in Cluster Edition.

* 1: Executable.
* 0: Not executable. An error is returned.

Executing DML directly on a Warehouse has performance advantages over going through a Broker, but the DML is not propagated to the rest of the same Group.
Therefore, use it only for emergency recovery from data discrepancies, or when data discrepancies within the Group are acceptable.

You must apply the property directly to each Warehouse you want.

The default value is 0.

{{< callout type="info" >}}
Even if data differs between Warehouses in the Group while this property is on, the Coordinator does not check for data discrepancies.
{{< /callout >}}

|(boolean)|Value|
|---|---|
|Minimum|0|
|Maximum|1|
|Default|0|

## COORDINATOR_DBS_PATH

Specifies the directory where the Coordinator data files are created.

The default value is `?/dbs`, and `?` is replaced with the `$MACHBASE_COORDINATOR_HOME` environment variable.
That is, it means the `$MACHBASE_COORDINATOR_HOME/dbs` directory.

It must be applied to the Coordinator, and it has no effect on other Nodes.

|(path)|Value|
|---|---|
|Default|?/dbs|

## COORDINATOR_DDL_REQUEST_TIMEOUT

Timeout the Coordinator waits after requesting a Node to execute DDL.

This value is the time the Coordinator waits after requesting each Node to execute DDL.

|(usec)|Value|
|---|---|
|Minimum|0|
|Maximum|2^64 - 1|
|Default|300000000|

## COORDINATOR_DDL_TIMEOUT

Timeout the Broker waits after requesting the Coordinator to execute DDL.

This value is the time the Broker waits after requesting the Coordinator to execute DDL for the entire Cluster.

|(usec)|Value|
|---|---|
|Minimum|0|
|Maximum|2^64 - 1|
|Default|300000000|

## COORDINATOR_DECISION_DELAY

Timeout from when the Coordinator requests a status change until the change actually takes effect.

If the status does not actually change within this time, the Cluster status is deactivated.

If the status of the Warehouse Active has not changed but a connected Standby exists, the Fail-Over operation starts.

|(usec)|Value|
|---|---|
|Minimum|0|
|Maximum|2^64 - 1|
|Default|1000000|

## COORDINATOR_DECISION_INTERVAL

Time that determines how often the Coordinator decides on status changes.

|(usec)|Value|
|---|---|
|Minimum|0|
|Maximum|2^64 - 1|
|Default|1000000|

## COORDINATOR_HOST_RESOURCE_ENABLE

Whether the Coordinator collects Host Resources of the Cluster Nodes.

|(boolean)|Value|
|---|---|
|Minimum|0 (false)|
|Maximum|1 (true)|
|Default|0 (false)|

## COORDINATOR_HOST_RESOURCE_COLLECT_INTERVAL

Interval at which Cluster Nodes collect Host Resources.

|(usec)|Value|
|---|---|
|Minimum|0|
|Maximum|2^64 - 1|
|Default|1000000|

## COORDINATOR_HOST_RESOURCE_INTERVAL

Interval at which the Coordinator exchanges Host Resources with Nodes.

|(usec)|Value|
|---|---|
|Minimum|0|
|Maximum|2^64 - 1|
|Default|1000000|

## COORDINATOR_HOST_RESOURCE_REQUEST_TIMEOUT

Time the Coordinator waits after requesting Host Resource information from Nodes.

|(usec)|Value|
|---|---|
|Minimum|0|
|Maximum|2^64 - 1|
|Default|10000000|

## COORDINATOR_NODE_REQUEST_TIMEOUT

Timeout the Coordinator waits after requesting a Node to execute a command.

Because this includes Node commands such as Add/Remove-node and Add/Remove-Package, setting it too short can prevent those commands from completing.

|(usec)|Value|
|---|---|
|Minimum|0|
|Maximum|2^64 - 1|
|Default|600000000|

## COORDINATOR_NODE_TIMEOUT

Time the Coordinator waits before determining that a Node has failed.

|(usec)|Value|
|---|---|
|Minimum|0|
|Maximum|2^64 - 1|
|Default|30000000|

## COORDINATOR_STARTUP_DELAY

Grace time from Coordinator startup until the Decision Thread is activated.

If starting the entire Cluster takes a long time, set a larger value so that the Coordinator starts controlling Nodes later.

If the Decision Thread runs before the entire Cluster is up, the Coordinator is more likely to make wrong decisions.

|(usec)|Value|
|---|---|
|Minimum|0|
|Maximum|2^64 - 1|
|Default|3000000|

## COORDINATOR_STATUS_NODE_INTERVAL

Interval at which the Coordinator exchanges status inquiry messages with Nodes.

|(usec)|Value|
|---|---|
|Minimum|0|
|Maximum|2^64 - 1|
|Default|1000000|

## COORDINATOR_STATUS_NODE_REQUEST_TIMEOUT

Time the Coordinator waits after sending status inquiries to Nodes.

If there is no response within this time, the Coordinator continues without updating the status of that Node.

If the network is in poor condition and the status must be updated, consider increasing this value.

However, when there is no response, the Coordinator always waits for the full, increased time.

|(usec)|Value|
|---|---|
|Minimum|0|
|Maximum|2^64 - 1|
|Default|15000000|

## COORDINATOR_DISK_FULL_UPPER_BOUND_RATIO

If the disk usage of any server in the Cluster exceeds this value, the Warehouse group to which that host belongs enters the DISKFULL state.

Input is restricted for a group in the DISKFULL state; only queries and deletions are allowed.

If the value is 0, this feature is disabled.

|(percent)|Value|
|---|---|
|Minimum|0|
|Maximum|99|
|Default|0|

## COORDINATOR_DISK_FULL_LOWER_BOUND_RATIO

If the disk usage of a server operating in the DISKFULL state falls below this value, the group returns to the normal state.

If the value is 0, this feature is disabled.

|(percent)|Value|
|---|---|
|Minimum|0|
|Maximum|99|
|Default|0|

## DEPLOYER_DBS_PATH

Specifies the directory where the Deployer data files are created.

The default value is `?/dbs`, and `?` is replaced with the `$MACHBASE_DEPLOYER_HOME` environment variable.
That is, it means the `$MACHBASE_DEPLOYER_HOME/dbs` directory.

It must be applied to the Deployer, and it has no effect on other Nodes.

|(path)|Value|
|---|---|
|Default|?/dbs|

## EXECUTION_STAGE_MEMORY_MAX

The maximum amount of Memory used by a Stage Thread that executes SELECT queries in Cluster Edition.

Because this is the maximum for each Stage, complex SELECT queries with more Stages can require more memory.
If a Stage exceeds the maximum size, the Stage is canceled and the Query is also canceled with an error.

You must apply the property directly to each Warehouse you want.

The default value is 1GB.

|(size)|Value|
|---|---|
|Minimum|0|
|Maximum|2^64 - 1|
|Default|1024 * 1024 * 1024|

## HTTP_ADMIN_PORT

Port number that receives requests from MWA or `machcoordinatoradmin`.

|(port)|Value|
|---|---|
|Minimum|1024|
|Maximum|65535|
|Default|5779|

## HTTP_CONNECT_TIMEOUT

Timeout used when connecting to `machcoordinatoradmin`.

|(usec)|Value|
|---|---|
|Minimum|0|
|Maximum|2^64 - 1|
|Default|30000000|

## HTTP_RECEIVE_TIMEOUT

Timeout used for receiving when communicating with `machcoordinatoradmin`.

|(usec)|Value|
|---|---|
|Minimum|0|
|Maximum|2^64 - 1|
|Default|3600000000|

## HTTP_SEND_TIMEOUT

Timeout used for sending when communicating with `machcoordinatoradmin`.

|(usec)|Value|
|---|---|
|Minimum|0|
|Maximum|2^64 - 1|
|Default|60000000|

## INSERT_BULK_DATA_MAX_SIZE

Maximum size of an input data block when executing Append or INSERT-SELECT.

|(size)|Value|
|---|---|
|Minimum|1024|
|Maximum|10 * 1024 * 1024|
|Default|1024 * 1024|

## INSERT_RECORD_COUNT_PER_NODE

Number of input records after which input switches to another Warehouse group.

|(count)|Value|
|---|---|
|Minimum|1|
|Maximum|2^32 - 1|
|Default|1000|

## LOOKUPNODE_COMMAND_RETRY_MAX_COUNT

Number of retries when a command to, or a connection to, a Lookup node fails.

|(count)|Value|
|---|---|
|Minimum|1|
|Maximum|3600|
|Default|30|

## STAGE_RESULT_BLOCK_SIZE

Maximum size of a block created in one Stage.

|(size)|Value|
|---|---|
|Minimum|1024|
|Maximum|2^32 - 1|
|Default|1024 * 1024|
