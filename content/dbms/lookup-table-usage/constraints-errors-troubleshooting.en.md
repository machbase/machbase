---
type: docs
title: '9.8 Constraints, Errors, and Troubleshooting'
weight: 80
toc: true
---
This section covers LOOKUP limitations, possible errors, and troubleshooting.


<a id="limitations-lookup-summary"></a>

## Limitation Summary

| Item | Limitation | Typical error |
|---|---|---|
| PRIMARY KEY | Required; only one column | `ERR-02322`, `ERR-02171` |
| PRIMARY KEY column | Cannot be a `SET` target | `ERR-02176` |
| Column types | `TEXT`, `CLOB`, `BLOB`, and `BINARY` unsupported | `ERR-02173` |
| JSON columns | Ordinary columns supported; PRIMARY KEY unsupported | — |
| Memory | Shares one limit with VOLATILE | `ERR-01344` |
| UPDATE | `WHERE` required; does not execute if omitted | — |

<a id="error-lookup-primary-key"></a>

## PRIMARY KEY Errors

LOOKUP cannot be created without a PRIMARY KEY or with more than one. Each statement below fails.

```sql
-- Expected failure: no PRIMARY KEY. (ERR-02322)
CREATE LOOKUP TABLE ch9_err_nopk (code VARCHAR(16), label VARCHAR(64));

-- Expected failure: two PRIMARY KEY columns. (ERR-02171)
CREATE LOOKUP TABLE ch9_err_twopk (
    code VARCHAR(16) PRIMARY KEY,
    name VARCHAR(32) PRIMARY KEY
);
```

Neither statement creates a table, so no cleanup is needed. If a composite key is required, encode
it in one column using a delimiter and follow [PRIMARY KEY Policy](../primary-key-policy/).

PRIMARY KEY column values cannot be updated.

```sql
CREATE LOOKUP TABLE ch9_err_pk (code VARCHAR(16) PRIMARY KEY, label VARCHAR(64));
INSERT INTO ch9_err_pk VALUES ('KR', '대한민국');

-- Expected failure: PRIMARY KEY cannot be a SET target. (ERR-02176)
UPDATE ch9_err_pk SET code = 'KO' WHERE code = 'KR';
```

To change a key, delete the existing row and insert it with the new key.

<a id="error-lookup-column-type"></a>

## Unsupported Column Types

LOOKUP columns cannot use `TEXT`, `CLOB`, `BLOB`, or `BINARY`. Declare long strings as `VARCHAR`;
store raw content separately in LOG when needed.

```sql
-- Expected failure: unsupported column type. (ERR-02173)
ALTER TABLE ch9_err_pk ADD COLUMN (memo TEXT);
```

JSON is supported for ordinary columns. For scope, see [JSON Columns and Queries](../json-column-query/).

```sql
DROP TABLE ch9_err_pk;
```

<a id="error-lookup-memory-limit"></a>

## Memory Limit

LOOKUP persists data on disk but executes queries in memory. Startup loads all rows and indexes into
memory. Exceeding the limit causes `ERR-01344`.

This limit is **shared with VOLATILE tables**. Although the setting name begins with `VOLATILE_`,
LOOKUP is included. Assess the combined usage when using both types.

```sql
SELECT NAME, VALUE FROM V$PROPERTY
 WHERE NAME = 'VOLATILE_TABLESPACE_MEMORY_MAX_SIZE';

SELECT * FROM V$STORAGE_DC_VOLATILE_TABLE;
```

Near the limit, reduce retained data, remove unused secondary indexes, or consider another table
type for large reference datasets using the criteria in
[Indexes and Performance](../index-performance/).

<a id="too-many-lookup-predicate-update-delete-row"></a>

## Scope of Multirow Changes

UPDATE/DELETE with general predicates can affect multiple rows. Check the target count using the
same predicate first and follow
[UPDATE/DELETE with General Predicates](../predicate-update-delete/).

<a id="error-lookup-json-path-primary-key"></a>

## JSON PRIMARY KEY Errors

JSON can be an ordinary column but cannot be declared as a PRIMARY KEY. Store the identifier in a
separate scalar column and follow the type/path rules in
[JSON Columns and Queries](../json-column-query/).

<a id="limitations-lookup"></a>

## Limitations and Considerations

- For primary key rules, see [PRIMARY KEY Policy](../primary-key-policy/).
- Measure memory scale and index cost as described in [Indexes and Performance](../index-performance/).
- Choose TAG for source time series and VOLATILE for caches that may be lost on restart.
- Follow the [SDK Append Matrix](/dbms/development-tools-integration/sdk-support-scope/#append-table-type-matrix) for Append availability.
