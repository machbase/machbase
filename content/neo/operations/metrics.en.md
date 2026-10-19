---
title: Metrics
type: docs
weight: 101
toc: true
---

{{< neo_since ver="8.7.0" />}}

Machbase Neo collects server status and request processing statistics and stores them in
`SYS._NEO_STATZ`. Query the metrics and time range you need with SQL, then visualize the results
by combining TQL's `SQL()` and `CHART()`.

Run the examples in this document while connected as `sys`.
The server creates and manages `_NEO_STATZ` automatically; you do not need to create the table
or insert data yourself.

## Storage Structure and Collection Interval

`_NEO_STATZ` is a regular transaction table with the following three columns, not a TAG table.

| Column | Type | Description |
|:-------|:-----|:------------|
| `NAME` | `VARCHAR(100)` | Metric key |
| `TIME` | `DATETIME` | Start time of the one-minute aggregation interval |
| `VALUE` | `DOUBLE` | Metric value for the interval |

A unique index covers `(NAME, TIME)`.
Values for the current interval update the same row. A new row is stored for the next interval.

- **Collection interval:** Periodically collected items, such as system status, are measured
  every 10 seconds. HTTP request statistics are collected as requests are processed.
- **Storage resolution:** One minute. Even when samples are collected every 10 seconds,
  each sample is not stored as a separate row.
- **Current interval:** The in-progress one-minute interval is also stored, so `VALUE` can change
  for the same `TIME`.
- **Retention:** Eight days. Old data is cleaned up at 15-minute intervals during writes,
  so rows older than eight days can remain until the next cleanup.

### Interpreting Values

Not every `VALUE` is a cumulative total since server startup or a one-minute average.
Interpret each item according to how it is collected.

| Method | Stored value | Examples |
|:-------|:-------------|:---------|
| Gauge | Last value measured in the interval | `runtime:heap_inuse`, `sys:session:count` |
| Counter | Sum of values collected in the interval | `http:count`, `http:send_bytes` |
| Odometer | Difference between the last value and the cumulative counter's baseline | `sys:execute:count`, `sys:pool:wait_count` |
| Histogram | Sample count and percentiles | `http:latency`, `http:latency:p99` |

For example, `http:latency` stores the **number of samples in the interval**, not a latency.
Actual latency values are stored in `http:latency:p50`, `http:latency:p90`, and
`http:latency:p99`. Divide a value in `ns` by `1000000` to convert it to `ms`.

An interval with no requests may have no HTTP metric rows.
**A missing row is not the same as a value of zero.**
Sums, differences, and percentiles for the current interval represent values collected so far,
not the completed interval. Do not interpret a one-minute interval's difference directly as
throughput per second.

## Finding Metric Keys

The keys collected depend on your configuration and the features in use.
First, check which keys are actually stored on the current server.

```sql
SELECT NAME FROM _NEO_STATZ GROUP BY NAME ORDER BY NAME;
```

Use `LIKE` to filter for a specific category.

```sql
SELECT NAME FROM _NEO_STATZ WHERE NAME LIKE 'http:%'
GROUP BY NAME
ORDER BY NAME;
```

You can also check the stored time range and row count for each key.

```sql
SELECT NAME, MIN(TIME) AS FIRST_TIME, MAX(TIME) AS LAST_TIME, COUNT(*) AS POINTS
FROM _NEO_STATZ
GROUP BY NAME
ORDER BY NAME;
```

HTTP keys appear after requests have been processed.
MQTT keys appear when the MQTT broker is in use, and rollup keys appear when there are rollups
eligible for collection. Previously stored keys can remain queryable throughout the retention
period even after the corresponding feature is no longer used.

## Querying with SQL

The following query retrieves Go heap usage over the last hour in chronological order.
Change `SYSDATE - 1h` to `SYSDATE - 30m`, `SYSDATE - 1d`, or another range as needed.

```sql
SELECT TIME, VALUE
FROM _NEO_STATZ
WHERE NAME = 'runtime:heap_inuse'
  AND TIME >= SYSDATE - 1h
ORDER BY TIME;
```

To query only completed intervals, excluding the current one-minute interval, add this condition:

```sql
SELECT TIME, VALUE
FROM _NEO_STATZ
WHERE NAME = 'runtime:heap_inuse'
  AND TIME >= SYSDATE - 1h
  AND TIME < DATE_TRUNC('minute', SYSDATE)
ORDER BY TIME;
```

## Visualizing with TQL

Run the following examples in the web UI's TQL editor.
Pair the `TIME` and value returned by `SQL()` using `list()` to create a point on a time-axis chart.
To plot another metric, change the `NAME` condition, unit conversion, and chart labels.
Sort query results with `ORDER BY TIME`.

### Heap Usage

Convert heap usage from bytes to MiB for display.

```js
SQL(`
    SELECT TIME, VALUE / 1048576.0 AS HEAP_MIB
    FROM _NEO_STATZ
    WHERE NAME = 'runtime:heap_inuse'
      AND TIME >= SYSDATE - 1h
    ORDER BY TIME
`)
MAPVALUE(1, list(value(0), value(1)))
CHART(
    size("800px", "350px"),
    chartOption({
        animation: false,
        xAxis: { type: "time" },
        yAxis: { type: "value", name: "MiB" },
        tooltip: { trigger: "axis" },
        legend: {},
        series: [
            { name: "Go heap", type: "line", showSymbol: false, data: column(1) }
        ]
    })
)
```

### Database Connection Pool

To display different keys on one chart, use `CASE` and `GROUP BY TIME` to combine values
with the same timestamp into a single row.
The following example compares open connections with connections in use.
Here, `MAX()` selects the value for each key at the same `TIME`; it does not calculate
a maximum across different timestamps.

```js
SQL(`
    SELECT TIME,
        MAX(CASE WHEN NAME = 'sys:pool:open' THEN VALUE END) AS OPEN_CONNS,
        MAX(CASE WHEN NAME = 'sys:pool:in_use' THEN VALUE END) AS IN_USE_CONNS
    FROM _NEO_STATZ
    WHERE NAME IN ('sys:pool:open', 'sys:pool:in_use')
      AND TIME >= SYSDATE - 1h
    GROUP BY TIME
    ORDER BY TIME
`)
MAPVALUE(1, list(value(0), value(1)))
MAPVALUE(2, list(value(0), value(2)))
CHART(
    size("800px", "350px"),
    chartOption({
        animation: false,
        xAxis: { type: "time" },
        yAxis: { type: "value", name: "Connections", minInterval: 1 },
        tooltip: { trigger: "axis" },
        legend: {},
        series: [
            { name: "Open", type: "line", showSymbol: false, data: column(1) },
            { name: "In use", type: "line", showSymbol: false, data: column(2) }
        ]
    })
)
```

### HTTP Response Latency

Compare p50, p90, and p99 latency for all HTTP requests in milliseconds.
The percentiles represent the distribution of samples collected in each one-minute interval.
Results may be empty if there have been no requests, so use the server's HTTP API before running
the example.

```js
SQL(`
    SELECT TIME,
        MAX(CASE WHEN NAME = 'http:latency:p50' THEN VALUE END) / 1000000.0 AS P50,
        MAX(CASE WHEN NAME = 'http:latency:p90' THEN VALUE END) / 1000000.0 AS P90,
        MAX(CASE WHEN NAME = 'http:latency:p99' THEN VALUE END) / 1000000.0 AS P99
    FROM _NEO_STATZ
    WHERE NAME IN ('http:latency:p50', 'http:latency:p90', 'http:latency:p99')
      AND TIME >= SYSDATE - 1h
    GROUP BY TIME
    ORDER BY TIME
`)
MAPVALUE(1, list(value(0), value(1)))
MAPVALUE(2, list(value(0), value(2)))
MAPVALUE(3, list(value(0), value(3)))
CHART(
    size("800px", "350px"),
    chartOption({
        animation: false,
        xAxis: { type: "time" },
        yAxis: { type: "value", name: "ms" },
        tooltip: { trigger: "axis" },
        legend: {},
        series: [
            { name: "p50", type: "line", showSymbol: false, data: column(1) },
            { name: "p90", type: "line", showSymbol: false, data: column(2) },
            { name: "p99", type: "line", showSymbol: false, data: column(3) }
        ]
    })
)
```

Change the query's keys to `http:query:latency:p50` and the corresponding p90/p99 keys
to compare only `/db/query` requests.
Extending the query range does not change the stored one-minute resolution.
Also, a simple average of p99 values from multiple intervals is not the p99 for the entire period.

## Main Metrics

The following lists describe the main built-in collection items.
Use the SQL above to check which keys actually exist.
In the tables, "Gauge" means the last measured value, "Counter" means the sum within an interval,
and "Odometer" means the difference in a cumulative counter.

### System and Go Runtime

CPU and memory percentages and TCP connection counts describe the host system.
Go runtime items describe the Machbase Neo process.

| Key | Method | Description / Unit |
|:----|:-------|:-------------------|
| `ps:cpu_percent` | Gauge | Host CPU usage / % |
| `ps:mem_percent` | Gauge | Host memory usage / % |
| `runtime:goroutines` | Gauge | Number of Go goroutines |
| `runtime:heap_inuse` | Gauge | Size of in-use Go heap spans / bytes |
| `runtime:cgo_call` | Odometer | Number of cgo calls |
| `netstat:tcp_established` | Gauge | Number of ESTABLISHED TCP connections |
| `netstat:tcp_fin_wait1` | Gauge | Number of FIN_WAIT1 TCP connections |
| `netstat:tcp_fin_wait2` | Gauge | Number of FIN_WAIT2 TCP connections |
| `netstat:tcp_time_wait` | Gauge | Number of TIME_WAIT TCP connections |
| `netstat:tcp_close_wait` | Gauge | Number of CLOSE_WAIT TCP connections |
| `netstat:tcp_listen` | Gauge | Number of LISTEN TCP sockets |

### Database

| Key | Method | Description / Unit |
|:----|:-------|:-------------------|
| `sys:sysmem` | Gauge | Sum of `USAGE` in `V$SYSMEM` / bytes |
| `sys:session:count` | Gauge | Number of DB sessions that are not closed |
| `sys:append:open` | Odometer | Number of APPEND open operations |
| `sys:append:close` | Odometer | Number of APPEND close operations |
| `sys:append:data:success` | Odometer | Increase in `APPEND_DATA_SUCCESS` |
| `sys:append:data:failure` | Odometer | Increase in `APPEND_DATA_FAILURE` |
| `sys:execute:count` | Odometer | Increase in the `EXECUTE` count in `V$SYSTIME` |
| `sys:execute:time:avg` | Gauge | Average of `V$SESTIME.MAX_MSEC` across sessions / ns |
| `sys:execute:time:max` | Gauge | Maximum of `V$SESTIME.MAX_MSEC` across sessions / ns |

`sys:execute:time:avg` is the average of each session's `MAX_MSEC`,
not the average duration of all individual SQL executions.

### Server Internal Connection Pool

These statistics describe the server's default `database/sql` connection pool.
Distinguish them from `sys:session:count`, which counts DB sessions across the server.

| Key | Method | Description / Unit |
|:----|:-------|:-------------------|
| `sys:pool:max_open` | Gauge | Maximum connection setting; 0 means unlimited |
| `sys:pool:open` | Gauge | Number of open connections |
| `sys:pool:in_use` | Gauge | Number of connections in use |
| `sys:pool:idle` | Gauge | Number of idle connections |
| `sys:pool:wait_count` | Odometer | Number of waits for a connection |
| `sys:pool:wait_duration` | Odometer | Total connection wait time / ns |
| `sys:pool:max_idle_closed` | Odometer | Connections closed due to the maximum idle connection limit |
| `sys:pool:max_idletime_closed` | Odometer | Connections closed due to exceeding the maximum idle time |
| `sys:pool:max_lifetime_closed` | Odometer | Connections closed due to exceeding the maximum lifetime |

### HTTP

Request counts, byte counts, and status code counts are sums within an interval.
The base latency key stores the sample count; the `:p50`, `:p90`, and `:p99` keys store
latencies in nanoseconds.

| Key | Description |
|:----|:------------|
| `http:count` | Total HTTP requests |
| `http:latency` | Sample count for overall HTTP request latency |
| `http:latency:p50`,<br/> `http:latency:p90`,<br/> `http:latency:p99` | Percentiles of overall HTTP request latency / ns |
| `http:write:count` | Number of `/db/write` requests |
| `http:write:latency` | Sample count for `/db/write` request latency |
| `http:write:latency:p50`,<br/> `http:write:latency:p90`,<br/> `http:write:latency:p99` | Percentiles of `/db/write` request latency / ns |
| `http:query:count` | Number of `/db/query` requests |
| `http:query:latency` | Sample count for `/db/query` request latency |
| `http:query:latency:p50`,<br/> `http:query:latency:p90`,<br/> `http:query:latency:p99` | Percentiles of `/db/query` request latency / ns |
| `http:tql:count` | Number of `/db/tql` requests |
| `http:tql:latency` | Sample count for `/db/tql` request latency |
| `http:tql:latency:p50`,<br/> `http:tql:latency:p90`,<br/> `http:tql:latency:p99` | Percentiles of `/db/tql` request latency / ns |
| `http:recv_bytes` | Sum of collected request body sizes / bytes |
| `http:send_bytes` | Sum of collected response body sizes / bytes |
| `http:status_1xx`, `http:status_2xx`,<br/> `http:status_3xx`, `http:status_4xx`,<br/> `http:status_5xx` | Response count by status code class |

### MQTT

All items below store the last measured broker statistic.
In particular, cumulative statistics such as received/sent bytes and messages store
**the cumulative values provided by the broker**, unlike HTTP's per-interval sums.

| Key | Description / Unit |
|:----|:-------------------|
| `mqtt:recv_bytes` | Cumulative bytes received / bytes |
| `mqtt:send_bytes` | Cumulative bytes sent / bytes |
| `mqtt:recv_msgs` | Cumulative PUBLISH messages received |
| `mqtt:send_msgs` | Cumulative PUBLISH messages sent |
| `mqtt:drop_msgs` | Cumulative dropped messages |
| `mqtt:recv_pkts` | Cumulative packets received |
| `mqtt:send_pkts` | Cumulative packets sent |
| `mqtt:retained` | Number of retained messages |
| `mqtt:subscriptions` | Number of subscriptions |
| `mqtt:clients` | Clients connected or with retained sessions |
| `mqtt:clients_connected` | Number of connected clients |
| `mqtt:clients_disconnected` | Disconnected clients with retained sessions |
| `mqtt:inflight` | Number of in-flight messages |
| `mqtt:inflight_dropped` | Cumulative messages dropped while in flight |

### TQL Cache

These items also store the last measured value.
`items` is the current number of items; the others are cumulative counts tracked by the cache.

| Key | Description |
|:----|:------------|
| `tql:cache:items` | Current number of cache items |
| `tql:cache:evictions` | Cumulative number of items evicted from the cache |
| `tql:cache:insertions` | Cumulative number of cache insertions |
| `tql:cache:hits` | Cumulative cache hits |
| `tql:cache:misses` | Cumulative cache misses |

### Rollups

`<rollup_table>` is replaced by the rollup table name converted to lowercase.
All items store the last measured value.

| Key | Description / Unit |
|:----|:-------------------|
| `sys:rollup:<rollup_table>:gap` | Sum of RID differences between the source table and the rollup's processing position |
| `sys:rollup:<rollup_table>:last_elapse` | Maximum `LAST_ELAPSED_MSEC` for the rollup, converted to ns |
| `sys:rollup_global:gap` | Sum of gaps across all rollups included in collection |
| `sys:rollup_global:last_elapse` | Maximum execution time among rollups that ran during the preceding collection interval / ns |

`sys:rollup_global:last_elapse` is 0 if no rollup ran during the preceding collection interval.
