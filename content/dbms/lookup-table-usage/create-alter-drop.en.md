---
type: docs
title: '9.3 Create, Alter, and Drop'
weight: 30
toc: true
---
This section explains how to create, alter, and drop LOOKUP tables.


<a id="original-85-creating-lookup-tables"></a>

## Creating and Managing LOOKUP Tables

Create a reference table as follows. A LOOKUP table must specify a `PRIMARY KEY`.

<a id="create-lookup-table"></a>

## Creating a LOOKUP Table

```sql
CREATE LOOKUP TABLE ch9_ddl (id INTEGER PRIMARY KEY, name VARCHAR(20));
```

Use meaningful column names for reference data used in production.

```sql
CREATE LOOKUP TABLE ch9_ddl_equip (
    equip_id   LONG PRIMARY KEY,
    equip_name VARCHAR(128),
    location   VARCHAR(64),
    status     VARCHAR(16),
    updated_at DATETIME
);
```

The `PRIMARY KEY` uniquely identifies rows and provides a basis for UPDATE, DELETE, and JOIN. If the
business key combines several columns, encode that combination in a separate key column or use a
SEQUENCE-based surrogate key.

```sql
CREATE LOOKUP TABLE ch9_ddl_price (
    price_key  VARCHAR(64) PRIMARY KEY,
    product_id VARCHAR(32),
    region     VARCHAR(16),
    price      DOUBLE
);
```

<a id="create-lookup-auto-increment"></a>

## AUTO_INCREMENT PRIMARY KEY

To have the server generate a numeric PRIMARY KEY, specify `AUTO_INCREMENT` on a single `LONG` or
`INT64` column.

```sql
CREATE LOOKUP TABLE ch9_ddl_registry (
    equip_id   LONG PRIMARY KEY AUTO_INCREMENT,
    equip_name VARCHAR(128),
    location   VARCHAR(64)
);

INSERT INTO ch9_ddl_registry(equip_name, location)
VALUES ('compressor-01', 'SEOUL-A');
```

The server generates a value when the primary key column is omitted or set to NULL. A single
`INSERT ... VALUES` can also specify a primary key in `0..INT64_MAX`. If the specified value is at
least the next automatic value, the next value advances to `specified value + 1`. Smaller values do
not move it backward. Data and the next automatic value survive a normal restart.

LOOKUP tables with AUTO_INCREMENT do not support `INSERT ... SELECT` or `ON DUPLICATE KEY UPDATE`.
For obtaining inserted IDs through an SDK, see
[ROWID and INSERT Result IDs](/dbms/reference/sql/rowid/).

<a id="create-lookup-sequence"></a>

## Using a SEQUENCE Column

For automatic numbering, use a `LONG PROPERTY(SEQUENCE=1)` column. Obtain the next value with
`NEXTVAL()` during insertion.

```sql
CREATE LOOKUP TABLE ch9_ddl_alarm (
    seq         LONG PROPERTY(SEQUENCE=1) PRIMARY KEY,
    sensor_id   VARCHAR(64),
    alarm_type  VARCHAR(32),
    occurred_at DATETIME,
    message     VARCHAR(256)
);

INSERT INTO ch9_ddl_alarm
VALUES (NEXTVAL(seq), 'TEMP-01', 'HIGH', NOW, '온도 초과');
```

For detailed policies, see [SEQUENCE Columns](/dbms/lookup-table-usage/sequence-column/).
`PROPERTY(SEQUENCE)` and `AUTO_INCREMENT` are separate features and must not be specified together
on one column.

<a id="alter-lookup-column"></a>

## Adding and Dropping Columns

In Standard Edition, you can add and drop fixed-length numeric ARRAY columns in LOOKUP tables.

```sql
ALTER TABLE ch9_ddl_equip
    ADD COLUMN (limits DECIMAL(12,4)[2] DEFAULT [0.0000, NULL]);

ALTER TABLE ch9_ddl_equip
    DROP COLUMN (limits);
```

Without DEFAULT, the new ARRAY column is a whole-array NULL in existing rows. With DEFAULT, existing
rows also receive that value. The ARRAY DEFAULT must contain exactly the declared number of
elements. ARRAY columns cannot be PRIMARY KEY or index keys.

For supported types and limitations, see [Numeric ARRAY Types](/dbms/reference/sql/types/array/).

<a id="alter-lookup-index"></a>

## Adding Indexes

Add indexes to columns frequently queried or used in JOIN predicates.

```sql
CREATE INDEX ch9_ddl_loc_idx ON ch9_ddl_equip(location);
CREATE INDEX ch9_ddl_status_idx   ON ch9_ddl_equip(status);
```

A default index is created on the PRIMARY KEY column; do not add a duplicate index on it. More
indexes increase insertion and update costs. Add them only for columns with clear query predicates.

<a id="delete-lookup-data"></a>

## Deleting Data and Dropping Tables

Use `DELETE` to remove rows. A primary key predicate is the clearest approach for a single-row deletion.

```sql
DELETE FROM ch9_ddl_equip
WHERE equip_id = 1001;
```

Bulk deletion can use general predicates. For production data, first check the target count with the
same predicate.

```sql
SELECT COUNT(*)
FROM ch9_ddl_equip
WHERE status = 'RETIRED';

DELETE FROM ch9_ddl_equip
WHERE status = 'RETIRED';
```

Use `DROP TABLE` to remove the table itself.

```sql
DROP TABLE ch9_ddl_alarm;
DROP TABLE ch9_ddl_registry;
DROP TABLE ch9_ddl_price;
DROP TABLE ch9_ddl_equip;
DROP TABLE ch9_ddl;
```

`DROP TABLE` removes both the definition and data. Back up or export data first when needed.

<a id="create-lookup-limitations"></a>

## Considerations

- A `PRIMARY KEY` is required for LOOKUP tables.
- Only one column can be designated as the `PRIMARY KEY`.
- To change a `PRIMARY KEY` value, delete the existing row and insert it with the new key.
- Consider TRANSACTION tables when reference data grows or query/update patterns become complex.
