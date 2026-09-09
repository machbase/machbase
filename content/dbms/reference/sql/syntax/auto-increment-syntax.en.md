---
type: docs
title: 'AUTO_INCREMENT'
weight: 230
toc: true
aliases:
  - /dbms/rdb-table-usage/auto-increment/
---

`AUTO_INCREMENT` is a column property that instructs the server to generate values for a single
64-bit integer PRIMARY KEY.

<span class="badge-since">LOOKUP and VOLATILE supported since Machbase 8.7.0</span>

## Support Scope

| Item | Support |
|---|---|
| Edition | Standard Edition |
| Tables | TRANSACTION, LOOKUP, VOLATILE |
| Column types | `LONG`, `INT64` |
| Key | Single column-level `PRIMARY KEY` |

Table-level and composite primary keys are unsupported. Do not combine `PROPERTY(SEQUENCE)` on the
same LOOKUP column or use NEXTVAL().

```sql
CREATE TRANSACTION TABLE device_master (
    id          LONG PRIMARY KEY AUTO_INCREMENT,
    device_name VARCHAR(80),
    site_code   VARCHAR(32)
);

CREATE LOOKUP TABLE lookup_order (
    id   INT64 PRIMARY KEY AUTO_INCREMENT,
    item VARCHAR(100)
);

CREATE VOLATILE TABLE volatile_order (
    id   LONG PRIMARY KEY AUTO_INCREMENT,
    item VARCHAR(100)
);
```

TRANSACTION table DDL cannot run during an explicit transaction. COMMIT or ROLLBACK before creating
the table.

## Automatic Value Generation

Omit the automatic column or insert NULL to have the server generate a value.

```sql
INSERT INTO device_master(device_name, site_code)
VALUES ('compressor-01', 'SEOUL-A');

INSERT INTO device_master(id, device_name, site_code)
VALUES (NULL, 'pump-02', 'SEOUL-A');
```

A non-NULL value can also be specified directly. If it is at least the next automatic value,
numbering advances beyond it. Smaller values do not move numbering backward. 0 is valid. After
INT64_MAX, no more values can be generated and automatic INSERT fails.

Do not depend on number reuse after duplicate keys or failed INSERTs. These are row identifiers, not
gap-free business sequence numbers.

## Differences by Table Type

| Behavior | TRANSACTION | LOOKUP | VOLATILE |
|---|:---:|:---:|:---:|
| Rows and next automatic value survive restart | Yes | Yes | No |
| Explicit transactions | Yes | No | No |
| Automatic values in `INSERT ... SELECT` | Yes | No | No |
| Single INSERT result ROWID | Yes | Yes | Yes |

VOLATILE tables and values disappear on server restart. Only TRANSACTION data migration can use
INSERT ... SELECT with the automatic column omitted.

```sql
INSERT INTO device_master(device_name, site_code)
SELECT device_name, site_code
  FROM staging_device
 ORDER BY device_name;
```

## Checking INSERT Results

Supported SDKs can return generated identifiers from successful single INSERT ... VALUES execution
results. Batch, Append, loaders, INSERT ... SELECT, and UPSERT do not return a single value. For
conditions, see [ROWID](../../rowid/); for language APIs, see
[SDK Feature Support](/dbms/development-tools-integration/sdk-support-scope/).

## Related Documentation

- [TRANSACTION Table Structure](/dbms/rdb-table-usage/table-structure-schema/)
- [LOOKUP Table Structure](/dbms/lookup-table-usage/table-structure-schema/)
- [VOLATILE Table Structure](/dbms/volatile-table-usage/table-structure-schema/)
- [LOOKUP SEQUENCE](/dbms/lookup-table-usage/sequence-column/)
