---
type: docs
title: 'NEXTVAL Function'
weight: 60
toc: true
---

`NEXTVAL` returns the next automatic value for a LOOKUP table SEQUENCE column as `INT64`.
It can be used only in an `INSERT` value expression.

## Syntax

```sql
NEXTVAL(sequence_column)
```

- `sequence_column` must be created with `PROPERTY(SEQUENCE=...)`.
- It cannot be used outside `INSERT`, such as in SELECT or WHERE.
- Exactly one argument is required: a SEQUENCE column in the same INSERT target table.

---

## Creating a Sequence Column

SEQUENCE columns are supported on LOOKUP `LONG` or `INT64` columns.
`PROPERTY(SEQUENCE=1)` sets the starting value to 1.

```sql
CREATE LOOKUP TABLE seq_lookup (
    id   LONG PROPERTY(SEQUENCE=1) PRIMARY KEY,
    name VARCHAR(64)
);
```

---

## Using NEXTVAL

```sql
-- Insert automatic IDs with NEXTVAL
INSERT INTO seq_lookup (id, name) VALUES (NEXTVAL(id), 'sensor-a');
INSERT INTO seq_lookup (id, name) VALUES (NEXTVAL(id), 'sensor-b');
INSERT INTO seq_lookup (id, name) VALUES (NEXTVAL(id), 'sensor-c');

-- Check results
SELECT * FROM seq_lookup;
id    name
----------
1     sensor-a
2     sensor-b
3     sensor-c

DROP TABLE seq_lookup;
```

---

## Notes

- `NEXTVAL` can be used only in `INSERT`.
- SEQUENCE columns are supported only in **LOOKUP tables**. They are unavailable in TAG, LOG,
  VOLATILE, and TRANSACTION tables.
- Types other than `LONG`/`INT64`, ordinary columns, and SELECT/WHERE calls cause errors.
- Sequence values may not be reused after transaction rollback or errors, so gaps may occur.
- For DDL details, see [DDL - Sequence Column](../../syntax/).
