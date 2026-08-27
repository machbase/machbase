---
type: docs
title: '17.1.1.15 INDEX'
weight: 150
toc: true
---

<a id="create-index"></a>

## CREATE INDEX

Starting with Machbase 8.7.0, the main CREATE INDEX forms support `IF NOT EXISTS` after `INDEX`.

```sql
CREATE [UNIQUE | PRIMARY KEY] INDEX [IF NOT EXISTS] index_name
    ON index_target(index_column_list)
    [INDEX_TYPE index_type]
    [TABLESPACE tablespace_name]
    [index_properties];
```

<a id="create-index-if-not-exists"></a>

### IF NOT EXISTS

When an index with the same name already exists in the same database and owner namespace, the
statement succeeds and retains that index.

- For a new name, Machbase performs the normal table, column, index-type, property, and privilege
  validation before creating the index.
- For an existing name, Machbase does not compare or change the table, columns, index type, JSON
  path, or properties.
- The namespace is `database + owner + index name`; the same name under another database or owner is
  independent.
- Without `IF NOT EXISTS`, the existing duplicate-name error is unchanged.

{{< callout type="warning" >}}
`IF NOT EXISTS` does not reconcile index definitions. An existing name causes a no-op even when the
new target is missing or the requested definition differs. Verify the effective table, columns,
type, and properties with `SHOW INDEX` or the system catalog after an idempotent deployment.
{{< /callout >}}

```sql
CREATE LOG TABLE sensor_log_ifne (
    sensor_id INTEGER,
    value     DOUBLE
);

CREATE INDEX IF NOT EXISTS sensor_log_ifne_idx
    ON sensor_log_ifne(sensor_id);

-- The existing SENSOR_ID mapping is retained.
CREATE INDEX IF NOT EXISTS sensor_log_ifne_idx
    ON sensor_log_ifne(value);

SHOW INDEX sensor_log_ifne_idx;

DROP TABLE sensor_log_ifne;
```

The option applies to normal indexes, Standard Edition TRANSACTION `UNIQUE` and `PRIMARY KEY`
indexes, TAG data and METADATA JSON-path indexes, and the general form with `INDEX_TYPE`.

Deprecated dedicated `CREATE BITMAP INDEX`, `CREATE KEYWORD INDEX`, and `CREATE REDBLACK INDEX`
forms do not accept this option. Use the general form instead.

```sql
CREATE INDEX IF NOT EXISTS idx_message
    ON app_log(message) INDEX_TYPE KEYWORD;
```
