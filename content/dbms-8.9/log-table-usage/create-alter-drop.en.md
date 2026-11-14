---
type: docs
title: '7.3 Create, Alter, and Drop'
weight: 30
toc: true
---

Adding a column takes little SQL, but production changes also require checking which values appear
in existing rows and whether existing ingestion programs continue to work. This section changes a
schema with data already present and checks the results.

<a id="original-85-creating-log-tables"></a>

<a id="log라고-명시해서-만듭니다"></a>

## Creating a LOG Table

`CREATE TABLE` without a table type creates a TRANSACTION table. Use `CREATE LOG TABLE` in this exercise.

```sql
CREATE LOG TABLE ch7_ddl (
    event_id INTEGER,
    category VARCHAR(32),
    severity SHORT,
    message  VARCHAR(128)
);
INSERT INTO ch7_ddl VALUES (1, 'network', 3, 'connection timeout');
```

<a id="create-log-schema-rules"></a>

Do not redeclare the automatic `_arrival_time` column in DDL. Use a separate DATETIME column for
actual event time. LOG does not support PRIMARY KEY or UNIQUE constraints.

<a id="alter-log-table"></a>

<a id="기존-행에서-새-컬럼-값을-확인합니다"></a>

## Adding Columns and Defaults

```sql
ALTER TABLE ch7_ddl ADD COLUMN (host_name VARCHAR(64));
ALTER TABLE ch7_ddl ADD COLUMN (source_kind VARCHAR(16) DEFAULT 'agent');
ALTER TABLE ch7_ddl ADD COLUMN (channels INT32[3] DEFAULT [1, NULL, 3]);

SELECT event_id, host_name, source_kind, channels
  FROM ch7_ddl
 ORDER BY event_id;
```

For existing row 1, `host_name` is NULL, `source_kind` is `agent`, and `channels` is `[1, NULL, 3]`.
This shows the difference between columns with and without DEFAULT. An ARRAY DEFAULT must have the
same number of elements as the declared length.

Next, rename a column and increase its string length.

```sql
ALTER TABLE ch7_ddl RENAME COLUMN category TO event_category;
ALTER TABLE ch7_ddl MODIFY COLUMN (message VARCHAR(4096));
ALTER TABLE ch7_ddl MODIFY COLUMN severity SET MINMAX_CACHE_SIZE = 1048576;

SELECT event_id, event_category, severity, message FROM ch7_ddl;
```

Existing values are retained. After renaming, queries must also use `event_category`. The MINMAX
example specifies 1 MiB for a numeric column; this is not a recommended value for every table.

Be careful with type changes. Extending a VARCHAR length does not convert TEXT to VARCHAR.
`MINMAX_CACHE_SIZE` also cannot be set on variable-length columns such as VARCHAR or TEXT.

<a id="not-null은-기존-데이터-검사도-포함합니다"></a>

## NOT NULL and Existing Data

Because `event_category` currently contains a value, the following change is allowed.

```sql
ALTER TABLE ch7_ddl MODIFY COLUMN event_category NOT NULL;
ALTER TABLE ch7_ddl MODIFY COLUMN event_category NULL;
```

`NOT NULL` without an option checks existing rows. It cannot be applied to `host_name`, which
contains NULL. Run the following SQL separately only if you want to verify the failure.

```sql
-- Expected failure: host_name is NULL in an existing row.
ALTER TABLE ch7_ddl MODIFY COLUMN host_name NOT NULL;
```

`NOT NULL NOCHECK` skips the check for existing NULL values. It neither fills existing NULL values
nor guarantees that historical data satisfies the constraint. The normal exercise does not use it.

<a id="alter-log-limitations"></a>

<a id="컬럼을-지울-때는-인덱스부터-확인합니다"></a>

## Dropping Indexes and Columns

```sql
CREATE INDEX ch7_ddl_host_idx ON ch7_ddl(host_name) INDEX_TYPE LSM;
DROP INDEX ch7_ddl_host_idx;
ALTER TABLE ch7_ddl DROP COLUMN (host_name);
ALTER TABLE ch7_ddl DROP COLUMN (source_kind);
ALTER TABLE ch7_ddl DROP COLUMN (channels);

SELECT event_id, event_category, severity, message FROM ch7_ddl;
```

Drop an index before dropping a column it references. Internal columns `_ARRIVAL_TIME` and `_RID`
cannot be dropped, renamed, or have their attributes changed. At least one user column must remain.
A VARCHAR length can only be increased and must not exceed 32,767 bytes.

<a id="delete-log-table-definition"></a>

<a id="데이터를-비우는-것과-정의를-없애는-것은-다릅니다"></a>

## Deleting Data and Dropping Tables

Caution: the following commands remove example data. LOG data cannot be recovered with a TRANSACTION
table `ROLLBACK`.

```sql
TRUNCATE TABLE ch7_ddl;
SELECT COUNT(*) AS remaining_rows FROM ch7_ddl;
DROP TABLE ch7_ddl;
```

After TRUNCATE, the count is 0 and the definition remains. The final DROP also removes the
definition. To remove only older data, use [Retention Deletion](../operations-lifecycle/).

<a id="create-log-checklist"></a>

<a id="운영-적용은-입력-프로그램과-함께-준비하세요"></a>

## Operational DDL Considerations

Before a change, coordinate ingestion and DDL timing. Afterward, check column names, order, and
types in SQL, Appenders, and file mappings. If a resource-in-use error occurs, check which jobs use
the table before retrying.

If the failing change is unclear, collect the original DDL and the SQL that failed. Together they
help narrow down the cause.
