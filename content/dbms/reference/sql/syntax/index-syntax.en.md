---
type: docs
title: 'INDEX'
weight: 150
toc: true
---

This reference explains index syntax and support by table type. Indexes reduce query cost but
require maintenance during ingestion and changes. Add them after checking actual predicates and
execution plans.

<a id="create-index"></a>

## CREATE INDEX

<span class="badge-since">Supported since Machbase 8.7.0</span>

```sql
create_index_stmt ::=
    'CREATE' index_modifier? 'INDEX' [ 'IF NOT EXISTS' ] index_name
    'ON' index_target '(' index_column_list ')'
    [ 'INDEX_TYPE' ( 'LSM' | 'KEYWORD' | 'BITMAP' | 'REDBLACK' | 'TAG' ) ]
    [ 'TABLESPACE' tablespace_name ]
    [ index_property_list ]

index_modifier ::= 'UNIQUE' | 'PRIMARY KEY'

index_target ::= table_name | table_name 'METADATA'

index_column_list ::=
    column_name ( ',' column_name )*
  | column_name json_path

index_property_list ::=
    ( 'MAX_LEVEL'        '=' number
    | 'PAGE_SIZE'        '=' number
    | 'BITMAP_ENCODE'    '=' ( 'EQUAL' | 'RANGE' )
    | 'PART_VALUE_COUNT' '=' number )
    ( ',' index_property_list )*
```

<a id="create-index-if-not-exists"></a>

### IF NOT EXISTS

IF NOT EXISTS succeeds without error and retains the existing index if the same index name exists
for the same database and owner.

- If the name does not exist, validate table, column, index type, properties, and privileges as for ordinary CREATE INDEX, then create it.
- If the name exists, do not compare or change table, column, index type, JSON path, or properties.
- The duplicate namespace is database + owner + index name. The same name in another database or owner is a different index.
- Without the option, CREATE INDEX returns the existing duplicate-name error.

{{< callout type="warning" >}}
IF NOT EXISTS does not reconcile index definitions. An existing name makes the statement a
successful no-op even if its target table/column is absent or its definition differs. After repeated
deployment, verify actual tables, columns, types, and properties with SHOW INDEX or the system
catalog.
{{< /callout >}}

```sql
CREATE LOG TABLE sensor_log_ifne (
    sensor_id INTEGER,
    value     DOUBLE
);

CREATE INDEX IF NOT EXISTS sensor_log_ifne_idx
    ON sensor_log_ifne(sensor_id);

-- Existing name: succeeds and retains the original SENSOR_ID mapping.
CREATE INDEX IF NOT EXISTS sensor_log_ifne_idx
    ON sensor_log_ifne(value);

SHOW INDEX sensor_log_ifne_idx;

DROP TABLE sensor_log_ifne;
```

### Supported Conditional Creation Forms

| Form | Support |
|---|---|
| Ordinary CREATE INDEX IF NOT EXISTS | Ordinary indexes supported by the table type |
| CREATE UNIQUE INDEX IF NOT EXISTS | Standard Edition TRANSACTION |
| CREATE PRIMARY KEY INDEX IF NOT EXISTS | Standard Edition TRANSACTION |
| TAG data JSON path / TAG METADATA index | Standard and Cluster Editions |
| INDEX_TYPE in ordinary syntax | Existing table/index-type support |

Deprecated CREATE BITMAP INDEX, CREATE KEYWORD INDEX, and CREATE REDBLACK INDEX forms do not accept
IF NOT EXISTS. Use ordinary syntax.

```sql
CREATE INDEX IF NOT EXISTS idx_message
    ON app_log(message) INDEX_TYPE KEYWORD;
```

## Support by Table Type

| Table type | Indexes | Main uses |
|------------|--------|-----------|
| LOG | LSM, KEYWORD, BITMAP | Range queries, text search, analytical predicates |
| TAG | TAG/KV secondary, JSON path | Value-column and JSON-member predicates |
| TAG METADATA | Automatic column indexes, JSON path | Tag-attribute predicates |
| TRANSACTION | PRIMARY KEY, UNIQUE, ordinary BTREE | Relational keys and composite predicates |
| VOLATILE | REDBLACK | In-memory key/predicate queries |
| LOOKUP | REDBLACK | In-memory key/predicate queries |

The default internal index depends on table type. Specifying an index type from another table type
does not necessarily create the same structure.

## LOG Indexes

```sql
CREATE INDEX idx_ts ON sensor_log (ts);
CREATE INDEX idx_msg ON app_log (message) INDEX_TYPE KEYWORD;
CREATE INDEX idx_status ON sensor_log (status)
    INDEX_TYPE BITMAP BITMAP_ENCODE = RANGE;
```

| Type | Targets and characteristics |
|------|-------------|
| LSM | Default LOG range index |
| KEYWORD | SEARCH/ESEARCH on VARCHAR/TEXT |
| BITMAP | Repeated-value analysis; not for VARCHAR, TEXT, or BINARY |

Choose properties such as LSM MAX_LEVEL/PAGE_SIZE and BITMAP BITMAP_ENCODE through measurements of
data distribution and query predicates.

## TAG Indexes

Default access structures for TAG names and the time axis are managed automatically. Consider TAG/KV
secondary indexes when value columns are frequently used as standalone predicates.

```sql
CREATE INDEX idx_value ON sensor_tag (value) INDEX_TYPE TAG;
```

JSON value columns support indexes by path.

```sql
CREATE INDEX idx_sensor ON tag_json (value.sensor.name);
CREATE INDEX idx_metric ON tag_json (value->'$.metric');
CREATE INDEX idx_item ON tag_json (value.items[0]."product-id");
```

Ordinary TAG METADATA columns are indexed automatically. Use the following form to add a path from a
METADATA JSON column.

```sql
CREATE INDEX idx_ship_owner
ON ships METADATA (info->'$.owner');
```

For support scope and execution-plan examples, see
[TAG Indexes and Performance](/dbms/tag-table-usage/index-performance/).

## TRANSACTION Indexes

TRANSACTION supports PRIMARY KEY, UNIQUE INDEX, and ordinary single/composite indexes.

```sql
CREATE PRIMARY KEY INDEX idx_pk_order ON orders (order_id);
CREATE UNIQUE INDEX uidx_account_email ON account (email);
CREATE UNIQUE INDEX uidx_tenant_login ON account (tenant_id, login_name);
CREATE INDEX idx_category_name ON product (category, product_name);
```

A table permits one single-column PRIMARY KEY. CREATE UNIQUE INDEX supports composite columns;
NULL-containing keys are not duplicates of other NULL-containing keys. See
[TRANSACTION Indexes and Performance](/dbms/rdb-table-usage/index-performance/).

## VOLATILE and LOOKUP Indexes

VOLATILE and LOOKUP use REDBLACK in-memory indexes.

```sql
CREATE INDEX idx_status ON device_status (status) INDEX_TYPE REDBLACK;
```

For primary key and secondary-index design by type, see:

- [VOLATILE Indexes and Performance](/dbms/volatile-table-usage/index-performance/)
- [LOOKUP Indexes and Performance](/dbms/lookup-table-usage/index-performance/)

<a id="drop-index"></a>

## DROP INDEX

```sql
drop_index_stmt ::= 'DROP INDEX' index_name
```

```sql
DROP INDEX idx_status;
```

Deletion can fail while sessions use the target index. Check execution plans and production queries
using it before dropping it.

## Related Documentation

- [SEARCH / ESEARCH / REGEXP](../search-esearch-regexp-syntax/)
- [Query Performance Tuning](/dbms/performance-tuning/performance-query-tuning/)
