---
type: docs
title: '11.5.5 Append API'
weight: 50
toc: true
aliases:
  - /dbms/reference/sdk-api/jdbc/append-api/
---

The Machbase Append API ingests many rows in sequence. JDBC exposes it through
`MachStatement` extension methods. This page focuses on LOG ingestion; check the
[SDK Support Matrix](../../sdk-support-scope/#append-table-type-matrix) for other table types.

## API

| Method | Description |
|--------|------|
| `executeAppendOpen(tableName, errorCheckCount)` | Starts an Append session and returns column metadata. |
| `executeAppendOpen(tableName, inputColumns, errorCheckCount)` | Starts an Append session targeting selected columns or ARRAY elements in Machbase DBMS 8.7.0. |
| `executeAppendData(metadata, data)` | Sends one row. |
| `executeAppendDataByTime(metadata, time, data)` | Sends one row with a timestamp in nanoseconds. |
| `executeAppendFlush()` | Synchronizes pending responses. |
| `executeAppendClose()` | Closes the Append session. |
| `executeSetAppendErrorCallback(callback)` | Registers a row-error callback. |
| `getAppendSuccessCount()` | Returns the number of successful rows. |
| `getAppendFailureCount()` | Returns the number of failed rows. |

The public `executeAppendData()` returns `1` on success and throws `SQLException` for an
invalid internal result. Also check final success/failure counts and callback results.

## Ingestion Example

```sql
CREATE LOG TABLE sensor_data (
    time DATETIME,
    name VARCHAR(40),
    value DOUBLE
);
```

```java
import com.machbase.jdbc.MachStatement;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.util.ArrayList;

try (MachStatement statement =
         (MachStatement) connection.createStatement()) {
    ResultSet appendResult =
        statement.executeAppendOpen("sensor_data", 100);
    ResultSetMetaData metadata = appendResult.getMetaData();

    statement.executeSetAppendErrorCallback(
        (errorNumber, errorMessage, rowMessage) ->
            System.err.printf(
                "Append error [%05d]: %s%n%s%n",
                errorNumber, errorMessage, rowMessage));

    long baseTime = System.currentTimeMillis() * 1_000_000L;

    for (int index = 0; index < 10_000; index++) {
        ArrayList<Object> row = new ArrayList<>();
        row.add(baseTime + index);
        row.add("sensor-" + (index % 10));
        row.add(20.0 + index * 0.001);

        int result = statement.executeAppendData(metadata, row);
        if (result != 1 && result != 2) {
            throw new SQLException(
                "Append failed at row " + index);
        }
    }

    statement.executeAppendFlush();
    statement.executeAppendClose();
    appendResult.close();

    System.out.printf("success=%d failure=%d%n",
        statement.getAppendSuccessCount(),
        statement.getAppendFailureCount());
}
```

<a id="array와-선택-컬럼"></a>

## ARRAY and Selected Columns

Column selection is not required for sparse ARRAY ingestion. Open with the standard
`executeAppendOpen(tableName, errorCheckCount)` and pass `MachSparseArray` as the row ARRAY
value according to the returned metadata.

```java
ResultSet opened = statement.executeAppendOpen("ARRAY_APPEND_FULL_EXAMPLE", 0);
```

Start with the [standard Open example](../../data-input-load-export/array-append/#jdbc-full-open),
which covers connection, ingestion, Close, and queries. Pass `ID` and the ARRAY column in
declaration order. Do not add the automatic `_arrival_time` to the row.

In Machbase DBMS 8.7.0, an `executeAppendOpen()` overload accepts column names or
`ARRAY_COLUMN[position]` targets.

```java
ResultSet appendResult = statement.executeAppendOpen(
    "sensor_array",
    new String[] {"ID", "CHANNELS[0]", "CHANNELS[3]"},
    0);
```

To populate different ARRAY positions for each row, create a `MachSparseArray` with
`MachConnection.createSparseArrayOf()`. Map keys are 0-based. An empty map represents an
ARRAY with all NULL elements; Java `null` represents a NULL array.

```java
Map<Integer, Object> entries = new HashMap<Integer, Object>();
entries.put(Integer.valueOf(1), Integer.valueOf(200));
entries.put(Integer.valueOf(3), Integer.valueOf(400));

MachSparseArray sparse = connection.createSparseArrayOf(
    "INT32", 4, entries);
```

Use `java.sql.Array`, `Connection.createArrayOf()`, and `PreparedStatement.setArray()` for
dense ARRAY retrieval and prepared input. See
[Sparse ARRAY and Selected-Column Append API](../../data-input-load-export/array-append/)
for complete examples and target conflict rules.

SQL ARRAY element targets and `MachSparseArray` positions are 0-based. Standard JDBC
parameter positions and the slice index in `java.sql.Array.getArray(index, count)` remain
1-based. Do not mix these conventions.

## DATETIME

Pass Append DATETIME values as `long` epoch nanoseconds.

```java
long epochNanoseconds =
    System.currentTimeMillis() * 1_000_000L;
```

Use `executeAppendDataByTime()` for table ingestion paths that accept a separate timestamp.
Match input column order and Java types to the ResultSetMetaData returned by `executeAppendOpen()`.

## Flush and Close

1. Start a session with `executeAppendOpen()`.
2. Call `executeAppendData()` repeatedly.
3. Call `executeAppendFlush()` for an intermediate check if needed.
4. Call `executeAppendClose()` after sending all input.
5. Check success/failure counts and callback results.

Use try-with-resources and `finally` to close the Append session and Statement even on
exceptions. Save or log failed rows in the callback. Use business keys to prevent duplicate
ingestion from unconditional retries.

## Size and Scope

Ordered append shares the protocol packet limit. Keep each fully encoded row below 64KiB.
For large values such as BLOB/CLOB, check both row size and client memory usage.

Append batches on TRANSACTION tables are applied independently of SQL transactions.
Use [JDBC Transactions](../transaction-pooling/) for multiple DML operations that require rollback.
