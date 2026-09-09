---
type: docs
title: '16.6.10 Version and Compatibility'
weight: 100
toc: true
---

This page covers Machbase 8.7.0 backward compatibility, upgrade considerations, and supported
operating systems/platforms.

## 8.7.0 Backward Compatibility

### Client Driver Compatibility

| Server Version | 8.5 Client Driver | 8.7.0 Client Driver |
|-----------|:---------------------:|:---------------------:|
| 8.7.0 server | Limited compatibility | Full compatibility |
| 8.5 server | Full compatibility | Backward compatible |

- With an 8.5 client driver, some new features of an 8.7.0 server may be unavailable.
- Older server or driver combinations may return legacy or indeterminate nullable metadata.
  Applications that depend on this metadata must upgrade both the server and SDK
  to 8.7.0.
- SQL using all CAST target types and length/precision options requires an 8.7.0 server.
  Conversion of an entire numeric ARRAY to another type with the same cardinality through
  `CAST(array_expression AS TYPE[N])` is also available from this version. In Cluster Edition,
  all nodes must run the same version with CAST and ARRAY support. For syntax and conversion rules,
  see the [CAST Function](/dbms/reference/sql/functions/functions-full/#cast).
- 8.7.0 servers support `CREATE INDEX IF NOT EXISTS`. If the same index name already exists for
  the same database and owner, it succeeds while retaining the existing definition. Verify actual
  index mappings after repeated deployments. Older servers do not support this syntax. For details,
  see [INDEX Syntax](/dbms/reference/sql/syntax/index-syntax/#create-index-if-not-exists).

- 8.7.0 Standard Edition servers support positional and named bind parameters for NAME and
  BASETIME predicate values in TAG data UPDATE. Older servers may reject the same prepared
  UPDATE with `ERR-02190`. For predicate forms and SDK APIs, see
  [TAG Data UPDATE Bind Parameters](/dbms/reference/sql/syntax/dml-syntax/tag-data-update-syntax/#tag-data-update-predicate-bind).

- BASE DISTANCE TAG statistics views on 8.7.0 servers expose axis columns with `*_DISTANCE` names
  and their original `DOUBLE`, `LONG`, or `ULONG` types. Legacy `*_TIME` names are not provided
  as aliases. Existing tables also use the new schema after a server restart. The BASE TIME TAG
  `*_TIME DATETIME` schema is unchanged. Update application SQL and result mappings using the
  conversion table in [Per-tag Statistics Views](/dbms/tag-table-usage/query-analysis/#tag-stat-axis-schema).

- In 8.7.0 Standard Edition, SELECT/JOIN plan improvements may change table scan order and
  unordered result order compared with older versions. Use `ORDER BY` when order matters.
  After upgrading, verify both results and execution plans using the procedure in
  [SELECT/JOIN Optimizer](/dbms/performance-tuning/performance-query-tuning/#select-join-optimizer).
- With multi-host URLs, the 8.7.0 JDBC driver tries the next host after a connection-stage I/O
  error. If an older driver terminates on certain socket errors at the first host, replace it
  with the 8.7.0 JDBC driver and check the URL and timeout settings in
  [Multi-host Connections](/dbms/development-tools-integration/jdbc/#jdbc-multi-host).

- Machbase DBMS 8.7.0 supports fixed-length numeric ARRAYs and selected-column Append. Applications
  using ARRAYs must pair a DBMS 8.7.0 server with an SDK build containing the feature. Upgrade
  all Cluster Edition nodes together. For SQL and API details, see
  [Numeric ARRAY Types](/dbms/reference/sql/types/array/) and
  [Sparse ARRAY and Selected-column Append APIs](/dbms/development-tools-integration/data-input-load-export/array-append/).

- ARRAY columns support `ADD COLUMN` and `DROP COLUMN` in Standard Edition LOG, VOLATILE, LOOKUP,
  TRANSACTION, and TAG METADATA, and in Cluster Edition LOG tables. For differences in DEFAULT
  application to existing rows by table type, see
  [DDL Syntax](/dbms/reference/sql/syntax/ddl-syntax/#add-column).

- Public ARRAY positions are 0-based. Code using the initial 1-based ARRAY SQL, sparse objects,
  or indexed Append targets must decrement each position by one. Stored ARRAY data and dense
  element order are unchanged, so data migration is unnecessary.
- For feature differences by server/SDK combination, see [Server and SDK Compatibility](../compatibility-xma-protocol/).

<a id="removed-features-870"></a>

### Features Removed in 8.7.0

Machbase 8.7.0 does not provide the following features or interfaces. There is no compatibility
layer for removed settings, SQL, or C APIs. Update configuration files, operational SQL, and
applications before upgrading.

| 8.5 Feature or Interface | 8.7.0 Status | User Impact | Migration |
|--------------------------|------------|-------------|-----------|
| DB HTTP/REST (`/machbase`, `/machiot`, port 5657) | Removed | Existing HTTP query and Append requests are unavailable | Use SQLCLI, ODBC, JDBC, Python, Go, Node.js, or .NET SDKs |
| WebAdmin/MWA, static ClusterAdmin UI | Removed | Web UIs and associated startup scripts are unavailable | Use server and cluster command-line tools |
| STREAM SQL and catalogs | Removed | Registered STREAMs cannot run or expose status | Use Fluentd or application jobs |
| Result Cache | Removed | Result cache settings, status queries, and flush commands are unavailable | Use indexes, ROLLUP, query optimization, or application caches |
| `machcli.h` and `MachCLI*()` | Removed | Existing C/C++ source and binaries cannot be used unchanged | Migrate to Machbase SQLCLI or ODBC |

The following similarly named features remain supported.

| Retained Feature | Description |
|-----------|------|
| Machbase SQLCLI | `SQL*` APIs in `<machbase_sqlcli.h>`. This API set is separate from ODBC. |
| ODBC, JDBC, and language SDKs | Supported drivers, including Python, Go, Node.js, and .NET, remain available. |
| MachEngine API | Existing `Mach*` APIs remain available. |
| PVO Cache | Reuses execution plan objects; it is distinct from the removed Result Cache. |
| Coordinator administration REST | Administration API, separate from data SQL REST. The Coordinator `/admin/` path remains available. |

#### Clean Up Configuration Before Upgrading

If the following properties remain in the 8.7.0 `machbase.conf`, they are treated as unknown
properties and prevent server startup. Remove them all before replacing the binaries.

```text
HTTP_AUTH
HTTP_ENABLE
HTTP_MAX_MEM
HTTP_PORT_NO
RS_CACHE_APPROXIMATE_RESULT_ENABLE
RS_CACHE_ENABLE
RS_CACHE_MAX_MEMORY_PER_QUERY
RS_CACHE_MAX_MEMORY_SIZE
RS_CACHE_MAX_RECORD_PER_QUERY
RS_CACHE_TIME_BOUND_MSEC
STREAM_THREAD_COUNT
STREAM_WAIT_MS
```

If existing STREAM definitions are needed, record `V$STREAMS` and the associated SQL before
stopping the 8.5 server. In 8.7.0, `SYS_STREAM_STMTS`, `V$STREAMS`, `V$HTTP_STATUS`,
`V$RS_CACHE_LIST`, and `V$RS_CACHE_STAT` are not registered.

After upgrading, verify that each query below returns `0`.

```sql
SELECT COUNT(*) AS removed_property_count
FROM V$PROPERTY
WHERE NAME IN (
    'HTTP_AUTH', 'HTTP_ENABLE', 'HTTP_MAX_MEM', 'HTTP_PORT_NO',
    'RS_CACHE_APPROXIMATE_RESULT_ENABLE', 'RS_CACHE_ENABLE',
    'RS_CACHE_MAX_MEMORY_PER_QUERY', 'RS_CACHE_MAX_MEMORY_SIZE',
    'RS_CACHE_MAX_RECORD_PER_QUERY', 'RS_CACHE_TIME_BOUND_MSEC',
    'STREAM_THREAD_COUNT', 'STREAM_WAIT_MS'
);

SELECT COUNT(*) AS removed_table_count
FROM V$TABLES
WHERE NAME IN (
    'SYS_STREAM_STMTS', 'V$HTTP_STATUS', 'V$RS_CACHE_LIST',
    'V$RS_CACHE_STAT', 'V$STREAMS'
);
```

### DDL Concurrency Compatibility

Machbase 8.7.0 uses different DDL concurrency policies by edition.

| Edition | 8.7.0 Behavior | `DDL_LOCK_TIMEOUT` |
|---------|------------|--------------------|
| Standard | DDL on independent objects can run concurrently | Available. Default: `0` (NOWAIT) |
| Cluster | Retains the existing catalog-wide DDL policy | Not available |

In Standard Edition, conflicting DDL on the same or directly related objects returns
`ERR-02031: Resource busy (<object>)` immediately by default. Deployment scripts that assume
older waiting behavior must explicitly adopt an appropriate approach after upgrading.

- Set a bounded wait in the deployment session with `ALTER SESSION SET DDL_LOCK_TIMEOUT = seconds`.
- Apply bounded retries and wait intervals only to `ERR-02031`.
- Recheck object state before retrying. Do not retry `already exists`, privilege, or syntax errors.

For conflict relationships and configuration, see
[DDL Concurrency and Locks](/dbms/reference/sql/syntax/ddl-syntax/#ddl-concurrency).


### Backup File Compatibility

| Backup Version | Restore in 8.7.0 | Notes |
|--------------|:-----------:|------|
| 8.5 backup | O | Use `MOUNT` or `machadmin -r` |
| 8.7.0 backup | O | |
| 8.4 or earlier backup | △ | Version-dependent; testing required |


## Canonical Upgrade Reference

For execution order, supported platforms, and prechecks, see
[Upgrade](../../../installation-deployment-upgrade/upgrade/). This page maintains SQL, server, and
client compatibility facts only.
