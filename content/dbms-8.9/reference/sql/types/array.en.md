---
type: docs
title: 'Numeric ARRAY Types'
weight: 30
toc: true
---

Machbase DBMS 8.7.0 supports fixed-length, one-dimensional ARRAYs containing a fixed number
of values of the same numeric type. Use them to store multiple numeric values in one row,
such as sensor coordinates or per-axis measurements, and query individual elements.

For sparse input and selected-column Append APIs, see
[Sparse ARRAY and Selected-column Append APIs](../../../../development-tools-integration/data-input-load-export/array-append/).


## Supported Types and Declaration Limits

Append [cardinality] to the numeric element type when declaring a column. Cardinality is the
fixed number of elements declared for the column, not the number of non-NULL elements in each row.
A missing entire array (whole-array NULL) differs from a missing value at a particular position
(element NULL).

| Element Type | DDL Example | Description |
|---|---|---|
| `INT16` | `INT16[4]` | Signed 16-bit integer |
| `UINT16` | `UINT16[4]` | Unsigned 16-bit integer |
| `INT32` | `INT32[4]` | Signed 32-bit integer |
| `UINT32` | `UINT32[4]` | Unsigned 32-bit integer |
| `INT64` | `INT64[4]` | Signed 64-bit integer |
| `UINT64` | `UINT64[4]` | Unsigned 64-bit integer |
| `FLOAT` | `FLOAT[4]` | Single-precision floating-point |
| `DOUBLE` | `DOUBLE[4]` | Double-precision floating-point |
| `DECIMAL(p,s)` | `DECIMAL(12,4)[4]` | Fixed-point number |

- Cardinality ranges from 1 through 1024.
- DECIMAL precision ranges from 1 through 65.
- DECIMAL scale ranges from 0 through 30 and cannot exceed precision.

The following aliases map to their canonical element types.

| Alias | Canonical Type |
|---|---|
| `SHORT` | `INT16` |
| `USHORT` | `UINT16` |
| `INT`, `INTEGER` | `INT32` |
| `UINTEGER` | `UINT32` |
| `LONG` | `INT64` |
| `ULONG` | `UINT64` |
| `NUMERIC`, `DEC`, `FIXED`, `NUMBER` | `DECIMAL` |

## Creating Tables and Adding Columns

This example stores four channel values, three counters, and two fixed-point values.

```sql
CREATE LOG TABLE SENSOR_ARRAY
(
    ID       INTEGER,
    CHANNELS DOUBLE[4],
    COUNTERS UINT64[3],
    AMOUNTS  DECIMAL(12,4)[2]
);
```

For tables that already support ADD COLUMN, add columns using the same ARRAY declaration
and remove them with the existing DROP COLUMN syntax.

```sql
ALTER TABLE SENSOR_ARRAY
    ADD COLUMN (STATUS_VALUES INT32[3]);

ALTER TABLE SENSOR_ARRAY
    ADD COLUMN (LIMITS DECIMAL(12,4)[2] DEFAULT [0.0000, NULL]);

ALTER TABLE SENSOR_ARRAY
    DROP COLUMN (STATUS_VALUES);

ALTER TABLE SENSOR_ARRAY
    DROP COLUMN (LIMITS);
```

Omitting scale, as in DECIMAL(12)[2], means DECIMAL(12,0)[2].

For TAG METADATA ARRAYs, use METADATA ADD COLUMN and METADATA DROP COLUMN.

```sql
ALTER TABLE SENSOR_TAG METADATA
    ADD COLUMN (LIMITS DECIMAL(12,4)[2] DEFAULT [0.0000, NULL]);

ALTER TABLE SENSOR_TAG METADATA
    DROP COLUMN (LIMITS);
```

ARRAY is supported in ordinary data columns in the following locations.

- LOG tables
- Ordinary TAG DATA columns
- Ordinary TAG METADATA columns
- VOLATILE tables
- LOOKUP tables
- Standard Edition TRANSACTION tables

Adding ARRAY does not expand a table's existing DML scope. LOG UPDATE remains unsupported,
and TAG UPDATE is limited to the existing allowed DATA or
METADATA paths.

### ADD COLUMN Support

| Edition | Table or Column Area | ARRAY ADD/DROP |
|---|---|:---:|
| Standard | LOG | O |
| Standard | VOLATILE | O |
| Standard | LOOKUP | O |
| Standard | TRANSACTION | O |
| Standard | TAG METADATA | O |
| Standard | Ordinary TAG DATA columns | X |
| Cluster | LOG | O |
| Cluster | Other tables or TAG METADATA | X |

Ordinary TAG DATA ARRAY columns can be declared in CREATE TABLE, but cannot be added
with ALTER.

<a id="default와-기존-row"></a>

### DEFAULT and Existing Rows

- Without DEFAULT, the new ARRAY column is whole-array NULL for rows existing before ALTER.
- LOG, LOOKUP, TRANSACTION, and TAG METADATA apply an explicit ARRAY DEFAULT to
  existing rows.
- Like scalar ADD COLUMN, VOLATILE does not rewrite existing rows with DEFAULT, so the
  new ARRAY column is whole-array NULL.
- Cluster LOG applies an explicit ARRAY DEFAULT to existing rows.
- The DEFAULT constructor must contain exactly the declared number of elements.

If a new tag is registered automatically by TAG DATA INSERT or Append after ALTER, the new
metadata row does not receive the ADD COLUMN DEFAULT. Added ARRAY metadata columns are
whole-array NULL. This DEFAULT applies only to metadata rows that existed before ALTER.

ARRAY cannot be used for the following roles.

- PRIMARY KEY, UNIQUE, or ordinary index keys
- `AUTO_INCREMENT`, `SEQUENCE`
- TAG NAME, BASETIME, BASE DISTANCE, or SUMMARIZED columns

TAG METADATA ARRAY columns do not receive automatic indexes, and explicit indexes are
not supported.

The following declarations are not supported.

```sql
INT32[]
INT32[0]
INT32[1025]
VARCHAR[4]
INT32[2][3]
DECIMAL[4](12,4)
```

## Inserting ARRAY Values

Both ARRAY[...] and shorthand [...] are supported.

```sql
INSERT INTO SENSOR_ARRAY VALUES
    (1,
     ARRAY[1.5, NULL, 3.5, 4.5],
     [1, NULL, 3],
     [12.3400, NULL]);

INSERT INTO SENSOR_ARRAY VALUES
    (2,
     [10.0, 20.0, 30.0, 40.0],
     [4, 5, 6],
     [1.2500, 2.5000]);

INSERT INTO SENSOR_ARRAY VALUES (3, NULL, NULL, NULL);
```

The constructor element count must exactly match the target column's cardinality. A mismatch
fails the statement rather than padding or truncating. Empty [] and ARRAY[] cannot be stored
as zero-cardinality values.

Each element follows the target numeric type's conversion, sign, range, and DECIMAL
precision/scale rules. If any element cannot be converted, the entire statement fails;
no partial ARRAY is stored.

### Numeric Ranges

Integer types cannot store internal NULL sentinel values as actual data.

| Type | Storable Range |
|---|---|
| `INT16` | `-32767..32767` |
| `UINT16` | `0..65534` |
| `INT32` | `-2147483647..2147483647` |
| `UINT32` | `0..4294967294` |
| `INT64` | `-9223372036854775807..9223372036854775807` |
| `UINT64` | `0..18446744073709551614` |

The reserved maximum finite NULL sentinels of FLOAT and DOUBLE also cannot be actual elements.
Infinity handling for larger inputs follows the corresponding scalar type.

### Type Inference Without a Target

Without a target column, as in SELECT [1,2,3], a common type is inferred from all elements.

- If all non-NULL elements have one type, preserve that type.
- Promote signed/unsigned integers to the smallest integer type that holds all values.
- Signed integers mixed with UINT64 use DECIMAL(20,0).
- DECIMAL inputs combine required integer digits and scale.
- FLOAT alone remains FLOAT; mixed with other numeric types, it promotes to DOUBLE.
- Empty arrays, all-NULL arrays, nonnumeric elements, and nested arrays cause inference errors.

With a target column, as in INSERT, UPDATE, or a prepared parameter, validate each element
against the target's element type, cardinality, and DECIMAL metadata.

### Whole-array NULL and Element NULL

A NULL ARRAY and an ARRAY containing NULL elements are distinct values.

```sql
-- The entire ARRAY is NULL.
INSERT INTO SENSOR_ARRAY (ID, CHANNELS) VALUES (10, NULL);

-- The ARRAY exists and all four elements are NULL.
INSERT INTO SENSOR_ARRAY (ID, CHANNELS)
VALUES (11, [NULL, NULL, NULL, NULL]);
```

NOT NULL constrains only the entire ARRAY value. An ARRAY whose elements are all NULL
can therefore be inserted into a NOT NULL column.

## Querying Elements

Element positions start at 0. For cardinality 4, valid positions are 0 through 3.

```sql
SELECT CHANNELS,
       CHANNELS[0] AS FIRST_CHANNEL,
       CHANNELS[3] AS LAST_CHANNEL,
       CHANNELS[4] AS OUT_OF_RANGE
  FROM SENSOR_ARRAY;
```

The following cases return SQL NULL rather than an error.

- Negative index or index at least equal to cardinality
- SQL NULL index expression
- Whole-array NULL
- NULL element at the position

{{< callout type="warning" >}}
An element [position] can follow only a simple, unquoted column name.
A[0] is supported;
T.A[0] and "A"[0] are not supported.
{{< /callout >}}

## ARRAY_LENGTH

ARRAY_LENGTH() returns the declared cardinality unless the entire array is NULL.

```sql
SELECT ID, ARRAY_LENGTH(CHANNELS)
  FROM SENSOR_ARRAY;
```

It returns cardinality even if all elements are NULL. A whole-array NULL returns NULL.
ARRAY_LENGTH(NULL) without type information causes an error because the argument type cannot be determined.

## Whole-array CAST

Convert every element of a numeric ARRAY to another type with the same cardinality using
CAST(array_expression AS TYPE[N]).

```sql
SELECT CAST(CHANNELS AS INT32[4])
  FROM SENSOR_ARRAY;

SELECT CAST(AMOUNTS AS DECIMAL(10,2)[2])
  FROM SENSOR_ARRAY;
```

- Input must be a numeric ARRAY or SQL NULL.
- Targets can use the numeric element types and aliases in this document.
- Input and target cardinalities must match exactly.
- Whole-array NULL and each element NULL are preserved.
- Each non-NULL element follows the corresponding scalar CAST numeric conversion rules.
- DECIMAL[N] means DECIMAL(10,0)[N]; DECIMAL(p)[N] means DECIMAL(p,0)[N].

- If any element violates range or conversion rules, CAST and the containing statement fail.

In prepared statements, the CAST target determines parameter and result element types,
cardinality, and DECIMAL precision/scale. Rebind the same statement with ARRAY values,
whole-array NULL, or sparse ARRAYs specifying selected positions.

```sql
SELECT CAST(? AS INT32[3]);
SELECT CAST(? AS DECIMAL(12,4)[3]);
```

To combine ARRAY results in CASE and UNION ALL, element type, cardinality, and DECIMAL
precision/scale must all match. Otherwise, explicitly CAST to the same ARRAY type
before combining.

The following conversions are unsupported.

- Scalar expansion to ARRAY
- ARRAY reduction to scalar
- Padding/truncation between different cardinalities
- String, date, IP, BINARY, or JSON ARRAY targets

For full syntax, numeric conversion, and error rules, see
[CAST](../../functions/functions-full/#cast).

## Comparisons and Expressions

Whole ARRAYs support `=`, `<>`, `IS NULL`, and `IS NOT NULL`. Element NULLs in corresponding positions
match in whole-array equality comparisons. Whole-array NULL follows ordinary SQL
NULL rules.

```sql
SELECT ID
  FROM SENSOR_ARRAY
 WHERE CHANNELS = [1.5, NULL, 3.5, 4.5]
    OR CHANNELS[1] IS NULL;
```

Element expressions can appear in ordinary expressions and predicates of the corresponding
numeric type. Whole ARRAYs are unsupported in the following locations.

- `DISTINCT`
- `GROUP BY`
- `ORDER BY`
- DISTINCT arguments to aggregate functions

## VIEW, INSERT SELECT, CASE, and Upsert

VIEW and INSERT ... SELECT preserve element type, cardinality, and DECIMAL precision/scale.
When inserting into a different numeric ARRAY type, each element converts to the target type;
if any conversion fails, the entire statement fails.

CASE results in INSERT and UPDATE also follow the target ARRAY contract.

```sql
UPDATE SENSOR_LOOKUP
   SET AMOUNTS = CASE WHEN ID = 1
                     THEN [12345678.1234, NULL]
                     ELSE AMOUNTS
                 END
 WHERE ID = 1;
```

For LOOKUP/VOLATILE duplicate-key upserts, direct ARRAY values, constant CASE expressions,
and prepared whole-array binds use the same conversion rules. Whether an upsert right-hand
expression can reference existing row columns follows the table's existing policy.

## Metadata and Display Format

DESC and SQL export display canonical declarations.

```sql
DESC SENSOR_ARRAY;
```

System catalogs preserve ARRAY type code, cardinality, precision, and scale as separate fields.
SQLColumns() in SQLCLI or ODBC returns the following.

- `DATA_TYPE`: `SQL_MACHBASE_ARRAY`
- TYPE_NAME: Canonical declaration such as INT32[3] or DECIMAL(12,4)[2]
- `COLUMN_SIZE`: cardinality
- DECIMAL_DIGITS: DECIMAL element scale

Paths requiring textual results, such as machsql, generic ODBC text queries, and Go database/sql,
use [value,null,value]. Lowercase null is an element NULL; SQL NULL for the column result
is a whole-array NULL.

## Reading and Writing ARRAYs with SDKs

The following examples share this table and data.

```sql
CREATE LOG TABLE SDK_ARRAY_SAMPLE
(
    ID INTEGER,
    A_I32 INT32[3],
    A_U64 UINT64[3],
    A_DEC DECIMAL(12,4)[3]
);

INSERT INTO SDK_ARRAY_SAMPLE VALUES
    (1,
     [1,NULL,-3],
     [1,NULL,18446744073709551614],
     [1.2500,NULL,-3.7500]);
INSERT INTO SDK_ARRAY_SAMPLE (ID) VALUES (2);
```

SDKs represent whole-array NULL with their NULL value and element NULL with NULL inside the
collection. Use SDK types that preserve UINT64 and DECIMAL precision.

### C SQLCLI

Use SQL_C_MACHBASE_ARRAY and SQL_MACHBASE_ARRAY_DESC for typed fetch.

```c
SQLINTEGER values[3] = {0};
SQLLEN elements[3] = {0};
SQLLEN outer = 0;
SQL_MACHBASE_ARRAY_DESC array = {0};

array.struct_size = sizeof(array);
array.element_c_type = SQL_C_SLONG;
array.capacity = 3;
array.values = values;
array.element_indicators = elements;

SQLExecDirect(stmt,
    (SQLCHAR*)"SELECT A_I32 FROM SDK_ARRAY_SAMPLE WHERE ID=1", SQL_NTS);
SQLBindCol(stmt, 1, SQL_C_MACHBASE_ARRAY, &array, sizeof(array), &outer);
SQLFetch(stmt);
/* outer != SQL_NULL_DATA, array.count == 3,
 * values[0] == 1, elements[1] == SQL_NULL_DATA, values[2] == -3 */
```

For whole-array NULL, outer == SQL_NULL_DATA and array.count == 0. Provide element_indicators
to distinguish element NULLs. To fetch DECIMAL as strings, set element_c_type = SQL_C_CHAR
and value_stride to the spacing between element buffers.

For prepared INSERT, set capacity, count, and ColumnSize to the target cardinality.

```c
array.count = 3;
SQLPrepare(stmt,
    (SQLCHAR*)"INSERT INTO SDK_ARRAY_SAMPLE(ID,A_I32) VALUES(3,?)", SQL_NTS);
SQLBindParameter(stmt, 1, SQL_PARAM_INPUT,
    SQL_C_MACHBASE_ARRAY, SQL_MACHBASE_ARRAY, 3, 0,
    &array, sizeof(array), &outer);
SQLExecute(stmt);
```

Set outer = SQL_NULL_DATA for whole-array NULL input. ARRAY parameter-set execution is currently
unsupported and returns HYC00. Legacy SQLAppendBatch also lacks an ARRAY type code and does
not support ARRAY, but does not guarantee the same SQLSTATE.

### C++

C++ uses the SQLCLI descriptor ABI directly. Keep vector size fixed so its address remains stable
from bind until fetch completes.

```cpp
std::vector<SQLINTEGER> values(3);
std::vector<SQLLEN> indicators(3);
SQLLEN outer = 0;
SQL_MACHBASE_ARRAY_DESC array{};
array.struct_size = sizeof(array);
array.element_c_type = SQL_C_SLONG;
array.capacity = values.size();
array.values = values.data();
array.element_indicators = indicators.data();

SQLBindCol(stmt, 1, SQL_C_MACHBASE_ARRAY,
           &array, sizeof(array), &outer);
```

In the application model, represent whole-array NULL with the outer optional in
`std::optional<std::vector<std::optional<T>>>` and element NULL with
an inner optional.

### Machbase ODBC and Generic ODBC

ODBC C programs using Machbase headers use the same ARRAY descriptor as C SQLCLI.
Generic tools that do not recognize the custom type can query canonical text or project
individual elements.

```sql
SELECT ID, A_I32, A_I32[1], A_I32[2], A_I32[3]
  FROM SDK_ARRAY_SAMPLE
 ORDER BY ID;
```

### JDBC

JDBC returns java.sql.Array. UINT64 uses BigInteger and DECIMAL uses
BigDecimal to preserve precision.

```java
try (Connection con = DriverManager.getConnection(
         "jdbc:machbase://127.0.0.1:5656/machbasedb", "SYS", "MANAGER");
     Statement st = con.createStatement();
     ResultSet rs = st.executeQuery(
         "SELECT A_I32 FROM SDK_ARRAY_SAMPLE ORDER BY ID")) {
    rs.next();
    java.sql.Array sqlArray = rs.getArray(1);
    Object[] values = (Object[])sqlArray.getArray();
    // [Integer(1), null, Integer(-3)]
    rs.next();
    assert rs.getArray(1) == null && rs.wasNull();
}
```

JDBC metadata reports Types.ARRAY, precision as cardinality, and DECIMAL scale as the element
scale. Pass values created with Connection.createArrayOf() to PreparedStatement.setArray().


### Python

Python returns ARRAY as list, element NULL as None inside the list, and whole-array NULL
as None for the column. UINT64 uses arbitrary-precision int; DECIMAL uses Decimal.

```python
from decimal import Decimal
from machbaseAPI import connect

conn = connect(host="127.0.0.1", port=5656,
               user="SYS", password="MANAGER")
try:
    rows = conn.cursor(dictionary=True).execute(
        "SELECT A_I32,A_U64,A_DEC FROM SDK_ARRAY_SAMPLE ORDER BY ID"
    ).fetchall()
    assert rows[0]["A_I32"] == [1, None, -3]
    assert rows[0]["A_U64"][2] == 18446744073709551614
    assert rows[0]["A_DEC"][0] == Decimal("1.2500")
    assert rows[1]["A_I32"] is None
finally:
    conn.close()
```

Prepared execute() and executemany() encode list or tuple values as ARRAY.
Check ARRAY type code, cardinality, and DECIMAL element metadata in
cursor.column_metadata.

### Node.js

Node.js returns ARRAY as JavaScript Array. INT64 and UINT64 use bigint;
DECIMAL uses strings to preserve precision.

```javascript
const { createConnection } = require('@machbase/ts-client');
const conn = createConnection({
  host: '127.0.0.1', port: 5656, user: 'SYS', password: 'MANAGER',
});
await conn.connect();
try {
  const [rows] = await conn.query(
    'SELECT A_I32,A_U64,A_DEC FROM SDK_ARRAY_SAMPLE ORDER BY ID',
  );
  console.log(rows[0].A_I32); // [1, null, -3]
  console.log(rows[0].A_U64); // [1n, null, 18446744073709551614n]
  console.log(rows[1].A_I32); // null: whole NULL
} finally {
  await conn.end();
}
```

Convert bigint to strings before JSON.stringify(), and do not coerce DECIMAL strings to Number.
A prepared statement's getColumns() exposes ARRAY cardinality and element
precision/scale metadata.

### .NET full/legacy provider

MachConnector40 full/legacy providers return ARRAY as object[]. Element NULL is null inside
the array; use IsDBNull() to distinguish whole-array NULL.

```csharp
using Mach.Data.MachClient;
using var conn = new MachConnection(
    "SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD=MANAGER");
conn.Open();
using var cmd = new MachCommand(
    "SELECT A_I32 FROM SDK_ARRAY_SAMPLE ORDER BY ID", conn);
using var reader = cmd.ExecuteReader();
reader.Read();
var values = (object[])reader.GetValue(0);
Console.WriteLine((int)values[0]);
Console.WriteLine(values[1] is null);
reader.Read();
Console.WriteLine(reader.IsDBNull(0));
```

Elements use short, ushort, int, uint, long, ulong, float, double, or
 decimal. Values outside CLR decimal range are returned as invariant strings.
GetSchemaTable() provides provider type, cardinality, element scale, and object[] field type.


### Go neo-client

This section covers the neo-client SDK connecting directly to Machbase DBMS, not a Machbase Neo
server. The 0-based ARRAY API is in the v2 module
source after [`neo-client` PR #17](https://github.com/machbase/neo-client/pull/17).

Until a public v2 release is specified, use that source checkout with an explicit local module
connection such as go.work or replace. Do not assume public v1 releases contain the feature.

```go
import (
    "context"
    "database/sql"
    "fmt"

    client "github.com/machbase/neo-client/v2"
    "github.com/machbase/neo-client/v2/api"
)

db, err := sql.Open(client.DefaultDriverName, dsn)
if err != nil { return err }
defer db.Close()

dense, err := api.NewArray(api.SqlTypeInt32,
    int32(10), nil, int32(30))
if err != nil { return err }
if _, err = db.ExecContext(context.Background(),
    "INSERT INTO SDK_ARRAY_SAMPLE(ID,A_I32) VALUES(3,?)", dense); err != nil {
    return err
}

rows, err := db.QueryContext(context.Background(),
    "SELECT A_I32 FROM SDK_ARRAY_SAMPLE WHERE ID=3")
if err != nil { return err }
defer rows.Close()
for rows.Next() {
    var raw sql.NullString
    if err := rows.Scan(&raw); err != nil { return err }
    fmt.Println(raw.String) // [10,null,30]
}
return rows.Err()
```

database/sql returns canonical strings. Use sql.NullString to check whole-array NULL,
then parse valid values with array.Scan(raw.String), or whole-array NULL with
array.Scan(nil). To preserve original narrow integer and FLOAT types, create the receiver
from element metadata first. Set DECIMAL precision/scale with
NewSparseArrayWithMeta().

ColumnTypes().DatabaseTypeName() provides the ARRAY type name; DecimalSize() provides DECIMAL
element precision/scale. Length() currently reports encoded payload byte length, not cardinality,
and must not be used as cardinality. Standard database/sql metadata does not directly
provide cardinality.

## Command-line Tools and Data Movement

### machsql

machsql prints canonical ARRAY strings.

```sql
SELECT ID, CHANNELS, ARRAY_LENGTH(CHANNELS), CHANNELS[1]
  FROM SENSOR_ARRAY
 ORDER BY ID;
```

Save the SQL to a file and run it as follows.

```bash
machsql -s 127.0.0.1 -P 5656 -u SYS -p MANAGER -f array_query.sql
```

### machloader

machloader text input/output uses canonical [value,null,value] format. Because delimiters
or quotes may occur within an ARRAY, enclose ARRAY fields
in CSV.

```csv
1,"[1.5,null,3.5,4.5]"
```

Verify by round trip that whole-array NULL and all-element-NULL ARRAY remain distinct.
CSV automatic table creation does not infer ARRAY, so create the table explicitly
before importing.

### Backup, Restore, and Mount

Backup and restore preserve element type, cardinality, DECIMAL precision/scale, and NULL
information. Mounted queries provide the same results and metadata. Use Machbase DBMS 8.7.0
for backup, restore, and mount operations involving ARRAY data.

## Versions and Errors

- ARRAY is supported in Machbase DBMS 8.7.0.
- SQL ARRAY element positions and Machbase-specific SDK positions are 0-based. Decrement
  positions in legacy 1-based SQL and SDK calls by one.
- Pair a Machbase DBMS 8.7.0 server with an SDK build containing ARRAY support.
- Unsupported servers or SDKs return errors instead of automatically converting ARRAYs to
  other types.
- Cardinality, position, or element conversion errors fail the entire statement; no partial ARRAY
  is stored.
- Applications must treat whole-array NULL and all-element-NULL ARRAY as distinct values.
- This document covers Machbase DBMS SQL and SDK features. Machbase Neo, HTTP, TQL, and ILP
  are outside its scope.
