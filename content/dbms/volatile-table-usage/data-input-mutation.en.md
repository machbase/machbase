---
type: docs
title: '10.4 Data Input and Mutation'
weight: 40
toc: true
aliases:
  - /dbms/volatile-table-usage/on-duplicate-key-update/
---

This section provides runnable examples of `INSERT`, duplicate-key updates, and `DELETE` for VOLATILE tables.

<a id="original-85-insert-update"></a>
<a id="on-duplicate-key-update"></a>

## Inserting and Updating Data

Run the following examples in order through the final cleanup statement. To repeatedly change values
for the same key, such as current state, define a `PRIMARY KEY` and use `ON DUPLICATE KEY UPDATE`.

```sql
CREATE VOLATILE TABLE ch10_mutation (
    id         INTEGER PRIMARY KEY,
    direction  VARCHAR(10),
    refcnt     INTEGER
);

INSERT INTO ch10_mutation VALUES (1, 'west', 0);
INSERT INTO ch10_mutation VALUES (2, 'east', 0);

INSERT INTO ch10_mutation VALUES (1, 'south', 0)
ON DUPLICATE KEY UPDATE;

INSERT INTO ch10_mutation VALUES (1, 'south', 0)
ON DUPLICATE KEY UPDATE SET refcnt = 1;

SELECT * FROM ch10_mutation ORDER BY id;
```

If the key does not exist, a new row is inserted. If it exists, the statement without `SET` updates
the entire row with the input values; the statement with `SET` updates only the specified columns.
The `PRIMARY KEY` itself cannot be updated.

Bulk ingestion APIs differ by language and driver in initialization, binding, and error handling.
Use the corresponding driver example in [SDKs and Integration](/dbms/development-tools-integration/)
instead of copying incomplete snippets.

<a id="volatile-primary-key-update"></a>

## Conditional Updates

Use `UPDATE` to change selected columns of an existing row. `INSERT ... ON DUPLICATE KEY UPDATE`
inserts a missing row or updates an existing one; `UPDATE` changes values only when the target row
exists.

`UPDATE` on a VOLATILE table requires `WHERE` and supports only a `PRIMARY KEY = value` predicate,
as with conditional deletion. Predicates on other columns and compound predicates are unsupported.
Updating all rows by omitting `WHERE` is also unsupported.

```sql
UPDATE ch10_mutation SET refcnt = refcnt + 1 WHERE id = 2;
SELECT * FROM ch10_mutation ORDER BY id;
```

The `SET` clause cannot specify the `PRIMARY KEY` column. To change a key, delete the existing row
and insert it again with the new key.

<a id="original-85-deleting-data"></a>

## Deleting Data

Conditional deletion supports only a `PRIMARY KEY = value` predicate. Predicates on other columns
and compound predicates are unsupported.

```sql
DELETE FROM ch10_mutation WHERE id = 2;
SELECT * FROM ch10_mutation ORDER BY id;
DROP TABLE ch10_mutation;
```

To remove all rows while retaining the table definition, omit WHERE, as in `DELETE FROM table_name`.
To reset the schema as well, drop and recreate the table. A server restart removes only the data and
preserves the definition, so maintain a separate reload script rather than a recreation script.
