---
type: docs
title: '9.13 Predicate UPDATE/DELETE'
weight: 130
toc: true
aliases:
  - /dbms/lookup-table-usage/privilege-predicate-performance/
---

LOOKUP tables can update or delete multiple rows using general predicates as well as primary keys.
Check the target row count with the same predicate before making changes.

This exercise uses one table, which is cleaned up at the end.

```sql
CREATE LOOKUP TABLE ch9_predicate (
    equip_id VARCHAR(32) PRIMARY KEY,
    site     VARCHAR(16),
    status   VARCHAR(16),
    score    INTEGER
);

INSERT INTO ch9_predicate VALUES ('EQ-01', 'SEOUL', 'READY',   10);
INSERT INTO ch9_predicate VALUES ('EQ-02', 'SEOUL', 'READY',   20);
INSERT INTO ch9_predicate VALUES ('EQ-03', 'SEOUL', 'RETIRED', 30);
INSERT INTO ch9_predicate VALUES ('EQ-04', 'BUSAN', 'READY',   40);
```

<a id="condition-lookup-update"></a>

## UPDATE

All matching rows are updated. `SET` expressions can reference current row values, but the primary
key column itself cannot be changed.

LOOKUP UPDATE requires `WHERE`. Specify a supported predicate even when updating every row. This
differs from DELETE, which permits deleting all rows without WHERE.

```sql
-- Count affected rows before the change.
SELECT COUNT(*) FROM ch9_predicate
 WHERE site = 'SEOUL' AND status = 'READY';

UPDATE ch9_predicate
   SET status = 'ACTIVE', score = score + 10
 WHERE site = 'SEOUL' AND status = 'READY';

SELECT equip_id, site, status, score FROM ch9_predicate ORDER BY equip_id;
```

COUNT is 2. Only EQ-01 and EQ-02 become `ACTIVE`, with scores of 20 and 30. EQ-03 remains unchanged
because its status differs, despite being in SEOUL; EQ-04 remains unchanged because its site
differs, despite being READY.

<a id="condition-lookup-delete"></a>

## DELETE

All matching rows are deleted. Omitting `WHERE` deletes every row in the table.

```sql
SELECT COUNT(*) FROM ch9_predicate WHERE status = 'RETIRED';

DELETE FROM ch9_predicate WHERE status = 'RETIRED';

SELECT equip_id, status FROM ch9_predicate ORDER BY equip_id;
```

COUNT is 1. EQ-03 is deleted, leaving three rows.

<a id="design-condition-lookup-update-delete"></a>

## Predicate Design Guidelines

1. Use primary key predicates for single-row changes.
2. Check the impact scope with `SELECT COUNT(*)` using the same predicate before bulk changes.
3. Consider extracting frequently filtered JSON values into ordinary indexed columns.
4. To change a primary key, delete the existing row and insert it with the new key.

Check the SQL reference for the precise scope of supported operators and JSON predicates.

- [LOOKUP predicate UPDATE](/dbms/reference/sql/syntax/dml-syntax/lookup-predicate-update-syntax/)
- [LOOKUP predicate DELETE](/dbms/reference/sql/syntax/dml-syntax/lookup-predicate-delete-syntax/)

## Permissions and Performance

UPDATE and DELETE require the respective `UPDATE` and `DELETE` privileges on the target table. Grant
`SELECT` only if the application itself reads before/after values. Use
[Privilege Management](/dbms/security-access-control/privileges/) as the authoritative reference for
privilege SQL.

Primary key equality directly locates one row; general predicates evaluate conditions to collect
target rows. Use prepared statements and binding for repeated single-row changes. For bulk changes,
measure the row count and execution time for the same predicate in a validation environment.


```sql
DROP TABLE ch9_predicate;
```
